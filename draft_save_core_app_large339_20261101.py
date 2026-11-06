import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module
import census_compile_save_core_near140_20261101 as C

REPORT = ROOT / 'evidence/lanes/save-core/app-large339-20261101.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare():
    C.SNAPSHOT='evidence/verification/accepted-cohort130-identities-v2-20261101.json'
    ranges,receipts=C.exclusions()
    jobs=[]
    for tag in ('314','315','316'):
        old=json.loads((ROOT/f'evidence/lanes/save-core/app-large{tag}-20261101.json').read_text())
        archive=old['fullProvenanceSidecar'];rows=json.loads(gzip.decompress((ROOT/archive['path']).read_bytes()))
        for row in rows:
            address=int(row['address'],0)
            if any(address<end and start<address+row['bytes'] for start,end in ranges):continue
            job=dict(old['queue']['jobs'][next(i for i,r in enumerate(old['queue']['jobs']) if int(r['address'],0)==address)])
            job.update(work=f'work/save-core/app-large339/{address:08x}',source=None,originDraft=row.get('source') or row.get('originDraft'),reusedDraft=False,newAddressNamedDraftAttempt=False)
            if address==0x020BB878:job['originDraft']='nonmatching/save-core/20261101-app-large323/native_main_020bb878.c'
            (ROOT/job['work']).mkdir(parents=True,exist_ok=True);jobs.append(job)
    assert len(jobs)==len({row['address'] for row in jobs}) and 1<=len(jobs)<=38
    return dict(schema=1,exclusions=receipts,jobs=jobs,selectedFunctions=len(jobs),selectedNativeBytes=sum(row['bytes'] for row in jobs),sourceCredit=0,pilot='Same earlier38 identities,refreshed current selected-source arity hypotheses;reuse only,no new-address discovery or source credit')


def run(job):
    folder = ROOT / job['work']
    path = folder / 'job.json'
    path.write_text(json.dumps(job, indent=2) + '\n')
    producer = ROOT / 'evidence/application/save_core_app_large339_worker_20261101.py'
    process = subprocess.run([sys.executable, str(producer), str(path)], cwd=ROOT, capture_output=True,
                             text=True, timeout=300, creationflags=subprocess.CREATE_NO_WINDOW)
    (folder / 'worker-stdout.txt').write_text(process.stdout)
    (folder / 'worker-stderr.txt').write_text(process.stderr)
    result = folder / 'result.json'
    if process.returncode or not result.exists():
        return dict(job, workerFailure=process.stderr[-2500:], exitCode=process.returncode, sourceCredit=0)
    return json.loads(result.read_text())


def save(queue, rows):
    counts = dict(selected=queue['selectedFunctions'], selectedNativeBytes=queue['selectedNativeBytes'],
        completed=len(rows), newAddressAttempts=sum(row['newAddressNamedDraftAttempt'] for row in queue['jobs']),
        drafted=sum(bool(row.get('drafted')) for row in rows),
        refinedExistingDrafts=sum(bool(row.get('refinedDraftThisSweep')) for row in rows),
        compiled=sum(bool(row.get('compilable')) for row in rows),
        realLinked=sum(bool(row.get('realLinked')) for row in rows),
        near=sum(bool(row.get('nearCandidate')) for row in rows),
        exactByteCandidates=sum(bool(row.get('byteExactCandidate')) for row in rows),
        nativeSemanticallyQualified=0, acceptedSourceBytes=0)
    raw = (json.dumps(sorted(rows, key=lambda row: int(row['address'], 0)), indent=2) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    sidecar = ROOT / 'evidence/vectors/save-core-app-large339-provenance-20261101.json.gz'
    sidecar.write_bytes(packed)
    REPORT.write_text(json.dumps(dict(schema=1, complete=len(rows) == len(queue['jobs']), queue=queue,
        counts=counts, compilerWorkers=2, fullProvenanceSidecar=dict(path=sidecar.relative_to(ROOT).as_posix(),
            sha256=sha(packed), compressedBytes=len(packed), uncompressedSha256=sha(raw),
            uncompressedBytes=len(raw), contexts=len(rows)),
        generatorSha256=sha(Path(__file__).read_bytes()), limitations=[
            'Primary ARM9 main600..4000-byte application-anchor and save/mechanics-prioritized hypotheses with optional immediate mixed-width field hypotheses are selected after accepted128,pending108+,own canonical and overlay-exception exclusions. Existing draft source hashes are recorded; this is not complete backlog coverage.',
            'Single-basic-block field hints with no dynamic access,negative fields,unaligned fields or overlaps are experimental views,not original declarations orfull cross-block alias analysis. Fresh m2c contexts retain source-hash-qualified input hypotheses and inferred scalar/pointer globals. Those are hypotheses,not original ABI/type truth;missing macros,stack arguments and unsupported value uses remain failures.',
            'Two isolated workers use separate module/address outputs and at most two compiler profiles per function. Prior source and registered inputs remain unchanged.',
            'Variadic context can expose single-byte formatting destinations and stale extra words;scalarFormattingBufferReview remains unresolved source extent evidence. Drafted,compilable,linked,near,byte-exact,semantically qualified and accepted source remain separate. Every result here has zero accepted source credit.']), indent=2) + '\n')
    print(json.dumps(counts), flush=True)


def main():
    queue, rows = prepare(), []
    save(queue, rows)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, job) for job in queue['jobs']]
        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())
            save(queue, rows)


if __name__ == '__main__':
    main()
