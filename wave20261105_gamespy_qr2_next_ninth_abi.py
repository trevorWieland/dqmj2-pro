import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(row):
    header=ROOT/'src/runtime/parallel_wave20261105/gamespy-qr2-next/ninth/020b7920/types.h'
    text=header.read_text();address=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[address-0x2000000:address-0x2000000+row['bytes']]
    instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native,address));calls=[item for item in instructions if item.mnemonic=='blx' and re.fullmatch(r'r\d+|ip',item.op_str)]
    slots=[('playerteam_count_callback',152,'int(key_type,void*)'),('key_list_callback',148,'void(key_type,key_buffer*,void*)'),('server_key_callback',136,'void(int,buffer*,void*)'),('server_key_callback',136,'void(int,buffer*,void*)'),('player_key_callback',140,'void(int,int,buffer*,void*)'),('team_key_callback',144,'void(int,int,buffer*,void*)')]
    if len(calls)!=len(slots) or 'unsigned char unknown_0ac_10b[96];' not in text or 'void* udata;' not in text:raise ValueError('Measured partial callback view changed')
    witnesses=[]
    for call,(name,offset,signature) in zip(calls,slots):
        nearby=[dict(address=hex(item.address),instruction=item.mnemonic+' '+item.op_str,bytes=item.bytes.hex()) for item in instructions if call.address-24<=item.address<=call.address]
        witnesses.append(dict(slot=name,measuredSlotOffset=offset,sourceAbi=signature,userdataWordOffset=268,originalIndirectCallsite=hex(call.address),originalInstruction=call.mnemonic+' '+call.op_str,originalBytes=call.bytes.hex(),nearbyOriginalArgumentAndSlotFlow=nearby,
            targetIdentity='Unresolved runtime function-pointer input; original target/module/mode is not inferred',fixtureScope='Synthetic ARM/Thumb interworking inputs only',calleeSourceOrExecutionCredit=0))
    return dict(status='passed',program='',processor='arm9',module='main',mode='thumb',address=row['address'],targetSha256=row['targetSha256'],sourceHeader=header.relative_to(ROOT).as_posix(),sourceHeaderSha256=sha256(header),witnesses=witnesses,
        knownRecordPrefix=[0,172],opaqueRecordInterval=[172,268],userdataOffset=268,viewExtent=272,completeObjectStorageCredit=0,noStaticCallbackNamespaceInvented=True)
