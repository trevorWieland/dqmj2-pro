import hashlib
import itertools
import json
import random
from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
import arm7_sdk177_unsigned_quotient_native_20261101 as native
from project import ROOT,sha256,write_json
REPORT=ROOT/'evidence/arm7/sdk179-unsigned-quotient-abi-20261101.json'
def cases():
    edges=(0,1,255,65535,0xffffffff,1<<32,1<<63,0xffffffffffffffff);pairs=list(itertools.product(edges,(0,1,2,3,10,1<<32,1<<63,0xffffffffffffffff)));rng=random.Random(0x179)
    return pairs+[(rng.getrandbits(64),rng.getrandbits(64)or 1)for unused in range(128)]+[(rng.getrandbits(64),0)for unused in range(64)]
def measure():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[]
    for index,(numerator,denominator)in enumerate(cases()):
        record=native.run(main,wram,numerator,denominator,index)
        expected=numerator//denominator if denominator else numerator
        if record['quotient']!=expected or not record['calleeSaved']or not record['nonstackUnchanged']:raise ValueError('Explicit canonical u64 helper contract failed')
        if not denominator and[pc for pc,size,mode in record['visited']]!=[0x3806bf0,0x3806bf4,0x3806bf8,0x3806c04,0x3806c08,0x3806c0c,0x3806c10]:raise ValueError('Zero-denominator native direct-return path differs')
        records.append(record)
    inventory=ROOT/'evidence/arm7/ghidra-runtime-inventory.json';row=next(r for r in json.loads(inventory.read_text())['functions']if int(r['address'],0)==native.ENTRY and r['module']=='arm7-wram')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);zero=[]
    for pc in(0x3806bf0,0x3806bf4,0x3806bf8,0x3806c04,0x3806c08,0x3806c0c,0x3806c10):
        offset=pc-native.WRAM;insn=next(decoder.disasm(wram[offset:offset+4],pc));zero.append(dict(address=hex(pc),word=hex(int.from_bytes(wram[offset:offset+4],'little')),mnemonic=insn.mnemonic,operands=insn.op_str))
    expected_ops=[('push','{r4, r5, r6, r7, fp, ip, lr}'),('mov','r4, #0'),('b','#0x3806c04'),('orrs','r5, r3, r2'),('bne','#0x3806c14'),('pop','{r4, r5, r6, r7, fp, ip, lr}'),('bx','lr')]
    if[(r['mnemonic'],r['operands'])for r in zero]!=expected_ops:raise ValueError('Canonical zero helper instruction semantics differ')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',mode='arm',entry=hex(native.ENTRY),inputModuleSha256=hashlib.sha256(wram).hexdigest(),moduleInventorySha256=sha256(inventory),canonicalInventoryEntry=row,helperCAbi=dict(arguments=['u64 numerator inR0:R1','u64 denominator inR2:R3'],returnValue='u64 quotient inR0:R1',calleeSavedAndStackPreserved=True,nonzeroContract='floor unsigned numerator/denominator',zeroContract='numerator returned unchanged',sourceApiName='native_host_arm7_wram_03806bf0'),actualOwnReturns=len(records),nonzeroActualReturns=sum(bool(r['denominator'])for r in records),zeroActualReturns=sum(not r['denominator']for r in records),records=records,zeroPathInstructions=zero,zeroUniversalNumeratorReason='ORRS tests onlyR3|R2; zero path restores saved registers and BX LR without writingR0/R1',siblingEntry=dict(address='0x3806bfc',sourceCredit=0,notUsedByCaller=True),completeHelperBoundaryOrGlobalCfgNotClaimed=True,originalHelperSourceAndAssemblyCredit=0,initializedDenominatorDelta=0,sourceCredit=0)
    write_json(REPORT,report);return report
if __name__=='__main__':
    result=measure();print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),returns=result['actualOwnReturns'],nonzero=result['nonzeroActualReturns'],zero=result['zeroActualReturns'])),flush=True)
