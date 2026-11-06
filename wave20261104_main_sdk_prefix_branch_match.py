import hashlib
import re
import shutil
from pathlib import Path
import wave20261104_main_sdk_prefix_match as F
from project import ROOT,configuration,read_json,write_json,sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-sdk-prefix/branch-following'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w4sp/b/p'


def binding_controls(row,directory):
    bindings=qualified_bindings(row)
    selected=next(((name,b) for name,b in bindings.items() if b['kind']=='function'),None)
    if selected is None:return []
    name,binding=selected;results=[]
    flip='arm' if binding['mode']=='thumb' else 'thumb'
    for label,changes in [('wrong-mode',dict(mode=flip)),('interior-entry',dict(address=hex(int(binding['address'],0)+4))),('wrong-cpu',dict(processor='arm7'))]:
        altered={key:dict(value) for key,value in bindings.items()};altered[name].update(changes)
        try:F.L.validate(row,altered,directory/label)
        except (ValueError,AssertionError) as error:results.append(dict(kind=label,symbol=name,originalBinding=binding,changedBinding=altered[name],rejected=True,reason=str(error),sourceOrBehaviorCredit=0))
        else:raise ValueError('Altered SDK binding unexpectedly passed: '+label)
    return results


def negative_control(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    original = source.read_text(encoding='utf-8')
    opening = original.index('{')
    signature = re.search(r'(?m)^\s*([A-Za-z_][A-Za-z_0-9 \t*]*?)\s*native_main_[0-9a-f]+\s*\(', re.sub(r'__declspec\([^)]*\)', '', original[:opening]))
    if not signature:
        raise ValueError('SDK negative return type could not be identified')
    return_type = signature[1].strip()
    result = 'return;' if return_type == 'void' else return_type + ' negative_value = {0};\n    return negative_value;'
    wrong = directory / source.name
    wrong.write_text(original[:opening] + '{\n    ' + result + '\n}\n')
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT / pin['path'], directory / Path(pin['path']).name)
    row = F.compile_source(item, wrong, directory)
    try:
        F.L.validate(row, qualified_bindings(row), directory / 'link')
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, dict) or failure.get('caller') != row['name'] or failure.get('nativeBytes') != item['bytes']:
            raise
        return dict(kind='Complete ordinary C zero-value return substitution preserving the declared return ABI', rejectedByFullGenuineLinkComparison=True, caller=row['name'], wrongSourceSha256=sha256(wrong), wrongObjectSha256=row['objectSha256'], comparison=failure, originalSourceUnchanged=sha256(source) == item['sourceSha256'], sourceOrBehaviorCredit=0)
    raise ValueError('Whole-C SDK negative control unexpectedly matched')


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    metadata,image,unused=F.L.measured_module('main')
    assert metadata['sha256']==inputs['moduleSha256'] and inputs['romSha256']==configuration()['romSha256']
    matches,controls,layouts=[],[],[]
    for item in inputs['entries']:
        source=F.checked_source(item);directory=WORK/format(int(item['address'],0),'08x')
        row=F.compile_source(item,source,directory/'source');assert row['relocations']==item['priorRelocations'] and row['compiledBytes']==item['bytes']
        row['sourceDependencies']=item['sourceDependencies'];bindings=qualified_bindings(row);assert bindings==item['qualifiedDependencies']
        proof=F.L.validate(row,bindings,directory/'source/link');address=int(item['address'],0);body=(directory/'source/link/caller.bin').read_bytes();assert body==image[address-0x02000000:address-0x02000000+item['bytes']]
        layouts.append(dict(address=item['address'],**F.layout_checks(item,source,directory/'layout')))
        controls.append(dict(address=item['address'],**negative_control(item,source,directory/'negative')))
        controls.extend(dict(address=item['address'],**value) for value in binding_controls(row,directory/'binding'))
        row.update(program='',realLink=proof,manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),exactAfterDeclaredRelocation=proof['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuinely linked native extent',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=item['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],qualifiedDependencies=bindings,nativeSymbolEntries=bindings,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,referenceFunction=item['referenceFunction'],actualNativeFunctionReturns=0,calleeCodeOrSourceCredit=0)
        matches.append(row);print('proved ordinary SDK C',item['address'],item['bytes'],item['referenceFunction'],flush=True)
    assert len(matches)==11 and sum(r['bytes'] for r in matches)==364
    closure=code_closure([Path(__file__).name])
    report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],processor='arm9',module='main',program='',allPassed=True,matches=matches,matchedFunctions=11,matchedBytes=364,ordinaryCBytes=364,justifiedAssemblyBytes=0,actualNativeFunctionReturns=0,hardwareOrCalleeExecutionCredit=0,sourceOnlyCompilerInputs=True,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],typedLayoutChecks=layouts,negativeEvidence=controls,freshCompileObjectsAndLinkedReportsEveryRun=True,limits=['Complete ordinary C native extents, original object relocations and genuine pinned MW link equality are proved, including real ARM/Thumb function target modes.','Exploratory opcode masks earn no credit; raw manual BL-versus-BLX scorer mismatches are preserved separately.','No physical hardware, wait/IRQ behavior, native callee or game execution credit is claimed.','The public SDK source is comparative evidence and does not establish this modified game SDK revision or original authorship.','Shared module/ROM acceptance remains coordinator owned.'])
    write_json(LANE/'match.json',report);print(dict(functions=11,bytes=364,controls=len(controls)),flush=True)


if __name__=='__main__':main()
