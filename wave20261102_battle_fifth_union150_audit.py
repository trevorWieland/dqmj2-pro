import sys
sys.dont_write_bytecode=True
import collections
import hashlib
import json
import re
from pathlib import Path

from project import ROOT,read_json,write_json,sha256,configuration
sys.path.insert(0,str(ROOT/'deps/native'))
from elftools.elf.elffile import ELFFile

SPEC='cohort150-parallel-wave20261102-following-specification.json'
CONFIG='provenance/parallel-wave20261102-following-packets.json'
MANIFEST='provenance/cohort150-parallel-wave20261102-following-source-files.json'
OUT='evidence/lanes/parallel-wave20261102/battle-fifth/union150-audit.json'


def number(value):
    return int(value,0)if isinstance(value,str)else int(value)


def identity(row):
    return(row.get('program')or'',row['processor'],row['module'],row['mode'],number(row['address']),number(row['bytes']))


def namespace(key):
    return key[:3]


def overlap(first,second):
    return namespace(first)==namespace(second)and first[4]<second[4]+second[5]and second[4]<first[4]+first[5]


def main():
    rom=configuration()['romSha256']
    cache={}
    watched={}
    def digest(name):
        path=Path(name)
        if not path.is_absolute():path=ROOT/path
        path=path.resolve()
        assert path.is_relative_to(ROOT)and path.is_file(),str(path)
        key=path.relative_to(ROOT).as_posix()
        if key not in cache:cache[key]=sha256(path)
        return cache[key]
    def pin(value):
        assert digest(value['path'])==value['sha256'],value['path']
    def watch(name):
        watched[name]=digest(name)
    def mandatory_closure(initial):
        pending=list(initial)
        found={}
        while pending:
            value=pending.pop(0)
            pin(value)
            name=Path(value['path']).as_posix()
            if name in found:
                assert found[name]==value['sha256']
                continue
            found[name]=value['sha256']
            if name.endswith('.json'):
                value=read_json(ROOT/name)
                if isinstance(value,dict):pending.extend(value.get('mandatoryExternalInputs',[]))
        return found
    for name in[SPEC,CONFIG,MANIFEST,'source-map.json','recovery.json','project.json']:
        watch(name)
    spec=read_json(ROOT/SPEC)
    config=read_json(ROOT/CONFIG)
    selected=read_json(ROOT/'source-map.json')
    receipt149=read_json(ROOT/'evidence/verification/cohort-2026-10-29-149.json')
    assert spec['cohort']==config['cohort']==150 and spec['previousAcceptedCohort']==149
    assert not spec['migrations'] and spec['originalChecksRetained']
    assert len(config['readyPackets'])==len(spec['packets'])==5
    assert selected['buildSha256']==rom and len(selected['matchedFunctions'])==receipt149['sourceMatchedFunctions']==9920
    assert receipt149['linksPending']is False and receipt149['moduleComparisonsExact']==20
    expected={identity(row)for row in spec['expectedAdditions']}
    assert len(expected)==len(spec['expectedAdditions'])==95 and sum(key[5]for key in expected)==27280
    baseline=[identity(row)for row in selected['matchedFunctions']]
    owner={}
    all_rows=[]
    summaries=[]
    produced=set()
    immutable_inputs={}
    anchor_count=0
    relocation_count=0
    maximum_lines=0
    absent_canonical=[]
    for ready_name,packet in zip(config['readyPackets'],spec['packets']):
        watch(ready_name)
        ready=read_json(ROOT/ready_name)
        assert ready['status']=='ready-for-coordinator-acceptance'and ready['romSha256']==rom
        assert len(ready['packets'])==1
        source_packet=ready['packets'][0]
        produced.update([source_packet['report'],packet['report']])
        assert packet['producer'][0]=='replay_parallel_packet.py'and not packet['directProducer']
        descriptor_name=packet['producer'][1]
        watch(descriptor_name)
        descriptor=read_json(ROOT/descriptor_name)
        assert descriptor['romSha256']==rom and descriptor['producer']==source_packet['producer']
        assert descriptor['workerReport']==source_packet['report']and descriptor['canonicalReport']==packet['report']
        assert source_packet['producer']and all(isinstance(item,str)for item in source_packet['producer'])
        assert source_packet['producer'][0].endswith('.py')and(ROOT/source_packet['producer'][0]).is_file()
        pin(ready['canonicalDescriptor'])
        original_descriptor=read_json(ROOT/ready['canonicalDescriptor']['path'])
        assert original_descriptor['producer']==descriptor['producer']
        direct={value['path']:value['sha256']for value in descriptor['frozenInputs']}
        closure=mandatory_closure(descriptor['frozenInputs'])
        assert direct==closure,'Mandatory replay inputs are not all directly pinned'
        inherited=mandatory_closure(original_descriptor['frozenInputs'])
        assert inherited.items()<=direct.items()
        immutable_inputs.update(direct)
        for value in ready['files']:
            if value['path']!=source_packet['report']:pin(value)
        report=read_json(ROOT/source_packet['report'])
        assert report['romSha256']==rom and not report.get('failed')and report.get('allPassed')is not False
        rows=report['matches']
        keys={identity(row)for row in rows}
        assert len(keys)==len(rows)==ready['functions']and sum(row['bytes']for row in rows)==ready['bytes']
        assert keys=={identity(row)for row in descriptor['identities']}=={identity(row)for row in ready['identities']}
        assert keys=={identity(row)for row in original_descriptor['identities']}
        descriptor_rows={identity(row):row for row in descriptor['identities']}
        existing=ROOT/packet['report']
        if existing.is_file():
            canonical=read_json(existing)
            assert {identity(row)for row in canonical['matches']}==keys
            assert {(identity(row),row['sourceSha256'],row['targetSha256'])for row in canonical['matches']}=={(identity(row),row['sourceSha256'],row['targetSha256'])for row in rows}
        else:absent_canonical.append(packet['report'])
        for row in rows:
            key=identity(row)
            assert key not in owner and key[0]in['','dwc/utility.bin/move/child.srl']
            owner[key]=ready_name
            assert row['processor']in['arm7','arm9']and row['mode']=='arm'
            assert row['exactAfterDeclaredRelocation']and row['bytes']==row['compiledBytes']
            assert Path(row['source']).suffix=='.c'and not row.get('originalObjectScaffolding',False)
            assert row.get('ordinaryFunctionCredit',1)==1 and row.get('ordinaryCBytes',row['bytes'])==row['bytes']
            assert row.get('originalDataSourceCredit',0)==row.get('justifiedAssemblyBytes',0)==0
            source=descriptor_rows[key]
            assert source['source']==row['source']and source['sourceSha256']==row['sourceSha256']and source['targetSha256']==row['targetSha256']
            for value in[dict(path=row['source'],sha256=row['sourceSha256']),*row.get('sourceDependencies',[])]:
                pin(value)
                text=(ROOT/value['path']).read_text(encoding='utf-8')
                maximum_lines=max(maximum_lines,len(text.splitlines()))
                assert len(text.splitlines())<=500 and not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|/\*|//',text)
            assert digest(row['object'])==row['objectSha256']
            assert digest(row.get('compilerPath',row.get('compiler')))==row['compilerSha256']
            flags=row['compilerFlags']
            processor=[flags[index+1]for index,value in enumerate(flags)if value=='-proc'][-1]
            assert processor==('arm7tdmi'if row['processor']=='arm7'else'arm946e')
            proof=row['realLink']
            assert proof['exactCallerBytes']and proof['splitPreservesRelocationTypesAddendsAndEncodedHBits']
            assert proof['calleeCodeOrSourceCredit']==0
            for name,value in proof.items():
                if re.search(r'callee.*credit',name,re.I):assert value==0
            assert proof['linkedCallerSha256']==proof['nativeSpanSha256']==row['targetSha256']
            assert digest(proof['linkedElf'])==proof['linkedElfSha256']and digest(proof['lcf'])==proof['lcfSha256']
            caller=(ROOT/proof['lcf']).parent/'caller.bin'
            assert len(caller.read_bytes())==row['bytes']and digest(caller)==row['targetSha256']
            assert proof['linkerAttempt']['exitCode']==0 and digest(proof['linkerAttempt']['command'][0])==proof['linkerSha256']
            relocation_count+=len(proof['originalRelocations'])
            for binding in proof.get('bindings',proof.get('bindingOnlyProbes',[])):
                assert binding.get('processor',row['processor'])==row['processor']
                assert(binding.get('program')or'')==(row.get('program')or'')
                if binding.get('kind')!='function':continue
                assert binding['initializedCodeBytes']==binding['nativeCalleeBytesUsed']==binding['calleeSourceCredit']==0
                path=binding.get('anchorObject',binding.get('object'))
                assert digest(path)==binding.get('anchorObjectSha256',binding.get('objectSha256'))
                with (ROOT/path).open('rb')as stream:
                    elf=ELFFile(stream)
                    symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
                    symbol=next(value for value in symbols if value.name==binding['name'])
                    assert symbol['st_info']['type']=='STT_FUNC'and symbol['st_size']==0
                    assert not any(section['sh_flags']&2 and section['sh_type']!='SHT_NOBITS'and section['sh_size']for section in elf.iter_sections())
                anchor_count+=1
            all_rows.append(row)
        summaries.append(dict(ready=ready_name,readySha256=digest(ready_name),functions=len(rows),bytes=sum(row['bytes']for row in rows),rootDescriptor=descriptor_name,directMandatoryInputs=descriptor['frozenInputs'],primaryProducedReport=source_packet['report'],canonicalReportPresentAtPreparation=existing.is_file()))
    actual=set(owner)
    assert actual==expected
    conflicts=[dict(first=owner[first],second=owner[second],firstIdentity=first,secondIdentity=second)for index,first in enumerate(actual)for second in list(actual)[:index]if overlap(first,second)]
    prior=[dict(packet=owner[key],identity=key,selected149=other)for key in actual for other in baseline if overlap(key,other)]
    assert not conflicts and not prior
    manifest=read_json(ROOT/MANIFEST)
    assert manifest['sourceCredit']==0 and manifest['producedReportPinsDescribePreSealHandoff']and not manifest['executableInputsCommitted']
    staged={value['path']:value['sha256']for value in manifest['files']+manifest['privateComparisonInputs']}
    for name,digest_value in immutable_inputs.items():assert staged.get(name)==digest_value
    for value in manifest['files']+manifest['privateComparisonInputs']:
        if value['path']not in produced:pin(value)
    for row in all_rows:
        assert staged[row['source']]==row['sourceSha256']
        for value in row.get('sourceDependencies',[]):assert staged[value['path']]==value['sha256']
    assert all(sha256(ROOT/name)==value for name,value in watched.items()),'Prepared union/baseline changed during audit'
    groups=collections.defaultdict(lambda:[0,0])
    for key in actual:
        groups[key[:3]][0]+=1
        groups[key[:3]][1]+=key[5]
    result=dict(schemaVersion=1,passed=True,sourceCredit=0,readOnly=True,producerReruns=0,registrySpecSourceIndexMutations=0,specification=dict(path=SPEC,sha256=digest(SPEC)),configuration=dict(path=CONFIG,sha256=digest(CONFIG)),sourceManifest=dict(path=MANIFEST,sha256=digest(MANIFEST)),baseline149=dict(selectedFunctionCount=9920,sourceMapSha256=watched['source-map.json'],receipt='evidence/verification/cohort-2026-10-29-149.json'),packetCount=5,functions=95,bytes=27280,expectedAdditionsExactlyEqualCanonicalIdentityUnion=True,fullProgramCpuModuleModeIdentitiesPreserved=True,overlapChecksIgnoreModeWithinSamePhysicalNamespace=True,interPacketConflicts=conflicts,selected149Conflicts=prior,packets=summaries,namespaceTotals=[dict(program=key[0],processor=key[1],module=key[2],functions=value[0],bytes=value[1])for key,value in sorted(groups.items())],immutableDirectMandatoryInputsVerified=len(immutable_inputs),stagedAuthoredOrMetadataPins=len(manifest['files']),privateComparisonPins=len(manifest['privateComparisonInputs']),completeGenuineCallerSpansVerified=95,originalRelocationRecords=relocation_count,zeroInitializedCodeTypedFunctionAnchors=anchor_count,calleeAndOriginalScaffoldingSourceCredit=0,maximumSourceOrHeaderLines=maximum_lines,canonicalReportsNotYetGeneratedAtPreparation=absent_canonical,guardedInputHashesUnchanged=watched,generator=dict(path=Path(__file__).name,sha256=sha256(__file__)),limits=['Static independent intake/physical-union verification only; individual dynamic/model qualification remains in the linked packet receipts.','Missing future cohort canonical reports are expected at preparation: their frozen descriptors fully declare the identity/source/native-span set and true producers; shared replay must regenerate them before sealing.','This receipt grants no accepted bytes and does not establish shared module links, exact ROM packaging, committed closure, a full cold replay or platform execution.'])
    write_json(ROOT/OUT,result)
    print(dict(passed=True,packets=5,functions=95,bytes=27280,anchors=anchor_count,relocations=relocation_count,receipt=OUT))


if __name__=='__main__':
    main()
