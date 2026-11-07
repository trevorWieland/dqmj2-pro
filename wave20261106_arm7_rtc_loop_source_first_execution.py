import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261106_arm7_rtc_loop_source_first_models import SP,STOP,scenario


def run(row,body,f,images,ordinal):
    plan=scenario(f,ordinal);entry=int(row['address'],0);vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T)
    for start,size in[(0x02000000,0x800000),(0x037f8000,0x20000),(0x04000000,0x10000)]:vm.mem_map(start,size)
    for start,image in images:vm.mem_write(start,image)
    vm.mem_write(entry,body);vm.mem_write(SP-2048,bytes((i*31+ordinal*7)&255 for i in range(4096)))
    for address,raw in plan['initial'].items():vm.mem_write(address,raw)
    initial=[0x11220000+i*256+ordinal for i in range(15)];initial[:4]=(plan['args']+[0,0,0,0])[:4];initial[13:15]=[SP,STOP];vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal%16)<<28)|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):name for name,b in row['nativeSymbolEntries'].items()if b['kind']=='function'};pcs=[];calls=[];writes=[];failures=[];returned=False;completed=False;rejected=False
    def memory(uc,access,address,size,value,user):
        writes.append(dict(provider=False,address=address,size=size,value=value))
        if not(SP-plan['frame']<=address and address+size<=SP)and not any(a<=address and address+size<=b for a,b in plan['allowedWriteRanges']):failures.append('Caller write escapes measured stack or consumed busy word')
    def code(uc,address,size,user):
        nonlocal returned,completed,rejected
        pcs.append(address)
        if address==STOP:returned=True;failures.append('Original cyclic thread unexpectedly returned');uc.emu_stop();return
        if address in imports:
            n=len(calls);action=plan['actions'][n]if n<len(plan['actions'])else dict(address=0,args=[],returned=0,checks=[],mutations=[],stop=False);sp=uc.reg_read(R.UC_ARM_REG_SP);args=[uc.reg_read(r)for r in C.REGISTERS[:min(4,len(action['args']))]];mode='thumb'if uc.reg_read(R.UC_ARM_REG_CPSR)&32 else'arm';calls.append(dict(symbol=imports[address],address=address,args=args,mode=mode,stack=sp,boundedStop=action['stop']))
            if address!=action['address']or args!=action['args']or mode!='arm'or sp!=SP-plan['frame']:failures.append('Exact typed import arguments/mode/frame differ');rejected=True;uc.emu_stop();return
            for at,raw in action['checks']:
                if bytes(uc.mem_read(at,len(raw)))!=raw:failures.append('Independent complete consumed-group/shared-clock boundary model differs')
            if action['stop']:completed=True;uc.emu_stop();return
            for at,raw in action['mutations']:uc.mem_write(at,raw);writes.append(dict(provider=True,address=at,hex=raw.hex()))
            lr=uc.reg_read(R.UC_ARM_REG_LR)
            for i,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+n*16+i)
            uc.reg_write(R.UC_ARM_REG_R0,action['returned']);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+n)%16<<28)|0x10);uc.reg_write(R.UC_ARM_REG_PC,lr)
        elif not entry<=address<entry+len(body):raise ValueError(('Unowned/provider/tail instructions not authorized',hex(address)))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(entry,STOP+4,count=20000)
    if not completed and not rejected and not returned:raise ValueError('Bounded original loop failed to reach next receive boundary')
    if not completed:return dict(actualTopReturn=returned,boundedIterationComplete=False,modelFailures=failures,calls=calls,rejectedAtObservedBoundary=rejected)
    if len(calls)!=len(plan['actions']):failures.append('Independent bounded import count differs')
    for at,raw in plan['regions'].items():
        if bytes(vm.mem_read(at,len(raw)))!=raw:failures.append('Independent full consumed-region byte model differs')
    registers=[vm.reg_read(r)for r in C.REGISTERS]
    if registers[13]!=SP-plan['frame']:failures.append('Persistent original thread stack extent differs')
    return dict(actualTopReturn=False,boundedIterationComplete=True,modelFailures=failures,calls=calls,writes=writes,pcs=pcs,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),ramSha256=C.sha(bytes(vm.mem_read(0x02000000,0x800000))),wramSha256=C.sha(bytes(vm.mem_read(0x037f8000,0x20000))))
