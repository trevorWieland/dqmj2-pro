import concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module
SNAPSHOT='evidence/verification/accepted-cohort99-identities-v2-20261101.json'
REPORT='evidence/lanes/save-core/near-refresh121-20261101.json'
WORK=ROOT/'work/save-core-lane/20261101-near-refresh121'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def number(v):return int(v,0) if isinstance(v,str) else v


def prepare():
    old=json.loads((ROOT/'evidence/lanes/save-core/historical-near-census108-20261101.json').read_text());snapshot=json.loads((ROOT/SNAPSHOT).read_text());blocked=[(number(r['address']),number(r.get('bytes',0) or 0)) for r in snapshot['functions'] if r['processor']=='arm9' and r['module']=='main'];blocked.extend([(0x20444EC,28),(0x20633C8,100),(0x20C5E88,192)])
    for path in (ROOT/'evidence/matches').glob('mechanics-save-20261101-lane-*.json'):
        d=json.loads(path.read_text())
        blocked.extend((number(r['address']),number(r['bytes'])) for r in d.get('matches',[]) if r.get('module')=='main')
    best={}
    for r in old['candidates']:
        a,n=number(r['address']),r['bytes'];origin=Path(r['sourceOriginRoot'])/r['source']
        if not 0x2040000<=a<a+n<=0x20D0000 or n<128 or any(a<b+m and b<a+n for b,m in blocked):continue
        if not origin.exists() or sha(origin.read_bytes())!=r['sourceSha256']:continue
        key=(a,r['mode'])
        if key not in best or r['historicalRatio']>best[key]['historicalRatio']:best[key]=r
    chosen=sorted(best.values(),key=lambda r:(-r['bytes'],-r['historicalRatio']))[:32];jobs=[];meta,arm,config=measured_module('main')
    for r in chosen:
        a,n=number(r['address']),r['bytes'];aliases=[line.split()[0] for line in config.splitlines() if line.startswith('func_') and f'addr:0x{a:08x}' in line and f'kind:function({r["mode"]},size=0x{n:x})' in line];assert len(aliases)==1,(a,aliases);work=f'work/save-core-lane/20261101-near-refresh121/{a:08x}';(ROOT/work).mkdir(parents=True,exist_ok=True);jobs.append(dict(module='main',processor='arm9',program='',mode=r['mode'],address=hex(a),bytes=n,alias=aliases[0],nativeSpanSha256=sha(arm[a-0x2000000:a-0x2000000+n]),work=work,originDraft=r['source'],originSourceRoot=r['sourceOriginRoot'],originSourceSha256=r['sourceSha256'],compilerPath=r['compilerPath'],compilerSha256=r['compilerSha256'],flags=r['flags'],historicalRatio=r['historicalRatio'],newAddressNamedDraftAttempt=False,refinesPriorDecompilerAttempt=True))
    return dict(jobs=jobs,selectedNativeBytes=sum(j['bytes'] for j in jobs),acceptedSnapshot=SNAPSHOT,acceptedSnapshotSha256=sha((ROOT/SNAPSHOT).read_bytes()),historicalCensusSha256=sha((ROOT/'evidence/lanes/save-core/historical-near-census108-20261101.json').read_bytes()))


def run(job):
    folder=ROOT/job['work'];path=folder/'job.json';path.write_text(json.dumps(job,indent=2)+'\n');process=subprocess.run([sys.executable,str(ROOT/'evidence/application/save_core_near_refresh121_worker_20261101.py'),str(path)],cwd=ROOT,capture_output=True,text=True,timeout=180);(folder/'worker-output.txt').write_text(process.stdout);(folder/'worker-errors.txt').write_text(process.stderr);target=folder/'result.json'
    if process.returncode or not target.exists():return dict(job,workerFailure=process.stderr[-1800:],exitCode=process.returncode,sourceCredit=0)
    return json.loads(target.read_text())


def save(queue,rows):
    counts=dict(selected=len(queue['jobs']),selectedNativeBytes=queue['selectedNativeBytes'],completed=len(rows),drafted=sum(bool(r.get('drafted')) for r in rows),compiled=sum(bool(r.get('compilable')) for r in rows),realLinked=sum(bool(r.get('realLinked')) for r in rows),near=sum(bool(r.get('nearCandidate')) for r in rows),byteExactCandidates=sum(bool(r.get('byteExactCandidate')) for r in rows),nativeSemanticValidated=0,acceptedSourceCredit=0);out=dict(schemaVersion=1,complete=len(rows)==len(queue['jobs']),queue=queue,counts=counts,functions=sorted(rows,key=lambda r:number(r['address'])),generatorSha256=sha(Path(__file__).read_bytes()),replay='python refresh_save_core_near121_20261101.py',limitations=['Two isolated workers refresh32 historical identities with qualified/frozen-source input hypotheses andmixed inferred scalar/address-only globals,never blind width rewrites. Originalhistoricalsource and accepted/pendingintervals remain unchanged.','Each unit reproduces its actual historical compilerPath/hash/flags;source byte identity/ordinary-C draft,compilation,genuine linker proximity,native proof andaccepted coverage remain separate. No duplicate/new-source credit follows fromre-drafting oldhypotheses.','Prior buffer extent/escape/stack-arity,untranslated macros,return/input/field widths remain unresolved until independently qualified. No forcedregisters,opcodepatches,assembly,unproved argument invention orsharedregistry edits.']);(ROOT/REPORT).write_text(json.dumps(out,indent=2)+'\n');print(counts,flush=True)


def main():
    queue=prepare();rows=[];save(queue,rows)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for future in concurrent.futures.as_completed([pool.submit(run,j) for j in queue['jobs']]):rows.append(future.result());save(queue,rows)


if __name__=='__main__':main()
