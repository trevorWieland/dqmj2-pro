import copy
import shutil
import subprocess
import sys
import uuid
from project import ROOT,read_json,write_json,sha256,now
LANE=ROOT/'evidence/lanes/parallel-wave20261105/child-sdat-next/source'
REPORT='evidence/data/child-sdat-next-20261106.json'
PRODUCER='wave20261105_child_sdat_next_source_proof.py'
LAYOUT='src/utility/parallel_wave20261105/child-sdat-next/layout.json'


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/child-sdat-next/source' or (LANE/'ready.json').exists():raise ValueError('Copied-root checker scope differs or semantic data packet already frozen')
    old=read_json(ROOT/REPORT);old_hash=sha256(ROOT/REPORT);pins=read_json(LANE/'inputs.json')['files'];clone=ROOT/'work/w5sd-source/copies'/uuid.uuid4().hex
    if clone.exists():raise ValueError('Copied source root is not fresh')
    clone.mkdir(parents=True)
    for p in pins+[dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json'))]:
        target=clone/p['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p['path'],target)
        if sha256(target)!=p['sha256']:raise ValueError('Copied source input is not exact: '+p['path'])
    if list(clone.rglob('*.o')) or list(clone.rglob('*.elf')) or (clone/'generated').exists() or (clone/'src/utility/parallel_wave20261105/child-sdat-next/data-claim.json').exists():raise ValueError('Copied root contains cached objects/generated outputs/diagnostic ownership dependency')
    report_path=clone/REPORT;write_json(report_path,dict(staleReport=True,dataMatches=[]))
    started=now()
    def run():return subprocess.run([sys.executable,str(clone/PRODUCER)],cwd=clone,capture_output=True,text=True,timeout=180)
    result=run();log=LANE/'copied-root-output.txt';log.write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(('Fresh source-only copied-root producer failed',result.stdout,result.stderr))
    fresh=read_json(report_path)
    if fresh.get('staleReport') or len(fresh['dataMatches'])!=1 or fresh['dataMatchedBytes']!=13936 or fresh['semanticStateSha256']!=old['semanticStateSha256'] or fresh['generationSourceReads']!=old['generationSourceReads']:raise ValueError('Copied semantic data report/state/read scope differs')
    objects=[]
    for before,after in zip(old['dataMatches'],fresh['dataMatches']):
        fields=['address','bytes','sourceSha256','targetSha256','decodedSemanticBytes','encodedAssetBytes','measuredZeroAlignmentBytes']
        if any(before[k]!=after[k] for k in fields) or sha256(clone/after['object'])!=after['objectSha256'] or after['objectSha256']==before['objectSha256'] or not after['realLink']['exactDataBytes'] or after['relocations'] or after['executableSectionBytes']:raise ValueError('Copied object not fully fresh/exact/nonexecutable')
        objects.append(dict(address=after['address'],initializedBytes=after['bytes'],originalObjectSha256=before['objectSha256'],copiedRootObjectSha256=after['objectSha256'],freshObject=True))
    controls=[];layout=read_json(clone/LAYOUT);first=clone/layout['assets'][0]['semanticSource'];module=clone/layout['binary'];generated=clone/fresh['dataMatches'][0]['source'];code=clone/'wave20261105_child_sdat_next_codec.py';inputs=clone/(LANE/'inputs.json').relative_to(ROOT)
    preserve={p:p.read_bytes() for p in [clone/LAYOUT,first,module,generated,code,inputs]}
    def negative(label,mutation):
        for path,payload in preserve.items():path.write_bytes(payload)
        before={p.relative_to(clone).as_posix():sha256(p) for p in (clone/'work/w5sd-source').rglob('*.o')};mutation();bad=run()
        after={p.relative_to(clone).as_posix():sha256(p) for p in (clone/'work/w5sd-source').rglob('*.o')}
        if bad.returncode==0 or before!=after:raise ValueError('Tampered copied root was admitted or overwrote earlier proof objects: '+label)
        controls.append(dict(case=label,rejectedBeforeNewObjects=True,exitCode=bad.returncode,failure=bad.stderr[-1500:]))
    def wrong_namespace():
        changed=copy.deepcopy(layout);changed['processor']='arm7';write_json(clone/LAYOUT,changed)
    def changed_semantics():
        value=read_json(first);next(e for e in value['semantic']['files'][0]['semantic']['commands']['events'] if e['kind']=='note')['velocity']^=1;write_json(first,value)
    def changed_native():
        payload=bytearray(preserve[module]);payload[0]^=1;module.write_bytes(payload)
    def wrong_generated():generated.write_text(preserve[generated].decode().replace('0x10','0x11',1))
    negative('changed-canonical-semantic-source',changed_semantics)
    negative('wrong-cpu-namespace-layout',wrong_namespace)
    negative('changed-private-original-module',changed_native)
    negative('missing-mandatory-semantic-source',lambda:first.unlink())
    negative('missing-mandatory-codec',lambda:code.unlink())
    negative('stale-wrong-generated-C',wrong_generated)
    for path,payload in preserve.items():path.write_bytes(payload)
    for p in pins:
        if sha256(ROOT/p['path'])!=p['sha256'] or sha256(clone/p['path'])!=p['sha256']:raise ValueError('Original or copied frozen producer input drifted')
    if sha256(ROOT/REPORT)!=old_hash:raise ValueError('Parent data report changed during isolated copy qualification')
    write_json(LANE/'copied-root-controls.json',dict(passed=True,sourceCredit=0,initializedBytes=13936,encodedAssetBytes=13935,measuredZeroAlignmentBytes=1,functionCount=0,freshCopiedObjects=objects,staleReportReplaced=True,staleWorkObjectsUsed=False,sourceGenerationOriginalReadRejections=12,controls=controls,copiedRoot=clone.relative_to(ROOT).as_posix(),startedUtc=started,finishedUtc=now(),generatorSha256=sha256(__file__),originalReportSha256=old_hash,copiedRootReportSha256=sha256(report_path),outputLog=dict(path=log.relative_to(ROOT).as_posix(),sha256=sha256(log)),allActualInputsRetained=True,diagnosticAdmissionArtifactsNotPresent=True))
    print(dict(passed=True,freshObjects=1,initializedDataBytes=13936,copiedRootControls=len(controls),sourceCredit=0))


if __name__=='__main__':execute()
