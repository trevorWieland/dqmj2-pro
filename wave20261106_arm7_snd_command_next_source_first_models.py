from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
QUEUE=0x03809060
SLOT=0x03807edc
WORK_DATA=0x03807ee0
SHARED0=0x02720000
SHARED1=0x02720800
INFO=0x02722000
COMMANDS=0x02726000


def arguments(identifier,variant):
    values=[0x81234567,0x89abcdef,0xcafedcba,0xfedc9876]if variant else[0x00030005,0x07654321,0x3210a5c3,0x7521b4d6]
    if identifier==29:values[0]=SHARED1
    if identifier==33:values[0]=INFO
    return values


def fixtures():
    rows=[dict(entry=0x03801f1c,messages=[[[identifier,arguments(identifier,variant)]]],tag=0xfffffffe)for identifier in range(34)for variant in [0,1]]
    rows.extend(dict(entry=0x03801f1c,messages=[[[identifier,[mask,cap,alarm,0x87654321]]]],tag=0xffffffff)for identifier in [12,13]for mask,cap,alarm in [(0,0,0),(1,1,1),(0x8000,2,0x80),(0xffff,3,0xff),(0x80000000,7,0x80000000)])
    rows.extend(dict(entry=0x03801f1c,messages=[[[identifier,arguments(0,1)]]],tag=0xffffffff)for identifier in [34,255,0xffffffff])
    rows.extend([dict(entry=0x03801f1c,messages=[],tag=0xffffffff),dict(entry=0x03801f1c,messages=[[]],tag=0xffffffff),dict(entry=0x03801f1c,messages=[[[0,arguments(0,0)],[1,arguments(1,1)]],[[29,arguments(29,0)],[31,arguments(31,0)]]],tag=0xffffffff,mutate=True),dict(entry=0x03801f1c,messages=[[[identifier,arguments(identifier,1)]for identifier in range(34)]],tag=0xffffffff)])
    rows.extend(dict(entry=0x03801f1c,messages=[[[identifier,[mask,0xfedcba98,3,0]]]],tag=0xfffffffe)for identifier in [19,20,21]for mask in [0x8000,0,0x80000000])
    return rows


def scenario(f,ordinal):
    p=Plan(ordinal,88);p.buffer(SP-88,52,0xa5);p.buffer(SHARED0,640,0x5a);p.buffer(SHARED1,640,0xa5);p.u32(SHARED0,f['tag']);p.u32(SHARED1,8);p.constant(SLOT,p32(SHARED0));p.buffer(WORK_DATA,4480);p.buffer(QUEUE,32);p.buffer(INFO,4576,0xa5);p.buffer(COMMANDS,8192,0x77);p.allowed.extend([(SLOT,SLOT+4),(SHARED0,SHARED0+4),(SHARED1,SHARED1+4),(INFO,INFO+4576)])
    for ch in range(16):p.constant(0x04000403+16*ch,bytes([0x23+ch]));p.allowed.append((0x04000403+16*ch,0x04000404+16*ch))
    p.constant(0x04000508,bytes.fromhex('2a55'));p.allowed.append((0x04000508,0x0400050a));messages=[];nextIndex=0
    for message in f['messages']:
        commands=[]
        for identifier,args in message:
            address=COMMANDS+32*nextIndex;nextIndex+=1;commands.append((address,identifier,args))
        for i,(address,identifier,args)in enumerate(commands):p.write(address,b''.join(map(p32,[(commands[i+1][0]if i+1<len(commands)else 0),identifier,*args])))
        messages.append(commands)
    p.capture();reads=[];currentShared=SHARED0;mutated=False
    def call(address,args=(),returned=0,checks=(),mutations=()):
        nonlocal mutated
        changes=list(mutations)
        if f.get('mutate')and not mutated and address==0x03800310:
            changes.append((COMMANDS,p32(0)+p32(0xffffffff)+bytes(16)));p.write(COMMANDS,changes[-1][1]);mutated=True
        for i,value in enumerate(args[4:]):p.u32(SP-88+4*i,value)
        p.action(address,list(args),returned,checks=checks,mutations=changes)
    def mmio(address,width,value):
        p.mmio.append((address,width,value));raw=int(value).to_bytes(width,'little')
        if address in [0x04000508,0x04000509]:
            pair=bytearray(p.regions[0x04000508]);pair[address-0x04000508:address-0x04000508+width]=raw;p.regions[0x04000508]=bytes(pair)
        else:p.regions[address]=raw
    def capture_start(cap):
        raw=p.regions[0x04000508]
        if cap&3==3:
            old=int.from_bytes(raw,'little');reads.append((0x04000508,2,old));mmio(0x04000508,2,old|0x8080)
        elif cap&3:
            index=0 if cap&1 else 1;address=0x04000508+index;old=raw[index];reads.append((address,1,old));mmio(address,1,old|128)
    for commands in messages:
        head=commands[0][0]if commands else 0;p.u32(SP-64,head);call(0x037fc760,[QUEUE,SP-64,0],1,mutations=[(SP-64,p32(head))])
        for address,identifier,args in commands:
            copied=p.read(address,24);p.write(SP-60,copied);a,b,c,d=args
            direct={0:(0x03800310,[a,b,c,d]),1:(0x03800340,[a]),2:(0x038000b4,[a,b,c,d]),3:(0x038002f0,[a]),4:(0x0380039c,[a,b]),5:(0x03800414,[a,b]),6:(0x038006a4,[a,b,c,d]),7:(0x038006e8,[a&0xffffff,b,c,d,a>>24]),8:(0x038004e0,[a,b,c]),9:(0x0380054c,[a,b,c]),10:(0x03801c50,[a,b,((c&65535)|0xffff0000)if c&0x8000 else c&65535]),11:(0x03801c70,[a,((b&65535)|0xffff0000)if b&0x8000 else b&65535]),14:(0x037fe804,[a&65535,b&0x7ffffff,(d>>24)&3,(d>>26)&3,d&65535,c&0x3fffff,(c>>24)&127,(c>>22)&3,a>>16,(d>>16)&127]),15:(0x037fe8d0,[a,d,b&127,(b>>8)&3,(c>>8)&65535,c&127]),16:(0x037fe97c,[a,b&127,(b>>8)&3,(c>>8)&65535,c&127]),17:(0x037ff0fc,[(c>>31)&1,(c>>30)&1,a,b,(c>>29)&1,(c>>28)&1,(c>>27)&1]),18:(0x03801d50,[a,b,0,c,0,d]),22:(0x037febe0,[a]),23:(0x037fe7bc,[a]),24:(0x037feb6c,[a]),25:(0x037fe7cc,[a,b,c,d]),26:(0x037ffbe0,[a,b]),27:(0x037ffcc0,[a,b]),28:(0x037ffb30,[a,b]),30:(0x038005bc,[a,b]),31:(0x03800648,[a,b]),32:(0x037ffd14,[a,b])}
            if identifier in direct:target,values=direct[identifier];call(target,values,0x76543210)
            elif identifier in [19,20,21]:
                for ch in range(16):
                    if a&(1<<ch):call({19:0x037feac0,20:0x037fea48,21:0x037fead8}[identifier],[ch,b,c]if identifier==20 else[ch,b])
            elif identifier in [12,13]:
                enabled=0x81234567;call(0x037fdd00,[],enabled)
                if identifier==12:
                    for ch in range(16):
                        if a&(1<<ch):at=0x04000403+16*ch;value=p.regions[at][0];reads.append((at,1,value));mmio(at,1,value|128)
                    capture_start(b)
                    for alarm in range(8):
                        if c&(1<<alarm):call(0x03801dac,[alarm])
                else:
                    for alarm in range(8):
                        if c&(1<<alarm):call(0x03801e68,[alarm])
                    for ch in range(16):
                        if a&(1<<ch):call(0x037fea20,[ch,d])
                    for cap in range(2):
                        if b&(1<<cap):mmio(0x04000508+cap,1,0)
                call(0x037fdd14,[enabled]);call(0x03801c8c)
            elif identifier==29:p.regions[SLOT]=p32(a);currentShared=a
            elif identifier==33:
                raw=p.read(WORK_DATA,4480);call(0x037fdfec,[WORK_DATA,INFO,4480],mutations=[(INFO,raw)]);p.write(INFO,raw);p.u32(INFO+4544,WORK_DATA)
                for ch in range(16):value=0x81000000+ch*0x10203;call(0x037febd0,[ch],value);p.u32(INFO+4480+ch*4,value)
                call(0x037ffcf8,[0],0xf00f00ff);p.u32(INFO+4548,0xf00f00ff)
        p.u32(currentShared,(p.r32(currentShared)+1)&0xffffffff)
    call(0x037fc760,[QUEUE,SP-64,0],0);result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=reads,faultRegisters=[],instructionBudget=150000);return result
