import itertools
from wave20261105_socket_thumb_next_memory import Memory
SOCKETS=[0x02402000,0x02402200]
SENDS=[0x02403000,0x02403200]
BUFFER=0x02405000
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f724':32,'0208f7e4':56,'0208f900':0}


def signed(v):return v if v<0x80000000 else v-0x100000000


def fixtures(name):
    if name=='0208f900':return [dict(size=s,inValue=i,outValue=o) for s,i,o in itertools.product([0,1,16,65536,0x7fffffff],[0,1,15,65535],[0,1,15,65535])]
    if name=='0208f724':
        rows=[dict(mode=i,block=i,flag=[0,4,5,0x80000004][i%4],state=[0,1,5,9,13,0x8005,0xffff][i%7],invalid=int(i%13==0),tryResult=i%3,mutate=bool(i&1),returned=[0,-6,7,0x80000000][i%4],null=False) for i in range(256)]
        return rows+[dict(mode=m,block=b,flag=f,state=s,invalid=0,tryResult=t,mutate=z,returned=0x80000000,null=False) for m,b,f,s,t,z in itertools.product([0,1,4,255],[0,1],[0,4],[0,1,5,9,13],[0,1],[False,True])]+[dict(mode=0,block=0,flag=0,state=0,invalid=i,tryResult=0,mutate=False,returned=0,null=True) for i in [0,1,-1]]
    return [dict(mode=m,length=n,flag=f,path=p,mutate=z) for m,n,f,p,z in itertools.product([0,1,4,255],[-1,0,1,8,17,29],[0,1,2,3,0x80000001],['normal','zero-once','zero-only','exec-fail'],[False,True]) if not (p=='zero-only' and f&1 and n>0)]


def scenario(name,f,ordinal):
    memory=Memory({**{p:128 for p in SOCKETS},**{p:272 for p in SENDS},BUFFER:128},ordinal);get,setv=memory.get,memory.set
    socket,send=SOCKETS[0],SENDS[0]
    for i,p in enumerate(SOCKETS):setv(p+104,SENDS[i]);setv(p+112,f.get('state',5),2);setv(p+114,f.get('block',1),1);setv(p+115,f.get('mode',0),1);setv(p+72,70)
    for p in SENDS:setv(p+248,f.get('size',64));setv(p+256,f.get('inValue',3),2);setv(p+258,f.get('outValue',11),2);setv(p+268,SOCKETS[1])
    initial=memory.snapshot();actions=[]
    def word(at,v,size=4):return at,int(v&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if SP-SPECS[name]<=at and at+len(raw)<=SP:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    if name=='0208f900':
        arguments=[socket,0x11223344,0x55667788,0x99aabbcc];available=get(send+258,2)-get(send+256,2)-1
        result=(available+(signed(get(send+248)) if available<0 else 0))&0xffffffff
    elif name=='0208f724':
        socket=0 if f['null'] else socket;arguments=[socket,BUFFER,31,0x8012,0x89abcdef,f['flag']]
        invalid=call(0x02090294,[socket],f['invalid'])
        if invalid:result=-28
        elif not socket or not get(socket+112,2)&1:result=-39
        elif get(socket+115,1) in [0,4] and (not get(socket+112,2)&4 or get(socket+112,2)&8):result=-56
        else:
            noBlock=bool(f['flag']&4) or get(socket+114,1)==0
            changes=[word(socket+104,SENDS[1]),word(socket+114,0,1),word(socket+115,128,1)] if f['mutate'] else []
            locked=call(0x020071a8 if noBlock else 0x0200708c,[send+224],f['tryResult'],changes)
            if noBlock and not locked:result=-6
            else:
                flag=0 if noBlock else 1
                result=call(0x0208f7e4,[socket,BUFFER,31,0x8012,0x89abcdef,flag],f['returned'])
                call(0x02007110,[send+224])
    else:
        arguments=[socket,BUFFER,f['length']&0xffffffff,0x8012,0x89abcdef,f['flag']]
        length=f['length'];sendLength=signed(get(SOCKETS[1]+72));sendLength-=42 if f['mode']==1 else 54;buffer=BUFFER;copied=0
        if f['mode']==1 and length>sendLength:result=-35
        else:
            minimum=length if f['mode']==1 else min(length,sendLength);iteration=0;result=None
            while length>0:
                iteration+=1
                if iteration>8:raise ValueError('Bounded write-buffer model did not terminate')
                available=0 if f['path']=='zero-only' or f['path']=='zero-once' and iteration==1 else min(length,8)
                changes=[word(SP-24,7+iteration)]
                if f['mutate']:changes += [word(socket+104,SENDS[1]),word(SOCKETS[1]+72,0),word(socket+115,128,1)]
                call(0x0208f898,[socket,length,minimum,SP-24,f['flag']],available,changes)
                if available>0:
                    returned=call(0x0208f91c,[socket,buffer,available,7+iteration,0x8012,0x89abcdef,f['flag']],(0 if f['mode']==1 else 0x80000000 if f['mode']==4 else -1) if f['path']=='exec-fail' else 1)
                    if signed(returned)<=0:result=-6;break
                    buffer+=available;length-=available;copied+=available
                if not f['flag']&1:
                    result=-6 if available<=0 else copied;break
                if f['path']=='zero-only':raise ValueError('Blocking zero-only allocator would not return')
            if result is None:result=copied
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=[])
