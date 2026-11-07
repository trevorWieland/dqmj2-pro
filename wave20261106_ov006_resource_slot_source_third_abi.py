import hashlib
import re
from project import ROOT
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from wave20261106_ov006_resource_slot_source_third_bindings import inputs


def check_source(source):
    text=source.read_text();header=(source.parent/'context.h').read_text()
    if re.findall(r'extern\s+void\s+native_fn_ov006_021e6e2c\s*\(([^)]*)\)\s*;',header)!=['u32']:raise ValueError('Measured helper consumes one complete u32 input; a zero-arg/narrow/unspecified declaration is not valid')
    if re.findall(r'\bnative_fn_ov006_021e6e2c\s*\(([^)]*)\)',text)!=['asset']:raise ValueError('Loaded opaque asset word must explicitly flow to real callee argument0')


def proof(source):
    check_source(source);value,images,inventories,records=inputs();image=images['ov006'];base=int(value['images']['ov006']['base'],0);a=0x21e6e2c;body=image[a-base:a-base+68];caller=image[0x21e7004-base:0x21e7018-base];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    decoded=[(i.address,i.mnemonic,i.op_str)for i in decoder.disasm(body,a)];by_address={x[0]:x[1:]for x in decoded}
    if by_address.get(a+8)!=('mov','r1, r0')or by_address.get(a+12)!=('add','r0, sp, #0')or by_address.get(a+16)!=('mov','r2, #0')or by_address.get(a+20)!=('bl','#0x204518c'):raise ValueError('Original helper input-use/known three-word layout boundary changed')
    call=[(i.address,i.mnemonic,i.op_str)for i in decoder.disasm(caller,0x21e7004)]
    if call[-3:]!=[(0x21e700c,'bl','#0x203cc2c'),(0x21e7010,'mov','r4, r0'),(0x21e7014,'bl','#0x21e6e2c')]:raise ValueError('Actual original loader result/input-preservation/call word sequence differs')
    canonical='func_ov006_021e6e2c kind:function(arm,size=0x44) addr:0x021e6e2c'
    if canonical not in inventories['ov006'].splitlines():raise ValueError('Original canonical same-module ARM entry absent')
    return dict(program='',processor='arm9',module='ov006',mode='arm',address=hex(a),bytes=68,nativeBodySha256=hashlib.sha256(body).hexdigest(),canonicalEntry=canonical,actualOriginalCallerSequence=call,calleeEntryUse=decoded[:6],consumedSourceBoundary='void native_fn_ov006_021e6e2c(u32); called with the just-loaded opaque asset word',calleeFunctionsOrBytesOrExecutionsCredited=0,limits='A one-word caller/import contract is qualified; the callee is not reconstructed or executed, and its internal layout/storage/IO semantics are not credited.')
