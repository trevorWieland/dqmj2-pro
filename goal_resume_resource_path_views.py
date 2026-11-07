import argparse
import os
import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256

SOURCE=ROOT/'src/runtime/goal_resume20261107/resource_path_api'
LANE=ROOT/'evidence/lanes/parallel-wave20261107/resource-path-api-migration'
WORK=ROOT/'work/goal-resume-20261107/resource-path-api'
AUDIT=ROOT/'evidence/lanes/parallel-wave20261107/resource-path-api-audit/audit.json'
SDK=ROOT/'src/runtime/20261102_nitrosdk18424/native_main_0200bfe4.c'


def mirror(path):
    return SOURCE/Path(path).relative_to('src')


def include(path,target):
    return '#include "'+os.path.relpath(target,path.parent).replace('\\','/')+'"'


def typedefs(text):
    result={}
    for match in re.finditer(r'\btypedef\b',text):
        depth=0
        for end in range(match.start(),len(text)):
            if text[end]=='{':depth+=1
            elif text[end]=='}':depth-=1
            elif text[end]==';'and not depth:
                declaration=text[match.start():end+1]
                name=re.search(r'\b(\w+)\s*;$',declaration)
                if name:result[name[1]]=declaration
                break
    return result


def sdk_header():
    text=SDK.read_text();decls=typedefs(text)
    names=['u8','u16','u32','BOOL','FSCommandType','FSResult','FSFileLink','FSDirPos','FSFileID','FSDirEntry','FSSeekDirInfo','FSReadDirInfo','FSFindPathInfo','FSGetPathInfo','FSOpenFileFastInfo','FSOpenFileDirectInfo','FSCloseFileInfo','FSReadFileInfo','FSWriteFileInfo','FSFile']
    queue=re.search(r'struct _OSThreadQueue\s*\{[^}]+\};',text)[0]
    pieces=[decls[n]for n in names[:4]]+['typedef struct _OSThread OSThread;','typedef struct _OSThreadQueue OSThreadQueue;',queue,'struct FSFile;','struct FSArchive;']+[decls[n]for n in names[4:]]
    result='#ifndef RESOURCE_PATH_SDK_FILE_H\n#define RESOURCE_PATH_SDK_FILE_H\n'+'\n'.join(pieces)+'\n#endif\n'
    if len(result.splitlines())>500 or '/*'in result or '//'in result:raise ValueError('Exact SDK type closure violates source policy')
    proof=dict(source=SDK.relative_to(ROOT).as_posix(),sourceSha256=sha256(SDK),completeTypedefs=names,opaqueTags=['_OSThread','FSArchive'],completeTag='FSFile',queueTag='_OSThreadQueue',sdkWord='unsigned long',apiWord='unsigned int',declarations=[dict(name=n,sha256=__import__('hashlib').sha256(decls[n].encode()).hexdigest())for n in names],rule='Every completed type and queue definition is copied exactly from the unchanged selected SDK open source. Opaque dependencies keep identical original tags and are never completed differently.')
    return result,proof


def initialize():
    if SOURCE.exists()or WORK.exists()or(LANE/'claim.json').exists():raise ValueError('Provider source/work roots must be new')
    audit=read_json(AUDIT)
    if sha256(AUDIT)!='07f5481decd6793a9c2cd1358f7bb8c899a57fef1e2f8cfb053dfae7fa1ccf8f':raise ValueError('Approved scope audit changed')
    rows=audit['minimumMigrationInventory']
    if len(rows)!=27 or sum(r['bytes']for r in rows)!=4812:raise ValueError('Approved minimum scope differs')
    for r in rows:
        if sha256(ROOT/r['sourceUnit'])!=r['sourceSha256']:raise ValueError('Selected source changed')
        for d in r.get('sourceDependencies')or[]:
            if sha256(ROOT/d['path'])!=d['sha256']:raise ValueError('Selected dependency changed')
    LANE.mkdir(parents=True,exist_ok=True);SOURCE.mkdir(parents=True)
    api='#ifndef RESOURCE_PATH_API_H\n#define RESOURCE_PATH_API_H\nextern unsigned int native_main_0202a8e0(const void *);\nextern unsigned int native_fn_0202a8e0(const void *);\nextern unsigned int native_main_0203cc3c(const void *,unsigned int);\nextern unsigned int native_fn_0203cc3c(const void *,unsigned int);\n#endif\n'
    (SOURCE/'resource_path_api.h').write_text(api)
    header,proof=sdk_header();(SOURCE/'sdk_file.h').write_text(header);write_json(LANE/'sdk-types.json',proof)
    claim=dict(schemaVersion=1,status='authorized-additive-pointer-API-views',sourceCredit=0,coordinatorOnlyAdoption=True,scopeAudit=dict(path=AUDIT.relative_to(ROOT).as_posix(),sha256=sha256(AUDIT)),selectedFunctions=27,preservedBytes=4812,accepted173Functions=23,prepared174Functions=4,canonicalTypes=['unsigned int(const void*)','unsigned int(const void*,unsigned int)'],sourceRoot=SOURCE.relative_to(ROOT).as_posix(),workRoot=WORK.relative_to(ROOT).as_posix(),originals=[{k:r.get(k)for k in('id','program','processor','module','mode','address','bytes','sourceUnit','sourceSha256','sourceDependencies','object','objectSha256','compilerSha256','compilerFlags','evidence','inputBytesSha256')}for r in rows],statusGlobalConsumersUnchanged=[r['id']for r in audit['fileStatusGlobalConsumers']],newSources=[dict(original=r['sourceUnit'],view=mirror(r['sourceUnit']).relative_to(ROOT).as_posix())for r in rows],authorization='Root authorizes exact27-row additive scope, providers first; unchanged allocated contracts are mandatory. No searches, shared selection or global edits. SDK init/close match actual selected unsignedint(void*) definitions; open uses exact BOOL(FSFile*,constchar*) source type.')
    write_json(LANE/'claim.json',claim)
    size=next(r for r in rows if int(r['address'],0)==0x0202a8e0)
    destination=mirror(size['sourceUnit']);destination.parent.mkdir(parents=True)
    context=destination.with_name('context.h')
    context.write_text(include(context,SOURCE/'sdk_file.h')+'\n'+include(context,SOURCE/'resource_path_api.h')+'\nextern unsigned int native_data_020edec8;\nextern unsigned int native_fn_0200bd04(void *);\nextern BOOL native_fn_0200bfe4(FSFile *,const char *);\nextern unsigned int native_fn_0200c02c(void *);\n')
    destination.write_text('#include "context.h"\nunsigned int native_main_0202a8e0(const void *path)\n{\n    FSFile file;\n    unsigned int length=0;\n    native_fn_0200bd04(&file);\n    if(native_fn_0200bfe4(&file,path)){\n        length=file.prop.file.bottom-file.prop.file.top;\n        native_data_020edec8=length!=0?0:3;\n        native_fn_0200c02c(&file);\n    }else native_data_020edec8=1;\n    return length;\n}\n')
    load=next(r for r in rows if int(r['address'],0)==0x0203cc3c)
    destination=mirror(load['sourceUnit']);destination.parent.mkdir(parents=True)
    text=(ROOT/load['sourceUnit']).read_text()
    text=text.replace('extern u32 native_fn_0203cb8c();','extern u32 native_fn_0203cb8c(u32,u32,u32);')
    text=text.replace('u32 native_main_0203cc3c(u32 arg0, u32 arg1)','unsigned int native_main_0203cc3c(const void *path, unsigned int heap)')
    text=text.replace('native_fn_0203cb8c(arg0, arg1, 1)','native_fn_0203cb8c((u32)path, heap, 1)')
    destination.write_text(include(destination,SOURCE/'resource_path_api.h')+'\n'+text)
    write_json(LANE/'provider-views.json',dict(files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(SOURCE.rglob('*'))if p.is_file()],sourceCredit=0,providersOnly=True))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--providers',action='store_true',required=True);parser.parse_args()
    initialize()
    print(dict(providersCreated=2,sourceCredit=0,sourceRoot=SOURCE.relative_to(ROOT).as_posix()),flush=True)


if __name__=='__main__':main()
