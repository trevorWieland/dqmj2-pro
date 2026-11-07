from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,CFM,p16


def fixtures():
    rows=[]
    for main in [0,1,2,0xffff0001]:
        for use in [0,1]:rows.append(dict(entry=0x027e93ac,main=main,use=use))
    for diversity,use,mode,main in [(d,u,m,a)for d in [0,1,2,0xffff0001]for u in [0,1,2,0xffff0001]for m in [1,2]for a in [0,1]]:
        if (diversity>1 or use>1)and(mode!=1 or main):continue
        rows.append(dict(entry=0x027e9414,diversity=diversity,use=use,mode=mode,main=main))
    for mode,mask,busy,command in [(1,0,0,0),(1,31,1,0),(1,2,0,1),(2,0,0,1),(2,31,0,0),(2,31,1,0),(3,31,0,0),(65535,31,0,1),(1,8,0,1),(1,16,0,1)]:rows.append(dict(entry=0x027eaf7c,mode=mode,mask=mask,busy=busy,command=command))
    for state,mlme,tasks,race in [(0,0,[],False),(0,0x35,[4],False),(32,0,[],False),(32,0x35,[],False),(64,0x35,[4,7,9],False),(64,0x35,[4],True)]:rows.append(dict(entry=0x027eb13c,state=state,mlme=mlme,tasks=tasks,race=race))
    return rows


def scenario(f,ordinal):
    entry=f['entry'];p=Plan(ordinal,0 if entry in [0x027e93ac,0x027e9414]else 16);p.constant(0x04808290,p16(0xa5b6));p.constant(0x04808004,p16(f.get('command',0)));p.u16(CTX+826,0xa5c7);p.returned=None
    if entry==0x027e93ac:p.args=[f['main']];p.u16(CTX+826,0xa5c7|(32 if f['use']else 0));p.allowed.extend([(CTX+826,CTX+828),(0x04808290,0x04808292)])
    elif entry==0x027e9414:p.args=[f['diversity'],f['use']];p.u16(CTX+826,0xa5c7|(8 if f['main']else 0));p.u16(CTX+814,f['mode']);p.allowed.extend([(CTX+826,CTX+828),(0x04808290,0x04808292)])
    elif entry==0x027eaf7c:p.u16(CTX+848,f['mode']);p.u16(CTX+1108,f['busy']);p.u16(CTX+942,0x8123);p.u16(CTX+1020,65535);p.allowed.extend([(CTX+1020,CTX+1022),(0x04808004,0x04808006)])
    else:p.u16(CTX+830,0x1234);p.u16(CTX+844,f['state']);p.u16(CTX+1028,f['mlme']);p.u32(CTX+1056,CFM);p.allowed.extend([(CTX+830,CTX+832),(CTX+1028,CTX+1030),(CFM+4,CFM+6)])
    p.capture()
    if entry==0x027e93ac:
        p.returned=5 if f['main']>1 else 0
        if not p.returned:
            p.u16(CTX+826,(p.r16(CTX+826)&~8)|(f['main']<<3));value=f['use']^f['main'];p.regions[0x04808290]=p16(value);p.mmio=[(0x04808290,2,value)]
    elif entry==0x027e9414:
        p.returned=5 if f['diversity']>1 or f['use']>1 else 11 if f['diversity']==1 and f['mode']!=1 else 0
        if not p.returned:
            use=f['use']if f['diversity']==0 else 0;p.u16(CTX+826,(p.r16(CTX+826)&~(16|32))|(use<<5)|(f['diversity']<<4));value=use^f['main'];p.regions[0x04808290]=p16(value);p.mmio=[(0x04808290,2,value)]
    elif entry==0x027eaf7c:
        def check(address,bit):value=int(bool(f['mask']&(1<<bit)));p.action(0x027eae74,[address],value);return value
        if f['mode']==1:
            if check(CTX+1188,0):p.action(0x027eaef4);p.action(0x027f1210)
            if check(CTX+1108,1):p.action(0x027eaf30,[CTX+1108])
        elif f['mode']==2:
            check(CTX+1168,2)
            if check(CTX+1108,1):
                if f['busy']:p.action(0x027eaef4)
                p.action(0x027f1f5c,[0x8123]);p.u16(CTX+1020,0)
        if check(CTX+1088,3):p.action(0x027eaf30,[CTX+1088])
        if check(CTX+1068,4):p.action(0x027eaf30,[CTX+1068])
        if f['command']==0:p.regions[0x04808004]=p16(1);p.mmio=[(0x04808004,2,1)]
    else:
        p.u16(CTX+830,0x9234)
        if f['state']:
            changed=[]
            if f['race']:p.u16(CTX+1028,0);changed=[(CTX+1028,p16(0))]
            p.action(0x037f9198,checks=[(CTX+830,p16(0x9234))],mutations=changed)
            if f['mlme']and not f['race']:p.u16(CTX+1028,0);p.u16(CFM+4,6);p.action(0x027edb20,checks=[(CTX+1028,p16(0)),(CFM+4,p16(6))])
            p.action(0x027e9d00)
        for task in f['tasks']+[65535]:p.action(0x037f8650,[3],task)
        p.action(0x037f8598,[3,23])
    return p.finish()
