import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from capstone.arm import ARM_OP_IMM
from link_runtime_unit import measured_module
from match_mechanics_save_20261029_record33 import sha,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA

TARGETS={0x020C3258:'reused recovery controller'}


def main():
    verify_inputs()
    modules=json.loads((ROOT/'provenance/seed-manifest.json').read_text())['modules']
    callers,inputs=[],[]
    for item in modules:
        name=item['name']
        if name!='main' and name!='itcm' and not re.fullmatch(r'ov\d{3}',name):continue
        metadata,binary,config=measured_module(name)
        base=int(metadata['base'],0)
        inputs.append(dict(module=name,sha256=sha(binary),symbols=metadata['symbolsFile'],
            symbolsSha256=sha((ROOT/metadata['symbolsFile']).read_bytes())))
        for alias,mode,n,raw in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',config,re.M):
            start,length=int(raw,0),int(n,0)
            cs=Cs(CS_ARCH_ARM,CS_MODE_ARM if mode=='arm' else CS_MODE_THUMB)
            cs.detail=True
            body=binary[start-base:start-base+length]
            code=list(cs.disasm(body,start))
            for index,instruction in enumerate(code):
                if instruction.mnemonic not in ['bl','blx']:continue
                if not instruction.operands or instruction.operands[0].type!=ARM_OP_IMM:continue
                target=instruction.operands[0].imm&~1
                if target not in TARGETS:continue
                callers.append(dict(module=name,processor='arm9',mode=mode,parent=hex(start),parentBytes=length,
                    alias=alias,nativeSpanSha256=sha(body),callsite=hex(instruction.address),
                    instructionBytes=instruction.bytes.hex(),targetModule='main',target=hex(target),role=TARGETS[target],
                    context=[dict(address=hex(i.address),mnemonic=i.mnemonic,operands=i.op_str,bytes=i.bytes.hex())
                        for i in code[max(0,index-5):index+5]],
                    qualification='Static configured-function disassembly only;literal-pool/data classification,loaded-overlay context andpath reachability require independent validation'))
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,mainSha256=MAIN_SHA,
        sourceCreditAdded=0,targets={hex(a):v for a,v in TARGETS.items()},moduleInputs=inputs,
        callsites=len(callers),distinctParents=len({(r['module'],r['parent'],r['mode']) for r in callers}),
        callers=callers,limitations=[
            'Immediate BL/BLX inventory over configured ARM/Thumb function extents;it is not an executed call graph. Code/data boundaries and containing-function identity may require shared-tail/literal reconciliation.',
            'Logical0/1 identify observed wrapper arguments only. Static calls do not establish physical bank choice,fallback order,chronology,current validity or ordinary boot/load reachability.',
            'Modules remain separate despite overlapping load addresses;no overlay source is authored and no new matching-source credit is claimed.'])
    path=ROOT/'evidence/analysis/save-core-recovery-parent162-20261101.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)+'\n')
    verify_inputs()
    print(dict(callsites=report['callsites'],distinctParents=report['distinctParents']))
    for row in callers:print(row['module'],row['parent'],row['callsite'],row['role'])


if __name__=='__main__':
    main()
