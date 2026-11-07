import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from goal_resume_resource_path_views import SOURCE,LANE,WORK,AUDIT,mirror,include
from goal_resume_resource_path_compile import reference,compile_source,normalized,object_contract,linker
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM


def inventory():
    if sha256(AUDIT)!='07f5481decd6793a9c2cd1358f7bb8c899a57fef1e2f8cfb053dfae7fa1ccf8f':raise ValueError('Authorized scope audit changed')
    return read_json(AUDIT)['minimumMigrationInventory']


def original_bytes(row):
    module=next(m for m in read_json(ROOT/'provenance/seed-manifest.json')['modules']if m['name']==row['module'])
    if sha256(ROOT/module['binary'])!=module['sha256']:raise ValueError('Original physical module changed')
    data=(ROOT/module['binary']).read_bytes();start=int(row['address'],0)-int(module['base'],0)
    body=data[start:start+row['bytes']]
    if hashlib.sha256(body).hexdigest()!=row['inputBytesSha256']:raise ValueError('Frozen original function span changed')
    return module,data,body


def witness():
    destination=LANE/'word-boundary-witness.json'
    if destination.exists():raise ValueError('Boundary witness already exists')
    results=[]
    for address,count,rule in [(0x02043018,20,'Incoming R0 is retained in R6 and reaches BL unchanged; explicit existing arg0 supplies the path word.'),(0x022096f4,16,'Incoming R0 is retained in R4 and reaches BL unchanged; explicit existing arg0 supplies the path word.'),(0x021d77f8,36,'LDR reads a four-byte filename address at table+4*index, moves retained R4 to R0, then BL size.'),(0x021e6bdc,36,'LDR reads a four-byte filename address at table+4*index, moves retained R4 to R0, then BL size.'),(0x020c55dc,140,'The canonical UINT loader result is stored as a file address, records starts at+8, word0/byte4 are consumed at offsets0/4 with44-byte stride and1399 iterations.')]:
        row=next(r for r in inventory()if int(r['address'],0)==address);module,data,body=original_bytes(row)
        instructions=[dict(address=hex(i.address),mnemonic=i.mnemonic,operands=i.op_str)for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(body[:count],address)]
        result=dict(identity={k:row[k]for k in('id','program','processor','module','mode','address','bytes')},source=row['sourceUnit'],sourceSha256=row['sourceSha256'],inputModule=module['binary'],inputModuleSha256=module['sha256'],inputBytesSha256=row['inputBytesSha256'],instructions=instructions,measuredBoundary=rule)
        if address in(0x021d77f8,0x021e6bdc):
            table=0x0220c8a8 if address==0x021d77f8 else 0x0220d15c;base=int(module['base'],0);entries=[]
            for index in range(4):
                value=struct.unpack_from('<I',data,table-base+4*index)[0];offset=value-base;end=data.find(b'\0',offset,offset+128)
                if offset<0 or end<offset:raise ValueError('Sampled filename table word lacks its actual bounded string')
                entries.append(dict(index=index,address=hex(value),bytesSha256=hashlib.sha256(data[offset:end+1]).hexdigest(),bytesIncludingTerminator=end-offset+1))
            result.update(tableAddress=hex(table),entryBytes=4,sampledEntries=entries,limits='Four actual entries are witnessed; this does not invent a table bound or an out-of-range index guard.')
        results.append(result)
    row=next(r for r in inventory()if int(r['address'],0)==0x020c55dc);ref=reference(0x020c55dc)
    folder=WORK/'boundary-geometry';folder.mkdir(parents=True,exist_ok=True);source=folder/'geometry.c';obj=folder/'geometry.o'
    header=ROOT/row['sourceDependencies'][0]['path']
    checks=['sizeof(void*)==4','sizeof(unsigned int)==4','sizeof(FieldFile)==52','sizeof(FieldRecord)==44','sizeof(FieldManager)==8','(unsigned int)&((FieldFile*)0)->records==8','(unsigned int)&((FieldRecord*)0)->byte4==4','(unsigned int)&((FieldManager*)0)->records==4']
    source.write_text('#include "'+header.as_posix()+'"\n'+'\n'.join('typedef char Boundary'+str(i)+'[('+condition+')?1:-1];'for i,condition in enumerate(checks))+'\n')
    command=[str(ROOT/ref['compilerPath']),*ref['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Actual retained field-record geometry failed',process.stdout,process.stderr))
    proof=dict(schemaVersion=1,status='measured-existing-word-boundaries',sourceCredit=0,sourceScopeFunctions=27,sourceScopeBytes=4812,results=results,geometry=dict(checks=checks,passed=True,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),header=header.relative_to(ROOT).as_posix(),headerSha256=sha256(header),compilerSha256=ref['compilerSha256'],compilerFlags=ref['compilerFlags']),canonicalCallerSignaturesUnchanged=True,limits=['No whole-program ISO-C repair is claimed. Existing nominal one-element file-record arrays and inherited unrelated interfaces are not rewritten.','Serialized32-bit filename addresses remain existing word carriers; conversions occur only at the reviewed typed API boundary.','The field-record loop witness describes native consumed layout, not a claim that the original single-element C array expresses its full dynamic extent.'])
    write_json(destination,proof)
    return proof


def edited(path,text):
    text=re.sub(r'^extern[^\n]*\bnative_fn_(?:0202a8e0|0203cc3c)\s*\([^;\n]*\);\s*\n','',text,flags=re.M)
    changes={
        'src/runtime/20261031_resource_load/native_main_0203cb8c.c':[('native_fn_0202a8e0(path)','native_fn_0202a8e0((const void *)path)')],
        'src/runtime/runtime08/native_main_02043018.c':[('native_fn_0202a8e0()','native_fn_0202a8e0((const void *)arg0)')],
        'src/runtime/ov000-drafts01/native_ov000_022096f4.c':[('native_fn_0202a8e0()','native_fn_0202a8e0((const void *)arg0)')],
        'src/overlays/ov006_root-global-widths-20261029a_12b96bbdc9a9.c':[('native_fn_0202a8e0(temp_r4)','native_fn_0202a8e0((const void *)(u32)temp_r4)')],
        'src/overlays/ov006_root-global-widths-20261029a_9f065757a20e.c':[('native_fn_0202a8e0(temp_r4)','native_fn_0202a8e0((const void *)(u32)temp_r4)')],
        'src/encounter/20261029-field-metadata/native_main_020c55dc.c':[('FieldFile *file = native_fn_0203cc3c','FieldFile *file = (FieldFile *)native_fn_0203cc3c')],
        'src/runtime/parallel_wave20261104/main-command-forward/next/context.h':[('extern int native_fn_0202a818(const char *,void *,u32,int);','extern u32 native_fn_0202a818(u32,u32,u32,u32);')],
        'src/runtime/parallel_wave20261104/main-command-forward/next/0205c668.c':[('native_fn_0202a818(name,data,size,0)','native_fn_0202a818((u32)name,(u32)data,size,0)')]
    }
    for before,after in changes.get(path,[]):
        if text.count(before)!=1:raise ValueError(('Reviewed typed boundary edit is ambiguous',path,before))
        text=text.replace(before,after)
    return text


def create_views():
    if not read_json(LANE/'word-boundary-witness.json')['geometry']['passed']:raise ValueError('Measured existing boundary gate is not closed')
    if not read_json(LANE/'faithful-size-qualified.json')['allocatedContractEqual']or not read_json(LANE/'0203cc3c-qualified.json')['allocatedContractEqual']:raise ValueError('Provider-first gate is not closed')
    paths={}
    for row in inventory():
        if int(row['address'],0)in(0x0202a8e0,0x0203cc3c):continue
        paths[row['sourceUnit']]=row['sourceSha256']
        for dependency in row.get('sourceDependencies')or[]:paths[dependency['path']]=dependency['sha256']
    outputs=[]
    for path,expected in sorted(paths.items()):
        old=ROOT/path;new=mirror(path)
        if sha256(old)!=expected or new.exists():raise ValueError(('Original changed or additive view already exists',path))
        text=edited(path,old.read_text())
        if old.suffix=='.c':text=include(new,SOURCE/'resource_path_api.h')+'\n'+text
        if len(text.splitlines())>500 or '/*'in text or '//'in text:raise ValueError(('View violates authored source policy',path))
        new.parent.mkdir(parents=True,exist_ok=True);new.write_text(text)
        outputs.append(dict(original=path,originalSha256=expected,view=new.relative_to(ROOT).as_posix(),viewSha256=sha256(new)))
    write_json(LANE/'caller-views.json',dict(status='additive-views-no-adoption',sourceCredit=0,sourceFunctions=25,files=outputs,boundaryWitnessSha256=sha256(LANE/'word-boundary-witness.json'),limits='Only reviewed prototypes, typed boundary conversions, and two explicit retained incoming arguments change; original statement/control-flow structure and public caller signatures are preserved.'))


def bindings(row):
    output={}
    for relocation in row['relocations']:
        name=relocation['symbol'];target=relocation['target'];qualified=re.search(r'_ov(\d{3})_',name);module='ov'+qualified[1]if qualified else'main'
        kind='data'if relocation['type']==2 else'function';mode='data'if kind=='data'else'arm'
        if kind=='function':
            candidates=[module]if qualified else['main',row['module']]
            found=[]
            for candidate in dict.fromkeys(candidates):
                unused,unused2,config=linker.measured_module(candidate)
                match=re.search(r'^\S+ kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x'+f'{int(target,0):08x}'+r'$',config,re.M)
                if match:found.append((candidate,match[1]))
            if len(found)!=1:raise ValueError(('Function binding lacks unique measured physical entry',name,target,found))
            module,mode=found[0]
        output[name]=dict(program='',processor='arm9',module=module,address=target,mode=mode,kind=kind)
    return output


def qualify_callers():
    if (LANE/'callers-qualified.json').exists():raise ValueError('Atomic caller qualification already finished')
    for pin in read_json(LANE/'caller-views.json')['files']:
        if sha256(ROOT/pin['view'])!=pin['viewSha256']or sha256(ROOT/pin['original'])!=pin['originalSha256']:raise ValueError('Frozen additive caller view or original changed')
    results=[]
    for selected in inventory():
        address=int(selected['address'],0)
        if address in(0x0202a8e0,0x0203cc3c):continue
        ref=reference(address);source=mirror(ref['source']);folder=WORK/'callers'/f'{address:08x}'
        qualified=LANE/'callers'/f'{address:08x}-qualified.json'
        if qualified.exists():
            prior=read_json(qualified)
            if sha256(source)!=prior['view']['sourceSha256']or sha256(ROOT/prior['view']['object'])!=prior['view']['objectSha256']or sha256(folder/'link/caller.bin')!=ref['targetSha256']or not prior['allocatedContractEqual']or not prior['rawRelocationsEqual']:raise ValueError('Already qualified immutable view/link changed')
            results.append(prior)
            continue
        row=compile_source(source,folder/'compile',ref)
        old=normalized(object_contract(ROOT/ref['object']));new=normalized(object_contract(ROOT/row['object']))
        raw=linker.relocation_rows(ROOT/ref['object'],ref['name']);fresh=linker.relocation_rows(ROOT/row['object'],row['name'])
        result=dict(identity={k:selected[k]for k in('id','program','processor','module','mode','address','bytes')},previousSource=ref['source'],previousSourceSha256=ref['sourceSha256'],previousObject=ref['object'],previousObjectSha256=ref['objectSha256'],view=row,allocatedContractEqual=old==new,rawRelocationsEqual=raw==fresh,sourceCredit=0)
        output=LANE/'callers'/f'{address:08x}-comparison.json';write_json(output,result)
        if old!=new or raw!=fresh or not row['exactAfterDeclaredRelocation']or row['compiledBytes']!=ref['bytes']:
            write_json(LANE/'atomic-stop.json',dict(status='blocked-allocated-or-native-contract-changed',sourceCredit=0,failed=result,completedFunctions=len(results),remainingFunctions=25-len(results)-1,prohibitedNextSteps=['No alternate cast/profile/source search','No new700 caller compiles','No adoption']))
            raise ValueError(('Atomic migration stopped on unchanged recipe',selected['module'],selected['address'],row['compiledBytes'],row['matchingBytes']))
        native_bindings=bindings(row);result['realLink']=linker.validate(row,native_bindings,folder/'link');result['nativeSymbolEntries']=native_bindings
        if raw!=linker.relocation_rows(folder/'link/caller.o',row['name']):raise ValueError('Fresh real native link changed raw relocations')
        write_json(LANE/'callers'/f'{address:08x}-qualified.json',result);results.append(result)
        print(dict(module=row['module'],address=row['address'],bytes=row['bytes'],allocatedEqual=True,rawRelocationsEqual=True,realNativeLink=True),flush=True)
    write_json(LANE/'callers-qualified.json',dict(status='all27-native-object-contracts-qualified-no-adoption',sourceCredit=0,providerFunctions=2,callerAndHeaderConsumerFunctions=len(results),functions=27,preservedBytes=4812,results=results,behaviorQualified=False,inputOnlyReplayPassed=False))


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--witness',action='store_true');group.add_argument('--views',action='store_true');group.add_argument('--qualify',action='store_true');args=parser.parse_args()
    if args.witness:witness()
    elif args.views:create_views()
    else:qualify_callers()


if __name__=='__main__':main()
