import shutil
import match_runtime
from project import ROOT,read_json,sha256
from wave20261106_ov000_slot_controller_first_paths import WORK,EVIDENCE,SOURCE
from wave20261106_ov000_slot_controller_first_bindings import negative_controls,inputs
from wave20261106_ov000_slot_controller_first_build import build
from wave20261106_ov000_slot_controller_first_compiler import compare
from wave20261106_ov000_slot_controller_first_fixtures import execute_one


def execute(rows):
    result=negative_controls(rows);wrong=[];layout=[];prototype=[]
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes()
    for row in rows:
        source=ROOT/row['source'];directory=WORK/'controls'/source.stem/'wrong-flag';directory.mkdir(parents=True,exist_ok=True)
        target=directory/source.name;header=directory/'context.h';shutil.copyfile(source.parent/'context.h',header)
        text=source.read_text()
        if text.count('flags|=2;')!=1:raise ValueError('Actual wrong-C status mutation source absent')
        target.write_text(text.replace('flags|=2;','flags|=4;'),encoding='utf-8')
        entry,body=build(target,directory/'build',negative=True)
        case=dict(args=[1,128,255,128,255,1,255,-128,1],occupied=False,allocationFails=False,first=128,flags=0,stateWords=[0,1,2,3,4,5,6])
        try:execute_one(row,body,case,main,image)
        except ValueError as error:
            if not str(error).startswith("('Independent consumed-field/provider ABI model differs'"):raise
            reason=str(error)
        else:raise ValueError('Genuinely linked wrong flag passed independent caller model')
        wrong.append(dict(address=row['address'],source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,independentSemanticModelRejected=True,reason=reason))
        for label,old,new in [('resource-offset','opaque[24]','opaque[20]'),('link-offset','opaque[3]','opaque[7]'),('signed-byte','typedef signed char s8;','typedef unsigned char s8;')]:
            directory=WORK/'controls'/source.stem/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            header_text=(source.parent/'context.h').read_text()
            if header_text.count(old)!=1:raise ValueError('Actual header negative target differs')
            (directory/'context.h').write_text(header_text.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong consumed field layout/signedness unexpectedly compiled')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        previous=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*previous,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/source.stem/'required-prototypes')
        finally:match_runtime.FLAGS=previous
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Diagnostic explicit-prototype compile differs')
        prototype.append(dict(address=row['address'],compiled=True,exactWholeFingerprint=True,ordinaryPrimaryFlagsUnchanged=True,diagnosticFlags=attempt[0]['compilerFlags']))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototype,actualWrongCallerModelRejections=len(wrong),actualWrongCallerReturns=0,actualStandaloneOriginalEntryExecutions=0)
    return result
