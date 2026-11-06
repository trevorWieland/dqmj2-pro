from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,BASE,FRAME,REQ,CFM,OUT,GAME,p16,p32


def fixtures():
    scan=dict(entry=0x027ec7f8,mode=2,sta=32,length=1,scan=0,channels=[1,0],duration=10,masks=1,disabled=0,confirmLength=40);rows=[scan]
    for field,values in [('mode',[0,1,3,65535]),('sta',[31]),('length',[0,32,33]),('scan',[1,2]),('channels',[[0],[1,15,0],list(range(1,17))]),('duration',[9,1000,1001]),('masks',[16,17]),('disabled',[1]),('confirmLength',[0,65535])]:rows.extend([{**scan,field:value}for value in values])
    rows.extend([dict(entry=0x027ed634,arg=0),dict(entry=0x027ed634,arg=0xdeadbeef)])
    for length in [0,1,2,3,16]:
        for align in [0,1,3]:rows.append(dict(entry=0x027edfa0,length=length,align=align,allocated=True))
    rows.append(dict(entry=0x027edfa0,length=8,align=0,allocated=False))
    for sta,match1,match2 in [(32,True,True),(64,False,True),(64,True,False),(64,True,True)]:
        for high in [False,True]:rows.append(dict(entry=0x027f2778,sta=sta,match1=match1,match2=match2,high=high,mpdu=27 if high else 256))
    for duplicate,multicast,status,respond,matched,allocated in [(True,True,0,False,True,True),(False,False,0,False,True,True),(False,True,0,False,False,True),(False,True,0,False,True,False),(False,True,0,False,True,True),(False,False,0x8000,True,True,True)]:rows.append(dict(entry=0x027f3148,duplicate=duplicate,multicast=multicast,status=status,respond=respond,matched=matched,allocated=allocated))
    from wave20261106_arm7_wl_followon_source_receive_auth import fixtures as auth_fixtures
    return rows+auth_fixtures()


def scenario(f,ordinal):
    if f['entry']==0x027f35cc:
        from wave20261106_arm7_wl_followon_source_receive_auth import scenario as auth_scenario
        return auth_scenario(f,ordinal)
    entry=f['entry'];p=Plan(ordinal,{0x027ec7f8:24,0x027ed634:8,0x027edfa0:24,0x027f2778:16,0x027f3148:56}[entry]);p.args=[FRAME]
    if entry==0x027ec7f8:
        p.args=[REQ,CFM];p.u16(CTX+814,f['mode']);p.u16(CTX+844,f['sta']);p.u16(REQ+22,f['length']);p.u16(REQ+56,f['scan']);channels=bytes(f['channels'])+bytes(16-len(f['channels']));p.write(REQ+58,channels);p.u16(REQ+74,f['duration']);p.u16(REQ+76,f['masks']);p.u16(CFM+2,f['confirmLength']);p.capture();p.allowed.extend([(CTX+1028,CTX+1034),(CTX+1052,CTX+1060),(CFM+2,CFM+4)]);p.u16(CTX+1032,f['confirmLength']-3);p.u16(CFM+2,3);p.returned=128
        if f['mode']not in [1,2,3]:p.returned=11
        elif f['sta']<32:p.returned=1
        elif f['length']>32 or f['scan']>1:p.returned=5
        else:
            first=p.byte_read(REQ+58)
            if first==0 or f['duration']>1000 or f['duration']<10 or f['masks']>16:p.returned=5
            else:
                for i,value in enumerate(channels):
                    p.byte_read(REQ+58+i)
                    if value==0:break
                    enabled=int(value!=f['disabled']);p.action(0x027ea4b0,[value],enabled)
                    if not enabled:p.returned=5;break
                if p.returned==128:
                    p.action(0x027e9578,[REQ+16]);p.action(0x027e95dc,[f['length'],REQ+24]);p.u32(CTX+1052,REQ);p.u32(CTX+1056,CFM);p.u16(CTX+1028,16);p.action(0x037f8598,[2,0],checks=[(CTX+1028,p16(16))])
    elif entry==0x027ed634:
        p.args=[f['arg']];p.u32(CTX+1056,CFM);p.capture();p.allowed.extend([(CFM+4,CFM+6),(CTX+1028,CTX+1030)]);p.u16(CFM+4,7);p.u16(CTX+1028,0x35);p.action(0x037f8598,[2,2],checks=[(CFM+4,p16(7)),(CTX+1028,p16(0x35))])
    elif entry==0x027edfa0:
        p.u16(CTX+996,f['length']);p.u32(CTX+992,GAME);p.u16(CTX+998,f['align']);p.u16(FRAME+18,0xab34);p.u16(FRAME+14,0xcd56);p.capture();p.allowed.append((OUT,OUT+62+f['length']));p.action(0x037f886c,[CTX+392,62+f['length']],OUT if f['allocated']else 0);p.returned=int(f['allocated'])
        if not f['allocated']:p.action(0x027eb078,[1])
        else:
            p.u16(OUT+12,0x8d);p.u16(OUT+14,22+(f['length']+1)//2);p.byte_write(OUT+31,0x34);p.byte_write(OUT+30,0x56);raw=p.read(FRAME+30,6);p.write(OUT+46,raw);p.action(0x027ea0ec,[OUT+46,FRAME+30],mutations=[(OUT+46,raw)]);p.u16(OUT+22,f['length'])
            if f['length']:
                if f['align']&1:
                    for i in range(f['length']):p.byte_write(OUT+60+i,p.byte_read(GAME+1+i))
                else:p.copy16(GAME,OUT+60,f['length']+1)
            p.action(0x037f8d58,[CTX+392,OUT],checks=[(OUT,p.read(OUT,62+f['length']))])
    elif entry==0x027f2778:
        p.u16(CTX+844,f['sta']);p.u16(CTX+1250,0x123);p.write(CTX+936,b'ABCDEF');p.write(CTX+966,b'abcdef');p.write(FRAME+30,b'ABCDEF'if f['match1']else b'123456');p.write(FRAME+36,b'abcdef'if f['match2']else b'654321');p.u16(FRAME+16,f['mpdu']);p.u16(BASE+24,0x4200);p.constant(0x04808098,p16(0x9234 if f['high']else 0x1234));p.constant(0x04808094,p16(0xa567 if f['high']else 0x2567));p.capture();p.returned=1;p.allowed.extend([(FRAME+6,FRAME+8),(BASE+12,BASE+16),(BASE+24,BASE+26)])
        if f['sta']==64:
            p.action(0x027ea480,[FRAME+30,CTX+936],int(f['match1']))
            if f['match1']:
                p.action(0x027ea480,[FRAME+36,CTX+966],int(f['match2']))
                if f['match2']:
                    p.u16(FRAME+6,f['mpdu']-28);p.u16(BASE+12,0x185);p.u16(BASE+14,24);p.u16(BASE+24,0x4200|0x123|(0x1800 if f['high']else 0));p.action(0x037f8d58,[CTX+392,BASE],checks=[(BASE,p.read(BASE,64))]);p.returned=0
    else:
        checker=SP-56;p.buffer(checker,44,0xa5);p.u16(FRAME+36,3 if f['multicast']else 2);p.u16(FRAME+8,f['status']);p.u16(FRAME+6,32);p.u16(CTX+826,0xa5a4|(2 if f['respond']else 0));p.capture();p.action(0x027f2000,[FRAME+30,0x50],int(f['duplicate']))
        if not f['duplicate']and(f['multicast']or f['status']&0x8000):
            p.write(checker,bytes(44));p.action(0x037fdfd0,[0,checker,44],mutations=[(checker,bytes(44))]);p.u32(checker,FRAME+44);p.u16(checker+8,32);p.u16(checker+12,0 if f['respond']else 0x800);p.u16(checker+10,int(f['matched']));p.action(0x027f3c1c,[checker],checks=[(checker,p32(FRAME+44)),(checker+8,p16(32)),(checker+12,p16(0 if f['respond']else 0x800))],mutations=[(checker+10,p16(int(f['matched'])))])
            if f['matched']:
                p.action(0x027f1be8,[FRAME+30],OUT if f['allocated']else 0)
                if f['allocated']:p.action(0x027f1088,[OUT])
    return p.finish()
