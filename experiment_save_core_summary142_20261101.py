import concurrent.futures
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'nonmatching/save-core/20261101-save-summary142'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare():
    old = ROOT / 'nonmatching/save-core/20261031-lane-controller-context04'
    header = '\n'.join((old / 'native_main_02079d6c.c').read_text().splitlines()[:16]) + '\n'
    raw = (ROOT / 'evidence/analysis/save-core-save-summary142/initial-m2c.c.txt').read_text()
    globals_ = re.findall(r'^extern M2C_UNK (data_[0-9a-f]+);$', raw, re.M)
    raw = re.sub(r'^extern M2C_UNK data_[0-9a-f]+;\n', '', raw, flags=re.M)
    for name in globals_:
        references = list(re.finditer(r'\b' + name + r'\b', raw))
        assert references and all(raw[:m.start()].rstrip().endswith('&') for m in references)
        raw = re.sub(r'&\s*' + name + r'\b', name, raw)
    error = 'M2C_ERROR(/* Unable to find stack arg 0x0 in block */), M2C_ERROR(/* Unable to find stack arg 0x4 in block */)'
    assert raw.count(error) == 1
    raw = raw.replace(error, '2U, 0U')
    raw = raw.replace('    M2C_UNK sp10;', '    u16 text[30];')
    raw = raw.replace('    s16 spE;\n    s16 spC;', '    s16 coordinates[2];')
    raw = raw.replace('    M2C_UNK *var_r1;', '    u8 *cursor;')
    raw = re.sub(r'\bvar_r1\b', 'cursor', raw)
    raw = raw.replace('cursor = &sp10;', 'cursor = (u8 *)text;')
    raw = raw.replace('&sp10', 'text')
    raw = re.sub(r'\bspC\b', 'coordinates[0]', raw)
    raw = re.sub(r'\bspE\b', 'coordinates[1]', raw)
    raw = raw.replace('&coordinates[0]', 'coordinates')
    raw = raw.replace('func_020798b8', 'native_main_020798b8')
    raw = re.sub(r'\bfunc_((?:ov[0-9]{3}_)?[0-9a-f]{8})\b', r'native_fn_\1', raw)
    raw = re.sub(r'\bdata_([0-9a-f]{8})\b', r'native_data_\1', raw)
    aliases = sorted(set(re.findall(r'\b(native_fn_(?:ov[0-9]{3}_)?[0-9a-f]{8})\b', raw)))
    declarations = []
    for alias in aliases:
        declarations.append('extern void **native_fn_02049ad0(u32);' if alias == 'native_fn_02049ad0' else 'extern u32 ' + alias + '();')
    declarations += ['extern u8 native_' + name + '[];' for name in globals_]
    source = header + '\n'.join(declarations) + '\n' + raw
    assert not re.search(r'M2C_ERROR|M2C_UNK|/\*|//', source)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'native_main_020798b8.c').write_text(source, newline='\n')
    for name in ['native_main_02079d6c.c', 'native_main_02079f9c.c']:
        source = (old / name).read_text()
        if name == 'native_main_02079d6c.c':
            source = source.replace('    s16 sp14;', '    s16 coordinates[2];')
            source = source.replace('&sp14', 'coordinates')
            source = re.sub(r'\bsp14\b', 'coordinates[0]', source)
        assert len(source.splitlines()) <= 500
        (OUT / name).write_text(source, newline='\n')


def worker(task):
    address, length, speed = task
    sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
    path = ROOT / 'evidence/application/save_core_historical_link_20261031.py'
    spec = importlib.util.spec_from_file_location('summary142_build', path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.MODULE, builder.MODE, builder.ENTRY, builder.LENGTH = 'main', 'arm', address, length
    builder.NAME = f'native_main_{address:08x}'
    builder.SOURCE = (OUT / (builder.NAME + '.c')).relative_to(ROOT).as_posix()
    builder.WORK = f'work/save-core/save-summary142/{address:08x}/' + ('speed' if speed else 'default')
    base = json.loads((ROOT / 'evidence/lanes/save-core/slot-kind141-profile-20261101.json').read_text())
    builder.COMPILER, builder.COMPILER_HASH = base['compilerPath'], base['compilerSha256']
    builder.FLAGS = [*base['flags'], *(['-opt', 'speed'] if speed else [])]
    arm = builder.measured_module('main')[1]
    try:
        row, _ = builder.build(arm[address - 0x02000000:address - 0x02000000 + length])
        return dict(address=hex(address), speed=speed, row=row, sourceCredit=0)
    except Exception as error:
        return dict(address=hex(address), speed=speed, errorType=type(error).__name__, error=str(error), sourceCredit=0)


def main():
    prepare()
    tasks = [(address, length, speed) for address, length in [(0x020798B8, 1204), (0x02079D6C, 560), (0x02079F9C, 36)] for speed in [False, True]]
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(worker, tasks))
    path = ROOT / 'evidence/lanes/save-core/save-summary142-20261101.json'
    path.write_text(json.dumps(dict(schema=1, sourceCredit=0, rows=rows,
        measuredStackRepair=dict(callSite='0x02079a70', stack0=2, stack4=0,
            storeSites=['0x02079a58', '0x02079a60'], justification='Decoded original MOV/STR sequence,not inferred missing helper arity'),
        boundedLocals=dict(textBytes=60, halfwords=30, coordinatesBytes=4),
        limitations=['All units are source hypotheses with no accepted coverage. Temporary snapshot rendering/widget setup/teardown are not serialization or arbitration.','Declared60-byte text storage comes from the original7x8+4 halfword-clear loop;two coordinates share a real4-byte object. Other signatures,source return views and caller/device prerequisites remain unqualified.']), indent=2) + '\n')
    for result in rows:
        row = result.get('row', {})
        print(dict(address=result['address'], speed=result['speed'], error=result.get('error'),
                   compiledBytes=row.get('compiledBytes'), sameOffsetBytes=row.get('sameOffsetBytes'), exact=row.get('exactByteEqual')))


if __name__ == '__main__':
    main()
