import shutil
import match_runtime
from project import ROOT,sha256
from wave20261106_ov000_roster_menu_source_first_paths import WORK
from wave20261106_ov000_roster_menu_source_first_bindings import negative_controls,inputs
from wave20261106_ov000_roster_menu_source_first_build import build
from wave20261106_ov000_roster_menu_source_first_compiler import compare
from wave20261106_ov000_roster_menu_source_first_fixtures import execute_one,cases


def execute(rows):
    result=negative_controls(rows);value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();wrong=[];layout=[];prototypes=[]
    changes=[('wrong-incoming-stack-initialization','    Point position;','    Point position;\n    position.x=0;position.y=0;',0,False),('wrong-sixth-actual-stack-argument','&position,2,2,15','&position,2,2,14',0,False),('wrong-signed-roster-resource','u8 y;s8 resource;','u8 y;u8 resource;',1,True)]
    for row in rows:
        source=ROOT/row['source']
        for label,old,new,case_index,change_header in changes:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;header=(source.parent/'context.h').read_text();text=source.read_text()
            if change_header:
                if header.count(old)!=1:raise ValueError('Actual signed resource mutation absent')
                header=header.replace(old,new)
            else:
                if text.count(old)!=1:raise ValueError('Actual caller mutation absent')
                text=text.replace(old,new)
            target.write_text(text,encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');entry,body=build(target,directory/'build',negative=True)
            try:execute_one(row,body,cases()[case_index],value,image,main)
            except ValueError as error:
                if not str(error).startswith("('Independent incoming-stack/caller model differs'"):raise
                reason=str(error)
            else:raise ValueError('Genuinely linked wrong incoming-stack/stack-argument/signed behavior passed')
            wrong.append(dict(address=row['address'],case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),headerSha256=sha256(directory/'context.h'),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,actualCallerReturnedThenIndependentModelRejected=True,reason=reason))
        for label,old,new in [('slot-extent','u32 id;u8 x;u8 y;','u32 id;u16 x;u8 y;'),('cursor-offset','u8 opaque0[16];LayoutState cursor;','u8 opaque0[12];LayoutState cursor;'),('signed-halfword','typedef signed short s16;','typedef unsigned short s16;')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target);header=(source.parent/'context.h').read_text()
            if header.count(old)!=1:raise ValueError('Actual layout mutation absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong actual menu/Point layout unexpectedly compiled')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/'required-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototypes,actualWrongCallerReturns=len(wrong),actualStandaloneOriginalEntryExecutions=0)
    return result
