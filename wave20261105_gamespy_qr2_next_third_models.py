import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,half,put,signed

C,C2,S,A,P,P2,T=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700e00,0x20e1714
DIV=0x2026350
ARITY={DIV:2,0x20a8a3c:2,0x20a8640:1,0x20a8644:2,0x20a8720:2,0x20a89f0:2,0x20b4228:2,0x20b5cd0:1,0x20b4540:1,0x20b3be4:1,0x20b5b4c:1}


def initial(address,v):
    regions={C:bytes(160),C2:bytes(160),S:bytes(76),A:bytes(16),P:bytes(16),P2:bytes(16),T:bytes(16),SP-0x1000:bytes(0x1000)}
    memory=Memory(regions)
    for record,ip,port in [(C,v.get('ip',0),v.get('port',0)),(C2,v.get('ip2',0),v.get('port2',0))]:
        for offset,value in [(0,ip),(8,S),(12,v.get('state',0)),(20,v.get('free',0)),(36,v.get('callback',0))]:put(memory,record+offset,value)
        put(memory,record+4,port,2)
    put(memory,S+12,A+0x100);put(memory,S+16,A);put(memory,S+24,v.get('error',0))
    put(memory,P,C);put(memory,P2,C2);put(memory,T,v.get('now',0));put(memory,T+4,v.get('lookupValue',C2))
    for index in range(4):put(memory,A+index*4,C if index==v.get('match',-1) else C2)
    args={0x20b5970:[P,v.get('buckets',32)],0x20b5984:[P,P2],0x20b59ac:[S,v.get('ip',0),v.get('port',0)],0x20b5cd0:[C],0x20b5e8c:[P,T],0x20b5f14:[S]}
    return memory,args[address]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];normalized=a[:];result=v.get('helper',1)
    if target==DIV:
        if not a[1]:raise ValueError('Unsigned division by zero is outside the C caller model')
        result=a[0]//a[1]
    elif target==0x20a8a3c:
        record=word(memory,a[1]);normalized=[a[0],word(memory,record),half(memory,record+4)];result=T+4 if v.get('found',1) else 0
    elif target==0x20a8640:result=v.get('count',3)
    elif target==0x20a8644:result=A+4*a[1]
    elif target==0x20a89f0:normalized=[a[0],word(memory,a[1])]
    elif target==0x20b4228:
        put(memory,C+12,v.get('afterState',v.get('state',0)));put(memory,C+20,v.get('afterFree',v.get('free',0)));put(memory,C+36,v.get('afterCallback',v.get('callback',0)))
    elif target in [0x20b4540,0x20b3be4,0x20b5b4c]:normalized=[a[0],word(memory,S+24)]
    elif target in [0x20a8720,0x20b5cd0]:pass
    else:raise ValueError('Unqualified third-packet supplied SDK contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];contract='word';result=1
    def call(target,*arguments):
        returned,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return returned
    if address==0x20b5970:
        numerator=(word(memory,C)*half(memory,C+4))&0xffffffff;denominator=args[1]&0xffffffff;call(DIV,numerator,denominator);result=numerator%denominator
    elif address==0x20b5984:
        ip1,ip2=word(memory,C),word(memory,C2)
        if ip1!=ip2:result=(ip1-ip2)&0xffffffff
        else:
            difference=(half(memory,C+4)-half(memory,C2+4))&65535;result=difference if difference<32768 else difference-65536
    elif address==0x20b59ac:
        put(memory,TMP,args[1]);put(memory,TMP+4,args[2],2);put(memory,TMP+8,TMP);found=call(0x20a8a3c,A+0x100,TMP+8);result=word(memory,found) if found else 0
    elif address==0x20b5cd0:
        contract='void'
        if not word(memory,C+20) and not word(memory,C+36):
            if word(memory,C+12)==7:
                count=signed(call(0x20a8640,A))
                for index in range(max(0,count)):
                    slot=call(0x20a8644,A,index)
                    if word(memory,slot)==C:call(0x20a8720,A,index);break
            else:put(memory,TMP,C);call(0x20a89f0,A+0x100,TMP)
    elif address==0x20b5e8c:
        state=word(memory,C+12)
        if state!=7 and not call(0x20b4228,C,word(memory,T)):result=0
        elif word(memory,C+12)==7 and not word(memory,C+20) and not word(memory,C+36):call(0x20b5cd0,C)
    elif address==0x20b5f14:
        contract='void'
        if not word(memory,S+24):
            put(memory,S+24,1);call(0x20b4540,S)
            if call(0x20b3be4,S):call(0x20b5b4c,S)
    else:raise ValueError('Caller outside third packet')
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,contract,result&0xffffffff


def cases(address):
    if address==0x20b5970:return [dict(ip=ip,port=port,buckets=count) for ip in [0,1,0x7fffffff,0x80000000,0xffffffff,0x12345678] for port in [0,1,32768,65535] for count in [1,2,3,31,32,0x7fffffff]]
    if address==0x20b5984:return [dict(ip=ip,ip2=ip2,port=port,port2=port2) for ip in [0,1,0x7fffffff,0x80000000,0xffffffff] for ip2 in [0,1,0x7fffffff,0x80000000,0xffffffff] for port in [0,1,32768,65535] for port2 in [0,1,32768,65535]]
    if address==0x20b59ac:return [dict(ip=ip,port=port,found=found,lookupValue=value) for ip in [0,0x0100007f,0xffffffff] for port in [0,1,65535] for found in [0,1] for value in [0,C,C2]]
    if address==0x20b5cd0:return [dict(state=state,free=free,callback=callback,count=count,match=match) for state in [0,6,7] for free in [0,1] for callback in [0,1] for count in [0,1,3] for match in [-1,0,2]]
    if address==0x20b5e8c:return [dict(state=state,free=free,callback=callback,afterState=after,afterFree=after_free,afterCallback=after_callback,helper=result,now=now) for state in [0,7] for free in [0,1] for callback in [0,1] for after in [0,7] for after_free in [0,1] for after_callback in [0,1] for result in [0,1,0x80000000] for now in [0,0xffffffff]]
    if address==0x20b5f14:return [dict(error=error,helper=result) for error in [0,1,0xffffffff] for result in [0,1,0x80000000]]
    raise ValueError('Third caller lacks bounded vectors')
