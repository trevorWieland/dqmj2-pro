import gzip
import hashlib
import json
import random
from pathlib import Path
from functools import lru_cache
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
import audit_arm7_bulk_20261030 as inventory
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,sha256,write_json

WRAM,SHARED,STACK,RETURN=0x037f8000,0x027ff000,0x023e0000,0x023ff000
BITS,LOCK=0x027fffb8,0x027ffff0
CONFIG={
    '':dict(binary='extract/arm7/runtime/arm7-wram.bin',sha256='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c',init=0x037fb998,get=0x037fbbfc,release=0x037fbca4,flag=0x038076ec,wait=0x037fba0c,lateRead=0x037fbc8c),
    'dwc/utility.bin/move/child.srl':dict(binary='extract/utility/runtime/utility-child-arm7-wram.bin',sha256='13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6',init=0x037fc0b8,get=0x037fbe1c,release=0x037fbeb4,flag=0x038059b8,wait=0x037fc0ac,lateRead=0x037fbe9c)}


def digest(value):return hashlib.sha256(value).hexdigest()


@lru_cache(maxsize=2)
def native_specs(program):
    return {s['address']:s for s in inventory.specs() if s['program']==program and s['mode']=='arm'}


def qualify_roles(binary,program):
    config=CONFIG[program];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    def instruction(address):
        row=next(decoder.disasm(binary[address-WRAM:address-WRAM+4],address),None)
        if row is None:raise ValueError('Measured lock word instruction missing')
        return row
    if program:
        requirements={0x037fc108:('str','r1, [r0]'),0x037fc110:('rsb','r1, r0, #0'),0x037fc118:('str','r1, [r0]'),0x037fc0f4:('ldrh','r0, [r4, #4]')}
        literal_loader=0x037fc104;next_loader=0x037fc114
    else:
        requirements={0x037fb9e4:('str','r0, [r1]'),0x037fb9e8:('lsl','r0, r0, #0x10'),0x037fb9ec:('str','r0, [r1, #4]'),0x037fb9d0:('ldrh','r0, [r4, #4]')}
        literal_loader=0x037fb9dc;next_loader=None
    requirements.update({config['lateRead']:('ldr','r2, [r3]'),config['lateRead']+4:('bic','r2, r2, r1'),config['lateRead']+8:('str','r2, [r3]')})
    for address,expected in requirements.items():
        row=instruction(address)
        if (row.mnemonic,row.op_str)!=expected:raise ValueError('Measured bitmap/handshake role differs at'+hex(address))
    for address,wanted in ((literal_loader,BITS),(next_loader,BITS+4)):
        if address is None:continue
        row=instruction(address)
        if row.mnemonic!='ldr' or row.operands[1].type!=3 or row.reg_name(row.operands[1].mem.base)!='pc':raise ValueError('Bitmap initializer literal mapping changed')
        location=address+8+row.operands[1].mem.disp
        if int.from_bytes(binary[location-WRAM:location-WRAM+4],'little')!=wanted:raise ValueError('Actual initializer bitmap address changed')
    return dict(program=program,mode='arm',bitmapBase=hex(BITS),bitmapBytes=8,handshake=hex(LOCK),handshakeBytes=8,ownerReadBytes=2,ownerReadOffset=4,extensionStoreBytes=2,extensionOffset=6,initializerEntry=hex(config['init']),reservationEntry=hex(config['get']),finalLiveRead=hex(config['lateRead']),codeRoleChecks=len(requirements),sourceCredit=0)


def setup(program,seed):
    config=CONFIG[program];binary=(ROOT/config['binary']).read_bytes()
    if sha256(ROOT/config['binary'])!=config['sha256']:raise ValueError('Original bitmap module changed')
    specs=native_specs(program)
    qualify_roles(binary,program)
    chosen={name:specs[config[name]] for name in ('init','get','release')}
    late=next(i for i in chosen['get']['instructions'] if i.address==config['lateRead'])
    if late.mnemonic!='ldr' or late.op_str!='r2, [r3]' or BITS not in chosen['get']['pools'].values() or BITS not in chosen['init']['pools'].values():raise ValueError('Explicit final word read and original initializer literals differ')
    allowed={i.address for s in chosen.values() for i in s['instructions']};regions={WRAM:binary+bytes(0x18000-len(binary)),SHARED:random.Random(seed+317).randbytes(0x1000),STACK:random.Random(seed+701).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():cpu.mem_map(first,len(data));cpu.mem_write(first,data)
    writes=[];state=dict(entry=None,pc=None,instructions=0,lateValue=None,lateWrites=0)
    def code(uc,pc,size,unused):
        state['pc']=pc;state['instructions']+=1
        if uc.reg_read(UC_ARM_REG_CPSR)&32 or pc not in allowed:raise ValueError('Bitmap fixture escaped measured original ARM instructions')
        if state['entry']==config['get'] and pc==config['lateRead'] and state['lateValue'] is not None:
            target=uc.reg_read(match_runtime.REGISTERS[3])
            if target not in (BITS,BITS+4):raise ValueError('Final read address left the two measured words')
            uc.mem_write(target,state['lateValue'].to_bytes(4,'little'));state['lateWrites']+=1
    def write(uc,access,address,size,value,unused):writes.append([address,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    def invoke(kind,args=(),budget=5000,stop_at_wait=False,late_value=None):
        initial=[(seed*0x10203+i*0x1030507+0x7129)&0xffffffff for i in range(15)];initial[:len(args)]=args;initial[13:]=[STACK+0x3000,RETURN];flags=0x1f|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,flags)
        for register,value in zip(match_runtime.REGISTERS,initial):cpu.reg_write(register,value)
        guard=bytes(cpu.mem_read(STACK+0x3000,0x1000));writes.clear();state.update(entry=config[kind],instructions=0,lateValue=late_value,lateWrites=0);fault=None
        try:cpu.emu_start(config[kind],config['wait'] if stop_at_wait else RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:return dict(actualReturn=False,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,actualWaitBoundary=stop_at_wait and cpu.reg_read(UC_ARM_REG_PC)==config['wait'] and fault is None,postBoundaryStateCredit=0,instructions=state['instructions'])
        result=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if result[4:12]!=initial[4:12] or result[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=flags&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard:raise ValueError('Bitmap routine preserved ABI/stack/mode differs')
        return dict(actualReturn=True,returnBits=hex(result[0]),instructions=state['instructions'],syntheticFinalReadTransitions=state['lateWrites'],
            nonstackWrites=[w for w in writes if not STACK<=w[0]<STACK+0x4000])
    return dict(cpu=cpu,regions=regions,invoke=invoke,config=config,chosen=chosen)


def words(cpu):return [int.from_bytes(cpu.mem_read(BITS+4*i,4),'little') for i in range(2)]


def initialize(machine,flag,owner):
    cpu=machine['cpu'];cpu.mem_write(machine['config']['flag'],flag.to_bytes(4,'little'));cpu.mem_write(LOCK+4,owner.to_bytes(2,'little'))
    before={first:bytearray(cpu.mem_read(first,len(data))) for first,data in machine['regions'].items() if first!=STACK}
    wait=not flag and owner!=0x7f;result=machine['invoke']('init',stop_at_wait=wait)
    if wait:
        if result['actualReturn'] or not result['actualWaitBoundary']:raise ValueError('Unready initializer must naturally stop before its wait/Bios thunk')
        return dict(flag=flag,owner=owner,execution=result,returnCredit=0,originalWaitOrBiosExecutionCredit=0)
    if not result['actualReturn']:raise ValueError('Supported native initializer failed to return')
    expected=[]
    if not flag:
        expected=[[machine['config']['flag'],4,1],[LOCK+6,2,0],[BITS,4,0xffffffff],[BITS+4,4,0xffff0000],[LOCK+6,2,0xbf]]
        for address,size,value in expected:
            first=WRAM if address>=WRAM else SHARED;before[first][address-first:address-first+size]=value.to_bytes(size,'little')
    if result['nonstackWrites']!=expected or any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in before.items()):raise ValueError('Independent complete initializer memory/write model differs')
    return dict(flag=flag,owner=owner,execution=result,initializedBitmapWords=words(cpu),nativeInitializationCondition='flag0 and owner007F',returnCredit=1)


def reserve(machine,initial,late=None):
    cpu=machine['cpu'];cpu.mem_write(BITS,b''.join(value.to_bytes(4,'little') for value in initial));expected=initial[:]
    selected=0 if initial[0] else 1 if initial[1] else None;result=machine['invoke']('get',late_value=late)
    if not result['actualReturn']:raise ValueError('Original bounded bitmap reservation failed to return')
    if selected is None:returned=0xfffffffd;write=[]
    else:
        index=32-initial[selected].bit_length();returned=0x80+32*selected+index
        if late is not None:expected[selected]=late
        expected[selected]&=~(1<<(31-index));write=[[BITS+4*selected,4,expected[selected]]]
    if int(result['returnBits'],0)!=returned or words(cpu)!=expected or result['nonstackWrites']!=write or result['syntheticFinalReadTransitions']!=(1 if late is not None and selected is not None else 0):raise ValueError('Independent full-word selection/late-read/clear model differs')
    return dict(initialWords=initial,syntheticBeforeFinalRead=late,execution=result,finalWords=expected,returnedBits=hex(returned),ordinaryIdValidityClaim=False)


def release(machine,identifier):
    cpu=machine['cpu'];initial=[0x10203040,0x89abcdef];cpu.mem_write(BITS,b''.join(v.to_bytes(4,'little') for v in initial));result=machine['invoke']('release',[identifier])
    selected=1 if identifier>=0xa0 else 0;shift=(identifier-(0xa0 if selected else 0x80))&255;mask=0x80000000>>shift if shift<32 else 0;expected=initial[:];expected[selected]|=mask
    if not result['actualReturn'] or words(cpu)!=expected or result['nonstackWrites']!=[[BITS+4*selected,4,expected[selected]]]:raise ValueError('Independent zero-extended16 ID/ARM register-shift word model differs')
    return dict(id=identifier,execution=result,finalWords=expected,syntheticOutsideInitializedPool=not 0x80<=identifier<=0xaf,resourceValidityClaim=False)


def main():
    rom='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    if sha256(ROOT/'inputs/game.nds')!=rom:raise ValueError('Original measured ROM changed')
    records=[];totals=dict(initializerReturns=0,reservationReturns=0,releaseReturns=0,connectedReturns=0,unreadyBoundaryStops=0);controls=[]
    vectors=[[0,0],[0xffffffff,0xffffffff],[0x80000001,0xffffffff]]+[[1<<i,0xffffffff] for i in range(32)]+[[0,1<<i] for i in range(32)]+[[random.Random(i+317).getrandbits(32),random.Random(i+701).getrandbits(32)] for i in range(16)]
    for program,config in CONFIG.items():
        machine=None
        for flag in (0,1,2,0xffffffff):
            for owner in (0,1,0x7f,0xffff):
                machine=setup(program,flag+owner);row=initialize(machine,flag,owner);totals['initializerReturns']+=row['returnCredit'];totals['unreadyBoundaryStops']+=not row['returnCredit'];records.append(dict(program=program,kind='init',state=row))
        for index,pair in enumerate(vectors):
            for late in (None,0xa5a5a5a5):
                machine=setup(program,index*2+(late is not None));row=reserve(machine,pair,late);totals['reservationReturns']+=1;records.append(dict(program=program,kind='reserve',state=row))
        for identifier in [*range(0x80,0xc0),0,1,0x7f,0xc0,0xff,0x100,0x19f,0x1a0,0xffff]:
            records.append(dict(program=program,kind='release',state=release(setup(program,identifier),identifier)));totals['releaseReturns']+=1
        machine=setup(program,701);initialize(machine,0,0x7f);sequence=[]
        for index in range(49):sequence.append(reserve(machine,words(machine['cpu'])))
        if [r['returnedBits'] for r in sequence]!=[hex(v) for v in range(0x80,0xb0)]+['0xfffffffd']:raise ValueError('Actual initialized pool must reserve48 IDs then return-3')
        totals['connectedReturns']+=50;records.append(dict(program=program,kind='native-init-to-exhaustion',states=sequence,actualInitializerReturns=1,actualReservationReturns=49,normalInitialFreeIdPool='80..AF',syntheticLowSecondWordIds='B0..BF are raw only'))
        machine=setup(program,709);cap=machine['invoke']('get',budget=1)
        if cap['actualReturn']:raise ValueError('Prologue cap gained a return')
        controls.append(dict(program=program,kind='prologue-cap',execution=cap,returnCredit=0))
        binary=(ROOT/config['binary']).read_bytes();qualify_roles(binary,program)
        for label,address in [('initial-word-store',0x037fc108 if program else 0x037fb9e4),('owner-offset',0x037fc0f4 if program else 0x037fb9d0),('fresh-word-load',config['lateRead']),('final-word-store',config['lateRead']+8)]:
            changed=bytearray(binary);changed[address-WRAM]^=4
            try:qualify_roles(bytes(changed),program)
            except ValueError as error:controls.append(dict(program=program,kind=label,rejected=True,reason=str(error),returnCredit=0))
            else:raise ValueError('Mutated native word-region role accepted')
        print(dict(program=program,totals=totals,sourceCredit=0),flush=True)
    encoded=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();product=ROOT/'work/arm7-bulk-20261030/lane-lock-bitmaps692-native-v2/supported-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True);product.write_bytes(gzip.compress(encoded,compresslevel=9,mtime=0))
    output=ROOT/'evidence/arm7/lane-lock-bitmap-region-v2-20261031.json'
    write_json(output,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=rom,sourceCredit=0,assemblySourceCredit=0,functionMatchedBytes=0,moduleOwnershipClaim=False,originalDataSourceCredit=0,
        freshMachinePerIndependentScenario=True,isolatedRegisterStatePerCall=True,connectedSameMachineScenarioExplicit=True,nativeRoleQualifications=[qualify_roles((ROOT/c['binary']).read_bytes(),p) for p,c in CONFIG.items()],nativeInputNamespaces=[dict(program=p,processor='arm7',module='utility-child-arm7-wram' if p else 'arm7-wram',mode='arm',**c,functions=[dict(address=hex(c[k]),bytes=native_specs(p)[c[k]]['bytes'],mode='arm',kind=k) for k in ('init','get','release')]) for p,c in CONFIG.items()],absoluteMeasuredRegions=[dict(address=hex(BITS),bytes=8,kind='two shared native32 bitmap words',nativeInitialization=[0xffffffff,0xffff0000]),dict(address=hex(LOCK),bytes=8,kind='partial shared handshake view',ownerHalfwordOffset=4,extensionHalfwordOffset=6,originalAllocationExtentProved=False)],
        totals=totals,actualNormalReturns=sum(v for k,v in totals.items() if k!='unreadyBoundaryStops'),providerCalls=0,actualWaitThunkOrBiosExecutions=0,
        syntheticFinalReadInterleavings=True,actualConcurrentProcessors=False,controls=controls,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),rawSha256=digest(encoded),records=len(records),gzipMtime=0),
        limits=['Original-module-only proof, not original/compiled C equivalence or source credit','Normal readiness is supplied synthetically; natural unready paths stop before the original wait thunk and receive zero normal-return credit',
            'Full two-word tests include synthetic states beyond the initialized48-ID pool; no resource validity or game meaning follows',
            'Late shared-word mutations occur at the measured final native LDR and are controlled fixture interleavings, not concurrent hardware execution',
            'Original linker unknown-data refusals remain unchanged; absolute-region/source adoption requires integrator review',
            'Pinned public inline assembly is comparative reference only; no original assembly provenance or assembly source credit']))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),actualReturns=sum(v for k,v in totals.items() if k!='unreadyBoundaryStops'),sourceCredit=0))


if __name__=='__main__':main()
