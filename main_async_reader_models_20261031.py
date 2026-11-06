import random
import struct
from itertools import product

MASK=0xFFFFFFFF
ERROR=0x020EDEC8
DEFAULT=0x020EDECC
CONTEXT=0x02301000
DATA=0x02302000
INIT=0x0200BD04
OPEN=0x0200BFE4
SEEK=0x0200C190
READ=0x0200C170


def put(data,offset,value):struct.pack_into('<I',data,offset,value&MASK)


def recipes():
    pairs=[(0,0),(0,1),(8,0),(0,0xFFFFFFFF),(0xFFFFFFFF,0),(0x80000000,0x7FFFFFFF),(0x7FFFFFFF,0x80000000),(0xFFFFFFFF,0xFFFFFFFF)]
    outcomes=[(0,0),(1,0),(1,1),(0x80000000,0xFFFFFFFF)]
    for tag,(default,busy,flags,length,offset,outcome)in enumerate(product([False,True],[0,1,255],[0,1,2,0x80000000,MASK],[0,1,MASK,0x80000000],[0,1,MASK],outcomes)):
        start,end=pairs[tag%len(pairs)]
        yield dict(tag=tag,default=default,busy=busy,flags=flags,length=length,offset=offset,opened=outcome[0],read=outcome[1],start=start,end=end,path=[0,1,0x80000000,MASK][tag%4],buffer=DATA+tag%16)


def construct(case):
    rng=random.Random(0xA954000+case['tag']);initial=bytearray(rng.randbytes(84));initial[0]=case['busy'];put(initial,0x18,case['flags'])
    old_error=rng.getrandbits(32);context=DEFAULT if case['default']else CONTEXT;file=context+12
    output=bytearray(initial);events=[];initialized=None;result=0
    if case['busy']:error=5
    elif case['flags']&1:error=4
    else:
        local=bytearray(output[12:])
        for offset,value in [(0,0),(4,0),(8,0),(12,0),(16,14),(24,0),(28,0)]:put(local,offset,value)
        initialized=bytes(local);output[12:]=local
        def service(address,args,value):
            after=bytearray(rng.randbytes(72));put(after,36,case['start']);put(after,40,case['end'])
            event=dict(address=address,args=args,result=value,fileBefore=bytes(output[12:]),fileAfter=bytes(after),
                errorBefore=events[-1]['errorAfter']if events else old_error,errorAfter=rng.getrandbits(32))
            events.append(event);output[12:]=after
        service(OPEN,[file,case['path']],case['opened'])
        if not case['opened']:error=1
        else:
            size=case['length']or((case['end']-case['start'])&MASK)
            if case['offset']:
                service(SEEK,[file,case['offset'],0],rng.getrandbits(32))
                put(output,0x30,rng.getrandbits(32));put(output,0x34,rng.getrandbits(32));events[-1]['fileAfter']=bytes(output[12:])
            service(READ,[file,case['buffer'],size],case['read'])
            if not case['read']:error=2
            else:put(output,4,size);put(output,8,case['buffer']);output[0]=1;error=0;result=1
    return dict(initial=bytes(initial),oldError=old_error,context=context,file=file,initialized=initialized,events=events,output=bytes(output),error=error,result=result)
