import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,sha256,write_json
import arm7_runtime
import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_CALL,CS_GRP_JUMP
from capstone.arm import ARM_OP_MEM,ARM_REG_PC
from wave20261105_arm7_boundary_next_flow import analyze,union,overlap,rows
LANE=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next'
WORK=ROOT/'work/w5ab'
NAMESPACE=('', 'arm7','arm7-main')
ENTRY=0x027e0898


def pin(name):return dict(path=name,sha256=sha256(ROOT/name))


def committed(revision,name):return subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT)


def number(value):return int(value,0) if isinstance(value,str) else int(value)


def scope(row,parent=None):
    parent=parent or {}
    return row.get('program',parent.get('program')) or '',row.get('processor',parent.get('processor')),row.get('module',parent.get('module'))


def protected_intersections(begin,end,protections):
    return [dict(record=p,intersection=dict(start=hex(max(begin,p['start'])),endExclusive=hex(min(end,p['end'])),bytes=min(end,p['end'])-max(begin,p['start']))) for p in protections if tuple(p['namespace'])==NAMESPACE and max(begin,p['start'])<min(end,p['end'])]


def protections(revision,frontier):
    values=[];pins=[];rawLedger=committed(revision,'ledger/functions.jsonl')
    if hashlib.sha256(rawLedger).hexdigest()!=frontier['committedLedgerSha256']:raise ValueError('Committed159 native ledger differs from frontier')
    def add(row,kind,parent=None):
        identity=scope(row,parent)
        if identity!=NAMESPACE:return
        size=row.get('storedBytes',row.get('bytes'))
        if not size or not row.get('address'):return
        address=number(row['address']);values.append(dict(namespace=list(identity),start=address,end=address+size,kind=kind,id=row.get('id'),address=row['address'],bytes=size))
    ledger=[json.loads(line) for line in rawLedger.splitlines()]
    for r in ledger:add(r,'accepted-native-function-or-pool' if r['states']['functionMatched'] else 'existing-positive-native-function-extent')
    for name,key in [('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        raw=committed(revision,name);pins.append(dict(gitObject=revision+':'+name,sha256=hashlib.sha256(raw).hexdigest()))
        for r in json.loads(raw)[key]:
            if not r.get('processor') and r.get('module')=='arm7-main':r=dict(r,processor='arm7')
            add(r,'committed-native-data-storage' if key=='records' else 'committed-linker-physical-region')
    atlasName='work/parallel-wave20261102/atlas/atlas.json'
    if sha256(ROOT/atlasName)!=frontier['inputPins'][atlasName]:raise ValueError('Frozen159 atlas input changed')
    pins.append(pin(atlasName));atlas=read_json(ROOT/atlasName)
    if atlas['sourceCommit']!=revision:raise ValueError('Atlas accepted epoch differs')
    module=next(m for m in atlas['modules'] if (m.get('program') or '',m['processor'],m['name'])==NAMESPACE)
    for offset,size,category in module['regions']:
        if category in [1,2,3,4,5]:values.append(dict(namespace=list(NAMESPACE),start=module['base']+offset,end=module['base']+offset+size,kind='accepted-atlas-physical-category-'+str(category),bytes=size))
    files=sorted((ROOT/'evidence/lanes').rglob('claim.json'));unparsed=[];broad=[]
    for path in files:
        name=path.relative_to(ROOT).as_posix();pins.append(pin(name));claim=read_json(path);items=claim.get('claimedFunctions',claim.get('functions'))
        if not isinstance(items,list):
            if scope(claim)==NAMESPACE:unparsed.append(dict(path=name,reason='No explicit function ownership list'))
            continue
        for item in items:
            if isinstance(item,dict):
                r=dict(item)
                if not r.get('address') and r.get('id'):
                    try:r['address']=hex(int(r['id'].rsplit('/',1)[-1],16))
                    except ValueError:pass
                before=len(values);add(r,'existing-reserved-function',claim)
                if len(values)>before:values[-1]['claim']=name
                elif scope(r,claim)==NAMESPACE and not r.get('address'):unparsed.append(dict(path=name,reason='Unparsed explicit ARM7 ownership row'))
            elif scope(claim)==NAMESPACE:unparsed.append(dict(path=name,reason='Nonobject ARM7 function ownership row'))
        if scope(claim)==NAMESPACE and claim.get('regionStart') and claim.get('regionEndExclusive'):broad.append(dict(path=name,start=claim['regionStart'],endExclusive=claim['regionEndExclusive'],interpretation='Collection/discovery envelope retained separately; exact listed function extents are protected, matching existing frontier parser. Coordinator must independently confirm ownership before source admission.'))
    pending=[]
    for path in sorted((ROOT/'provenance').glob('cohort16[012]-*specification*.json')):
        pins.append(pin(path.relative_to(ROOT).as_posix()));value=read_json(path)
        def visit(node):
            if isinstance(node,dict):
                if scope(node)==NAMESPACE and node.get('address') and node.get('bytes'):
                    add(node,'pending-cohort-physical-extent');pending.append(node['address'])
                for child in node.values():visit(child)
            elif isinstance(node,list):
                for child in node:visit(child)
        visit(value)
    return values,pins,dict(committedLedger=dict(gitObject=revision+':ledger/functions.jsonl',sha256=hashlib.sha256(rawLedger).hexdigest()),claimFiles=len(files),claimPathSet=sorted(p.relative_to(ROOT).as_posix() for p in files),unparsedArm7Claims=unparsed,broadHistoricalCollectionEnvelopes=broad,pendingArm7ExtentRows=pending,physicalRows=len(values),acceptedAtlasBytes=module['acceptedBytes'])


def certificate(flow,image,base,expectedHash):
    start=int(flow['entry'],0);end=int(flow['computedEvidenceEndExclusive'],0)
    if flow['entryMode']!='arm' or flow['architecture']!='ARMv4T' or not flow['completePhysicalEvidence'] or flow['unresolved'] or flow['unaccountedRanges']:raise ValueError('ARMv4T physical flow evidence incomplete')
    body=image[start-base:end-base]
    if C.sha(body)!=expectedHash or len(body)!=flow['computedEvidenceEnvelopeBytes']:raise ValueError('Original full evidence span/hash differs')
    mask=bytearray(len(body));instructionAddresses=set()
    for item in flow['instructions']:
        address=int(item['address'],0);word=image[address-base:address-base+4]
        if item['mode']!='arm' or item['hex']!=word.hex() or int(item['word'],0)!=int.from_bytes(word,'little'):raise ValueError('Actual ARM instruction identity differs')
        instructionAddresses.add(address)
        for at in range(address,address+4):mask[at-start]|=1
    for item in flow['literalReads']:
        address=int(item['address'],0);size=item['bytes'];word=image[address-base:address-base+size]
        if address<start or address+size>end or item['hex']!=word.hex() or item['value']!=hex(int.from_bytes(word,'little')):raise ValueError('Actual bounded literal-read identity differs')
        origin=int(item['origin'],0);decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;instruction=next(decoder.disasm(image[origin-base:origin-base+4],origin,count=1),None)
        if origin not in instructionAddresses or instruction is None or not instruction.mnemonic.startswith('ldr') or not any(o.type==ARM_OP_MEM and o.mem.base==ARM_REG_PC and not o.mem.index and origin+8+o.mem.disp==address for o in instruction.operands):raise ValueError('Literal-read original instruction/origin differs')
        width=1 if instruction.mnemonic.startswith('ldrb') else 2 if instruction.mnemonic.startswith(('ldrh','ldrsh')) else 4
        if width!=size:raise ValueError('Literal-read original access width differs')
        for at in range(address,address+size):mask[at-start]|=2
    if set(mask)-{1,2} or mask.count(1)!=flow['reachableInstructionBytes'] or mask.count(2)!=flow['literalReadBytes']:raise ValueError('Instruction/literal physical byte union does not close exactly')
    if set(instructionAddresses)!=set(a for r in flow['instructionRanges'] for a in range(int(r['start'],0),int(r['endExclusive'],0),4)):raise ValueError('Instruction range union differs from actual reachable instructions')
    return dict(status='passed',sourceCredit=0,start=hex(start),endExclusive=hex(end),bytes=len(body),nativeSpanSha256=C.sha(body),instructionBytes=mask.count(1),literalBytes=mask.count(2),overlapOrUnclassifiedBytes=0,nextEntryUsedToInferSize=False,mode='arm',architecture='ARMv4T')


def outside_references(layout,inventory,begin,end):
    binaries={m['id']:(ROOT/m['binary']).read_bytes() for m in layout['modules']};modules={m['id']:m for m in layout['modules']};direct=[];words=[]
    for function in inventory['functions']:
        if function['mode'] not in ['arm','thumb']:continue
        module=modules[function['module']];base=int(module['base'],0);raw=binaries[function['module']];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM if function['mode']=='arm' else CS_MODE_THUMB);decoder.detail=True
        for first,last in function['ranges']:
            first,last=int(first,0),int(last,0)
            for i in decoder.disasm(raw[first-base:last-base],first):
                if module['id']=='arm7-main' and begin<=i.address<end:continue
                if not(i.group(CS_GRP_CALL) or i.group(CS_GRP_JUMP)) or not i.operands or i.operands[0].type!=2:continue
                target=i.operands[0].imm&~1
                if begin<=target<end:direct.append(dict(module=module['id'],sourceRoot=function['address'],origin=hex(i.address),target=hex(target),mode=function['mode']))
    for module in layout['modules']:
        base=int(module['base'],0);raw=binaries[module['id']]
        for offset in range(0,len(raw)-3,4):
            origin=base+offset;value=int.from_bytes(raw[offset:offset+4],'little');target=value&~1
            if module['id']=='arm7-main' and begin<=origin<end:continue
            if begin<=target<end:words.append(dict(module=module['id'],origin=hex(origin),word=hex(value),canonicalTarget=hex(target),lowBit=value&1))
    interiors=[r for r in direct if int(r['target'],0)!=begin]+[r for r in words if int(r['canonicalTarget'],0)!=begin]
    return dict(status='passed' if not interiors else 'ambiguous',outsideDirectFlow=direct,outsideAlignedInitializedWords=words,interiorOrPoolEntries=interiors,scope='Only canonical host ARM7 bootstrap/WRAM/main; ARM9 and child programs are separate namespaces',limitations=['Configured Ghidra ranges/modes are a conservative direct-flow scan, not independent proof of every other function boundary/mode. Aligned initialized-word scan does not rule out opaque computed pointer producers.'])


def sdk_witnesses():
    name='evidence/tools/public-sdk-reference-acquisition-20261101.json';acquisition=read_json(ROOT/name);sdk=next(r for r in acquisition['references'] if r['repository']=='ntrtwl/NitroSDK');files=[]
    suffixes=['/libraries/wm/src/ARM7/wmsp_indicate.c','/libraries/wm/src/ARM7/wmsp_system.c','/libraries/wm/include/ARM7/wmsp_private.h']
    for suffix in suffixes:
        record=next(r for r in sdk['unmodifiedFiles'] if r['path'].endswith(suffix));raw=(ROOT/record['path']).read_bytes()
        if C.sha(raw)!=record['sha256'] or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=record['gitBlobSha1']:raise ValueError('Pinned primary SDK source/git blob changed')
        files.append(record)
    return dict(repository=sdk['repository'],revision=sdk['revision'],acquisition=pin(name),tree=dict(path=sdk['tree'],sha256=sdk['treeSha256']),files=files,correspondence='WMSP_IndicateThread receives fromWLmsgQ, tests WlCmdReq header code at12/group and0x80, dispatches indication handling, otherwise sends confirmQ. WM_sp_init passes that entry to OS_CreateThread. Native original call/literal/field records independently support this qualified correspondence.',historicalExactSDKVersionProved=False,sourceMatchProved=False,compilerInputsAdopted=False,sourceCredit=0)


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next' or WORK!=ROOT/'work/w5ab':raise ValueError('New ARM7 read-only evidence/work paths changed')
    LANE.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
    frontierName='evidence/verification/source95-frontier-20261105.json';frontier=read_json(ROOT/frontierName);revision=frontier['sourceRevision']
    closureName='evidence/verification/cohort159-expanded-source-closure-20261101.json'
    if frontier['acceptedCohort']!=159 or not json.loads(committed(revision,closureName))['passed']:raise ValueError('Closed159 accepted source epoch unavailable')
    conf=configuration();rom=conf['rom'].read_bytes()
    if C.sha(rom)!=conf['romSha256']:raise ValueError('Authoritative original ROM changed')
    offset,entryAddress,load,size=struct.unpack_from('<4I',rom,0x30);original=rom[offset:offset+size];layout=arm7_runtime.derive(original)
    if layout!=read_json(ROOT/'evidence/arm7/runtime-layout.json'):raise ValueError('ARM7 original-ROM loader mapping differs')
    for module in layout['modules']:
        if sha256(ROOT/module['binary'])!=module['sha256']:raise ValueError('Original ARM7 runtime module changed')
    module=next(m for m in layout['modules'] if m['id']=='arm7-main');base=int(module['base'],0);image=original[module['inputFileOffset']:module['inputFileOffset']+module['bytes']]
    inventoryName='evidence/arm7/ghidra-runtime-inventory.json';raw=committed(revision,inventoryName);inventory=json.loads(raw)
    if C.sha(raw)!=sha256(ROOT/inventoryName):raise ValueError('Original canonical ARM7 Ghidra inventory epoch changed')
    entry=next(r for r in inventory['functions'] if r['module']=='arm7-main' and int(r['address'],0)==ENTRY)
    entries=[int(r['address'],0) for r in inventory['functions'] if r['module']=='arm7-main'];flow=analyze(image,base,ENTRY);end=int(flow['computedEvidenceEndExclusive'],0);nativeHash=C.sha(image[ENTRY-base:end-base]);proof=certificate(flow,image,base,nativeHash)
    if flow['instructionRanges']!=[dict(start=a,endExclusive=b,bytes=int(b,0)-int(a,0)) for a,b in entry['ranges']]:raise ValueError('Independent ARM flow and old discontiguous body union disagree')
    protected,pins,protectionInputs=protections(revision,frontier);hits=protected_intersections(ENTRY,end,protected);outside=outside_references(layout,inventory,ENTRY,end)
    sdk=sdk_witnesses();generatorSources=[pin(name) for name in [Path(__file__).name,'wave20261105_arm7_boundary_next_flow.py','wave20261105_arm7_boundary_next_controls.py','arm7_runtime.py','project.py','match_runtime.py']];pins += [pin(frontierName),pin(inventoryName),pin('project.json'),pin('provenance/seed-manifest.json'),pin('evidence/arm7/runtime-layout.json'),pin('evidence/lanes/parallel-wave20261102/native-backlog/boundary-work.json'),*sdk['files'],*generatorSources]
    from wave20261105_arm7_boundary_next_controls import execute as negative_controls
    controls=negative_controls(image,base,entries,flow,nativeHash)
    if hits or protectionInputs['unparsedArm7Claims'] or outside['interiorOrPoolEntries']:raise ValueError(('Boundary proposal intersects ownership/storage or incoming aliases',hits,protectionInputs['unparsedArm7Claims'],outside['interiorOrPoolEntries']))
    for record in pins:
        if 'path' in record:
            if sha256(ROOT/record['path'])!=record['sha256']:raise ValueError('Read-only investigation input epoch changed: '+record['path'])
        elif C.sha(subprocess.check_output(['git','show',record['gitObject']],cwd=ROOT))!=record['sha256']:raise ValueError('Committed physical protection input changed')
    if protectionInputs['claimPathSet']!=sorted(p.relative_to(ROOT).as_posix() for p in (ROOT/'evidence/lanes').rglob('claim.json')):raise ValueError('Ownership path set changed during read-only audit')
    write_json(LANE/'027e0898-flow.json',flow);write_json(LANE/'027e0898-controls.json',controls)
    result=dict(schemaVersion=1,status='physical-boundary-proposal-for-independent-review',sourceCredit=0,sourceOwnershipGranted=False,productionInputsChanged=False,sourceRevision=revision,acceptedCohort=159,program='',processor='arm7',module='arm7-main',entryMode='arm',entry=hex(ENTRY),proposal=proof,originalRom=dict(path=conf['rom'].relative_to(ROOT).as_posix(),sha256=conf['romSha256'],arm7Header=dict(fileOffset=offset,entryAddress=hex(entryAddress),loadAddress=hex(load),bytes=size),originalArm7Sha256=C.sha(original)),runtimeModule=module,ghidraOriginalEntry=entry,flow=pin((LANE/'027e0898-flow.json').relative_to(ROOT).as_posix()),controls=pin((LANE/'027e0898-controls.json').relative_to(ROOT).as_posix()),physicalProtection=dict(status='passed',intersections=hits,inputs=protectionInputs),outsideReferences=outside,primarySDK=sdk,inputPins=pins,limits=['Read-only structural proof; no source authoring/ownership/config/registry/boundary publication or source credit. Coordinator must independently admit a source scope.','Derived full4464B comprises4392 reachable ARMv4T instruction bytes and72 uniquely read original literal bytes. Ten bounded switch entries are executable ARM branch instructions. Neither next-entry arithmetic nor Ghidra body bytes alone defines the extent.','No native caller/helper/game/platform execution or source equivalence/complete original declaration is claimed. Pinned primary SDK correspondence is qualified, not proof of historical revision.','Existing accepted/native/data/linkage spans and94 current/historical exact function claims are checked mode-independently in full host ARM7 namespace. Collection envelopes remain separately explicit; opaque computed pointer producers are not disproved.'])
    result['generatorSources']=generatorSources;result['pythonVersion']=sys.version;result['entryBoundaryLookupsProvidedToPrimaryAnalysis']=0
    write_json(LANE/'027e0898-proposal.json',result);print(dict(path=(LANE/'027e0898-proposal.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'027e0898-proposal.json'),nativeSpanSha256=nativeHash,bytes=proof['bytes'],sourceCredit=0),flush=True)


if __name__=='__main__':execute()
