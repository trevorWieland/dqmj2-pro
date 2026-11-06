import copy
import hashlib
import re
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261106_dwc_match_next_seventh_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

STATE,BITMAP,GLOBAL,CTRL,LIST,STOP,SP=0x209be60,0x209beac,0x21d19e0,0x2171000,0x2173000,0x27e0000,0x2701000
EXPECTED={STATE:'03490b685a6a9a62096848627047c046e0191d02',BITMAP:'78b400252e1c002907dd0123825d1c1c761c944025438e42f8db281c78bc7047'}
SITES={STATE:[0x209c080,0x209c08c,0x209c13c],BITMAP:[0x209c0d6]}


def validate(value,image,inventory,records):
    if len(value['helpers'])!=2 or (value['stateReadOffset'],value['lastStateWriteOffset'],value['aidDomain'],value['helperSourceCredit'])!=(0x24,0x28,[0,31],0):raise ValueError('Exact original helper field/domain contract differs')
    for row,a in zip(value['helpers'],[STATE,BITMAP]):
        size=len(bytes.fromhex(EXPECTED[a]))
        if (row['program'],row['processor'],row['module'],row['mode'],row['address'],row['bytes'])!=('','arm9','main','thumb',hex(a),size):raise ValueError('Exact original helper namespace/mode/boundary differs')
        body=image[a-0x2000000:a-0x2000000+size]
        if body.hex()!=row['originalHex'] or row['originalHex']!=EXPECTED[a] or hashlib.sha256(body).hexdigest()!=row['targetSha256']:raise ValueError('Complete original canonical helper bytes differ')
        canonical=f'func_{a:08x} kind:function(thumb,size=0x{size:x}) addr:0x{a:08x}'
        if row['canonicalInventoryRecord']!=canonical or canonical not in inventory.splitlines():raise ValueError('Original complete helper inventory boundary differs')
        wanted=[f'from:0x{site:08x} kind:thumb_call to:0x{a:08x} module:main' for site in SITES[a]]
        if row['callerOriginalRecords']!=wanted or any(x not in records.splitlines() for x in wanted):raise ValueError('Original caller/helper branch evidence differs')
        if len(row['sourceReferences'])!=2 or any(sha256(ROOT/p['path'])!=p['sha256'] for p in row['sourceReferences']):raise ValueError('Previously frozen helper ordinary C/include evidence differs')
    if 'from:0x0209be70 kind:load to:0x021d19e0 module:main' not in records.splitlines() or 'data_021d19e0 kind:bss addr:0x021d19e0' not in inventory.splitlines():raise ValueError('Original helper core-pointer data record differs')


def validate_layout(value,image,inventory,records):
    if tuple(value[k] for k in ['program','processor','module','mode','callerAddress','callerBytes','friendPointerOffset','matchPointerOffset','opaqueInterStartSpan','formalFriendControlSizeClaim','storageExtentAuthorshipCredit'])!=('','arm9','main','thumb',hex(0x209b450),0x1a4,0x318,0x378,96,False,0):raise ValueError('Measured adjacent initializer layout namespace/offset differs')
    canonical='func_0209b450 kind:function(thumb,size=0x1a4) addr:0x0209b450'
    if value['callerInventoryRecord']!=canonical or canonical not in inventory.splitlines() or hashlib.sha256(image[0x9b450:0x9b5f4]).hexdigest()!=value['callerTargetSha256']:raise ValueError('Original complete initializer body/boundary differs')
    for field,start,end in [('friend',0x209b52c,0x209b546),('match',0x209b546,0x209b56a)]:
        if value[field+'SequenceAddress']!=hex(start) or value[field+'SequenceHex']!=image[start-0x2000000:end-0x2000000].hex():raise ValueError('Original pointer-construction sequence differs')
    if image[0x9b538:0x9b53e].hex()!='c62080001018' or image[0x9b560:0x9b566].hex()!='de2080001018' or struct.unpack_from('<I',image,0x9b5d0)[0]!=GLOBAL:raise ValueError('Original R2 core pointer and R0 start offsets differ')
    if any(x not in records.splitlines() for x in ['from:0x0209b542 kind:thumb_call to:0x0209cdac module:main','from:0x0209b566 kind:thumb_call to:0x0209de84 module:main']):raise ValueError('Original adjacent initializer targets differ')


def standalone(image,address,seed):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);context=bytearray([0x61])*160;struct.pack_into('<I',context,0x24,seed+100);old=bytes(context);aids=bytes([0,31,seed%32,(seed+7)%32]);count=seed%5;cpu.mem_write(GLOBAL,struct.pack('<I',CTRL));cpu.mem_write(CTRL,old);cpu.mem_write(LIST,aids);initial=[0x64700000+i*0x101+seed for i in range(15)];initial[-2:]=[SP,STOP|1];initial[0]=seed%8 if address==STATE else LIST;initial[1]=count;cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    stopped=False;size=len(bytes.fromhex(EXPECTED[address]))
    def code(machine,at,length,user):
        nonlocal stopped
        if at==STOP:stopped=True;machine.emu_stop();return
        if not address<=at<address+size or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Original helper escaped complete canonical Thumb body')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.emu_start(address|1,STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS];expected=bytearray(old);expected_return=None
    if address==STATE:struct.pack_into('<II',expected,0x24,seed%8,seed+100)
    else:
        expected_return=0
        for aid in aids[:count]:expected_return|=1<<aid
    passed=stopped and regs[4:12]==initial[4:12] and regs[13]==SP and bytes(cpu.mem_read(CTRL,160))==expected and bytes(cpu.mem_read(LIST,4))==aids and struct.unpack('<I',cpu.mem_read(GLOBAL,4))[0]==CTRL and (expected_return is None or regs[0]==expected_return)
    if not passed:raise ValueError(('Original helper independent memory/bitmap/ABI model differs',hex(address),seed))
    return dict(address=hex(address),seed=seed,aidCount=count if address==BITMAP else None,returnBitmap=expected_return,expectedControlSha256=hashlib.sha256(expected).hexdigest(),completeOriginalReturn=True,calleeSavedAndStackPassed=True,modelPassed=True)


def execute():
    assert_owned(LANE,SOURCE,WORK);value=read_json(LANE/'helpers.json');layout=read_json(LANE/'initializer-layout.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text();validate(value,image,inventory,records);validate_layout(layout,image,inventory,records);observations=[standalone(image,a,seed) for a in [STATE,BITMAP] for seed in range(64)];negatives=[]
    for index in range(2):
        for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('address',hex(int(value['helpers'][index]['address'],0)+2)),('bytes',value['helpers'][index]['bytes']-2),('targetSha256','0'*64),('canonicalInventoryRecord','wrong'),('originalHex','00'*value['helpers'][index]['bytes']),('callerOriginalRecords',[])]:
            bad=copy.deepcopy(value);bad['helpers'][index][key]=wrong
            try:validate(bad,image,inventory,records)
            except ValueError:negatives.append(dict(helper=index,field=key,rejected=True))
            else:raise ValueError('Wrong original helper contract accepted')
        bad=bytearray(image);bad[int(value['helpers'][index]['address'],0)-0x2000000]^=1
        try:validate(value,bytes(bad),inventory,records)
        except ValueError:negatives.append(dict(helper=index,field='actual-original-byte',rejected=True))
        else:raise ValueError('Changed actual native helper body accepted')
    for key,wrong in [('stateReadOffset',0x28),('lastStateWriteOffset',0x24),('aidDomain',[0,32])]:
        bad=copy.deepcopy(value);bad[key]=wrong
        try:validate(bad,image,inventory,records)
        except ValueError:negatives.append(dict(field=key,rejected=True))
        else:raise ValueError('Wrong original helper typed domain accepted')
    for key,wrong in [('friendPointerOffset',0x31c),('matchPointerOffset',0x374),('opaqueInterStartSpan',92),('formalFriendControlSizeClaim',True),('mode','arm')]:
        bad=copy.deepcopy(layout);bad[key]=wrong
        try:validate_layout(bad,image,inventory,records)
        except ValueError:negatives.append(dict(layoutField=key,rejected=True))
        else:raise ValueError('Wrong original adjacent-start layout accepted')
    proof=dict(status='passed',root=str(ROOT),standaloneOriginalEntries=len(observations),observations=observations,negativeCases=negatives,initializerInstructionsExecuted=0,formalFriendTypeSizeProven=False,sourceCredit=0,calleeBodySourceCredit=0,originalStorageAuthorshipCredit=0);write_json(LANE/'helpers-proof.json',proof);return proof
