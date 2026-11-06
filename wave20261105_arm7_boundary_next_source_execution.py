import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261105_arm7_boundary_next_source_models import SP,STOP,FRAME,scenario


def run(row,body,f,images,ordinal=0):
    plan=scenario(f,ordinal);address=int(row['address'],0);vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x800000);vm.mem_map(0x037f8000,0x20000)
    for base,image in images:vm.mem_write(base,image)
    vm.mem_write(address,body)
    for at,raw in plan['initial'].items():vm.mem_write(at,raw)
    vm.mem_write(SP-256,bytes((i*31+ordinal*7)&255 for i in range(512)));initial=[0x11220000+i*256+ordinal for i in range(15)];initial[:4]=plan['args'];initial[13:15]=[SP,STOP];vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal%16)<<28)|0x10)
    for reg,value in zip(C.REGISTERS,initial):vm.reg_write(reg,value)
    imports={int(b['address'],0):name for name,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];pcs=[];failures=[];returned=False;rejected=False
    def memory(uc,access,at,size,value,user):
        writes.append(dict(provider=False,address=at,size=size,value=value))
        if not(SP-FRAME<=at and at+size<=SP) and (at,size) not in plan['allowedWrites']:failures.append('Caller write escaped original72B frame/observed callback halfword fields')
    def code(uc,at,size,user):
        nonlocal returned,rejected
        pcs.append(at)
        if at==STOP:returned=True;uc.emu_stop();return
        if at in imports:
            index=len(calls);action=plan['actions'][index] if index<len(plan['actions']) else dict(address=0,args=[],returned=0,checks=[],mutations=[]);args=[uc.reg_read(r) for r in C.REGISTERS[:len(action['args'])]];mode='thumb' if uc.reg_read(R.UC_ARM_REG_CPSR)&32 else 'arm';calls.append(dict(symbol=imports[at],address=at,arguments=args,mode=mode,program='',processor='arm7'))
            if at!=action['address'] or args!=action['args'] or mode!='arm' or uc.reg_read(R.UC_ARM_REG_SP)!=SP-FRAME:failures.append('Independent exact ARM7 import identity/minimum words/frame/mode differs');rejected=True;uc.emu_stop();return
            for base,raw in action['checks']:
                if bytes(uc.mem_read(base,len(raw)))!=raw:failures.append('Independent guarded WMSP/status/packet/callback state before import differs')
            for base,raw in action['mutations']:uc.mem_write(base,raw);writes.append(dict(provider=True,address=base,hex=raw.hex()))
            lr=uc.reg_read(R.UC_ARM_REG_LR)
            for n,reg in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(reg,0xcafe0000+len(calls)*16+n)
            uc.reg_write(R.UC_ARM_REG_R0,action['returned']);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16<<28)|0x10);uc.reg_write(R.UC_ARM_REG_PC,lr)
        elif not address<=at<address+len(body):raise ValueError(('No original imported ARM7/body execution authorized',hex(at)))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=12000)
    if not returned:
        if not rejected:raise ValueError('Controlled finite ARM7 indication caller did not return')
        return dict(actualTopReturn=False,modelFailures=failures,rejectedAtObservedProtocolBoundary=True,calls=calls)
    registers=[vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Original ARM7 callee-saved registers/SP differ')
    if len(calls)!=len(plan['actions']):failures.append('Independent finite message/import count differs')
    for at,raw in plan['regions'].items():
        if bytes(vm.mem_read(at,len(raw)))!=raw:failures.append('Independent complete borrowed WMSP/status/packet/callback bytes differ')
    return dict(actualTopReturn=True,modelFailures=failures,rejectedAtObservedProtocolBoundary=False,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,pcs=pcs,ramSha256=C.sha(bytes(vm.mem_read(0x02000000,0x800000))),wramSha256=C.sha(bytes(vm.mem_read(0x037f8000,0x20000))))
