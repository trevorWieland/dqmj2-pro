import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_later_sdk_build import build
from wave20261105_main_later_sdk_bindings import verify_original

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk'
WORK=ROOT/'work/w5ml/sdk/fixtures'
BASE,PLAYER,COMMAND,STOP,SP=0x2000000,0x2170000,0x2172000,0x27e0000,0x2701000


def run(image,address,body,player_flags,counter,status,seed,flags):
    player=bytearray(((i*29+seed*17)&127)|128 for i in range(0x174));command=bytearray([0x53]*0x30)
    struct.pack_into('<I',player,0x110,player_flags);struct.pack_into('<i',player,0x114,counter);struct.pack_into('<I',player,0x118,0xdeadbeef);struct.pack_into('<I',player,0x134,0);struct.pack_into('<I',player,0x13c,0);struct.pack_into('<I',player,0x16c,0)
    struct.pack_into('<IIII',command,8,PLAYER,status,0,0);struct.pack_into('<I',command,0x2c,0);expected=bytearray(player)
    if address==0x203ab50:
        if player_flags&0x20 and counter>0:struct.pack_into('<i',expected,0x114,counter-1)
        if status==0:struct.pack_into('<I',expected,0x118,1)
    elif player_flags&1:raise ValueError('Inactive-only shutdown fixture received active state')
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(address,body);cpu.mem_write(PLAYER,bytes(player));cpu.mem_write(COMMAND,bytes(command));cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000)
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0]=COMMAND if address==0x203ab50 else PLAYER;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    reads=[];writes=[];pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        executable_end=address+len(body)-(20 if address==0x203ab50 else 8)
        if not address<=at<executable_end:raise ValueError('Administrative fixture entered imported callback/I/O/helper/data code')
        pcs.append(hex(at))
    def memory(machine,access,at,size,value,user):
        if SP-0x1000<=at<SP:return
        (writes if access==un.UC_MEM_WRITE else reads).append([hex(at),size])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_READ|un.UC_HOOK_MEM_WRITE,memory);cpu.emu_start(address,STOP+4,count=256)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS];actual_player=bytes(cpu.mem_read(PLAYER,len(player)));actual_command=bytes(cpu.mem_read(COMMAND,len(command)))
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Complete administrative caller failed actual return/ABI bound')
    expected_writes=[]
    if address==0x203ab50:
        if player_flags&0x20 and counter>0:expected_writes.append([hex(PLAYER+0x114),4])
        if status==0:expected_writes.append([hex(PLAYER+0x118),4])
    allowed_reads={PLAYER+0x110,PLAYER+0x114,PLAYER+0x134,COMMAND+8,COMMAND+0xc,COMMAND+0x10,COMMAND+0x2c}
    correct=actual_player==bytes(expected) and actual_command==bytes(command) and writes==expected_writes and all(int(at,0) in allowed_reads and width==4 for at,width in reads)
    actual=dict(registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),playerSha256=C.sha(actual_player),commandSha256=C.sha(actual_command),reads=reads,writes=writes,pcs=pcs,actualTopReturn=True,actualImportedBodiesOrCallbacksExecuted=0)
    return actual,correct


def execute(rows):
    row=next(r for r in rows if r['address']=='0x203ab50');source=ROOT/row['source'];text=source.read_text();before='player->finishCounter--;'
    if text.count(before)!=1:raise ValueError('Administrative counter mutation not isolated')
    target=WORK/'wrong-counter/source.c';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text.replace(before,'player->finishCounter++;'))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],target.parent/(ROOT/pin['path']).name)
    bad,bad_body=build(target,target.parent/'build',True);verify_original(bad,bad['nativeSymbolEntries'])
    if bad['compiledBytes']!=2088 or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong complete2088B C must genuinely compile/link and fail native bytes')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negatives=[];seed=0
    for address in (0x203a5ec,0x203ab50):
        row=next(r for r in rows if int(r['address'],0)==address);native=image[address-BASE:address-BASE+row['bytes']];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        if address==0x203a5ec:vectors=[(pf,0,0) for pf in (0,2,4,0x20,0x40,0xfffffffe) for repeat in range(4)]
        else:vectors=[(pf,counter,status) for pf in (0,0x10,0x20,0x40,0xffffffff) for counter in (-1,0,1,5,2147483647) for status in (0,1,2,0xffffffff)]
        for pf,counter,status in vectors:
            flags=((seed&15)<<28)|0x10;args=(pf,counter,status,seed,flags);seed+=1;original,ok=run(image,address,native,*args);rebuilt,good=run(image,address,linked,*args)
            if not ok or not good or original!=rebuilt:raise ValueError(('Independent administrative memory model failed',hex(address),args,ok,good,original))
            records.append(dict(address=hex(address),playerFlags=hex(pf),counter=counter,status=status,seed=seed-1,flags=flags,original=original,recompiled=rebuilt))
            if address==0x203ab50 and pf&0x20 and counter in (1,5):
                negative,accepted=run(image,address,bad_body,*args)
                if accepted:raise ValueError('Wrong counter increment escaped independent expected decrement model')
                negatives.append(dict(counter=counter,playerFlags=hex(pf),status=status,result=negative,independentAdministrativeModelRejected=True))
    result=dict(status='passed',traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),functionsWithAdministrativePaths=2,supportedReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),wrongReturningControls=len(negatives),wholeCNegativeControlsRejected=1,actualNativeCalleeBodiesExecuted=0,actualCallbacksOrIOOrHardwareExecuted=0,originalStorageExtentAuthorshipCredit=0,decoderPayloadPathsExecuted=0,unicornVersion=un.__version__,wrongC=dict(row=bad,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target)),records=records,wrongRecords=negatives,limits=['Complete100B ShutdownPlayer executes only inactive bit0-clear early-return states. Complete2088B MakeWaveData executes only zero-buffer/zero-channel/null-callback administrative paths, including finish-counter decrement and setup prepareFlag update.','Actual top returns and precise supplied player/command memory, preserved ABI and absence of imported/callback/data execution are checked. Wrong complete2088B C increments instead of decrements and is rejected after genuine compile/link and actual return.','PCM/ADPCM payload decoding, valid audio files/game state, callbacks, streaming I/O, mutexes, cache operations, devices and scenes remain unexecuted. These finite administrative vectors do not establish those paths; complete source-byte and full genuine-link evidence are separate.'])
    write_json(LANE/'administrative-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongRecords','wrongC']}
