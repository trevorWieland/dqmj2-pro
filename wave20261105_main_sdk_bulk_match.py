import copy
import hashlib
import shutil
from pathlib import Path
import wave20261105_main_sdk_bulk_compiler as C
import wave20261105_main_sdk_bulk_bindings as B
import wave20261105_main_sdk_bulk_fixture as V
import wave20261104_main_sdk_prefix_match as F
from project import ROOT, configuration, read_json, write_json, sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/first'
INPUT = LANE / 'inputs.json'
WORK = ROOT / 'work/w5sb/proof'
F.C = C


def negative(item, source, directory):
    if int(item['address'], 0) != 0x02012464:
        return F.negative_control(item, source, directory)
    directory.mkdir(parents=True, exist_ok=True)
    text = source.read_text()
    assert text.count('> 16 ') == 1 and text.count('= 16 ') == 1
    wrong = directory / source.name
    wrong.write_text(text.replace('> 16 ', '> 15 ').replace('= 16 ', '= 15 '))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], directory / Path(pin['path']).name)
    row = F.compile_source(item, wrong, directory)
    try:
        F.L.validate(row, qualified_bindings(row), directory / 'link')
    except ValueError as error:
        failure = error.args[0]
        assert isinstance(failure, dict) and failure['nativeBytes'] == item['bytes'] and failure['matchingBytes'] < item['bytes']
    else:
        raise ValueError('Wrong element-count source unexpectedly matched')
    body = (directory / 'link/caller.bin').read_bytes()
    case = next(case for case in V.cases(0x02012464) if case['count'] == 16 and case['length'] == 48)
    try:
        V.invoke(0x02012464, body, case)
    except AssertionError:
        pass
    else:
        raise ValueError('Wrong count clamp passed the measured 16-element oracle')
    return dict(kind='Change the ordinary C element-count clamp from16 to15', rejectedByFullGenuineLinkComparison=True,
        rejectedByBoundedNativeCountOracle=True, comparison=failure, wrongSourceSha256=sha256(wrong), wrongObjectSha256=row['objectSha256'], sourceOrCalleeCredit=0)


def binding_controls(row, directory):
    bindings = qualified_bindings(row)
    selected = next(((name, binding) for name, binding in bindings.items() if binding['kind'] == 'function'), None)
    if selected is None:
        return []
    name, binding = selected
    results = []
    for label, changes in [('wrong-mode', dict(mode='thumb')), ('interior-entry', dict(address=hex(int(binding['address'], 0) + 4))), ('wrong-cpu', dict(processor='arm7')), ('wrong-module', dict(module='ov001'))]:
        altered = {key: dict(value) for key, value in bindings.items()}
        altered[name].update(changes)
        try:
            B.verify(row, altered)
        except (ValueError, AssertionError) as error:
            results.append(dict(kind=label, symbol=name, changedBinding=altered[name], rejected=True, reason=str(error), sourceOrCalleeCredit=0))
        else:
            raise ValueError('Wrong SDK import namespace passed: ' + label)
    return results


def main():
    inputs = read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    metadata, image, unused = F.L.measured_module('main')
    assert metadata['sha256'] == inputs['moduleSha256'] and inputs['romSha256'] == configuration()['romSha256']
    matches, controls, layouts, models, namespaces = [], [], [], [], []
    for item in inputs['entries']:
        assert sha256(ROOT / item['provenance']['referenceSource']) == item['provenance']['referenceSourceSha256']
        source = F.checked_source(item)
        directory = WORK / format(int(item['address'], 0), '08x')
        row = F.compile_source(item, source, directory / 'source')
        assert row['relocations'] == item['priorRelocations'] and row['compiledBytes'] == item['bytes']
        row['sourceDependencies'] = item['sourceDependencies']
        bindings = qualified_bindings(row)
        assert bindings == item['qualifiedDependencies']
        namespaces.append(dict(address=item['address'], **B.verify(row, bindings)))
        proof = F.L.validate(row, bindings, directory / 'source/link')
        body = (directory / 'source/link/caller.bin').read_bytes()
        address = int(item['address'], 0)
        assert body == image[address - 0x02000000:address - 0x02000000 + item['bytes']]
        assert hashlib.sha256(body).hexdigest() == item['targetSha256']
        layouts.append(dict(address=item['address'], **F.layout_checks(item, source, directory / 'layout')))
        if address == 0x02012464:
            altered = copy.deepcopy(item)
            check = next(check for check in altered['extraLayoutChecks'] if check.get('member') == 'gameInfoLength')
            check['offset'] = 61
            try:
                F.layout_checks(altered, source, directory / 'wrong-layout')
            except ValueError as error:
                controls.append(dict(address=item['address'], kind='Wrong WMBssDesc gameInfoLength field offset61 instead of60', rejectedByPinnedNativeCompilerLayoutAssertions=True, reason=str(error), sourceOrCalleeCredit=0))
            else:
                raise ValueError('Incorrect published SDK/native structure layout passed')
        controls.append(dict(address=item['address'], **negative(item, source, directory / 'negative')))
        controls.extend(dict(address=item['address'], **control) for control in binding_controls(row, directory / 'binding'))
        model = V.prove(row, body)
        models.append(model)
        row.update(program='', realLink=proof, manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'], matchingBytes=row['matchingBytes']),
            exactAfterDeclaredRelocation=proof['exactCallerBytes'], matchingBytes=item['bytes'], matchingBytesScope='Complete genuinely linked native extent',
            sourceLanguage='C', ordinaryCOnly=True, ordinaryCBytes=item['bytes'], justifiedAssemblyBytes=0, justifiedAssemblyRanges=[], qualifiedDependencies=bindings,
            nativeSymbolEntries=bindings, sourceOnlyCompilerInput=True, originalObjectScaffolding=False, referenceFunction=item['referenceFunction'],
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'], calleeCodeOrSourceCredit=0, originalStorageSourceCredit=0)
        matches.append(row)
        print('proved SDK C', item['address'], item['bytes'], item['referenceFunction'], flush=True)
    assert len(matches) == 11 and sum(row['bytes'] for row in matches) == 2344
    closure = code_closure([Path(__file__).name])
    limits = ['Complete ordinary C native extents, original object relocations and genuine pinned MW link equality are proved.',
        'Bounded element parsing, TGID sequencing and WM forwarding use explicitly supplied RTC/initializer contracts; no native callee, physical radio, time, multiboot protocol or game execution is credited.',
        'The other eight exact caller bodies receive no execution credit; original extern storage and compiler helper bodies receive zero source credit.',
        'Public SDK source is comparative evidence, not proof of the original game SDK revision or authorship. Shared acceptance remains coordinator owned.']
    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=metadata['sha256'], processor='arm9', module='main', program='', allPassed=True,
        matches=matches, matchedFunctions=11, matchedBytes=2344, ordinaryCBytes=2344, justifiedAssemblyBytes=0,
        actualNativeAndSourceCallerReturns=sum(row['actualNativeAndSourceCallerReturns'] for row in models), suppliedCalleeSourceOrExecutionCredit=0,
        sourceOnlyCompilerInputs=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure], replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))],
        typedLayoutChecks=layouts, negativeEvidence=controls, boundedCallerModels=models, namespaceProofs=namespaces,
        freshCompileObjectsAndLinkedReportsEveryRun=True, limits=limits)
    write_json(LANE / 'match.json', report)
    print(dict(functions=11, bytes=2344, returns=report['actualNativeAndSourceCallerReturns'], controls=len(controls)), flush=True)


if __name__ == '__main__':
    main()
