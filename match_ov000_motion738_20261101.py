import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_motion738_machine_20261101 as M
import ov000_motion738_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_motion738'
WORK=ROOT/'work/ol738-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';old=c.symbol_address
    def resolver(symbol):
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('738 unqualified compiler intrinsic '+symbol)
        return old(symbol)
    c.symbol_address=resolver
    try:rows,unused=c.compare(source,'ov000','2','off',True)
    finally:c.symbol_address=old
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('738 compiler failed',rows))
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'canonical-link';bindings=qualified_bindings(row)
    if private:
        try:canonical=validate(row,bindings,directory)
        except ValueError as error:
            if not isinstance(error.args[0],dict):raise
            canonical=error.args[0]
        proof,body=link_private(row,bindings,directory,WORK/name/'private-link',M.PRIVATE)
        return dict(source=row,canonicalComparison=canonical,privateLink=proof),body
    proof=validate(row,bindings,directory)
    return dict(**row,realLink=proof),(directory/'caller.bin').read_bytes()

def compact(result):return{key:result[key]for key in['profile','direct','coreRegistersAndCpsr','nativeCalls','watchedNativeReturns','nonstackWrites','ownObserved','nativeObserved','instructions']}|dict(finalState=result['finalState'].hex())

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('738 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-motion738-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('738 frozen input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov000'and any(max(r['address'],a)<min(r['address']+r['bytes'],a+n)for a,n in[(M.ENTRY,M.SIZE),(M.CLAMP,M.CLAMP_SIZE)])for r in accepted):raise ValueError('738 already-selected overlap')
    original=M.inputs()
    if original['module']['sha256']!=pins['ov000Sha256']:raise ValueError('738 module0 image differs')
    matches=[];bodies={}
    for filename,address,size in[('source.c',M.ENTRY,M.SIZE),('clamp.c',M.CLAMP,M.CLAMP_SIZE)]:
        row,body=compile_unit(SOURCE/filename,filename)
        if len(body)!=size:raise ValueError('738 wrong matched extent')
        matches.append(row);bodies[address]=body
    traces,cases=[],[];seen={M.ENTRY:set(),M.CLAMP:set()};watched=0;by_entry={};wide_returns=[]
    for direct,profiles in[(False,P.profiles()),(True,P.direct_profiles())]:
        for profile in profiles:
            native=M.Machine(original,profile,direct=direct).run();candidate=M.Machine(original,profile,bodies,direct).run();nm,cm=P.model(native),P.model(candidate)
            if nm!=cm or native['before']!=candidate['before']or native['after']!=candidate['after']or native['coreRegistersAndCpsr']!=candidate['coreRegistersAndCpsr']or native['nativeCalls']!=candidate['nativeCalls']or native['watchedNativeReturns']!=candidate['watchedNativeReturns']or native['nonstackWrites']!=candidate['nonstackWrites']:raise ValueError(('738 full physical state/call comparison differs',profile['name']))
            if not direct and profile['active']!=0:
                word=native['coreRegistersAndCpsr'][0];signed=word if word<0x80000000 else word-0x100000000
                if signed!=P.s16(word):wide_returns.append(profile['name'])
            seen[M.CLAMP if direct else M.ENTRY].update(native['ownObserved']);count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);watched+=count
            for result in[native,candidate]:
                for item in result['watchedNativeReturns']:by_entry[item['entry']]=by_entry.get(item['entry'],0)+1
            trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallWordsAndOrderedWritesEqual=True)
            traces.append(trace);cases.append(dict(profile=profile['name'],directClamp=direct,actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=0,traceSha256=c.sha(encoded(trace))))
    if seen[M.ENTRY]!=set(range(M.ENTRY,M.ENTRY+480,4))or seen[M.CLAMP]!=set(range(M.CLAMP,M.CLAMP+M.CLAMP_SIZE,4)):raise ValueError('738 own native code coverage incomplete')
    template=(SOURCE/'source.c').read_text();clamp=(SOURCE/'clamp.c').read_text();variants=[('wrong-ratio',template.replace('02025578(8.0f','02025578(7.0f',1),False,P.profiles()[0]),('wrong-active-sign',template.replace('if(native_data_ov000_02245e54.field20==0)','if((s32)native_data_ov000_02245e54.field20<=0)',1),False,next(p for p in P.profiles()if p['active']==0x80000000)),('wrong-clamp-minimum',clamp.replace('0x80000','0x7F000'),True,next(p for p in P.direct_profiles()if p['vector'][0]<0x7F000))]
    narrow=template.replace('void native_ov000_022199b8(void)','s16 native_ov000_022199b8(void)').replace('if(native_data_ov000_02245e54.field20==0)return;','if(native_data_ov000_02245e54.field20==0)return 0;')
    end=narrow.rfind('}')
    narrow=narrow[:end]+'    return native_data_ov000_02245e54.field12;\n'+narrow[end:]
    variants.append(('wrong-narrow-return',narrow,False,P.profiles()[48]))
    controls=[]
    for name,text,direct,profile in variants:
        directory=ROOT/'nonmatching/overlay-lane/20261101-motion738-controls'/name;directory.mkdir(parents=True,exist_ok=True);path=directory/'source.c'
        if path.exists()and path.read_text()!=text:raise ValueError('738 frozen wrong source differs')
        path.write_text(text);path.with_name('context.h').write_bytes((SOURCE/'context.h').read_bytes());wrong,body=compile_unit(path,name,True);result=M.Machine(original,profile,direct=direct,private_body=body).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('738 returning wrong control escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-motion738-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    total=len(cases);report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=matches,canonicalMatchedFunctions=2,canonicalMatchedBytes=632,sourceCreditPendingIntegrator=632,callerRawReturnOutsideStoredSigned16=dict(count=len(wide_returns),profiles=wide_returns),callerPairs=len(P.profiles()),directClampPairs=len(P.direct_profiles()),actualTopReturns=total*2,actualWatchedNativeDependencyReturns=watched,nativeDependencyCounts={hex(k):v for k,v in sorted(by_entry.items())},providedCalls=0,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallWordsAndOrderedWritesEqual=True,allOwnCodeObserved=dict(callerCodeBytes=480,callerLiteralBytes=12,clampCodeBytes=140,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['Two genuine canonical632-byte ordinary C matches; parent integration/full module/ROM acceptance is still required.', 'All listed lower helpers run original native instructions; the rebuilt peer substitutes both newly linked units. Dependency returns include the clamp when reached by its parent and exclude it in direct-clamp top tests; no providers or duplicate top-return additions.', 'State, raw selected byte, table row14, actor vector and offsets are synthetic initialized inputs. Index0/1/127/255 is not proof of a legal game table extent, loaded scene, field meaning or current state.', 'Signed count is nonzero; conversion/multiply/divide/add/subtract results are finite and signed32 truncations in range. Count0, NaN/infinity inputs, malformed pointers/aliasing and other scene prerequisites remain unsupported.', 'Global02245EA0 is the exact+0x4C embedded12B vector at02245E54, represented as one C object. GetterDF1F0 output is explicitly passed intoDF3BC; legacy selected source already declares its s32 parameter, while the older generated draft context had omitted it.', 'Both source functions use void implementation views. Complete physical R0 is measured independently: top early return0, otherwise final pre-narrowing conversion word; clamp final pre-upper-store Z residue. No semantic/public original return type is claimed.', 'Main02041F74 original native copy uses nonnull12B output in the caller; its null behavior is static evidence only. Entry25CA4 branches into shared float code and remains zero source/boundary credit.', 'No host Windows/Android execution, application edits, actual map/camera/battle reachability or external SDK source adoption.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-motion738.json',report);print(dict(functions=2,matchedBytes=632,callerPairs=report['callerPairs'],directClampPairs=report['directClampPairs'],actualTopReturns=total*2,actualWatchedNativeDependencyReturns=watched,providedCalls=0,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
