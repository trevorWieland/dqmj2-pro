import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261105_socket_thumb_next_twelfth_models import SP,STOP,SOCKETS,RECEIVES,SPECS,scenario
from wave20261105_socket_thumb_next_twelfth_callbacks import TARGETS


def run(row,body,fixture,main,ordinal=0):
    address=int(row['address'],0);name=format(address,'08x');plan=scenario(name,fixture,ordinal)
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000)
    vm.mem_write(0x02000000,main);vm.mem_write(address,body)
    for base,raw in plan['initial'].items():vm.mem_write(base,raw)
    vm.mem_write(SP-256,bytes((i*31+ordinal*7)&255 for i in range(512)))
    initial=[0x11220000+i*256+ordinal for i in range(15)]
    initial[:4]=plan['args'][:4];initial[-2:]=[SP,STOP|1]
    for index,value in enumerate(plan['args'][4:]):vm.mem_write(SP+index*4,int(value&0xffffffff).to_bytes(4,'little'))
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x30)
    for reg,value in zip(C.REGISTERS,initial):vm.reg_write(reg,value)
    imports={int(b['address'],0)&~1:(symbol,b) for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'}
    calls,writes,pcs,failures=[],[],[],[]
    returned,rejected=False,False

    def memory(uc,access,at,size,value,user):
        writes.append(dict(provider=False,address=at,size=size,value=value))
        stack=SP-SPECS[name]<=at and at+size<=SP
        field=(at,size) in plan['allowedWrites']
        if not (stack or field):failures.append('Caller write escaped exact measured frame/field width')

    def code(uc,at,size,user):
        nonlocal returned,rejected
        pcs.append(at)
        if at==STOP:returned=True;uc.emu_stop();return
        if at in imports or at in TARGETS.values():
            if at in imports:symbol,binding=imports[at]
            else:
                kind,mode=next(key for key,v in TARGETS.items() if v==at);symbol='fixture_'+kind;binding=dict(mode=mode,program='',processor='arm9',module='main')
            index=len(calls)
            action=plan['actions'][index] if index<len(plan['actions']) else dict(address=0,args=[],returned=0,checks=[],mutations=[])
            arguments=[uc.reg_read(reg) for reg in C.REGISTERS[:min(4,len(action['args']))]]
            arguments += [int.from_bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP)+index*4,4),'little') for index in range(max(0,len(action['args'])-4))]
            actual_mode='thumb' if uc.reg_read(R.UC_ARM_REG_CPSR)&32 else 'arm'
            calls.append(dict(symbol=symbol,address=at,mode=actual_mode,arguments=arguments,program=binding.get('program') or '',processor=binding['processor'],module=binding['module']))
            if at!=action['address'] or arguments!=action['args'] or actual_mode!=binding['mode'] or uc.reg_read(R.UC_ARM_REG_SP)!=SP-SPECS[name]:
                failures.append('Independent ordered provider identity/mode and all minimum observed argument words')
                rejected=True;uc.emu_stop();return
            for base,raw in action['checks']:
                if bytes(uc.mem_read(base,len(raw)))!=raw:failures.append('Independent complete field/guard state before provider differs')
            for base,raw in action['mutations']:
                uc.mem_write(base,raw);writes.append(dict(provider=True,address=base,hex=raw.hex()))
            lr=uc.reg_read(R.UC_ARM_REG_LR)
            for index,reg in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(reg,0xcafe0000+len(calls)*16+index)
            words=action['returned'] if isinstance(action['returned'],list) else [action['returned']]
            for reg,value in zip(C.REGISTERS,words):uc.reg_write(reg,value)
            uc.reg_write(R.UC_ARM_REG_CPSR,(ordinal+len(calls))%16<<28|0x10|(32 if lr&1 else 0))
            uc.reg_write(R.UC_ARM_REG_PC,lr)
        elif not address<=at<address+len(body):raise ValueError(('No original socket/thread/provider body execution authorized',hex(at)))

    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    vm.emu_start(address|1,STOP+4,count=4000)
    if not returned:
        if not rejected:raise ValueError('Actual Thumb socket caller did not return')
        return dict(modelFailures=failures,actualTopReturn=False,rejectedAtObservedProtocolBoundary=True,calls=calls)
    registers=[vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual Thumb callee-saved registers/SP differ')
    if (plan['result'] is not None and registers[0]!=plan['result']) or len(calls)!=len(plan['actions']):failures.append('Independent full-word result or provider count differs')
    for base,raw in plan['regions'].items():
        if bytes(vm.mem_read(base,len(raw)))!=raw:failures.append('Independent full borrowed socket/thread/singleton/address state or guards differ')
    return dict(registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,pcs=pcs,ramSha256=C.sha(bytes(vm.mem_read(0x02000000,0x800000))),modelFailures=failures,actualTopReturn=True,rejectedAtObservedProtocolBoundary=False)
