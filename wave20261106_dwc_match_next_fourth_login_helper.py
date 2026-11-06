import copy
import hashlib
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json
from wave20261106_dwc_match_next_fourth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

ENTRY,GLOBAL,CTRL,STOP,SP=0x209cba8,0x21d1b68,0x2171000,0x27e0000,0x2701000
EXPECTED='05484068002804d04068052801d10120704700207047c046681b1d02'


def validate(value,image,inventory,records):
    if (value['program'],value['processor'],value['module'],value['mode'],value['address'],value['bytes'])!=('','arm9','main','thumb',hex(ENTRY),28):raise ValueError('Exact original login leaf identity differs')
    body=image[ENTRY-0x2000000:ENTRY-0x2000000+28]
    if body.hex()!=EXPECTED or hashlib.sha256(body).hexdigest()!=value['targetSha256']:raise ValueError('Original complete login leaf differs')
    if value['inventoryRecord']!='func_0209cba8 kind:function(thumb,size=0x1c) addr:0x0209cba8' or value['inventoryRecord'] not in inventory.splitlines():raise ValueError('Canonical original login leaf boundary differs')
    if value['originalLiteralRecord']!='from:0x0209cbc0 kind:load to:0x021d1b68 module:main' or value['originalLiteralRecord'] not in records.splitlines() or struct.unpack_from('<I',body,24)[0]!=GLOBAL:raise ValueError('Original login leaf BSS literal differs')
    if value['globalRecord']!='data_021d1b68 kind:bss addr:0x021d1b68' or value['globalRecord'] not in inventory.splitlines() or value['pointerOffset']!=4 or value['stateOffset']!=4 or value['width']!=4:raise ValueError('Original login pointer/state view differs')


def execute():
    assert_owned(LANE,SOURCE,WORK);value=read_json(LANE/'login-helper.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text();validate(value,image,inventory,records);observations=[]
    for seed in range(64):
        present=bool(seed//32);state=[0,1,2,3,4,5,6,0xffffffff][(seed//4)%8];cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(GLOBAL,struct.pack('<III',0x12345678,CTRL if present else 0,0x87654321));cpu.mem_write(CTRL,struct.pack('<II',0xabcdef11,state));cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);initial=[(0x51d00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
        cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
        for reg,item in zip(C.REGISTERS,initial):cpu.reg_write(reg,item)
        done=[]
        def code(machine,at,size,user):
            if at==STOP:done.append(machine.reg_read(ar.UC_ARM_REG_R0));machine.emu_stop();return
            if not ENTRY<=at<ENTRY+22 or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Original login leaf escaped instruction range/mode')
        def write(machine,access,at,size,item,user):raise ValueError('Original login leaf wrote memory')
        cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ENTRY|1,STOP+4,count=24);registers=[cpu.reg_read(r) for r in C.REGISTERS]
        if done!=[int(present and state==5)] or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Original login predicate/ABI differs')
        observations.append(dict(seed=seed,present=present,state=state,returned=done[0],expected=int(present and state==5),calleeSavedAndMemoryPreserved=True))
    negatives=[]
    for name,key,wrong in [('CPU','processor','arm7'),('program','program','child'),('module','module','ov000'),('mode','mode','arm'),('interior-entry','address',hex(ENTRY+2)),('extent','bytes',26),('pointer-offset','pointerOffset',8),('state-offset','stateOffset',8),('width','width',2),('wrong-load','originalLiteralRecord',value['originalLiteralRecord'].replace('021d1b68','021d1b6c'))]:
        bad=copy.deepcopy(value);bad[key]=wrong
        try:validate(bad,image,inventory,records)
        except ValueError:negatives.append(name)
        else:raise ValueError('Invalid original login leaf contract accepted')
    for offset in [0,10,24]:
        bad=bytearray(image);bad[ENTRY-0x2000000+offset]^=1
        try:validate(value,bytes(bad),inventory,records)
        except ValueError:negatives.append('native-byte-'+str(offset))
        else:raise ValueError('Changed original login leaf accepted')
    proof=dict(status='passed',originalEntry=hex(ENTRY),bytes=28,standaloneOriginalEntries=len(observations),observations=observations,negativeCases=negatives,sourceCredit=0,calleeBodySourceCredit=0,originalStorageAuthorshipCredit=0);write_json(LANE/'login-helper-proof.json',proof);return proof
