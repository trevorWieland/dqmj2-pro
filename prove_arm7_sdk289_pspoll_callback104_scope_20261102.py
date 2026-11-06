import hashlib
import itertools
import json
from pathlib import Path
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk288_transmit_context_20261102 as context
import link_arm7_bulk_20261030 as strict
from project import ROOT,sha256,write_json

TOP,SIZE,CODE=0x027f0950,104,100

def case(main,wram,status,retry,old,mode,offset,index):
    cpu,setup=context.setup(main,wram,index,mode,context_offset=offset);base=setup['context'];frame=context.DATA+0x5100;installed=int.from_bytes(cpu.mem_read(base+0x464,4),'little')
    if installed!=TOP:raise ValueError('Real initializer did not install callback in this supported mode')
    initial_values={0x53c:old,0x540:old^0x55555555,0x544:old^0xaaaaaaaa,0x54c:old};cpu.mem_write(frame,struct.pack('<HHH',status,0x55aa,retry));cpu.mem_write(base+0x454,struct.pack('<H',0xffff))
    for offset,value in initial_values.items():cpu.mem_write(base+offset,struct.pack('<I',value))
    rng=random.Random(0x289000+index);initial=[rng.getrandbits(32)for r in REGISTERS];initial[:2]=[frame,rng.getrandbits(32)];initial[-2:]=[context.STACK+0x3800,context.STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    state=dict(returned=False);stores=[];visited=[]
    def code(machine,pc,size,user):
        if pc==context.STOP:state['returned']=True;machine.emu_stop();return
        if not TOP<=pc<TOP+CODE:raise ValueError('Callback escaped its complete100-byte ARM instruction span')
        visited.append(pc)
    def write(machine,access,address,width,value,user):stores.append([address,width,value&((1<<(width*8))-1)])
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:cpu.emu_start(installed,context.STOP+4,count=200)
    finally:
        for token in tokens:cpu.hook_del(token)
    expected=[[base+0x544,4,(initial_values[0x544]+(retry&255))&0xffffffff]]
    if status&2:expected.append([base+0x540,4,(initial_values[0x540]+1)&0xffffffff])
    else:expected.extend([[base+0x53c,4,(initial_values[0x53c]+1)&0xffffffff],[base+0x54c,4,(initial_values[0x54c]+1)&0xffffffff]])
    expected.append([base+0x454,2,0]);checks=dict(actualReturn=state['returned'],independentOrderedStores=stores==expected,calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(index&1),realInstallerPointer=installed==TOP,ignoredSecondWordNoSourceMeaning=True)
    return dict(statusWord=status,retryWord=retry,counterSeed=old,modeArgument=mode,context=hex(base),installedPointerWord=hex(base+0x464),actualOwnReturn=state['returned'],passed=all(checks.values()),checks=checks,orderedStores=stores,expectedOrderedStores=expected,instructions=len(visited),visited=sorted(set(visited)),nativePrerequisiteReturns=setup['prerequisiteReturns'],prefixBoundaryNormalReturnCredit=0,wrongFullRetryModelRejected=retry!=retry&255,sourceCredit=0)

def main():
    main_path=ROOT/'extract/arm7/runtime/arm7-main.bin';wram_path=ROOT/'extract/arm7/runtime/arm7-wram.bin';main=main_path.read_bytes();wram=wram_path.read_bytes();body=main[TOP-context.MAIN:TOP-context.MAIN+SIZE]
    if struct.unpack_from('<I',body,100)[0]!=context.WORD or struct.unpack_from('<I',body,96)[0]!=0xe12fff1e:raise ValueError('Callback final BX and sole pointer literal changed')
    inv_path=ROOT/'evidence/arm7/ghidra-runtime-inventory.json';inventory=json.loads(inv_path.read_text());overlaps=[r for r in inventory['functions']if r['module']=='arm7-main'and int(r['minimumAddress'],0)<TOP+SIZE and int(r['maximumAddress'],0)>=TOP]
    if overlaps:raise ValueError('Unreviewed callback extent overlaps existing configured function')
    modules,functions=strict.namespace('')
    if TOP in functions:raise ValueError('Original callback unknown-function refusal changed')
    refs=[];pointers=[]
    for module,binary,base in [('arm7-main',main,context.MAIN),('arm7-wram',wram,context.WRAM)]:
        for offset in range(0,len(binary)-3,4):
            word=struct.unpack_from('<I',binary,offset)[0];pc=base+offset
            if TOP<=word<TOP+SIZE:pointers.append(dict(module=module,address=hex(pc),target=hex(word),kind='aligned-word-candidate'))
            if word&0x0e000000==0x0a000000 and word>>28!=15:
                displacement=(word&0xffffff)<<2
                if displacement&0x02000000:displacement-=0x04000000
                target=(pc+8+displacement)&0xffffffff
                if TOP<=target<TOP+SIZE:refs.append(dict(module=module,address=hex(pc),target=hex(target),insideOwnBody=TOP<=pc<TOP+CODE,link=bool(word&0x01000000)))
    if any(not r['insideOwnBody']and int(r['target'],0)!=TOP for r in refs):raise ValueError('Outside aligned ARM candidate enters callback interior')
    results=[]
    for index,args in enumerate(itertools.product((0,1,2,3,0xffff),(0,1,127,255,256,257,0xffff),(0,1,0xffffffff),(0,2,3),(0,4))):
        result=case(main,wram,*args,index);results.append(result)
        if not result['passed']:raise ValueError('Native callback independent state model failed')
    reference=ROOT/'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/libraries/wl_arm7/src/TxCtrl.c';report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),contextGenerator=Path(context.__file__).name,contextGeneratorSha256=sha256(context.__file__),romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',processor='arm7',program='',module='arm7-main',mode='arm',address=hex(TOP),bytes=SIZE,instructionBytes=CODE,literalBytes=4,inputMainSha256=sha256(main_path),inputWramSha256=sha256(wram_path),targetSha256=hashlib.sha256(body).hexdigest(),instructionSha256=hashlib.sha256(body[:CODE]).hexdigest(),literal=body[CODE:].hex(),inventory=inv_path.relative_to(ROOT).as_posix(),inventorySha256=sha256(inv_path),configuredOverlaps=overlaps,defaultCanonicalEntryAbsent=True,alignedArmBranchCandidates=refs,alignedPointerCandidates=pointers,actualOwnReturns=len(results),actualPrerequisiteReturns=sum(len(r['nativePrerequisiteReturns'])for r in results),allPassed=all(r['passed']for r in results),sourceReference=reference.relative_to(ROOT).as_posix(),sourceReferenceSha256=sha256(reference),sourceReferenceName='TxqEndPsPoll',referenceRevisionEquivalenceUnproved=True,results=results,sourceCredit=0,denominatorByteIncrease=0,assemblyProvenanceCredit=0,limitations=['Aligned ARM candidate scan does not prove arbitrary indirect or unaligned data reference absence','Direct execution uses real installed callback pointer with synthetic frame/status/counters; enclosing hardware IRQ scene reachability is unproved','No shared configuration namespace or source-admission adapter changed']);write_json(ROOT/'evidence/attempts/arm7-sdk289-pspoll-callback104-scope-20261102.json',report);print(json.dumps({k:report[k]for k in('actualOwnReturns','actualPrerequisiteReturns','allPassed','targetSha256','sourceCredit')}),flush=True)

if __name__=='__main__':main()
