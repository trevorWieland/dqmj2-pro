import hashlib
import re
import struct
from project import ROOT, sha256

VIEWS = []


def verify(header):
    text = header.read_text()
    assert 'extern u32 native_fn_0204b61c(u32,u32);' in text
    image = (ROOT/'extract/arm9/arm9.bin').read_bytes()
    config = (ROOT/'config/arm9/symbols.txt').read_text()
    relocations = (ROOT/'config/arm9/relocs.txt').read_text()
    assert re.search(r'kind:function\(arm,size=0xc\) addr:0x0204b61c$',config,re.M)
    assert re.search(r'kind:function\(arm,size=0x94\) addr:0x0204b380$',config,re.M)
    branch = image[0x4b61c:0x4b628]
    target = image[0x4b380:0x4b414]
    assert struct.unpack('<III',branch) == (0xe59fc000,0xe12fff1c,0x0204b380)
    assert re.search(r'^from:0x0204b624 kind:load to:0x0204b380 module:main$',relocations,re.M)
    assert struct.unpack_from('<I',target,12)[0] == 0xe1a04001
    assert struct.unpack_from('<I',target,44)[0] == 0xe3540000
    assert struct.unpack_from('<I',target,92)[0] == 0xe3540000
    return dict(originalTrampoline=dict(program='',processor='arm9',module='main',mode='arm',address='0x204b61c',bytes=12,completeNativeSha256=hashlib.sha256(branch).hexdigest(),
        instructionWitnesses=['LDR IP,[PC] at0204b61c','BX IP at0204b620','original literal0204b624 points to configured ARM main entry0204b380']),
        originalTarget=dict(program='',processor='arm9',module='main',mode='arm',address='0x204b380',bytes=148,completeNativeSha256=hashlib.sha256(target).hexdigest(),
            secondIncomingWordWitness='MOV R4,R1 at0204b38c; full-word CMP R4,#0 at0204b3ac and0204b3dc'),
        originalRelocationsSha256=sha256(ROOT/'config/arm9/relocs.txt'),callerDeclaration='u32 native_fn_0204b61c(u32,u32)',
        rawGlobalStorageViewsNotCompleteDataReconstruction=True,sourceOrExecutionCreditForTrampolineOrTarget=0,completeCalleeSemanticsProven=False)
