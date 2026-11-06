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
import ov005_controller700_machine_20261101 as M
import ov005_controller700_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov005_20261101_controller702/source.c'
WORK=ROOT/'work/ol702-proof'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov005','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('702 ordinary C compilation failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes(),directory


def compact(result):return {key:result[key]for key in['profile','connected','coreRegistersAndCpsr','watchedNativeReturns','providedCalls','nonstackWrites','ownObserved','callerObserved','nativeObserved','instructions']}


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('702 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov005-controller702-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('702 frozen input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9'and not row.get('program')and row['module']=='ov005'and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE)for row in accepted):raise ValueError('702 accepted snapshot overlap')
    original=M.inputs();row,proof,body,directory=compile_unit(SOURCE,'positive',True)
    span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    if body!=span:raise ValueError('702 complete canonical real-linked bytes differ')
    row['exactBytes'],row['genuineLinkComparison']=M.SIZE,freeze_link(proof)
    profiles=P.profiles();selected={}
    for p in profiles:selected.setdefault(p['selector'],p)
    jobs=[(p,False)for p in profiles]+[(p,True)for p in selected.values()]
    traces,cases=[],[];seen,caller_seen=set(),set();dependencies,providers=0,0
    for index,(profile,connected)in enumerate(jobs):
        native=M.Machine(original,profile,None,connected).run();candidate=M.Machine(original,profile,body,connected).run();nm,cm=P.model(native),P.model(candidate)
        if nm!=cm:raise ValueError('702 independent models differ')
        for key in['after','coreRegistersAndCpsr','watchedNativeReturns','providedCalls','nonstackWrites']:
            if native[key]!=candidate[key]:raise ValueError(('702 native/C complete state differs',profile['name'],connected,key))
        seen.update(native['ownObserved']);caller_seen.update(native['callerObserved'])
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);provided=len(native['providedCalls'])+len(candidate['providedCalls']);dependencies+=count;providers+=provided
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,fullMainRamIncludingStackEqual=True,allArmCoreRegistersAndCpsrEqual=True,orderedWritesAndAllRawProviderWordsEqual=True,fullAfterMainRamSha256=c.sha(native['after']),itcmRange='Mapped zero only to intercept provided01FF8580; nonstack-write guard forbids ITCM effects',sourceFunctionExecutedAtCanonicalAddress=True)
        traces.append(trace);cases.append(dict(profile=profile['name'],connectedOrdinaryCaller=connected,topEntry=hex(M.CALLER if connected else M.ENTRY),actualTopReturns=2,actualNativeDependencyReturns=count,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
        if index%60==0:print(dict(completedPairs=index+1,total=len(jobs)),flush=True)
    if seen!=set(range(M.ENTRY,M.ENTRY+932,4)):raise ValueError(('702 full caller code coverage differs',sorted(set(range(M.ENTRY,M.ENTRY+932,4))-seen),sorted(seen-set(range(M.ENTRY,M.ENTRY+932,4)))))
    template=SOURCE.read_text();header=SOURCE.with_name('context.h').read_text()
    wrong_copy=template.replace('u32 *auxiliary = native_data_ov005_021ed494','u8 *auxiliary = native_data_ov005_021ed494',1)
    choices=[('wrong-final-mode',template.replace('s8 *, 9) = 3','s8 *, 9) = 2',1),header,profiles[0]),('wrong-auxiliary-byte-copy',wrong_copy,header.replace('extern u32 native_data_ov005_021ed494[]','extern u8 native_data_ov005_021ed494[]'),profiles[3]),('wrong-special-fullword-predicate',template.replace('if (*(s32 *) native_fn_02064340() == 1)','if (*(s32 *) native_fn_02064340() != 0)',1),header,next(p for p in profiles if p['selector']==48 and p['specialWord']==2)),('wrong-sentinel-byte-width',template,header.replace('extern u32 native_data_ov005_021e7764[]','extern u8 native_data_ov005_021e7764[]'),next(p for p in profiles if p['selector']==50))]
    controls=[]
    for name,text,context,profile in choices:
        if text==template and context==header:raise ValueError('702 wrong source/context unchanged')
        target=ROOT/'nonmatching/overlay-lane/20261101-controller702-controls'/name;target.mkdir(parents=True,exist_ok=True);source=target/'source.c'
        for path,content in[(source,text),(source.with_name('context.h'),context)]:
            if path.exists()and path.read_text()!=content:raise ValueError('702 frozen wrong input differs')
            path.write_text(content)
        wr,wp,unused,wd=compile_unit(source,name,False);private,wb=link_private(wr,qualified_bindings(wr),wd,WORK/name/'private-link',0x02650000)
        result=M.Machine(original,profile,wb,False,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('702 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,modelFailure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,source=wr,canonicalComparison=wp,privateLink=private,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    literals=[]
    for offset in range(932,952,4):
        target,readers=M.ENTRY+offset,[]
        for index in range(0,932,4):
            word,pc=int.from_bytes(span[index:index+4],'little'),M.ENTRY+index
            if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==target:readers.append(hex(pc))
        if not readers or any(int(pc,16)not in seen for pc in readers):raise ValueError('702 observed literal readers absent')
        literals.append(dict(address=hex(target),bytes=4,value=hex(int.from_bytes(span[offset:offset+4],'little')),observedUnconditionalReaders=readers))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov005-controller702-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    row['oracle']=dict(callerPairs=len(jobs),directInitializerPairs=len(profiles),connectedSlot0CallerPairs=len(selected),actualTopReturns=len(jobs)*2,actualNativeDependencyReturns=dependencies,providedCalls=providers,observedCodeBytes=932,referencedLiteralBytes=20,unclassifiedBytes=0,allArmCoreRegistersAndCpsrEqual=True,fullMainRamIncludingStackAndOrderedWritesEqual=True,allRelevantAndRawProviderWordsAndEffectsEqual=True,scopeOfNativeDependencies='Direct:actual08C58 memory clear. Connected:also actualDFAB0 state getter and actualE1600 constructor callback; the final source function adds no duplicate source credit as a dependency.',casesEvidence=cases)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=literals,connectedCaller=dict(entry=hex(M.CALLER),bytes=348,context=hex(M.CALLCTX),table='0x021E6EA4',tableIndex=0,entryStage=0,callbackCallPc='0x021DF67C',callbackReturnPc='0x021DF680',callbackPhysicalR0='0xFFFFFFFF',immediateDiscard='MOV R0,#1;STR R0,[R4,#4]',finalStage=1,finalPhysicalR0=8,observedCallerCodeBytes=len(caller_seen)*4,sourceCredit=0,unknownOtherCallbackSignatures=True),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),wholeModuleLinked=False,sourceReconstructionComplete=False,limits=['Single952B ordinary source unit with932 observed code+20 literal bytes; module/ROM acceptance remains separate.','Source return view is void, with physicalR0=-1 preserved in every direct/callback test. Known table index0/stage0 native caller discardsR0; other indirect/public callback prototypes remain unqualified.','All services except actual08C58,DFAB0 and source callback are supplied boundaries:see explicit provided-call traces. Neither clock/RTC/hardware,resource/heap/rendering state nor current scene is claimed native-reproduced.','0F3E0 supplies16 raw output bytes; own code adds2000 modulo32 to first word. Calendar/valid-date semantics of that external routine are not inferred from the test provider.','GlobalDD494 andE7764 word accesses follow original LDR/STR and independent full-width profiles/returning wrong-width controls. Signed final-byte source view matches native code, without assigning a game meaning.','The connected dispatcher uses synthetic index0/stage0 context and unchanged original table/code; its later stages/slot1 return semantics/slot2 cleanup, recursion,actual resource lifecycle and real reachability are outside this fixture.','ITCM01FF8580 and Thumb02089AA4 are supplied boundaries; mode-correct return is enforced and neither is counted native. No emulator/device/audio/application changes.'])
    write_json(ROOT/'evidence/matches/ov005-20261101-controller702.json',report)
    print(dict(functions=1,matchedBytes=952,callerPairs=len(jobs),actualTopReturns=len(jobs)*2,actualNativeDependencyReturns=dependencies,providedCalls=providers,wrongActualReturns=len(controls),connectedPairs=len(selected)),flush=True)


if __name__=='__main__':execute()
