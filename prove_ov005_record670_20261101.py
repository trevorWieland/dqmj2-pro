import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov005_record670_machine_20261101 as M
import ov005_record670_models_20261101 as P
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-record670/unsigned-views/source.c'
WORK=ROOT/'work/ol670-proof'


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_private(source,name):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov005','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError('670 ordinary C compilation failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    canonical_directory=WORK/name/'canonical-link'
    try:
        canonical=validate(row,qualified_bindings(row),canonical_directory)
    except ValueError as error:
        if not isinstance(error.args[0],dict):
            raise
        canonical=error.args[0]
    private,body=link_private(row,qualified_bindings(row),canonical_directory,WORK/name/'private-link',M.PRIVATE)
    return dict(source=row,canonicalComparison=canonical,privateLink=private),body


def compact(result):
    return {key:result[key] for key in ['profile','candidate','coreRegistersAndCpsr','watchedNativeReturns','providedCalls','nonstackWrites','ownObserved','nativeObserved','instructions']}|dict(output=result['output'].hex(),checksumSnapshot=result['checksumSnapshot'].hex())


def execute():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':
        raise ValueError('670 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov005-record670-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError(('670 frozen input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9' and not row.get('program') and row['module']=='ov005' and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE) for row in accepted):
        raise ValueError('670 accepted snapshot overlap')
    original=M.inputs()
    packet,body=compile_private(SOURCE,'positive')
    if packet['canonicalComparison'].get('matchingBytes')!=581 or len(body)!=1008:
        raise ValueError('670 frozen nonmatching hypothesis changed')
    profiles=P.profiles()
    traces,cases=[],[]
    seen,seen_private=set(),set()
    registers_changed=set()
    dependencies,providers=0,0
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body,flag).run() for flag in [False,True]]
        nm,cm=P.model(native),P.model(candidate)
        if nm!=cm:
            raise ValueError('670 independent full models differ')
        lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
        if native['after'][:lo]!=candidate['after'][:lo] or native['after'][hi:]!=candidate['after'][hi:]:
            raise ValueError('670 complete nonstack RAM differs')
        nw,cw=[[row[1:] for row in item['nonstackWrites']] for item in [native,candidate]]
        if nw!=cw:
            raise ValueError('670 ordered nonstack effects differ')
        differences=[index for index,(left,right)in enumerate(zip(native['coreRegistersAndCpsr'],candidate['coreRegistersAndCpsr']))if left!=right]
        if differences!=[3,14]:
            raise ValueError(('670 physical register differences changed',differences))
        registers_changed.update(differences)
        if candidate['coreRegistersAndCpsr'][3]!=3 or native['coreRegistersAndCpsr'][3]!=0xA6700300:
            raise ValueError('670 observed nonsemantic R3 residues changed')
        seen.update(native['ownObserved'])
        seen_private.update(candidate['ownObserved'])
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns'])
        provided=len(native['providedCalls'])+len(candidate['providedCalls'])
        dependencies+=count
        providers+=provided
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,completeNonstackRamAndOrderedWritesEqual=True,privateCodeLoadedIdenticallyInBothMachines=True,nonstackBeforeSha256=c.sha(native['before'][:lo]+native['before'][hi:]),nonstackAfterSha256=c.sha(native['after'][:lo]+native['after'][hi:]),nonstackExclusions=[],stackMemoryDifferent=True,physicalRegisterDifferences=differences)
        traces.append(trace)
        cases.append(dict(profile=profile['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
    expected=set(range(M.ENTRY,M.ENTRY+996,4))
    if seen!=expected or seen_private!=set(range(M.PRIVATE,M.PRIVATE+1004,4)):
        raise ValueError('670 native/private code coverage differs')
    template=SOURCE.read_text()
    sum_line='    M2C_FIELD(arg1, s32 *, 0x250) = (s32) (M2C_FIELD(arg0, u16 *, 0x1E8) + (M2C_FIELD(arg0, u16 *, 0x1E6) + M2C_FIELD(arg0, u16 *, 0x1E4)));\n'
    checksum_line='    M2C_FIELD(arg1, s16 *, 0x266) = (s16) native_fn_ov005_021e1014(arg1);\n'
    variants=[('wrong-record-byte33',template.replace('M2C_FIELD(var_r7, u8 *, 0x33) = (u8) M2C_FIELD(var_r8, u8 *, 0x32)','M2C_FIELD(var_r7, u8 *, 0x33) = (u8) M2C_FIELD(var_r8, u8 *, 0x33)',1),'record-0'),('wrong-nonzero-count',template.replace('if (temp_r0 != 0) {','if (1) {',1),'record-2'),('wrong-checksum-order',template.replace(sum_line,'',1).replace(checksum_line,sum_line+checksum_line,1),'record-0')]
    controls=[]
    for name,text,case in variants:
        if text==template:
            raise ValueError('670 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-record670-controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists() and source.read_text()!=text:
            raise ValueError('670 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wrong,wrong_body=compile_private(source,name)
        profile=next(p for p in profiles if p['name']==case)
        result=M.Machine(original,profile,wrong_body,True).run()
        try:
            P.model(result)
        except ValueError as error:
            failure=str(error)
        else:
            raise ValueError(('670 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,modelFailure=failure)
        traces.append(dict(negativeEvidence=name,**trace))
        controls.append(dict(name=name,**wrong,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces))
    artifact=ROOT/'evidence/generated/ov005-record670-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    word=int.from_bytes(span[-4:],'little')
    readers=[]
    for offset in range(0,996,4):
        instruction,pc=int.from_bytes(span[offset:offset+4],'little'),M.ENTRY+offset
        if instruction>>28==14 and instruction&0x0F7F0000==0x051F0000 and pc+8+((instruction&4095)if instruction&0x00800000 else-(instruction&4095))==M.ENTRY+996:
            readers.append(hex(pc))
    if word!=M.GLOBAL or not readers:
        raise ValueError('670 native literal classification differs')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],mode='arm',address=hex(M.ENTRY),bytes=M.SIZE,sourceCredit=0,exactByteCredit=0,**packet,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=providers,allCallerCodeObserved=dict(nativeCodeBytes=996,privateCodeBytes=1004,nativeLiteralBytes=4,nativeUnclassifiedBytes=0),literalEvidence=dict(address=hex(M.ENTRY+996),value=hex(word),bytes=4,observedUnconditionalReaders=readers),allOutputAndOtherNonstackRamEqual=True,allOrderedNonstackWritesEqual=True,fullFinalRegistersEqual=False,physicalRegisterDifferences=dict(indices=sorted(registers_changed),R3='Native restores incomingA6700300; C returns3 as caller-saved residue. No equivalence for callers that rely on physicalR3.',LR='Native21E6AE4 versus private26503E8 are actual final-call return addresses; PC returns to same sentinel.',equal='R0,R1,R2,R4..R12,SP,PC,CPSR'),privateStorageComparison='Identical candidate code is mapped in both machines before entry; complete nonstack state is compared with no private-code exclusion.',watchedNativeRanges={hex(k):v for k,v in original['ranges'].items()},negativeEvidence=controls,cases=cases,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['1000B ordinary draft with581 canonical matching bytes and a1008B genuine private-origin binary; zero function/byte/module credit.', 'Inputs and outputs are separate synthetic disjoint objects. Point payloads, metadata, curve data, normalization outputs and global words are supplied test state, not current game data.', 'NativeE6AEC/52 andE6B20/16 wrappers execute original instructions; theirCF590 outparam normalization andCF6A4 alias-pair identity boundaries are supplied. Unused raw helper/provider registers and stack addresses are recorded but not public semantic signatures.', 'NativeE6660/24 always forwards(handle,pointer) to0202A498, even pointer0. General heap release is supplied; the earlier unqualified native heap write is retained separately as a failed harness boundary.', '020CF620/658,020449D4,ov005E65EC,0203CC2C/CF9C and0202A498 are provided zero-RAM services, with explicit normalized output bytes atCF590 helper stack slots. They never count as native dependency returns.', 'Watched native return total counts only listed entries, including nested wrappers and direct float SDK entries; deeper unobserved library internal returns are not added.', 'Binary32 arithmetic is finite and nonnegative; unsigned table fields and byte variants keep signed conversion in range. Global shifts use explicit unsigned32 before shifting. NaN/Inf, buffer aliasing, malformed resources, allocator context and ordinary scene reachability remain unsupported.', 'Measured source-record byte0x32 to target-record byte0x33 propagation uses supplied source bytes. It establishes no initial writer, field meaning, save persistence or birth/reward scene connection.'])
    write_json(ROOT/'evidence/attempts/ov005-record670-functional-source-20261101.json',report)
    print(dict(callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=providers,wrongActualReturns=len(controls),sourceCredit=0),flush=True)


if __name__=='__main__':
    execute()
