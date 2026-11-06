import re
import shutil
from pathlib import Path
import wave20261104_main_front_compiler as C
import wave20261104_main_front_state_fixture as V
import wave20261104_main_sdk_prefix_match as F
import wave20261104_main_tail_bindings as B
from project import ROOT,configuration,read_json,write_json,sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-front/seventh'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w4af/stateproof/p'


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
    edits={0x02042e30:('0xF6','0xF7',2,'Change the selector0 second output and returned word by one'),0x02042aac:('0xffffffff,entry->word4','0xffffffff,(u8)entry->word4',1,'Narrow the measured second callee argument from16 to8bits')}
    before,after,count,meaning=edits[int(item['address'],0)]
    assert text.count(before)==count
    wrong=directory/source.name
    wrong.write_text(text.replace(before,after,count))
    for pin in item['sourceDependencies']:
        shutil.copyfile(ROOT/pin['path'],directory/Path(pin['path']).name)
    row=compile_source(item,wrong,directory)
    try:F.L.validate(row,qualified_bindings(row),directory/'link')
    except ValueError as error:
        failure=error.args[0]
        assert isinstance(failure,dict) and failure['nativeBytes']==item['bytes']
        assert failure['matchingBytes']<item['bytes']
        return dict(kind='Meaningful ordinary C source change preserving the explicit callee ABI',semanticConsequence=meaning,rejectedByFullGenuineLinkComparison=True,comparison=failure,wrongSourceSha256=sha256(wrong),wrongObjectSha256=row['objectSha256'],sourceOrCalleeCredit=0)
    raise ValueError('Wrong selector/mask source unexpectedly matched')


def verify_abi(inputs):
    import hashlib
    import sys
    sys.path.insert(0,str(ROOT/'deps/native'))
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
    path=ROOT/inputs['abiEvidence']
    abi=read_json(path);item=abi['payloadBoundary']
    assert sha256(ROOT/item['acceptedSource'])==item['acceptedSourceSha256']
    text=(ROOT/item['acceptedSource']).read_text()
    assert re.search(r'native_main_0205e7a8\(u32 arg0, u32 arg1\)',text)
    assert 'native_fn_0205f13c(arg0, arg1, -1, -1)' in text
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();address=int(item['address'],0)
    body=image[address-0x02000000:address-0x02000000+item['bytes']]
    assert hashlib.sha256(body).hexdigest()==item['targetSha256']
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;first=None;prefix=[]
    for instruction in decoder.disasm(body,address):
        if instruction.mnemonic=='bl':
            assert instruction.op_str=='#0x205f13c';first=instruction.address;break
        assert 'r1' not in [instruction.reg_name(r) for r in instruction.regs_access()[1]]
        prefix.append(dict(address=hex(instruction.address),instruction=instruction.mnemonic+' '+instruction.op_str))
    assert first is not None
    return dict(originalIncomingR1PreservedToFirstCall=hex(first),prefix=prefix,acceptedSource=item['acceptedSource'],acceptedSourceSha256=item['acceptedSourceSha256'],originalTargetSha256=item['targetSha256'],calleeSourceOrExecutionCredit=0)


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    metadata,image,unused=F.L.measured_module('main')
    assert inputs['romSha256']==configuration()['romSha256'] and metadata['sha256']==inputs['moduleSha256']
    abi=verify_abi(inputs)
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
        for name,binding in bindings.items():
            changes=[('wrong-module',dict(module='ov001'))]
            if name=='native_fn_0205e7a8':changes+=[('payload-mode',dict(mode='thumb')),('payload-entry',dict(address=hex(int(binding['address'],0)+4))),('payload-cpu',dict(processor='arm7'))]
            for label,change in changes:
                altered={n:dict(v) for n,v in bindings.items()};altered[name].update(change)
                try:
                    if label=='wrong-module':B.verify_original(row,altered)
                    else:F.L.validate(row,altered,directory/'binding'/label/name)
                except (ValueError,AssertionError) as error:controls.append(dict(address=item['address'],kind=label,symbol=name,rejected=True,reason=str(error),sourceCredit=0))
                else:raise ValueError('Altered state binding passed')
        if address==0x02042aac:
            target=directory/'signed-layout';target.mkdir(parents=True,exist_ok=True)
            wrong=target/source.name;shutil.copyfile(source,wrong)
            for pin in item['sourceDependencies']:
                text=(ROOT/pin['path']).read_text();assert text.count('u16 word4;')==1
                (target/Path(pin['path']).name).write_text(text.replace('u16 word4;','s16 word4;'))
            wrongrow=compile_source(item,wrong,target)
            try:F.L.validate(wrongrow,qualified_bindings(wrongrow),target/'link')
            except ValueError as error:
                failure=error.args[0];assert isinstance(failure,dict) and failure['matchingBytes']<item['bytes']
            else:raise ValueError('Signed payload field matched')
            try:V.execute(address,native,(target/'link/caller.bin').read_bytes(),bindings)
            except AssertionError:rejected=True
            else:raise ValueError('Signed payload model passed')
            controls.append(dict(address=item['address'],kind='Same-layout signedness source change',rejectedByGenuineLinkAndHighBitPayloadModels=rejected,comparison=failure,wrongHeaderSha256=sha256(target/'context.h'),wrongObjectSha256=wrongrow['objectSha256'],calleeSourceCredit=0))
        header=''.join((ROOT/pin['path']).read_text() for pin in item['sourceDependencies'])
        for name in bindings:
            assert re.search(r'\b'+name+r'\s*\([^;{}]*\)\s*;',header),'Missing explicit import ABI: '+name
        row.update(program='',realLink=proof,originalCallsiteWitness=witness,manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),exactAfterDeclaredRelocation=proof['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuinely linked native caller extent',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=item['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],qualifiedDependencies=bindings,nativeSymbolEntries=bindings,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,actualNativeFunctionReturns=fixtures[-1]['actualNativeReturns'],actualSourceFunctionReturns=fixtures[-1]['actualSourceReturns'],actualNativeAndSourceCallerReturns=2*fixtures[-1]['cases'],nativeCalleeSourceCredit=0)
        matches.append(row)
        print('proved front C',item['address'],item['bytes'],flush=True)
    assert len(matches)==2 and sum(r['bytes'] for r in matches)==428
    closure=code_closure([Path(__file__).name])
    report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],processor='arm9',module='main',program='',allPassed=True,matches=matches,matchedFunctions=2,matchedBytes=428,ordinaryCBytes=428,justifiedAssemblyBytes=0,modelCases=78,actualNativeAndSourceCallerReturns=156,nativeCalleeBodiesExecuted=0,hardwareOrGameExecutionCredit=0,sourceOnlyCompilerInputs=True,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],typedLayoutChecks=layouts,measuredCalleeAbi=abi,negativeEvidence=controls,callerModels=fixtures,freshCompileObjectsAndLinkedReportsEveryRun=True,limits=['Complete ordinary C caller extents, original callsite namespace/mode/entry and genuine pinned MW linker bytes are proved.','The word-pair model checks all nine selectors, out-of-range defaults and aliased output pointers.','The state caller model uses explicit provided query and two-word payload contracts, including high unsigned16-bit payloads and full-word signed-frame capture.','The accepted payload callee source and original incoming-R1 flow support the import ABI; the callee receives zero new source or execution credit.','The nearby96-byte helper and other larger drafts remain uncredited; no game, hardware or native provided-callee execution is claimed. Shared acceptance is coordinator owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=2,bytes=428,callerReturns=156,controls=len(controls)),flush=True)


if __name__=='__main__':main()
