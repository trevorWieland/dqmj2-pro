import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
import main_resource_binding_fixture_20261102 as binding
import main_resource_setup_fixture_20261102 as setup

WORK=ROOT/'work/main-resource-binding1808-windows32-20261102'
REPORT=ROOT/'evidence/ports/main-resource-binding1808-windows32-20261102.json'
DRIVER=ROOT/'src/ports/20261102_resource_binding1808/driver.inc'
NATIVE=ROOT/'evidence/matches/main-resource-binding1792-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_resource_binding_v5/native_main_{a}.c'for a in['0202edfc','0202efe4','0202f250','0202bedc']]
SOURCES += [ROOT/f'src/runtime/20261102_resource_binding_v3/native_main_{a}.c'for a in['0202f170','0202f3dc']]
SETUP_SOURCE=ROOT/'src/runtime/20261102_resource_binding_v4/native_main_02031fa4.c'
HELPERS=['src/runtime/20261101_resource_dictionary/native_main_0202bbb4.c',
 'src/runtime/main-null01/native_main_0202beec.c','src/runtime/main-null01/native_main_0202ec30.c',
 'src/runtime/main-null01/native_main_0202ec44.c','src/runtime/main-null01/native_main_0202ed70.c',
 'src/runtime/runtime06/native_main_0202ec58.c','src/runtime/runtime09/native_main_0202ed84.c',
 'src/math/20261031_atan2/division.c','src/runtime/runtime08/native_main_02002458.c']
ALIASES=['0202edfc','0202efe4','0202f170','0202f250','0202f3dc','0202bedc','0202bbb4',
 '0202beec','0202ec30','0202ec44','0202ed70','0202ec58','0202ed84','0200235c','020023c4']


def compile_sources(label,mutation=None):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);setup_source=SETUP_SOURCE;paths=[*SOURCES,*[ROOT/p for p in HELPERS]]
    if mutation:
        address,old,new=mutation;original=next(p for p in[*paths,SETUP_SOURCE]if p.stem=='native_main_'+address)
        text=original.read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text
        wrong=folder/original.name;wrong.write_text(changed,encoding='utf-8')
        if original==SETUP_SOURCE:setup_source=wrong
        else:paths=[wrong if p==original else p for p in paths]
    glue=folder/'driver.c';glue.write_text('#include "'+setup_source.as_posix()+'"\n#include "'+DRIVER.as_posix()+'"\n',encoding='utf-8')
    definition=folder/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n',encoding='ascii')
    library=folder/'kernel32.lib';commands=[[str(tools/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(library)]]
    aliases=['/Dnative_fn_'+a+'=native_main_'+a for a in ALIASES]
    aliases.append('/Dnative_fn_02002458=resource_hardware_divide_setup')
    objects=[];inputs=[]
    for number,path in enumerate([*paths,glue]):
        obj=folder/f'unit{number:02}.obj';objects.append(obj)
        commands.append([str(tools/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/GS-','/Zl','/Brepro',
         '/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-strict-aliasing','/w',*aliases,'/c',str(path),'/Fo'+str(obj)])
        inputs.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))
    exe=folder/'resource_binding.exe';commands.append([str(tools/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86',
     '/nodefaultlib','/timestamp:0','/fixed','/base:0x00400000','/out:'+str(exe),*[str(p)for p in objects],str(library)])
    for command in commands:
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(command,run.stdout.decode(errors='replace'),run.stderr.decode(errors='replace'))
    raw=exe.read_bytes();offset=struct.unpack_from('<I',raw,0x3C)[0]
    assert struct.unpack_from('<H',raw,offset+4)[0]==0x14C and struct.unpack_from('<I',raw,offset+8)[0]==0
    for obj in objects:assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
    return exe,dict(inputs=inputs,objectHashes=[sha256(p)for p in objects],binarySha256=sha256(exe),commands=commands,driverSha256=sha256(DRIVER))


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256'];cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==4352
    chunks=[struct.pack('<I',len(cases))];expected=[]
    for row in cases:
        case=row['case'];index=case['index']
        if row['kind']=='setup':
            page,output,result,calls,services=setup.prepare(index);entry=setup.ENTRY;args=[binding.DATA];fail=services.fail;keys=services.keys
        else:
            page,entry,args=binding.inputs(index);output,result=binding.model(page,entry,args);calls=[];fail=0;keys=[0,0,0]
        assert hashlib.sha256(output).hexdigest()==case['dataSha256']
        chunks.append(struct.pack('<9I',entry,*args,*([0]*(4-len(args))),fail,*keys)+page)
        expected.append(dict(result=result,dataSha256=case['dataSha256'],calls=calls,divisions=len(case['divisionOperations'])))
    payload=b''.join(chunks);results=[]
    controls=[('texture-xor',('0202edfc','matData->texImageParam |=','matData->texImageParam ^=')),
     ('palette-xor',('0202f170','plttBase + vramOffset','plttBase ^ vramOffset')),
     ('missing-texture',('0202efe4','result = 0 ;','result = 1 ;')),
     ('allocation-format',('02031fa4','NNS_G3D_RESPLTT_USEPLTT4 = 0x8000','NNS_G3D_RESPLTT_USEPLTT4 = 0x4000')),
     ('success-return',('02031fa4','return 1 ;','return 0 ;'))]
    for label,mutation in[('preferred',None),*controls]:
        exe,built=compile_sources(label,mutation)
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        cursor=rejected=divisions=backend_calls=subset_rejected=subset_count=0;summary=[]
        for index,wanted in enumerate(expected):
            ordinal,result,count,div=struct.unpack_from('<4I',run.stdout,cursor);cursor+=16;assert ordinal==index and count<=16
            calls=[]
            for _ in range(count):
                address,n=struct.unpack_from('<2I',run.stdout,cursor);cursor+=8;assert n<=3
                values=list(struct.unpack_from('<'+str(n)+'I',run.stdout,cursor));cursor+=4*n;calls.append([address,values])
            data=run.stdout[cursor:cursor+65536];cursor+=65536;digest=hashlib.sha256(data).hexdigest()
            passed=digest==wanted['dataSha256']and calls==wanted['calls']and(wanted['result']is None or result==wanted['result'])
            if mutation is None:assert div==wanted['divisions'],(index,div,wanted['divisions'])
            rejected+=not passed;divisions+=div;backend_calls+=count;summary.append(dict(index=index,passed=passed,dataSha256=digest,calls=calls))
            if mutation is not None:
                kind='binding'if label in['texture-xor','palette-xor','missing-texture']else'setup'
                limit=1000 if kind=='binding'else 1536
                if cases[index]['kind']==kind and cases[index]['case']['index']<limit:subset_count+=1;subset_rejected+=not passed
        assert cursor==len(run.stdout)and(rejected==0)==(mutation is None),(label,rejected)
        if mutation is not None:
            native_control=next(r for r in report['negativeControls']if r['label']==label)
            assert subset_count==native_control['actualWrongReturns']and subset_rejected==native_control['independentModelRejections'],(label,subset_count,subset_rejected,native_control)
        results.append(dict(label=label,build=built,actualPublicCalls=len(cases),rejected=rejected,positiveControls=len(cases)-rejected,nativeControlSubsetCalls=subset_count,nativeControlSubsetRejects=subset_rejected,
         actualCompiledDivisionSetterCalls=divisions,providedBackendCalls=backend_calls,
         caseSha256=hashlib.sha256(json.dumps(summary,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=4352,actualWrongPublicCalls=21760,
     allSevenSourceBodiesIncludedUnmodified=True,selectedDictionaryAndDivisionCCompiled=True,hardwareModeledAfterActualCompiledSetter=True,
     allocationFreeUploadBoundariesExplicit=True,nativeReportSha256=sha256(NATIVE),fullGame=False,renderedScene=False,androidDeviceExecutions=0,
     reproductionCommand='python check_main_resource_binding1808_windows32_20261102.py'))
    print(dict(actualPreferred=4352,actualWrong=21760,wrongRejected=sum(r['rejected']for r in results[1:]),divisionSetterCalls=results[0]['actualCompiledDivisionSetterCalls']))


if __name__=='__main__':
    main()
