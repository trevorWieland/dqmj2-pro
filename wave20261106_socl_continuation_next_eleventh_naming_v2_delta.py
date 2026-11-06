import gzip
import json
from project import ROOT,read_json,write_json,sha256

RENAMES={'signature_length':'pub_algorithm','certificate_flag':'date_ok','certificate_name':'issuer'}
LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2'
PREVIOUS=LANE.parent/'eleventh'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next'


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2'or (LANE/'ready.json').exists():raise ValueError('Exact new unsealed naming packet required')
    ready=PREVIOUS/'ready.json'
    if sha256(ready)!='e85ab323ba327b1dadaafe9895b76d0622ff826ec8ca1ca9d72e5044614bd47b':raise ValueError('Original frozen eleventh READY changed')
    immutable=0
    for pin in read_json(ready)['files']:
        if pin.get('role','').startswith('produced-'):continue
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original immutable eleventh pin changed:'+pin['path'])
        immutable+=1
    sources=[]
    for name in ['context.h','020911b0.c','02091c5c.c']:
        before=SOURCE/'eleventh'/name;after=SOURCE/'eleventh-naming-v2'/name;expected=before.read_text()
        for old,new in RENAMES.items():expected=expected.replace(old,new)
        if expected!=after.read_text():raise ValueError('Source delta exceeds exact three identifier renames:'+name)
        sources.append(dict(name=name,beforeSha256=sha256(before),afterSha256=sha256(after),onlyAuthorizedIdentifierRenames=True))
    old=read_json(PREVIOUS/'match.json');new=read_json(LANE/'match.json');rows=[]
    for before in old['matches']:
        after=next(r for r in new['matches']if r['address']==before['address'])
        for key in ['program','processor','module','mode','bytes','compiledBytes','targetSha256','compilerFlags','compilerSha256','outputSha256','relocations','nativeSymbolEntries']:
            if before[key]!=after[key]:raise ValueError('Naming replacement altered executable/profile/binding contract:'+key)
        if not after['realLink']['exactCallerBytes']or before['object']==after['object']:raise ValueError('Fresh genuine naming object absent')
        rows.append(dict(address=after['address'],bytes=after['bytes'],nativeSha256=after['targetSha256'],freshObject=after['object'],genuineCompleteNativeLink=True,unchangedRelocationsBindingsFlagsAndOutput=True))
    prior=json.loads(gzip.decompress((PREVIOUS/'traces.json.gz').read_bytes()));current=json.loads(gzip.decompress((LANE/'traces.json.gz').read_bytes()))
    for trace in prior:
        if trace['caller']=='0x20911b0':trace['fixture']['pub_algorithm']=trace['fixture'].pop('length')
    if prior!=current:raise ValueError('Naming-only runtime fixture observations changed')
    output=LANE/'readability-delta.json';write_json(output,dict(status='passed',sourceCredit=0,ordinaryFunctionCount=2,alreadyProvedBytes=584,renames=RENAMES,originalReadySha256=sha256(ready),originalImmutablePinsChecked=immutable,sources=sources,freshGenuineRows=rows,fixturePairsUnchanged=len(current),actualNativeAndSourceReturns=new['actualNativeAndSourceCallerReturns'],actualNativeCalleeExecution=0,limits=['Only three source/access-view identifier names change: offset1116 pub_algorithm,1455 date_ok,1456 issuer. Types, widths, offsets, control flow, flags, complete executable bytes, relocations, bindings and all native/model observations are unchanged.','Both packets are pending coordinator acceptance alternatives for the same two identities, not additive source credit. The original packet remains immutable and must stay unselected when this replacement is selected.','Field naming follows pinned public metadata corroborated by original ROM accesses, without claiming exact public SDK source-version identity.']))
    return dict(path=output.relative_to(ROOT).as_posix(),sha256=sha256(output))


if __name__=='__main__':print(execute())
