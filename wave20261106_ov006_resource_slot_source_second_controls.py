import shutil
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_resource_slot_source_second_paths import WORK
from wave20261106_ov006_resource_slot_source_second_bindings import negative_controls
from wave20261106_ov006_resource_slot_source_second_build import build
from wave20261106_ov006_resource_slot_source_second_compiler import compare
from wave20261106_ov006_resource_slot_source_second_models import check


def execute(rows):
    result=negative_controls(rows);wrong=[];types=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];text=source.read_text();header=(source.parent/'context.h').read_text()
        for label,old,new in[('wrong-mode5-branch','if(spec->mode!=5)','if(spec->mode!=4)'),('wrong-reloaded-layer','resource->layer','spec->mode')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
            if text.count(old)!=1:raise ValueError('Actual whole-C control absent')
            target.write_text(text.replace(old,new),encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');mutant,body=build(target,directory/'build',negative=True);model=check([mutant],[body],negative=True)
            wrong.append(dict(case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=mutant['object'],objectSha256=mutant['objectSha256'],realLink=mutant['realLink'],nativeWholeExtentMismatchRejected=True,boundedWrongCModel=model,wrongCCompleteReturnsNotClaimed=True))
        for label,old,new in[('tuple-mode-width','s8 tag;u8 font;u8 mode;','s8 tag;u8 font;u32 mode;'),('resource-byte-position','u8 gap0[0x1c];','u8 gap0[0x18];')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            if header.count(old)!=1:raise ValueError('Actual tuple/resource layout control absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong consumed record layout compiled')
            types.append(dict(case=label,rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls/require-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual closed prototype preflight differs')
        prototypes.append(dict(exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=types,explicitPrototypePreflight=prototypes,providerBodyCredit=0,wrongCCompleteReturningCalls=0)
    return result
