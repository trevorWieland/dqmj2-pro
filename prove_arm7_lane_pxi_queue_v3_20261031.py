import hashlib
import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,write_json

BASE,STACK,RETURN,IO,RECV=0x037F8000,0x023E0000,0x023FF000,0x04000000,0x04100000
DATA,PROBE,LOG=0x023C0000,0x023C7000,0x023C7800
ADDRESS,SIZE,CODE=0x037FE4A8,224,216
CONTROL,SEND,CALLBACKS=IO+0x184,IO+0x188,0x038078D0
HELPERS={0x037FE448:92,0x037FDD00:20,0x037FDD14:24}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def execute(body,words,send_full,seed,budget=20000,callback_mask=0,initial_error=False,probe=None):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE or len(words)>16 or any(not 0<=word<=0xFFFFFFFF for word in words):
        raise ValueError('Measured RX unit or bounded synthetic FIFO word inputs differ')
    if probe is None or probe[1]['physicalArgumentWords']!=3 or probe[1]['codeBytes']!=56 or probe[1]['bytes']!=60 or probe[1]['sourceCredit']!=0 or probe[1]['originalCalleeCredit']!=0 or digest(probe[0])!=probe[1]['linkedBodySha256']:
        raise ValueError('Explicit three-u32 compiled callback contract differs')
    wram=bytearray(raw+random.Random(seed+43).randbytes(0x18000-len(raw)))
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    wram[CALLBACKS-BASE:CALLBACKS-BASE+32*4]=b''.join((PROBE if callback_mask&(1<<i) else 0).to_bytes(4,'little') for i in range(32))
    regions={BASE:bytes(wram),STACK:random.Random(seed+67).randbytes(0x4000),RETURN:bytes(0x1000),
        DATA:random.Random(seed+101).randbytes(0x8000),IO:random.Random(seed+173).randbytes(0x1000),RECV:random.Random(seed+229).randbytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    cpu.mem_write(PROBE,probe[0])
    cpu.mem_write(LOG,bytes(49*4))
    full=2 if send_full else 0
    final_base=full|(0x8000 if initial_error else 0)
    cpu.mem_write(CONTROL,(full|(0x4000 if initial_error else 0)|(0 if words else 256)).to_bytes(2,'little'))
    expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in regions.items() if base!=STACK}
    stores=[]
    expected_updates=[]
    initial_status=int.from_bytes(cpu.mem_read(CONTROL,2),'little')
    if initial_error:
        stores.append([CONTROL,2,initial_status|0xC000])
        expected_updates.append([CONTROL,2,(initial_status|0x8000)&~0x4000,'explicit-W1C-error-contract'])
    callbacks=[]
    echoes=[]
    for index,word in enumerate(words):
        expected_updates.extend([[RECV,4,word,'queue-word-read'],[CONTROL,2,final_base|(256 if index+1==len(words) else 0),'receive-empty-after-pop']])
        tag=word&31
        if tag and callback_mask&(1<<tag):
            arguments=[tag,word>>6,(word>>5)&1]
            item=len(callbacks)
            callbacks.append(arguments)
            for column,value in enumerate(arguments):
                target=LOG+4+item*12+column*4
                expected[DATA][target-DATA:target-DATA+4]=value.to_bytes(4,'little')
                stores.append([target,4,value])
            expected[DATA][LOG-DATA:LOG-DATA+4]=(item+1).to_bytes(4,'little')
            stores.append([LOG,4,item+1])
        elif tag and not word&32:
            echoes.append(word|32)
            if not send_full:
                stores.append([SEND,4,word|32])
    if words:
        expected[RECV][:4]=words[-1].to_bytes(4,'little')
    expected[IO][0x184:0x186]=(final_base|256).to_bytes(2,'little')
    if echoes and not send_full:
        expected[IO][0x188:0x18C]=echoes[-1].to_bytes(4,'little')
    queue=list(words)
    writes,reads,visited,frames,updates=[],[],set(),[],[]
    counts={key:0 for key in (*HELPERS,PROBE)}
    callback_arguments=[]
    pending=[]
    send_arguments=[]
    steps=[0]
    def code(uc,pc,size,unused):
        steps[0]+=1
        for update in pending:
            uc.mem_write(update[0],update[2].to_bytes(update[1],'little'))
            updates.append(update)
        pending.clear()
        if uc.reg_read(UC_ARM_REG_CPSR)&32 or size!=4 or pc%4 or not (ADDRESS<=pc<ADDRESS+CODE or PROBE<=pc<PROBE+56 or any(first<=pc<first+length for first,length in HELPERS.items())):
            raise ValueError('RX queue execution escaped owned ARM/real sender/IRQ scopes')
        if frames and frames[-1][1]==pc:
            counts[frames.pop()[0]]+=1
        if ADDRESS<=pc<ADDRESS+CODE:
            visited.add(pc)
        if pc in HELPERS or pc==PROBE:
            frames.append((pc,uc.reg_read(match_runtime.REGISTERS[14])))
            if pc==PROBE:
                callback_arguments.append([uc.reg_read(register) for register in match_runtime.REGISTERS[:3]])
            if pc==0x037FE448:
                send_arguments.append(uc.reg_read(match_runtime.REGISTERS[0]))
    def read(uc,access,target,size,value,unused):
        reads.append([target,size])
        if target==RECV:
            if size!=4 or uc.reg_read(UC_ARM_REG_PC)!=0x037FE504 or not queue:
                raise ValueError('FIFO provider accessed outside its exact declared word-read boundary')
            word=queue.pop(0)
            status=final_base|(0 if queue else 256)
            uc.mem_write(RECV,word.to_bytes(4,'little'))
            uc.mem_write(CONTROL,status.to_bytes(2,'little'))
            updates.extend([[RECV,4,word,'queue-word-read'],[CONTROL,2,status,'receive-empty-after-pop']])
    def write(uc,access,target,size,value,unused):
        value&=(1<<(size*8))-1
        writes.append([target,size,value])
        if target==CONTROL:
            if not initial_error or size!=2 or not value&0x4000 or uc.reg_read(UC_ARM_REG_PC)!=0x037FE4E0:
                raise ValueError('FIFO error provider accessed outside its exact acknowledgment boundary')
            pending.append([CONTROL,2,value&~0x4000,'explicit-W1C-error-contract'])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
    initial[13:]=[STACK+0x3000,RETURN]
    flags=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
    cpu.reg_write(UC_ARM_REG_CPSR,flags)
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    guard=bytes(cpu.mem_read(STACK+0x3000,0x1000))
    fault=None
    try:
        cpu.emu_start(ADDRESS,RETURN,timeout=500000,count=budget)
    except (UcError,ValueError) as error:
        fault=str(error)
    actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
    record=dict(words=words,sendFull=send_full,callbackMask=callback_mask,initialError=initial_error,seed=seed,actualReturn=actual,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
        fault=fault,instructions=steps[0],visited=sorted(visited))
    if not actual:
        return dict(record,returnCredit=0,postBoundaryStateExcluded=True)
    registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=flags&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard or frames or queue:
        raise ValueError('RX queue actual return/callee-preserved register/SP/LR/control/queue model differs')
    nonstack=[row for row in writes if not STACK<=row[0]<STACK+0x4000]
    if callback_arguments!=callbacks or send_arguments!=echoes or nonstack!=stores or updates!=expected_updates or any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
        raise ValueError('Independent RX no-callback dispatch/echo/MMIO contract or complete memory/store model differs')
    pairs=len(words)+1+len(echoes)
    if counts!={0x037FE448:len(echoes),0x037FDD00:pairs,0x037FDD14:pairs,PROBE:len(callbacks)}:
        raise ValueError('Actual RX original sender and IRQ-helper return counts differ')
    return dict(record,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,
        providerUpdates=updates,actualOriginalHelperReturns={hex(key):count for key,count in counts.items() if key!=PROBE},
        actualSyntheticCallbackReturns=counts[PROBE],
        senderWordArguments=send_arguments,callbackArguments=callback_arguments,independentCompleteMemoryAndExactNonstackStores=True,
        memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in regions.items()},
        providerContract='Explicit bounded FIFO pop/receive-empty MMIO contract; no physical hardware or W1C error semantics',
        physicalIpcHardwareCredit=0,originalCallbackSourceCredit=0,originalErrorHardwareCredit=0)


def main():
    from build_arm7_lane_pxi_recv_callback_v3_20261031 import build
    probe=build()
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    body=raw[ADDRESS-BASE:ADDRESS-BASE+SIZE]
    records=[]
    for words in ([],[0],[1],[0x21],[0xFFFFFFFF],[0xFFFFFFDF],[0,1,0x21,0xFFFFFFDF],[1,1,1,1]):
        for full in (False,True):
            for mask in (0,0xFFFFFFFF,2,0x80000000):
                for error in (False,True):
                    record=execute(body,words,full,3,callback_mask=mask,initial_error=error,probe=probe)
                    if not record['actualReturn']:
                        raise ValueError(record)
                    records.append(record)
    write_json(ROOT/'evidence/attempts/arm7-lane-pxi-queue-v3-20261031.json',dict(sourceCredit=0,records=records,
        actualOriginalReturns=len(records),syntheticCallback=probe[1],physicalIpcHardwareCredit=0,
        limitations=['Bounded FIFO pop/empty and W1C error-ack contracts are explicit synthetic boundaries',
            'Compiled three-u32 callback contracts log arguments only and have no original-callee/source credit',
            'No physical hardware/game callback or module/source credit from this original-only probe']))
    print(dict(actualOriginalReturns=len(records),sourceCredit=0))


if __name__=='__main__':
    main()
