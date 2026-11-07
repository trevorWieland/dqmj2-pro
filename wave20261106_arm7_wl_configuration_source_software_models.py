from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,BASE,FRAME,REQ,CFM,OUT,GAME,p16,p32
TABLE=0x02718000
QUEUE=0x0271e000


def fixtures():
    rows=[]
    for count,nodes in [(0,2),(1,0),(1,1),(3,3)]:rows.append(dict(entry=0x027e8da8,count=count,nodes=nodes))
    for number in [0,1,16,0xffff0010]:rows.append(dict(entry=0x027e8de8,number=number,game=GAME))
    for mode in [0,1,2,3,4,65535]:rows.append(dict(entry=0x027e8f3c,mode=mode))
    for length in [0,1,31,32,33]:
        for state,mode,previous,offset in [(32,1,32,12),(64,1,length,12),(64,1,length,0),(64,1,(length+1)&65535,12),(64,2,0,12)]:rows.append(dict(entry=0x027e95dc,length=length,state=state,mode=mode,previous=previous,offset=offset))
    for period in [0,9,10,1000,1001,65535]:rows.append(dict(entry=0x027e96ec,period=period))
    for length in [0,1,2,3,128,129,0xffff0080]:
        for align in [0,1,3]:rows.append(dict(entry=0x027e9f60,length=length,align=align))
    for cam,race in [(0,False),(1,False),(15,False),(3,True)]:rows.append(dict(entry=0x027ea048,cam=cam,race=race))
    for nodes,successes in [(0,0),(1,0),(1,1),(3,1),(3,3)]:rows.append(dict(entry=0x027ec690,nodes=nodes,successes=successes))
    for number in [0,1,15,16,65535]:
        for frameLife in [0,1,63,64,65535]:rows.append(dict(entry=0x027ee438,number=number,frameLife=frameLife,camLife=0x8123))
    return rows


def scenario(f,ordinal):
    entry=f['entry'];p=Plan(ordinal,{0x027e8da8:16,0x027e8de8:16,0x027e8f3c:8,0x027e95dc:32,0x027e96ec:8,0x027e9f60:24,0x027ea048:8,0x027ec690:24,0x027ee438:8}[entry]);p.buffer(TABLE,448,0xa5);p.returned=None
    if entry==0x027e8da8:
        p.args=[REQ];p.u32(REQ,OUT if f['nodes']else 0xffffffff);p.u16(REQ+8,f['count'])
        for i in range(f['nodes']):p.u32(OUT+32*i+4,OUT+32*(i+1)if i+1<f['nodes']else 0xffffffff)
    elif entry==0x027e8de8:p.args=[TABLE,f['number']];p.u32(CTX+992,f['game']);p.allowed.extend([(CTX+796,CTX+804),(CTX+992,CTX+996)])
    elif entry==0x027e8f3c:p.args=[f['mode']];p.u16(CTX+850,0x8123);p.u32(CTX+832,0x12340001);p.constant(0x04808006,p16(0xa5f5));p.allowed.extend([(CTX+814,CTX+816),(CTX+848,CTX+850),(CTX+832,CTX+836),(0x04808006,0x04808008)])
    elif entry==0x027e95dc:p.args=[f['length'],REQ];p.u16(CTX+844,f['state']);p.u16(CTX+814,f['mode']);p.u16(CTX+866,f['previous']);p.u16(CTX+982,f['offset']);p.u32(CTX+1196,FRAME);p.allowed.extend([(CTX+866,CTX+900),(FRAME,FRAME+512)])
    elif entry==0x027e96ec:p.args=[f['period']];p.u16(CTX+824,0xffff);p.constant(0x0480808c,p16(0xa5b6));p.allowed.extend([(CTX+946,CTX+948),(0x0480808c,0x0480808e)])
    elif entry==0x027e9f60:p.args=[f['length'],REQ];p.u16(CTX+998,f['align']);p.u32(CTX+992,GAME);p.allowed.extend([(CTX+996,CTX+998),(CTX+1000,CTX+1002),(GAME,GAME+256)])
    elif entry==0x027ea048:p.u16(CTX+942,0x8123);p.u16(CTX+972,f['cam']);p.constant(0x0480802a,p16(0xa5b6));p.allowed.extend([(CTX+942,CTX+944),(CTX+972,CTX+974),(0x0480802a,0x0480802c)])
    elif entry==0x027ec690:
        p.u32(CTX+772,QUEUE);p.u32(CTX+500,OUT if f['nodes']else 0xffffffff);p.u16(CTX+508,f['nodes'])
    else:
        p.args=[REQ,CFM];p.u32(CTX+796,TABLE);p.u16(CTX+802,16);p.u16(REQ+16,f['number']);p.u16(REQ+18,f['camLife']);p.u16(REQ+20,f['frameLife']);p.allowed.extend([(CFM+2,CFM+4),(TABLE,TABLE+448)])
        for i in range(16):p.u16(TABLE+i*28+24,[0,1,65535][i%3])
    p.capture()
    if entry==0x027e8da8:
        if f['count']:
            for i in range(f['nodes']):
                address=OUT+32*i;nextAddress=OUT+32*(i+1)if i+1<f['nodes']else 0xffffffff;p.u32(address+4,0xdeadc0de);p.u32(REQ,nextAddress);p.u16(REQ+8,max(0,f['count']-i-1));p.action(0x037f8908,[REQ,address],mutations=[(address+4,p32(0xdeadc0de)),(REQ,p32(nextAddress)),(REQ+8,p16(max(0,f['count']-i-1)))])
    elif entry==0x027e8de8:
        for address,size in [(CTX+796,40),(CTX+836,192)]:p.write(address,bytes(size));p.action(0x037fdf74,[0,address,size],mutations=[(address,bytes(size))])
        p.u32(CTX+796,TABLE);p.u16(CTX+800,f['number']);p.u16(CTX+802,f['number']);p.u32(CTX+992,f['game'])
    elif entry==0x027e8f3c:
        p.returned=5 if f['mode']>3 else 0
        if not p.returned:
            p.u16(CTX+814,f['mode']);p.u16(CTX+848,f['mode']);word=(0xa5f5&~7)|f['mode'];p.regions[0x04808006]=p16(word);p.mmio=[(0x04808006,2,word)];p.action(0x027e9c58,[0x8123],returned=5,checks=[(CTX+814,p16(f['mode'])),(CTX+848,p16(f['mode'])),(0x04808006,p16(word))]);p.u32(CTX+832,0x12340009)
    elif entry==0x027e95dc:
        length=f['length'];p.returned=0
        if length>32:p.returned=5
        elif f['state']==64 and f['mode']==1 and f['previous']!=length:p.returned=6
        else:
            for i in range(length):p.byte_write(CTX+868+i,p.byte_read(REQ+i))
            for i in range(length,32):p.byte_write(CTX+868+i,0)
            p.u16(CTX+866,length)
            if f['state']==64 and f['mode']==1 and f['offset']:
                for i in range(length):p.byte_write(FRAME+38+f['offset']+i,p.byte_read(CTX+868+i))
    elif entry==0x027e96ec:
        p.returned=0 if 10<=f['period']<=1000 else 5
        if not p.returned:p.u16(CTX+946,f['period']);p.regions[0x0480808c]=p16(f['period']);p.mmio=[(0x0480808c,2,f['period'])];p.action(0x027e9e3c,[65535],returned=5)
    elif entry==0x027e9f60:
        length=f['length'];p.returned=4 if length>128 else 0
        if not p.returned:
            if length:
                if f['align']&1:
                    p.byte_write(GAME,255)
                    for i in range(length):p.byte_write(GAME+1+i,p.byte_read(REQ+i))
                else:p.copy16(REQ,GAME,length+1)
            p.u16(CTX+996,length);p.u16(CTX+1000,1)
    elif entry==0x027ea048:
        p.u16(CTX+942,0);p.action(0x037fb3b4,checks=[(CTX+942,p16(0))]);p.regions[0x0480802a]=p16(0);p.mmio=[(0x0480802a,2,0)]
        if f['cam']:
            cam=f['cam'];changed=[]
            if f['race']:cam=4;p.u16(CTX+972,cam);changed=[(CTX+972,p16(cam))]
            p.action(0x027f0d6c,[f['cam']],mutations=changed);p.action(0x027ebc50,[cam,32]);p.u16(CTX+972,0)
    elif entry==0x027ec690:
        for i in range(f['nodes']):
            address=OUT+32*i;success=i<f['successes'];p.action(0x037fc6d4,[QUEUE,address,0],int(success))
            if not success:break
            nextAddress=OUT+32*(i+1)if i+1<f['nodes']else 0xffffffff;p.u32(CTX+500,nextAddress);p.u16(CTX+508,f['nodes']-i-1);p.action(0x037f87ac,[CTX+500,address],mutations=[(CTX+500,p32(nextAddress)),(CTX+508,p16(f['nodes']-i-1))])
    else:
        p.u16(CFM+2,1);p.returned=0
        if (f['number']>=16 and f['number']!=65535)or(f['frameLife']>63 and f['frameLife']!=65535):p.returned=5
        else:
            indices=range(1,16)if f['number']==65535 else[f['number']]if f['number']else[]
            for i in indices:
                p.u16(TABLE+i*28+26,f['camLife'])
                if p.r16(TABLE+i*28+24):p.u16(TABLE+i*28+24,f['camLife'])
            if f['frameLife']:p.action(0x027e9e3c,[f['frameLife']],returned=5)
    return p.finish()
