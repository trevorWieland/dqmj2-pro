import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    assert len(rows)==1 and rows[0]['address']=='0x20b438c';row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();items=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(image[0xb438c:0xb447e],0x20b438c))
    assert(items[0].mnemonic,items[0].op_str)==('push','{r4, r5, r6, r7, lr}')and(items[1].mnemonic,items[1].op_str)==('sub','sp, #0x14')
    loads=[i for i in items if i.mnemonic=='ldr'and re.fullmatch(r'r\d+, \[sp, #0x(?:28|2c|30|34)\]',i.op_str)];assert{int(re.search(r'#(0x[0-9a-f]+)',i.op_str)[1],0)for i in loads}=={40,44,48,52}
    return dict(status='passed',caller=row['address'],inputWords=8,registerArguments=['socket','connection_out_pointer','remote_address','message'],entryStackArguments=['length@0','timeout@4','callbacks_pointer@8','blocking_word@12'],savedRegisterBytes=20,localStackBytes=20,originalStackArgumentLoads=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in loads],observedHelperEntries=[w['target']for w in row['originalNamespaceWitnesses']['witnesses']if 'actualMnemonic'in w],sourceHeaders=sorted({(pin['path'],sha256(ROOT/pin['path']))for pin in row['sourceDependencies']}),limits=['Callbacks pointer is forwarded as incoming data and no callback implementation executes. Constructor/start/free/think/sleep/parser effects are supplied contracts.','Blocking-loop models deliberately provide finite state progress. Connected completion requires a nonnull connection output pointer, matching the source boundary; hangs, device networking and invalid-pointer behavior are unproved.','All original storage, opaque helper bodies, actual service/device/scenes and game/platform completion receive zero extra credit.'])
