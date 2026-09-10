import json,sys,tempfile,os
from . import seal,Receiver,benchmark,modulate,demodulate

def fixture():
    key=os.urandom(32); frame=seal(key,{'message':'inert fixture'})
    with tempfile.TemporaryDirectory() as directory:
        receiver=Receiver(key,directory+'/replay.sqlite')
        result=receiver.receive(demodulate(modulate(frame))); receiver.close()
    return {'verified':result=={'message':'inert fixture'},'frame_bytes':len(frame),'production_keys_used':False}
if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ('fixture','benchmark'): sys.exit(2)
    print(json.dumps(fixture() if sys.argv[1]=='fixture' else benchmark()))
