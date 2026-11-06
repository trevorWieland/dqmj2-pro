import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import match_ov001_float575_20261101 as S
import ov001_float578_machine_20261101 as M
import ov001_float578_models_20261101 as P
WORK=ROOT/'work/ol579-family'
SOURCES={0x0221239C:ROOT/'src/overlays/ov001_20261101_float579/variant_a.c',0x022125D0:ROOT/'src/overlays/ov001_20261101_float579/variant_b.c'}
PINS=ROOT/'evidence/verification/ov001-float579-inputs-20261101.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    previous=c.symbol_address
    def resolver(symbol):
        if symbol=='_s32_div_f':return M.M.DIV
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('579 unqualified compiler intrinsic rejected: '+symbol)
        return previous(symbol)
    c.symbol_address=resolver;c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,'ov001','2','off',True)
    finally:c.symbol_address=previous
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('579 compiler failed')
    row=rows[0];header=source.with_name(re.search(r'#include "([^"\n]+)"',source.read_text())[1]);row['sourceDependencies']=[dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes(),header


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('579 runtime differs')
    for row in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('579 input differs',row['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort107-identities-v2-20261101.json';accepted=json.loads(snapshot.read_text())['functions']
    for address,size in M.ENTRIES.items():
        if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov001'and max(r['address'],address)<min(r['address']+r['bytes'],address+size)for r in accepted):raise ValueError('579 accepted overlap')
    S.execute();standalone=json.loads((ROOT/'evidence/matches/ov001-20261101-float575.json').read_text());smallrow=standalone['matches'][0];smallbody=(S.WORK/'caller/link/caller.bin').read_bytes();original=M.M.inputs()
    if smallbody!=original['overlay'][M.M.ENTRY-M.M.OVERLAY:M.M.ENTRY-M.M.OVERLAY+M.M.SIZE]:raise ValueError('579 fresh reconstructed dependency differs')
    units={};matches=[smallrow]
    for address,source in SOURCES.items():
        row,proof,body,header=compile_unit(source,str(address),True)
        if body!=original['overlay'][address-M.M.OVERLAY:address-M.M.OVERLAY+M.ENTRIES[address]]:raise ValueError('579 fresh genuine bytes differ')
        row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=M.ENTRIES[address];units[address]=dict(row=row,body=body,header=header);matches.append(row)
    profiles=P.profiles();traces=[];cases={a:[]for a in SOURCES};seen={a:set()for a in SOURCES};smallSeen=set();totals={a:dict(watched=0,nested=0,sourceDependency=0,provided=0,powerForwardings=0,domain=0,binaryOnly=0)for a in SOURCES};controls=[]
    for p in profiles:
        address=p['entry'];n=M.Machine(original,p).run();nm=P.model(n);candidate=M.Machine(original,p,units[address]['body'],smallbody).run();cm=P.model(candidate)
        if nm!=cm or n['allArmCoreRegistersAndCpsr']!=candidate['allArmCoreRegistersAndCpsr']or n['nativeReturns']!=candidate['nativeReturns']or n['callEvents']!=candidate['callEvents']or n['powerTargetWords']!=candidate['powerTargetWords']or n['nonstackWrites']!=candidate['nonstackWrites']or n['after']!=candidate['after']:raise ValueError(('579 complete original/composed-source differs',p['name']))
        seen[address].update(n['ownObserved']);smallSeen.update(n['smallObserved']);watched=len(n['nativeReturns'])*2;nested=sum(r['scope']=='nested_math'for r in n['nativeReturns'])*2;stats=totals[address];stats['watched']+=watched;stats['nested']+=nested;stats['sourceDependency']+=2;stats['provided']+=nm['providedCalls']*2;stats['powerForwardings']+=len(n['powerTargetWords'])*2;stats['domain']+=int(p['sourceDomain']);stats['binaryOnly']+=int(not p['sourceDomain']);trace=dict(profile=p,model=nm,allArmCoreRegistersAndCpsr=n['allArmCoreRegistersAndCpsr'],returnedWords=n['returnedWords'],nativeReturns=n['nativeReturns'],callEvents=n['callEvents'],powerTargetWords=n['powerTargetWords'],nonstackWrites=n['nonstackWrites'],completeRamSha256=c.sha(n['after']),nativeInstructions=n['instructions'],composedCandidateInstructions=candidate['instructions'],largeObserved=n['ownObserved'],smallObserved=n['smallObserved']);traces.append(trace);cases[address].append(dict(profile=p['name'],actualTopReturns=2,actualWatchedDependencyReturns=watched,actualSmallDependencyReturnsSubset=2,providedCalls=nm['providedCalls']*2,sourceDomain=p['sourceDomain'],traceSha256=c.sha(encoded(trace))))
    for address,size in M.ENTRIES.items():
        if seen[address]!=set(range(address,address+size-12,4)):raise ValueError(('579 large code coverage differs',hex(address),len(seen[address])*4))
    for address,source in SOURCES.items():
        text=source.read_text();header=units[address]['header'];offset='0x28'if address==0x0221239C else'0x20';recipes=[('coordinate',text.replace('var_r7 += '+offset+';','var_r7 += '+hex(int(offset,0)+1)+';',1)),('header-field',text.replace('M2C_FIELD(arg0, s16 *, 0x26) = 0xA;','M2C_FIELD(arg0, s16 *, 0x26) = 0xB;',1)),('small-limit',text.replace('native_fn_ov001_022122ac(arg0, 7,','native_fn_ov001_022122ac(arg0, 6,',1))]
        for name,wrongText in recipes:
            if wrongText==text:raise ValueError('579 wrong source recipe absent')
            directory=ROOT/f'nonmatching/overlay-lane/20261101-float579-controls/{address:08x}/{name}';directory.mkdir(parents=True,exist_ok=True);wrongSource=directory/'source.c'
            if wrongSource.exists()and wrongSource.read_text()!=wrongText:raise ValueError('579 frozen wrong source differs')
            wrongSource.write_text(wrongText);wrongSource.with_name(header.name).write_bytes(header.read_bytes());wrongRow,wrongProof,wrongBody,unused=compile_unit(wrongSource,f'wrong-{address}-{name}',False);p=dict(name=f'wrong-{address}-{name}',entry=address,number=12345,secondary=123456,x=17,y=-1,flagsSet=True,sourceDomain=True);r=M.Machine(original,p,wrongBody,smallbody).run()
            try:P.model(r)
            except ValueError as error:failure=str(error)
            else:raise ValueError('579 wrong source escaped independent model')
            trace=dict(profile=p,actualReturned=True,returnedWords=r['returnedWords'],nativeReturns=r['nativeReturns'],callEvents=r['callEvents'],powerTargetWords=r['powerTargetWords'],nonstackWrites=r['nonstackWrites'],instructions=r['instructions'],failure=failure);controls.append(dict(name=name,address=hex(address),actualReturned=True,source=wrongRow,genuineLinkComparison=wrongProof,traceSha256=c.sha(encoded(trace)),failure=failure,trace=trace))
    raw=encoded(dict(cases=traces,wrongSources=[r['trace']for r in controls]));artifact=ROOT/'evidence/generated/ov001-float579-connected-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for r in controls:del r['trace']
    for address,unit in units.items():
        stats=totals[address];unit['row']['oracle']=dict(cases=len(cases[address]),actualTopReturns=len(cases[address])*2,actualNativeDependencyReturns=stats['watched'],nestedWatchedReturnsSubset=stats['nested'],actualSmallSourceDependencyReturnsSubset=stats['sourceDependency'],providedCalls=stats['provided'],actualPowerTargetForwardings=stats['powerForwardings'],sourceDomainPairs=stats['domain'],binaryOnlyPairs=stats['binaryOnly'],composedReconstructedSmallC=True,fullRamCoreRegistersCpsrAndOrderedWritesEqual=True,observedOwnInstructionBytes=len(seen[address])*4,referencedLiteralBytes=12,unclassifiedBytes=0,casesEvidence=cases[address],counting='Watched return total already includes nested math and the actual240-byte dependency; its candidate implementation is freshly linked C. Provided services are separate.')
    symbols={r['symbol']:r['target']for row in matches for r in row['relocations']}
    for row in matches:row['nativeSymbolEntries']=qualified_bindings(row)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleInputSha256=original['module']['sha256'],matches=matches,nativeSymbols=symbols,negativeEvidence=controls,standaloneSmallEvidence=dict(report='evidence/matches/ov001-20261101-float575.json',sha256=sha256(ROOT/'evidence/matches/ov001-20261101-float575.json'),includedAsFirstMatch=True,sourceCreditCountedOnce=True),connectedProof=dict(actualLargeTopReturns=len(profiles)*2,actualSmallDependencyReturnsSubset=len(profiles)*2,smallObservedInstructionBytes=len(smallSeen)*4,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw),uncompressedBytes=len(raw))),wholeModuleLinked=False,sourceReconstructionComplete=False,limitations=['Three source functions total1096 bytes; helper/runtime/data-table source is not credited.','Synthetic object fields/targets and four zero-RAM-effect UI service boundaries; no actual scene or widget initialization claim.','Finite primary-number domains keep measured byte-table accesses within0..9; six additional raw overflow/negative layout pairs are binary observations with C table extent/domain unproved.','Secondary full-word values execute actual freshly rebuilt240C dependency, including negative words; no fake parameter or supplied small-caller implementation.','Native FP execution is bounded by the frozen301-probe paths plus canonical signed division; general math semantics and original public typedefs remain unproved.','Raw coordinate, header selector, context+0x23 byte, field+0x10/+0x26 and target+0x7C effects have no inferred gameplay meaning.']);write_json(ROOT/'evidence/matches/ov001-20261101-float579-family.json',report);print(dict(functions=3,matchedBytes=1096,standaloneSmallTopReturns=smallrow['oracle']['actualTopReturns'],largeTopReturns=len(profiles)*2,watchedLargeDependencyReturns=sum(v['watched']for v in totals.values()),actualSmallDependencyReturnsSubset=len(profiles)*2,providedLargeCalls=sum(v['provided']for v in totals.values()),sourceDomainLargePairs=sum(v['domain']for v in totals.values()),binaryOnlyLargePairs=sum(v['binaryOnly']for v in totals.values()),wrongLargeActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
