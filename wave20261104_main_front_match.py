import re
import shutil
from pathlib import Path
import wave20261104_main_front_compiler as C
import wave20261104_main_front_fixture as V
import wave20261104_main_sdk_prefix_match as F
import wave20261104_main_tail_bindings as B
from project import ROOT,configuration,read_json,write_json,sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-front/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w4af/p'


def compile_source(item,source,directory):
    C.FLAGS=item['flags'][:]
    C.WORK=directory/'compile'
    rows,unused=C.compare(source,'main','2','off',compiler=ROOT/item['compilerPath'])
    assert len(rows)==1 and not rows[0].get('compileFailed'),rows
    row=rows[0]
    assert row['address']==item['address'] and row['bytes']==item['bytes'] and row['targetSha256']==item['targetSha256']
    assert row['compilerFlags']==item['flags']
    return row


def negative(item,source,directory):
    directory.mkdir(parents=True,exist_ok=True)
    address=int(item['address'],0)
    kind,targets=V.FAMILIES[address]
    text=source.read_text()
    if kind=='mmio':
        before,after='& 3','& 1'
        assert text.count(before)==4
        meaning='Discard the upper bit from the first selected 16-bit background register result'
    else:
        before='native_fn_'+format(targets[0],'08x')+'('
        after='native_fn_'+format(targets[1],'08x')+'('
        assert text.count(before)==1
        meaning='Route selector zero to the independently qualified selector-one SDK entry'
    wrong=directory/source.name
    wrong.write_text(text.replace(before,after,1))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT/pin['path'],directory/Path(pin['path']).name)
    row=compile_source(item,wrong,directory)
    try:F.L.validate(row,qualified_bindings(row),directory/'link')
    except ValueError as error:
        failure=error.args[0]
        assert isinstance(failure,dict) and failure['nativeBytes']==failure['linkedBytes']==item['bytes']
        assert failure['matchingBytes']<item['bytes']
        return dict(kind='Meaningful same-extent ordinary C source change',semanticConsequence=meaning,rejectedByFullGenuineLinkComparison=True,comparison=failure,wrongSourceSha256=sha256(wrong),wrongObjectSha256=row['objectSha256'],sourceOrCalleeCredit=0)
    raise ValueError('Wrong selector/mask source unexpectedly matched')


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    metadata,image,unused=F.L.measured_module('main')
    assert inputs['romSha256']==configuration()['romSha256'] and metadata['sha256']==inputs['moduleSha256']
    matches,controls,layouts,fixtures=[],[],[],[]
    for item in inputs['entries']:
        source=F.checked_source(item)
        directory=WORK/format(int(item['address'],0),'08x')
        row=compile_source(item,source,directory/'source')
        assert row['relocations']==item['priorRelocations'] and row['compiledBytes']==item['bytes']
        row['sourceDependencies']=item['sourceDependencies']
        bindings=qualified_bindings(row)
        assert bindings==item['qualifiedDependencies']
        witness=B.verify_original(row,bindings)
        proof=F.L.validate(row,bindings,directory/'source/link')
        code=(directory/'source/link/caller.bin').read_bytes()
        address=int(item['address'],0)
        native=image[address-0x02000000:address-0x02000000+item['bytes']]
        assert code==native
        fixtures.append(dict(address=item['address'],**V.execute(address,native,code,bindings)))
        layouts.append(dict(address=item['address'],**F.layout_checks(item,source,directory/'layout')))
        controls.append(dict(address=item['address'],**negative(item,source,directory/'negative')))
        controls.extend(dict(address=item['address'],**value) for value in F.binding_controls(row,directory/'binding'))
        header=''.join((ROOT/pin['path']).read_text() for pin in item['sourceDependencies'])
        for name in bindings:
            assert re.search(r'\b'+name+r'\s*\([^;{}]*\)\s*;',header),'Missing explicit import ABI: '+name
        row.update(program='',realLink=proof,originalCallsiteWitness=witness,manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),exactAfterDeclaredRelocation=proof['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuinely linked native caller extent',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=item['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],qualifiedDependencies=bindings,nativeSymbolEntries=bindings,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,actualNativeFunctionReturns=8,actualSourceFunctionReturns=8,actualNativeAndSourceCallerReturns=16,nativeCalleeSourceCredit=0)
        matches.append(row)
        print('proved front C',item['address'],item['bytes'],flush=True)
    assert len(matches)==8 and sum(r['bytes'] for r in matches)==956
    closure=code_closure([Path(__file__).name])
    report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],processor='arm9',module='main',program='',allPassed=True,matches=matches,matchedFunctions=8,matchedBytes=956,ordinaryCBytes=956,justifiedAssemblyBytes=0,modelCases=96,actualNativeAndSourceCallerReturns=128,terminateEntryEndpoints=64,nativeCalleeBodiesExecuted=0,hardwareOrGameExecutionCredit=0,sourceOnlyCompilerInputs=True,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],typedLayoutChecks=layouts,negativeEvidence=controls,callerModels=fixtures,freshCompileObjectsAndLinkedReportsEveryRun=True,limits=['Complete ordinary C extents, original callsite CPU/module/mode/entry witnesses and genuine pinned MW linker bytes are proved.','The bounded caller model checks four selectors, forwarding, prescribed 16-bit register reads and preserved ABI; SDK callees are deterministic providers, with zero native callee body execution.','Invalid selectors stop at the actual termination entry. These endpoints are not counted as successful caller returns or hardware behavior.','No game/scene/platform execution, physical graphics/DMA/cache behavior or supplied callee source credit is claimed.','The separate888-byte controller remains uncredited because its original overlay candidate set is unresolved. Shared acceptance is coordinator owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=8,bytes=956,callerReturns=128,controls=len(controls)),flush=True)


if __name__=='__main__':main()
