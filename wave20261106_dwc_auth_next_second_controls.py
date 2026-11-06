from wave20261106_dwc_auth_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
import copy
import hashlib
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_auth_next_second_compiler import COMPILER,compare
from wave20261106_dwc_auth_next_second_bindings import verify_original,negative_controls
from wave20261106_dwc_auth_next_context_link import inspect_object,validate as context_link,generated_definition,context_contract
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile


def geometry(row):
    assert_owned(LANE,SOURCE,WORK);folder=WORK/'geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u32)==4']
    if row['address']=='0x2097fac':checks+=['sizeof(wchar_t)==2','sizeof(size_t)==4'];wrong=text.replace('typedef unsigned short wchar_t;','typedef unsigned long wchar_t;',1)
    else:
        checks+=['sizeof(DWCAuthParam)==72','(u32)&((DWCAuthParam*)0)->alloc==64','(u32)&((DWCAuthParam*)0)->free==68','sizeof(DWCAuthResult)==452','sizeof(DWCAuth)==5108','(u32)&((DWCAuth*)0)->result==0x1008','(u32)&((DWCAuth*)0)->param==0x11cc','(u32)&((DWCAuth*)0)->http==0x1314','(u32)&((DWCAuthGlobals*)0)->auth==8'];wrong=text.replace('stack[4096]','stack[4092]',1)
    if row['address']=='0x209770c':checks+=['sizeof(DWCHttpParam)==28',*['(u32)&((DWCHttpParam*)0)->'+field+'=='+str(i*4) for i,field in enumerate(['url','action','len_recvbuf','alloc','free','ignoreca','timeout'])]]
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Actual consumed Auth/CAL layout failed',positive.stdout,positive.stderr))
    if wrong==text:raise ValueError('Meaningful wrong layout did not mutate')
    (folder/'context.h').write_text(wrong);negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if negative.returncode==0:raise ValueError('Wrong actual Auth/CAL layout admitted')
    return dict(address=row['address'],checks=checks,positiveExitCode=0,wrongLayoutRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout)


def prototype_presence(row):
    folder=WORK/'required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def allocated(path):
        with path.open('rb') as stream:return [(s.name,s['sh_flags'],s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&2]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or allocated(obj)!=allocated(ROOT/row['object']):raise ValueError(('Required actual prototypes failed or changed allocated caller/context',positive.stdout,positive.stderr))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name={'0x209770c':'DWC_Http_Create','0x2097ab0':'DWC_Http_GetResult','0x2097fac':'DWC_Http_Add_PostBase64Item'}[row['address']];changed=text.replace(name+'(','missing_callable_declaration(',1)
    if changed==text:raise ValueError('Actual provider declaration did not mutate')
    header.write_text(changed);negative_obj=folder/'missing.o'
    if negative_obj.exists():negative_obj.unlink()
    negative=subprocess.run([str(COMPILER),*flags,'-c',str(wrong),'-o',str(negative_obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or negative_obj.exists() or 'no prototype' not in negative.stdout:raise ValueError(('Actual missing provider declaration admitted',negative.stdout,negative.stderr))
    return dict(address=row['address'],positiveExitCode=0,actualExecutableAndInitializedContextSectionsUnchanged=True,diagnosticFlags=flags,missingActualProvider=name,negativeExitCode=negative.returncode,negativeStdout=negative.stdout,primaryFlagsUnchanged=True,sourceCredit=0)


def context_controls(row):
    item,native=context_contract();source=ROOT/row['source'];definition=generated_definition()
    if (source.parent/'context-data.h').read_text()!=definition:raise ValueError('Actual semantic header generation changed')
    positive=inspect_object(ROOT/row['object'],row);rejected=[]
    for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('address','0x209770e'),('bytes',190)]:
        bad=copy.deepcopy(row);bad[key]=wrong
        try:inspect_object(ROOT/row['object'],bad)
        except ValueError as error:rejected.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong context caller namespace/mode/extent admitted')
    wrong_results=[]
    for label,before,after in [('timeout','20000','20001'),('URL','native_data_020deb48','native_data_020deb90'),('URL-addend','native_data_020deb48','native_data_020deb48+8')]:
        folder=WORK/'wrong-context'/label;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'wrong.c';shutil.copyfile(source,wrong);header=folder/'context-data.h';text=header.read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Wrong semantic compiler context did not mutate')
        header.write_text(changed);rows,_=compare(wrong,folder/'c');bad=rows[0];bad.update(program='');bindings=qualified_bindings(bad)
        if label=='timeout':
            proof=context_link(bad,bindings,folder/'l',allow_wrong_context=True)
            if not proof['exactCallerBytes'] or proof['contextExactOriginalBytes']:raise ValueError('Wrong initializer genuine link control failed')
            try:inspect_object(ROOT/bad['object'],bad)
            except ValueError as error:reason=str(error)
            else:raise ValueError('Wrong context initializer admitted on positive path')
            wrong_results.append(dict(case=label,genuinelyLinked=True,callerStillExact=True,contextRejected=True,reason=reason,realLink=proof))
        else:
            try:inspect_object(ROOT/bad['object'],bad,allow_wrong_context=True)
            except ValueError as error:wrong_results.append(dict(case=label,actualCompilerObjectRejected=True,reason=str(error)))
            else:raise ValueError('Wrong URL target or addend admitted')
    return dict(status='passed',positiveWholeOriginalCompilerObject=positive,actualInitializerGeneratedFromSemanticSource=True,generator='wave20261106_dwc_auth_next_context_link.py:generated_definition',semanticSource=item['semanticSource'],semanticSourceSha256=item['semanticSourceSha256'],declaredStorageCredit=0,nativeContextSha256=hashlib.sha256(native).hexdigest(),namespaceNegatives=rejected,wrongContext=wrong_results,allProductionCallsUseStrictDefaults=True)


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],requiredPrototypeDiagnostics=[prototype_presence(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),jointContextControls=context_controls(next(r for r in rows if r['address']=='0x209770c')),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
