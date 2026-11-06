import copy
from project import ROOT, read_json, write_json, sha256
from parallel_status import interval
from audit_original_assembly_ranges_20261105 import qualify


def main():
    path = 'evidence/matches/cohort155-parallel-wave20261104-e-main-sdk-prefix-original-asm-0.json'
    rows = read_json(ROOT / path)['matches']
    positives = [qualify(row, interval(row)) for row in rows]
    assert len(positives) == 9 and sum(row['justifiedAssemblyBytes'] for row in positives) == 1184
    mutations = [
        ('language', ['sourceLanguage'], 'C'),
        ('classification', ['assemblyJustification', 'classification'], 'inferred-assembly'),
        ('explicit-origin', ['assemblyJustification', 'originalExplicitAsmDeclaration'], False),
        ('source-origin', ['assemblyJustification', 'sourceStatementsDerivedFromPublishedSdkNotDisassembly'], False),
        ('ordinary-exception', ['assemblyJustification', 'ordinaryLogicAssemblyExceptions'], 1),
        ('origin-sha', ['assemblyJustification', 'publishedSourceSha256'], '0' * 64),
        ('origin-escape', ['assemblyJustification', 'publishedSource'], '../outside.c'),
        ('ordinary-accounting', ['ordinaryCBytes'], 1),
        ('assembly-accounting', ['justifiedAssemblyBytes'], 60),
        ('partial-range', ['justifiedAssemblyRanges', 0, 'bytes'], 60),
        ('nonzero-offset', ['justifiedAssemblyRanges', 0, 'offset'], 4),
        ('interior-address', ['justifiedAssemblyRanges', 0, 'address'], '0x0200d8c8'),
        ('other-cpu', ['justifiedAssemblyRanges', 0, 'processor'], 'arm7'),
        ('other-program', ['justifiedAssemblyRanges', 0, 'program'], 'dwc/utility.bin/move/child.srl'),
        ('other-module', ['justifiedAssemblyRanges', 0, 'module'], 'ov001'),
        ('other-mode', ['justifiedAssemblyRanges', 0, 'mode'], 'thumb'),
        ('unpublished-declaration', ['assemblyJustification', 'publishedAsmDeclaration'], 'asm void Other(void)'),
        ('unjustified-necessity', ['assemblyJustification', 'hardwareOrAbiNecessity'], ''),
        ('raw-source', ['assemblyJustification', 'rawExecutableBytesStoredAsSource'], True),
        ('execution-credit', ['assemblyJustification', 'hardwareExceptionOrCalleeExecutionCredit'], 1),
        ('duplicate-range', ['justifiedAssemblyRanges'], rows[0]['justifiedAssemblyRanges'] * 2),
    ]
    controls = []
    for name, keys, value in mutations:
        wrong = copy.deepcopy(rows[0])
        target = wrong
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        try:
            qualify(wrong, interval(rows[0]))
        except (AssertionError, ValueError):
            controls.append(name)
        else:
            raise AssertionError('Invalid original assembly contract admitted: ' + name)
    output = 'evidence/lanes/parallel-wave20261104/original-assembly-range-controls.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, positiveFunctions=9,
        positiveAssemblyBytes=1184, negativeControls=controls, sourceReport=path,
        sourceReportSha256=sha256(ROOT / path), qualifierSha256=sha256(ROOT / 'audit_original_assembly_ranges_20261105.py'),
        originalProductionClassifierRetained=True, originalMixedRangeAuditorUnchanged=True,
        nativeHardwareOrExceptionExecutionCredit=0))
    print(dict(passed=True, functions=9, assemblyBytes=1184, rejectedControls=len(controls)))


if __name__ == '__main__':
    main()
