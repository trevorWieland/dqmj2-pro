import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261106_socl_continuation_next_eleventh_naming_v2_models import SP,STOP,CTX,OUT,SPECS,scenario


def run(row,body,fixture,main,ordinal=0):
    address=int(row['address'],0);name=format(address,'08x');plan=scenario(name,fixture,ordinal);vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);vm.mem_write(address,body)
    for base,raw in plan['initial'].items():vm.mem_write(base,raw)
    vm.mem_write(SP-256,bytes((i*31+ordinal*7)&255 for i in range(512)));initial=[0x11220000+i*256+ordinal for i in range(15)];initial[:4]=plan['args'];initial[-2:]=[SP,STOP|1];vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x30)
    for reg,value in zip(C.REGISTERS,initial):vm.reg_write(reg,value)
    imports={int(b['address'],0)&~1:(symbol,b) for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];pcs=[];failures=[];reads=[];returned=False;rejected=False
    def reading(uc,access,at,size,value,user):
        if not (address<=at and at+size<=address+len(body) or SP-SPECS[name]<=at and at+size<=SP or any(base<=at and at+size<=base+extent for base,extent in plan['readable'])):failures.append('Caller read escaped measured frame/body and explicit borrowed fixture memory')
    def memory(uc,access,at,size,value,user):
        writes.append(dict(provider=False,address=at,size=size,value=value));stack=SP-SPECS[name]<=at and at+size<=SP;field=any(base<=at and at+size<=base+extent for base,extent in plan['writable'])
        if not (stack or field):failures.append('Caller write escaped exact measured frame/counter/output width')
    def code(uc,at,size,user):
        nonlocal returned,rejected
        pcs.append(at)
        if at==STOP:returned=True;uc.emu_stop();return
        if at in imports:
            symbol,binding=imports[at];index=len(calls);action=plan['actions'][index] if index<len(plan['actions']) else dict(address=0,args=[],returned=0,checks=[],mutations=[],stackWords=[]);arguments=[uc.reg_read(reg) for reg in C.REGISTERS[:len(action['args'])]];mode='thumb' if uc.reg_read(R.UC_ARM_REG_CPSR)&32 else 'arm';stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),len(action['stackWords'])*4));actualStack=[int.from_bytes(stack[i:i+4],'little') for i in range(0,len(stack),4)]
            calls.append(dict(symbol=symbol,address=at,mode=mode,arguments=arguments,stackWords=actualStack,program=binding.get('program') or '',processor=binding['processor'],module=binding['module']))
            if at!=action['address'] or arguments!=action['args'] or mode!=binding['mode'] or actualStack!=action['stackWords']:
                failures.append('Independent ordered provider identity/mode and complete observed register/stack arguments');rejected=True;uc.emu_stop();return
            for base,raw in action['checks']:
                if bytes(uc.mem_read(base,len(raw)))!=raw:failures.append('Independent complete state before provider differs')
            for base,raw in action['mutations']:
                if raw:uc.mem_write(base,raw)
                writes.append(dict(provider=True,address=base,hex=raw.hex()))
            lr=uc.reg_read(R.UC_ARM_REG_LR)
            for i,reg in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(reg,0xcafe0000+len(calls)*16+i)
            uc.reg_write(R.UC_ARM_REG_R0,action['returned']);uc.reg_write(R.UC_ARM_REG_CPSR,(ordinal+len(calls))%16<<28|0x10|(32 if lr&1 else 0));uc.reg_write(R.UC_ARM_REG_PC,lr)
        elif not address<=at<address+len(body):raise ValueError(('No actual provider or unrelated original code execution authorized',hex(at)))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.hook_add(unicorn.UC_HOOK_MEM_READ,reading);vm.emu_start(address|1,STOP+4,count=10000)
    if not returned:
        if not rejected:raise ValueError('Actual continuation caller did not return')
        return dict(modelFailures=failures,actualTopReturn=False,rejectedAtObservedProtocolBoundary=True,calls=calls)
    registers=[vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual Thumb callee-saved/SP differs')
    if (plan['result'] is not None and registers[0]!=plan['result']) or len(calls)!=len(plan['actions']):failures.append('Independent whole-word result/provider count differs')
    if plan['volatileStateReads'] is not None and (len(reads)!=plan['volatileStateReads'] or any(r['size']!=2 for r in reads)):failures.append('Required volatile signed16 state read count/width differs')
    for base,raw in plan['regions'].items():
        if bytes(vm.mem_read(base,len(raw)))!=raw:failures.append('Independent whole borrowed context/output/data/guard state differs')
    for base,raw in plan['extraChecks']:
        if bytes(vm.mem_read(base,len(raw)))!=raw:failures.append('Ordered generated hash/seed stack bytes differ')
    return dict(registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,volatileStateReads=reads,pcs=pcs,ramSha256=C.sha(bytes(vm.mem_read(0x02000000,0x800000))),modelFailures=failures,actualTopReturn=True,rejectedAtObservedProtocolBoundary=False)
