from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32


def fixtures():
    rows=[dict(entry=0x027e97bc,channel=channel,random=random)for channel,random in [(0,0),(65535,0x1234),(0x8001,65535)]]
    rows.extend(dict(entry=0x027e9d88,rf=rf,bbp=bbp)for rf in [0,1,2,3,5,65535]for bbp in [0,0x12ff])
    rows.extend(dict(entry=entry,time=value,callback=callback)for entry in [0x027eab68,0x027eaaf8]for value in [0,1,63,64,1000,0x80000001,0xffffffff]for callback in [0x027ea9a8,0x037f84e0])
    rows.extend(dict(entry=0x027e9e3c,life=life,beacon=beacon)for life,beacon in [(0,0),(1,1),(5,100),(65535,65535),(6553600,1),(6553700,1),(0x80000000,2),(0xffffffff,65535),(0x10001,1)])
    rows.extend(dict(entry=0x027e89ec,crc=crc,dma=dma,cam=cam,irq=irq)for crc,dma,cam,irq in [(0,0,0,False),(0,1,27,False),(0,2,28,False),(0,0xffffffff,0xffffffff,True),(1,32,57,False),(2,0x80000000,56,True),(0xffffffff,1024,1,False)])
    return rows


def scenario(f,ordinal):
    entry=f['entry'];p=Plan(ordinal,{0x027e97bc:16,0x027e9d88:8,0x027eab68:16,0x027eaaf8:16,0x027e9e3c:16,0x027e89ec:24}[entry]);reads=[]
    if entry==0x027e97bc:
        p.buffer(SP-16,8,0xa5);p.constant(0x04808044,p16(f['random']));p.allowed.append((CTX+856,CTX+858))
    elif entry==0x027e9d88:
        p.u16(CTX+1528,f['rf'])
        for offset,value in [(0x36,0x1234),(0x168,0x5678),(0x158,0xabcd),(0x15c,f['bbp'])]:p.constant(0x04808000+offset,p16(value));p.allowed.append((0x04808000+offset,0x04808002+offset))
    elif entry in [0x027eab68,0x027eaaf8]:p.args=[f['time'],f['callback']];p.buffer(SP-16,4,0xa5)
    elif entry==0x027e9e3c:p.args=[f['life']];p.u16(CTX+946,f['beacon']);p.allowed.extend([(CTX+824,CTX+826),(CTX+976,CTX+978)])
    else:
        p.args=[REQ];p.buffer(SP-24,12,0xa5);fields={0:CTX,4:OUT+512,8:512,12:0x81234567,16:CFM,20:GAME,24:0x80000003,28:f['dma'],32:0x1234,44:OUT,48:f['cam']}
        for offset,value in fields.items():p.u32(REQ+offset,value)
        p.constant(0x04000304,p16(0x8001));p.constant(0x04000206,p16(0xa5a5));p.allowed.extend([(0x0380fff4,0x0380fff8),(CTX,CTX+1684),(0x04000304,0x04000306),(0x04000206,0x04000208)])
    p.capture()
    if entry==0x027e97bc:
        local=SP-16;mac=bytes.fromhex('01ab2389cd45');p.action(0x027f4e1c,[54,6,local+2],mutations=[(local+2,mac)]);p.write(local+2,mac);p.action(0x027f4e1c,[60,2,local],mutations=[(local,p16(f['channel']))]);p.u16(local,f['channel'])
        calls=[(0x027e8e68,[local+2]),(0x027e8ec8,[7]),(0x027e8efc,[f['channel']&0x7ffe]),(0x027e8f3c,[2]),(0x027e8fbc,[0]),(0x027e8ff0,[0]),(0x027e9090,[0]),(0x027e90b4,[0x027f730c]),(0x027e96ec,[500]),(0x027e9114,[0]),(0x027e914c,[0]),(0x027e9184,[16]),(0x027e91bc,[65535,0]),(0x027e926c,[0x027f72ac]),(0x027e929c,[1]),(0x027e9344,[0]),(0x027e9b98,[0x027f72a8]),(0x027e9368,[0,31]),(0x027e9e3c,[5]),(0x027e9414,[0,0]),(0x027e93ac,[0]),(0x027e94e8,[0]),(0x027e9528,[0])]
        for address,args in calls:
            checks=[(local+2,mac)]if address==0x027e8e68 else[(0x027f730c,bytes(80))]if address==0x027e90b4 else[(0x027f72ac,bytes(32))]if address==0x027e926c else[(0x027f72a8,p16(3)+p16(3))]if address==0x027e9b98 else[];p.action(address,args,0x80000000+address,checks=checks)
        p.action(0x027ead78,[f['random']+(f['random']<<8),f['random']]);p.u16(CTX+856,1);reads=[(0x04808044,2,f['random'])]*3
    elif entry==0x027e9d88:
        p.mmio=[(0x04808036,2,0)];p.regions[0x04808036]=p16(0);p.action(0x037fb32c,[8000,0x027ea9a8]);p.mmio.append((0x04808168,2,0));p.regions[0x04808168]=p16(0)
        if f['rf']==2:
            p.mmio.append((0x04808158,2,0x6001));p.regions[0x04808158]=p16(0x6001);p.action(0x037fb420,[],0xffffffff);reads=[(0x0480815c,2,f['bbp'])];p.action(0x027ea5fc,[1,f['bbp']&127]);p.action(0x027ea5fc,[1,f['bbp']]);p.action(0x037fb32c,[40000,0x027ea9a8]);p.action(0x027ea7cc)
        elif f['rf']==3:p.action(0x027ea7cc)
    elif entry in [0x027eab68,0x027eaaf8]:
        alarm=CTX+1588;p.action(0x037fd5c0,[alarm]);ticks=(33514*f['time'])//64
        if entry==0x027eab68:
            quotient=ticks//1000;p.action(0x03806bf0,[ticks&0xffffffff,ticks>>32,1000,0],quotient&0xffffffff);p.actions[-1]['returnedHigh']=quotient>>32;ticks=quotient
        p.u32(SP-16,0);p.action(0x037fd4dc,[alarm,ticks&0xffffffff,ticks>>32,f['callback'],0])
    elif entry==0x027e9e3c:
        p.returned=0
        if f['life']==65535:p.u16(CTX+824,65535);p.u16(CTX+976,65535)
        else:
            product=(f['life']*f['beacon'])&0xffffffff;value=product//100;p.action(0x03806e44,[product,100],value)
            if value>65536:p.returned=5
            else:p.u16(CTX+824,f['life']&65535);p.u16(CTX+976,value&65535)
    else:
        local=SP-24;p.action(0x037fe014,[0,CTX,1684],checks=[(0x0380fff4,p32(CTX))],mutations=[(CTX,bytes(1684))]);p.write(CTX,bytes(1684));p.action(0x037fbbfc,[],0x8123abcd);p.u32(CTX+788,0x8123abcd);p.u32(CTX+780,0x80000003);count=f['dma']//2;p.u32(CTX+784,count if count else 0xffffffff);p.action(0x027e8c78,[REQ+32]);p.action(0x027f4ecc,[],0);p.mmio=[(0x04000304,2,0x8003),(0x04000206,2,0x30)];p.regions[0x04000304]=p16(0x8003);p.regions[0x04000206]=p16(0x30);reads=[(0x04000304,2,0x8001)];p.u32(CTX+1676,3)
        p.action(0x027f4e1c,[60,2,CTX+1682],mutations=[(CTX+1682,p16(0x8123))]);p.u16(CTX+1682,0x8123);p.action(0x027f4e1c,[62,2,CTX+1680],mutations=[(CTX+1680,p16(0x4567))]);p.u16(CTX+1680,0x4567);p.u32(CTX+776,CFM);p.u32(CTX+772,GAME);p.action(0x03806e44,[f['cam'],28],f['cam']//28);p.action(0x027e8de8,[OUT,f['cam']//28])
        for address in [0x027e8bd0,0x027ec6f0,0x027ee0bc,0x027ec480,0x027ea954]:p.action(address)
        p.action(0x027f4d38,[local+8],f['crc'],mutations=[(local+8,p32(0x89abcdef))]);p.u32(local+8,0x89abcdef)
        if f['crc']:p.u16(CTX+830,0x80)
        else:
            for address in [0x027ea6bc,0x027eb22c,0x027e9d88,0x027ea72c,0x027ea7cc,0x027eb3d0,0x027eb55c,0x027ea764,0x027e97bc,0x027e9d00]:p.action(address)
        p.u32(local,512);p.u32(local+4,0x81234567);p.action(0x037fc054,[CTX+24,0x037f84e0,0,OUT+512,512,0x81234567]);p.action(0x037fc36c,[CTX+24]);status=0x7001 if f['irq']else p.r16(CTX+830);p.action(0x027eb8c8,[],checks=[(CTX+830,p16(p.r16(CTX+830)))],mutations=[(CTX+830,p16(status))]if f['irq']else[]);p.u16(CTX+830,status);p.returned=status
    result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=reads,faultRegisters=[],instructionBudget=30000);return result
