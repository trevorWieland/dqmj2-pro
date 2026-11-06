import json
import match_runtime as c
from project import ROOT,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def run():
    results=[]
    for name,folder in[('raw-m2c-repeated-exits','nonmatching/overlay-lane/20261031-birth379/ov000/0221b070-arm'),('wide-loop-only','nonmatching/overlay-lane/20261031-birth382/0221b070'),('wide-loop-narrow-call-and-first-input','nonmatching/overlay-lane/20261031-birth392'),('common-exit-nested-ordinary-if','nonmatching/overlay-lane/20261031-birth393'),('second-required-input','nonmatching/overlay-lane/20261031-birth394')]:
        source=ROOT/folder/'source.c';c.WORK=ROOT/'work/ol397'/name/'compile';rows,unused=c.compare(source,'ov000','2','off',True,thumb=False)
        row=rows[0]
        try:proof=validate(row,qualified_bindings(row),ROOT/'work/ol397'/name/'link')
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
        results.append(dict(name=name,compilation=row,genuineLinkComparison=proof,sourceCredit=0,sourceSha256=sha256(source),contextSha256=sha256(source.with_name('context.h'))))
    report=dict(schemaVersion=1,sourceCredit=0,originalDsExecutions=0,variants=results,generatorSha256=sha256(__file__),reproductionCommand='python experiment_ov000_birth397_20261031.py',limits=['Compile/link history only;original caller/replacement/stat-reset qualification uses395','Common switch exit replaces repeated epilogues;ordinary nestedif replacesm2c comma-Booleanmaterialization','Native221FA70 storesincomingR1 and2220160 preservesit/passesit toD05C;bothordinarycallersprepare0','Wide loop index plusoutgoing(s8)slot castfollowsnativeLSL/ASRcaller sequence,without register forcing','No accepted source or pinned compiler was changed'])
    write_json(ROOT/'evidence/attempts/ov000-birth397-repair-history-20261031.json',report)
    print(json.dumps([dict(name=r['name'],compiledBytes=r['compilation']['compiledBytes'],matchingBytes=r['compilation']['matchingBytes'],genuineExact=r['genuineLinkComparison'].get('exactCallerBytes',False))for r in results]))

if __name__=='__main__':run()
