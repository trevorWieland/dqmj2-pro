from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

C,SK,O,REC,ST=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000
SP,STOP,TMP,MAGIC,DIV=0x2701000,0x27e0000,0x2700200,0,0
ARITY={0x20a8d88:1,0x20a8c00:6,0x20a8c9c:1,0x20b514c:3,0x20b51dc:4,0x20b5f14:1,0x20b4f80:5,0x20a8ef8:0,0x20a8640:1,0x20a865c:2}


def dynamic_callbacks(v):return{}


def initial(address,v):
    m=Memory({C:bytes(160),SK:bytes(76),O:v.get('count',0).to_bytes(4,'little'),REC:bytes([0xa5])*16,ST:bytes(16),SP-0x1000:bytes(0x1000)})
    put(m,C+96,O);put(m,C+88,v.get('bufferLen',7));put(m,SK,v.get('socket',11))
    if address==0x20b523c:return m,[SK]
    if address==0x20b5344:return m,[C,v['sn'],v['length']&0xffffffff]
    raise ValueError('Outside selected receive/builder scope')


def effect(at,a,m,v):
    result=0 if v.get('fail')==at else v.get('result',1);norm=a[:]
    if at==0x20a8d88:result=int(word(m,ST)<len(v['receives']))
    elif at==0x20a8c00:
        index=word(m,ST);length=v['receives'][index];put(m,ST,index+1);norm=[a[0],a[2],a[3],word(m,a[5])];m.write(a[4],bytes([0x7f,2,0x12,0x34,1,2,3,4]));put(m,a[5],v.get('returnedAddrLen',6));result=length&0xffffffff
        if length>=0:m.write(a[1],bytes((i*13+index)&255 for i in range(length)))
    elif at==0x20a8c9c:result=v['errors'][word(m,ST)-1]&0xffffffff
    elif at in [0x20b514c,0x20b51dc]:
        if 'afterResetSocket'in v:put(m,SK,v['afterResetSocket'])
    elif at==0x20b4f80:norm=[a[0],m.read(a[1],max(0,s32(a[2]))).hex(),a[2],a[3],a[4]]
    elif at==0x20b5f14:pass
    elif at==0x20a8ef8:
        result=v.get('now',0)
        if 'afterClockBufferLen'in v:put(m,C+88,v['afterClockBufferLen'])
    elif at==0x20a8640:result=word(m,O)
    elif at==0x20a865c:
        norm=[a[0],m.read(a[1],16).hex()]
        if v.get('delta',1):m.write(REC,m.read(a[1],16));put(m,O,word(m,O)+v.get('delta',1))
    else:raise ValueError(('Unqualified measured import',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=1
    def call(at,args):
        value,norm=effect(at,[a&0xffffffff for a in args],m,v);calls.append((hex(at),norm));return value
    if address==0x20b523c:
        while call(0x20a8d88,[word(m,SK)]):
            put(m,TMP+1516,8);ret=call(0x20a8c00,[word(m,SK),TMP,1500,0,TMP+1504,TMP+1516]);ip=word(m,TMP+1508);port=int.from_bytes(m.read(TMP+1506,2),'big')
            if ret==0xffffffff:
                error=s32(call(0x20a8c9c,[word(m,SK)]))
                if error==-15:
                    if not call(0x20b514c,[SK,ip,port]):result=0;break
                elif error==-23:
                    if not call(0x20b51dc,[SK,ip,port,0]):result=0;break
                elif error!=-35:call(0x20b5f14,[SK]);result=0;break
            elif not call(0x20b4f80,[SK,TMP,ret,ip,port]):result=0;break
    else:
        start=word(m,C+88);length=v['length']&0xffffffff;now=call(0x20a8ef8,[]);m.write(TMP,start.to_bytes(4,'little')+length.to_bytes(4,'little')+v['sn'].to_bytes(2,'little')+bytes(2)+now.to_bytes(4,'little'));count=call(0x20a8640,[O]);call(0x20a865c,[O,TMP]);result=int(call(0x20a8640,[O])==count+1)
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result


def cases(address):
    if address==0x20b5344:
        rows=[dict(sn=sn,length=length,now=now,bufferLen=buffer,count=count,delta=delta)for sn in [0,1,65535]for length in [-1,0,32]for now in [0,0xffffffff]for buffer in [0,7,255]for count in [0,3]for delta in [0,1,2]]
        rows.append(dict(rows[0],bufferLen=7,afterClockBufferLen=99));return rows
    if address!=0x20b523c:raise ValueError('No selected receive/builder vectors')
    rows=[]
    for receive in [0,3,1500,-2,-1]:
        for error in [-15,-23,-35,-42,-6,0,-1]:
            for fail in [None,0x20b514c,0x20b51dc,0x20b4f80]:rows.append(dict(receives=[receive],errors=[error],fail=fail))
    rows +=[dict(receives=[],errors=[]),dict(receives=[-1,-1,3,0,-2],errors=[-15,-35,0,0,0],afterResetSocket=77),dict(receives=[-1,-1],errors=[-23,-35],returnedAddrLen=1)];return rows
