import copy
import shutil
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import wave20261105_main_sdk_bulk_compiler as C
import wave20261105_main_sdk_bulk_system_bindings as B
import wave20261105_main_sdk_bulk_system_fixture as V
import wave20261104_main_sdk_prefix_match as F
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/system/packet'
INPUT = LANE / 'inputs.json'
WORK = ROOT / 'work/w5sb/system-proof'
F.C = C


def controls(item, row, source, directory):
    results = []
    target = directory / 'wrong-err-guard'
    target.mkdir(parents=True, exist_ok=True)
    text = source.read_text()
    assert text.count('if (err)') == 1
    wrong = target / source.name
    wrong.write_text(text.replace('if (err)', 'if (!err)'))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], target / Path(pin['path']).name)
    changed = F.compile_source(item, wrong, target)
    try:
        F.L.validate(changed, qualified_bindings(changed), target / 'link')
    except ValueError as error:
        failure = error.args[0]
        assert isinstance(failure, dict) and failure['nativeBytes'] == 940 and failure['matchingBytes'] < 940
    else:
        raise ValueError('Wrong SDK callback error guard matched')
    body = (target / 'link/caller.bin').read_bytes()
    case = next(case for case in V.cases() if case['err'] == 1)
    try:
        V.invoke(body, case)
    except AssertionError:
        pass
    else:
        raise ValueError('Wrong SDK error guard passed the bounded no-call oracle')
    results.append(dict(kind='Invert the original FIFO transport error guard', rejectedByFullGenuineLinkComparison=True, rejectedByBoundedCallerOracle=True,
        comparison=failure, wrongSourceSha256=sha256(wrong), wrongObjectSha256=changed['objectSha256'], sourceOrCalleeCredit=0))
    altered = copy.deepcopy(item)
    check = next(check for check in altered['extraLayoutChecks'] if check['type'] == 'NativeStorage_020e5d80' and check.get('member') == 'field_0050')
    check['offset'] = 84
    try:
        F.layout_checks(altered, source, directory / 'wrong-layout')
    except ValueError as error:
        results.append(dict(kind='Wrong common-bank callback field offset84 instead of80', rejectedByPinnedNativeCompiler=True, reason=str(error), sourceOrCalleeCredit=0))
    else:
        raise ValueError('Wrong SDK common-static layout passed')
    bindings = qualified_bindings(row)
    name, binding = next((name, binding) for name, binding in bindings.items() if binding['kind'] == 'function')
    for label, changes in [('wrong-mode', dict(mode='thumb')), ('interior-entry', dict(address=hex(int(binding['address'], 0) + 4))), ('wrong-cpu', dict(processor='arm7')), ('wrong-module', dict(module='ov001'))]:
        altered_bindings = {key: dict(value) for key, value in bindings.items()}
        altered_bindings[name].update(changes)
        try:
            B.verify(row, altered_bindings, item['provenance'])
        except (ValueError, AssertionError) as error:
            results.append(dict(kind=label, rejected=True, reason=str(error), changedBinding=altered_bindings[name], sourceOrCalleeCredit=0))
        else:
            raise ValueError('Wrong SDK callback binding passed')
    changed_row = copy.deepcopy(row)
    relocation = next(rel for rel in changed_row['relocations'] if rel['type'] == 2 and rel['addend'])
    relocation['addend'] += 4
    try:
        B.verify(changed_row, bindings, item['provenance'])
    except ValueError as error:
        results.append(dict(kind='Changed original common-bank relocation addend by4', rejected=True, reason=str(error), sourceOrCalleeCredit=0))
    else:
        raise ValueError('Changed SDK resolved literal address passed')
    return results


def main():
    inputs = read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    metadata, image, unused = F.L.measured_module('main')
    assert metadata['sha256'] == inputs['moduleSha256'] and inputs['romSha256'] == configuration()['romSha256']
    assert len(inputs['entries']) == 1
    item = inputs['entries'][0]
    assert sha256(ROOT / item['provenance']['referenceSource']) == item['provenance']['referenceSourceSha256']
    source = F.checked_source(item)
    row = F.compile_source(item, source, WORK / 'source')
    assert row['compiledBytes'] == row['bytes'] == item['bytes'] == 940 and row['relocations'] == item['priorRelocations']
    row['sourceDependencies'] = item['sourceDependencies']
    bindings = qualified_bindings(row)
    assert bindings == item['qualifiedDependencies']
    namespace = B.verify(row, bindings, item['provenance'])
    real = F.L.validate(row, bindings, WORK / 'source/link')
    body = (WORK / 'source/link/caller.bin').read_bytes()
    assert body == image[0x11ac8:0x11ac8 + 940]
    layout = F.layout_checks(item, source, WORK / 'layout')
    negatives = controls(item, row, source, WORK / 'negative')
    model = V.prove(row, body)
    row.update(program='', realLink=real, manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'], matchingBytes=row['matchingBytes']),
        exactAfterDeclaredRelocation=real['exactCallerBytes'], matchingBytes=940, matchingBytesScope='Complete genuinely linked native extent', sourceLanguage='C',
        ordinaryCOnly=True, ordinaryCBytes=940, justifiedAssemblyBytes=0, justifiedAssemblyRanges=[], qualifiedDependencies=bindings, nativeSymbolEntries=bindings,
        sourceOnlyCompilerInput=True, originalObjectScaffolding=False, referenceFunction='WmReceiveFifo', actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],
        nativeAndSourceTerminationEntryStops=model['nativeAndSourceTerminationEntryStops'], calleeCodeOrSourceCredit=0, originalStorageSourceCredit=0)
    closure = code_closure([Path(__file__).name])
    limits = ['Complete ordinary C caller extent, original relocation records and addends, typed common-static storage and genuine MW link equality are proved.',
        'Bounded native/source caller cases use explicit supplied cache, finish, memory and user-callback contracts. Supplied callees and physical radio/cache/IRQ behavior receive zero execution/source credit.',
        'A terminate-entry stop is distinct from a return; no OS termination implementation or hardware execution is credited.',
        'Original extern storage, lexical/profiling reference objects and surrounding unselected SDK functions receive zero source credit. Shared acceptance remains coordinator owned.']
    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=metadata['sha256'], processor='arm9', module='main', program='', allPassed=True,
        matches=[row], matchedFunctions=1, matchedBytes=940, ordinaryCBytes=940, justifiedAssemblyBytes=0, sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'], nativeAndSourceTerminationEntryStops=model['nativeAndSourceTerminationEntryStops'],
        suppliedCalleeSourceOrExecutionCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__), generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))], typedLayoutChecks=[layout], negativeEvidence=negatives, boundedCallerModels=[model],
        namespaceProofs=[namespace], freshCompileObjectsAndLinkedReportsEveryRun=True, limits=limits)
    write_json(LANE / 'match.json', report)
    print(dict(functions=1, bytes=940, model=model, controls=len(negatives)), flush=True)


if __name__ == '__main__':
    main()
