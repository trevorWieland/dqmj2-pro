import re
import sys
from project import ROOT, sha256
sys.path.insert(0,str(ROOT/'deps/native'))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

VIEWS = [
    ('src/runtime/runtime08/native_main_02048f6c.c','9b91d09fd6dbe034dc002ffc24ae888f2bac2646039cffbffd7dec6a5d61ed25','u32','s32 arg0','native_fn_02048f6c','u32','int'),
    ('src/runtime/runtime07/native_main_020c48f8.c','35de2445df913e0153b944fa4ee67855edef01ae8a4e8db8fcf5ea08ca92c32e','u32','s8 arg0','native_fn_020c48f8','u32','s8'),
    ('src/runtime/runtime07/native_main_020cb42c.c','4f5776c55d3a3ff029c898639092b2c6d1da2ca7c5cbd50b7305788dd6f67288','u32','s32 arg0','native_fn_020cb42c','u32','int'),
    ('src/runtime/runtime07/native_main_020cb2fc.c','8aa1c7d0f6a24487cef15597d3e15dcaecc1a09cab246525b524b0e831a2fcfa','u32','void','native_fn_020cb2fc','u32','void'),
    ('src/runtime/runtime09/native_main_020cd4e8.c','f3abd35261572281725367cbd3ff9e316c8c4f150df89cbf28b590dc3e94517d','u32','u32 arg0, u32 arg1','native_fn_020cd4e8','u32','u32,u32')]


def verify(header):
    text = header.read_text()
    views = []
    for name,digest,result,parameters,import_name,import_result,import_parameters in VIEWS:
        source = ROOT/name
        assert sha256(source) == digest
        original_name = import_name.replace('native_fn_','native_main_')
        assert re.search(r'\b'+result+r'\s+'+original_name+r'\('+re.escape(parameters)+r'\)',source.read_text())
        assert 'extern '+import_result+' '+import_name+'('+import_parameters+');' in text
        views.append(dict(source=name,sourceSha256=digest,acceptedDefinition=result+' '+original_name+'('+parameters+')',
            callerDeclaration=import_result+' '+import_name+'('+import_parameters+')',sourceOrExecutionCredit=0))
    image = (ROOT/'extract/arm9/arm9.bin').read_bytes()
    symbols = (ROOT/'config/arm9/symbols.txt').read_text()
    decoder = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    probes = []
    for address,size,end,words in [(0x02065730,232,0x02065800,5),(0x020cb5c4,428,0x020cb76c,4)]:
        assert re.search(r'kind:function\(arm,size=0x'+format(size,'x')+r'\) addr:0x'+format(address,'08x')+r'$',symbols,re.M)
        native = image[address-0x02000000:address-0x02000000+size]
        instructions = {ins.address:(ins.mnemonic,ins.op_str) for ins in decoder.disasm(native[:end-address],address)}
        if words == 5:
            expected = {0x02065730:('push','{r3, r4, r5, r6, r7, r8, sb, sl, lr}'),0x02065734:('sub','sp, sp, #4'),
                0x02065738:('mov','sl, r0'),0x0206573c:('mov','sb, r1'),0x02065740:('mov','r8, r2'),0x02065744:('mov','r7, r3'),
                0x0206577c:('ldr','r1, [sp, #0x28]')}
            incoming = [dict(address=hex(pc),instruction=operation+' '+operands) for pc,(operation,operands) in instructions.items() if operation.startswith('ldr') and '[sp' in operands]
            assert incoming == [dict(address='0x206577c',instruction='ldr r1, [sp, #0x28]')]
            explanation = 'Nine saved words plus4-byte local frame place the measured fifth incoming word atSP+40.'
        else:
            expected = {0x020cb5c8:('mov','r4, r0'),0x020cb5cc:('mov','sl, r1'),0x020cb5d0:('mov','sb, r2'),0x020cb5d4:('mov','r8, r3'),
                0x020cb658:('ldrsb','r2, [sl]'),0x020cb68c:('strb','r0, [sl]'),
                0x020cb6bc:('ldrsb','r0, [sb]'),0x020cb6c4:('strb','r0, [sb]'),
                0x020cb6c8:('ldrsb','r0, [r8]'),0x020cb6d0:('strb','r0, [r8]')}
            assert not any(op.startswith('ldr') and '[sp' in operands for op,operands in instructions.values())
            incoming = []
            explanation = 'R1/R2/R3 are retained separately and directly accessed with signed-byte loads and byte stores; no incoming stack reads occur in the measured instruction range.'
        assert all(instructions.get(pc) == value for pc,value in expected.items())
        probes.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=size,
            completeNativeSha256=__import__('hashlib').sha256(native).hexdigest(),callerWordInputs=words,originalInstructionWitnesses=[dict(address=hex(pc),mnemonic=op,operands=operands) for pc,(op,operands) in expected.items()],
            incomingStackWordLoads=incoming,qualification=explanation,calleeSourceOrExecutionCredit=0))
    return dict(acceptedCSignatureViews=views,originalNativeInterfaceWitnesses=probes,completeCalleeSemanticsProven=False,suppliedCalleeSourceOrExecutionCredit=0)
