import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native'), str(ROOT / 'evidence/application')]
from link_runtime_unit import measured_module


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare():
    rows = json.loads(gzip.decompress((ROOT / 'evidence/vectors/save-core-mechanics148-provenance-20261101.json.gz').read_bytes()))
    selected = [0x0206E73C, 0x02070FD8, 0x020743F8, 0x02076DEC, 0x0207726C]
    jobs = []
    for row in rows:
        address = int(row['address'], 0)
        if address not in selected:
            continue
        original = ROOT / row['source']
        text = original.read_text()
        repairs = []
        if address == 0x0206E73C:
            text = text.replace('temp_r7 = *temp_r4_2;', 'temp_r7 = *(void **)temp_r4_2;')
            text = text.replace('    s16 sp10;', '    u16 sp10[32];').replace('    s16 spC;', '    s16 spC[2];')
            text = text.replace('&spC', 'spC').replace('&sp10', 'sp10')
            repairs.append('Native6E778 loads full pointer word through raw61DCC holder;native stackC/E signed-short pair and10..4F text backing are explicit')
        elif address == 0x02070FD8:
            text = text.replace('*(temp_r7 + var_r5)', '*(u8 *)(temp_r7 + var_r5)')
            repairs.append('Native71104 LDRB requires byte view of descriptor threshold pointer')
        elif address == 0x020743F8:
            text = text.replace('*temp_r4 =', '*(u16 *)temp_r4 =')
            text = text.replace('*(native_data_021c5df8', '*(u32 *)(native_data_021c5df8')
            text = text.replace('*(native_data_020dbc18', '*(u16 *)(native_data_020dbc18')
            repairs.append('Native74508 word table load and74538 halfword lookup,followed by measured halfword destination store;byte offsets retained')
        elif address == 0x02076DEC:
            text = text.replace('*(native_data_021c64d0', '*(u32 *)(native_data_021c64d0')
            text = text.replace('*(sp14 +', '*(u8 *)(sp14 +').replace('*(sp18 +', '*(u8 *)(sp18 +')
            repairs.append('Native76E3C pointer-word table,76E70/7716C descriptor byte loads,and77180 low-byte record read with stride2')
        elif address == 0x0207726C:
            text = text.replace('*(native_data_021c64d0', '*(u32 *)(native_data_021c64d0')
            text = text.replace('*(temp_r10 +', '*(u8 *)(temp_r10 +')
            repairs.append('Native7324/73A8/7400/748C/7580/7608/7798/77B0 table pointer-word loads;7738 descriptor byte load')
        assert text != original.read_text() and len(text.splitlines()) <= 500
        path = ROOT / 'nonmatching/save-core/20261101-mechanics-pointer149' / original.name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        jobs.append(dict(address=address, bytes=row['bytes'], source=path.relative_to(ROOT).as_posix(),
            origin=original.relative_to(ROOT).as_posix(), originSha256=sha(original.read_bytes()),
            sourceSha256=sha(path.read_bytes()), repairs=repairs))
    assert len(jobs) == 5
    return jobs


def worker(job):
    spec = importlib.util.spec_from_file_location('mechanics_pointer149_builder', ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.MODE = job['address'], job['bytes'], 'arm'
    builder.MODULE, builder.NAME = 'main', 'native_main_' + f"{job['address']:08x}"
    builder.SOURCE, builder.WORK = job['source'], 'work/save-core/mechanics-pointer149/' + f"{job['address']:08x}"
    arm = measured_module('main')[1]
    native = arm[job['address'] - 0x02000000:job['address'] - 0x02000000 + job['bytes']]
    try:
        row, body = builder.build(native)
        return dict(job, compileSucceeded=True, realLinkCompared=True, candidate=row,
            byteExact=row['exactByteEqual'], sourceCreditAdded=0)
    except Exception as error:
        return dict(job, compileSucceeded=False, errorType=type(error).__name__, error=str(error),
            compilerProcess=builder.LAST_COMPILE, sourceCreditAdded=0)


def main():
    jobs = prepare()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(worker, jobs))
    payload = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    sidecar = 'evidence/vectors/save-core-mechanics-pointer149-20261101.json.gz'
    packed = gzip.compress(payload, mtime=0)
    (ROOT / sidecar).write_bytes(packed)
    report = dict(schema=1, draftedFunctions=len(rows), draftedNativeBytes=sum(r['bytes'] for r in rows),
        compileSucceeded=sum(r['compileSucceeded'] for r in rows),
        byteExactCandidates=sum(r.get('byteExact', False) for r in rows), qualifiedSourceBytes=0,
        vectorSidecar=dict(path=sidecar, sha256=sha(packed), uncompressedSha256=sha(payload)),
        rows=[{k: r[k] for k in ['address', 'bytes', 'source', 'origin', 'repairs', 'compileSucceeded']} |
            dict(byteExact=r.get('byteExact', False), compiledBytes=r.get('candidate', {}).get('compiledBytes'),
                sameOffsetBytes=r.get('candidate', {}).get('sameOffsetBytes'), error=r.get('error')) for r in rows])
    path = ROOT / 'evidence/lanes/save-core/mechanics-pointer149-20261101.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'rows'}))


if __name__ == '__main__':
    main()
