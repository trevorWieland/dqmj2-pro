import hashlib
import re
import sys
from project import ROOT, sha256
sys.path.insert(0,str(ROOT/'deps/native'))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

VIEWS = [
    ('src/save_recovery_records.c','cb6891e60297df0b4df002ff9ef04e28e70c19fe7d1964d7845f8fcc04571b14'),
    ('src/runtime/runtime05/native_main_020629e0.c','2b8cdcf9c44f6f55207338fe94dc0e09f6f49672d0a2d603c3da3991fb8453e3'),
    ('src/runtime/runtime09/native_main_020c8fa8.c','37da572d3f40232c47cbce6e5e9a5fdf6825002ce2c2fde7a80312b13bf7ba97'),
    ('src/mechanics_save/20261030_predicate_abi/native_main_02072f48.c','d6a8593201308390f013358cdb2df4b99ba6ba01c33c138ff1462484e54d766a'),
    ('src/mechanics_save/20261101_lane_holder_pair/native_main_020c9a3c.c','e3f46f5cad4e08bb3c131b5a2b07a919accfa280a499d06a9ee8a362a3767d03'),
    ('src/mechanics_save/20261101_lane_holder_pair/native_main_020cce5c.c','32dc20ad21eb3da8930000c7268c3926f8f6d6eddd06774462d2bfb17600ba8d'),
    ('src/runtime/runtime07/native_main_020c9a84.c','57e2bfd352057c64fba46b5d9772bfb40a08ae303c6f6b83e4195268293f6ee1')]


def verify(header):
    text = header.read_text()
    for name,digest in VIEWS:
        assert sha256(ROOT/name) == digest
    compact = lambda value: re.sub(r'\s+','',value)
    saved = (ROOT/VIEWS[0][0]).read_text()
    original_type = re.search(r'typedef struct\s*\{[^{}]*\}\s*SavedRecord;',saved)[0]
    assert compact(original_type) in compact(text)
    assert 'SavedRecord *save_record_by_id(u32 id)' in saved and 'SavedRecord *save_party_record(int slot)' in saved
    assert 'u32 save_party_count(void)' in saved
    declarations = ['SavedRecord* native_fn_02062a10(u32)','SavedRecord* native_fn_02062a50(int)','u32 native_fn_02062aa0(void)',
        'u32 native_fn_020629e0(void)','u32 native_fn_020c8fa8(void)','u32 native_fn_02072f48(s32)',
        'u32 native_fn_020c9a3c(s32,u32,u32,u32,s16)','u32 native_fn_020cce5c(s32,u32,u32,u32,s16)',
        'u32 native_fn_020c9a84(void*,s16,s16,s8,s8,s8,s32)']
    assert all(compact('extern '+declaration+';') in compact(text) for declaration in declarations)
    getter = (ROOT/VIEWS[2][0]).read_text()
    assert 'return (u32) native_data_021d63c8;' in getter
    image = (ROOT/'extract/arm9/arm9.bin').read_bytes()
    symbols = (ROOT/'config/arm9/symbols.txt').read_text()
    decoder = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    probes = []
    for address in [0x020c9984,0x020ccd44]:
        assert re.search(r'kind:function\(arm,size=0xb8\) addr:0x'+format(address,'08x')+r'$',symbols,re.M)
        body = image[address-0x02000000:address-0x02000000+184]
        instructions = {ins.address-address:(ins.mnemonic,ins.op_str) for ins in decoder.disasm(body[:176],address)}
        expected = {0:('push','{r4, r5, r6, r7, lr}'),4:('sub','sp, sp, #0x1c'),
            8:('mov','r6, r0'),12:('mov','r5, r1'),16:('mov','r4, r2'),20:('mov','r7, r3'),
            28:('ldrb','r2, [sp, #0x30]'),36:('ldrb','r1, [sp, #0x34]'),44:('ldrb','r2, [sp, #0x38]'),
            64:('ldrsb','r2, [sp, #0x3c]'),72:('ldr','r1, [sp, #0x40]')}
        assert all(instructions.get(offset)==value for offset,value in expected.items())
        name = 'native_fn_'+format(address,'08x')
        assert 'extern u32 '+name+'(u32,u32,u32,s32,u8,u8,u8,s8,s32);' in text
        probes.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=184,completeNativeSha256=hashlib.sha256(body).hexdigest(),
            registerWords=4,entryStackWords=5,frameBytes=48,inputStackOffsets=[0,4,8,12,16],inputStackAccesses=['u8','u8','u8','s8','u32'],
            originalInstructionWitnesses=[dict(offset=offset,mnemonic=op,operands=operands) for offset,(op,operands) in expected.items()],calleeSourceOrExecutionCredit=0))
    return dict(acceptedSignatureSources=[dict(path=name,sha256=digest) for name,digest in VIEWS],callerDeclarations=declarations,
        completeNineWordBuilderInterfaces=probes,originalGetterWordAddress='0x21d63c8',completeCalleeSemanticsProven=False,
        suppliedCalleeSourceOrExecutionCredit=0,noNewSaveOrMechanicsMeaningInferred=True)
