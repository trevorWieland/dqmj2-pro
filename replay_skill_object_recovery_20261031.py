import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import recover_skill_stack_input_20261031 as S
import save_core_resource_release_build_20261031 as B
from preparation_build_20261029 import FLAGS
from link_runtime_unit import measured_module
from match_mechanics_save_20261029_record33 import verify_inputs
SOURCE='nonmatching/save-core/20261031-skill-input-family/native_main_02057d1c_recovered_object.c'
RAW='nonmatching/save-core/20261031-skill-input-family/native_main_02057d1c_typed_self.c'
ASM='evidence/generated/20261031-skill-input/main_02057d1c.s'


def main():
    verify_inputs()
    assert B.sha((ROOT/RAW).read_bytes())=='158b264dee57093f3b493bd1d2945d7f8dadd94900854757546fc105dc2f5362'
    raw=(ROOT/RAW).read_text()
    assembly=(ROOT/ASM).read_text()
    source,changes=S.recover(raw,assembly)
    assert source==(ROOT/SOURCE).read_text() and len(changes)==1
    B.MODULE,B.ENTRY,B.LENGTH,B.NAME,B.SOURCE='main',0x02057D1C,304,'native_main_02057d1c',SOURCE
    B.WORK='work/save-core-lane/20261031-skill-input-recovery-check'
    B.FLAGS=[*FLAGS,'-opt','speed']
    arm=measured_module('main')[1]
    native=arm[0x57D1C:0x57E4C]
    assert B.sha(native)=='e5418d5284fc81d347e48271c7438e3c51e81a796364905c85ff1abf869c518a'
    row,body=B.build(native)
    assert row['compiledBytes']==308 and row['sameOffsetBytes']==178 and not row['exactByteEqual']
    report=dict(schemaVersion=1,changes=changes,builds=[row],newSourceBytes=0,knownArithmeticErrorRetained=True,
        inputs=[dict(path=p,sha256=B.sha((ROOT/p).read_bytes())) for p in (RAW,ASM,SOURCE,'recover_skill_stack_input_20261031.py','qualified_skill_input_contexts_20261031.py')],
        reproductionCommand='python replay_skill_object_recovery_20261031.py',limitations=[
            'Only a compiling source-shape hypothesis;full caller native execution and signed-division correction remain required',
            'Generated assembly is scaffolding supporting the conservative text transform,not reconstructed source or a complete frame proof',
            'No exact source credit;source remains nonmatching. The emitted scalar declarations and other call signatures remain separate hypotheses'])
    target=ROOT/'evidence/attempts/skill-input-recovered-object-20261031.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    verify_inputs()
    print(dict(compiledBytes=len(body),sameOffsetBytes=row['sameOffsetBytes'],exact=False,sourceCredit=0,reportSha256=B.sha(target.read_bytes())))


if __name__=='__main__':main()
