import random
from collections import Counter
import match_runtime
from arm7_lane_channel_five_native_20261031 import digest
from arm7_lane_skip_native_20261031 import inventory,executable
from arm7_lane_sdk_division_scope_20261031 import validate_scope,additional
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,MAIN,DATA,STACK,RETURN,MMIO=0x037F8000,0x027E0000,0x023C0000,0x023E0000,0x023FF000,0x04000000
SIZES={0x03800310:48,0x03801D50:92,0x03801DAC:188}
CODES={0x03800310:44,0x03801D50:88,0x03801DAC:180}
ALARMS,PLAYERS=0x03808E60,0x03808420
ARITIES={0x038000B4:4,0x037FD5C0:1,0x037FD3A0:1,0x037FD4DC:5,0x037FD54C:7,0x037FD21C:0}


def setup(address,body,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or digest(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or len(body)!=SIZES[address]:
        raise ValueError('Measured connected SDK runtime modules/complete own function differ')
    division_scope=validate_scope(raw)
    wram=bytearray(raw+bytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(wram),MAIN:main+bytes(0x20000-len(main)),DATA:bytes(0x8000),
        STACK:random.Random(seed+107).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:bytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    entries,ranges=inventory()
    reads,writes,visited,direct,frames=[],[],set(),[],[]
    returns=Counter()
    state=dict(stage='prerequisite',instructions=0,lastPc=None,preparedFlags=None,observedTick=None)
    def arguments(count):
        values=[cpu.reg_read(r) for r in match_runtime.REGISTERS[:min(4,count)]]
        if count>4:
            stack=cpu.reg_read(match_runtime.REGISTERS[13])
            values.extend(int.from_bytes(cpu.mem_read(stack+index*4,4),'little') for index in range(count-4))
        return values
    def code(machine,pc,size,unused):
        state['instructions']+=1
        thumb=bool(machine.reg_read(UC_ARM_REG_CPSR)&32)
        if not executable(pc,size,thumb) and not additional(pc,size,thumb):
            raise ValueError('Connected SDK execution escaped current qualified module instruction map: '+hex(pc))
        while frames and frames[-1][1]==pc:
            returns[frames.pop()[0]]+=1
        if state['stage']=='caller' and address<=pc<address+SIZES[address]:
            if pc>=address+CODES[address]:
                raise ValueError('Connected SDK own literal pool was executed')
            visited.add(pc)
        if pc in ARITIES and state['stage']=='caller':
            lr=machine.reg_read(match_runtime.REGISTERS[14])
            if address<=lr<address+CODES[address]:
                direct.append(dict(address=hex(pc),arguments=arguments(ARITIES[pc])))
        if address==0x03800310 and pc==0x0380031C and state['stage']=='caller':
            player=machine.reg_read(match_runtime.REGISTERS[4])
            state['preparedFlags']=int.from_bytes(machine.mem_read(PLAYERS+player*36,1),'little')
        if address==0x03801DAC and pc==0x03801E28 and state['stage']=='caller':
            state['observedTick']=machine.reg_read(match_runtime.REGISTERS[0])|(machine.reg_read(match_runtime.REGISTERS[1])<<32)
        if pc in entries and pc!=address:
            lr=machine.reg_read(match_runtime.REGISTERS[14])
            if lr!=RETURN:
                frames.append([pc,lr])
        state['lastPc']=pc
    def write(machine,access,target,size,value,unused):
        if state['stage']=='caller':
            writes.append([target,size,value&((1 << size*8)-1),hex(machine.reg_read(UC_ARM_REG_PC))])
    def read(machine,access,target,size,value,unused):
        if state['stage']=='caller':
            reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    def invoke(entry,args=(),budget=200000,caller=False):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:min(4,len(args))]=args[:4]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        cpu.mem_write(STACK+0x3000,b''.join(value.to_bytes(4,'little') for value in args[4:]))
        caller_stack=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        state['stage']='caller' if caller else 'prerequisite'
        first=state['instructions']
        fault=None
        try:
            cpu.emu_start(entry,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned and (registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:]):
            raise ValueError('Connected SDK native caller/prerequisite violated preserved register/SP/LR contract')
        if returned and (bytes(cpu.mem_read(STACK+0x3000,0x1000))!=caller_stack or bytes(cpu.mem_read(RETURN,0x1000))!=regions[RETURN]):
            raise ValueError('Connected SDK caller-visible stack/return guards changed')
        return dict(entry=hex(entry),actualReturn=returned,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
            instructions=state['instructions']-first,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR))
    return dict(cpu=cpu,invoke=invoke,address=address,seed=seed,regions=regions,state=state,reads=reads,writes=writes,
        visited=visited,directCalls=direct,frames=frames,helperReturns=returns,divisionScope=division_scope)


def smoke(address,body):
    machine=setup(address,body,7)
    invoke,cpu=machine['invoke'],machine['cpu']
    prerequisites=[]
    if address==0x03800310:
        prerequisites.append(invoke(0x037FD3A0,[0x038079E8]))
        prerequisites.append(invoke(0x037FFEF0,[]))
        args=[0,DATA+0x1000,0,DATA+0x2000]
    else:
        prerequisites.append(invoke(0x037FD3A0,[ALARMS+20]))
        args=[0,123,0,0,0,255] if address==0x03801D50 else [0]
        if address==0x03801DAC:
            prerequisites.append(invoke(0x03801D50,[0,123,0,0,0,255]))
    if any(not row['actualReturn'] for row in prerequisites):
        raise ValueError('Connected SDK original prerequisite failed: '+str(prerequisites))
    result=invoke(address,args,caller=True)
    return dict(prerequisites=prerequisites,result=result,directCalls=machine['directCalls'],
        helperReturns={hex(a):count for a,count in machine['helperReturns'].items()},
        finalAlarm=bytes(cpu.mem_read(ALARMS,64)).hex(),finalPlayer=bytes(cpu.mem_read(PLAYERS,36)).hex())


def cases(address):
    if address==0x03800310:
        return [dict(index=index,offset=offset,mode=mode,passes=2) for index in range(16) for offset in (0,4) for mode in range(4)]
    return [dict(index=index,enable=enable,tick=tick,period=period,identifier=identifier,clock=clock,passes=2)
        for index in (0,7) for enable in ((0,1,255) if address==0x03801D50 else (0,1))
        for tick in (0,0xFFFFFFFF,0x100000000,0xFFFFFFFFFFFFFFFF)
        for period in ((0,0x100000000) if address==0x03801D50 else (0,1,0x100000000))
        for identifier in (0,0xFFFFFFFF)
        for clock in ((0,0xFFFFFFFFFFFE) if address==0x03801DAC else (0,))]


def execute(address,body,case,seed,budget=200000):
    machine=setup(address,body,seed)
    cpu,invoke=machine['cpu'],machine['invoke']
    prerequisites=[]
    index=case['index']
    if address==0x03800310:
        prerequisites.extend([invoke(0x037FD3A0,[0x038079E8]),invoke(0x037FFEF0,[])])
        sequence=bytearray([255]*0x100)
        offset=case['offset']
        if case['mode'] in (1,2):
            sequence[offset:offset+3]=bytes([254,1 if case['mode']==1 else 255,0 if case['mode']==1 else 255])
        cpu.mem_write(DATA+0x1000,bytes(sequence))
        if case['mode']==3:
            for track in range(32):
                cpu.mem_write(0x03808660+track*64,b'\x01')
        args=[index,DATA+0x1000,offset,DATA+0x2000]
        record=PLAYERS+index*36
    else:
        record=ALARMS+index*64
        prerequisites.append(invoke(0x037FD3A0,[record+20]))
        tick,period,identifier=case['tick'],case['period'],case['identifier']
        if address==0x03801DAC:
            prerequisites.append(invoke(0x03801D50,[index,tick&0xFFFFFFFF,tick>>32,period&0xFFFFFFFF,period>>32,identifier]))
            args=[index]
        else:
            cpu.mem_write(record+4,(0x1122334455667788).to_bytes(8,'little')+(0x8877665544332211).to_bytes(8,'little'))
            cpu.mem_write(record+1,b'\xa5')
            args=[index,tick&0xFFFFFFFF,tick>>32,period&0xFFFFFFFF,period>>32,identifier]
        if case['enable']:
            prerequisites.append(invoke(0x037FD4DC,[record+20,16,0,0x03801EA8,0x1234]))
            cpu.mem_write(record,bytes([case['enable']]))
        clock=case['clock']
        cpu.mem_write(0x038078A0,((clock>>16)&0xFFFFFFFF).to_bytes(4,'little')+((clock>>48)&0xFFFF).to_bytes(4,'little'))
        cpu.mem_write(0x04000100,(clock&0xFFFF).to_bytes(2,'little'))
    if any(not row['actualReturn'] for row in prerequisites):
        return dict(case=case,prerequisites=prerequisites,states=[],visited=[],unsupportedPrerequisite=True)
    states=[]
    for iteration in range(case['passes']):
        old=bytes(cpu.mem_read(record,36 if address==0x03800310 else 64))
        machine['reads'].clear()
        machine['writes'].clear()
        machine['directCalls'].clear()
        machine['frames'].clear()
        machine['helperReturns'].clear()
        machine['state'].update(preparedFlags=None,observedTick=None)
        returned=invoke(address,args,budget=budget,caller=True)
        if not returned['actualReturn']:
            states.append(dict(execution=returned,actualReturn=False,postFaultStateExcluded=True))
            break
        current=bytes(cpu.mem_read(record,len(old)))
        direct=machine['directCalls']
        own_stores=[row[:3] for row in machine['writes'] if address<=int(row[3],0)<address+CODES[address] and not STACK<=row[0]<STACK+0x4000]
        if address==0x03800310:
            prepared=machine['state']['preparedFlags']
            expected=[dict(address='0x38000b4',arguments=args)]
            if prepared is None or current[0]!=(prepared|2) or direct!=expected or own_stores!=[[record,1,prepared|2]]:
                raise ValueError('Native prepare caller/actual-return/prepared-bit model differs')
        elif address==0x03801D50:
            if current[0]!=0 or current[1]!=(case['identifier']&255) or int.from_bytes(current[4:12],'little')!=case['tick'] or int.from_bytes(current[12:20],'little')!=case['period']:
                raise ValueError('Native full64-bit setup record/enable/id model differs')
            expected=[dict(address='0x37fd5c0',arguments=[record+20])] if old[0] else []
            if direct!=expected:
                raise ValueError('Native setup cancel precondition/physical ABI differs')
        else:
            if current[0]!=1 or current[1:20]!=old[1:20]:
                raise ValueError('Native alarm-start enable/preserved64-bit/id model differs')
            expected=[dict(address='0x37fd5c0',arguments=[record+20])] if old[0] else []
            expected.append(dict(address='0x37fd3a0',arguments=[record+20]))
            token=index|(current[1]<<8)
            tick=int.from_bytes(old[4:12],'little')
            period=int.from_bytes(old[12:20],'little')
            if period:
                observed=machine['state']['observedTick']
                if observed is None or observed!=case['clock']:
                    raise ValueError('Periodic alarm-start did not actually return from original GetTick')
                first=(tick+observed)&0xFFFFFFFFFFFFFFFF
                expected.extend([dict(address='0x37fd21c',arguments=[]),dict(address='0x37fd54c',arguments=[record+20,first&0xFFFFFFFF,first>>32,
                    period&0xFFFFFFFF,period>>32,0x03801EA8,token])])
            else:
                expected.append(dict(address='0x37fd4dc',arguments=[record+20,tick&0xFFFFFFFF,tick>>32,0x03801EA8,token]))
            if direct!=expected:
                raise ValueError('Native one-shot/periodic/cancel/64-bit callback-registration ABI model differs')
        if machine['frames']:
            raise ValueError('Connected SDK helper return frames remained incomplete')
        states.append(dict(execution=returned,actualReturn=True,finalRecord=current.hex(),directCalls=list(direct),
            ownOrderedNonstackStores=own_stores,nonstackWrites=[row[:3] for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
            nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
            actualNestedReturns={hex(a):count for a,count in sorted(machine['helperReturns'].items())},
            originalPreparedFlags=machine['state']['preparedFlags'],originalReturnedTick=machine['state']['observedTick'],
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},
            independentOwnRecordAndPhysicalAbiModel=True))
    return dict(case=case,prerequisites=prerequisites,states=states,visited=sorted(machine['visited']),
        limitations=['Original sequence/alarm constructors and dependencies execute without providers; disposable work,bank,stream,clock/MMIO state is synthetic',
            'Enabled alarm prerequisites use actual original SetAlarm plus an explicit SND enable-byte store; enclosing producer reachability is unclaimed',
            'Callbacks are registered at their qualified original ARM identity but never executed; physical IRQ timing/FIFO behavior is unqualified'])
