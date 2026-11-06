import concurrent.futures
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]


def worker(task):
    name, profile = task
    path = ROOT / 'evidence/application/save_core_historical_link_20261031.py'
    spec = importlib.util.spec_from_file_location('switch141_' + name, path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.MODULE, builder.MODE = 0x02046188, 236, 'main', 'arm'
    builder.NAME, builder.SOURCE = profile['name'], profile['source']
    builder.COMPILER, builder.COMPILER_HASH = profile['compilerPath'], profile['compilerSha256']
    builder.FLAGS = profile['flags']
    builder.WORK = 'work/save-core/switch-mask141/' + name
    arm = builder.measured_module('main')[1]
    row, _ = builder.build(arm[0x46188:0x46274])
    return dict(variant=name, row=row)


def main():
    profiles = json.loads((ROOT / 'evidence/lanes/save-core/measured-inputs140-profile-20261101.json').read_text())['rows']
    original = next(p for p in profiles if int(p['address'], 0) == 0x02046188)
    source = (ROOT / original['source']).read_text()
    tasks = []
    for name, typ, expression in [('byte', 'u8', '(u8)arg1'), ('word', 'u32', '(arg1 & 255U)')]:
        text = source.replace('    s32 temp_r4;', f'    s32 temp_r4;\n    {typ} selector;')
        text = text.replace('    switch ((u8)arg1)', f'    selector = {expression};\n    switch (selector)')
        target = ROOT / f'nonmatching/save-core/20261101-switch-mask141/{name}.c'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, newline='\n')
        profile = dict(original, source=target.relative_to(ROOT).as_posix())
        tasks.append((name, profile))
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(worker, tasks))
    path = ROOT / 'evidence/lanes/save-core/switch-mask141-20261101.json'
    path.write_text(json.dumps(dict(sourceCredit=0, rows=rows), indent=2) + '\n')
    for result in rows:
        row = result['row']
        print(dict(variant=result['variant'], compiledBytes=row['compiledBytes'],
                   sameOffsetBytes=row['sameOffsetBytes'], exact=row['exactByteEqual']))


if __name__ == '__main__':
    main()
