import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

G,GD,NAT,TAIL=0x21d2bc4,0x20e172c,0x21d2bf0,0x21d2c70
SP,STOP,MAGIC,CB=0x2701000,0x27e0000,0,0x27e0100
ARITY={0x20a8ef8:0,0x20b6334:2,0x20b633c:1,0x20a8b6c:1,CB:55}


def dynamic_callbacks(v):return{CB:dict(mode=v.get('mode','thumb'),kind='function',fixtureOnly=True,runtimeTargetNamespaceUnresolved=True)}


def initial(address,v):
    if address!=0x20b6aa8:raise ValueError('Caller outside fourteenth scope')
    payload=bytes((i*17+v.get('payloadSeed',7))&255 for i in range(216));memory=Memory({G:bytes(32),GD:bytes(12),NAT:payload,SP-0x1000:bytes(0x1000)})
    put(memory,G+8,0x55667788);put(memory,G+12,CB|(1 if v.get('mode','thumb')=='thumb'else 0));put(memory,G+16,v['start'])
    put(memory,GD,6);put(memory,GD+4,v.get('ert',11));put(memory,GD+8,v.get('mapping',10));put(memory,NAT+140,3);put(memory,NAT+144,4)
    return memory,[v['socket']]


def effect(target,args,memory,v):
    a=[x&0xffffffff for x in args];result=0x12345678;normalized=a[:]
    if target==0x20a8ef8:result=v['now']
    elif target==0x20b6334:
        if a[1]!=NAT:raise ValueError('Natify caller must forward original full object base')
        if v.get('thinkMutation'):put(memory,NAT,0x87654321)
        result=v.get('active',0)
    elif target==0x20b633c:
        if a[0]!=NAT:raise ValueError('Determine caller must forward original full object base')
        put(memory,NAT+140,v.get('beforeType',6));put(memory,NAT+144,v.get('beforeScheme',4));result=v.get('success',1)
    elif target==CB:
        payload=struct.pack('<'+'I'*54,*a[1:]);normalized=[a[0],payload.hex()]
        put(memory,NAT+140,v.get('afterType',0x11223344));put(memory,NAT+144,v.get('afterScheme',0x89abcdef));put(memory,NAT,0xaabbccdd)
        if v.get('callbackPorts')is not None:
            mapping,ert=v['callbackPorts'];put(memory,GD+8,mapping);put(memory,GD+4,ert)
    elif target==0x20a8b6c:
        if v.get('closeOther')and a[0]==word(memory,GD+8):put(memory,GD+4,0xffffffff)
    else:raise ValueError(('Unqualified status caller contract',hex(target)))
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];active=1
    def call(target,*arguments):
        result,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return result
    socket=args[0]&0xffffffff
    if socket!=0xffffffff:
        elapsed=(call(0x20a8ef8)-word(memory,G+16))&0xffffffff
        active=call(0x20b6334,socket,NAT)if elapsed<10000 else 0
        if active==0:
            success=call(0x20b633c,NAT);snapshot=list(struct.unpack('<'+'I'*54,memory.read(NAT,216)));call(CB,success,*snapshot)
            put(memory,GD,word(memory,TAIL+12));put(memory,G+8,word(memory,TAIL+16))
            if word(memory,GD+8)!=0xffffffff:call(0x20a8b6c,word(memory,GD+8))
            put(memory,GD+8,0xffffffff)
            if word(memory,GD+4)!=0xffffffff:call(0x20a8b6c,word(memory,GD+4))
            put(memory,GD+4,0xffffffff)
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'word',active


def cases(address):
    if address!=0x20b6aa8:raise ValueError('No status caller vectors')
    ports=[(-1,-1),(-1,11),(10,-1),(10,11)]
    vectors=[dict(socket=s,start=start,now=(start+age)&0xffffffff,active=active,mode=mode,mapping=mapping,ert=ert)for s in [0,7]for start in [0,0xfffffff0]for age in [0,9999,10000,10001]for active in [0,1,0x80000000]for mode in ['arm','thumb']for mapping,ert in ports]
    vectors +=[dict(socket=-1,start=0,now=10000,mode=mode,mapping=mapping,ert=ert)for mode in ['arm','thumb']for mapping,ert in ports]
    vectors +=[dict(socket=7,start=0,now=10000,success=success,callbackPorts=ports,closeOther=close,mode=mode,thinkMutation=True,payloadSeed=39)for success in [0,1,0x80000000]for ports in [(-1,-1),(-1,12),(13,-1),(13,12)]for close in [False,True]for mode in ['arm','thumb']]
    return vectors
