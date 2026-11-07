import argparse
import hashlib
import json
import struct

import match_runtime
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261106_nns_primary_readonly_scout import intervals
from qualify_arm7_scoped_control import walk
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection


def main():
    parser=argparse.ArgumentParser();parser.add_argument('kind',choices=['channel','rtc']);args=parser.parse_args()
    lane,address,size,digest=('arm7-wl-channel-next',0x027e990c,652,'a0fa03ac0f2be9afabadcfdfd47798dd3681360a9f52a3a91f600309f1d825d0')if args.kind=='channel'else('arm7-rtc-loop-next',0x027f60b4,1156,'b94ce8832b55c9f90fc913ed3b1780ec496a7ecf3328b56041e48a8e606f2098')
    proposal_name=f'evidence/lanes/parallel-wave20261106/{lane}-proposal/proposal.json'
    assert sha256(ROOT/proposal_name)==digest;proposal=read_json(ROOT/proposal_name)
    for pin in proposal['actualInputPins']:assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    control_name='evidence/verification/arm7-channel-rtc-scoped-native-control-qualification-20261106.json';control=read_json(ROOT/control_name)
    assert control['passed']and control['positiveCases']==2 and control['negativeCases']==17 and not control['originalValidatorsChanged']
    assert sha256(ROOT/'qualify_arm7_scoped_control.py')==control['scopedQualifierSha256']
    assert sha256(ROOT/'qualify_arm7_scoped_control_cases.py')==control['caseGeneratorSha256']
    assert sha256(ROOT/'qualify_arm7_pm_mic_boundaries_v1_20261106.py')==control['originalReturnValidatorSha256']
    config=configuration();assert sha256(config['rom'])==config['romSha256'];rom=config['rom'].read_bytes()
    assert struct.unpack_from('<4I',rom,0x30)==(624640,0x02380000,0x02380000,160048)
    raw=rom[624640:624640+160048];assert struct.unpack_from('<3I',raw,160036)==(0x027e0000,96388,6504)
    image=raw[63636:160024];base=0x027e0000
    assert image==(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    assert hashlib.sha256(image).hexdigest()==proposal['nativeBoundary']['moduleSha256']
    import link_arm7_bulk_20261030 as linker
    modules,functions=linker.namespace('')
    assert address in functions and functions[address]['mode']=='arm'and functions[address]['module']=='arm7-main'
    assert not any(address<a<address+size for a,r in functions.items()if r['module']=='arm7-main')
    flow_name=f'evidence/lanes/parallel-wave20261106/{lane}-proposal/coordinator-scoped-flow.json'
    assert read_json(ROOT/flow_name)==proposal['nativeBoundary']['flow']
    row=dict(proposal['identity'],flow=dict(path=flow_name,sha256=sha256(ROOT/flow_name)),entryReachableInstructionBytes=proposal['nativeBoundary']['flow']['reachableInstructionBytes'],actualLiteralReadBytes=16,nativeSpanSha256=proposal['nativeBoundary']['targetSha256'])
    review=walk(row,image,base,args.kind)
    ledger=[json.loads(line)for line in(ROOT/'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines()]
    original=next(r for r in ledger if r['id']==row['id']);assert not original['states']['functionMatched']and not original.get('sourceUnit')and original['bytes']is None
    protection=list(intervals([r for r in ledger if r['states']['functionMatched']or r.get('sourceUnit')]))
    pins=[]
    for path in sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json'))):
        protection.extend(intervals(read_json(path)));pins.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))
    for name,key in [('ledger/data.json','records'),('ledger/linkage.json','regions')]:protection.extend(intervals(read_json(ROOT/name)[key]));pins.append(dict(path=name,sha256=sha256(ROOT/name)))
    assert not any((p,c,m)==('','arm7','arm7-main')and max(a,address)<min(b,address+size)for p,c,m,a,b in protection)
    primary=proposal['primarySource'];data=(ROOT/primary['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==primary['sha256']and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==primary['gitBlob']
    assert hashlib.sha256(proposal['publishedFunction']['publishedText'].encode()).hexdigest()==proposal['publishedFunction']['bodySha256']
    context=proposal['sourceCompilerContext'];assert sha256(ROOT/context['compiler'])==context['compilerSha256']
    diagnostic=proposal['actualPrimaryElf'];assert not diagnostic['objectUsedAsImplementationInput']and sha256(ROOT/diagnostic['object']['path'])==diagnostic['object']['sha256']
    with(ROOT/diagnostic['object']['path']).open('rb')as stream:
        elf=ELFFile(stream);symbols=elf.get_section_by_name('.symtab');symbol=symbols.get_symbol_by_name(diagnostic['function'])[0]
        assert symbol['st_info']['type']=='STT_FUNC'and symbol['st_size']==size
        section_id=symbol['st_shndx'];section=elf.get_section(section_id);offset=symbol['st_value']-section['sh_addr']
        assert section['sh_flags']&4 and any(s.name=='$a'and s['st_shndx']==section_id and s['st_value']==symbol['st_value']for s in symbols.iter_symbols())
        compiled=bytearray(section.data()[offset:offset+size]);native=bytearray(image[address-base:address-base+size]);relocations=[]
        for sec in elf.iter_sections():
            if not isinstance(sec,RelocationSection)or sec['sh_info']!=section_id:continue
            for r in sec.iter_relocations():
                at=r['r_offset']-offset
                if not 0<=at<size:continue
                expected=next(e for e in diagnostic['actualElfRelocations']if e['offset']==at)
                assert r['r_info_type']==expected['type']in(1,2)and r['r_addend']==expected['explicitAddend']and at%4==0
                value=struct.unpack_from('<I',native,at)[0];assert value==int(expected['nativeWord'],0)
                if r['r_info_type']==1:
                    assert value>>24==0xeb;disp=value&0xffffff;disp-=0x1000000 if disp&0x800000 else 0
                    target=address+at+8+disp*4;assert target==int(expected['nativeTarget'],0)and target in functions and functions[target]['mode']=='arm'
                elif args.kind=='channel':assert value in(0x027f4e7c,0x027f4e1c)and value in functions and functions[value]['mode']=='arm'
                else:assert value in(0x027f8e34,0x027f8e38,0x027f8f34)
                relocations.append(at);compiled[at:at+4]=bytes(4);native[at:at+4]=bytes(4)
        assert len(relocations)==len(set(relocations))==len(diagnostic['actualElfRelocations'])and compiled==native
        assert size-4*len(relocations)==diagnostic['matchedNonRelocationBytes']==diagnostic['comparableNonRelocationBytes']
        if args.kind=='rtc':
            work=symbols.get_symbol_by_name('rtcWork')[0];assert work['st_info']['bind']=='STB_LOCAL'and work['st_size']==948 and work['st_value']==4
    if args.kind=='rtc':
        supplement_name='evidence/lanes/parallel-wave20261106/arm7-rtc-loop-next-proposal/native-interface-supplement-v1.json'
        assert sha256(ROOT/supplement_name)=='96825665767329b0a792de38a8526217d687be5dcdffb39bd28618030b8e4441'
        assert struct.unpack_from('<I',image,0x027f5f24-base)[0]==address
        call=struct.unpack_from('<I',image,0x027f5eb0-base)[0];assert call>>24==0xeb
        disp=call&0xffffff;disp-=0x1000000 if disp&0x800000 else 0
        assert 0x027f5eb0+8+disp*4==0x037fc054
        assert base+96388<=0x027f8e34 and 0x027f8e38+948==base+96388+6504
        assert not proposal['globalScope']['nativeFullWorkAllocationProven']and proposal['globalScope']['sourceDefinedStorage']==0
    assert all(sha256(ROOT/p['path'])==p['sha256']for p in pins)
    folder=ROOT/f'evidence/lanes/parallel-wave20261106/{lane}';assert not folder.exists()
    assert not(ROOT/proposal['proposedSourceRoot']).exists()and not(ROOT/proposal['proposedWorkRoot']).exists()and not list(ROOT.glob(proposal['proposedHelperPrefix']+'*.py'))
    claim_name=(folder/'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT/claim_name,dict(owner='ds_tooling_research',status='coordinator-admitted-source-scope-no-credit',sourceCredit=0,createdUtc=now(),
        exclusiveSourceRoot=proposal['proposedSourceRoot'],exclusiveWorkRoot=proposal['proposedWorkRoot'],helperPrefix=proposal['proposedHelperPrefix'],
        claimedFunctions=[dict(proposal['identity'],targetSha256=proposal['nativeBoundary']['targetSha256'],physicalFlow=row['flow'],binary=proposal['nativeBoundary']['module'],base=base)],
        importedGlobalView=proposal['globalScope'],scopedNativeControl=proposal['scopedControlQualification'],sourceDefinedStorage=0,
        experimentBudget='One authenticated actual primary context; genuine C external typed views before compile; no BSS/local rebinding, object patches, profile or register grids. Stop on nonmatch/unresolved layout. Full bounded behavior, links, negatives and copied-root proof before Ready.'))
    write_json(folder/'coordinator-admission.json',dict(passed=True,sourceCredit=0,functions=1,initializedCandidateBytes=size,claim=claim_name,claimSha256=sha256(ROOT/claim_name),
        exclusiveSourceRoot=proposal['proposedSourceRoot'],sharedDispatchUnchanged=True,actualDispatchSha256=sha256(ROOT/'evidence/lanes/parallel-wave20261102/dispatch.json'),
        proposal=dict(path=proposal_name,sha256=digest),protectionPins=pins,independentNativeReview=review,scopedQualification=control_name,scopedQualificationSha256=sha256(ROOT/control_name),
        originalReturnValidatorChanged=False,globalLedgerBoundaryPromoted=False,storageAndProviderCredit=0,sourceBoundaryCodeShapeStillUnproved=True,generatorSha256=sha256(__file__)))
    print(dict(passed=True,kind=args.kind,functions=1,bytes=size,sourceCredit=0))


if __name__=='__main__':main()
