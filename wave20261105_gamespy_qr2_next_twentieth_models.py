from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

C,SK,D,A,O,F,AI,OI,IB,OV=0x2170000,0x2171000,0x2172000,0x2173000,0x2173100,0x2173200,0x2174000,0x2174200,0x2175000,0x2176000
SP,STOP,TMP,MAGIC,DIV=0x2701000,0x27e0000,0x2700800,0x20e170c,0
ARITY={0x20b4634:1,0x20a8640:1,0x20b3e80:5,0x20b3d04:4,0x20b3a58:2,0x20b39c4:1,0x20b5514:3,0x20b42a4:1,0x20b589c:1,0x20b3ca4:4,0x20b45dc:3,0x20b475c:3,0x20b47c8:3,0x20b4834:3,0x20b48c8:3,0x20b4984:1,0x20b49b8:3,0x20b4a00:1,0x20a8644:2,0x20b45d4:2,0x20b3b50:1,0x20a86b8:3,0x20b3b80:3,0x20b5810:3,0x20b4ac8:2,0x20b4a30:4,0x20b4be4:3,0x20b45b0:2,0x20b465c:2,0x20b4c90:1,0x20b4c40:1,0x20b4ad4:6,0x20b4640:1,0x20b5900:2,0x201b248:3,0x20a8ef8:0,0x20b3db0:2,0x20b4dbc:3,0x20b4df0:3,0x20b4e84:3,0x20b4e8c:3,0x20b4ee8:1}
TYPES={0:0x20b475c,1:0x20b47c8,2:0x20b4834,3:0x20b48c8,4:0x20b4984,5:0x20b49b8,6:0x20b4a00}


def dynamic_callbacks(v):return{}
def h(m,a):return int.from_bytes(m.read(a,2),'little')
def ph(m,a,n):m.write(a,(n&65535).to_bytes(2,'little'))
def diff(a,b):value=(a-b)&65535;return value-65536 if value&32768 else value


def initial(address,v):
    m=Memory({C:bytes(160),SK:bytes(76),D:bytes((i*17+3)&255 for i in range(128)),A:bytes(4),O:bytes(4),F:bytes(4),AI:bytes([0x9b])*128,OI:bytes([0x6a])*128,IB:bytes([0x33])*256,OV:bytes.fromhex('ddccbbaa'),MAGIC:b'time\0',SP-0x1000:bytes(0x1000)})
    for at,value in [(C+8,SK),(C+12,v.get('state',5)),(C+52,v.get('ping',1)),(C+68,IB),(C+72,256),(C+76,v.get('bufferLen',0)),(C+92,A),(C+96,O),(C+156,F),(SK+64,v.get('protocol',0)),(SK+68,v.get('offset',0)),(F,v.get('filters',0))]:put(m,at,value)
    ph(m,C+102,v.get('expected',0));m.write(C+104,bytes([0x77])*32)
    serials=v.get('serials',[]);outs=v.get('outSerials',[0,10,65530]);put(m,A,len(serials));put(m,O,len(outs))
    for array,items in [(AI,serials),(OI,outs)]:
        for i,sn in enumerate(items):
            put(m,array+i*16,i*8);put(m,array+i*16+4,4);put(m,array+i*16+8,v.get('type',7));ph(m,array+i*16+(12 if array==AI else 8),sn)
    length=v.get('length',32)
    if address==0x20b45b0:m.write(D+v['pos'],v['value'].to_bytes(2,'big'));return m,[D,v['pos']]
    if address==0x20b4cb0:
        off=v.get('offset',0);m.write(D+off+3,v.get('sn',0).to_bytes(2,'big'));m.write(D+off+5,v.get('esn',0).to_bytes(2,'big'))
    if address==0x20b4df0:m.write(D,v.get('minimum',0).to_bytes(2,'big')+v.get('maximum',0).to_bytes(2,'big'))
    if address==0x20b4e8c:m.write(D,b'time'if v.get('prefix',True)else b'xxxx');put(m,D+4,v.get('start',0))
    if address in [0x20b475c,0x20b47c8,0x20b49b8,0x20b4df0,0x20b4e8c]:return m,[C,D,length&0xffffffff]
    if address in [0x20b4a30,0x20b4cb0,0x20b4f10]:return m,[C,v.get('type',0)&0xffffffff,D,length&0xffffffff]
    if address==0x20b4ad4:return m,[C,v.get('type',7),v.get('sn',0),D,length,OV]
    if address in [0x20b4a00,0x20b4c40,0x20b4ee8]:return m,[C]
    raise ValueError('Unselected GT2 receiver')


def effect(at,a,m,v):
    result=0 if v.get('fail')==at else v.get('result',1);norm=a[:]
    if at==0x20a8640:result=word(m,a[0])
    elif at==0x20a8644:
        base=AI if a[0]==A else OI if a[0]==O else None
        if base is None or a[1]>=8:raise ValueError('Bounded supplied ArrayNth index')
        result=base+a[1]*16
    elif at==0x20b45d4:result=diff(a[0],a[1])
    elif at==0x20b45b0:result=int.from_bytes(m.read(a[0]+a[1],2),'big')
    elif at==0x20b3b50:result=v.get('free',word(m,C+72)-word(m,C+76))
    elif at==0x20a86b8:
        raw=m.read(a[1],14);norm=[a[0],raw.hex(),a[2]]
        if v.get('insert',True):
            count=word(m,A);index=v.get('insertIndex',count);index=count if index<0 else min(index,count)
            for i in range(count,index,-1):m.write(AI+i*16,m.read(AI+(i-1)*16,16))
            m.write(AI+index*16,raw);put(m,A,count+1)
    elif at==0x20b3b80:
        length=s32(a[2]);norm=[a[0],a[1],a[2],m.read(a[1],max(0,length)).hex()];start=word(m,C+76)
        if length>=0:m.write(IB+start,m.read(a[1],length));put(m,C+76,start+length)
    elif at==0x20b4be4:
        count=word(m,A);index=a[2]
        for i in range(index,count-1):m.write(AI+i*16,m.read(AI+(i+1)*16,16))
        put(m,A,count-1)
    elif at==0x20b4a30:
        if v.get('bumpExpected',True)and result:ph(m,C+102,h(m,C+102)+1)
    elif at==0x20b4ad4:m.write(a[5],v.get('overflow',0).to_bytes(4,'little'));norm=a[:5]+[v.get('overflow',0)]
    elif at==0x20b465c:
        if 'afterESN'in v:ph(m,C+102,v['afterESN'])
    elif at==0x20b4c90:put(m,C+144,1);put(m,C+148,v.get('now',0))
    elif at==0x20b42a4:put(m,C+12,7)
    elif at==0x20b589c:
        if 'afterSendState'in v:put(m,C+12,v['afterSendState'])
    elif at==0x20b3a58:
        raw=m.read(a[1],32);out=bytes(b^0xa5 for b in raw);m.write(a[0],out);norm=[a[0]if a[0]==C+104 else'local-response32',raw.hex()]
    elif at==0x20b39c4:m.write(a[0],bytes((i*19+7)&255 for i in range(32)));norm=['local-challenge32']
    elif at==0x20b5514:
        norm=[a[0],m.read(a[1],32).hex(),m.read(a[2],32).hex()]
        if 'afterSendState'in v:put(m,C+12,v['afterSendState'])
    elif at==0x201b248:norm=[m.read(a[0],a[2]).hex(),m.read(a[1],a[2]).hex(),a[2]];result=0 if norm[0]==norm[1]else 1
    elif at==0x20a8ef8:
        result=v.get('now',0)
        if 'afterClockStart'in v:put(m,D+4,v['afterClockStart'])
    elif at in ARITY:pass
    else:raise ValueError(('Unqualified original helper',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=1;length=v.get('length',32);typ=v.get('type',0)
    def call(at,args):
        value,norm=effect(at,[a&0xffffffff for a in args],m,v);calls.append((hex(at),norm));return value
    def boolean(at,args):return int(call(at,args)!=0)
    if address==0x20b45b0:result=int.from_bytes(m.read(D+v['pos'],2),'big')
    elif address==0x20b475c:
        if s32(word(m,C+12))not in [5,6]:result=boolean(0x20b4634,[C])
        elif call(0x20a8640,[F]):result=boolean(0x20b3e80,[C,0,D,length,1])
        else:result=boolean(0x20b3d04,[C,D,length,1])
    elif address==0x20b47c8:
        if word(m,C+12)!=2 or length<32:result=boolean(0x20b4634,[C])
        else:
            call(0x20b3a58,[TMP,D]);call(0x20b39c4,[TMP+64]);call(0x20b3a58,[C+104,TMP+64]);result=boolean(0x20b5514,[C,TMP,TMP+64])
            if result:put(m,C+12,3)
    elif address==0x20b49b8:
        if word(m,C+12)!=1:result=boolean(0x20b4634,[C])
        else:
            call(0x20b42a4,[C]);result=boolean(0x20b589c,[C])
            if result:result=boolean(0x20b3ca4,[C,2,D,length])
    elif address in [0x20b4a00,0x20b4ee8]:
        if address!=0x20b4ee8 or word(m,C+12)!=7:
            if address==0x20b4a00:result=boolean(0x20b589c,[C])
            if result:result=boolean(0x20b45dc,[C,2,0 if word(m,C+12)==6 else 1])
    elif address==0x20b4a30:
        ph(m,C+102,h(m,C+102)+1)
        if typ in TYPES:result=boolean(TYPES[typ],[C]if typ in [4,6]else[C,D,length])
    elif address==0x20b4ad4:
        sn=v['sn'];num=call(0x20a8640,[A]);duplicate=False
        for i in range(s32(num)):
            ptr=call(0x20a8644,[A,i]);other=h(m,ptr+12)
            if other==sn:put(m,OV,0);duplicate=True;break
            if s32(call(0x20b45d4,[other,sn]))>0:break
        if not duplicate:
            if s32(call(0x20b3b50,[C+68]))<length:put(m,OV,1)
            else:
                put(m,TMP,word(m,C+76));put(m,TMP+4,length);put(m,TMP+8,typ);ph(m,TMP+12,sn);call(0x20a86b8,[A,TMP,0x20b4ac9])
                if call(0x20a8640,[A])!=num+1:put(m,OV,1)
                else:
                    call(0x20b3b80,[C+68,D,length])
                    if num==0:result=boolean(0x20b5810,[C,h(m,C+102),(sn-1)&65535])
                    else:
                        last=call(0x20a8644,[A,num])
                        if h(m,last+12)==sn:
                            prev=call(0x20a8644,[A,num-1]);delta=call(0x20b45d4,[sn,h(m,prev+12)])&65535
                            if delta>1:result=boolean(0x20b5810,[C,(h(m,prev+12)+1)&65535,(sn-1)&65535])
                    if result:put(m,OV,0)
    elif address==0x20b4c40:
        while result:
            count=call(0x20a8640,[A]);restart=False
            for i in range(s32(count)-1,-1,-1):
                ptr=call(0x20a8644,[A,i])
                if h(m,ptr+12)==h(m,C+102):
                    result=boolean(0x20b4a30,[C,word(m,ptr+8),IB+word(m,ptr),word(m,ptr+4)])
                    if result:call(0x20b4be4,[C,ptr,i]);restart=True
                    break
            if not restart:break
    elif address==0x20b4cb0:
        off=word(m,SK+68);header=off+7
        if length<header:result=boolean(0x20b4634,[C])
        else:
            sn=call(0x20b45b0,[D+off,3]);esn=call(0x20b45b0,[D+off,5])
            if word(m,SK+64)==2 and typ==0:m.write(D+off+5,m.read(D,2));start=D+7;remaining=length-7
            else:start=D+header;remaining=length-header
            result=boolean(0x20b465c,[C,esn])
            if result:
                expected=h(m,C+102)
                if sn==expected:
                    call(0x20b4c90,[C]);result=boolean(0x20b4a30,[C,typ,start,remaining])
                    if result:result=boolean(0x20b4c40,[C])
                elif s32(call(0x20b45d4,[sn,expected]))<0:call(0x20b4c90,[C])
                else:
                    put(m,TMP,0);result=boolean(0x20b4ad4,[C,typ,sn,start,remaining,TMP])
                    if result and word(m,TMP):result=boolean(0x20b4640,[C])
    elif address==0x20b4df0:
        minimum=call(0x20b45b0,[D,0]);maximum=minimum
        if length==4:maximum=call(0x20b45b0,[D,2])
        elif length!=2:result=boolean(0x20b4634,[C]);return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result
        count=call(0x20a8640,[O])
        for i in range(s32(count)):
            ptr=call(0x20a8644,[O,i]);sn=h(m,ptr+8)
            if s32(call(0x20b45d4,[sn,minimum]))>=0 and s32(call(0x20b45d4,[sn,maximum]))<=0:
                if not boolean(0x20b5900,[C,ptr]):result=0;break
    elif address==0x20b4e8c:
        if word(m,C+52)and length==8 and call(0x201b248,[D,MAGIC,4])==0:
            start=word(m,D+4);now=call(0x20a8ef8,[]);result=boolean(0x20b3db0,[C,(now-start)&0xffffffff])
    elif address==0x20b4f10:
        start=D+word(m,SK+68)+3;remaining=length-word(m,SK+68)-3
        if typ in [100,101,103]:result=boolean({100:0x20b4dbc,101:0x20b4df0,103:0x20b4e8c}[typ],[C,start,remaining])
        elif typ==102:result=boolean(0x20b4e84,[C,D,length])
        elif typ==104:result=boolean(0x20b4ee8,[C])
    else:raise ValueError('Unknown GT2 caller model')
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result


def cases(address):
    def row(**kw):return dict(entry=address,**kw)
    if address==0x20b45b0:return[row(pos=pos,value=value)for pos in [0,1,5,63]for value in [0,1,0xffff,0x80ff]]
    if address==0x20b475c:return[row(state=state,filters=filters,fail=fail)for state in [-1,0,5,6,7]for filters in [0,1,-1]for fail in [None,0x20b4634,0x20b3e80,0x20b3d04]]
    if address==0x20b47c8:return[row(state=state,length=length,fail=fail,afterSendState=7)for state in [2,3]for length in [0,31,32,64]for fail in [None,0x20b4634,0x20b5514]]
    if address==0x20b49b8:return[row(state=state,length=length,fail=fail)for state in [-1,0,1,7]for length in [0,8]for fail in [None,0x20b4634,0x20b589c,0x20b3ca4]]
    if address==0x20b4a00:return[row(state=state,fail=fail,afterSendState=after)for state in [5,6,7]for fail in [None,0x20b589c,0x20b45dc]for after in [5,6,7]]
    if address==0x20b4a30:return[row(type=typ,expected=expected,result=result)for typ in [-1,*range(9)]for expected in [0,65535]for result in [0,1,0x80000000]]
    if address==0x20b4ad4:return[row(serials=serials,sn=sn,type=7,length=4,free=free,insert=insert,insertIndex=index,fail=fail,expected=5)for serials in [[],[10],[10,20],[65530,1]]for sn in [0,10,11,65535]for free in [-1,4,8]for insert in [False,True]for index in [0,-1]for fail in [None,0x20b5810]]
    if address==0x20b4c40:return[row(serials=serials,expected=expected,fail=fail,type=7)for serials in [[],[0,1,2],[2,1,0],[10],[65535,0]]for expected in [0,1,65535]for fail in [None,0x20b4a30]]
    if address==0x20b4cb0:
        rows=[row(offset=off,protocol=protocol,type=typ,length=32,sn=sn,esn=0x1234,expected=100,fail=fail,overflow=overflow)for off in [0,2]for protocol in [0,2]for typ in [0,2]for sn in [99,100,101]for fail in [None,0x20b465c,0x20b4a30,0x20b4c40,0x20b4ad4,0x20b4640]for overflow in [0,1]]
        rows +=[row(offset=off,length=length,type=0,sn=0,expected=0,fail=fail)for off in [0,2]for length in [-1,0,6,7,8]for fail in [None,0x20b4634]];rows +=[row(length=32,sn=10,expected=1,afterESN=10,type=0)];return rows
    if address==0x20b4df0:return[row(length=length,minimum=minimum,maximum=maximum,outSerials=[0,10,65530],fail=fail)for length in [0,2,4,5]for minimum,maximum in [(0,0),(65520,10),(10,65520)]for fail in [None,0x20b4634,0x20b5900]]
    if address==0x20b4e8c:return[row(ping=ping,length=length,prefix=prefix,start=start,now=now,fail=fail)for ping in [0,1]for length in [0,7,8,9]for prefix in [False,True]for start in [0,0xffffffff]for now in [0,0xfffffff0]for fail in [None,0x20b3db0]]
    if address==0x20b4ee8:return[row(state=state,result=result)for state in [-1,5,6,7]for result in [0,1,0x80000000]]
    if address==0x20b4f10:return[row(offset=off,type=typ,length=length,result=result)for off in [0,2]for typ in range(99,106)for length in [-1,0,3,32]for result in [0,1]]
    raise ValueError('No receiver cases')
