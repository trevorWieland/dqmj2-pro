import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True


def sha(raw):return hashlib.sha256(raw).hexdigest()


def run(job):
 folder=ROOT/job['work'];folder.mkdir(parents=True,exist_ok=True);path=folder/'job.json';path.write_text(json.dumps(job,indent=2)+'\n')
 command=[sys.executable,'-I','-S',str(ROOT/'evidence/application/save_core_breadth409_worker_20261102.py'),str(path)]
 try:
  p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=240,creationflags=subprocess.CREATE_NO_WINDOW);(folder/'driver-stdout.txt').write_text(p.stdout);(folder/'driver-stderr.txt').write_text(p.stderr)
  if p.returncode:result=dict(job,driverFailure=dict(exitCode=p.returncode,stderr=p.stderr),drafted=False,compilable=False,byteExactCandidate=False)
  else:result=json.loads((folder/'result.json').read_text())
 except subprocess.TimeoutExpired:result=dict(job,driverFailure='240-second isolated worker bound',drafted=False,compilable=False,byteExactCandidate=False)
 print(json.dumps(dict(address=job['address'],drafted=result.get('drafted',False),compiled=result.get('compilable',False),exact=result.get('byteExactCandidate',False))),flush=True);return result


def main():
 queue=json.loads((ROOT/'evidence/lanes/save-core/breadth409-queue-20261102.json').read_text());jobs=queue['jobs'];assert len(jobs)==3
 snapshot=queue['freshExclusionSnapshot'];assert sha((ROOT/snapshot['path']).read_bytes())==snapshot['sha256'];claims=[r for r in json.loads((ROOT/snapshot['path']).read_text())['functions'] if r['processor']=='arm9' and r.get('program','')=='' and r['module']=='main']
 for x in jobs:
  start=int(x['address'],0);assert not[r for r in claims if start<r['address']+int(r.get('bytes') or 1) and r['address']<start+x['bytes']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,jobs))
 raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-breadth409-20261102.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,selectedFunctions=len(jobs),selectedNativeBytes=sum(x['bytes'] for x in jobs),drafted=sum(bool(x.get('drafted')) for x in rows),compiled=sum(bool(x.get('compilable')) for x in rows),near=sum(bool(x.get('nearCandidate')) for x in rows),exactCandidates=sum(bool(x.get('byteExactCandidate')) for x in rows),genuineLinkedProfiles=sum(bool(p.get('realLinkSucceeded')) for x in rows for p in x.get('compileAttempts',[])),actualNativeReturns=0,fullProvenanceSidecar=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),contentSha256=sha(raw)),queueSha256=sha((ROOT/'evidence/lanes/save-core/breadth409-queue-20261102.json').read_bytes()),workerSha256=sha((ROOT/'evidence/application/save_core_breadth409_worker_20261102.py').read_bytes()),generatorSha256=sha(Path(__file__).read_bytes()),limits=queue['limits']+['At most three isolated compiler subprocess workers,each with separate function work/generated/output paths. Default/speed compiler candidates remain hypotheses,not settings established for these units.','Source current views,typed helper declarations and measured binary64 lowering apply only to fresh hypotheses;no accepted source/catalogue is changed. No draft,compile,link or proximity score constitutes decompilation acceptance.'])
 path=ROOT/'evidence/lanes/save-core/breadth409-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))


if __name__=='__main__':main()
