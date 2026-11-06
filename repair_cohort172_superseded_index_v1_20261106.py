import gzip
import subprocess
from project import ROOT,read_json,write_json,sha256,now


def main():
    failed=read_json(ROOT/'evidence/verification/cohort172-continuation-driver-v44-20261105.json')
    assert failed['state']=='failed' and len(failed['steps'])==5 and failed['steps'][-1]['exitCode']==1
    for step in failed['steps']:assert sha256(ROOT/step['log'])==step['logSha256']
    prefix='src/runtime/parallel_wave20261106/gp-core-resume-next/first/'
    expected={prefix+a+'/'+f for a in ['020aa9b4','020aced4','020acf00']for f in ['context.h','match.c','string.h']}
    staged=set(subprocess.check_output(['git','diff','--cached','--name-only','--',prefix],cwd=ROOT,text=True).splitlines())
    assert staged==expected
    package=read_json(ROOT/'cohort172-parallel-wave20261105-q-package.json')
    declared=set(package['extra'])|set(package.get('traces',[]))
    for name in package['manifests']:declared.update(r['path']for r in read_json(ROOT/name)['files'])
    closure=read_json(ROOT/'evidence/verification/cohort172-captured-oracle-closure-20261031.json')['sourceAndEvidenceHashes']
    registered={p for batch in read_json(ROOT/'recovery.json')['batches']for p in batch.get('sourceHashes',{})}
    assert not staged&(declared|set(closure)|registered)
    for name in staged:assert subprocess.run(['git','cat-file','-e','HEAD:'+name],cwd=ROOT,capture_output=True).returncode!=0
    before={name:sha256(ROOT/name)for name in ['recovery.json','source-preferences.json','ledger/functions.jsonl',*sorted(staged)]}
    folder=ROOT/'evidence/attempts/cohort172-superseded-unselected-gp-source-20261106';assert not folder.exists();folder.mkdir()
    rows=[]
    for number,name in enumerate([*sorted(staged),'logs/integration/cohort172-stage-20261101.txt','evidence/verification/cohort172-captured-oracle-closure-20261031.json']):
        path=ROOT/name;target=folder/(str(number)+'.gz');target.write_bytes(gzip.compress(path.read_bytes(),mtime=0));assert gzip.decompress(target.read_bytes())==path.read_bytes()
        rows.append(dict(originalPath=name,originalSha256=sha256(path),archive=target.relative_to(ROOT).as_posix(),archiveSha256=sha256(target)))
    manifest=folder/'manifest.json';write_json(manifest,dict(sourceCredit=0,reason='Unselected superseded candidate files were stale staged additions; no current packet manifest, registered source or captured oracle requires them',files=rows))
    subprocess.run(['git','restore','--staged','--source=HEAD','--',*sorted(staged)],cwd=ROOT,check=True)
    assert before=={name:sha256(ROOT/name)for name in before}
    assert not subprocess.check_output(['git','diff','--cached','--name-only','--',prefix],cwd=ROOT,text=True).strip()
    receipt='evidence/verification/cohort172-superseded-index-repair-v1-20261106.json'
    write_json(ROOT/receipt,dict(passed=True,sourceCredit=0,createdUtc=now(),unstagedOnly=sorted(staged),workingFilesUnchanged=True,acceptedRegistryPreferencesLedgerUnchanged=True,notDeclaredRegisteredOrCaptured=True,archive=manifest.relative_to(ROOT).as_posix(),archiveSha256=sha256(manifest),originalGuardUnchanged=True,generatorSha256=sha256(__file__)))
    extras=[receipt,'repair_cohort172_superseded_index_v1_20261106.py',manifest.relative_to(ROOT).as_posix(),*[r['archive']for r in rows]]
    for config in ['provenance/parallel-wave20261105-q-packets.json','cohort172-parallel-wave20261105-q-package.json']:
        path=ROOT/config;document=read_json(path)
        for name in extras:
            if name not in document['extra']:document['extra'].append(name)
        write_json(path,document)
    print(dict(passed=True,unstagedSupersededFiles=9,workingFilesChanged=0,sourceCredit=0,originalGuardsUnchanged=True))


if __name__=='__main__':main()
