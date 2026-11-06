import re
import hashlib
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    indexed={int(row['address'],0):row for row in rows};assert len(indexed)==13
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);row=indexed[0x20b4ad4];items=list(cs.disasm(image[0xb4ad4:0xb4be0],0x20b4ad4))
    assert(items[0].mnemonic,items[0].op_str)==('push','{r3, r4, r5, r6, r7, lr}')and(items[1].mnemonic,items[1].op_str)==('sub','sp, #0x18')
    required=[('ldr','r0, [sp, #0x34]'),('str','r0, [sp, #0x34]'),('ldr','r1, [sp, #0x30]')];assert all(any((i.mnemonic,i.op_str)==q for i in items)for q in required)
    spill=next(i for i in items if i.address==0x20b4ade);assert(spill.mnemonic,spill.op_str)==('str','r0, [sp, #0x34]')
    pointer=next(w for w in row['originalNamespaceWitnesses']['witnesses']if w['origin']=='0x20b4be0');assert pointer['target']=='0x20b4ac9'and pointer['canonicalInstructionEntry']=='0x20b4ac8'and pointer['mode']=='thumb'
    return dict(status='passed',bufferIncomingAbi=dict(caller='0x20b4ad4',inputWords=6,registerWords=4,entryStackWords=['message_len@entrySP+0','overflow_pointer@entrySP+4'],savedRegisterBytes=24,localStackBytes=24,actualOriginalInstructionFlow=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in items if i.address<=0x20b4ae4],incomingPointerIdempotentSpill=dict(originalInstructionAddress=hex(spill.address),bytes=spill.bytes.hex(),entryOffset=4,width=4,storedValue='Unchanged incoming overflow-pointer word loaded at4ada',fixtureAllowance='Only caller020b4ad4,entrySP+4,width4 and exact fixture OV pointer value; all other caller writes remain bounded',oldFrozenFixturesUnchanged=True),originalTypedComparatorPointer=pointer,comparatorOriginalBodySha256=hashlib.sha256(image[0xb4ac8:0xb4ad4]).hexdigest(),comparatorBodyBytes=12,comparatorSourceOrExecutionCredit=0),incomingMessageRecord=dict(cSize=16,definedForwardedPrefixBytes=14,fields=dict(start=0,length=4,type=8,serial=12),uninitializedPaddingBytes=[14,15],independentArrayInsertProjection='Only14 initialized bytes are interpreted; source/native caller GPR/CPSR/ordered-write traces still compare completely'),sourceHeaders=sorted({(pin['path'],sha256(ROOT/pin['path']))for row in rows for pin in row['sourceDependencies']}),limits=['Published C definitions were exposed in private diagnostic builds to prevent unused static-handler deletion; all final selected translation units are ordinary C with exact full extents and genuine links.','Array/collection/auth/filter/delivery/helper behavior is supplied ABI context. The comparator is passed with an actually qualified Thumb entry/tag and its body never executes in these caller fixtures.','Uninitialized incoming-record padding has no inferred content. No original storage, opaque helper body, networking/device/scenes or game/platform completion credit is granted.'])
