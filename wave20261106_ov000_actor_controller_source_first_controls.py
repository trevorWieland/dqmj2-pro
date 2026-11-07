import shutil
import match_runtime
from project import ROOT,read_json,sha256
from wave20261106_ov000_actor_controller_source_first_paths import WORK,EVIDENCE
from wave20261106_ov000_actor_controller_source_first_bindings import negative_controls,inputs
from wave20261106_ov000_actor_controller_source_first_build import build
from wave20261106_ov000_actor_controller_source_first_compiler import compare
from wave20261106_ov000_actor_controller_source_first_fixtures import execute_one


MUTATIONS={0x0220c768:('timer*178','timer*176',2),0x0220d8c4:('actor->timer>15','actor->timer>14',4),0x0220fcb8:('unknown5[5]!=7','unknown5[5]!=6',4),0x02210008:('unknown5[2]==8','unknown5[2]==7',3)}


def execute(rows):
    result=negative_controls(rows);wrong=[];layout=[];prototypes=[];fixtures=read_json(EVIDENCE/'caller-fixtures.json')
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes()
    for row in rows:
        source=ROOT/row['source'];address=int(row['address'],0);old,new,index=MUTATIONS[address];directory=WORK/'controls'/source.stem/'wrong-C';directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source.parent/'context.h',directory/'context.h');text=source.read_text()
        if text.count(old)!=1:raise ValueError('Actual meaningful actor C mutation absent')
        target.write_text(text.replace(old,new),encoding='utf-8');entry,body=build(target,directory/'build',negative=True);case=next(v['input']for v in fixtures['records']if v['address']==row['address']and v['case']==index)
        try:execute_one(row,body,case,value,image,main)
        except ValueError as error:
            if not str(error).startswith("('Independent actor/record/state/DSP model differs'"):raise
            reason=str(error)
        else:raise ValueError('Genuinely linked wrong C passed independent actor model')
        wrong.append(dict(address=row['address'],mutation=[old,new],source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],completeNativeMismatchRejected=True,actualWrongCallerReturnedThenIndependentModelRejected=True,reason=reason))
        for label,old,new in [('actor-ID-offset','collision[102]','collision[100]'),('record-layout','unknown5[15]','unknown5[19]'),('signed-half','typedef signed short s16;','typedef unsigned short s16;')]:
            directory=WORK/'controls'/source.stem/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target);header=(source.parent/'context.h').read_text()
            if header.count(old)!=1:raise ValueError('Actor header mutation absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong actual actor/record layout unexpectedly compiled')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/source.stem/'required-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual explicit prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototypes,actualWrongCallerReturns=len(wrong),actualStandaloneOriginalEntryExecutions=0)
    return result
