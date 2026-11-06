import json
import match_runtime as c
from project import ROOT,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def run():
    results=[]
    for name,folder in[('raw-erased-width-and-inputs','nonmatching/overlay-lane/20261031-birth379/ov000/0221b624-arm'),('measured-byte-flow','nonmatching/overlay-lane/20261031-birth384'),('typed-state-no-gain','nonmatching/overlay-lane/20261031-birth386'),('explicit-required-inputs','nonmatching/overlay-lane/20261031-birth387')]:
        source=ROOT/folder/'source.c';c.WORK=ROOT/'work/ol391'/name/'compile';rows,unused=c.compare(source,'ov000','2','off',True,thumb=False)
        row=rows[0]
        try:proof=validate(row,qualified_bindings(row),ROOT/'work/ol391'/name/'link')
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
        results.append(dict(name=name,compilation=row,genuineLinkComparison=proof,sourceCredit=0,sourceSha256=sha256(source),contextSha256=sha256(source.with_name('context.h'))))
    report=dict(schemaVersion=1,sourceCredit=0,originalDsExecutions=0,variants=results,generatorSha256=sha256(__file__),reproductionCommand='python experiment_ov000_birth391_20261031.py',limits=['Compile/link history only;native byte-flow ABI uses385 andcaller oracle uses388','Typed signed32+0/signed8+10 state view with actual4-byte alignment gave no additional code equality','No accepted source or pinned compiler was changed;ordinary missing-input and width repairs account for exactness'])
    write_json(ROOT/'evidence/attempts/ov000-birth391-repair-history-20261031.json',report)
    print(json.dumps([dict(name=r['name'],compiledBytes=r['compilation']['compiledBytes'],matchingBytes=r['compilation']['matchingBytes'],genuineExact=r['genuineLinkComparison'].get('exactCallerBytes',False))for r in results]))

if __name__=='__main__':run()
