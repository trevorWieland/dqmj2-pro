import json
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
VARIANTS=[('old-narrow-loop','20261031-recruit320/buffer'),('wide-signed-loop','20261031-recruit351/signed-loop'),('wide-unsigned-loop','20261031-recruit351/unsigned-loop'),('wide-loop-pointer-return','20261031-recruit352/pointer-view')]

def run():
    metadata,image,unused=measured_module('ov001')
    target=image[0x022095F4-0x021D7240:0x022095F4-0x021D7240+400]
    results=[]
    for name,path in VARIANTS:
        source=ROOT/'nonmatching/overlay-lane'/path/'source.c'
        c.WORK=ROOT/'work/ol354'/name/'compile'
        rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
        directory=ROOT/'work/ol354'/name/'link'
        try:proof=validate(rows[0],qualified_bindings(rows[0]),directory)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=rows[0]['name']:raise
        body=(directory/'caller.bin').read_bytes()
        results.append(dict(name=name,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),compilation=rows,genuineLinkComparison=proof,measuredLinkedBytes=len(body),measuredMatchingBytes=sum(a==b for a,b in zip(body,target)),fullNativeSpanEqual=body==target))
    getter=image[0x021FBE70-0x021D7240:0x021FBE70-0x021D7240+24]
    report=dict(schemaVersion=1,sourceCredit=0,romSha256=c.sha((ROOT/'inputs/game.nds').read_bytes()),processor='arm9',program='',module='ov001',mode='arm',address='0x022095F4',bytes=400,moduleSha256=metadata['sha256'],nativeSpanSha256=c.sha(target),variants=results,qualifiedGetterView=dict(address='0x021FBE70',bytes=24,spanSha256=c.sha(getter),returnView='u8*',nativeFacts=['Literal addresses02239ABC,byte+67 is read,zero gates return0 and nonzero returns the literal address','The measured template is cleared/copied as132 bytes by its callers; a byte pointer preserves actual byte-scaled accesses','No incoming word is consumed by the24-byte getter; original formal typedef/name remains unknown'],scope='New caller-specific context only; accepted getter source and shared projections remain unchanged'),loopView=dict(indexView='s32',outgoingSlotCast='s8',nativeFacts=['ADD R5,R5,1 and CMP R5,R0 retain a full-word loop state','LSL/ASR24 occurs only in the outgoing62E44 R1 view','The narrow-loop draft instead truncates its loop increment,changes saved registers and emits404 bytes']),actualDsExecutions=0,generatorSha256=sha256(__file__),reproductionCommand='python experiment_ov001_recruit354_20261031.py')
    write_json(ROOT/'evidence/attempts/ov001-recruit354-type-repair-20261031.json',report)
    print(json.dumps([{k:r[k]for k in['name','measuredLinkedBytes','measuredMatchingBytes','fullNativeSpanEqual']}for r in results]))

if __name__=='__main__':run()
