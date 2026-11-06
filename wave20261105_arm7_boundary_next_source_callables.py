import copy
from project import ROOT,read_json,sha256
import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_REG_PC
from link_arm7_bulk_20261030 import namespace
from wave20261105_arm7_boundary_next_source_build import CERTIFICATE_SHA,LANE
CALLABLE_SHA='e98acab20c4b22cb7d2e6b687d2a26f289e8f44de6def1c6813df1c774b97cae'
EXPECTED={0x027e1ad4:dict(size=20,origin=0x027e1724,target=0x027e1ae8,sha='c8ba599a4eba7b471ef5d8da2304a450c51fbcd36e2eac0d0579bc7c824bea66',instructions=[('ldr','ip, [pc, #8]'),('lsl','r0, r0, #0x10'),('lsr','r0, r0, #0x10'),('bx','ip')]),0x027e1c00:dict(size=12,origin=0x027e19fc,target=0x027e1c0c,sha='0efe594f4dc2a41a0386fc147b3dc29c9a162be343824591b6098b457423baf3',instructions=[('ldr','ip, [pc]'),('bx','ip')])}


def verify(row,image,certificate,functions):
    address=int(row['address'],0);expected=EXPECTED.get(address)
    if expected is None or (row['program'],row['processor'],row['module'],row['mode'],row['architecture'])!=('','arm7','arm7-main','arm','ARMv4T'):raise ValueError('Exact original callback entry namespace/mode differs')
    if (row['observedSpanBytes'],int(row['literalOrigin'],0),int(row['tailTarget'],0),row['observedSpanSha256'])!=(expected['size'],expected['origin'],expected['target'],expected['sha']):raise ValueError('Original callback entry/span/pointer origin/target differs')
    base=0x027e0000;body=image[address-base:address-base+expected['size']]
    if C.sha(body)!=expected['sha'] or int.from_bytes(image[expected['origin']-base:expected['origin']-base+4],'little')!=address:raise ValueError('Actual whole callback tail thunk/pointer word changed')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;instructions=list(decoder.disasm(body[:-4],address))
    if [(i.mnemonic,i.op_str) for i in instructions]!=expected['instructions'] or any((int.from_bytes(i.bytes,'little')>>28)!=14 for i in instructions):raise ValueError('Actual original ARMv4T callback transfer/argument flow differs')
    load=instructions[0];pool=load.address+8+load.operands[1].mem.disp
    if pool!=address+expected['size']-4 or int.from_bytes(image[pool-base:pool-base+4],'little')!=expected['target'] or expected['target']&1:raise ValueError('Actual original callback tail literal/mode differs')
    target=functions.get(expected['target'])
    if target is None or (target['program'],target['processor'],target['module'],target['mode'],target['kind'])!=('','arm7','arm7-main','arm','function'):raise ValueError('Original tail target lacks qualified same-namespace ARM entry')
    reads=[r for r in certificate['literalReads'] if int(r['address'],0)==expected['origin']]
    if not reads:raise ValueError('Original selected caller does not read this callback word')
    for read in reads:
        origin=int(read['origin'],0);instruction=next(decoder.disasm(image[origin-base:origin-base+4],origin,count=1),None)
        if instruction is None or not instruction.mnemonic.startswith('ldr') or instruction.operands[1].mem.base!=ARM_REG_PC or origin+8+instruction.operands[1].mem.disp!=expected['origin']:raise ValueError('Original caller callback load/origin differs')
    return dict(program='',processor='arm7',module='arm7-main',mode='arm',kind='function',address=hex(address),boundarySource='exact-original-caller-function-word-and-ARMv4T-tail-thunk',originalPointerWord=hex(address),originalPointerPool=hex(expected['origin']),actualCallerLoads=reads,observedEntryBytes=expected['size'],observedEntrySha256=expected['sha'],originalTailTarget=target,sourceCredit=0,calleeSourceCredit=0,nativeCalleeBodiesExecuted=0,bindingOnly=True)


def qualified():
    if sha256(LANE/'callable-entries-qualified.json')!=CALLABLE_SHA or sha256(LANE/'native-certificate.json')!=CERTIFICATE_SHA:raise ValueError('Immutable original callable/native certificate changed')
    certificate=read_json(LANE/'native-certificate.json');image=(ROOT/certificate['binary']).read_bytes()
    if C.sha(image)!=certificate['inputModuleSha256']:raise ValueError('Original ARM7 module changed')
    unused,functions=namespace('');return {int(r['address'],0):verify(r,image,certificate,functions) for r in read_json(LANE/'callable-entries-qualified.json')['entries']}


def controls():
    certificate=read_json(LANE/'native-certificate.json');image=(ROOT/certificate['binary']).read_bytes();unused,functions=namespace('');rows=read_json(LANE/'callable-entries-qualified.json')['entries'];proofs=[];bad=[]
    for row in rows:
        proofs.append(verify(row,image,certificate,functions))
        for field,value in [('program','dwc/utility.bin/move/child.srl'),('processor','arm9'),('module','arm7-wram'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('address',row['tailTarget']),('literalOrigin',hex(int(row['literalOrigin'],0)+4)),('tailTarget',hex(int(row['tailTarget'],0)+4)),('observedSpanBytes',row['observedSpanBytes']+4),('observedSpanSha256','0'*64)]:
            changed=copy.deepcopy(row);changed[field]=value
            try:verify(changed,image,certificate,functions)
            except ValueError as error:bad.append(dict(entry=row['address'],case=field,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original callable certificate admitted')
        changed=bytearray(image);changed[int(row['address'],0)-0x027e0000]^=1
        try:verify(row,bytes(changed),certificate,functions)
        except ValueError as error:bad.append(dict(entry=row['address'],case='actual-native-thunk-code',rejected=True,reason=str(error)))
        else:raise ValueError('Modified original callable thunk admitted')
        changed=bytearray(image);offset=int(row['literalOrigin'],0)-0x027e0000;changed[offset:offset+4]=int(row['tailTarget'],0).to_bytes(4,'little')
        try:verify(row,bytes(changed),certificate,functions)
        except ValueError as error:bad.append(dict(entry=row['address'],case='actual-pointer-redirected-to-canonical-tail',rejected=True,reason=str(error)))
        else:raise ValueError('Original callable pointer redirected to its tail')
    return dict(status='passed',sourceCredit=0,entries=proofs,negativeControls=bad,originalThunkToTailControls=thunk_transfers(image),nativeCalleeBodiesExecutedInCallerFixtures=0,originalTailBodiesExecuted=0,newEntryOwnershipGranted=False,limits=['Only two exact original callback entry words gain binding-only ARM typing; no alias/redirection, reconstructed callee body, storage/source credit or arbitrary entry admission. Separate controls execute the exact two original tiny thunks only until their actual measured tail entry, never its body.'])


def thunk_transfers(image):
    import unicorn
    from unicorn import arm_const as R
    results=[];bad=[]
    if not hasattr(R,'UC_CPU_ARM_TI925T'):raise ValueError('Pinned ARMv4T unit CPU unavailable')
    for address,expected in EXPECTED.items():
        body=image[address-0x027e0000:address-0x027e0000+expected['size']]
        def evaluate(raw,value,flags):
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x027e0000,0x20000);vm.mem_write(address,raw)
            initial=[(0x12345678+i*0x1010101)&0xffffffff for i in range(15)];initial[0]=value;initial[13]=0x027ff000;initial[14]=0x027fd001;vm.reg_write(R.UC_ARM_REG_CPSR,flags|0x10)
            for reg,word in zip(C.REGISTERS,initial):vm.reg_write(reg,word)
            pcs=[]
            def hook(uc,at,size,user):
                pcs.append(at)
                if at==expected['target']:uc.emu_stop()
                elif not address<=at<address+expected['size']-4:raise ValueError('Thunk escaped the exact measured body/tail boundary')
            vm.hook_add(unicorn.UC_HOOK_CODE,hook);vm.emu_start(address,expected['target']+4,count=16);actual=[vm.reg_read(reg) for reg in C.REGISTERS];wanted=list(initial);wanted[0]=value&0xffff if expected['size']==20 else value;wanted[12]=expected['target']
            if actual!=wanted or vm.reg_read(R.UC_ARM_REG_CPSR)!=(flags|0x10) or pcs[-1]!=expected['target']:raise ValueError('Actual original ARMv4T thunk R0/IP/LR/SP/mode/flags transfer differs')
            return dict(argument=value,flags=hex(flags),registers=actual,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),pcs=pcs,stoppedBeforeTailBody=True,actualCallerReturn=False)
        cases=[evaluate(body,value,flags<<28) for value in [0,1,65535,65536,0x12345678,0x80000000,0xffffffff] for flags in [0,5,10,15]]
        changed=bytearray(body);changed[-4:]=(expected['target']+4).to_bytes(4,'little')
        try:evaluate(bytes(changed),0x12345678,0xa0000000)
        except ValueError as error:bad.append(dict(entry=hex(address),case='wrong-actual-tail-word',rejected=True,reason=str(error),analysisOnlyInMemoryTamper=True))
        else:raise ValueError('Wrong actual thunk tail transfer admitted')
        results.append(dict(entry=hex(address),nativeSpanSha256=C.sha(body),cases=cases,actualThunkToTailTransfers=len(cases),tailBodyInstructionsExecuted=0,sourceCredit=0))
    return dict(status='passed',cpu='TI925T ARMv4T instruction-set unit model',originalThunkEntriesExecuted=2,actualThunkToTailTransfers=sum(r['actualThunkToTailTransfers'] for r in results),sourceCredit=0,results=results,negativeControls=bad)
