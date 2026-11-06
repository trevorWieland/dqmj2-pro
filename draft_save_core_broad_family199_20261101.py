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

REPORT = ROOT / 'evidence/lanes/save-core/broad-family199-20261101.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare():
    C.SNAPSHOT='evidence/integration/root-accepted114-identities-v2-20261101.json'
    ranges, receipts = C.exclusions()
    metadata, binary, config = measured_module('main')
    paths = subprocess.check_output(['rg', '--files', 'src', 'nonmatching'], cwd=ROOT, text=True).splitlines()
    sources = {}
    for path in paths:
        match = re.search(r'(?:native_main_|func_)([0-9a-f]{8})', Path(path).name)
        if match and Path(path).suffix in ('.c', '.cpp'):
            sources.setdefault(int(match[1], 16), []).append(path.replace('\\', '/'))
    jobs = []
    for name, mode, n, raw in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', config, re.M):
        address, length = int(raw, 0), int(n, 0)
        if not 0x02040000 <= address < 0x020D0000 or mode != 'arm' or not 400 <= length <= 5000:
            continue
        if any(address < end and start < address + length for start, end in ranges):
            continue
        code=binary[address-0x02000000:address-0x02000000+length]
        call_offsets=[]
        for offset in range(0,len(code)-3,4):
            word=int.from_bytes(code[offset:offset+4],'little')
            if word>>24==0xEB:
                delta=word&0xFFFFFF
                if delta&0x800000:delta-=1<<24
                if address+offset+8+delta*4==0x0201D444:call_offsets.append(offset)
        folder = ROOT / f'work/save-core/broad-family199/{address:08x}'
        folder.mkdir(parents=True, exist_ok=True)
        origins = sorted(sources.get(address, []), key=lambda p: (not p.startswith('nonmatching/save-core/'), len(p)))
        origin = origins[0] if origins else None
        if origin is not None:
            continue
        jobs.append(dict(formatterCallOffsets=call_offsets,module='main', processor='arm9', program='', mode=mode, address=hex(address),
            bytes=length, alias=name, nativeSpanSha256=sha(binary[address - 0x02000000:address - 0x02000000 + length]),
            nativeModuleSha256=metadata['sha256'], work=folder.relative_to(ROOT).as_posix(), source=None,
            originDraft=origin, reusedDraft=False, sourceOriginSha256=sha((ROOT / origin).read_bytes()) if origin else None,
            newAddressNamedDraftAttempt=not bool(origins), boundaryConfidence='Measured configured extent; ABI/code-data/semantic qualification remains separate'))
    jobs.sort(key=lambda row: (int(row['address'],0)!=0x020C61A4,not row['newAddressNamedDraftAttempt'], -row['bytes'], int(row['address'], 0)))
    jobs = jobs[:40]
    assert 20 <= len(jobs) <= 40
    return dict(schema=1, exclusions=receipts, jobs=jobs,
                selectedFunctions=len(jobs), selectedNativeBytes=sum(row['bytes'] for row in jobs), sourceCredit=0)


def run(job):
    folder = ROOT / job['work']
    path = folder / 'job.json'
    path.write_text(json.dumps(job, indent=2) + '\n')
    producer = ROOT / 'evidence/application/save_core_broad_family199_worker_20261101.py'
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
    sidecar = ROOT / 'evidence/vectors/save-core-broad-family199-provenance-20261101.json.gz'
    sidecar.write_bytes(packed)
    REPORT.write_text(json.dumps(dict(schema=1, complete=len(rows) == len(queue['jobs']), queue=queue,
        counts=counts, compilerWorkers=3, fullProvenanceSidecar=dict(path=sidecar.relative_to(ROOT).as_posix(),
            sha256=sha(packed), compressedBytes=len(packed), uncompressedSha256=sha(raw),
            uncompressedBytes=len(raw), contexts=len(rows)),
        generatorSha256=sha(Path(__file__).read_bytes()), limitations=[
            'Primary ARM9 configured main functions400..5000 bytes with no address-named prior C are selected after accepted114,pending108+,own canonical and overlay-exception exclusions. Differently named prior source absence is not asserted; this is not complete backlog coverage.',
            'Fresh m2c contexts retain source-hash-qualified input hypotheses and inferred scalar/pointer globals. Those are hypotheses,not original ABI/type truth;missing macros,stack arguments and unsupported value uses remain failures.',
            'Three isolated workers use separate module/address outputs and at most two compiler profiles per function. Prior source and registered inputs remain unchanged.',
            'Variadic context can expose single-byte formatting destinations and stale extra words;scalarFormattingBufferReview remains unresolved source extent evidence. Drafted,compilable,linked,near,byte-exact,semantically qualified and accepted source remain separate. Every result here has zero accepted source credit.']), indent=2) + '\n')
    print(json.dumps(counts), flush=True)


def main():
    queue, rows = prepare(), []
    save(queue, rows)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run, job) for job in queue['jobs']]
        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())
            save(queue, rows)


if __name__ == '__main__':
    main()
