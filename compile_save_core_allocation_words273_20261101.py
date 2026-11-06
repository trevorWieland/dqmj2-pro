import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module


def compile_one(source, speed):
    spec = importlib.util.spec_from_file_location('allocation_words273_' + str(speed), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.NAME = 0x0207726C, 1516, 'native_main_0207726c'
    builder.SOURCE = source
    builder.WORK = 'work/save-core/allocation-words273/' + Path(source).stem + ('-speed' if speed else '-space')
    if speed:
        builder.FLAGS = [*builder.FLAGS, '-opt', 'speed']
    arm = measured_module('main')[1]
    row, body = builder.build(arm[0x7726C:0x77858])
    return row


def main():
    origin = 'nonmatching/save-core/20261101-explicit-byte-views262/native_main_0207726c.c'
    text = (ROOT / origin).read_text()
    descriptor = text.replace('extern u8 native_data_021c64d0[];', 'extern u32 native_data_021c64d0[];')
    old = '*(native_data_021c64d0 + (M2C_FIELD(native_data_021c6330, s32 *, 0) * 4))'
    assert descriptor.count(old) == 3
    descriptor = descriptor.replace(old, 'native_data_021c64d0[M2C_FIELD(native_data_021c6330, s32 *, 0)]')
    words = descriptor.replace('extern u32 native_data_021c6524;', 'extern u32 native_data_021c6524[];')
    words = words.replace('(&native_data_021c6524)[', 'native_data_021c6524[')
    words = words.replace('field_1ec = native_data_021c6524;', 'field_1ec = native_data_021c6524[0];')
    folder = ROOT / 'nonmatching/save-core/20261101-allocation-words273'
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, value in [('descriptor_words', descriptor), ('descriptor_and_roster_words', words)]:
        path = folder / (name + '.c')
        if path.exists():
            assert path.read_text() == value
        else:
            path.write_text(value)
        for speed in (False, True):
            rows.append(compile_one(path.relative_to(ROOT).as_posix(), speed))
    report = dict(schema=1, origin=origin, rows=rows, sourceCredit=0,
        changes=['Descriptor table021C64D0 holds full address words written by native constructor atSTATE+29C.',
            'Index scaling isfour bytes once. The prior byte declaration erased the native pointer high bits.',
            'Roster word indexing removes pointer arithmetic beyond an inferred scalar declaration;no array extent isclaimed.'],
        limitations=['Unaccepted source hypotheses only;other scalar/array inferences,ABI contracts andfull caller effects remain under review.',
            'These are source views with no original declarations,lifecycle or scene reachability claim.'])
    target = ROOT / 'evidence/lanes/save-core/allocation-words273-20261101.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps([dict(source=row['source'], compiledBytes=row['compiledBytes'], sameOffsetBytes=row['sameOffsetBytes']) for row in rows]))


if __name__ == '__main__':
    main()
