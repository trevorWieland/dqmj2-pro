import shutil
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_resource_slot_source_first_paths import WORK
from wave20261106_ov006_resource_slot_source_first_bindings import negative_controls
from wave20261106_ov006_resource_slot_source_first_build import build
from wave20261106_ov006_resource_slot_source_first_compiler import compare
from wave20261106_ov006_resource_slot_source_first_models import check


def execute(rows):
    result=negative_controls(rows);wrong=[];types=[];prototypes=[]
    changes={0x21e6c44:('wrong-loop-bound','while(index<11)','while(index<10)'),0x21e7268:('wrong-byte-sentinel','0220d114=127','0220d114=126'),0x21e75ec:('wrong-fifth-stack-word','0,0,-1,-1','0,0,-1,-2'),0x21e7608:('wrong-entry-tag','prefix.field4=-1','prefix.field4=-2'),0x21e76f0:('wrong-signed-point','==127?0:8','==127?0:7'),0x21e79b0:('wrong-state-mask','020414c8(63)','020414c8(62)'),0x21e7ab0:('wrong-narrowed-stack-byte','(s8)fourth','(s8)(fourth+1U)'),0x21e7b00:('wrong-resource-width','resource->width','resource->height')}
    for row in rows:
        a=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();header=(source.parent/'context.h').read_text();label,old,new=changes[a];directory=WORK/'controls'/format(a,'08x')/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
        if text.count(old)!=1:raise ValueError('Actual whole-C mutation absent')
        target.write_text(text.replace(old,new),encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');mutant,body=build(target,directory/'build',negative=True);model=check([mutant],[body],negative=True)
        wrong.append(dict(address=row['address'],case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=mutant['object'],objectSha256=mutant['objectSha256'],realLink=mutant['realLink'],nativeWholeExtentMismatchRejected=True,actualBoundedWrongCModel=model,wrongCCompleteReturnsNotClaimed=True))
        if a==0x21e6c44:old,new='s8 tag;u8 font;u8 mode;','s8 tag;u32 font;u8 mode;'
        elif a in[0x21e7268,0x21e79b0]:old,new='u8 gap2c[8];','u8 gap2c[4];'
        elif a in[0x21e7608,0x21e75ec]:old,new='typedef signed int s32;','typedef signed short s32;'
        elif a in[0x21e76f0,0x21e7ab0]:old,new='typedef signed char s8;','typedef unsigned char s8;'
        else:old,new='typedef unsigned char u8;','typedef signed char u8;'
        directory=WORK/'controls'/format(a,'08x')/'wrong-consumed-type';directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
        if header.count(old)!=1:raise ValueError('Actual consumed-type mutation absent')
        (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
        if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong actual layout/width/signedness compiled')
        types.append(dict(address=row['address'],rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/format(a,'08x')/'require-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual strict prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=types,explicitPrototypePreflight=prototypes,providerBodyCredit=0,wrongCCompleteReturningCalls=0)
    return result
