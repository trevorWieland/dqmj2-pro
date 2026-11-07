import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261106_ov001_record_helpers_source_first_models import SP,STOP,scenario


def run(row,body,f,images,ordinal):
    plan=scenario(f,ordinal);entry=int(row['address'],0);vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    for start,size in [(0x02000000,0x800000),(0x037f8000,0x20000),(0x04000000,0x10000),(0x04800000,0x10000)]:vm.mem_map(start,size)
    for start,image in images:vm.mem_write(start,image)
    vm.mem_write(entry,body);vm.mem_write(SP-2048,bytes((i*31+ordinal*7)&255 for i in range(4096)))
    for address,raw in plan['initial'].items():vm.mem_write(address,raw)
    initial=[0x11220000+i*256+ordinal for i in range(15)];initial[:4]=(plan['args']+[0,0,0,0])[:4];initial[13:15]=[SP,STOP]
    for i,value in enumerate(plan['args'][4:]):vm.mem_write(SP+i*4,int(value).to_bytes(4,'little'))
    vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal%16)<<28)|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):name for name,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};pcs=[];calls=[];writes=[];failures=[];returned=False;rejected=False;sramReads=[];sramWrites=[];pendingFaults=[];mmioReads=[];tableReads=[];spiCursor=0;flagReads=[]
    def memory(uc,access,address,size,value,user):
        writes.append(dict(provider=False,address=address,size=size,value=value))
        if 0x04804000<=address<0x04806000:
            sramWrites.append((address,size,value))
            if plan['sramFault']=='all'or plan['sramFault']=='first'and address==0x04804000:pendingFaults.append((address,value&~1))
        if address in plan['faultRegisters']:pendingFaults.append((address,value^1))
        if not(SP-plan['frame']<=address and address+size<=SP) and not any(a<=address and address+size<=b for a,b in plan['allowedWriteRanges']):failures.append('Caller write escapes measured frame or bounded borrowed data')
    def code(uc,address,size,user):
        nonlocal returned,rejected
        for at,value in pendingFaults:uc.mem_write(at,int(value).to_bytes(2,'little'))
        pendingFaults.clear()
        pcs.append(address)
        if address==STOP:returned=True;uc.emu_stop();return
        if address in imports:
            n=len(calls);action=plan['actions'][n] if n<len(plan['actions']) else dict(address=0,args=[],returned=0,checks=[],mutations=[]);sp=uc.reg_read(R.UC_ARM_REG_SP);args=[uc.reg_read(r) for r in C.REGISTERS[:min(4,len(action['args']))]]+[int.from_bytes(uc.mem_read(sp+4*i,4),'little') for i in range(max(0,len(action['args'])-4))];mode='thumb' if uc.reg_read(R.UC_ARM_REG_CPSR)&32 else 'arm';calls.append(dict(symbol=imports[address],address=address,args=args,mode=mode,stack=sp))
            argumentMatch=all((SP-plan['frame']<=a and a+512<=SP) if e=='frame-buffer' else a==e for a,e in zip(args,action['args']))
            if address!=action['address'] or not argumentMatch or mode!='arm' or sp!=SP-plan['frame']:failures.append('Independent exact import words/mode/identity/frame differs');rejected=True;uc.emu_stop();return
            for at,raw in action['checks']:
                if bytes(uc.mem_read(at,len(raw)))!=raw:failures.append('Independent protocol-boundary borrowed bytes differ')
            for at,raw in action['mutations']:uc.mem_write(at,raw);writes.append(dict(provider=True,address=at,hex=raw.hex()))
            lr=uc.reg_read(R.UC_ARM_REG_LR)
            for i,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+n*16+i)
            uc.reg_write(R.UC_ARM_REG_R0,action['returned']);uc.reg_write(R.UC_ARM_REG_R1,action['returnedHigh'])if 'returnedHigh'in action else None;uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+n)%16<<28)|0x10);uc.reg_write(R.UC_ARM_REG_PC,lr)
        elif not entry<=address<entry+len(body):raise ValueError(('No imported/tail/platform body execution authorized',hex(address)))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    def read_memory(uc,access,address,width,value,user):
        nonlocal spiCursor
        if address in [0x040001c0,0x040001c2]and plan['spiReadScript']:
            if spiCursor>=len(plan['spiReadScript']):failures.append('SPI read exceeds bounded actual device contract');return
            at,size,result=plan['spiReadScript'][spiCursor];spiCursor+=1
            if(address,width)!=(at,size):failures.append('Actual SPI register/read width/order differs')
            uc.mem_write(address,int(result).to_bytes(width,'little'))
        if 0x04000000<=address<0x05000000:mmioReads.append((address,width,int.from_bytes(uc.mem_read(address,width),'little')))
        instruction=int.from_bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_PC),4),'little')
        if instruction&0x0e000000!=0x08000000 and any(a<=address<a+n for a,n in plan['typedReadRegions']):
            flagReads.append((address,width,int.from_bytes(uc.mem_read(address,width),'little')))
        if any(a<=address<a+n for a,n in tableRanges):
            if not any(a<=address and address+width<=a+n for a,n in tableRanges)or width!=2 or address%2:failures.append('Imported constant table read violates typed bounded halfwords')
            tableReads.append((address,width,int.from_bytes(uc.mem_read(address,width),'little')))
    tableRanges=[]
    vm.hook_add(unicorn.UC_HOOK_MEM_READ,read_memory)
    vm.emu_start(entry,STOP+4,count=plan['instructionBudget'])
    if not returned:
        if not rejected:raise ValueError('Bounded peripheral caller did not return')
        return dict(actualTopReturn=False,modelFailures=failures,calls=calls,rejectedAtObservedBoundary=True)
    registers=[vm.reg_read(r) for r in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:failures.append('Callee-saved GPR/SP contract differs')
    if plan['returnValue'] is not None and registers[0]!=plan['returnValue']:failures.append('Independent return-value model differs')
    if len(calls)!=len(plan['actions']):failures.append('Independent bounded import count differs')
    if sramReads!=plan['sramReads']or sramWrites!=plan['sramWrites']:failures.append('Independent exact bounded SRAM read/write sequence/width/value differs')
    observedMmio=[(w['address'],w['size'],w['value'])for w in writes if not w['provider']and 0x04000000<=w['address']<0x05000000]
    if observedMmio!=plan['expectedMmioWrites']:failures.append('Independent exact MMIO write order/width/value differs')
    if spiCursor!=len(plan['spiReadScript']):failures.append('Bounded SPI device read script not fully consumed')
    if tableReads!=plan['expectedTableReads']:failures.append('Exact original table read index/width/value differs')
    if flagReads!=plan['expectedFlagReads']:failures.append('Exact typed byte/halfword/argument-word read boundary differs')
    if mmioReads!=plan['expectedMmioReads']:failures.append('Independent ordered MMIO read addresses/widths/values differ')
    for at,raw in plan['regions'].items():
        if bytes(vm.mem_read(at,len(raw)))!=raw:failures.append('Independent complete borrowed-region byte model differs at '+hex(at))
    return dict(actualTopReturn=True,modelFailures=failures,typedFlagReads=flagReads,typedTableReads=tableReads,mmioReads=mmioReads,calls=calls,writes=writes,pcs=pcs,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),ramSha256=C.sha(bytes(vm.mem_read(0x02000000,0x800000))),wramSha256=C.sha(bytes(vm.mem_read(0x037f8000,0x20000))))
