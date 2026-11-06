from project import ROOT, sha256, write_json
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

UNITS = [
    ('02037d6c-25db874f41d0', '02037d6c', [
        ('native_fn_0202b784();', 'native_fn_0202b784(u32, u32, u32);'),
        ('native_fn_0202ba20();', 'native_fn_0202ba20(void *, u32);'),
        ('extern u32 native_fn_02037d28();', 'extern u32 native_fn_02037d28(u32);'),
        ('native_fn_02037d28();', 'native_fn_02037d28(temp_r0);'),
        ('native_fn_0202ba20(arg0 + 4,', 'native_fn_0202ba20((u8 *)arg0 + 4,')]),
    ('02037d38-f5b2f68eb536', '02037d38', [
        ('native_fn_0202b9dc();', 'native_fn_0202b9dc(void *, u32);'),
        ('native_fn_02037d6c();', 'native_fn_02037d6c(s32 *);'),
        ('native_fn_0202b9dc(arg0 + 4,', 'native_fn_0202b9dc((u8 *)arg0 + 4,')]),
    ('02037750-099ac6001d23', '02037750', [
        ('*native_data_020f1f10 =', '*(u32 *)native_data_020f1f10 =')]),
]


def main():
    results = []
    for key, address, replacements in UNITS:
        original = ROOT / f'nonmatching/main-runtime/20261031-qualified-main-frontier/{key}/source.c'
        source = ROOT / f'src/runtime/20261031_field_widths/native_main_{address}.c'
        text = original.read_text()
        for before, after in replacements:
            assert text.count(before) == 1, (address, before)
            text = text.replace(before, after)
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists() or source.read_text() == text
        source.write_text(text, encoding='utf-8')
        compiler.WORK = ROOT / f'work/main-field-width-probe-20261031/{address}/compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off')
        assert len(rows) == 1
        row = rows[0]
        result = dict(match=row, input=original.relative_to(ROOT).as_posix(), inputSha256=sha256(original))
        try:
            result['proof'] = validate(row, qualified_bindings(row), compiler.WORK.parent / 'link')
        except ValueError as error:
            result['linkFailure'] = str(error)
        results.append(result)
    write_json(ROOT / 'evidence/attempts/main-field-width-probe-20261031.json',
               dict(results=results, genuineUnits=sum('proof' in row for row in results), sourceCredit=0))
    print(dict(genuineUnits=sum('proof' in row for row in results), sourceCredit=0))


if __name__ == '__main__':
    main()
