import hashlib
import json
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=Path(__file__).resolve().parent
BASE,MAIN,DATA,STACK,RETURN,MMIO=0x037F8000,0x027E0000,0x023C0000,0x023E0000,0x023FF000,0x04000000
ADDRESS,SIZE,CODE=0x03800414,204,196
PLAYERS,TRACKS,SHARED=0x03808420,0x03808660,DATA+0x800
STREAM=DATA+0x2000


def digest(data):
    return hashlib.sha256(data).hexdigest()


@lru_cache(maxsize=1)
def inventory():
    report=json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    entries={int(row['address'],0):row for row in report['functions']}
    ranges=[]
    for row in entries.values():
        for first,last in row['ranges']:
            ranges.append((int(first,0),int(last,0),row['mode']=='thumb'))
    return entries,ranges


@lru_cache(maxsize=None)
def executable(pc,size,thumb):
    return any(first<=pc and pc+size<=last and thumb==mode for first,last,mode in inventory()[1])


def cases():
    return [dict(player=player,ticks=ticks,track=track,wait=wait,shared=shared,counter=counter,passes=2)
        for player in (0,7,15) for ticks in (0,1,2,4,0xFFFFFFFF)
        for track,wait in ((None,0),(0,0),(15,2),(0,8))
        for shared,counter in ((False,0),(True,0),(True,0xFFFFFFFE))
        if ticks!=0xFFFFFFFF or wait<8]


def execute(body,case,seed,budget=100000):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or digest(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or len(body)!=SIZE:
        raise ValueError('Measured ARM7 executable inputs/complete caller extent differ')
    wram=bytearray(0x18000)
    wram[:len(raw)]=raw
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={BASE:bytes(wram),MAIN:main+bytes(0x20000-len(main)),DATA:random.Random(seed+119).randbytes(0x4000),
        STACK:random.Random(seed+193).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:bytes(0x10000)}
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    entries,ranges=inventory()
    writes,visited,frames,contracts,direct=[],set(),[],[],[]
    arities={0x03800A7C:2,0x038009E0:3,0x03800A48:1,0x037FEFB4:0,0x03800CF0:2,0x03800B00:1,0x037FEF64:0}
    returns=Counter()
    state={'stage':'prerequisite','lastPc':None,'instructionCount':0}
    def code(machine,pc,size,unused):
        thumb=bool(machine.reg_read(UC_ARM_REG_CPSR)&32)
        if not executable(pc,size,thumb):
            raise ValueError('Skip escaped inventoried original ARM/Thumb instructions: '+hex(pc))
        while frames and pc==frames[-1][1]:
            returns[frames.pop()[0]]+=1
        if pc in entries:
            link=machine.reg_read(match_runtime.REGISTERS[-1]) & ~1
            frames.append((pc,link))
            contracts.append([pc,[machine.reg_read(r) for r in match_runtime.REGISTERS[:4]]])
            if pc in arities and ADDRESS<=link<ADDRESS+CODE:
                direct.append([pc,[machine.reg_read(r) for r in match_runtime.REGISTERS[:arities[pc]]]])
        if state['stage']=='caller':
            visited.add(pc)
        state['lastPc']=pc
        state['instructionCount']+=1
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value & ((1 << size*8)-1)])
    def interrupt(machine,number,unused):
        raise ValueError('Provider-free skip context reached an unsupported architectural service')
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_INTR,interrupt)
    def run(address,args,phase,limit):
        registers=[random.Random(seed+phase*119+i).getrandbits(32) for i in range(15)]
        registers[:len(args)]=args
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0xD3)
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        frames.clear()
        first,first_contract,first_direct=len(writes),len(contracts),len(direct)
        before=Counter(returns)
        before_count=state['instructionCount']
        fault=None
        try:
            cpu.emu_start(address,RETURN,count=limit,timeout=200000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        observed=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            while frames and frames[-1][1]==RETURN:
                returns[frames.pop()[0]]+=1
            if observed[4:12]!=registers[4:12] or observed[-2:]!=registers[-2:]:
                raise ValueError('Actual skip/prerequisite return ABI differs')
        delta=returns-before
        return dict(address=hex(address),actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=observed,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first:],actualArgumentRegisters=contracts[first_contract:],
            directCallerContracts=direct[first_direct:],
            actualFunctionReturns={hex(a):n for a,n in sorted(delta.items())},pendingFrames=[list(f) for f in frames],
            instructions=state['instructionCount']-before_count)
    prerequisites=[run(0x037FD3A0,[0x038079E8],0,10000),run(0x037FFEF0,[],1,10000)]
    if not all(row['actualReturn'] for row in prerequisites):
        raise ValueError('Real alarm/sequence initializer did not actually return')
    for player in range(16):
        cpu.mem_write(PLAYERS+player*36+8,bytes([255])*16)
    player=PLAYERS+case['player']*36
    cpu.mem_write(player,b'\x01')
    if case['track'] is not None:
        prerequisites.append(run(0x038008F0,[TRACKS],2,10000))
        if not prerequisites[-1]['actualReturn']:
            raise ValueError('Real track initializer did not actually return')
        cpu.mem_write(player+8+case['track'],b'\x00')
        cpu.mem_write(TRACKS+0x20,case['wait'].to_bytes(4,'little'))
        cpu.mem_write(TRACKS+0x24,STREAM.to_bytes(4,'little')*2)
        cpu.mem_write(TRACKS+0x3C,bytes(4))
        cpu.mem_write(STREAM,bytes([255])*64)
    cpu.mem_write(0x03807EDC,(SHARED if case['shared'] else 0).to_bytes(4,'little'))
    cpu.mem_write(SHARED+4,(0xFFFFFFFF).to_bytes(4,'little'))
    counter=SHARED+0x40+case['player']*36
    cpu.mem_write(counter,case['counter'].to_bytes(4,'little'))
    state['stage']='caller'
    records=[]
    remaining=case['wait']
    alive=case['track'] is not None
    expected_counter=case['counter']
    for phase in range(case['passes']):
        expected_calls=[]
        for slot_index in range(16):
            expected_calls.append([0x03800A7C,[player,slot_index]])
            if alive and slot_index==case['track']:
                expected_calls.extend([[0x038009E0,[TRACKS,player,127]],[0x03800A48,[TRACKS]]])
        expected_calls.append([0x037FEFB4,[]])
        increment=0
        stopped=False
        for index in range(min(case['ticks'],max(remaining+1,1))):
            expected_calls.append([0x03800CF0,[player,0]])
            if not alive:
                stopped=True
                break
            if remaining>0:
                remaining-=1
            if remaining==0:
                alive=False
                stopped=True
                break
            increment+=1
        if stopped:
            expected_calls.append([0x03800B00,[player]])
        expected_calls.append([0x037FEF64,[]])
        row=run(ADDRESS,[case['player'],case['ticks']],3+phase,budget)
        if row['actualReturn']:
            if row['directCallerContracts']!=expected_calls or row['pendingFrames']:
                raise ValueError('Independent complete caller API ordering/arguments/actual returns differ')
            if case['shared']:
                expected_counter=(expected_counter+increment)&0xFFFFFFFF
                actual=int.from_bytes(cpu.mem_read(counter,4),'little')
                if actual!=expected_counter:
                    raise ValueError('Independent complete-iteration counter/wrap differs: '+repr((case,phase,actual,expected_counter)))
            if stopped and bytes(cpu.mem_read(player,1))[0]&1:
                raise ValueError('Early-exit player stop did not clear its active bit')
            if case['track'] is not None:
                actual_wait=int.from_bytes(cpu.mem_read(TRACKS+0x20,4),'little')
                slot=bytes(cpu.mem_read(player+8+case['track'],1))[0]
                if actual_wait!=remaining or slot!=(0 if alive else 255):
                    raise ValueError('Independent wait/termination/slot effects differ: '+repr((case,phase,actual_wait,remaining,slot,alive)))
        row['expectedCompletedIterations']=increment
        row['regions']={hex(a):digest(bytes(cpu.mem_read(a,len(data)))) for a,data in regions.items()}
        records.append(row)
        if not row['actualReturn']:
            break
    return dict(prerequisites=prerequisites,states=records,visited=sorted(visited),providerCalls=0,
        limitations=['Synthetic stream and player mutations after real constructors','Zero-clock disposable MMIO; no physical scheduler, scene or asset validity claim'])
