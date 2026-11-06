import gzip
import json
import re
import sys
import struct
import match_runtime as c
import unicorn
from project import ROOT,write_json,sha256,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import match_main_builder588_20261101 as H
import overlay_builder590_machine_20261101 as M
import overlay_builder590_models_20261101 as P
WORK=ROOT/'work/ol590-proof'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def literal_evidence(original,unit,seen):
    entry,size=unit['entry'],unit['size'];offset=entry-0x021D7240;span=original['overlay'][offset:offset+size];address=entry+size-4;value=struct.unpack_from('<I',span,size-4)[0];readers=[]
    for index in range(0,size-4,4):
        word=struct.unpack_from('<I',span,index)[0];pc=entry+index
        if word>>28==14 and word&0x0F7F0000==0x051F0000:
            target=pc+8+((word&4095)if word&0x00800000 else-(word&4095))
            if target==address:readers.append(dict(pc=hex(pc),instructionWord=hex(word),observed=pc in seen))
    if not readers or not all(r['observed']for r in readers)or value!=unit['globalAddress']:raise ValueError('590 native literal classification differs')
    return dict(address=hex(address),bytes=4,value=hex(value),classification='Unconditional PC-relative word load, dynamically observed reader, not executed as code',readers=readers)


def compile_unit(source,module,name):
    old=c.symbol_address
    def resolver(symbol):
        if symbol=='_s32_div_f':return M.DIV
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('590 unqualified intrinsic rejected')
        return old(symbol)
    c.symbol_address=resolver;c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,module,'2','off',True)
    finally:c.symbol_address=old
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('590 C compilation failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('590 runtime differs')
    pins=ROOT/'evidence/verification/overlay-builder590-inputs-20261101.json'
    for item in json.loads(pins.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('590 frozen input differs',item['path']))
    H.WORK=WORK/'main-helper';helperRow,helperProof,mainBody=H.compile_unit(H.SOURCE,'caller',True);results=[];traces=[];profiles=P.profiles();negative=[]
    for module in M.UNITS:
        source=ROOT/f'nonmatching/overlay-lane/20261101-builder590/{module}/source.c';row,proof,body=compile_unit(source,module,module);original=M.inputs(module);cases=[];seen=set();deps=0;provided=0;registerDifferences=[];binaryZero=[];allWriteOrders=True
        for index,p in enumerate(profiles):
            native=M.Machine(original,p).run();candidate=M.Machine(original,p,body,mainBody).run();nm=P.model(native);cm=P.model(candidate)
            if nm!=cm:raise ValueError(('590 source/native semantic models differ',module,p['name']))
            for key in['mainCalls','providedCalls','tailForwardings']:
                if native[key]!=candidate[key]:raise ValueError(('590 measured argument contracts differ',module,p['name'],key))
            nw=[item[1:]for item in native['nonstackWrites']];cw=[item[1:]for item in candidate['nonstackWrites']];ordered=nw==cw;allWriteOrders&=ordered;seen.update(native['ownObserved']);count=len(native['nativeReturns'])+len(candidate['nativeReturns']);deps+=count;provided+=len(native['providedCalls'])*2;different=[i for i,(a,b)in enumerate(zip(native['coreRegistersAndCpsr'],candidate['coreRegistersAndCpsr']))if a!=b]
            if different:registerDifferences.append(dict(profile=p['name'],coreWordIndexes=different))
            if not nm['abstractCDefinedDivisionDomain']:binaryZero.append(p['name'])
            trace=dict(module=module,profile=p,model=nm,native={k:native[k]for k in['returnedWords','coreRegistersAndCpsr','nativeReturns','mainCalls','providedCalls','nonstackWrites','tailForwardings','ownObserved','helperObserved','instructions']},candidate={k:candidate[k]for k in['returnedWords','coreRegistersAndCpsr','nativeReturns','mainCalls','providedCalls','nonstackWrites','tailForwardings','ownObserved','helperObserved','instructions']},nativeFullAfterRamSha256=c.sha(native['after']),candidateFullAfterRamSha256=c.sha(candidate['after']),orderedWriteEffectsEqual=ordered,rawCoreDifferences=different);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualDependencyReturns=count,providedCalls=len(native['providedCalls'])*2,definedCModel=nm['abstractCDefinedDivisionDomain'],orderedWriteEffectsEqual=ordered,traceSha256=c.sha(encoded(trace))))
            if index%20==0:print(dict(module=module,completedPairs=index+1,total=len(profiles)),flush=True)
        expected=set(range(M.UNITS[module]['entry'],M.UNITS[module]['entry']+M.UNITS[module]['size']-4,4))
        if seen!=expected:raise ValueError(('590 native own instruction coverage differs',module,len(seen),len(expected)))
        template=source.read_text();variants=[('quotient',template.replace(' % ',' / ',1))]
        if module=='ov006':variants.append(('drop-stack-gap',template.replace('u8 arg6, u32 arg7, s32 arg8','u8 arg6, s32 arg8',1)))
        for name,wrong in variants:
            if wrong==template:raise ValueError('590 wrong source unchanged')
            d=ROOT/f'nonmatching/overlay-lane/20261101-builder590-controls/{module}-{name}';d.mkdir(parents=True,exist_ok=True);s=d/'source.c'
            if s.exists()and s.read_text()!=wrong:raise ValueError('590 frozen wrong source differs')
            s.write_text(wrong);s.with_name('context.h').write_bytes(source.with_name('context.h').read_bytes());wr,wp,wb=compile_unit(s,module,module+'-wrong-'+name);p=profiles[17];result=M.Machine(original,p,wb,mainBody).run()
            try:P.model(result)
            except ValueError as error:failure=str(error)
            else:raise ValueError('590 compiled wrong source escaped independent model')
            negative.append(dict(module=module,name=name,actualReturned=True,source=wr,genuineLinkComparison=wp,failure=failure,profile=p,returnedWords=result['returnedWords'],mainCalls=result['mainCalls'],nativeReturns=result['nativeReturns']))
        results.append(dict(module=module,processor='arm9',program='',mode='arm',address=hex(M.UNITS[module]['entry']),bytes=M.UNITS[module]['size'],source=row,genuineLinkComparison=proof,sourceCredit=0,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualDependencyReturns=deps,providedCalls=provided,nativeOwnObservedCodeBytes=len(seen)*4,nativeReferencedLiteralBytes=4,nativeLiteralEvidence=literal_evidence(original,M.UNITS[module],seen),orderedWritesEqual=allWriteOrders,rawCoreDifferences=registerDifferences,compiledZeroDenominatorPairs=binaryZero,cases=cases))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/overlay-builder590-functional-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],sourceCredit=0,groups=results,matchingSourceDependency=dict(source=helperRow,genuineLinkComparison=helperProof,newCredit=0),negativeEvidence=negative,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['Both larger source units remain nonmatching and gain zero exact-source bytes.','Only bounded synthetic descriptor/bank/slot/counter contexts are supplied; no allocation, rendering or ordinary scene claim.','The original and fresh linked candidate execute actual signed division, main49794 and native index/getter/counter helpers; only lower49BE4 is supplied with zero RAM effects.','Count0 cases are compiled binary evidence outside abstract C division/remainder semantics; count1..127 is finite target C. Counts128..255 and their potential signed-byte loop wrap remain unsupported.','The ov006 drafting signature preserves the observed unconsumed incoming SP+0xC slot before consumed SP+0x10, without claiming the original formal arity or an invented wide argument.','Source top return is a void view: every physical result/core difference is retained, not promoted to semantic return meaning.','A matching source dependency adds no new source credit, and its actual returns are already included in dependency totals.'])
    write_json(ROOT/'evidence/attempts/overlay-builder590-functional-drafts-20261101.json',report);print([dict(module=r['module'],pairs=r['callerPairs'],top=r['actualTopReturns'],dependencies=r['actualDependencyReturns'],provided=r['providedCalls'],sourceCredit=0)for r in results],flush=True)


if __name__=='__main__':execute()
