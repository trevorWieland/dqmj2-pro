import shutil
import match_runtime
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from project import ROOT,sha256
from wave20261106_ov000_controller_composite_second_next_first_paths import WORK
from wave20261106_ov000_controller_composite_second_next_first_bindings import negative_controls,inputs
from wave20261106_ov000_controller_composite_second_next_first_build import build
from wave20261106_ov000_controller_composite_second_next_first_compiler import compare
from wave20261106_ov000_controller_composite_second_next_first_fixtures import execute_one,make_case

MUTATIONS={0x21ec044:('point.x+=8;\n    native_fn_0204a154(7','point.x+=9;\n    native_fn_0204a154(7',0)}


def payload(path,name):
    with path.open('rb')as stream:
        elf=ELFFile(stream);entry=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name);start=entry['st_value']&~1
        return elf.get_section(entry['st_shndx']).data()[start:start+entry['st_size']]


def execute(rows):
    result=negative_controls(rows);wrong=[];layout=[];prototype=[]
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes()
    for row in rows:
        address=int(row['address'],0);source=ROOT/row['source'];old,new,index=MUTATIONS[address];directory=WORK/'controls'/source.stem/'wrong-C';directory.mkdir(parents=True,exist_ok=True);target=directory/source.name
        shutil.copyfile(source.parent/'context.h',directory/'context.h');text=source.read_text()
        if text.count(old)!=1:raise ValueError('Actual independent wrong-C mutation target differs')
        target.write_text(text.replace(old,new));entry,body=build(target,directory/'build',negative=True)
        try:execute_one(row,body,make_case(address,index),main,image)
        except ValueError as error:
            if not str(error).startswith("('Independent two-point ABI/mutation/order model differs'"):raise
            reason=str(error)
        else:raise ValueError('Wrong complete linked C passed independent branch model')
        wrong.append(dict(address=row['address'],source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),sourceMutation=[old,new],reachedCase=index,object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,independentModelRejectedAfterActualCallerReturn=True,reason=reason))
        original=(source.parent/'context.h').read_text();resource='opaque0[24]'if'opaque0[24]'in original else'opaque[24]'
        for label,before,after in [('point-layout','struct{s16 x,y;}Point16','struct{s16 wrong,x,y;}Point16'),('signed-half','typedef signed short s16;','typedef unsigned short s16;'),('entry-link-offset','EntryView{LinkView*link','EntryView{u32 wrong;LinkView*link')]:
            directory=WORK/'controls'/source.stem/label;directory.mkdir(parents=True,exist_ok=True);target=directory/source.name;shutil.copyfile(source,target)
            if original.count(before)!=1:raise ValueError(('Actual header negative absent',source,label))
            (directory/'context.h').write_text(original.replace(before,after));attempt,unused=compare(target,directory/'compile')
            if len(attempt)!=1 or not attempt[0].get('compileFailed'):raise ValueError('Wrong consumed layout/signedness accepted')
            layout.append(dict(address=row['address'],case=label,rejected=True,compilerDiagnostics=attempt[0]))
        previous=match_runtime.FLAGS
        try:
            match_runtime.FLAGS=[*previous,'-requireprotos','-w','error'];attempt,unused=compare(source,WORK/'controls'/source.stem/'required-prototypes')
        finally:match_runtime.FLAGS=previous
        if len(attempt)!=1 or attempt[0].get('compileFailed')or not attempt[0]['exactAfterDeclaredRelocation']:raise ValueError('Strict explicit-prototype diagnostic differs')
        if payload(ROOT/attempt[0]['object'],row['name'])!=payload(ROOT/row['object'],row['name'])or relocation_rows(ROOT/attempt[0]['object'],row['name'])!=relocation_rows(ROOT/row['object'],row['name']):raise ValueError('Strict diagnostic changed original complete compiler bytes/relocation payloads')
        prototype.append(dict(address=row['address'],compiled=True,completeObjectFunctionAndRelocationFingerprintUnchanged=True,primaryFlagsUnchanged=True,diagnosticFlags=attempt[0]['compilerFlags']))
    result.update(wholeCNegativeControlsRejected=len(wrong),wrongC=wrong,layoutAndSignednessNegatives=layout,explicitPrototypePreflight=prototype,actualWrongCallerModelRejections=len(wrong),actualWrongCallerReturns=len(wrong),actualStandaloneOriginalEntryExecutions=0)
    return result
