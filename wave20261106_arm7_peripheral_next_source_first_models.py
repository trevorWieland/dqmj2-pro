from itertools import combinations
from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
SPI_CNT=0x040001c0
SPI_DATA=0x040001c2
PANEL=0x027fffaa


def fixtures():
    rows=[]
    for process in range(32,46):
        rows.append(dict(entry=0x027f5188,process=process,available=1,valid=1))
        if process in [35,36,37,38,39,40,43]:rows.append(dict(entry=0x027f5188,process=process,available=1,valid=0))
    rows.extend(dict(entry=0x027f5188,process=process,available=available,valid=1)for process,available in [(32,0),(35,0),(45,0),(0,1),(65535,1),(0x12340023,1),(35,0xffffffff)])
    rows.append(dict(entry=0x027f5188,process=35,available=1,valid=1,mutateProcess=True))
    rows.extend(dict(entry=0x027f6538,status1=bits,status2=status)for bits in [0,16,32,48]for status in [0,0x55,255])
    rows.extend(dict(entry=0x027f65c8,bcd=value)for value in [0,1,0x12345678,0x99999999,0x10000000,0x90000009])
    rows.extend(dict(entry=0x027f65c8,bcd=(bad<<(nibble*4))|(0x11111111&~(15<<(nibble*4))))for nibble in range(8)for bad in [10,12,14])
    rows.extend(dict(entry=0x027f667c,format=value,status=status)for value in [0,1,2,3,65534,65535]for status in [0,2,0xfd,0xff])
    rows.extend(dict(entry=0x0380433c,argument=value,queued=queued)for value in [0,1,0x81234567,0xffffffff]for queued in [0,1,0xffffffff])
    sets=[([1000]*5,0),([100,101,102,4000,4095],2),([1000,3000,1008,1016,4000],8),([1000,3000,1008,1004,4000],8),([0,4095,2048,1024,3072],7),([4095,4094,0,4093,1],2),([7,8,9,10,11],1),([0,8,16,24,32],8),([16,0,32,8,24],8),([1234]*5,-1),([0,4095,0,4095,0],0x7fffffff)]
    rows.extend(dict(entry=0x038044bc,samples=samples,range=distance,axis=axis,busy=busy,noise=0x8007 if busy else 0)for samples,distance in sets for axis in [0,1]for busy in [0,1])
    return rows


def scenario(f,ordinal):
    entry=f['entry'];frames={0x027f5188:16,0x027f6538:16,0x027f65c8:8,0x027f667c:16,0x0380433c:16,0x038044bc:48};p=Plan(ordinal,frames[entry]);mmioReads=[];script=[]
    if entry==0x027f5188:p.args=[REQ];p.u32(REQ,1);p.u32(REQ+4,f['process']);p.u32(REQ+8,0x81234567);p.u32(REQ+12,0x12345678);p.u32(REQ+16,OUT);p.u32(REQ+20,0xabcdef01)
    elif entry==0x027f6538:p.buffer(SP-16,4,0xa5)
    elif entry==0x027f65c8:p.args=[f['bcd']]
    elif entry==0x027f667c:p.args=[f['format']];p.buffer(SP-16,8,0xa5)
    elif entry==0x0380433c:p.args=[f['argument']];p.buffer(SP-16,4,0xa5);p.constant(PANEL,bytes.fromhex('7c2a5ba9'));p.allowed.append((PANEL,PANEL+4))
    else:
        p.args=[REQ,f['range']&0xffffffff,f['axis'],CFM];p.buffer(SP-48,20,0xa5);p.constant(SPI_CNT,p16(0));p.constant(SPI_DATA,p16(0x7777));p.allowed.extend([(REQ,REQ+2),(CFM,CFM+2),(SPI_CNT,SPI_CNT+2),(SPI_DATA,SPI_DATA+2)])
    p.capture()
    if entry==0x027f5188:
        enabled=0x81234567;p.action(0x037fdd00,[],enabled);p.action(0x03803b0c,[1],f['available'])
        if not f['available']:p.action(0x037fdd14,[enabled]);p.action(0x03803a48,[f['process']&65535,4])
        else:
            p.action(0x03803b28,[1]);p.action(0x037fdd14,[enabled]);process=f['process'];guard=0x027f545c if process in [35,36]else 0x027f5480 if process in [37,38,39,40,43]else 0
            if guard:p.action(guard,[],f['valid'])
            if guard and not f['valid']:p.action(0x03803a48,[process&65535,3]);p.action(0x03803b40,[1])
            elif 32<=process<=45:
                target={32:0x027f54b0,33:0x027f5514,34:0x027f5554,35:0x027f55c4,36:0x027f56ec,37:0x027f580c,38:0x027f5918,39:0x027f5a24,40:0x027f5aac,41:0x027f5b34,42:0x027f5b74,43:0x027f5bb4,44:0x027f5bf4,45:0x027f5c90}[process];args=[OUT]if process in [34,44]else[0x81234567,0x12345678,OUT]if process in [35,36,37,38]else[0x81234567]if process in [39,40]else[];changes=[]
                if process in [37,38]:args[1]&=65535
                if f.get('mutateProcess'):changes=[(REQ+4,p32(0x87654321))];p.u32(REQ+4,0x87654321)
                p.action(target,args,mutations=changes);p.action(0x03803a48,[p.r32(REQ+4)&65535,0]);p.action(0x03803b40,[1])
            else:p.action(0x03803b40,[1]);p.action(0x03803a48,[process&65535,1])
    elif entry==0x027f6538:
        local=SP-16;p.action(0x027f6b10,[local+2],mutations=[(local+2,bytes([f['status1']]))]);p.write(local+2,bytes([f['status1']]))
        bits=f['status1']&48
        if bits:
            p.action(0x027f6b74,[local],mutations=[(local,bytes([f['status2']]))]);p.write(local,bytes([f['status2']]));status=p.r16(local)
            if bits&16:status&=~15
            if bits&32:status&=~64
            p.u16(local,status);p.action(0x027f6ba0,[local],checks=[(local,p16(status))]);p.action(0x027f6074,[48,(1 if bits&16 else 0)|(2 if bits&32 else 0)])
    elif entry==0x027f65c8:
        digits=[(f['bcd']>>(4*i))&15 for i in range(8)];p.returned=0 if any(n>=10 for n in digits)else sum(n*10**i for i,n in enumerate(digits))
    elif entry==0x027f667c:
        stat,alarm=SP-16,SP-12
        if f['format']&1:
            p.action(0x037fe5a8,[0x8000]);p.action(0x027f6ec0,[0x86,0,stat,1],mutations=[(stat,bytes([f['status']]))]);p.write(stat,bytes([f['status']]))
            if not f['status']&2:
                value=p.r16(stat)|2;p.u16(stat,value);p.action(0x037fe5a8,[0x8000]);p.action(0x027f6f1c);p.action(0x027f6f90,[6,0]);p.action(0x027f7010,[stat,1],checks=[(stat,p16(value))]);p.action(0x027f6f5c)
                for register in [0x10,0x50]:
                    raw=bytes([0x83,0x51 if register==0x10 else 0x12,0xa9]);p.action(0x027f6ec0,[0x86,register,alarm,3],mutations=[(alarm,raw)]);p.write(alarm,raw);changed=bytes([raw[0],raw[1]^0x12,raw[2]^0x45]);p.action(0x027f6db0,[alarm],checks=[(alarm,p.read(alarm,4))],mutations=[(alarm,changed)]);p.write(alarm,changed);p.action(0x027f6f1c);p.action(0x027f6f90,[6,register]);p.action(0x027f7010,[alarm,3],checks=[(alarm,p.read(alarm,4))]);p.action(0x027f6f5c)
    elif entry==0x0380433c:
        p.action(0x03803b7c,[0,16,1,f['argument']],f['queued'])
        if not f['queued']:
            value=p.r32(SP-16)|0x06000000;p.u32(SP-16,value);p.regions[PANEL]=p32(value);p.action(0x03803a48,[16,f['argument']&255])
    else:
        command=0xd1 if f['axis']==0 else 0x91
        def wait(control):
            script.extend([(SPI_CNT,2,control|128)]*f['busy']);script.append((SPI_CNT,2,control))
        wait(0);p.mmio.append((SPI_CNT,2,0x8a01));p.mmio.append((SPI_DATA,2,command));wait(0x8a01)
        for i,value in enumerate(f['samples']):
            raw=(value<<3)|f['noise'];high=(raw>>8)&255;low=raw&255;p.mmio.append((SPI_DATA,2,0));wait(0x8a01);script.append((SPI_DATA,2,high));p.mmio.append((SPI_DATA,2,command));wait(0x8a01);script.append((SPI_DATA,2,low));p.u32(SP-48+4*i,value)
        p.mmio.append((SPI_CNT,2,0x8201));p.regions[SPI_CNT]=p16(0x8201);p.regions[SPI_DATA]=p16(low);p.action(0x03804498);samples=f['samples'];density=max(samples)-min(samples);p.u16(CFM,density);p.returned=1 if f['axis']==0 else 2;output=(samples[0]+samples[4])//2&~7
        for i,j,k in combinations(range(5),3):
            if abs(samples[i]-samples[j])<=f['range']and abs(samples[i]-samples[k])<=f['range']:output=(2*samples[i]+samples[j]+samples[k])//4&~7;p.returned=0;break
        p.u16(REQ,output);mmioReads=list(script)
    result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=mmioReads,faultRegisters=[],spiReadScript=script,instructionBudget=50000);return result
