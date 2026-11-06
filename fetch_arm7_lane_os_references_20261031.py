import hashlib
import json
import urllib.request
from project import ROOT,sha256,write_json

COMMIT='b623abef1b4dfe204ca50aab42447ac00c134290'


def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'private-local-source-reference-audit','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(request,timeout=30) as response:
        return response.read()


def main():
    tree=json.loads(get('https://api.github.com/repos/pret/pokediamond/git/trees/'+COMMIT+'?recursive=1'))
    if tree.get('truncated'):
        raise ValueError('Pinned public SDK reference tree was truncated')
    rows=[row for row in tree['tree'] if row['type']=='blob' and (
        row['path'].startswith('arm7/lib/src/OS_') and row['path'].endswith('.c')
        or row['path'].startswith('arm7/lib/include/OS_') and row['path'].endswith('.h')
        or row['path'].startswith('include/nitro/OS_') and row['path'].endswith('.h'))]
    files=[]
    for row in rows:
        path=row['path']
        raw=get('https://raw.githubusercontent.com/pret/pokediamond/'+COMMIT+'/'+path)
        git=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if git!=row['sha'] or len(raw)!=row['size']:
            raise ValueError('Public OS reference failed independent Git/length validation: '+path)
        destination=ROOT/'deps/references/pokediamond-b623abef-lane-os-20261031'/path
        if destination.exists() and destination.read_bytes()!=raw:
            raise ValueError('Refusing to overwrite changed OS reference bytes')
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(raw)
        files.append(dict(upstreamPath=path,url='https://github.com/pret/pokediamond/blob/'+COMMIT+'/'+path,
            gitBlobSha1=git,localPath=destination.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha256(destination)))
    report=ROOT/'evidence/research/20261031-arm7-lane-os-reference-source.json'
    write_json(report,dict(generator='fetch_arm7_lane_os_references_20261031.py',generatorSha256=sha256(__file__),
        repository='https://github.com/pret/pokediamond',commit=COMMIT,accessDate='2026-10-31',files=files,
        referenceOnly=True,compilerInput=False,sourceCredit=0,originalAssemblyJustification=False,
        limitation='Unmodified public credential-free references only; ordinary C must be adapted and independently compiled/linked/native-validated. No historical assembly or byte credit follows from these files.'))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),files=len(files),
        cSources=[row['upstreamPath'] for row in files if row['upstreamPath'].endswith('.c')]))


if __name__=='__main__':
    main()
