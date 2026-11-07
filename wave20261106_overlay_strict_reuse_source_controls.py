import shutil
import match_runtime
from project import ROOT,sha256
from wave20261106_overlay_strict_reuse_source_paths import WORK
from wave20261106_overlay_strict_reuse_source_bindings import negative_controls
from wave20261106_overlay_strict_reuse_source_build import build
from wave20261106_overlay_strict_reuse_source_compiler import compare
from wave20261106_overlay_strict_reuse_source_models import check


def execute(rows):
    result=negative_controls(rows);wrong=[];layout=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];original=source.read_text();header=(source.parent/'context.h').read_text()
        changes=[('wrong-modulo-shift','(u32)result << 5','(u32)result << 4'),('wrong-target-flag','target[6] |= 2','target[6] |= 4')]if row['module']=='ov003'else[('wrong-signed-rounding','+ 4U','+ 3U'),('wrong-final-s16-narrow','return (s16)','return (s32)')]
        for label,old,new in changes:
            directory=WORK/'controls'/row['module']/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
            if original.count(old)!=1:raise ValueError('Actual wrong-C mutation absent')
            target.write_text(original.replace(old,new),encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');entry,body=build(target,directory/'build',negative=True);model=check([entry],[body],negative=True)
            wrong.append(dict(case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,independentActualCallerModel=model))
        mutations=[('word-width','typedef unsigned int u32;','typedef unsigned short u32;'),('signed-offset','typedef int s32;','typedef unsigned int s32;')]if row['module']=='ov003'else[('s16-signedness','typedef signed short s16;','typedef unsigned short s16;'),('byte-signedness','typedef unsigned char u8;','typedef signed char u8;')]
        for label,old,new in mutations:
            directory=WORK/'controls'/row['module']/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            if header.count(old)!=1:raise ValueError('Actual type mutation absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong consumed width/signedness unexpectedly compiled')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/row['module']/'required-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual closed-prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototypes,providerBodyCredit=0)
    return result
