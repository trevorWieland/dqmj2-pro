import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,now
from qualify_oracle_context_cache_v2_20261106 import ast_proof,controls
LANE=ROOT/'evidence/lanes/parallel-wave20261105/source-capture-performance-next'
WORK=ROOT/'work/w5cp'
REVISION='af5a4bd4f100fe5a727824a00a21e0ae3442b1a6'
CAPTURE='evidence/verification/cohort162-captured-oracle-closure-20261031.json'


def git_blob(revision,name):return subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT)


def materialize():
    if WORK!=ROOT/'work/w5cp' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/source-capture-performance-next':raise ValueError('New real-epoch comparator directories differ')
    proof=ast_proof();metadata=WORK/('real162-'+uuid.uuid4().hex[:8]);root=metadata/'root'
    if metadata.exists() or shutil.disk_usage(ROOT).free<4*1024**3:raise ValueError('New immutable source snapshot is not fresh or disk space is insufficient')
    root.mkdir(parents=True);raw=git_blob(REVISION,CAPTURE);capture=json.loads(raw)
    if capture['missingRequiredPaths'] or capture['registrySha256']!='e58cc14722e45de2cbdd4c76bfd4bf94a3745d139434ffb52c120f90e1f37006':raise ValueError('Pinned captured162source epoch differs')
    tree_raw=subprocess.check_output(['git','ls-tree','-rz',REVISION],cwd=ROOT);tree={}
    for row in tree_raw.split(b'\0'):
        if not row:continue
        fields,name=row.split(b'\t',1);mode,kind,oid=fields.decode().split();tree[name.decode('utf-8')]=(mode,kind,oid)
    names=set(capture['sourceAndEvidenceHashes']);bootstrap=['oracle_source_closure_20261031.py','static_json_reads_20261031.py','project.py'];names.update(bootstrap);pins=[];bytes_written=0;started=now();begin=time.perf_counter();log=metadata/'git-materialization-stderr.txt'
    state=dict(status='materializing-immutable-git-captured-source',sourceCredit=0,sourceCommit=REVISION,capture=dict(path=CAPTURE,sha256=hashlib.sha256(raw).hexdigest()),metadata=metadata.relative_to(ROOT).as_posix(),root=root.relative_to(ROOT).as_posix(),startedUtc=started,requestedFiles=len(names),copiedFiles=0,bytesCopied=0)
    write_json(metadata/'state.json',state)
    with log.open('wb') as errors:
        process=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors)
        try:
            for name in sorted(names):
                relative=Path(name)
                if relative.is_absolute() or '..' in relative.parts or not name in tree:raise ValueError('Captured source path escapes/missing in immutable tree: '+name)
                mode,kind,oid=tree[name]
                if mode not in ['100644','100755'] or kind!='blob':raise ValueError('Captured tree contains a nonregular source blob; exact filesystem semantics need separate qualification')
                target=root/relative
                if not target.resolve().is_relative_to(root.resolve()):raise ValueError('Source snapshot write escaped owned directory')
                target.parent.mkdir(parents=True,exist_ok=True);process.stdin.write((oid+'\n').encode());process.stdin.flush();header=process.stdout.readline().decode().split()
                if len(header)!=3 or header[0]!=oid or header[1]!='blob':raise ValueError('Unexpected immutable Git blob response')
                size=int(header[2]);remaining=size;digest=hashlib.sha256()
                with target.open('wb') as stream:
                    while remaining:
                        chunk=process.stdout.read(min(1024*1024,remaining))
                        if not chunk:raise ValueError('Truncated immutable Git blob')
                        stream.write(chunk);digest.update(chunk);remaining-=len(chunk)
                if process.stdout.read(1)!=b'\n':raise ValueError('Git blob boundary differs')
                actual=digest.hexdigest();expected=capture['sourceAndEvidenceHashes'].get(name)
                if expected is not None and actual!=expected:raise ValueError('Captured source hash differs from immutable commit: '+name)
                pins.append(dict(path=name,sha256=actual,bytes=size,gitBlob=oid,role='captured-source-input' if name in capture['sourceAndEvidenceHashes'] else 'collector-runtime-bootstrap'));bytes_written+=size
                if len(pins)%500==0:
                    state.update(copiedFiles=len(pins),bytesCopied=bytes_written);write_json(metadata/'state.json',state);print(dict(copiedFiles=len(pins),bytesCopied=bytes_written),flush=True)
            process.stdin.close()
            if process.wait(timeout=30):raise ValueError('Immutable Git object stream failed')
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=30)
    name='oracle_source_closure_v2_20261106.py';target=root/name;shutil.copyfile(ROOT/name,target);pins.append(dict(path=name,sha256=sha256(target),bytes=target.stat().st_size,role='candidate-collector-bootstrap'))
    if sha256(root/'recovery.json')!=capture['registrySha256'] or sha256(root/'oracle_source_closure_20261031.py')!=proof['legacySourceSha256'] or sha256(root/name)!=proof['newSourceSha256']:raise ValueError('Copied source registry/collector epoch differs')
    snapshot=dict(schemaVersion=1,sourceCredit=0,sourceCommit=REVISION,originalCapture=dict(path=CAPTURE,sha256=hashlib.sha256(raw).hexdigest(),capturedPaths=len(capture['sourceAndEvidenceHashes'])),metadata=metadata.relative_to(ROOT).as_posix(),root=root.relative_to(ROOT).as_posix(),pins=pins,copiedBytes=bytes_written,astProof=proof,contextControls=controls(),startedUtc=started,finishedUtc=now(),elapsedSeconds=time.perf_counter()-begin,registrySha256=sha256(root/'recovery.json'),preferencesSha256=sha256(root/'source-preferences.json'),interpretedRegistrySha256=sha256(root/'interpreted-recovery.json'),noCompiledExecutablesOrOriginalNativeInputsCopied=True,relocationCaveat='Both collectors execute the complete real captured source corpus under the same private relocated ROOT. Original absolute repository references remain unchanged and are treated by the original scope rules; returned closure may differ from original live-root capture. This is not a clean-ROM or live-source acceptance proof.')
    write_json(metadata/'snapshot.json',snapshot);state.update(status='immutable-source-snapshot-ready',copiedFiles=len(pins),bytesCopied=bytes_written,finishedUtc=now());write_json(metadata/'state.json',state);write_json(LANE/'real-epoch-snapshot.json',dict(sourceCredit=0,metadata=metadata.relative_to(ROOT).as_posix(),snapshotSha256=sha256(metadata/'snapshot.json'),root=root.relative_to(ROOT).as_posix(),copiedFiles=len(pins),copiedBytes=bytes_written));print(dict(snapshotReady=True,metadata=metadata.relative_to(ROOT).as_posix(),copiedFiles=len(pins),copiedBytes=bytes_written),flush=True)
    return metadata


def verify_snapshot(metadata):
    data=read_json(metadata/'snapshot.json');root=ROOT/data['root'];expected={p['path']:p['sha256'] for p in data['pins']};actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if actual!=set(expected):raise ValueError('Immutable captured source directory epoch changed')
    for name,digest in expected.items():
        if sha256(root/name)!=digest:raise ValueError('Immutable captured source content changed: '+name)
    return data


def run(metadata,label):
    if label not in ['legacy','v2']:raise ValueError('Unknown compared collector')
    metadata=metadata.resolve()
    if not metadata.is_relative_to(WORK.resolve()):raise ValueError('Real comparator metadata path is not owned')
    snapshot=verify_snapshot(metadata);root=ROOT/snapshot['root'];launcher=metadata/'launch.py'
    launcher.write_text("import sys,time,json\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nfrom project import write_json,sha256\nmodule=__import__('oracle_source_closure_20261031' if sys.argv[2]=='legacy' else 'oracle_source_closure_v2_20261106')\nstart=time.perf_counter()\nresult=module.collect()\nelapsed=time.perf_counter()-start\nwrite_json(Path(sys.argv[3]),result)\nwrite_json(Path(sys.argv[4]),dict(collector=sys.argv[2],elapsedSeconds=elapsed,discoveredPaths=len(result['sourceAndEvidenceHashes']),missingRequiredPaths=result['missingRequiredPaths'],outputSha256=sha256(sys.argv[3]),collectorSha256=sha256(module.__file__)))\n",encoding='utf-8');log=metadata/(label+'.log');output=metadata/(label+'-closure.json');timing=metadata/(label+'-timing.json');command=[sys.executable,str(launcher),str(root),label,str(output),str(timing)];started=now();write_json(metadata/'state.json',dict(status='comparing-real-epoch-'+label,sourceCredit=0,command=command,startedUtc=started))
    with log.open('w',encoding='utf-8') as stream:result=subprocess.run(command,cwd=root,stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if result.returncode:raise ValueError('Complete real-epoch collector failed: '+label)
    verify_snapshot(metadata);data=read_json(output)
    if data['missingRequiredPaths'] or data['registrySha256']!=snapshot['registrySha256']:raise ValueError('Real-epoch closure failed original required/source registry checks')
    expected={p['path']:p['sha256'] for p in snapshot['pins']}
    for name,digest in data['sourceAndEvidenceHashes'].items():
        if name not in expected or expected[name]!=digest:raise ValueError('Returned real closure contains unknown/changed source')
    print(dict(label=label,passed=True,timing=read_json(timing),log=log.relative_to(ROOT).as_posix()),flush=True)


def compare(metadata):
    snapshot=verify_snapshot(metadata);a=read_json(metadata/'legacy-closure.json');b=read_json(metadata/'v2-closure.json')
    if a!=b:raise ValueError('Complete original and new real-epoch closure outputs differ')
    old=read_json(metadata/'legacy-timing.json');new=read_json(metadata/'v2-timing.json');receipt=dict(passed=True,sourceCredit=0,completeRealCapturedEpochOutputEquality=True,sourceCommit=REVISION,snapshot=dict(path=(metadata/'snapshot.json').relative_to(ROOT).as_posix(),sha256=sha256(metadata/'snapshot.json'),files=len(snapshot['pins']),bytes=snapshot['copiedBytes']),original=old,candidate=new,observedRealEpochSpeedRatio=old['elapsedSeconds']/new['elapsedSeconds'],registrySha256=snapshot['registrySha256'],sourcePreferencesSha256=snapshot['preferencesSha256'],interpretedRegistrySha256=snapshot['interpretedRegistrySha256'],astProof=snapshot['astProof'],contextControls=snapshot['contextControls'],allCapturedSourceAndDirectoryHashesUnchanged=True,noLiveStagesSwitched=True,noCompilerOrOriginalROMBuildExecuted=True,generatorSha256=sha256(__file__),relocationCaveat=snapshot['relocationCaveat'],limits=['Complete collector output equivalence on one immutable real captured source epoch; this does not prove full ROM reconstruction, current source acceptance, unrestricted filesystem caching or all future epochs.','Only pure lexical context is memoized. All original filesystem resolution/hash/required/static-json/import/include/skip behavior is retained. Existing live/frozen collector/stagers and active jobs were untouched.']);write_json(LANE/'full-real-epoch-equivalence.json',receipt);print(dict(passed=True,paths=len(a['sourceAndEvidenceHashes']),originalSeconds=old['elapsedSeconds'],candidateSeconds=new['elapsedSeconds'],observedRealEpochSpeedRatio=receipt['observedRealEpochSpeedRatio'],receiptSha256=sha256(LANE/'full-real-epoch-equivalence.json')),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['materialize','legacy','v2','compare','all']);parser.add_argument('--metadata');args=parser.parse_args();metadata=ROOT/args.metadata if args.metadata else None
    if args.action in ['materialize','all']:metadata=materialize()
    if args.action in ['legacy','v2']:run(metadata,args.action)
    if args.action=='compare':compare(metadata)
    if args.action=='all':run(metadata,'legacy');run(metadata,'v2');compare(metadata)
