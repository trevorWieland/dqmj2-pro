from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    original = ROOT / 'generated/recovery/20261101-large-profile-breadth21/arm-0202fb98.c'
    text = original.read_text(encoding='utf-8')
    before = """            temp_r0_2 = M2C_FIELD(arg0, s32 *, 8);
            if (*M2C_FIELD(arg0, s32 **, 0xB8) != 0) {
                M2C_FIELD(arg0, s32 *, 8) = (s32) (temp_r0_2 | 1);
            } else {
                M2C_FIELD(arg0, s32 *, 8) = (s32) (temp_r0_2 & ~1);
            }"""
    assert text.count(before) == 1
    ordered = """            temp_r0_2 = *M2C_FIELD(arg0, s32 **, 0xB8);
            if (temp_r0_2 != 0) {
                M2C_FIELD(arg0, s32 *, 8) |= 1;
            } else {
                M2C_FIELD(arg0, s32 *, 8) &= ~1;
            }"""
    ordered2 = """            temp_r0_2 = *M2C_FIELD(arg0, s32 **, 0xB8);
            temp_r1 = M2C_FIELD(arg0, s32 *, 8);
            if (temp_r0_2 != 0) {
                M2C_FIELD(arg0, s32 *, 8) = temp_r1 | 1;
            } else {
                M2C_FIELD(arg0, s32 *, 8) = temp_r1 & ~1;
            }"""
    results = []
    for label, block in [('original-order', before), ('read-predicate-first', ordered), ('explicit-read-order', ordered2)]:
        variant = text.replace(before, block).replace('temp_r4 >> 5', '(u32) temp_r4 >> 5')
        variant = variant.replace('(1 << (temp_r4 & 0x1F))', '(1U << (temp_r4 & 0x1F))')
        source = ROOT / f'generated/recovery/20261101-callback380/{label}/native_main_0202fb98.c'
        assert not source.exists()
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(variant, encoding='utf-8')
        for speed in [False, True]:
            directory = ROOT / f'work/main-callback380-20261101/{label}/{int(speed)}'
            compiler.WORK = directory / 'compile'
            rows, unused = compiler.compare(source, 'main', 2, 'off', speed=speed,
                compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
            row = rows[0]
            result = dict(label=label, speed=speed, source=source.relative_to(ROOT).as_posix(),
                sourceSha256=sha256(source), compilation=row, sourceCredit=0, exact=False)
            try:
                proof = validate(row, qualified_bindings(row), directory / 'link')
                result['exact'] = True
            except ValueError as error:
                assert isinstance(error.args[0], dict)
                proof = error.args[0]
            result['genuineLinkComparison'] = proof
            results.append(result)
            print(dict(label=label, speed=speed, exact=result['exact'], proof=proof), flush=True)
    write_json(ROOT / 'evidence/attempts/main-callback380-20261101.json',
        dict(sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
            originalSource=original.relative_to(ROOT).as_posix(), originalSourceSha256=sha256(original), results=results,
            limitations=['Canonical compiler/link hypotheses only; native fixtures and interface review are pending']))


if __name__ == '__main__':
    main()
