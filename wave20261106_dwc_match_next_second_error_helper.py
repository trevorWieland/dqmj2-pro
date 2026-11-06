import copy
import hashlib
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261106_dwc_match_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

ENTRY,END,GLOBAL,STOP,SP=0x209a9e4,0x209a9f8,0x21d19ac,0x27e0000,0x2701000
EXPECTED='03480068002801d00120704700207047ac191d02'


def validate(value,image,inventory,records):
    if (value['program'],value['processor'],value['module'],value['mode'],value['address'],value['bytes'])!=('','arm9','main','thumb',hex(ENTRY),20):raise ValueError('Exact error leaf identity differs')
    body=image[ENTRY-0x2000000:END-0x2000000]
    if body.hex()!=EXPECTED or hashlib.sha256(body).hexdigest()!=value['targetSha256']:raise ValueError('Whole original error leaf differs')
    if value['inventoryRecord']!='func_0209a9e4 kind:function(thumb,size=0x14) addr:0x0209a9e4' or value['inventoryRecord'] not in inventory.splitlines():raise ValueError('Canonical error leaf boundary differs')
    if value['originalLiteralRecord']!='from:0x0209a9f4 kind:load to:0x021d19ac module:main' or value['originalLiteralRecord'] not in records.splitlines():raise ValueError('Actual error leaf load differs')
    if value['globalRecord']!='data_021d19ac kind:bss addr:0x021d19ac' or value['globalRecord'] not in inventory.splitlines() or value['globalWidth']!=4:raise ValueError('Actual error BSS kind/width differs')
    if struct.unpack_from('<I',body,16)[0]!=GLOBAL:raise ValueError('Actual error leaf literal word differs')


def execute():
    assert_owned(LANE,SOURCE,WORK)
    value=read_json(LANE/'error-helper.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text();validate(value,image,inventory,records)
    observations=[]
    for seed,error in enumerate([0,1,2,0xffffffff,0x80000000,0x7fffffff,0x100,0xffff]*4):
        cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(GLOBAL,struct.pack('<I',error));cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000)
        initial=[(0x51c00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
        cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
        for reg,item in zip(C.REGISTERS,initial):cpu.reg_write(reg,item)
        done=[]
        def code(machine,at,size,user):
            if at==STOP:done.append(machine.reg_read(ar.UC_ARM_REG_R0));machine.emu_stop();return
            if not ENTRY<=at<ENTRY+16 or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Original error leaf escaped canonical instruction range/mode')
        def write(machine,access,at,size,item,user):raise ValueError('Original error leaf wrote memory')
        cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ENTRY|1,STOP+4,count=20)
        registers=[cpu.reg_read(r) for r in C.REGISTERS]
        if done!=[int(error!=0)] or registers[4:12]!=initial[4:12] or registers[13]!=SP or bytes(cpu.mem_read(GLOBAL,4))!=struct.pack('<I',error):raise ValueError('Original error predicate/ABI differs')
        observations.append(dict(seed=seed,errorWord=error,returned=done[0],expected=int(error!=0),calleeSavedAndMemoryPreserved=True))
    negatives=[]
    for name,key,wrong in [('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('mode','mode','arm'),('interior-entry','address',hex(ENTRY+2)),('extent','bytes',18),('word-width','globalWidth',2),('wrong-BSS','globalRecord',value['globalRecord'].replace('021d19ac','021d19b0')),('wrong-load','originalLiteralRecord',value['originalLiteralRecord'].replace('021d19ac','021d19b0'))]:
        bad=copy.deepcopy(value);bad[key]=wrong
        try:validate(bad,image,inventory,records)
        except ValueError:negatives.append(name)
        else:raise ValueError('Invalid original error helper contract accepted')
    for offset in [0,6,16]:
        bad=bytearray(image);bad[ENTRY-0x2000000+offset]^=1
        try:validate(value,bytes(bad),inventory,records)
        except ValueError:negatives.append('native-byte-'+str(offset))
        else:raise ValueError('Changed original error helper accepted')
    proof=dict(status='passed',originalEntry=hex(ENTRY),bytes=20,standaloneOriginalEntries=len(observations),observations=observations,negativeCases=negatives,sourceCredit=0,calleeBodySourceCredit=0,originalStorageAuthorshipCredit=0)
    write_json(LANE/'error-helper-proof.json',proof);return proof
