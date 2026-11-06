import json
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
VARIANTS=[('shared-loop-index','20261031-membership374'),('separate-indices','20261031-membership376/separate-indices'),('separate-signed','20261031-membership376/separate-signed'),('reordered-locals','20261031-membership376/found-first')]

def run():
    metadata,image,unused=measured_module('ov001')
    target=image[0x02209AC0-0x021D7240:0x02209AC0-0x021D7240+140]
    results=[]
    for name,path in VARIANTS:
        source=ROOT/'nonmatching/overlay-lane'/path/'source.c'
        c.WORK=ROOT/'work/ol378'/name/'compile'
        try:rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
        except Exception as error:
            if name!='raw-incomplete'or 'void'not in str(error):raise
            results.append(dict(name=name,compileFailed=True,failure=str(error),sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),actualDsExecutions=0,sourceCredit=0))
            continue
        if rows[0].get('compileFailed'):
            if name!='raw-incomplete' or 'void'not in rows[0].get('stdout',''):raise ValueError('Membership378 unexpected compilation failure')
            results.append(dict(name=name,compileFailed=True,compilation=rows,sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),actualDsExecutions=0,sourceCredit=0))
            continue
        directory=ROOT/'work/ol378'/name/'link'
        try:proof=validate(rows[0],qualified_bindings(rows[0]),directory)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=rows[0]['name']:raise
        body=(directory/'caller.bin').read_bytes()
        results.append(dict(name=name,sourceSha256=sha256(source),headerSha256=sha256(source.with_name('context.h')),compilation=rows,genuineLinkComparison=proof,measuredLinkedBytes=len(body),measuredMatchingBytes=sum(a==b for a,b in zip(body,target)),fullNativeSpanEqual=body==target,sourceInterfaceIncomplete=False,actualDsExecutions=0,sourceCredit=0))
    report=dict(schemaVersion=1,sourceCredit=0,romSha256=c.sha((ROOT/'inputs/game.nds').read_bytes()),processor='arm9',program='',module='ov001',mode='arm',address='0x02209AC0',bytes=140,moduleSha256=metadata['sha256'],nativeSpanSha256=c.sha(target),variants=results,scope='Compiler/link-only hypotheses; independent first/reserve loop indices follow ordinary lifetimes without any register declaration or code patch',generatorSha256=sha256(__file__),reproductionCommand='python experiment_ov001_membership378_20261031.py')
    write_json(ROOT/'evidence/attempts/ov001-membership378-index-lifetimes-20261031.json',report)
    print(json.dumps([{k:v for k,v in r.items()if k in['name','compileFailed','measuredLinkedBytes','measuredMatchingBytes','fullNativeSpanEqual','sourceInterfaceIncomplete']}for r in results]))

if __name__=='__main__':run()
