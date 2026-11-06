import json
from collections import Counter
import match_runtime
from arm7_lane_thread_exit_engine_20261031 import setup,BASE,DATA,RETURN
from unicorn import UC_HOOK_CODE,UcError
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,write_json

SIZES={0x037FC180:96,0x037FC1E0:64}
CODES={0x037FC180:88,0x037FC1E0:60}
PARENT,CHILD=0x038077C8,DATA+0x1000


def execute(address,body,seed,destructor_stack=False,budget=20000,callback_probe=None):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if address not in SIZES or len(body)!=SIZES[address]:
        raise ValueError('Exit source body extent differs')
    machine=setup(0x037FBF64,raw[0x3F64:0x4054],seed,callback_probe)
    cpu=machine['cpu']
    cpu.mem_write(address,body)
    cpu.mem_write(0x03807678,bytes(0x0380B4E4-0x03807678))
    prerequisites=[]
    for entry,args in ((0x037FBF64,[]),(0x037FC558,[]),(0x037FC054,[CHILD,0x037FC15C,0,DATA+0x6000,1024,0]),
                       (0x037FC36C,[CHILD]),(0x037FC590,[])):
        call=machine['invoke'](entry,args)
        if not call['actualReturn']:
            raise ValueError('Original init/create/wakeup prerequisite did not return')
        prerequisites.append(dict(entry=hex(entry),arguments=args,actualReturn=True))
    top=DATA+0x6800 if destructor_stack else 0
    cpu.mem_write(0x0380770C,top.to_bytes(4,'little'))
    if callback_probe is not None:
        cpu.mem_write(CHILD+0x98,(0x023C7000).to_bytes(4,'little'))
        cpu.mem_write(0x023C7800,bytes(8))
    predicted={base:bytearray(cpu.mem_read(base,len(data))) for base,data in machine['regions'].items()}
    def put(target,value,width=4):
        for base,data in predicted.items():
            if base<=target and target+width<=base+len(data):
                data[target-base:target-base+width]=(value&((1<<(width*8))-1)).to_bytes(width,'little')
                return
        raise ValueError('Independent exit model write escaped bounded backing')
    def peek(target,width=4):
        for base,data in predicted.items():
            if base<=target and target+width<=base+len(data):
                return bytes(data[target-base:target-base+width])
        raise ValueError('Independent exit model read escaped bounded backing')
    put(0x0380771C,PARENT)
    put(CHILD+0x48,2)
    if callback_probe is not None:
        put(CHILD+0x98,0)
        put(0x023C7800,1)
    if top:
        for offset in range(72):
            put(CHILD+offset,0,1)
        for offset,value in ((0,0x9F),(0x38,(top-0x40)&~7),(0x40,0x037FC1E4),(0x44,top)):
            put(CHILD+offset,value)
    state=dict(active=PARENT,serviceSp=0,pendingSave=None,pendingLoad=None,resumePc=None,
        saveReturns=0,resumed=0,loads=0,steps=0,callbackEntries=0,callbackReturns=0,pendingCallback=None)
    entries,visited,events=Counter(),set(),[]
    own_return_pcs={0x037FC1D0,0x037FC1D4,0x037FC214,0x037FC218}
    expected_loads=[CHILD]+([CHILD] if top else [])+[PARENT]
    def code(uc,pc,size,unused):
        state['steps']+=1
        if address<=pc<address+CODES[address]:
            visited.add(pc)
        if pc in (0x037FC180,0x037FC1E0):
            entries[pc]+=1
        if pc==0x037FC1E0 and int.from_bytes(uc.mem_read(CHILD+0x48,4),'little')!=1:
            raise ValueError('Exit handler was not entered with the measured READY state')
        if pc in own_return_pcs or pc==0x037FDE70:
            raise ValueError('Owned nonreturning exit reached an epilogue or termination fallback')
        if state['pendingCallback'] is not None and pc==state['pendingCallback']['lr']:
            before=state['pendingCallback']['registers']
            after=[uc.reg_read(register) for register in match_runtime.REGISTERS]
            if after[4:12]!=before[4:12] or after[13:]!=before[13:]:
                raise ValueError('Synthetic destructor callback violated preserved register/SP/LR contract')
            state.update(callbackReturns=state['callbackReturns']+1,pendingCallback=None)
        if pc==0x023C7000:
            if callback_probe is None or state['active']!=CHILD or uc.reg_read(match_runtime.REGISTERS[0])!=0 or bytes(uc.mem_read(CHILD+0x98,4))!=bytes(4):
                raise ValueError('Native destructor did not clear its one-argument callback before calling it')
            state['callbackEntries']+=1
            state['pendingCallback']=dict(lr=uc.reg_read(match_runtime.REGISTERS[14]),registers=[uc.reg_read(register) for register in match_runtime.REGISTERS])
        loading=state['pendingLoad']
        if loading and pc==loading['pc']:
            registers=[uc.reg_read(register) for register in match_runtime.REGISTERS]
            if registers!=loading['registers'] or uc.reg_read(UC_ARM_REG_CPSR)!=loading['cpsr']:
                raise ValueError('Exit context transfer differs from complete saved-register/CPSR model')
            state.update(active=loading['context'],serviceSp=loading['serviceSp'],loads=state['loads']+1,pendingLoad=None)
            if loading['context']==PARENT:
                state['resumePc']=loading['registers'][14]
        saving=state['pendingSave']
        if saving and pc==saving['lr']:
            if bytes(uc.mem_read(PARENT,72))!=peek(PARENT,72) or uc.reg_read(match_runtime.REGISTERS[0])!=0:
                raise ValueError('Original SaveContext ordinary return/context writes differ')
            state.update(saveReturns=state['saveReturns']+1,pendingSave=None)
        elif state['resumePc'] is not None and pc==state['resumePc']:
            if uc.reg_read(match_runtime.REGISTERS[0])!=1:
                raise ValueError('Resumed sleeping caller lost its saved discriminator')
            state.update(resumed=state['resumed']+1,resumePc=None)
        if pc==0x037FC64C:
            values=[uc.reg_read(register) for register in match_runtime.REGISTERS]
            flags=uc.reg_read(UC_ARM_REG_CPSR)
            if values[0]!=PARENT or state['active']!=PARENT:
                raise ValueError('Terminated secondary thread incorrectly saved a new context')
            saved=[flags,1,PARENT+4,flags,*values[3:13],values[13],values[14],0x037FC680,state['serviceSp']]
            for index,value in enumerate(saved):
                put(PARENT+4*index,value)
            state['pendingSave']=dict(lr=values[14])
        if pc==0x037FC680:
            context=uc.reg_read(match_runtime.REGISTERS[0])
            if state['loads']>=len(expected_loads) or context!=expected_loads[state['loads']]:
                raise ValueError('Exit transition selected an unexpected context')
            if context==CHILD and state['loads']==0:
                values=[int.from_bytes(cpu.mem_read(CHILD+4*index,4),'little') for index in range(18)]
                if values!=[0x1F,*([0]*13),(DATA+0x6000-4-0x40)&~7,0x037FC15C,0x037FC160,DATA+0x5FFC]:
                    raise ValueError('Original created secondary context differs from independent constructor model')
            else:
                if bytes(cpu.mem_read(context,72))!=peek(context,72):
                    raise ValueError('Original exit load record differs from independent final context model')
                values=[int.from_bytes(peek(context+4*index),'little') for index in range(18)]
            state['pendingLoad']=dict(context=context,pc=values[16]-4,registers=values[1:16],cpsr=values[0],serviceSp=values[17])
        if pc in (0x037FC15C,0x037FC180,0x037FC1E0,0x037FC220,0x037FC64C,0x037FC680):
            events.append(dict(pc=hex(pc),r0=hex(uc.reg_read(match_runtime.REGISTERS[0])),
                r1=hex(uc.reg_read(match_runtime.REGISTERS[1])),sp=hex(uc.reg_read(match_runtime.REGISTERS[13]))))
    cpu.hook_add(UC_HOOK_CODE,code)
    initial=[(seed*0x10305+0x12345678+index*0x1020304)&0xFFFFFFFF for index in range(15)]
    initial[0]=CHILD+0x80
    initial[13:]=[0x0380FB78,RETURN]
    cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
    cpu.reg_write(UC_ARM_REG_CPSR,0xD3)
    cpu.reg_write(match_runtime.REGISTERS[13],0)
    cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    machine['state']['caller']=True
    machine['reads'].clear()
    machine['writes'].clear()
    fault=None
    try:
        cpu.emu_start(0x037FC290,RETURN,timeout=500000,count=budget)
    except (UcError,ValueError) as error:
        fault=str(error)
    actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
    result=dict(address=hex(address),seed=seed,destructorStack=destructor_stack,syntheticCallbackContract=callback_probe is not None,actualResumedOuterSleepReturn=actual,
        actualOwnedNormalReturns=0,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,instructions=state['steps'],events=events,
        ownEntries={hex(key):value for key,value in sorted(entries.items())},visited=sorted(visited),originalPrerequisites=prerequisites)
    if not actual:
        return dict(result,postBoundaryStateExcluded=True,returnCredit=0)
    registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
        raise ValueError('Resumed actual SleepThread caller ABI differs')
    if state['loads']!=len(expected_loads) or state['saveReturns']!=1 or state['resumed']!=1 or entries!={0x037FC180:1,0x037FC1E0:1}:
        raise ValueError('Exit nonlocal transfers, entries and resumed caller counts differ')
    if any(state[key] is not None for key in ('pendingSave','pendingLoad','resumePc','pendingCallback')):
        raise ValueError('Exit context model did not complete its transfers')
    if state['callbackEntries']!=int(callback_probe is not None) or state['callbackReturns']!=state['callbackEntries']:
        raise ValueError('Destructor callback entries and genuine returns differ')
    stacks=[(0x0380F784,0x0380FB7C),(DATA+0x5C04,DATA+0x5FFC)]
    if top:
        stacks.append((DATA+0x6404,top))
    for base,expected in predicted.items():
        actual_memory=bytearray(cpu.mem_read(base,len(expected)))
        for first,last in stacks:
            first,last=max(first,base),min(last,base+len(expected))
            if first<last:
                actual_memory[first-base:last-base]=expected[first-base:last-base]
        if actual_memory!=expected:
            differences=[hex(base+i) for i,(a,b) in enumerate(zip(actual_memory,expected)) if a!=b]
            raise ValueError('Independent all-memory exit model outside declared stacks differs: '+repr(differences[:24]))
    return dict(result,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ordinarySaveReturns=1,resumedSavedContinuations=1,
        actualNonlocalContextTransfers=state['loads'],ordinaryLoadReturns=0,originalTerminationFallbackCredit=0,actualSyntheticCallbackReturns=state['callbackReturns'],
        independentCompleteContextAbiAndNonstackMemory=True,executionStackBytesIndependentlyModeled=False,
        declaredExecutionStackRanges=stacks,orderedReads=machine['reads'],orderedWrites=machine['writes'],
        memorySha256={hex(base):match_runtime.hashlib.sha256(bytes(cpu.mem_read(base,len(data)))).hexdigest() for base,data in machine['regions'].items()})


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    from build_arm7_lane_thread_exit_callback_20261031 import build
    probe=build()
    records=[]
    for address,size in SIZES.items():
        for stack in (False,True):
            for callback in (None,probe):
                record=execute(address,raw[address-BASE:address-BASE+size],3,stack,callback_probe=callback)
                if not record['actualResumedOuterSleepReturn']:
                    raise ValueError(record)
                records.append(record)
    path=ROOT/'evidence/attempts/arm7-lane-thread-exit-flow-20261031.json'
    write_json(path,dict(sourceCredit=0,records=records))
    print(dict(originalResumedSleepReturns=len(records),ownNormalReturnCredit=0))


if __name__=='__main__':
    main()
