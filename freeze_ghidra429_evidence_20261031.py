import gzip
import hashlib
import json
from project import ROOT,write_json,sha256

def run():
    directory=ROOT/'build/ghidra429/generated';rows=[]
    for path in sorted(directory.rglob('*')):
        if path.is_file():rows.append(dict(path=path.relative_to(directory).as_posix(),bytes=path.stat().st_size,sha256=sha256(path),utf8=path.read_text(encoding='utf-8')))
    payload=json.dumps(dict(schemaVersion=1,generatedScaffolding=True,sourceCredit=0,files=rows),indent=2,ensure_ascii=False).encode('utf-8');archive=ROOT/'evidence/generated/ghidra429-independent-exports-20261031.json.gz';archive.parent.mkdir(parents=True,exist_ok=True);archive.write_bytes(gzip.compress(payload,compresslevel=9,mtime=0))
    write_json(ROOT/'evidence/verification/ghidra429-export-archive-20261031.json',dict(schemaVersion=1,sourceCredit=0,archive=archive.relative_to(ROOT).as_posix(),archiveSha256=sha256(archive),archiveBytes=archive.stat().st_size,decodedSha256=hashlib.sha256(payload).hexdigest(),decodedBytes=len(payload),generatedFiles=[{k:v for k,v in r.items()if k!='utf8'}for r in rows],generatorSha256=sha256(__file__),reproductionCommand='python freeze_ghidra429_evidence_20261031.py',limits=['Generated C, inferred symbols and high p-code are retained as unaccepted frontend hypotheses','Deterministic JSON encoding andgzip timestamp do not turn generated output into source-match credit']))
    print(json.dumps(dict(generatedFiles=len(rows),archiveBytes=archive.stat().st_size,sha256=sha256(archive))))

if __name__=='__main__':run()
