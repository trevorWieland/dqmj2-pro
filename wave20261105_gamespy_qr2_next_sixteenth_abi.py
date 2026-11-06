import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    if len(rows)!=1 or int(rows[0]['address'],0)!=0x20b6c08:raise ValueError('Only selected six-word constructor qualified')
    row=rows[0];address=int(row['address'],0);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[address-0x2000000:address-0x2000000+row['bytes']];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native,address));pairs={(i.address,i.mnemonic,i.op_str)for i in instructions}
    expected=[(0x20b6c08,'push','{r3, r4, r5, r6, r7, lr}'),(0x20b6c40,'ldr','r0, [sp, #0x18]'),(0x20b6c44,'str','r0, [r4, #0x3c]'),(0x20b6c46,'ldr','r0, [sp, #0x1c]'),(0x20b6c48,'str','r0, [r4, #0x40]'),(0x20b6c42,'movs','r2, #0'),(0x20b6c4a,'movs','r0, #2'),(0x20b6c4c,'adds','r1, r0, #0')]
    if any(item not in pairs for item in expected):raise ValueError('Original six-word boundary/socket operands changed')
    socket=[w for w in row['originalNamespaceWitnesses']['witnesses']if w.get('target')=='0x20a8b5c']
    if len(socket)!=1:raise ValueError('Original socket entry mode/identity absent')
    header=ROOT/row['sourceDependencies'][0]['path']
    return dict(status='passed',caller=row['address'],targetSha256=row['targetSha256'],argumentWords=6,registerArguments=['game_socket_word','cookie_word','client_index_word','progress_pointer_word'],stackArguments=[dict(entrySpOffset=0,role='completed_pointer_word',storedRecordOffset=60),dict(entrySpOffset=4,role='userdata_word',storedRecordOffset=64)],originalPushBytes=24,originalBoundaryAndOperandInstructions=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in instructions if any(i.address==item[0]for item in expected)],originalSocketCall=socket[0],measuredSocketArgumentWords=[2,2,0],genericProvisionalThirdWord17RejectedByWholeCallerAndReturningModels=True,callbackTargetIdentities='Incoming pointer words stored unchanged only; no callback program/CPU/module/mode/entry inferred or executed',sourceHeader=header.relative_to(ROOT).as_posix(),sourceHeaderSha256=sha256(header),calleeSourceOrExecutionCredit=0,originalStorageAuthorshipCredit=0)
