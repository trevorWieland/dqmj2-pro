import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module


def main():
    origin = 'nonmatching/save-core/20261101-mixed-fields243/native_main_02076700.c'
    text = (ROOT / origin).read_text()
    assert text.count('&native_data_021c6234 +') == 3
    text = text.replace('&native_data_021c6234 +', '(u8 *)&native_data_021c6234 +')
    old = 'u8 field_2de; u8 field_2df; } ObservedFields_021c6234;'
    assert old in text
    text = text.replace(old, 'u8 field_2de; u8 field_2df; u8 opaque_2e0[40]; } ObservedFields_021c6234;')
    path = ROOT / 'nonmatching/save-core/20261101-roster-stride274/native_main_02076700.c'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_text() == text
    else:
        path.write_text(text)
    arm = measured_module('main')[1]
    rows = []
    for speed in (False, True):
        spec = importlib.util.spec_from_file_location('roster_stride274_' + str(speed), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        builder.ENTRY, builder.LENGTH, builder.NAME = 0x02076700, 448, 'native_main_02076700'
        builder.SOURCE = path.relative_to(ROOT).as_posix()
        builder.WORK = 'work/save-core/roster-stride274/' + ('speed' if speed else 'space')
        if speed:
            builder.FLAGS = [*builder.FLAGS, '-opt', 'speed']
        row, body = builder.build(arm[0x76700:0x768C0])
        rows.append(row)
    report = dict(schema=1, origin=origin, rows=rows, sourceCredit=0,
        minimumObservedGlobalBytes=0x308, reasons=['Native initialization writes six4-byte entries at byte offsets2F0..307.',
            'The base must be converted tobyte pointer before index*4 arithmetic;the previous inferred-struct pointer multiplied bystruct size.',
            'Opaque tail bytes only cover the directly observed six-word write extent;no original fields/declaration/full object extent isclaimed.'],
        limits=['Compiler/linking stage only. Ordinary caller reachability,callee interfaces andfull native effect tests remain unproved.'])
    output = ROOT / 'evidence/lanes/save-core/roster-stride274-20261101.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps([dict(compiledBytes=row['compiledBytes'], sameOffsetBytes=row['sameOffsetBytes'], exact=row['exactByteEqual']) for row in rows]))


if __name__ == '__main__':
    main()
