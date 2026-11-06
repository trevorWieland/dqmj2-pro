from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import measured_module


def main():
    spans=[(0x020379C4,40),(0x020379EC,52)]
    decoders={'arm':Cs(CS_ARCH_ARM,CS_MODE_ARM),'thumb':Cs(CS_ARCH_ARM,CS_MODE_THUMB)}
    for decoder in decoders.values():decoder.detail=True
    rows=[];interior=[];examined=0;starts=[]
    for module in read_json(ROOT/'evidence/regions/canonical-symbol-functions.json')['canonicalModules']:
        metadata,image,_=measured_module(module['module']);base=int(metadata['base'],0)
        for function in module['functions']:
            address=int(function['address'],0);size=function['size'];examined+=1
            if module['module']=='main':
                starts.extend(dict(address=hex(address),span=hex(target))for target,length in spans if target<address<target+length)
            for ins in decoders[function['mode']].disasm(image[address-base:address-base+size],address):
                if ins.mnemonic not in ['b','bl','blx','beq','bne','bge','bgt','ble','blt','bhi','bls','blo','bhs','bpl','bmi','bvs','bvc']:continue
                if not ins.operands or ins.operands[0].type!=2:continue
                destination=ins.operands[0].imm&~1
                for target,length in spans:
                    if not target<=destination<target+length:continue
                    if module['module']=='main'and target<=ins.address<target+length:continue
                    item=dict(sourceModule=module['module'],sourceFunction=hex(address),sourceInstruction=hex(ins.address),
                        target=hex(destination),targetFunction=hex(target),boundaryOnly=destination==target,sourceMode=function['mode'])
                    rows.append(item)
                    if destination!=target:interior.append(item)
    assert not interior and not starts
    write_json(ROOT/'evidence/abi/main-sound-fader92-boundary-candidates-20261102.json',dict(passed=True,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),sourceCredit=0,
        examinedConfiguredFunctionSpans=examined,externalDirectCandidates=rows,
        externalDirectInteriorCandidates=interior,configuredInteriorStarts=starts,
        indirectTargetsAndArbitraryDataReferencesNotProven=True,
        reproductionCommand='python audit_main_sound_fader92_boundaries_20261102.py',
        scope='Configured ARM/Thumb disassembly candidate audit, not a claim that every decoded byte is executable'))
    print(dict(examined=examined,directCandidates=len(rows),externalInterior=len(interior),configuredInteriorStarts=len(starts)))


if __name__=='__main__':
    main()
