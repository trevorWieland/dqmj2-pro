from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,BASE,FRAME,REQ,CFM,OUT,p16,p32

ENTRY=0x27f3f40


def fixtures():
    base=dict(entry=ENTRY,mode=1,kind=0,subtype=8,cam=7,multicast=False,fragments=1,duplicate=False,power=0,remaining=0,empty=False,bodyLength=10,psState=32,tx0=0,tx1=0,state=0,peer=False,status=17,mutateFC=False,counter=4)
    rows=[dict(base,empty=True),dict(base,mode=65535,cam=255)]
    for cam in[7,255]:
        for mode in[0,1,2,3,4]:
            for kind,subtype in[(0,15),(1,0),(2,0),(3,15)]:rows.append(dict(base,cam=cam,mode=mode,kind=kind,subtype=subtype))
    for mode,subtypes in[(1,[0,1,2,4,5,8,10,11,12]),(2,[1,3,4,5,8,10,11,12]),(3,[1,3])]:
        for subtype in subtypes:rows.append(dict(base,mode=mode,subtype=subtype,multicast=bool(subtype&1),remaining=bool(subtype&2),fragments=15,power=1))
    for subtype in[0,4,11]:rows.append(dict(base,cam=255,subtype=subtype))
    rows.extend([dict(base,duplicate=True,counter=0xffffffff),dict(base,fragments=0,counter=0xffffffff,multicast=True),dict(base,mutateFC=True),dict(base,cam=0,remaining=2)])
    for state,tx0,tx1 in[(32,0,0),(64,0,0),(64,1,0),(64,0,1),(64,1,1)]:rows.append(dict(base,kind=1,subtype=10,psState=state,tx0=tx0,tx1=tx1))
    for mode,subtype in[(2,14),(2,15),(3,14),(3,15)]:rows.append(dict(base,mode=mode,kind=1,subtype=subtype))
    for subtype,state in[(1,0x51),(3,0x61)]:
        rows.extend([dict(base,mode=2,subtype=subtype,state=state),dict(base,mode=2,subtype=subtype,state=state,peer=True,status=65535)])
    for old,duplicate,allocated in[(32,True,False),(32,False,False),(32,False,True)]:rows.append(dict(base,subtype=2,bodyLength=11,reassDuplicate=duplicate,reassState=old,allocated=allocated))
    return rows


def scenario(f,ordinal):
    p=Plan(ordinal,80);p.u32(CTX+476,0xffffffff if f['empty']else BASE);p.u16(CTX+484,3);p.u16(CTX+848,f['mode']);p.u16(CTX+844,32);p.u16(CTX+942,0x1234);p.u16(CTX+1028,f['state']);p.u32(CTX+1052,REQ);p.u32(CTX+1056,CFM);p.u16(CTX+412,f['tx0']);p.u16(CTX+424,f['tx1']);p.u16(FRAME+6,f['bodyLength']);p.u16(FRAME+8,0x8003|(f['fragments']<<4));p.u16(FRAME+18,0xcd34);fc=f['kind']<<2|f['subtype']<<4|f['power']<<12;p.u16(FRAME+20,fc);p.u16(FRAME+24,0x2230|int(f['multicast']));p.u16(FRAME+42,0x4567);p.u16(FRAME+46,f['status']);p.u16(FRAME+48,0x5678)
    for at in[1376,1380,1384,1400]:p.u32(CTX+at,f['counter'])
    p.capture();p.allowed=[(CTX,CTX+1684),(BASE,BASE+528),(CFM,CFM+128)]
    if f['empty']:return p.finish()
    p.u32(CTX+(1384 if f['multicast']else 1380),f['counter']+1);p.u32(CTX+1376,f['counter']+f['fragments']-1);mutations=[]
    if f['mutateFC']:
        fc=1<<2|10<<4|1<<12;p.u16(FRAME+20,fc);mutations=[(FRAME+20,p16(fc))]
    p.action(0x27eb9b4,[FRAME+30],f['cam'],checks=[(CTX+1376,p.read(CTX+1376,12))],mutations=mutations);cam=f['cam'];p.u16(FRAME+2,0 if cam==255 else cam);duplicate=False
    if cam==255:
        if f['mode']==1 and f['kind']==0:
            target={0:0x27f2f78,4:0x27f3148,11:0x27f35cc}.get(f['subtype'])
            if target:p.action(target,[FRAME],checks=[(FRAME+2,p16(0))])
    else:
        p.action(0x27ebe98,[cam]);p.action(0x27ebd38,[cam,0x34])
        if f['kind']==0:
            p.action(0x27ec08c,[cam],0x4567 if f['duplicate']else 0x4566)
            if f['duplicate']:p.u32(CTX+1400,f['counter']+1);duplicate=True
            else:p.action(0x27ebe58,[cam,0x4567])
        if not duplicate:
            if f['mode']==1:p.action(0x27ebd58,[cam,(fc>>12)&1])
            if f['mode']in[1,2,3]and f['kind']==0:
                subtype=f['subtype'];targets={8:0x27f284c,5:0x27f31fc,10:0x27f2e98,11:0x27f35cc,12:0x27f3b6c}
                if f['mode']==1:targets.update({0:0x27f2f78,4:0x27f3148})
                if subtype in targets:p.action(targets[subtype],[FRAME,0]if subtype==5 else[FRAME])
                elif f['mode']==1 and subtype==2 and f['bodyLength']>10:
                    p.action(0x27f2000,[FRAME+30,0x30],int(f['reassDuplicate']))
                    if not f['reassDuplicate']:
                        p.action(0x27ebfec,[cam],f['reassState']);p.action(0x27f2000,[FRAME+30,0xc0],0);p.action(0x27f1ec8,[FRAME+30,6,1],OUT if f['allocated']else 0)
                        if f['allocated']:p.action(0x27f1088,[OUT])
                elif f['mode']in[2,3]and subtype in[1,3]and f['state']==(0x51 if subtype==1 else 0x61):
                    p.action(0x27ea480,[REQ+16,FRAME+30],int(f['peer']))
                    if f['peer']:
                        p.action(0x27eabec,[]);p.u16(CFM+4,12);p.u16(CFM+6,f['status']);p.u16(CFM+8,0x1234);p.u16(CTX+1028,0x53 if subtype==1 else 0x63);p.action(0x37f8598,[2,3 if subtype==1 else 4],checks=[(CFM+4,p.read(CFM+4,6)),(CTX+1028,p.read(CTX+1028,2))])
            elif f['mode']==1 and f['kind']==1 and f['subtype']==10:
                p.action(0x27ebfec,[cam],f['psState'])
                if f['psState']==64:
                    p.action(0x27ebdf4,[cam])
                    if f['tx1']:p.action(0x27eff00,[1])
                    if f['tx0']:p.action(0x27eff00,[0])
    checks=[(CTX,p.read(CTX,1684)),(BASE,p.read(BASE,528)),(CFM,p.read(CFM,128))];p.u16(CTX+484,f['remaining']);p.action(0x37f8908,[CTX+476,BASE],0x87654321,checks=checks,mutations=[(CTX+484,p16(f['remaining']))])
    if f['remaining']:p.action(0x37f8598,[1,7])
    return p.finish()
