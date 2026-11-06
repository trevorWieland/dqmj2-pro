import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();evidence=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native,address));calls=[i for i in instructions if i.mnemonic=='blx'and re.fullmatch(r'r\d+|ip',i.op_str)]
        expected={0x20b67e0:[('completedCallback',60,'void(result_word,socket_word,peer8*,userdata_word)',[68,72,76,64])]}.get(address,[])
        if len(calls)!=len(expected):raise ValueError('Original indirect NAT callback count changed')
        header=ROOT/row['sourceDependencies'][0]['path']
        for call,(name,slot,signature,fields)in zip(calls,expected):
            nearby=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in instructions if call.address-30<=i.address<=call.address]
            evidence.append(dict(caller=row['address'],targetSha256=row['targetSha256'],slot=name,measuredRecordSlotOffset=slot,sourceAbi=signature,measuredArgumentFieldOffsets=fields,originalIndirectCallsite=hex(call.address),nativeInstruction=call.bytes.hex(),nearbyOriginalSlotAndArgumentFlow=nearby,sourceHeader=header.relative_to(ROOT).as_posix(),sourceHeaderSha256=sha256(header),targetIdentity='Unresolved runtime function-pointer input; no static program/CPU/module/mode/entry inferred',fixtureScope='Synthetic ARM/Thumb/mixed inputs only',calleeSourceOrExecutionCredit=0))
    if len(evidence)!=1:raise ValueError('One measured completion callback site required')
    return dict(status='passed',program='',processor='arm9',module='main',mode='thumb',witnesses=evidence,recordViewBytes=84,completeObjectStorageCredit=0,noStaticCallbackNamespaceInvented=True)
