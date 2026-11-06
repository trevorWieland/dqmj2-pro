from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    report_path = ROOT / 'evidence/attempts/main-random-word152-trials-20261101.json'
    assert not report_path.exists()
    input_path = ROOT / 'evidence/attempts/root-breadth-archive-recompile-v2-20261101.json'
    previous = next(row for row in read_json(input_path)['results'] if row['identity']['address'] == '0x203d158')
    original = ROOT / previous['source']
    assert sha256(original) == previous['sourceSha256']
    text = original.read_text()
    before = 'native_data_020f6028.field_c = (u32) (temp_r4 | (temp_r0 << 8) | ((u16) ((temp_r4 * ~temp_r0) + 0x7B) << 0x10));'
    assert text.count(before) == 1
    high = '((u32) (u16) ((temp_r4 * ~temp_r0) + 0x7B) << 16)'
    lows = ['(temp_r4 | (temp_r0 << 8))', '((temp_r0 << 8) | temp_r4)',
        '((u32) temp_r4 + ((u32) temp_r0 << 8))']
    variants = []
    for index, low in enumerate(lows):
        for reverse in [False, True]:
            value = high + ' | ' + low if reverse else low + ' | ' + high
            variants.append((f'expression-{index}-{int(reverse)}', text.replace(before, 'native_data_020f6028.field_c = ' + value + ';')))
    for kind in ['u16', 'u32']:
        for declaration in ['    u8 temp_r0;', '    u8 temp_r4;', '    u32 temp_r5;']:
            for reverse in [False, True]:
                modified = text.replace(declaration, '    ' + kind + ' high_half;\n' + declaration)
                value = '((u32) high_half << 16) | (temp_r4 | (temp_r0 << 8))' if reverse else '(temp_r4 | (temp_r0 << 8)) | ((u32) high_half << 16)'
                modified = modified.replace(before, 'high_half = (u16) ((temp_r4 * ~temp_r0) + 0x7B);\n        native_data_020f6028.field_c = ' + value + ';')
                variants.append((kind + '-' + declaration.strip().split()[-1].strip(';') + '-' + str(int(reverse)), modified))
    result = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        inputReport=input_path.relative_to(ROOT).as_posix(), inputReportSha256=sha256(input_path),
        source=original.relative_to(ROOT).as_posix(), sourceSha256=sha256(original), results=[],
        limitations=['Ordinary C expression/local-lifetime hypotheses only; original source and selected objects remain unchanged',
            'Unsigned high-half shifting avoids signed left-shift overflow in the earlier generated draft',
            'RNG meaning, caller reachability and independent execution require separate proof even after an exact link'])
    for label, modified in variants:
        source = ROOT / f'generated/recovery/20261101-random-word152/{label}/native_main_0203d158.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(modified, encoding='utf-8')
        compiler.WORK = ROOT / f'work/main-random-word152-trials-20261101/{label}/compile'
        flags = previous['compilation']['compilerFlags']
        rows, unused = compiler.compare(source, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
            speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed', compiler=ROOT / previous['compilation']['compilerPath'])
        row = rows[0]
        trial = dict(label=label, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            compilation=row, compiled=not row.get('compileFailed'), exact=False, sourceCredit=0)
        if trial['compiled']:
            try:
                proof = validate(row, qualified_bindings(row), ROOT / f'work/main-random-word152-trials-20261101/{label}/link')
                trial['exact'] = True
            except ValueError as error:
                proof = error.args[0]
            trial['genuineLinkComparison'] = proof
        result['results'].append(trial)
        write_json(report_path, result)
    result.update(finished=True, exactVariants=sum(row['exact'] for row in result['results']))
    write_json(report_path, result)
    print(dict(variants=len(variants), exactVariants=result['exactVariants'], sourceCredit=0))


if __name__ == '__main__':
    main()
