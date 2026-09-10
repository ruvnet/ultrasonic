"""Authenticated inert records and simulated aligned FSK. No execution or audio I/O."""
import hashlib,json,os,sqlite3,time
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
AAD=b'ruvnet/ultrasonic/v2/inert-record'
MAX_PAYLOAD=1024

def seal(key,record):
    if not isinstance(key,bytes) or len(key)!=32: raise ValueError('256 bit key required')
    if type(record) is not dict: raise ValueError('object required')
    raw=json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    if len(raw)>MAX_PAYLOAD: raise ValueError('payload too large')
    nonce=os.urandom(12)
    return b'UV2'+nonce+AESGCM(key).encrypt(nonce,raw,AAD)

class Receiver:
    def __init__(self,key,path):
        if len(key)!=32: raise ValueError('256 bit key required')
        self.key=key
        fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600); os.close(fd)
        if os.stat(path).st_mode & 0o077: raise ValueError('private database required')
        self.db=sqlite3.connect(path,timeout=5)
        self.db.execute('CREATE TABLE IF NOT EXISTS seen (digest TEXT PRIMARY KEY)'); self.db.commit()
    def receive(self,frame):
        if not isinstance(frame,bytes) or not 31<=len(frame)<=MAX_PAYLOAD+31 or frame[:3]!=b'UV2': raise ValueError('invalid frame')
        raw=AESGCM(self.key).decrypt(frame[3:15],frame[15:],AAD)
        record=json.loads(raw)
        if type(record) is not dict: raise ValueError('invalid record')
        digest=hashlib.sha256(frame).hexdigest()
        # One transaction serializes capacity and permanent replay tracking.
        try:
            self.db.execute('BEGIN IMMEDIATE')
            if self.db.execute('SELECT COUNT(*) FROM seen').fetchone()[0]>=100000: raise ValueError('ledger capacity reached; rotate key and ledger together')
            self.db.execute('INSERT INTO seen VALUES (?)',(digest,)); self.db.commit()
        except Exception:
            self.db.rollback(); raise
        return record
    def close(self): self.db.close()

def modulate(data):
    if not isinstance(data,bytes) or not 1<=len(data)<=MAX_PAYLOAD+31: raise ValueError('invalid data')
    bits=np.unpackbits(np.frombuffer(data,dtype=np.uint8))
    t=np.arange(96)/48000
    return np.sin(2*np.pi*(18000+bits[:,None].astype(np.float64)*1000)*t).reshape(-1)

def demodulate(samples):
    signal=np.asarray(samples,dtype=np.float64)
    if signal.ndim!=1 or len(signal)==0 or len(signal)%(96*8) or len(signal)>(MAX_PAYLOAD+31)*8*96 or not np.all(np.isfinite(signal)): raise ValueError('invalid samples')
    blocks=signal.reshape(-1,96); t=np.arange(96)/48000
    # Phase independent quadrature energy, vectorized across symbols.
    energies=[(blocks@np.sin(2*np.pi*f*t))**2+(blocks@np.cos(2*np.pi*f*t))**2 for f in (18000,19000)]
    return np.packbits(energies[1]>energies[0]).tobytes()

def benchmark():
    rng=np.random.default_rng(42); payload=rng.integers(0,256,128,dtype=np.uint8).tobytes(); signal=modulate(payload); results=[]
    for snr in (20,5,-5,-15):
        noise=rng.normal(0,np.sqrt(.5/10**(snr/10)),signal.shape); recovered=demodulate(signal+noise)
        errors=int(np.unpackbits(np.bitwise_xor(np.frombuffer(payload,dtype=np.uint8),np.frombuffer(recovered,dtype=np.uint8))).sum())
        results.append({'snr_db':snr,'bit_errors':errors,'bits':1024})
    return {'seed':42,'sample_rate':48000,'raw_bps':500,'results':results,'scope':'aligned numerical simulation only; no hardware, synchronization or channel acquisition validation'}
