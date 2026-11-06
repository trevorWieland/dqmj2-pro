import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import wave20261104_main_sdk_tail_compiler as C
import link_runtime_unit as L
from project import ROOT, configuration, read_json, write_json, sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-sdk-residual/tail'
WORK = ROOT / 'work/w4ms/tproof'
INPUT = LANE / 'inputs.json'


def checked_source(item):
    source = ROOT / item['source']
    pins = [dict(path=item['source'], sha256=item['sourceSha256']), *item['sourceDependencies']]
    for pin in pins:
        path = ROOT / pin['path']
        text = path.read_text(encoding='utf-8')
        if sha256(path) != pin['sha256'] or len(text.splitlines()) > 500 or '/*' in text or '//' in text:
            raise ValueError('Frozen readable source/header changed: ' + pin['path'])
        if re.search(r'\b(?:asm|__asm|__asm__|J2pUnknownVaList|va_list|size_t)\b', text):
            raise ValueError('Nonordinary or provisional source token')
        if path.suffix == '.h' and '#include' in text:
            raise ValueError('Packet header has undeclared transitive include')
    if sha256(ROOT / item['compilerPath']) != item['compilerSha256']:
        raise ValueError('Pinned source compiler changed')
    if any(flag.startswith('-D') or flag == '-i' for flag in item['flags']):
        raise ValueError('Provisional compiler inputs are forbidden')
    return source


def compile_source(item, source, directory):
    C.FLAGS = list(item['flags'])
    C.WORK = directory / 'compile'
    rows, unused = C.compare(source, 'main', C.FLAGS[0][2:], C.FLAGS[C.FLAGS.index('-inline') + 1], compiler=ROOT / item['compilerPath'])
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Fresh SDK compilation failed', rows))
    row = rows[0]
    if row['address'] != item['address'] or row['bytes'] != item['bytes'] or row['targetSha256'] != item['targetSha256']:
        raise ValueError('Complete native SDK identity changed')
    if row['compilerFlags'] != item['flags']:
        raise ValueError('Native compiler profile changed')
    if sha256(ROOT / row['object']) != row['objectSha256']:
        raise ValueError('Fresh SDK object differs from declared hash')
    return row


def layout_checks(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    text = ''.join((ROOT / p['path']).read_text() for p in item['sourceDependencies'])
    declarations = []
    checked = []
    for index, layout in enumerate(item.get('extraLayoutChecks', [])):
        expression = 'sizeof(' + layout['type'] + ') == ' + str(layout['bytes']) if layout.get('bytes') is not None else '1'
        if layout.get('member'):
            expression += ' && (unsigned int)&((' + layout['type'] + ' *)0)->' + layout['member'] + ' == ' + str(layout['offset'])
        declarations.append('typedef char NativeExtra_' + str(index) + '[(' + expression + ') ? 1 : -1];')
        checked.append(dict(kind='measured-parameter-structure', **layout))
    for layout in item['provenance']['typedStorageLayouts']:
        base = int(layout['nativeBase'], 0)
        typename = 'NativeStorage_' + format(base, '08x')
        if typename not in text:
            continue
        for member in layout['members']:
            field = member['field']
            name = 'LayoutCheck_' + format(base, '08x') + '_' + field
            declaration = 'typedef char ' + name + '[(sizeof(((' + typename + ' *)0)->' + field + ') == ' + str(member['bytes']) + ' && (unsigned int)&((' + typename + ' *)0)->' + field + ' == ' + str(member['offset']) + ') ? 1 : -1];'
            declarations.append(declaration)
            checked.append(dict(nativeBase=hex(base), field=field, offset=member['offset'], bytes=member['bytes']))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], directory / Path(pin['path']).name)
    check = directory / 'layout-check.c'
    check.write_text(''.join('#include "' + Path(pin['path']).name + '"\n' for pin in item['sourceDependencies']) + '\n'.join(declarations) + '\n')
    output = directory / 'layout-check.o'
    process = subprocess.run([str(ROOT / item['compilerPath']), *item['flags'], '-c', str(check), '-o', str(output)], cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('SDK native typed layout check failed', process.stdout, process.stderr))
    return dict(compilerChecks=len(checked), checkedMembers=checked, checkSourceSha256=sha256(check), checkObjectSha256=sha256(output), initializedDataOrCodeSourceCredit=0)


def negative_control(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    original = source.read_text(encoding='utf-8')
    opening = original.index('{')
    signature = re.search(r'(?m)^([A-Za-z_][A-Za-z_0-9 \t*]*?)\s+native_main_[0-9a-f]+\s*\(', original[:opening])
    if not signature:
        raise ValueError('SDK negative return type could not be identified')
    return_type = signature[1].strip()
    result = 'return;' if return_type == 'void' else return_type + ' negative_value = {0};\n    return negative_value;'
    wrong = directory / source.name
    wrong.write_text(original[:opening] + '{\n    ' + result + '\n}\n')
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], directory / Path(pin['path']).name)
    row = compile_source(item, wrong, directory)
    try:
        L.validate(row, qualified_bindings(row), directory / 'link')
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, dict) or failure.get('caller') != row['name'] or failure.get('nativeBytes') != item['bytes']:
            raise
        return dict(kind='Complete ordinary C zero-value return substitution preserving the declared return ABI', rejectedByFullGenuineLinkComparison=True, caller=row['name'], wrongSourceSha256=sha256(wrong), wrongObjectSha256=row['objectSha256'], comparison=failure, originalSourceUnchanged=sha256(source) == item['sourceSha256'], sourceOrBehaviorCredit=0)
    raise ValueError('Whole-C SDK negative control unexpectedly matched')



def data_binding_control(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    wrong = directory / source.name
    text = source.read_text()
    if 'native_data_main_020f1fa0' not in text:
        raise ValueError('Measured separate array symbol absent')
    wrong.write_text(text.replace('native_data_main_020f1fa0', 'native_data_main_020f1fa4'))
    for pin in item['sourceDependencies']:
        content = (ROOT / pin['path']).read_text().replace('native_data_main_020f1fa0', 'native_data_main_020f1fa4')
        (directory / Path(pin['path']).name).write_text(content)
    row = compile_source(item, wrong, directory)
    try:
        L.validate(row, qualified_bindings(row), directory / 'link')
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, dict) or failure.get('nativeBytes') != 224 or failure.get('matchingBytes') != 223:
            raise
        return dict(kind='Wrong independently named data-array identity advanced by four bytes',
            rejectedByFullGenuineLinkComparison=True, comparison=failure, wrongSourceSha256=sha256(wrong),
            wrongObjectSha256=row['objectSha256'], sourceOrBehaviorCredit=0)
    raise ValueError('Wrong array data identity unexpectedly matched')


def main():
    if sys.version_info[:3] != (3, 13, 5):
        raise ValueError('Pinned Python runtime changed')
    inputs = read_json(INPUT)
    for pin in inputs["files"]:
        if sha256(ROOT / pin["path"]) != pin["sha256"]:
            raise ValueError("Mandatory native runtime input changed: " + pin["path"])
    upstream = (ROOT / 'match_runtime.py').read_text().split('\ndef execute(', 1)[0]
    old = 'r"_(?:[us](?:32|64)|f|d)_\\w+"'
    new = 'r"(?:_(?:[us](?:32|64)|f|d)_\\w+|_ll_(?:sdiv|udiv|mod|umod))"'
    adapter = ROOT / 'wave20261104_main_sdk_tail_compiler.py'
    if upstream.count(old) != 1 or adapter.read_text() != upstream.replace(old, new):
        raise ValueError('Private compiler adapter differs beyond explicit helper-name recognition')
    metadata, image, unused = L.measured_module('main')
    if inputs['romSha256'] != configuration()['romSha256'] or inputs['moduleSha256'] != metadata['sha256']:
        raise ValueError('SDK packet original ROM/module identity changed')
    for pin in inputs['immutableNativeConfiguration']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('SDK native configuration changed')
    matches, controls, layouts = [], [], []
    for item in inputs['entries']:
        source = checked_source(item)
        directory = WORK / format(int(item['address'], 0), '08x')
        row = compile_source(item, source, directory / 'source')
        if row['relocations'] != item['priorRelocations'] or row['compiledBytes'] != item['bytes']:
            raise ValueError('Complete SDK native extent/relocation structure changed')
        row['sourceDependencies'] = item['sourceDependencies']
        bindings = qualified_bindings(row)
        if bindings != item['qualifiedDependencies']:
            raise ValueError('SDK function/data binding identities changed')
        proof = L.validate(row, bindings, directory / 'source/link')
        body = (directory / 'source/link/caller.bin').read_bytes()
        address = int(item['address'], 0)
        native = image[address - 0x02000000:address - 0x02000000 + item['bytes']]
        if body != native or hashlib.sha256(body).hexdigest() != item['targetSha256']:
            raise ValueError('Full genuine linked SDK caller differs')
        layouts.append(dict(address=item['address'], **layout_checks(item, source, directory / 'layout')))
        controls.append(dict(address=item['address'], **negative_control(item, source, directory / 'negative')))
        row.update(program='', realLink=proof, manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'], matchingBytes=row['matchingBytes']), exactAfterDeclaredRelocation=proof['exactCallerBytes'], exactAfterDeclaredRelocationBasis='Complete native caller extent, unchanged compiler object relocations/addends and genuine pinned MW linker equality', matchingBytes=item['bytes'], matchingBytesScope='Complete genuinely linked caller extent', sourceLanguage='C', ordinaryCOnly=True, sourceOnlyCompilerInput=True, originalObjectScaffolding=False, qualifiedDependencies=bindings, nativeSymbolEntries=bindings, ordinaryCBytes=item['bytes'], justifiedAssemblyBytes=0, justifiedAssemblyRanges=[], referenceFunction=item['referenceFunction'], actualNativeFunctionReturns=0, calleeCodeOrSourceCredit=0, originalStorageSourceCredit=0)
        controls.append(dict(address=item['address'], **data_binding_control(item, source, directory / 'binding')))
        matches.append(row)
        print('proved', item['address'], item['bytes'], item['referenceFunction'], flush=True)
    closure = code_closure([Path(__file__).name])
    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=metadata['sha256'], processor='arm9', module='main', program='', allPassed=True, matches=matches, matchedFunctions=len(matches), matchedBytes=sum(r['bytes'] for r in matches), sourceCreditPendingIntegrator=sum(r['bytes'] for r in matches), actualNativeFunctionReturns=0, sourceOnlyCompilerInputs=True, originalStorageSourceCredit=0, nativeCalleeSourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__), generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure], replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))], typedLayoutChecks=layouts, negativeEvidence=controls, freshCompileObjectsAndLinkedReportsEveryRun=True, limits=['Complete ordinary C units, configured extent, original relocation types/addends/encoded instructions and genuine pinned MW linking are proved.', 'No fixture, physical hardware, multiboot protocol, timing or scene execution credit is claimed; actual native returns remain zero.', 'Typed extern storage layouts and anonymous string addresses retain original storage without credit. Local and external callees receive zero source credit.', 'The pinned public reconstructed NitroSDK source is comparative evidence; it does not establish this game SDK revision or original authorship.', 'Shared module/ROM regression and acceptance are coordinator owned.'])
    report['compilerIntrinsicAdapter'] = dict(baseMatcherSha256=sha256(ROOT / 'match_runtime.py'), privateAdapterSha256=sha256(adapter), onlyDifference='Explicit _ll_sdiv/_ll_udiv/_ll_mod/_ll_umod name recognition; genuine native boundary/link gates unchanged', sourceObjectsAndRelocationsUnchanged=True, alternateEntryGateUnchanged=True)
    write_json(LANE / 'match.json', report)
    print(dict(functions=len(matches), bytes=report['matchedBytes'], nativeReturns=0, wholeCNegativesRejected=len(controls), nativeLayoutChecks=sum(r['compilerChecks'] for r in layouts)), flush=True)


if __name__ == '__main__':
    main()
