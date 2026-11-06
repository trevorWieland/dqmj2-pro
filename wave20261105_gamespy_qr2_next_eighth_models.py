import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,half,put

C,S=0x2170000,0x2171000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e1714
ARITY={0x20b45c8:3,0x20b4108:3,0x20b5d3c:5}


def initial(address,v):
    memory=Memory({C:bytes(160),S:bytes(76),MAGIC:bytes.fromhex('fefe00'),SP-0x1000:bytes(0x1000)})
    put(memory,C+8,S);put(memory,S+64,v['protocol']);put(memory,C+102,v.get('expected',0x80ff),2);put(memory,C+144,0xfedcba98);put(memory,C+136,0x44556677)
    args={0x20b57a0:[C],0x20b5810:[C,v.get('low',0),v.get('high',65535)],0x20b58ac:[S,v.get('ip',0x12345678),v.get('port',65535)]}
    return memory,args[address]


def effect(target,args,memory,v):
    if target==0x20b45c8:
        memory.write(args[0]+args[1],(args[2]&65535).to_bytes(2,'big'))
        return 0x33445566,[args[1],args[2]]
    if target==0x20b4108:
        packet=memory.read(args[1],args[2]);normalized=[args[0],packet.hex(),args[2]]
        if v['send']:put(memory,C+136,0x99887766)
        return v['send'],normalized
    if target==0x20b5d3c:return v['send'],[args[0],args[1],args[2],memory.read(args[3],args[4]).hex(),args[4]]
    raise ValueError(('Unqualified protocol contract',hex(target)))


def model(address,v):
    memory,args=initial(address,v);calls=[];prefix=(5 if address==0x20b57a0 else 7 if address==0x20b5810 else 3).to_bytes(2,'little') if v['protocol']==2 else b''
    if address==0x20b57a0:
        packet=prefix+b'\xfe\xfe\x64'+half(memory,C+102).to_bytes(2,'big');calls.append((hex(0x20b45c8),[len(prefix)+3,half(memory,C+102)]))
    elif address==0x20b5810:
        packet=prefix+b'\xfe\xfe\x65'+v['low'].to_bytes(2,'big');calls.append((hex(0x20b45c8),[len(prefix)+3,v['low']]))
        if v['low']!=v['high']:packet+=v['high'].to_bytes(2,'big');calls.append((hex(0x20b45c8),[len(prefix)+5,v['high']]))
    else:packet=prefix+b'\xfe\xfe\x68'
    memory.write(TMP,packet)
    target=0x20b5d3c if address==0x20b58ac else 0x20b4108
    supplied=[S,args[1],args[2],TMP,len(packet)] if address==0x20b58ac else [C,TMP,len(packet)]
    value,normalized=effect(target,supplied,memory,v);calls.append((hex(target),normalized))
    if address==0x20b57a0 and value:put(memory,C+144,0)
    return {at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000},calls,'word',int(value!=0)


def cases(address):
    protocols=[0,1,2,3,0xffffffff];returns=[0,1,0x80000000]
    if address==0x20b57a0:return [dict(protocol=p,expected=n,send=r)for p in protocols for n in [0,1,0x80ff,65535]for r in returns]
    if address==0x20b5810:return [dict(protocol=p,low=a,high=b,send=r)for p in protocols for a,b in [(0,0),(0,65535),(1,1),(1,2),(65535,0),(0x8000,0x7fff)]for r in returns]
    return [dict(protocol=p,ip=i,port=n,send=r)for p in protocols for i in [0,0x12345678,0xffffffff]for n in [0,1,0x80ff,65535]for r in returns]
