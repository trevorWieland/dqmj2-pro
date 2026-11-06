import copy
import re
import shutil
from pathlib import Path
import wave20261105_main_record_next_compiler as C
import wave20261105_main_record_next_first_fixture as V
import wave20261105_main_record_next_first_abi as A
import wave20261105_main_sdk_bulk_bindings as B
import wave20261104_main_sdk_prefix_match as F
from project import ROOT, configuration, read_json, write_json, sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-record-next/first'
INPUT = LANE / 'inputs-v2.json'
WORK = ROOT / 'work/w5rn/first-proof'


def compile_source(item,source,directory):
    C.FLAGS = item['flags'][:]
    C.WORK = directory / 'compile'
    rows,unused = C.compare(source,'main','2','off',compiler=ROOT/item['compilerPath'])
    assert len(rows) == 1 and not rows[0].get('compileFailed'),rows
    row = rows[0]
    assert row['address'] == item['address'] and row['bytes'] == item['bytes'] and row['targetSha256'] == item['targetSha256']
    assert row['compilerFlags'] == item['flags']
    return row


def negatives(item,row,source,native,directory):
    directory.mkdir(parents=True,exist_ok=True)
    changes = {
        0x020cc220:('case 2:','case 4:','Handle raw phase4 while dropping phase2'),
        0x020cadb4:('native_data_021d65f0,3,1','native_data_021d65f0,2,1','Change the first explicit append input word3 to2'),
        0x020cba50:('field00d1.bit3 = -1','field00d1.bit2 = -1','Set bit2 rather than the measured bit3'),
        0x020cba74:('field00d1.bit1 = -1','field00d1.bit0 = -1','Publish bit0 rather than the measured bit1')}
    before,after,meaning = changes[int(item['address'],0)]
    text = source.read_text()
    assert text.count(before) == 1
    wrong = directory / source.name
    wrong.write_text(text.replace(before,after))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT/pin['path'],directory/Path(pin['path']).name)
    bad = compile_source(item,wrong,directory)
    try:
        F.L.validate(bad,qualified_bindings(bad),directory/'link')
    except ValueError as error:
        failure = error.args[0]
        assert isinstance(failure,dict) and failure['nativeBytes'] == item['bytes'] and failure['matchingBytes'] < item['bytes']
    else:
        raise ValueError('Altered raw-state C source unexpectedly matched')
    try:
        V.prove(int(item['address'],0),native,(directory/'link/caller.bin').read_bytes())
    except AssertionError:
        pass
    else:
        raise ValueError('Altered raw-state C source passed its independent oracle')
    result = [dict(kind='ABI-preserving ordinary C change',meaning=meaning,rejectedByCompleteGenuineLink=True,rejectedByIndependentCallerOracle=True,
        wrongSourceSha256=sha256(wrong),wrongObjectSha256=bad['objectSha256'],comparison=failure,sourceOrExecutionCredit=0)]
    result.extend(F.binding_controls(row,directory/'bindings'))
    bindings = qualified_bindings(row)
    name = next(iter(bindings))
    altered = {key:dict(value) for key,value in bindings.items()}
    altered[name]['module'] = 'ov001'
    try:
        B.verify(row,altered)
    except (AssertionError,ValueError) as error:
        result.append(dict(kind='wrong-original-module',rejected=True,reason=str(error),sourceOrExecutionCredit=0))
    else:
        raise ValueError('Wrong module passed original relocation witnesses')
    wrong_layout = copy.deepcopy(item)
    wrong_layout['extraLayoutChecks'][0]['bytes'] = 4
    try:
        F.layout_checks(wrong_layout,source,directory/'wrong-layout')
    except ValueError as error:
        result.append(dict(kind='NativeBits incorrectly widened from1byte to4bytes',rejectedByPinnedCompiler=True,reason=str(error),sourceOrExecutionCredit=0))
    else:
        raise ValueError('Wrong native bitfield extent passed')
    assert sha256(source) == item['sourceSha256']
    return result


def main():
    inputs = read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT/pin['path']) == pin['sha256'],pin['path']
    metadata,image,unused = F.L.measured_module('main')
    assert inputs['romSha256'] == configuration()['romSha256'] and metadata['sha256'] == inputs['moduleSha256']
    abi = A.verify(ROOT/inputs['entries'][0]['sourceDependencies'][0]['path'])
    matches,models,controls,layouts = [],[],[],[]
    for item in inputs['entries']:
        source = F.checked_source(item)
        directory = WORK / format(int(item['address'],0),'08x')
        row = compile_source(item,source,directory/'source')
        assert row['compiledBytes'] == item['bytes'] and row['relocations'] == item['priorRelocations']
        row['sourceDependencies'] = item['sourceDependencies']
        bindings = qualified_bindings(row)
        assert bindings == item['qualifiedDependencies']
        namespace = B.verify(row,bindings)
        real = F.L.validate(row,bindings,directory/'source/link')
        linked = (directory/'source/link/caller.bin').read_bytes()
        start = int(item['address'],0)-0x02000000
        native = image[start:start+item['bytes']]
        assert linked == native
        header = ''.join((ROOT/pin['path']).read_text() for pin in item['sourceDependencies'])
        for name,binding in bindings.items():
            if binding['kind'] == 'function':
                signature = re.search(r'\b'+name+r'\s*\(([^;{}]*)\)\s*;',header)
                assert signature and signature[1].strip(),'Missing explicit native caller word ABI'
        layout = F.layout_checks(item,source,directory/'layout')
        model = V.prove(int(item['address'],0),native,linked)
        negative = negatives(item,row,source,native,directory/'negative')
        row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=item['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],
            realLink=real,originalCallsiteWitness=namespace,qualifiedDependencies=bindings,nativeSymbolEntries=bindings,
            manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),
            exactAfterDeclaredRelocation=real['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuine MW-linked native caller extent',
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],
            nativeCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract=item['boundaryReturnContract'])
        matches.append(row)
        models.append(model)
        controls.extend(dict(address=item['address'],**control) for control in negative)
        layouts.append(dict(address=item['address'],**layout))
        print('proved record C',item['address'],item['bytes'],model['cases'],flush=True)
    assert len(matches) == 4 and sum(row['bytes'] for row in matches) == 524
    closure = code_closure([Path(__file__).name])
    limits = ['Complete caller source spans, original relocation identities, ARM main entries and genuine MW links are proved; shared acceptance remains pending.',
        'Signed one-bit fields express the measured byte/bit positions under the pinned ARM compiler. Layout checks and native raw-byte models qualify this target-specific representation.',
        'The36-byte setter has a void source boundary. Its observed scratch GPR values are compared without claiming a semantic return value.',
        'Native/source caller execution uses supplied append, index, callback and finish contracts. No corresponding native callee bodies or hardware/game systems execute.',
        'Raw identifiers, phases, counters and field offsets carry no inferred save/UI/game-mechanics meaning. Original globals and retained ROM data receive zero source credit.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=4,matchedBytes=524,ordinaryCBytes=524,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layouts,negativeEvidence=controls,originalInterfaceProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__ == '__main__':
    main()
