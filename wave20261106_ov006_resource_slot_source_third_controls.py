import shutil
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_resource_slot_source_third_paths import WORK
from wave20261106_ov006_resource_slot_source_third_bindings import negative_controls
from wave20261106_ov006_resource_slot_source_third_build import build
from wave20261106_ov006_resource_slot_source_third_compiler import compare
from wave20261106_ov006_resource_slot_source_third_models import check
from wave20261106_ov006_resource_slot_source_third_abi import check_source,proof


def execute(rows):
    result=negative_controls(rows);wrong=[];types=[];prototypes=[];abi_controls=[]
    for row in rows:
        source=ROOT/row['source'];text=source.read_text();header=(source.parent/'context.h').read_text()
        for label,old,new in[('wrong-cursor-initial-value','sizeof(native_data_ov006_02218df8.rows[0]))=32','sizeof(native_data_ov006_02218df8.rows[0]))=31'),('wrong-sentinel-tag','if(spec->tag==127)','if(spec->tag==126)'),('wrong-secondary-font','if(secondarySpec->font==1)','if(secondarySpec->font==0)')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
            if text.count(old)!=1:raise ValueError('Actual whole676B C mutation absent')
            target.write_text(text.replace(old,new),encoding='utf-8');(directory/'context.h').write_text(header,encoding='utf-8');mutant,body=build(target,directory/'build',negative=True);model=check([mutant],[body],negative=True)
            wrong.append(dict(case=label,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),object=mutant['object'],objectSha256=mutant['objectSha256'],realLink=mutant['realLink'],nativeWholeExtentMismatchRejected=True,boundedWrongCModel=model,wrongCCompleteReturnsNotClaimed=True))
        for label,old,new in[('cursor-row-stride','u32 rows[2][4];','u32 rows[2][5];'),('build-record-layout','s8 tag8;u8 gap9;','s32 tag8;u8 gap9;')]:
            directory=WORK/'controls'/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            if header.count(old)!=1:raise ValueError('Actual cursor/build-record layout control absent')
            (directory/'context.h').write_text(header.replace(old,new),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong consumed row/record layout compiled')
            types.append(dict(case=label,rejected=True,compilerDiagnostics=attempt[0]))
        directory=WORK/'controls/wrong-zero-arg-prototype';directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;target.write_text(text.replace('native_fn_ov006_021e6e2c(asset)','native_fn_ov006_021e6e2c()'),encoding='utf-8');(directory/'context.h').write_text(header.replace('native_fn_ov006_021e6e2c(u32)','native_fn_ov006_021e6e2c(void)'),encoding='utf-8');attempt,unused=compare(target,directory/'compile')
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Wrong-prototype byte-exact negative no longer demonstrates the missing semantic guard')
        try:check_source(target)
        except ValueError as error:abi_controls.append(dict(case='zero-arg-caller-import',compiledWholeExtentByteExact=True,sourceABIRejected=True,reason=str(error),object=attempt[0]['object'],objectSha256=attempt[0]['objectSha256'],productionRejectsBeforeCompileOrGenuineLink=True))
        else:raise ValueError('Wrong zero-arg source contract passed real native input-use qualifier')
        flags=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*flags,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls/require-prototypes')
        finally:match_runtime.FLAGS=flags
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Actual closed prototype preflight differs')
        prototypes.append(dict(exactWholeFingerprint=True,diagnosticFlags=attempt[0]['compilerFlags'],primaryFlagsUnchanged=True))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=types,explicitPrototypePreflight=prototypes,sourceABIControls=abi_controls,providerBodyCredit=0,wrongCCompleteReturningCalls=0)
    return result
