import re
import shutil
from pathlib import Path
import wave20261104_main_front_compiler as C
import wave20261104_main_front_tenth_fixture as V
import wave20261104_main_sdk_prefix_match as F
import wave20261104_main_front_text_bindings as B
from project import ROOT,configuration,read_json,write_json,sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-front/tenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w4af/tenthproof/p'


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
    text=source.read_text()
    edits={0x02043570:('native_fn_0203d294(249)','native_fn_0203d294(248)','Change the measured random bound by one'),0x020462e0:('tile<<5,config->bytes8','tile<<5,config->paletteBytesC','Supply palette bytes as the fifth loader word')}
    before,after,meaning=edits[int(item['address'],0)]
    assert text.count(before)==1
    wrong=directory/source.name
    wrong.write_text(text.replace(before,after,1))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT/pin['path'],directory/Path(pin['path']).name)
    row=compile_source(item,wrong,directory)
    try:F.L.validate(row,qualified_bindings(row),directory/'link')
    except ValueError as error:
        failure=error.args[0]
        assert isinstance(failure,dict) and failure['nativeBytes']==item['bytes']
        assert failure['matchingBytes']<item['bytes']
        return dict(kind='Meaningful ABI-preserving ordinary C source change',semanticConsequence=meaning,rejectedByFullGenuineLinkComparison=True,comparison=failure,wrongSourceSha256=sha256(wrong),wrongObjectSha256=row['objectSha256'],sourceOrCalleeCredit=0)
    raise ValueError('Wrong selector/mask source unexpectedly matched')


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    metadata,image,unused=F.L.measured_module('main')
    assert inputs['romSha256']==configuration()['romSha256'] and metadata['sha256']==inputs['moduleSha256']
    stride=ROOT/inputs['slotStrideSource']
    assert 'arg0 * 0x210' in stride.read_text()
    matches,controls,layouts,fixtures=[],[],[],[]
    for item in inputs['entries']:
        source=F.checked_source(item)
        directory=WORK/format(int(item['address'],0),'08x')
        row=compile_source(item,source,directory/'source')
        assert row['relocations']==item['priorRelocations'] and row['compiledBytes']==item['bytes']
        row['sourceDependencies']=item['sourceDependencies']
        bindings=qualified_bindings(row)
        assert bindings==item['qualifiedDependencies']
        witness=B.verify(row,bindings)
        proof=F.L.validate(row,bindings,directory/'source/link')
        code=(directory/'source/link/caller.bin').read_bytes()
        address=int(item['address'],0)
        native=image[address-0x02000000:address-0x02000000+item['bytes']]
        assert code==native
        fixtures.append(dict(address=item['address'],**V.execute(address,native,code,bindings)))
        layouts.append(dict(address=item['address'],**F.layout_checks(item,source,directory/'layout')))
        controls.append(dict(address=item['address'],**negative(item,source,directory/'negative')))
        controls.extend(dict(address=item['address'],**value) for value in F.binding_controls(row,directory/'binding'))
        target=directory/'wrong-layout';target.mkdir(parents=True,exist_ok=True);wrong=target/source.name;shutil.copyfile(source,wrong)
        for pin in item['sourceDependencies']:
            text=(ROOT/pin['path']).read_text()
            before,after=('s16 kind2e;','u16 kind2e;') if address==0x02043570 else ('opaque4[140]','opaque4[136]')
            assert text.count(before)==1
            (target/Path(pin['path']).name).write_text(text.replace(before,after))
        wrongrow=compile_source(item,wrong,target)
        try:F.L.validate(wrongrow,qualified_bindings(wrongrow),target/'link')
        except ValueError as error:
            failure=error.args[0];assert isinstance(failure,dict) and failure['matchingBytes']<item['bytes']
        else:raise ValueError('Wrong signed kind or bank stride matched')
        try:V.execute(address,native,(target/'link/caller.bin').read_bytes(),bindings)
        except AssertionError:rejected=True
        else:raise ValueError('Wrong layout model passed')
        controls.append(dict(address=item['address'],kind='Wrong signed kind or bank stride',rejectedByGenuineLinkAndModels=rejected,comparison=failure,wrongHeaderSha256=sha256(target/'context.h'),sourceCredit=0))
        altered={name:dict(value) for name,value in bindings.items()};name=next(iter(bindings));altered[name]['module']='ov001'
        try:B.verify(row,altered)
        except (AssertionError,ValueError):controls.append(dict(address=item['address'],kind='wrong-original-module',rejected=True,sourceCredit=0))
        else:raise ValueError('Wrong original module passed')
        header=''.join((ROOT/pin['path']).read_text() for pin in item['sourceDependencies'])
        for name,binding in bindings.items():
            if binding['kind']!='function':continue
            assert re.search(r'\b'+name+r'\s*\([^;{}]*\)\s*;',header),'Missing explicit import ABI: '+name
        row.update(program='',realLink=proof,originalCallsiteWitness=witness,manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),exactAfterDeclaredRelocation=proof['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuinely linked native caller extent',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=item['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],qualifiedDependencies=bindings,nativeSymbolEntries=bindings,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,actualNativeFunctionReturns=fixtures[-1]['actualNativeReturns'],actualSourceFunctionReturns=fixtures[-1]['actualSourceReturns'],actualNativeAndSourceCallerReturns=2*fixtures[-1]['cases'],nativeCalleeSourceCredit=0)
        matches.append(row)
        print('proved front C',item['address'],item['bytes'],flush=True)
    assert len(matches)==2 and sum(r['bytes'] for r in matches)==284
    closure=code_closure([Path(__file__).name])
    report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],processor='arm9',module='main',program='',allPassed=True,matches=matches,matchedFunctions=2,matchedBytes=284,ordinaryCBytes=284,justifiedAssemblyBytes=0,modelCases=112,actualNativeAndSourceCallerReturns=224,nativeCalleeBodiesExecuted=0,hardwareOrGameExecutionCredit=0,sourceOnlyCompilerInputs=True,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],typedLayoutChecks=layouts,negativeEvidence=controls,callerModels=fixtures,freshCompileObjectsAndLinkedReportsEveryRun=True,limits=['Complete ordinary C caller extents, original import witnesses and genuine pinned MW links are proved.','The three-slot caller model checks signed16-bit filtering, three bounded random words per active slot, low-byte stores, the three-word builder boundary and the final active-slot count.','The resource caller model checks full-word bank storage, byte-width screen routing, both independent mode queries, optional palette routing and the original fifth stack argument.','Slot and resource tables are partial field views with measured strides; no complete game object meaning is inferred.','Random, builder and resource helpers use provided contracts; their source/implementation, game, graphics and hardware receive zero new execution or source credit. Shared acceptance is coordinator owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=2,bytes=284,callerReturns=224,controls=len(controls)),flush=True)


if __name__=='__main__':main()
