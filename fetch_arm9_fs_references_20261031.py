import hashlib
import json
from project import ROOT,sha256,write_json
from fetch_arm7_lane_os_references_20261031 import get

REPOSITORY='nitro-decomp/nitro'
COMMIT='10e447b8b7cf9dca488ef5d6af51d9ed5bef1aeb'


def main():
    tree=json.loads(get('https://api.github.com/repos/'+REPOSITORY+'/git/trees/'+COMMIT+'?recursive=1'));assert not tree.get('truncated')
    rows=[row for row in tree['tree'] if row['type']=='blob' and (row['path'].startswith(('src/fs/','include/nitro/fs/')) or row['path'].upper() in ['LICENSE','LICENSE.MD','COPYING','COPYING.TXT'])]
    assert rows and any(row['path'].upper().startswith(('LICENSE','COPYING')) for row in rows)
    files=[]
    for row in rows:
        raw=get('https://raw.githubusercontent.com/'+REPOSITORY+'/'+COMMIT+'/'+row['path']);blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert blob==row['sha'] and len(raw)==row['size']
        path=ROOT/'deps/reference/nitro-10e447b8'/row['path']
        if path.exists():assert path.read_bytes()==raw
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        files.append(dict(upstreamPath=row['path'],localPath=path.relative_to(ROOT).as_posix(),url='https://github.com/'+REPOSITORY+'/blob/'+COMMIT+'/'+row['path'],gitBlobSha1=blob,bytes=len(raw),sha256=sha256(path)))
    report=dict(generator='fetch_arm9_fs_references_20261031.py',generatorSha256=sha256(__file__),repository='https://github.com/'+REPOSITORY,commit=COMMIT,accessDate='2026-10-31',referenceOnly=True,compilerInput=False,sourceCredit=0,originalAssemblyJustification=False,files=files,limitations=['Pinned external C/headers are hypotheses for the measured build, not reconstructed J2P source','No pokediamond or other reference is assigned this repository license','Per-unit boundaries, compiler settings, source semantics, genuine linking and native regressions remain required'])
    write_json(ROOT/'evidence/research/20261031-arm9-fs-reference-source.json',report);print(dict(files=len(files),bytes=sum(row['bytes'] for row in files),sourceCredit=0))


if __name__=='__main__':main()
