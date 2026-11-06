import copy
import shutil
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import wave20261105_main_sdk_bulk_compiler as C
import wave20261105_main_sdk_bulk_varargs_abi as A
import wave20261105_main_sdk_bulk_varargs_bindings as B
import wave20261105_main_sdk_bulk_varargs_fixture as V
import wave20261105_main_sdk_bulk_varargs_helper_abi as H
import wave20261105_main_sdk_bulk_varargs_weak as W
import wave20261104_main_sdk_prefix_match as F
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/varargs/packet'
INPUT = LANE / 'inputs.json'
WORK = ROOT / 'work/w5sb/va-proof'
F.C = C


def negative(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    address = int(item['address'], 0)
    body = source.read_text()
    if address == 0x0201A670:
        before, after = '(str.base + len)[-1]', '(str.base + len)[0]'
    elif address == 0x0201A5C4:
        before, after = 'p->cur[i] = c;', 'p->cur[i] = c + 1;'
    elif address == 0x0201A618:
        before, after = 'p->cur[i] = s[i];', 'p->cur[i] = s[i + 1];'
    else:
        before = after = None
    if before:
        assert body.count(before) == 1
        body = body.replace(before, after)
    wrong = directory / source.name
    wrong.write_text(body)
    for pin in item['sourceDependencies']:
        text = (ROOT / pin['path']).read_text()
        if not before and Path(pin['path']).name == 'msl_arm_varargs.h':
            assert text.count(' + 3U) & ~3U') == 1
            text = text.replace(' + 3U) & ~3U', ' + 7U) & ~7U')
        (directory / Path(pin['path']).name).write_text(text)
    row = F.compile_source(item, wrong, directory)
    try:
        F.L.validate(row, qualified_bindings(row), directory / 'link')
    except ValueError as error:
        failure = error.args[0]
        assert isinstance(failure, dict) and failure['nativeBytes'] == item['bytes'] and failure['matchingBytes'] < item['bytes']
    else:
        raise ValueError('Wrong variadic/formatter C source matched')
    linked = (directory / 'link/caller.bin').read_bytes()
    cases = V.cases(address)
    case = next(case for case in cases if case['kind'] == 'send' and case['available'] and len(case['values']) == 3) if address == 0x020118A4 else \
        next(case for case in cases if case['kind'] == 'state' and case['initializedResult'] == 0 and case['now'] == 0 and len(case['values']) == 2) if address == 0x02011A34 else \
        next(case for case in cases if case['capacity'] == 1 and (case['kind'] == 'format' and case['format'] == b'abc' or case['kind'] != 'format' and case['count'] == 1))
    try:
        V.invoke(address, linked, case)
    except AssertionError:
        pass
    else:
        raise ValueError('Wrong C source passed the bounded argument/data oracle')
    return dict(kind='Wrong8-byte variadic slot stride' if before is None else 'Changed measured formatter data/terminator expression',
        rejectedByFullGenuineLinkComparison=True, rejectedByBoundedCallerOracle=True, comparison=failure, wrongSourceSha256=sha256(wrong), wrongObjectSha256=row['objectSha256'], sourceOrCalleeCredit=0)


def namespace_controls(item, row):
    bindings = qualified_bindings(row)
    selected = next(((name, binding) for name, binding in bindings.items() if binding['kind'] == 'function'), None)
    if selected is None:
        return []
    name, binding = selected
    controls = []
    for label, changes in [('wrong-mode', dict(mode='thumb')), ('interior-entry', dict(address=hex(int(binding['address'], 0) + 4))), ('wrong-cpu', dict(processor='arm7')), ('wrong-module', dict(module='ov001'))]:
        altered = {key: dict(value) for key, value in bindings.items()}
        altered[name].update(changes)
        try:
            B.verify(row, altered, item['provenance'])
        except (ValueError, AssertionError) as error:
            controls.append(dict(kind=label, rejected=True, reason=str(error), changedBinding=altered[name], sourceOrCalleeCredit=0))
        else:
            raise ValueError('Wrong variadic source namespace passed')
    return controls


def main():
    inputs = read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    macro_header = A.verify_abi(inputs)
    metadata, image, unused = F.L.measured_module('main')
    assert metadata['sha256'] == inputs['moduleSha256'] and configuration()['romSha256'] == inputs['romSha256']
    matches, layouts, negatives, models, namespaces, weak = [], [], [], [], [], []
    for item in inputs['entries']:
        source = A.checked_source(item, macro_header)
        directory = WORK / format(int(item['address'], 0), '08x')
        row = F.compile_source(item, source, directory / 'source')
        assert row['compiledBytes'] == row['bytes'] == item['bytes'] and row['relocations'] == item['priorRelocations']
        row['sourceDependencies'] = item['sourceDependencies']
        bindings = qualified_bindings(row)
        assert bindings == item['qualifiedDependencies']
        namespaces.append(dict(address=item['address'], **B.verify(row, bindings, item['provenance'])))
        real = F.L.validate(row, bindings, directory / 'source/link')
        body = (directory / 'source/link/caller.bin').read_bytes()
        start = int(item['address'], 0) - 0x02000000
        assert body == image[start:start + item['bytes']]
        layouts.append(dict(address=item['address'], **F.layout_checks(item, source, directory / 'layout')))
        if int(item['address'], 0) == 0x020118A4:
            wrong_layout = copy.deepcopy(item)
            next(check for check in wrong_layout['extraLayoutChecks'] if check['type'] == 'va_list')['bytes'] = 8
            try:
                F.layout_checks(wrong_layout, source, directory / 'wrong-va-layout')
            except ValueError as error:
                negatives.append(dict(address=item['address'], kind='Wrong8-byte va_list representation instead of the published4-byte pointer', rejectedByPinnedNativeCompilerLayoutAssertions=True, reason=str(error), sourceOrCalleeCredit=0))
            else:
                raise ValueError('Wrong variadic layout passed')
        negatives.append(dict(address=item['address'], **negative(item, source, directory / 'negative')))
        negatives.extend(dict(address=item['address'], **control) for control in namespace_controls(item, row))
        model = V.prove(row, body)
        models.append(model)
        if int(item['address'], 0) == 0x0201A670:
            weak.append(W.prove(item, row, directory / 'source/link'))
            target = directory / 'strong-export-control'
            target.mkdir(parents=True, exist_ok=True)
            strong_source = target / source.name
            original_text = source.read_text()
            assert original_text.count('__declspec(weak)') == 1
            strong_source.write_text(original_text.replace('__declspec(weak)', ''))
            for pin in item['sourceDependencies']:
                shutil.copyfile(ROOT / pin['path'], target / Path(pin['path']).name)
            strong_row = F.compile_source(item, strong_source, target)
            assert strong_row['relocations'] == row['relocations']
            strong_link = F.L.validate(strong_row, qualified_bindings(strong_row), target / 'link')
            strong_symbol, unused = W.inspect(ROOT / strong_row['object'], strong_row['name'])
            assert strong_symbol['binding'] == 1 and strong_symbol['type'] == 2 and strong_link['exactCallerBytes']
            try:
                W.prove(item, strong_row, target / 'link')
            except AssertionError:
                negatives.append(dict(address=item['address'], kind='Remove the actual published SDK weak export attribute while preserving every body byte and object relocation',
                    wrongCompilerBinding=1, requiredCompilerBinding=14, bodyAndGenuineLinkStillExact=True, rejectedByDeclaredWeakSourceExportContract=True,
                    wrongSourceSha256=sha256(strong_source), wrongObjectSha256=strong_row['objectSha256'], sourceOrCalleeCredit=0))
            else:
                raise ValueError('Strong source export passed the required SDK weak interface')
        row.update(program='', realLink=real, manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'], matchingBytes=row['matchingBytes']),
            exactAfterDeclaredRelocation=real['exactCallerBytes'], matchingBytes=item['bytes'], matchingBytesScope='Complete genuinely linked native extent', sourceLanguage='C',
            ordinaryCOnly=True, ordinaryCBytes=item['bytes'], justifiedAssemblyBytes=0, justifiedAssemblyRanges=[], qualifiedDependencies=bindings, nativeSymbolEntries=bindings,
            sourceOnlyCompilerInput=True, originalObjectScaffolding=False, referenceFunction=item['referenceFunction'], actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],
            calleeCodeOrSourceCredit=0, originalStorageSourceCredit=0)
        matches.append(row)
        print('proved ARM ABI C', row['address'], row['bytes'], flush=True)
    assert len(matches) == 5 and sum(row['bytes'] for row in matches) == 2792
    helper = H.prove()
    closure = code_closure([Path(__file__).name])
    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=metadata['sha256'], processor='arm9', module='main', program='', allPassed=True,
        matches=matches, matchedFunctions=5, matchedBytes=2792, ordinaryCBytes=2792, justifiedAssemblyBytes=0, sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models), sourceOrFunctionCreditForSuppliedCallees=0,
        generator=Path(__file__).name, generatorSha256=sha256(__file__), generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))], typedLayoutChecks=layouts, negativeEvidence=negatives,
        boundedCallerModels=models, namespaceProofs=namespaces, actualRetainedHelperAbiOnly=helper, weakSourceExportEvidence=weak, freshCompileObjectsAndLinkedReportsEveryRun=True,
        limits=['Complete ordinary C caller extents, original relocations/addends, original namespace witnesses and genuine pinned MW links are proved.',
            'Published ARM MSL char-pointer/four-byte variadic slots are separately pinned and qualified; earlier unknown-VA guards remain unchanged.',
            'Bounded models cover caller-visible arguments, data and return values under supplied SDK/queue/cache/string/division contracts; supplied native callee/hardware/radio/queue execution is not credited.',
            'The36 retained original division-helper ABI probes receive zero source/function coverage credit and are excluded from caller-return totals.',
            'The tiny formatter preserves its measured limited grammar, including literal treatment of unsupported# flags. Shared acceptance and generated canonical weak-scope preservation remain coordinator owned.'])
    write_json(LANE / 'match.json', report)
    print(dict(functions=5, bytes=2792, returns=report['actualNativeAndSourceCallerReturns'], controls=len(negatives), nativeHelperAbiOnly=36), flush=True)


if __name__ == '__main__':
    main()
