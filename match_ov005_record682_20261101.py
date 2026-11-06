import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
from link_private_overlay_hypothesis_20261101 import link_private
import ov005_record670_machine_20261101 as M
import ov005_record670_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov005_20261101_record682/source.c'
WORK=ROOT/'work/ol682-proof'


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov005','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError('682 ordinary C compilation failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:
        proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):
            raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes(),directory


def machine(original,profile,body,candidate):
    obj=M.Machine(original,profile,body,False)
    obj.u.mem_write(M.PRIVATE,bytes(len(body)))
    if candidate:
        obj.u.mem_write(M.ENTRY,body)
    obj.candidate=candidate
    obj.before=bytes(obj.u.mem_read(M.BASE,0x800000))
    return obj


def compact(result):
    return {key:result[key]for key in ['profile','candidate','coreRegistersAndCpsr','watchedNativeReturns','providedCalls','nonstackWrites','ownObserved','nativeObserved','instructions']}|dict(output=result['output'].hex(),checksumSnapshot=result['checksumSnapshot'].hex())


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':
        raise ValueError('682 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov005-record682-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError(('682 frozen input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9'and not row.get('program')and row['module']=='ov005'and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE)for row in accepted):
        raise ValueError('682 accepted snapshot overlap')
    original=M.inputs()
    row,proof,body,directory=compile_unit(SOURCE,'positive',True)
    span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    if body!=span:
        raise ValueError('682 complete canonical real-linked bytes differ')
    row['exactBytes'],row['genuineLinkComparison']=M.SIZE,freeze_link(proof)
    profiles=P.profiles()
    traces,cases=[],[]
    seen=set()
    dependencies,providers=0,0
    for profile in profiles:
        native,candidate=[machine(original,profile,body,flag).run()for flag in[False,True]]
        nm,cm=P.model(native),P.model(candidate)
        if nm!=cm:
            raise ValueError('682 complete independent models differ')
        for key in['coreRegistersAndCpsr','watchedNativeReturns','providedCalls','nonstackWrites','after','checksumSnapshot']:
            if native[key]!=candidate[key]:
                raise ValueError(('682 complete canonical state/trace differs',profile['name'],key))
        seen.update(native['ownObserved'])
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns'])
        provided=len(native['providedCalls'])+len(candidate['providedCalls'])
        dependencies+=count
        providers+=provided
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,fullRamIncludingStackEqual=True,allArmCoreRegistersAndCpsrEqual=True,allOrderedNonstackWritesAndRawContractsEqual=True,fullAfterRamSha256=c.sha(native['after']),candidateCallerOrigin=hex(M.ENTRY),privateCandidateCodePresent=False)
        traces.append(trace)
        cases.append(dict(profile=profile['name'],actualTopReturns=2,actualNativeDependencyReturns=count,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+996,4)):
        raise ValueError('682 complete code coverage differs')
    template=SOURCE.read_text()
    sum_line='    M2C_FIELD(arg1, s32 *, 0x250) = (s32) (M2C_FIELD(arg0, u16 *, 0x1E8) + (M2C_FIELD(arg0, u16 *, 0x1E6) + M2C_FIELD(arg0, u16 *, 0x1E4)));\n'
    checksum_line='    M2C_FIELD(arg1, s16 *, 0x266) = (s16) native_fn_ov005_021e1014(arg1);\n'
    variants=[('wrong-record-byte33',template.replace('M2C_FIELD(var_r7, u8 *, 0x33) = (u8) M2C_FIELD(var_r8, u8 *, 0x32)','M2C_FIELD(var_r7, u8 *, 0x33) = (u8) M2C_FIELD(var_r8, u8 *, 0x33)',1),'record-0'),('wrong-nonzero-count',template.replace('if (temp_r0 != 0) {','if (1) {',1),'record-2'),('wrong-checksum-order',template.replace(sum_line,'',1).replace(checksum_line,sum_line+checksum_line,1),'record-0')]
    controls=[]
    for name,text,case in variants:
        if text==template:
            raise ValueError('682 wrong source unchanged')
        target=ROOT/'nonmatching/overlay-lane/20261101-record682-controls'/name
        target.mkdir(parents=True,exist_ok=True)
        source=target/'source.c'
        if source.exists()and source.read_text()!=text:
            raise ValueError('682 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr,wp,unused,wd=compile_unit(source,name,False)
        private,wb=link_private(wr,qualified_bindings(wr),wd,WORK/name/'private-link',M.PRIVATE)
        profile=next(p for p in profiles if p['name']==case)
        result=M.Machine(original,profile,wb,True).run()
        try:
            P.model(result)
        except ValueError as error:
            failure=str(error)
        else:
            raise ValueError(('682 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,modelFailure=failure)
        traces.append(dict(negativeEvidence=name,**trace))
        controls.append(dict(name=name,source=wr,canonicalComparison=wp,privateLink=private,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces))
    artifact=ROOT/'evidence/generated/ov005-record682-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    readers=[]
    for offset in range(0,996,4):
        word,pc=int.from_bytes(span[offset:offset+4],'little'),M.ENTRY+offset
        if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==M.ENTRY+996:
            readers.append(hex(pc))
    if not readers or int.from_bytes(span[-4:],'little')!=M.GLOBAL:
        raise ValueError('682 literal classification differs')
    row['oracle']=dict(callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=dependencies,watchedOnlyNativeRanges={hex(k):v for k,v in original['ranges'].items()},providedCalls=providers,observedCodeBytes=996,referencedLiteralBytes=4,unclassifiedBytes=0,fullRamIncludingStackAndOrderedWritesEqual=True,allArmCoreRegistersAndCpsrEqual=True,allRelevantAndRawProviderWordsAndEffectsEqual=True,casesEvidence=cases)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={rel['symbol']:rel['target']for rel in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=dict(address=hex(M.ENTRY+996),bytes=4,value=hex(M.GLOBAL),observedUnconditionalReaders=readers),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),wholeModuleLinked=False,sourceReconstructionComplete=False,preferredFrozenSource='src/overlays/ov005_20261101_record682/source.c',historicalNearPacket='9d941776 remains unchanged with0 credit and its R3/LR differences',limits=['Single ordinary1000B source unit. All996 code bytes and4 literal bytes match through real canonical linking; module/ROM acceptance remains integrator-owned.', '32 disjoint synthetic input/output/tables/global-word profiles. Provider/scene/resource/heap/malformed/aliasing domains remain exactly those in the frozen670 fixture.', 'ProvidedCF620/658,CF590,CF6A4,449D4,E65EC,3CC2C/3CF9C,2A498 calls never count as native execution. Native wrappers and direct float/memory/ID/checksum/curve/point entries execute unchanged instructions.', 'Dependency count is watched entries only,including nested wrappers; deeper unobserved library internal returns are not added.', 'All final physical ARM registers includingR3/LR,complete RAM including stack,ordered writes and raw provider word views match at the original caller address. No private-origin adjustment or register exclusion is used for positive evidence.', 'Wrong controls use genuine private-origin links to preserve original following helper bytes if their bodies differ in size; wrong-source private effects carry0 source credit.', 'Source-record byte32 to target33 propagation remains raw format evidence with supplied source values. No initialization/meaning/persistence/current scene claim; no application changes.'])
    write_json(ROOT/'evidence/matches/ov005-20261101-record682.json',report)
    print(dict(functions=1,matchedBytes=1000,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=dependencies,providedCalls=providers,wrongActualReturns=len(controls),fullFinalPhysicalRegistersEqual=True),flush=True)


if __name__=='__main__':
    execute()
