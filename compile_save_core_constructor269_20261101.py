import concurrent.futures
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module


def compile_one(task):
    source, speed = task
    spec = importlib.util.spec_from_file_location('constructor269_' + str(speed), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.NAME = 0x02077A5C, 1084, 'native_main_02077a5c'
    builder.SOURCE = source
    builder.WORK = 'work/save-core/constructor269/' + Path(source).stem + ('-speed' if speed else '-space')
    if speed:
        builder.FLAGS = [*builder.FLAGS, '-opt', 'speed']
    arm = measured_module('main')[1]
    row, body = builder.build(arm[0x77A5C:0x77E98])
    return dict(speed=speed, **row)


def main():
    origin = 'nonmatching/save-core/20261101-mixed-fields243/native_main_02077a5c.c'
    text = (ROOT / origin).read_text()
    old = '&native_data_021c6234 + (var_r9 * 4)'
    assert old in text
    byte_view = text.replace(old, '(u8 *)&native_data_021c6234 + (var_r9 * 4)')
    popup = byte_view.replace('native_fn_ov000_02217bdc(5, 6, var_r9_2, 1, -1)',
                              'native_fn_ov000_02217bdc(5, 6, var_r9_2, 1, 1, -1)')
    assert popup != byte_view
    width = popup.replace('extern u32 native_fn_02048188();', 'extern u32 native_fn_02048188(u32 arg0, u32 arg1);')
    width = width.replace('native_fn_02048188(0x20)', 'native_fn_02048188(0x20, 0)')
    assert width != popup
    folder = ROOT / 'nonmatching/save-core/20261101-constructor269'
    folder.mkdir(parents=True, exist_ok=True)
    sources = []
    for name, value in [('byte_stride', byte_view), ('popup_six_words', popup), ('width_two_words', width)]:
        path = folder / (name + '.c')
        if path.exists():
            assert path.read_text() == value
        else:
            path.write_text(value)
        sources.append(path.relative_to(ROOT).as_posix())
    tasks = [(path, speed) for path in sources for speed in (False, True)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(compile_one, tasks))
    report = dict(schema=1, origin=origin, rows=rows, sourceCredit=0, compilerWorkers=2,
        changes=['Cast the observed global base to byte pointer before dynamic byte offset arithmetic.',
            'Native77CC0/77CD0 stores two stack words for the six-word popup call.',
            'Native77D38 clearsR1 before48188;77D64 setsR1=2 for the second call.'],
        limits=['New source hypotheses only;source API coherence,ordinary reachability,full effects and exact bytes remain unproved.',
            'No register forcing,padding,assembly,opcode edits or accepted source edits.'])
    target = ROOT / 'evidence/lanes/save-core/constructor269-20261101.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps([dict(source=r['source'], speed=r['flags'][-2:] == ['-opt', 'speed'],
        compiledBytes=r['compiledBytes'], sameOffsetBytes=r['sameOffsetBytes']) for r in rows]))


if __name__ == '__main__':
    main()
