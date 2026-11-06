from wave20261105_socket_thumb_next_memory import Memory

ENTRIES,SP,STOP=0x02400000,0x027f0000,0x027d0000
CTX=OUT=ENTRIES
SPECS={'020907f4':40}
NAMES=list(SPECS)


def fixtures(name):
    rows=[dict(timeout=0,entries=[],rounds=[[]],mutate=False),dict(timeout=1,entries=[],rounds=[[]],mutate=False),dict(timeout=0,entries=[(-1,0)],rounds=[[0x80]],mutate=False),dict(timeout=0,entries=[(11,-1)],rounds=[[0x10000]],mutate=False),dict(timeout=0,entries=[(11,1),(22,0)],rounds=[[0x10000,1]],mutate=True)]
    rows += [dict(timeout=n,entries=[(11,1)],rounds=[[0]],mutate=False) for n in [1,522,523,524,0x8000000000000000]]
    rows += [dict(timeout=n,entries=[(11,4)],rounds=[[0],[0],[4]],mutate=False) for n in [0xffffffffffffffff,0x100000001]]
    rows += [dict(timeout=0x100000000,entries=[(11,1),(22,2),(33,0)],rounds=[[1,2,0x40]],mutate=False)]
    rows += [dict(timeout=0,entries=[(11,1)],rounds=[[4]],mutate=False)]
    return rows


def scenario(name,f,ordinal):
    memory=Memory({ENTRIES:64},ordinal);actions=[]
    for i,(fd,events) in enumerate(f['entries']):memory.set(ENTRIES+i*8,fd);memory.set(ENTRIES+i*8+4,events,2);memory.set(ENTRIES+i*8+6,0x7fff,2)
    initial=memory.snapshot();rawtime=f['timeout']&0xffffffffffffffff;enabled=rawtime!=0xffffffffffffffff;time=rawtime if rawtime<1<<63 else rawtime-(1<<64);round=0
    while True:
        if round>8:raise ValueError('Bounded poll fixture fails to terminate')
        good=0;status=f['rounds'][min(round,len(f['rounds'])-1)]
        for i,(unusedfd,unusedevents) in enumerate(f['entries']):
            fd=memory.get(ENTRIES+i*8);event=memory.get(ENTRIES+i*8+4,2);event=event if event<32768 else event-65536;mask=(event|0xe0)&0xffffffff;mutations=[];checks=[(base,raw)for base,raw in memory.snapshot().items()]
            if f['mutate'] and round==0 and i==0:mutations=[(ENTRIES+4,b'\xff\xff'),(ENTRIES+12,b'\x01\x00')]
            actions.append(dict(address=0x2090138,args=[fd],returned=status[i]&0xffffffff,checks=checks,mutations=mutations,stackWords=[]))
            for at,raw in mutations:memory.put(at,raw)
            value=(status[i]&mask)&0xffffffff;memory.set(ENTRIES+i*8+6,value,2);good+=bool(value)
        if good or (enabled and time<=0):break
        actions.append(dict(address=0x2006b7c,args=[1],returned=0xa7000000+len(actions),checks=[(base,raw)for base,raw in memory.snapshot().items()],mutations=[],stackWords=[]));rawtime=(time-523)&0xffffffffffffffff;time=rawtime if rawtime<1<<63 else rawtime-(1<<64);round+=1
    return dict(initial=initial,regions=memory.snapshot(),args=[ENTRIES,len(f['entries']),f['timeout']&0xffffffff,(f['timeout']>>32)&0xffffffff],actions=actions,result=good,volatileStateReads=None,entryCount=len(f['entries']))
