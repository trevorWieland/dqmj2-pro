import json
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
VARIANTS=[('raw-incomplete','20261031-recruit355/ov001/02209cc0-arm'),('signed-byte-consumer','20261031-recruit356/02209cc0'),('wide-boolean','20261031-recruit358/wide-boolean'),('wide-action-order','20261031-recruit358/wide-boolean-action-first'),('sequential-erased-inputs','20261031-recruit362'),('explicit-required-inputs','20261031-recruit363')]

def run():
    metadata,image,unused=measured_module('ov001')
    target=image[0x02209CC0-0x021D7240:0x02209CC0-0x021D7240+1092]
    results=[]
    for name,path in VARIANTS:
        source=ROOT/'nonmatching/overlay-lane'/path/'source.c'
        c.WORK=ROOT/'work/ol365'/name/'compile'
        try:rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
        except Exception as error:
            if name!='raw-incomplete'or 'void'not in str(error):raise
            results.append(dict(name=name,compileFailed=True,failure=str(error),sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),actualDsExecutions=0,sourceCredit=0))
            continue
        if rows[0].get('compileFailed'):
            if name!='raw-incomplete' or 'void'not in rows[0].get('stdout',''):raise ValueError('Recruit365 unexpected compilation failure')
            results.append(dict(name=name,compileFailed=True,compilation=rows,sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),actualDsExecutions=0,sourceCredit=0))
            continue
        directory=ROOT/'work/ol365'/name/'link'
        try:proof=validate(rows[0],qualified_bindings(rows[0]),directory)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=rows[0]['name']:raise
        body=(directory/'caller.bin').read_bytes()
        results.append(dict(name=name,sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),compilation=rows,genuineLinkComparison=proof,measuredLinkedBytes=len(body),measuredMatchingBytes=sum(a==b for a,b in zip(body,target)),fullNativeSpanEqual=body==target,sourceInterfaceIncomplete=name=='sequential-erased-inputs',actualDsExecutions=0,sourceCredit=0))
    report=dict(schemaVersion=1,sourceCredit=0,romSha256=c.sha((ROOT/'inputs/game.nds').read_bytes()),processor='arm9',program='',module='ov001',mode='arm',address='0x02209CC0',bytes=1092,moduleSha256=metadata['sha256'],nativeSpanSha256=c.sha(target),variants=results,scope='Compiler/link-only hypotheses; the byte-equal362 still erases four required pointer/UID arguments and receives no acceptance',generatorSha256=sha256(__file__),reproductionCommand='python experiment_ov001_recruit365_20261031.py')
    write_json(ROOT/'evidence/attempts/ov001-recruit365-caller-shapes-20261031.json',report)
    print(json.dumps([{k:v for k,v in r.items()if k in['name','compileFailed','measuredLinkedBytes','measuredMatchingBytes','fullNativeSpanEqual','sourceInterfaceIncomplete']}for r in results]))

if __name__=='__main__':run()
