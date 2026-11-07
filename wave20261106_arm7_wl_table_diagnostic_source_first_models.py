from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
from project import ROOT,read_json


def crc_step(byte,total):
    total^=byte
    for _ in range(8):total=(total>>1)^(0xa001 if total&1 else 0)
    return total&65535


def tables():
    certificate=read_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-table-diagnostic-next/first/table-certificate.json');image=(ROOT/certificate['binary']).read_bytes();result={}
    for record in certificate['records']:
        start=int(record['address'],0)-certificate['base'];raw=image[start:start+record['bytes']];result[record['semanticName']]=[int.from_bytes(raw[i:i+2],'little')for i in range(0,len(raw),2)]
    return result


def fixtures():
    rows=[]
    for rf in [2,5]:
        rows.append(dict(entry=0x027eb55c,rf=rf,faultPhase=None))
        rows.extend(dict(entry=0x027eb55c,rf=rf,faultPhase=phase)for phase in range(5))
        rows.extend(dict(entry=0x027eb55c,rf=rf,faultPhase=None,writeFailure=index)for index in [0,104])
        rows.append(dict(entry=0x027eb55c,rf=rf,faultPhase=0,oneReadFault=True))
    rows.append(dict(entry=0x027eb55c,rf=2,faultPhase=None,ignoredWriteFailure=True))
    rows.extend(dict(entry=0x027eb22c,registerFault=fault)for fault in ['none','first','all'])
    rows.extend(dict(entry=0x027eadf4,data=data,total=total)for data in [0,1,15,16,128,255,85,170]for total in [0,1,15,16,256,32768,65535,0x1234])
    rows.extend(dict(entry=0x027eadf4,data=data,total=0)for data in range(2,15))
    rows.extend(dict(entry=0x027ea764,seed=seed)for seed in [0,1,255])
    rows.extend(dict(entry=0x027ea7cc,rf=rf,bits=bits,count=count)for rf,bits,count in [(2,24,0),(2,24,3),(2,8,2),(2,16,1),(2,32,2),(3,8,0),(3,8,1),(3,24,3),(5,0,2),(5,0x98,3),(5,32,1),(5,0x40,0)])
    return rows


def scenario(f,ordinal):
    entry=f['entry'];p=Plan(ordinal,{0x027eb55c:40,0x027eb22c:16,0x027ea7cc:40,0x027eadf4:8,0x027ea764:24}[entry]);data=tables();mmioReads=[];faults=[]
    if entry==0x027eb55c:p.u16(CTX+1528,f['rf']);p.u16(CTX+830,0x1204);p.allowed.append((CTX+830,CTX+832))
    elif entry==0x027eb22c:
        p.u16(CTX+830,0x1234);p.allowed.append((CTX+830,CTX+832));addresses=[0x04808000+n for n in data['test_reg'][::2]]
        for address in addresses:p.constant(address,p16(0xa5a5));p.allowed.append((address,address+2))
        faults=addresses if f['registerFault']=='all'else addresses[:1]if f['registerFault']=='first'else []
    elif entry==0x027eadf4:p.args=[f['data'],f['total']]
    elif entry==0x027ea764:p.buffer(SP-24,4,0xa5);p.constant(0x04808160,p16(0x1234));p.allowed.append((0x04808160,0x04808162))
    else:
        p.buffer(SP-40,8,0xa5);p.u16(CTX+1528,f['rf']);p.u16(CTX+1530,f['bits']);p.u16(CTX+1532,f['count']);p.u16(CTX+1536,0xa57e);p.u32(CTX+1540,0x12345678);p.allowed.extend([(CTX+1536,CTX+1537),(CTX+1540,CTX+1544)])
        for address in [0x04808000+n for n in data['macTxRxRegAdrs']]+[0x04808184]:p.constant(address,p16(0x1234));p.allowed.append((address,address+2))
    p.capture()
    if entry==0x027eadf4:p.returned=crc_step(f['data'],f['total'])
    elif entry==0x027eb55c:
        values=data['BBPDiagSkipAdrsES1'if f['rf']==5 else'BBPDiagSkipAdrsRelease'];skip=set();cursor=0
        for address in range(105):
            if address==values[cursor]:skip.add(address);cursor+=1
        state=[0xa5]*105;errors=0;readCount=0;finished=False
        def write(address,value,phase):
            state[address]=value&255;failure=phase==0 and f.get('writeFailure')==address or phase==1 and address==3 and f.get('ignoredWriteFailure',False);p.action(0x027ea5fc,[address,value],0xffffffff if failure else 0);return failure
        def read(address,expected,phase):
            nonlocal errors,readCount
            value=state[address]
            if f.get('faultPhase')==phase and(not f.get('oneReadFault')or readCount==0):value^=1
            p.action(0x027ea5d0,[address],value);readCount+=1
            if value!=expected:
                previous=errors;errors+=1
                return previous>32
            return False
        for phase in range(4):
            for address in range(105):
                value=255 if phase==0 else 0 if phase==1 else(0x55 if address%2==0 else 0xffaa)if phase==2 else 255-address
                if write(address,value,phase)and phase==0:errors=1;finished=True;break
            if finished:break
            for address in range(105):
                if address in skip:continue
                expected=255 if phase==0 else 0 if phase==1 else(0x55 if address%2==0 else 0xaa)if phase==2 else 255-address
                if read(address,expected,phase):finished=True;break
            if finished:break
        if not finished:
            for address in range(105):
                if address in skip:continue
                for bit in [1,2,4,8,16,32,64,128,0]:
                    write(address,bit,4)
                    if read(address,bit,4):finished=True;break
                if finished:break
        if errors:p.u16(CTX+830,0x120c)
    elif entry==0x027eb22c:
        pairs=list(zip(data['test_reg'][::2],data['test_reg'][1::2]));state={0x04808000+offset:0xa5a5 for offset,_ in pairs};errors=0;finished=False
        def write(offset,value):
            address=0x04808000+offset;value&=65535;p.mmio.append((address,2,value));state[address]=value^1 if address in faults else value;p.regions[address]=p16(state[address])
        def read(offset):
            address=0x04808000+offset;value=state[address];mmioReads.append((address,2,value));return value
        def check(offset,expected):
            nonlocal errors
            if read(offset)!=expected:
                previous=errors;errors+=1
                return previous>32
            return False
        for pattern in data['test_pattern']:
            for offset,mask in pairs:
                write(offset,pattern&mask)
                if check(offset,pattern&mask):finished=True;break
            if finished:break
        if not finished:
            for i,(offset,mask)in enumerate(pairs):write(offset,((i+1)*0x1234)&mask&65535)
            for i,(offset,mask)in enumerate(pairs):
                if check(offset,((i+1)*0x1234)&mask&65535):finished=True;break
        if not finished:
            for offset,_ in pairs:
                write(offset,0)
                if check(offset,0):break
        if errors:p.u16(CTX+830,0x1235)
    elif entry==0x027ea764:
        local=SP-24;p.u32(local,0);p.mmio=[(0x04808160,2,256)];p.regions[0x04808160]=p16(256)
        for i in range(105):
            byte=(i*7+f['seed'])&255;p.action(0x027f4e1c,[100+i,1,local],checks=[(local,p.read(local,4))],mutations=[(local,bytes([byte]))]);p.write(local,bytes([byte]));p.action(0x027ea5fc,[i,byte])
        p.action(0x027ea5fc,[90,2])
    else:
        local,reg=SP-40,SP-36;p.u32(local,0)
        for i,offset in enumerate(data['macTxRxRegAdrs']):
            value=(0xa100+i*0x123)&65535;p.action(0x027f4e1c,[68+i*2,2,local],checks=[(local,p.read(local,4))],mutations=[(local,p16(value))]);p.write(local,p16(value));address=0x04808000+offset;p.mmio.append((address,2,value));p.regions[address]=p16(value)
        control=((f['bits']>>7)<<8)|(f['bits']&127);p.u32(reg,control);p.mmio.append((0x04808184,2,control&65535));p.regions[0x04808184]=p16(control&65535)
        count=f['count']
        if f['rf']==3:
            byte=(count*3+0x55)&255;p.action(0x027f4e1c,[206+count,1,CTX+1536],mutations=[(CTX+1536,bytes([byte]))]);p.write(CTX+1536,bytes([byte]))
            for i in range(count):
                byte=(i*37+0x91)&255;p.u32(reg,0);p.action(0x027f4e1c,[206+i,1,reg],checks=[(reg,p32(0))],mutations=[(reg,bytes([byte]))]);value=byte|((i<<8)+0x50000);p.u32(reg,value);p.action(0x027ea62c,[value])
        else:
            width=((f['bits']&127)+7)//8;p.u32(reg,0)
            for i in range(count):
                word=0x247abc if i%2==0 else 0x200def;raw=p32(word)[:width];p.action(0x027f4e1c,[206+i*width,width,reg],checks=[(reg,p.read(reg,4))],mutations=[(reg,raw)]);p.write(reg,raw);value=p.r32(reg);p.action(0x027ea62c,[value])
                if f['rf']==2 and value>>18==9:p.u32(CTX+1540,value&~0x7c00)
    result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=mmioReads,faultRegisters=faults,instructionBudget=500000 if entry==0x027eb55c else 30000);return result
