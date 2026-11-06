from wave20261105_socket_thumb_next_memory import Memory

CTX,OUT,CACHE,SP,STOP=0x02400000,0x02410000,0x021d1748,0x027f0000,0x027d0000
SPECS={'020909c8':24,'02090a3c':32,'02090ae8':24}
NAMES=list(SPECS)


def fixtures(name):
    if name=='020909c8':return [dict(match=m,invalid=v,duplicate=d,alias=a,zero=z,pattern=p)for p,(m,v,d,a,z)in enumerate([(-1,-1,False,False,False),(0,-1,False,False,False),(3,-1,False,False,False),(2,2,False,False,False),(0,-1,True,False,False),(1,-1,False,False,True),(0,-1,False,True,False)])]
    if name=='02090a3c':return [dict(match=m,invalid=v,ipzero=iz,portzero=pz,agecase=age,pattern=p)for p,(m,v,iz,pz,age)in enumerate([(-1,-1,False,False,0),(-1,1,False,False,0),(3,1,False,False,0),(2,-1,True,False,0),(2,-1,False,True,0),(-1,-1,False,False,1),(-1,-1,False,False,2),(0,-1,False,False,0)])]
    return [dict(match=m,invalid=v,duplicate=d,pattern=p)for p,(m,v,d)in enumerate([(-1,-1,False),(0,-1,False),(3,-1,False),(0,-1,True),(2,0,True)])]


def scenario(name,f,ordinal):
    memory=Memory({CTX:192,OUT:64,CACHE:368},ordinal);actions=[];pattern=f['pattern'];tick=[0x0123456789abcdef,0xffffffffffff0000,0x0000000100010000,0xabcdeff000010000][pattern%4];now=(tick>>16)&0xffffffff;irq=[0,0x80,0xffffffff,0x12345678][pattern%4];context=CACHE+32 if f.get('alias')else CTX;ip=0 if f.get('zero')or f.get('ipzero')else 0xaabbccdd;port=0 if f.get('zero')or f.get('portzero')else 65535
    memory.put(CTX,bytes((i*17+pattern*13)&255 for i in range(48)));memory.put(CTX+116,bytes((i*31+pattern*7)&255 for i in range(32)))
    for i in range(4):
        base=CACHE+92*i;session=bytes((i*23+j*11+9)&255 for j in range(32));master=bytes((i*41+j*7+3)&255 for j in range(48));memory.put(base,session+master);when=(now-(i+1)*7)&0xffffffff
        if f.get('agecase')==1:when=now
        elif f.get('agecase')==2:when=(now+1)&0xffffffff if i==1 else now
        memory.set(base+80,when);memory.set(base+84,ip if i==f['match']or f.get('duplicate')and i in [0,2] else i+1);memory.set(base+88,port if i==f['match']or f.get('duplicate')and i in [0,2] else i+5,2);memory.set(base+90,0 if i==f['invalid']else 0x80 if i&1 else 1,1)
        if name=='02090ae8' and (i==f['match']or f.get('duplicate')and i in [0,2]):memory.put(base,memory.read(context+116,32))
    initial=memory.snapshot()
    def call(address,args,returned=0xa7000000,mutations=None,high=None):
        action=dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=[(base,raw)for base,raw in memory.snapshot().items()],mutations=list(mutations or []),stackWords=[])
        if high is not None:action['returnedHigh']=high
        actions.append(action)
        for base,raw in action['mutations']:memory.put(base,raw)
    def copy(source,destination,length):call(0x2008e0c,[source,destination,length],mutations=[(destination,memory.read(source,length))])
    def clock():call(0x2007a9c,[],tick&0xffffffff,high=tick>>32)
    call(0x2007ff4,[],irq)
    if name=='020909c8':
        memory.set(context+48,0,1)
        for i in range(4):
            base=CACHE+92*i
            if memory.get(base+90,1) and memory.get(base+84)==ip and memory.get(base+88,2)==port:
                copy(base,context+116,32);copy(base+32,context,48);clock();memory.set(base+80,now);memory.set(context+48,1,1);break
        args=[context,ip,port,0x33445566]
    elif name=='02090a3c':
        clock();candidate=CACHE;biggest=0
        for i in range(4):
            base=CACHE+92*i;valid=memory.get(base+90,1)
            if valid and ip and memory.get(base+84)==ip and port and memory.get(base+88,2)==port:candidate=base;break
            if biggest!=0xffffffff:
                if not valid:biggest=0xffffffff;candidate=base
                else:
                    age=(now-memory.get(base+80))&0xffffffff
                    if age>biggest:biggest=age;candidate=base
        copy(context+116,candidate,32);copy(context,candidate+32,48);memory.set(candidate+80,now);memory.set(candidate+90,1,1);memory.set(candidate+84,ip);memory.set(candidate+88,port,2);args=[context,ip,port,0x33445566]
    else:
        for i in range(4):
            base=CACHE+92*i
            if memory.get(base+90,1):
                same=memory.read(base,32)==memory.read(context+116,32);call(0x201b248,[base,context+116,32],0 if same else 0x80000000)
                if same:memory.set(base+90,0,1);break
        args=[context,0x11773355,0x22334455,0x33445566]
    call(0x2008008,[irq]);return dict(initial=initial,regions=memory.snapshot(),args=args,actions=actions,result=None,volatileStateReads=None,readable=[(CTX,192),(OUT,64),(CACHE,367)],context=context)
