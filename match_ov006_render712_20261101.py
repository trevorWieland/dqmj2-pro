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
import ov006_render712_machine_20261101 as M
import ov006_render712_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov006_20261101_render712/source.c'
WORK=ROOT/'work/ol712-proof'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov006','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('712 ordinary C compilation failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes(),directory


def compact(result):return {key:result[key]for key in['profile','coreRegistersAndCpsr','providedCalls','ownObserved','instructions']}


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('712 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov006-render712-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('712 frozen input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9'and not row.get('program')and row['module']=='ov006'and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE)for row in accepted):raise ValueError('712 accepted snapshot overlap')
    original=M.inputs();row,proof,body,directory=compile_unit(SOURCE,'positive',True);span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    if span!=body:raise ValueError('712 complete canonical real-linked bytes differ')
    row['exactBytes'],row['genuineLinkComparison']=M.SIZE,freeze_link(proof)
    interfaces=json.loads((ROOT/'evidence/abi/ov006-render712-word-interfaces-20261101.json').read_text())
    for function in interfaces['functions']:
        address=int(function['address'],0);native=original['overlay'][address-M.OVERLAY:address-M.OVERLAY+function['bytes']]
        if c.sha(native)!=function['nativeSpanSha256']:raise ValueError('712 minimum-word native span changed')
    if span[0xB4:0xBC]!=bytes.fromhex('1300a0e300008de5'):raise ValueError('712 native dominating19 store changed')
    profiles=P.profiles();traces,cases=[],[];seen=set();providers=0
    for index,profile in enumerate(profiles):
        native=M.Machine(original,profile).run();candidate=M.Machine(original,profile,body).run();nm,cm=P.model(native),P.model(candidate)
        if nm!=cm:raise ValueError('712 full independent models differ')
        for key in['after','coreRegistersAndCpsr','providedCalls']:
            if native[key]!=candidate[key]:raise ValueError(('712 native/C complete state differs',profile['name'],key))
        seen.update(native['ownObserved']);provided=len(native['providedCalls'])+len(candidate['providedCalls']);providers+=provided
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,allArmCoreRegistersAndCpsrEqual=True,fullRamIncludingStackEqual=True,allProviderMinimumWordsAndRawRegistersEqual=True,fullAfterRamSha256=c.sha(native['after']))
        traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualNativeDependencyReturns=0,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+960,4)):raise ValueError(('712 observed code coverage differs',sorted(set(range(M.ENTRY,M.ENTRY+960,4))-seen)))
    template,header=SOURCE.read_text(),SOURCE.with_name('context.h').read_text();name_text=template.replace('0x13U','0x12U');cap_text=template.replace('0xF423F','0xF423E');signed_text=template.replace('if (var_r1 != 0)','if ((s32)var_r1 > 0)',1);name_width_text=template.replace('M2C_FIELD(temp_r4, u8 *, 0x14)','M2C_FIELD(temp_r4, u16 *, 0x14)',1)
    choices=[('wrong-dominating-name-word',name_text,profiles[0]),('wrong-six-digit-cap',cap_text,profiles[3]),('wrong-signed-counter-predicate',signed_text,profiles[5]),('wrong-name-halfword-read',name_width_text,profiles[0])];controls=[]
    for name,text,profile in choices:
        if text==template:raise ValueError(('712 wrong source unchanged',name))
        target=ROOT/'nonmatching/overlay-lane/20261101-render712-controls'/name;target.mkdir(parents=True,exist_ok=True);source=target/'source.c'
        for path,content in[(source,text),(source.with_name('context.h'),header)]:
            if path.exists()and path.read_text()!=content:raise ValueError('712 frozen wrong source differs')
            path.write_text(content)
        wr,wp,unused,wd=compile_unit(source,name,False);private,wb=link_private(wr,qualified_bindings(wr),wd,WORK/name/'private-link',M.PRIVATE);result=M.Machine(original,profile,wb,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('712 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,modelFailure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,source=wr,canonicalComparison=wp,privateLink=private,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    literals=[]
    for offset in range(960,1000,4):
        target,readers=M.ENTRY+offset,[]
        for index in range(0,960,4):
            word,pc=int.from_bytes(span[index:index+4],'little'),M.ENTRY+index
            if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==target:readers.append(hex(pc))
        if not readers or any(int(pc,16)not in seen for pc in readers):raise ValueError('712 observed unconditional literal reader absent')
        literals.append(dict(address=hex(target),bytes=4,value=hex(int.from_bytes(span[offset:offset+4],'little')),observedUnconditionalReaders=readers))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov006-render712-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    row['oracle']=dict(callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=0,providedCalls=providers,observedCodeBytes=960,referencedLiteralBytes=40,unclassifiedBytes=0,allArmCoreRegistersAndCpsrEqual=True,fullRamIncludingStackEqual=True,allProviderMinimumWordsAndRawRegistersEqual=True,casesEvidence=cases)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov006',moduleSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=literals,minimumWordInterfaceEvidence=dict(path='evidence/abi/ov006-render712-word-interfaces-20261101.json',sha256=sha256(ROOT/'evidence/abi/ov006-render712-word-interfaces-20261101.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),wholeModuleLinked=False,sourceReconstructionComplete=False,limits=['Single1000B ordinary caller with960 observed code+40 literal bytes; no module/ROM acceptance yet.','All record queries,resource/text lookups,creation,clear and text/number formatting/rendering calls are explicitly supplied zero-RAM boundaries. Native dependency return count is0; none are mislabeled native execution.','Profiles use readable synthetic64B/12B record buffers,disjoint from stack/code,with an opaque record-word key. Null query returns/real resource validity/rendering effects/current scene are unqualified.','Every minimum7/8-word call interface is checked against an independent golden intent model and raw native stack/register captures. Minimum own reads and2 dominating-stack sites are native/hash-qualified; full public/transitive semantics remain unresolved.','Own byte-name test does not identify text encoding. Field meanings/display labels are not inferred from offsets,numeric caps or supplied text pointers.','Raw finalR0 passes through last supplied renderer word0/1/80000000/FFFFFFFF; this is not a native renderer-error or success-path claim.','Wrong controls are genuinely linked at a private address to preserve adjacent code and all actually return; no opcode patches/generic M2C_ERROR lowering/shared frontend edits.'])
    write_json(ROOT/'evidence/matches/ov006-20261101-render712.json',report);print(dict(functions=1,matchedBytes=1000,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=0,providedCalls=providers,wrongActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
