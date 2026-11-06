import os
import re
import subprocess
import match_runtime as compiler
import match_main_oam_reference296_closed_20261101 as builder
from slice_reference_sdk_entities_v3_20261102 import functions, slice_closed
from project import ROOT, write_json, sha256


def main():
    work = ROOT / 'work/main-tp256-reference-20261102'
    work.mkdir(parents=True, exist_ok=True)
    sdk = ROOT / 'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840'
    original = sdk / 'libraries/spi/src/tp.c'
    expanded = work / 'expanded.i'
    flags = [*compiler.FLAGS, '-lang', 'c99', '-DSDK_CW_FORCE_EXPORT_SUPPORT', '-DSDK_TS', '-DSDK_4M',
        '-DSDK_ARM9', '-DSDK_CW', '-DSDK_FINALROM', '-DSDK_CODE_ARM', '-DNNS_FINALROM']
    for folder in [sdk / 'include', ROOT / 'generated/sdk-reference/20261101/parse-only-headers',
        ROOT / 'generated/sdk-reference/20261101/include']:
        flags += ['-i', folder.as_posix()]
    command = [str(compiler.COMPILER), *flags, '-E', str(original), '-o', str(expanded)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ,
        LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, timeout=60)
    result = dict(sourceCredit=0, sourceOrigin=original.relative_to(ROOT).as_posix(), sourceOriginSha256=sha256(original),
        compilerSha256=sha256(compiler.COMPILER), command=command, preprocessExitCode=process.returncode,
        stdout=process.stdout.decode(errors='replace'), stderr=process.stderr.decode(errors='replace'))
    if not process.returncode:
        text = expanded.read_text(encoding='utf-8')
        seed = 'TP_RequestAutoSamplingStartAsync'
        for row in sorted(functions(text), key=lambda r: r['start'], reverse=True):
            header = text[row['start']:row['opening']]
            if row['name'] == seed or re.search(r'\binline\b', header): continue
            text = text[:row['start']] + re.sub(r'\bstatic\s+', '', header).rstrip() + ';\n' + text[row['end']:]
        text, selection = slice_closed(text, [seed])
        text = re.sub(r'\bstatic\s+struct\s*\{', 'extern struct {', text)
        for old, new in [(seed, 'native_main_0200ded8'), ('tpState', 'native_data_main_020e53d0'),
            ('OS_DisableInterrupts', 'native_fn_02007ff4'), ('OS_RestoreInterrupts', 'native_fn_02008008'),
            ('PXI_SendWordByFifo', 'native_fn_0200a440')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
        result.update(expandedSha256=sha256(expanded), selection=selection,
            unresolvedAssembly=bool(re.search(r'\b(?:asm|__asm|__asm__)\b', text)))
        source = ROOT / 'nonmatching/main/20261102-tp256-reference/native_main_0200ded8.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text, encoding='utf-8')
        result.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), physicalLines=len(text.splitlines()))
        if not result['unresolvedAssembly']:
            builder.WORK = work / 'qualified-build'
            try:
                row, proof, body = builder.build(source, 'positive', True)
                result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, linkedBytes=len(body))
            except Exception as error:
                result.update(genuineExact=False, refusalType=type(error).__name__, refusal=str(error))
    write_json(ROOT / 'evidence/attempts/main-tp256-reference-20261102.json', result)
    print({key: result.get(key) for key in ['preprocessExitCode', 'physicalLines', 'unresolvedAssembly', 'genuineExact', 'linkedBytes']})


if __name__ == '__main__':
    main()
