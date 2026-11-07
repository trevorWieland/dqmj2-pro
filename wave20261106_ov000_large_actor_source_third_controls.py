import shutil
import match_runtime
from project import ROOT,read_json,sha256
from wave20261106_ov000_large_actor_source_third_paths import WORK,EVIDENCE
from wave20261106_ov000_large_actor_source_third_bindings import negative_controls,inputs
from wave20261106_ov000_large_actor_source_third_build import build
from wave20261106_ov000_large_actor_source_third_compiler import compare
from wave20261106_ov000_large_actor_source_third_fixtures import execute_one


def execute(rows):
    result=negative_controls(rows);fixtures=read_json(EVIDENCE/'caller-fixtures.json');value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();wrong=[];layout=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];case=next(v['input']for v in fixtures['records']if v['case']==9)
        for label,change_header in [('wrong-fade-threshold',False),('wrong-packed-nibble-order',True)]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;header=(source.parent/'context.h').read_text();text=source.read_text()
            if change_header:
                old='Flags8 {u8 low:4;u8 high:4;}';new='Flags8 {u8 high:4;u8 low:4;}'
                if header.count(old)!=1:raise ValueError('Actual packed flags order mutation absent')
                header=header.replace(old,new)
            else:
                if text.count('remaining<20')!=1:raise ValueError('Actual fade boundary mutation absent')
                text=text.replace('remaining<20','remaining<19')
            target.write_text(text,encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');entry,body=build(target,directory/'build',negative=True)
            try:execute_one(row,body,case,value,image,main)
            except ValueError as error:
                if not str(error).startswith("('Independent fade/teleport/union/nibble model differs'"):raise
                reason=str(error)
            else:raise ValueError('Genuinely linked wrong packed/source behavior passed independent model')
            wrong.append(dict(address=row['address'],case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),headerSha256=sha256(directory/'context.h'),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,actualCallerReturnedThenIndependentModelRejected=True,reason=reason))
        for label,old,new in [('scratch-index-width','Vec3 position;u8 index;','Vec3 position;u16 index;'),('secondary-vector-offset','opaque7c[148]','opaque7c[144]'),('signed-half','typedef signed short s16;','typedef unsigned short s16;')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target);header=(source.parent/'context.h').read_text()
            if header.count(old)!=1:raise ValueError('Actual typed union/layout mutation absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong actual union/vector/signedness unexpectedly compiled')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/'required-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototypes,actualWrongCallerReturns=len(wrong),actualStandaloneOriginalEntryExecutions=0)
    return result
