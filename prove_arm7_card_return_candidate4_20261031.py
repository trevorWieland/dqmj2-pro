import json
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_JUMP,CS_GRP_CALL,CS_OP_IMM
from project import ROOT,sha256,write_json
MODULE='extract/arm7/runtime/arm7-wram.bin'
BASE=0x037f8000
TARGET=0x03803090
EXPECTED='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def qualify_roles(raw):
    word=lambda address:struct.unpack_from('<I',raw,address-BASE)[0]
    if word(TARGET)!=0xe12fff1e or word(0x038031d0)!=TARGET:raise ValueError('Candidate return word or constructor reference changed')
    code=raw[0x038031b0-BASE:0x038031bc-BASE]
    decoded=[(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(code,0x038031b0)]
    if decoded!=[('ldr','r1, [pc, #0x18]'),('ldr','r0, [pc, #0x10]'),('str','r1, [r0, #0x20]')]:raise ValueError('Qualified constructor load/store expression changed')
    if word(0x038031cc)!=0x038096e0:raise ValueError('Constructor second storage base changed')
    return dict(address=hex(TARGET),mode='arm',bytes=4,word=hex(word(TARGET)),nativeHex=raw[TARGET-BASE:TARGET-BASE+4].hex(),
        previousCompleteFunction=dict(address='0x03803070',bytes=32,end='0x03803090',poolAddress='0x0380308c',poolWord=hex(word(0x0380308c))),
        nextFunction='0x03803094',constructor='0x03803168',literalReference='0x038031d0',
        expressionInstructions=['0x038031b0','0x038031b4','0x038031b8'],storedAddress='0x03809700',
        actualIndirectCallObserved=False,callableAbiEstablished=False,sourceCredit=0,initializedDenominatorBytesAdded=0)


def qualify(raw):
    if match_runtime.hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('Measured module changed')
    return qualify_roles(raw)


def main():
    raw=(ROOT/MODULE).read_bytes();candidate=qualify(raw)
    functions=json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    if any(int(row['address'],0)==TARGET for row in functions):raise ValueError('Candidate unexpectedly already inventoried')
    references=[]
    for row in functions:
        if row['module']!='arm7-wram':continue
        address=int(row['address'],0);mode=CS_MODE_THUMB if row['mode']=='thumb' else CS_MODE_ARM
        decoder=Cs(CS_ARCH_ARM,mode);decoder.detail=True
        for instruction in decoder.disasm(raw[address-BASE:address-BASE+row['bodyBytes']],address):
            if (CS_GRP_JUMP in instruction.groups or CS_GRP_CALL in instruction.groups) and instruction.operands and instruction.operands[0].type==CS_OP_IMM and instruction.operands[0].imm==TARGET:
                references.append(dict(caller=row['address'],mode=row['mode'],instruction=hex(instruction.address),mnemonic=instruction.mnemonic))
    controls=[]
    for address in (TARGET,0x038031d0,0x038031cc):
        changed=bytearray(raw);changed[address-BASE]^=1
        try:qualify_roles(changed)
        except ValueError as error:controls.append(dict(changedAddress=hex(address),rejected=True,reason=str(error)))
        else:raise ValueError('Changed native boundary accepted')
    report=ROOT/'evidence/arm7/lane-card-return-candidate4-20261031.json'
    write_json(report,dict(generator='prove_arm7_card_return_candidate4_20261031.py',generatorSha256=sha256(__file__),
        program='',processor='arm7',module='arm7-wram',moduleSha256=EXPECTED,candidate=candidate,
        knownInventoryDirectBranchReferences=references,controls=controls,newSourceCredit=0,sharedConfigurationChanged=False,
        unknownSymbolRefusalPreserved=True,canonicalPromotionRequested=False,
        limitations=['A stored code-aligned BX LR address is a boundary candidate; it does not establish a complete callable ABI or ordinary C meaning',
            'No instruction is added to the linker namespace. The exact108-byte initializer remains unregistered and its unknown function target remains rejected',
            'Direct branch scan covers current mode-qualified heuristic function bodies, not all possible code/data aliases or indirect callers',
            'The4 bytes already belong to the initialized WRAM module; no denominator, source, original-assembly or actual-return credit is added']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),candidateBytes=4,knownDirectRefs=len(references),sourceCredit=0))


if __name__=='__main__':main()
