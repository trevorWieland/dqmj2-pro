import concurrent.futures
from pathlib import Path
import match_runtime as compiler
from project import ROOT, write_json, sha256
from link_runtime_unit import validate, measured_module
from recover_linked_runtime import qualified_bindings


def worker(spec):
    source, executable, opt = spec
    compiler.WORK = ROOT / 'work/main-fifo256-c99-ipa-20261102' / executable.split('/')[-2] / opt.replace(',', '-')
    compiler.FLAGS = [*compiler.FLAGS, '-lang', 'c99', '-ipa', 'file']
    rows, _ = compiler.compare(source, 'main', opt, 'off', compiler=ROOT / executable)
    result = dict(compiler=executable, optimization=opt, sourceCredit=0)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        return dict(result, compileRows=rows, genuineExact=False)
    row = rows[0]
    result['compilation'] = row
    try:
        proof = validate(row, qualified_bindings(row), compiler.WORK / 'link')
        result.update(genuineExact=True, genuineLinkComparison=proof)
    except ValueError as error:
        result.update(genuineExact=False, genuineLinkComparison=error.args[0])
    binary = compiler.WORK / 'link/caller.bin'
    if binary.exists():
        _, image, _ = measured_module('main')
        native, body = image[0xDED8:0xDFD8], binary.read_bytes()
        result.update(linkedBytes=len(body), matchingBytes=sum(a == b for a, b in zip(native, body)), linkedSha256=sha256(binary))
    return result


def main():
    report = ROOT / 'evidence/attempts/main-fifo256-c99-ipa-20261102.json'
    assert not report.exists()
    old = ROOT / 'generated/recovery/20261101-large-profile-breadth21/arm-0200ded8.c'
    text = old.read_text(encoding='utf-8')
    text = text.replace('extern u32 native_fn_02007ff4();', 'extern u32 native_fn_02007ff4(void);')
    text = text.replace('extern u32 native_fn_02008008();', 'extern void native_fn_02008008(u32);')
    text = text.replace('extern u32 native_fn_0200a440();', 'extern s32 native_fn_0200a440(u32, u32, u32);')
    text = text.replace('u32 native_main_0200ded8(s32 arg0, s16 arg1, s32 arg2, s16 arg3)',
        'void native_main_0200ded8(u32 arg0, u32 arg1, u32 arg2, u32 arg3)')
    text = text.replace('return (u32) native_data_020e53d0;', 'return;')
    text = text.replace('return M2C_FIELD(native_data_020e53d0, u32 (**)(u32, u32, u32), 4)(1, 4, 0);',
        'M2C_FIELD(native_data_020e53d0, void (**)(u32, u32, u32), 4)(1, 4, 0);\n        return;')
    text = text.replace('u32 (**)(u32, u32, u32)', 'void (**)(u32, u32, u32)')
    text = text.replace('return native_fn_02008008(temp_r5);', 'native_fn_02008008(temp_r5);')
    source = ROOT / 'nonmatching/main/20261102-fifo256-c99-ipa/native_main_0200ded8.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    jobs = [(source, exe, opt) for exe in compiler.COMPILER_PINS for opt in ['2', '4,p']]
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool: results = list(pool.map(worker, jobs))
    write_json(report, dict(sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), nativeReturns=0,
        selectedInterfacesNotQualified=True, results=results))
    print([(r.get('genuineExact'), r.get('linkedBytes'), r.get('matchingBytes')) for r in results])


if __name__ == '__main__':
    main()
