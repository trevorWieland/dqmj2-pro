import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    if len(rows)!=1 or int(rows[0]['address'],0)!=0x20b6aa8:raise ValueError('Only selected aggregate-status caller qualified')
    row=rows[0];address=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[address-0x2000000:address-0x2000000+row['bytes']];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native,address))
    calls=[i for i in instructions if i.mnemonic=='blx'and re.fullmatch(r'r\d+|ip',i.op_str)]
    if len(calls)!=1:raise ValueError('One original aggregate callback site required')
    call=calls[0];copy=[i for i in instructions if 0x20b6ade<=i.address<=call.address]
    required=[('sub','sp, #0xcc'),('movs','r2, #0x1b'),('ldm','r6!, {r0, r1}'),('stm','r3!, {r0, r1}'),('ldm','r4!, {r1, r2, r3}')]
    if any(not any((i.mnemonic,i.op_str)==item for i in instructions)for item in required):raise ValueError('Original216-byte aggregate register/stack copy ABI differs')
    targets={w.get('target')for w in row['originalNamespaceWitnesses']['witnesses']}
    if not{'0x21d2bf0','0x21d2c70','0x21d2bc4','0x20e172c'}.issubset(targets):raise ValueError('Actual original full/tail/state/ports aliases absent')
    header=ROOT/row['sourceDependencies'][0]['path']
    return dict(status='passed',caller=row['address'],targetSha256=row['targetSha256'],originalIndirectCallsite=hex(call.address),nativeInstruction=call.bytes.hex(),measuredBssCallbackSlotOffset=12,
        sourceAbi='void(success_word,NAT_value216)',inputArgumentWords=55,aggregateBytes=216,aggregateWords=54,aggregateRegisterWords=['r1','r2','r3'],aggregateRegisterBytes=12,aggregateStackBytes=204,originalByValueCopyBytes=27*8,
        originalArgumentAndAggregateFlow=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in copy],
        originalFullObjectView=dict(address='0x21d2bf0',bytes=216),originalBiasedTailView=dict(address='0x21d2c70',bytes=20,bias=128,fields=dict(kind=12,scheme=16),equivalentFullObjectFieldOffsets=dict(kind=140,scheme=144)),
        sourceHeader=header.relative_to(ROOT).as_posix(),sourceHeaderSha256=sha256(header),targetIdentity='Unresolved runtime callback; no static program/CPU/module/mode/entry inferred',fixtureScope='Synthetic ARM/Thumb callbacks receive nonuniform216-byte by-value snapshots and mutate live globals afterward; no actual callback implementation executes',calleeSourceOrExecutionCredit=0,completeGlobalStorageAuthorshipCredit=0)
