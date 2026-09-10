import unittest,tempfile,os,sqlite3
import numpy as np
from cryptography.exceptions import InvalidTag
from ultrasonic_v2 import seal,Receiver,modulate,demodulate,benchmark
class Channel(unittest.TestCase):
 def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.key=os.urandom(32); self.path=self.tmp.name+'/ledger'; self.receiver=Receiver(self.key,self.path)
 def tearDown(self): self.receiver.close(); self.tmp.cleanup()
 def test_roundtrip(self): self.assertEqual(self.receiver.receive(demodulate(modulate(seal(self.key,{'command':'inert'})))),{'command':'inert'})
 def test_tamper(self):
  frame=seal(self.key,{})
  with self.assertRaises(InvalidTag): self.receiver.receive(frame[:-1]+bytes([frame[-1]^1]))
 def test_wrong_key(self):
  with self.assertRaises(InvalidTag): self.receiver.receive(seal(os.urandom(32),{}))
 def test_replay_restart(self):
  f=seal(self.key,{}); self.receiver.receive(f); self.receiver.close(); self.receiver=Receiver(self.key,self.path)
  with self.assertRaises(sqlite3.IntegrityError): self.receiver.receive(f)
 def test_shared_ledger(self):
  f=seal(self.key,{}); other=Receiver(self.key,self.path); self.receiver.receive(f)
  with self.assertRaises(sqlite3.IntegrityError): other.receive(f)
  other.close()
 def test_bad_auth_no_ledger(self):
  f=seal(self.key,{})
  with self.assertRaises(InvalidTag): self.receiver.receive(f[:-1]+bytes([f[-1]^1]))
  self.assertEqual(self.receiver.receive(f),{})
 def test_size(self):
  with self.assertRaises(ValueError): seal(self.key,{'x':'x'*1024})
 def test_nonfinite(self):
  with self.assertRaises(ValueError): seal(self.key,{'x':float('nan')})
 def test_sample_bound(self):
  for x in ([],[0],np.full(768,float('nan'))):
   with self.assertRaises(ValueError): demodulate(x)
 def test_private_ledger(self): self.assertEqual(os.stat(self.path).st_mode&0o777,0o600)
 def test_simulation_repeatable(self): self.assertEqual(benchmark(),benchmark())
 def test_clean_bits(self):
  data=bytes(range(256)); self.assertEqual(demodulate(modulate(data)),data)
