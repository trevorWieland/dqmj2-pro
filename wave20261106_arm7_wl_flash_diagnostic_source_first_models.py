from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
SRAM=0x04804000


def crc_step(byte,total):
    total^=byte
    for _ in range(8):total=(total>>1)^(0xa001 if total&1 else 0)
    return total&65535


def fixtures():
    rows=[dict(entry=0x027ef4cc,signal=value)for value in [0,1,65535]]
    rows.extend([dict(entry=0x027eb3d0,fault=fault)for fault in ['none','first','all']])
    for length in [0,163,164,165,470,471,65535]:
        for allocated in [False,True]:rows.append(dict(entry=0x027f4ecc,length=length,allocated=allocated))
    for length in [163,164,165,470,471]:
        for good,output in [(True,False),(True,True),(False,True)]:rows.append(dict(entry=0x027f4d38,length=length,good=good,output=output))
    for address,size,null in [(42,0,False),(42,1,False),(43,3,False),(442,32,False),(42,32,True)]:rows.append(dict(entry=0x027f4e1c,address=address,size=size,null=null))
    for statuses in [[0],[1,0],[32,0],[33,1,0],[0x80,0]]:rows.append(dict(entry=0x027f4ddc,statuses=statuses))
    return rows


def scenario(f,ordinal):
    entry=f['entry'];p=Plan(ordinal,{0x027ef4cc:0,0x027eb3d0:8,0x027f4ecc:8,0x027f4d38:24,0x027f4e1c:16,0x027f4ddc:16}[entry]);p.buffer(SRAM,8192,0xa5);reads=[];stores=[];fault='none'
    registers=[0x048080a0,0x048080ac,0x04808004,0x04808012,0x04808010,0x04808194,0x04808040]
    for address in registers:p.constant(address,p16(0x1234))
    if entry==0x027ef4cc:p.u16(CTX+860,f['signal']);p.allowed.extend([(SRAM,SRAM+2),(SRAM+4,SRAM+6)]+[(address,address+2)for address in registers])
    elif entry==0x027eb3d0:p.u16(CTX+830,0x1234);p.allowed.extend([(SRAM,SRAM+8192),(CTX+830,CTX+832)]);fault=f['fault']
    elif entry==0x027f4ecc:
        local=SP-8;p.buffer(local,4,0xa5);p.u32(CTX+788,0x8123abcd);p.u32(CTX+792,GAME);p.allowed.append((CTX+792,CTX+796))
    elif entry==0x027f4d38:
        p.args=[CFM if f['output']else 0];p.u32(CTX+792,OUT);p.u16(OUT+2,f['length']);total=0
        if 164<=f['length']<=470:
            for byte in p.read(OUT+2,f['length']):total=crc_step(byte,total)
        p.u16(OUT,total if f['good']else total^1);p.allowed.append((CFM,CFM+4))
    elif entry==0x027f4e1c:p.args=[f['address'],f['size'],REQ];p.u32(CTX+792,0 if f['null']else OUT);p.allowed.append((REQ,REQ+256))
    else:p.buffer(SP-16,4,0xa5)
    p.capture()
    if entry==0x027ef4cc:
        if f['signal']:
            p.u16(SRAM,0);p.u16(SRAM+4,0);stores=[(SRAM,2,0),(SRAM+4,2,0)];p.regions[0x048080a0]=p16(0x9234);p.mmio=[(0x048080a0,2,0x9234)]
        else:
            p.mmio=[(0x048080ac,2,1),(0x04808004,2,0),(0x04808012,2,2),(0x04808010,2,65535),(0x04808194,2,0),(0x04808040,2,0)]
            for address,_,value in p.mmio:p.regions[address]=p16(value)
    elif entry==0x027eb3d0:
        errors=0;stop=False
        for phase in range(3):
            words=[(65535-i)&65535 if phase==0 else(0x5a5a if i%2==0 else 0xa5a5)if phase==1 else(0xa5a5 if i%2==0 else 0x5a5a)for i in range(4096)]
            for i,value in enumerate(words):
                address=SRAM+2*i;stores.append((address,2,value));actual=value&~1 if fault=='all'or fault=='first'and i==0 else value;p.u16(address,actual)
            for i,value in enumerate(words):
                address=SRAM+2*i;reads.append((address,2))
                if p.r16(address)!=value:
                    previous=errors;errors+=1
                    if previous>32:stop=True;break
            if stop:break
        if errors:p.u16(CTX+830,0x1236)
    elif entry==0x027f4ecc:
        local=SP-8;p.action(0x0380398c,[0x8123abcd]);p.action(0x027f4ddc);p.u32(local,f['length']);p.action(0x027f55c4,[44,2,local],checks=[(local,p32(0))],mutations=[(local,p16(f['length']))]);p.action(0x038039e8,[0x8123abcd]);p.returned=0
        if 164<=f['length']<=470:
            p.u32(local,f['length']+2);p.u32(CTX+792,OUT if f['allocated']else 0);p.action(0x037f886c,[CTX+392,f['length']+2],OUT if f['allocated']else 0)
            if f['allocated']:
                p.u32(CTX+792,OUT+12);p.action(0x0380398c,[0x8123abcd],checks=[(CTX+792,p32(OUT+12))]);p.action(0x027f4ddc);data=bytes((i*7+0x81)&255 for i in range(f['length']+2));p.write(OUT+12,data);p.action(0x027f55c4,[42,f['length']+2,OUT+12],mutations=[(OUT+12,data)]);p.action(0x038039e8,[0x8123abcd]);p.returned=1
    elif entry==0x027f4d38:
        p.returned=2
        if 164<=f['length']<=470:
            total=0
            for i in range(f['length']):byte=p.byte_read(OUT+2+i);previous=total;total=crc_step(byte,total);p.action(0x027eadf4,[byte,previous],total)
            stored=p.r16(OUT)
            if f['output']:p.u32(CFM,(total<<16)|stored)
            p.returned=int(total!=stored)
    elif entry==0x027f4e1c:
        if not f['null']:
            for i in range(f['size']):p.byte_write(REQ+i,p.byte_read(OUT+f['address']-42+i))
    else:
        local=SP-16
        for status in f['statuses']:
            p.write(local,bytes([status]));p.action(0x027f5554,[local],mutations=[(local,bytes([status]))])
            if status&32:p.action(0x027f5c90)
            elif not status&1:break
    result=p.finish();result.update(sramReads=reads,sramWrites=stores,sramFault=fault,instructionBudget=500000 if entry==0x027eb3d0 else 30000);return result
