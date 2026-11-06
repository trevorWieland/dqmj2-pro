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
    rows = json.loads(gzip.decompress((ROOT / 'evidence/vectors/save-core-save-family144-provenance-20261101.json.gz').read_bytes()))
    selected = [0x0207ADCC, 0x0207B004, 0x0207B5FC, 0x0207B768, 0x0207B790, 0x0207CD98, 0x0207D198, 0x0207D9B4]
    jobs = []
    for row in rows:
        address = int(row['address'], 0)
        if address not in selected:
            continue
        original = ROOT / row['source']
        text = original.read_text()
        repairs = []
        if address == 0x0207ADCC:
            text = text.replace('*(temp_r0 + var_r3)', '*(u8 *)(temp_r0 + var_r3)')
            repairs.append('LDRB at7ADF8 requires byte pointer view of raw returned descriptor address')
        elif address == 0x0207B004:
            text = text.replace('*(M2C_FIELD(native_data_021c6744, s32 *, 4) + (arg0 * 0x28))',
                '*(u32 *)(M2C_FIELD(native_data_021c6744, u32 *, 4) + (arg0 * 0x28))')
            repairs.append('LDR at7B010 loads pointer word;7B014 reads word at byte stride40')
        elif address == 0x0207B5FC:
            text = text.replace('(s32 arg0)', '(u8 *arg0)').replace('    u8 temp_r3;', '    u8 temp_r3;\n    u8 temp_r2;')
            text = text.replace('                *(arg0 + var_r5) = temp_r3;\n                *(arg0 + var_lr) = *(arg0 + var_r5);',
                '                temp_r2 = *(arg0 + var_r5);\n                *(arg0 + var_r5) = temp_r3;\n                *(arg0 + var_lr) = temp_r2;')
            repairs.append('LDRB/STRB byte input and native7B634 read-before-write swap;old draft lost aliased original byte')
        elif address in [0x0207B768, 0x0207D198]:
            text = text.replace('(s32 arg0)', '(const u8 *arg0)').replace('(s32 arg0,', '(const u8 *arg0,')
            repairs.append('Native LDRB scan consumes byte pointer,not dereference of scalar arithmetic')
        elif address == 0x0207B790:
            text = text.replace('    u8 sp0;', '    u8 sp0[64];').replace('= &sp0;', '= sp0;')
            text = text.replace('    var_r5 = saved_reg_r5;\n', '').replace('    var_r7 = saved_reg_r7;\n', '')
            text = text.replace('*(temp_r1 + var_r5)', '*(u8 *)(temp_r1 + var_r5)')
            repairs.append('Native64-byte local allocation,escaped byte pointer,and LDRB input;helper-kind default remains indeterminate outside demonstrated0/1/2 domain')
        elif address == 0x0207CD98:
            text = text.replace('extern s32 native_data_021c67a8;', 'extern u32 native_data_021c67a8;')
            text = text.replace('*(native_data_021c67a8 + (arg0 * 4))', '*(u32 *)(native_data_021c67a8 + ((u32)arg0 * 4))')
            repairs.append('Native global LDR followed by fullword indexed LDR;index multiplication is byte offset4')
        elif address == 0x0207D9B4:
            text = text.replace('var_r2 = var_r6 + (0x7FF & (temp_r2 >> 1));', 'var_r2 = (u8 *)(var_r6 + (0x7FF & (temp_r2 >> 1)));')
            text = text.replace('*var_r10 = temp_r0;', '*(u8 *)var_r10 = temp_r0;')
            repairs.append('Native byte copy source/destination pointer views;raw unsigned address arithmetic retained')
        assert text != original.read_text() and len(text.splitlines()) <= 500
        path = ROOT / 'nonmatching/save-core/20261101-pointer-frontier145' / original.name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        jobs.append(dict(address=address, bytes=row['bytes'], source=path.relative_to(ROOT).as_posix(),
            origin=original.relative_to(ROOT).as_posix(), originSha256=sha(original.read_bytes()),
            sourceSha256=sha(path.read_bytes()), repairs=repairs))
    assert len(jobs) == 8
    return jobs


def worker(job):
    spec = importlib.util.spec_from_file_location('pointer_frontier145_builder', ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.MODE = job['address'], job['bytes'], 'arm'
    builder.MODULE, builder.NAME = 'main', 'native_main_' + f"{job['address']:08x}"
    builder.SOURCE, builder.WORK = job['source'], 'work/save-core/pointer-frontier145/' + f"{job['address']:08x}"
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
    sidecar = 'evidence/vectors/save-core-pointer-frontier145-20261101.json.gz'
    packed = gzip.compress(payload, mtime=0)
    (ROOT / sidecar).write_bytes(packed)
    report = dict(schema=1, draftedFunctions=len(rows), draftedNativeBytes=sum(r['bytes'] for r in rows),
        compileSucceeded=sum(r['compileSucceeded'] for r in rows),
        byteExactCandidates=sum(r.get('byteExact', False) for r in rows), qualifiedSourceBytes=0,
        vectorSidecar=dict(path=sidecar, sha256=sha(packed), uncompressedSha256=sha(payload)),
        rows=[{k: r[k] for k in ['address', 'bytes', 'source', 'origin', 'repairs', 'compileSucceeded']} |
            dict(byteExact=r.get('byteExact', False), compiledBytes=r.get('candidate', {}).get('compiledBytes'),
                sameOffsetBytes=r.get('candidate', {}).get('sameOffsetBytes'), error=r.get('error')) for r in rows])
    path = ROOT / 'evidence/lanes/save-core/pointer-frontier145-20261101.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'rows'}))


if __name__ == '__main__':
    main()
