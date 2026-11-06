import copy
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path, PurePosixPath
from project import ROOT,configuration,native_dependencies,read_json,sha256
import match_runtime
import link_runtime_unit as linker
from elftools.elf.elffile import ELFFile
from qualify_arm9_reference_packets_v2_20261105 import qualify_report

SOURCE_COMMIT='e6a3a03ddf84996637858cc61f700f5d7b96d276'
ROM_SHA='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
REFERENCE='extract/arm9_overlays/ov000.bin'
REFERENCE_SHA='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6'
MANIFEST='provenance/cohort157-parallel-wave20261105-b-source-files.json'
SPEC='cohort157-parallel-wave20261105-b-specification.json'
REPORT='evidence/matches/cohort157-parallel-wave20261105-b-main-control-next-more-0.json'
EXPECTED={'0x207a168':72,'0x207a2d0':84}
ENTRY=(0,0x021d7240,364160,96160,35840260,35840264,0,16992928)
FLAGS=['-O4,p','-enum','int','-char','signed','-str','noreuse','-proc','arm946e','-gccext,on','-fp','soft','-inline','on,noauto','-Cpp_exceptions','off','-RTTI','off','-interworking','-w','off','-sym','on','-gccinc','-nolink','-msgstyle','gcc','-ipa','file','-lang','c99']


def require(condition,message):
    if not condition:raise ValueError(message)


def committed(name,revision=SOURCE_COMMIT):
    result=subprocess.run(['git','show',revision+':'+name],cwd=ROOT,capture_output=True,check=True)
    require((ROOT/name).read_bytes()==result.stdout,'Committed input differs: '+name)
    return json.loads(result.stdout)


def validate_entry(entry):
    require(tuple(entry)==ENTRY,'Exact host ARM9 overlay0 identity/layout/flags differs')
    ident,base,initialized,bss,first,last,file_id,flags=entry
    require(base%4==initialized%4==bss%4==first%4==last%4==0,'Overlay boundaries are unaligned')
    require(base<=first<last<=base+initialized,'Overlay constructors escape initialized image')
    require(flags>>24==1 and flags&0xffffff==215712,'Only measured compressed unsigned overlay is qualified')


def derive(rom,reference,seed):
    require(hashlib.sha256(rom).hexdigest()==ROM_SHA,'Authoritative original ROM changed')
    table,size=struct.unpack_from('<II',rom,0x50)
    fat,fat_size=struct.unpack_from('<II',rom,0x48)
    require((table,size,fat,fat_size)==(0x98600,256,0xc4e00,14040),'Measured overlay/FAT header boundaries differ')
    require(table+size<=len(rom) and fat+fat_size<=len(rom),'Original table bounds invalid')
    records=[struct.unpack_from('<8I',rom,at) for at in range(table,table+size,32)]
    selected=[r for r in records if r[0]==0]
    require(len(selected)==1,'Duplicate/missing overlay0 table entry')
    entry=selected[0]
    validate_entry(entry)
    first,last=struct.unpack_from('<II',rom,fat+entry[6]*8)
    require((first,last)==(823296,1039008) and first<last<=len(rom),'Measured overlay FAT file differs')
    native_dependencies(configuration())
    from ndspy import codeCompression
    stored=rom[first:last]
    data=codeCompression.decompress(stored)
    require(len(data)==entry[2] and hashlib.sha256(data).hexdigest()==REFERENCE_SHA,'Original overlay decompression identity differs')
    require(reference==data,'Extracted overlay differs from original ROM derivation')
    modules=[m for m in seed['modules'] if m['name']=='ov000']
    require(len(modules)==1,'Measured module inventory is ambiguous')
    module=modules[0]
    require((module['binary'],int(module['base'],0),module['bytes'],module['sha256'])==(REFERENCE,ENTRY[1],ENTRY[2],REFERENCE_SHA),'Measured overlay inventory differs')
    return dict(path=REFERENCE,sha256=REFERENCE_SHA,bytes=len(data),romSha256=ROM_SHA,overlayId=0,processor='arm9',program='',module='ov000',loadAddress=hex(entry[1]),bssBytes=entry[3],constructorRange=[hex(entry[4]),hex(entry[5])],originalOverlayTableOffset=hex(table),originalOverlayTableBytes=size,originalTableEntry=list(entry),originalFatOffset=hex(fat),originalFileId=entry[6],originalFatRange=[first,last],storedBytes=len(stored),storedSha256=hashlib.sha256(stored).hexdigest(),compressed=True,signed=False,committedAsAuthoredSource=False,reconstructedSourceBytes=0,reconstructedAssemblyBytes=0,sourceCredit=0)


def repository_path(name,suffix):
    require(isinstance(name,str) and name==PurePosixPath(name).as_posix() and '..' not in PurePosixPath(name).parts and not any(x in name for x in ['\\',':','\n','\r','\0']),'Noncanonical compiler input path')
    path=(ROOT/name).resolve()
    require(name.startswith('src/') and path.is_relative_to((ROOT/'src').resolve()) and path.suffix==suffix,'Production compiler input must be closed repository SRC C/header')
    return path


def text_closure(documents,source):
    require(source in documents,'Missing production C text')
    included=set()
    for name,text in documents.items():
        require(not any(token in text for token in ['\\','??','%:','\0']),'Ambiguous/continued/binary preprocessing input')
        require(not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin',text),'Executable assembly inclusion is not qualified')
        for line in text.splitlines():
            if '#' not in line:continue
            found=re.fullmatch(r'\s*#\s*include\s*"([^"<>]+)"\s*',line)
            require(found is not None,'Only explicit closed quoted includes are qualified')
            target=(PurePosixPath(name).parent/found.group(1)).as_posix()
            require(target in documents and target!=source,'Missing or recursive/unclosed include')
            included.add(target)
    require(included==set(documents)-{source},'Declared production include closure differs')


def row_inputs(row):
    require((row.get('program') or '',row.get('processor'),row.get('module'),row.get('mode'))==('','arm9','main','arm'),'Only proven host ARM9 main ARM callers are qualified; Thumb requires independent mode evidence')
    require(row.get('address') in EXPECTED and row.get('bytes')==EXPECTED[row['address']],'Unselected caller extent')
    require(row.get('compilerFlags')==FLAGS,'Actual pinned production compiler flags differ')
    require(row.get('exactAfterDeclaredRelocation') and row.get('realLink',{}).get('exactCallerBytes'),'Full original native caller/link proof missing')
    require(row['realLink']['linkedCallerSha256']==row['targetSha256']==row['outputSha256'],'Complete linked native hash differs')
    paths={row['source']:row['sourceSha256']}
    require(isinstance(row.get('sourceDependencies'),list),'Explicit header pins missing')
    for item in row['sourceDependencies']:
        require(item['path'] not in paths,'Repeated source/header input')
        repository_path(item['path'],'.h')
        paths[item['path']]=item['sha256']
    repository_path(row['source'],'.c')
    documents={}
    for name,digest in paths.items():
        require(sha256(ROOT/name)==digest,'Production source/header changed')
        require(subprocess.check_output(['git','show',SOURCE_COMMIT+':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),'Production source/header is not the committed source')
        documents[name]=(ROOT/name).read_text(encoding='utf-8')
    text_closure(documents,row['source'])
    return dict(originalCodeCompilerInput=False,source=row['source'],sha256=row['sourceSha256'],includes=row['sourceDependencies'],allInputsClosedSrcCAndHeaders=True)


def arm_mapping(path,name):
    with path.open('rb') as stream:
        elf=ELFFile(stream)
        symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
        entries=[s for s in symbols if s.name==name]
        require(len(entries)==1,'Ambiguous function in actual compiler object')
        symbol=entries[0]
        require(symbol['st_info']['type']=='STT_FUNC' and symbol['st_value']%2==0,'Actual compiler function is not ARM')
        mappings=[s for s in symbols if s['st_shndx']==symbol['st_shndx'] and s['st_value']==symbol['st_value'] and s.name in ['$a','$t']]
        require(len(mappings)==1 and mappings[0].name=='$a','Actual original/fresh ARM mapping absent or Thumb')
    return dict(mode='arm',entryValue=symbol['st_value'],functionBytes=symbol['st_size'],mapping='$a')


def validate_batch(batch,report,declared):
    require(batch['report']==REPORT,'Unqualified overlay reference consumer')
    require(batch['sourceHashes'].get(REFERENCE)==REFERENCE_SHA==declared.get(REFERENCE),'Exact registered/declared overlay pin differs')
    require(report['romSha256']==ROM_SHA and report['allPassed'],'Original consumer report identity/acceptance differs')
    require({r['address']:r['bytes'] for r in report['matches']}==EXPECTED,'Complete consumer namespace/extent set differs')
    for row in report['matches']:row_inputs(row)



def project_batches(actual_batches,report,declared):
    require(sum(b['report']==REPORT for b in actual_batches)==1,'Duplicate or missing exact overlay consumer')
    projected=copy.deepcopy(actual_batches)
    consumers=[]
    for batch in projected:
        references=[p for p in batch['sourceHashes'] if p.startswith('extract/arm9_overlays/')]
        if not references:continue
        require(references==[REFERENCE],'Unqualified overlay path; no blanket extraction exclusion')
        validate_batch(batch,report,declared)
        consumers.append(batch['report'])
        del batch['sourceHashes'][REFERENCE]
    require(consumers==[REPORT],'Actual exact overlay consumer set differs')
    return projected,consumers

def qualify(actual_batches,directory):
    own_hash=sha256(__file__)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',SOURCE_COMMIT,revision],cwd=ROOT,check=True)
    manifest=committed(MANIFEST)
    spec=committed(SPEC)
    seed=committed('provenance/seed-manifest.json')
    registry=committed('recovery.json',revision)
    require(actual_batches==registry['batches'],'Projection input is not exact committed native registry')
    snapshot={name:sha256(ROOT/name) for name in ['recovery.json','source-preferences.json','manifest.json',REPORT,MANIFEST,SPEC]}
    declared={p['path']:p['sha256'] for p in manifest['privateComparisonInputs']}
    baseline=json.loads(subprocess.check_output(['git','show',SOURCE_COMMIT+':'+REPORT],cwd=ROOT))
    report=committed(REPORT,revision)
    keys=['name','program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']
    require([{k:r.get(k) for k in keys} for r in report['matches']]==[{k:r.get(k) for k in keys} for r in baseline['matches']], 'Immutable accepted157 source/compiler/native contract differs')
    require(sha256(ROOT/report['generator'])==report['generatorSha256'],'Frozen original producer changed')
    packet=[p for p in spec['packets'] if p['report']==REPORT]
    require(len(packet)==1 and packet[0]['producer'][0]=='replay_parallel_packet.py','Committed selected packet absent')
    descriptor_name=packet[0]['producer'][1]
    descriptor=committed(descriptor_name)
    require(descriptor['canonicalReport']==REPORT and descriptor['producer'][0]==report['generator'],'Committed canonical producer closure differs')
    require({r['address']:r['bytes'] for r in descriptor['identities']}==EXPECTED,'Descriptor full identity set differs')
    require(all((r['program'],r['processor'],r['module'],r['mode'])==('','arm9','main','arm') for r in descriptor['identities']),'Descriptor namespace/mode differs')
    original_inputs=committed(report['inputManifest'])
    require(sha256(ROOT/report['inputManifest'])==report['inputManifestSha256'],'Actual producer input manifest changed')
    require({p['path']:p['sha256'] for p in original_inputs['files']}.get(REFERENCE)==REFERENCE_SHA,'Actual producer overlay role absent')
    for item in original_inputs['files']:
        require(sha256(ROOT/item['path'])==item['sha256'],'Original pinned actual input changed: '+item['path'])
    for row in report['matches']:
        for name in [row['source'],row['object'],row.get('compiler') or row['compilerPath'],*[h['path'] for h in row['sourceDependencies']]]:snapshot[name]=sha256(ROOT/name)
    derivation=derive(configuration()['rom'].read_bytes(),(ROOT/REFERENCE).read_bytes(),seed)
    projected,consumers=project_batches(actual_batches,report,declared)
    proof=qualify_report(REPORT,EXPECTED,directory/'compiler')
    links=[]
    for row,item in zip(report['matches'],proof['proofs']):
        require(row['address']==item['address'],'Fresh proof order differs')
        fresh=item['explicitC99Qualification']
        original_mapping=arm_mapping(ROOT/row['object'],row['name'])
        fresh_mapping=arm_mapping(ROOT/fresh['explicitC99Object'],row['name'])
        require(original_mapping==fresh_mapping,'Actual original/fresh ARM function boundaries differ')
        linked=copy.deepcopy(row)
        linked['object']=fresh['explicitC99Object']
        linked['objectSha256']=fresh['explicitC99ObjectSha256']
        result=linker.validate(linked,row['nativeSymbolEntries'],directory/'link'/row['address'])
        require(result['exactCallerBytes'] and result['linkedCallerSha256']==row['targetSha256'],'Fresh explicit C99 genuine full native link failed')
        require(all(p['initializedCodeBytes']==p['nativeCalleeBytesUsed']==p['calleeSourceCredit']==0 for p in result['bindingOnlyProbes']),'Callee executable scaffolding supplied to fresh link')
        links.append(dict(address=row['address'],sourceOnlyCompilerInput=row_inputs(row),originalMapping=original_mapping,freshMapping=fresh_mapping,explicitC99=fresh,freshGenuineLink=result))
    require(snapshot=={name:sha256(ROOT/name) for name in snapshot},'Registry/source/output scope changed during qualification')
    for item in original_inputs['files']:require(sha256(ROOT/item['path'])==item['sha256'],'Frozen actual input changed during qualification: '+item['path'])
    require(sha256(__file__)==own_hash,'Qualifier code changed during proof')
    derivation.update(referencedBy=consumers,role='Exact original ARM9 overlay0 ROM/FAT/decompression reference; never production compiler input')
    return projected,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=own_hash,acceptedSourceCommit=SOURCE_COMMIT,commitAtAudit=revision,overlay=derivation,consumers=consumers,consumerSourceFunctions=2,consumerSourceBytes=156,freshCompilerAndLinkProofs=links,privateInputDeclaration=dict(path=MANIFEST,sha256=sha256(ROOT/MANIFEST)),actualPinnedInputFilesVerified=len(original_inputs['files']),originalNativeHelperInvocationsReported=report['nativeCalleeBodiesExecuted'],referenceFixtureExecutionsAreNotSourceCredit=True,scopePins=snapshot,productionSourcesObjectsFlagsRegistryAndReportsUnchanged=True,limits=['Only this exact path/hash and committed two-row main ARM consumer is qualified. Other overlays/consumers/CPUs/programs/Thumb callers require independent qualification.','The original overlay remains local/private and excluded from Git; its derivation awards0 source/assembly/callee/storage bytes.','Fresh explicit-C99 C/header compiler inputs, complete function/relocation identity and genuine native links with zero-code binding anchors are independently required. No original executable is a compiler/linker implementation input.','This input-packaging qualification does not establish a full clean source-only build or native Windows/Android execution.'])
