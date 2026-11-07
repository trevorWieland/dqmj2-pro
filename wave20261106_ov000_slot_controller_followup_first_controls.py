import shutil
import match_runtime
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from project import ROOT,sha256
from wave20261106_ov000_slot_controller_followup_first_paths import WORK
from wave20261106_ov000_slot_controller_followup_first_bindings import negative_controls,inputs
from wave20261106_ov000_slot_controller_followup_first_build import build
from wave20261106_ov000_slot_controller_followup_first_compiler import compare
from wave20261106_ov000_slot_controller_followup_first_fixtures import execute_one,make_case

MUTATIONS={0x21efec4:('value+=2;','value+=3;',0),0x21f29ac:('field29*8;','field29*16;',3),0x2206868:('flags|=2;','flags|=4;',0),0x2207acc:('field29*8;','field29*16;',2),0x2208854:('field29*8;','field29*16;',2),0x22162e4:('127,1,1,30','126,1,1,30',0),0x221d05c:('flags&=~2;','flags&=~4;',3)}


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
            if not str(error).startswith("('Independent narrow ABI/field/order model differs'"):raise
            reason=str(error)
        else:raise ValueError('Wrong complete linked C passed independent branch model')
        wrong.append(dict(address=row['address'],source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),sourceMutation=[old,new],reachedCase=index,object=entry['object'],objectSha256=entry['objectSha256'],realLink=entry['realLink'],nativeWholeExtentMismatchRejected=True,independentModelRejectedAfterActualCallerReturn=True,reason=reason))
        original=(source.parent/'context.h').read_text();resource='opaque0[24]'if'opaque0[24]'in original else'opaque[24]'
        for label,before,after in [('resource-offset',resource,resource.replace('24','20')),('link-offset','u8 opaque[3]','u8 opaque[7]'),('signed-byte','typedef signed char s8;','typedef unsigned char s8;')]:
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
