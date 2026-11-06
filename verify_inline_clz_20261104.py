import copy
from project import ROOT, read_json, write_json, sha256
from qualify_inline_clz_20261104 import qualify, classify
from prepare_source_cohort_v3_20261102 import classify_additions


def main():
    report = read_json(ROOT / 'evidence/matches/cohort151-parallel-wave20261104-a-main-sdk-residual-0.json')
    rows = report['matches']
    positives = [qualify(row) for row in rows]
    tests = []

    def reject(name, mutate):
        row = copy.deepcopy(rows[0])
        mutate(row)
        try:
            qualify(row)
        except (AssertionError, ValueError, KeyError, StopIteration) as error:
            tests.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError('Invalid mixed input accepted: ' + name)

    reject('ordinary-source-label', lambda row: row.update(sourceLanguage='C'))
    reject('unknown-primitive', lambda row: row['assemblyJustification'].update(originalSymbol='other'))
    reject('raw-bytes', lambda row: row['assemblyJustification'].update(rawExecutableBytesStoredAsSource=True))
    reject('invented-caller-credit', lambda row: row['assemblyJustification'].update(wholeCallerBehaviorCredit=1))
    reject('invented-callee-credit', lambda row: row['assemblyJustification'].update(primitiveProbeCalleeSourceCredit=1))
    reject('provenance-identity', lambda row: row['assemblyJustification'].update(provenanceSha256='0' * 64))
    reject('source-identity', lambda row: row.update(sourceSha256='0' * 64))
    reject('object-identity', lambda row: row.update(objectSha256='0' * 64))
    reject('native-identity', lambda row: row.update(targetSha256='0' * 64))
    reject('wrong-cpu', lambda row: row.update(processor='arm7'))
    reject('overlapping-overlay', lambda row: row.update(module='ov005'))
    reject('different-program', lambda row: row.update(program='utility'))
    reject('thumb-mode', lambda row: row.update(mode='thumb'))
    reject('unpinned-context', lambda row: row.update(sourceDependencies=[]))
    reject('missing-instruction', lambda row: row['justifiedAssemblyRanges'].pop())
    reject('duplicate-instruction', lambda row: row['justifiedAssemblyRanges'].append(copy.deepcopy(row['justifiedAssemblyRanges'][0])))
    reject('wrong-instruction-address', lambda row: row['justifiedAssemblyRanges'][0].update(address='0x20355f0'))
    reject('wrong-instruction-encoding', lambda row: row['justifiedAssemblyRanges'][0].update(originalEncodedWord='00000000'))
    reject('unaligned-instruction', lambda row: row['justifiedAssemblyRanges'][0].update(offset=185))
    reject('instruction-count', lambda row: row['assemblyJustification'].update(nativeInstructions=100))
    reject('ordinary-byte-overcredit', lambda row: row.update(ordinaryCBytes=row['bytes']))
    reject('assembly-byte-undercredit', lambda row: row.update(justifiedAssemblyBytes=0))
    directory = ROOT / 'work/integration/inline-clz-classification-controls'
    directory.mkdir(parents=True, exist_ok=True)
    for name, edit in [('additional-asm', lambda text: text + '\nasm { mov r0, r0 }\n'),
                       ('changed-primitive', lambda text: text.replace('clz x, x', 'mov x, x'))]:
        original = ROOT / rows[0]['assemblyJustification']['sourceHelperPins'][0]['path']
        path = directory / (name + '.h')
        path.write_text(edit(original.read_text(encoding='utf-8')), encoding='utf-8')
        pin = dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path))

        def mutate(row):
            row['assemblyJustification']['sourceHelperPins'] = [pin]
            row['sourceDependencies'] = [pin]

        reject(name, mutate)
    after = {(row['module'], row['mode'], int(row['address'], 0)): dict(row, size=row['bytes']) for row in rows}
    accounting, receipts = classify(after, set(after), classify_additions)
    assert accounting['newMixedSourceFunctions'] == 3
    assert accounting['newOrdinaryCBytes'] == 1120 and accounting['newVerifiedOriginalAssemblyBytes'] == 24
    assert accounting['newOrdinaryCFunctions'] == accounting['newVerifiedOriginalAssemblyFunctions'] == 0
    write_json(ROOT / 'evidence/lanes/parallel-wave20261104/inline-clz-classification-controls.json', dict(
        passed=True, sourceCredit=0, positiveMixedFunctions=len(positives), negativeControls=tests,
        accounting=accounting, sourceObjectAndNativeFilesUnchanged=True,
        ordinaryAndWholeAssemblyClassifierUnchanged=True, wholeCallerBehaviorCredit=0))
    print(dict(passed=True, positiveFunctions=len(positives), negativeControls=len(tests), accounting=accounting))


if __name__ == '__main__':
    main()
