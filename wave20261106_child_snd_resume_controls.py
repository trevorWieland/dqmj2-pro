import shutil
import match_lowlevel
from project import ROOT,sha256
from wave20261106_child_snd_resume_paths import WORK
from wave20261106_child_snd_resume_bindings import negatives
from wave20261106_child_snd_resume_build import build
from wave20261106_child_snd_resume_compiler import compare
from wave20261106_child_snd_resume_models import check


def execute(rows):
    result=negatives(rows);wrong=[];layout=[];prototypes=[]
    for row in rows:
        source=ROOT/row['source'];original=source.read_text();header=(source.parent/'context.h').read_text()
        changes=[('wrong-null-player-return','if (player == ((void *)0) ) return 0','if (player == ((void *)0) ) return 1'),('wrong-bank-load-flags','(1 << 1) | (1 << 2)','(1 << 1)'),('wrong-unsigned-volume-offset','handle, sound->param.volume','handle, sound->param.channelPrio')]
        for label,old,new in changes:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
            if original.count(old)!=1:raise ValueError('Actual wrong-C mutation absent')
            target.write_text(original.replace(old,new),encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');entry,body=build(target,directory/'build',negative=True);model=check([entry],[body],negative=True)
            wrong.append(dict(case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,independentActualCallerModel=model))
        for label,old,new in[('sound-volume-width','    u16 bankNo;\n    u8 volume;','    u16 bankNo;\n    u16 volume;'),('archive-base-offset','    u32 baseOffset;','    u32 opaque;\n    u32 baseOffset;'),('unsigned-byte-semantics','typedef unsigned char u8;','typedef signed char u8;')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            if header.count(old)!=1:raise ValueError('Actual layout/type mutation absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if not attempt.get('compileFailed'):raise ValueError('Wrong consumed layout/signedness unexpectedly compiled')
            layout.append(dict(case=label,rejected=True,compilerDiagnostics=attempt))
        flags=match_lowlevel.FLAGS
        try:
            match_lowlevel.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls/required-prototypes')
        finally:match_lowlevel.FLAGS=flags
        if attempt.get('compileFailed')or not attempt['exactAfterDeclaredRelocation']:raise ValueError('Actual closed prototype preflight differs')
        prototypes.append(dict(address=row['address'],exactWholeFingerprint=True,diagnosticFlags=attempt['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototypes,providerBodyCredit=0)
    return result
