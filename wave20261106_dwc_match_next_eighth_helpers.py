import copy
import hashlib
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json
from wave20261106_dwc_match_next_eighth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

TYPE,MASK,WORD,STRLEN,LIST,STOP,SP=0x2096d9c,0x2096cf8,0x2096ce8,0x201d69c,0x2173000,0x27e0000,0x2701000
EXPECTED={TYPE:('thumb','004b1847f96c0902'),MASK:('thumb','08b5fff7f5ff0321084008bd'),WORD:('thumb','0068c10a014808407047c046ffff1f00'),STRLEN:('arm','0020e0e3d110d0e0012082e2000051e3fbffff1a0200a0e11eff2fe1')}


def validate(value,image,inventory,records):
    if len(value['helpers'])!=4 or tuple(value[k] for k in ['typeWordOffset','typeShift','typeMask','originalBindingVeneerCredit','calleeSourceCredit'])!=(0,11,3,0,0):raise ValueError('Exact original helper field/mask/source-credit contract differs')
    for row,a in zip(value['helpers'],[TYPE,MASK,WORD,STRLEN]):
        mode,hexadecimal=EXPECTED[a];size=len(bytes.fromhex(hexadecimal))
        if tuple(row[k] for k in ['program','processor','module','mode','address','bytes'])!=('','arm9','main',mode,hex(a),size):raise ValueError('Exact canonical helper namespace/mode/boundary differs')
        body=image[a-0x2000000:a-0x2000000+size];canonical=f'func_{a:08x} kind:function({mode},size=0x{size:x}) addr:0x{a:08x}'
        if body.hex()!=row['originalHex'] or row['originalHex']!=hexadecimal or hashlib.sha256(body).hexdigest()!=row['targetSha256']:raise ValueError('Complete original helper bytes differ')
        if row['canonicalInventoryRecord']!=canonical or canonical not in inventory.splitlines():raise ValueError('Complete original helper canonical boundary differs')
    needed=['from:0x0209d524 kind:thumb_call to:0x02096d9c module:main','from:0x02096da0 kind:load to:0x02096cf9 module:main','from:0x02096cfa kind:thumb_call to:0x02096ce8 module:main','from:0x0209c1b0 kind:thumb_call_arm to:0x0201d69c module:main']
    if any(x not in records.splitlines() for x in needed) or struct.unpack_from('<I',image,0x96da0)[0]!=(MASK|1):raise ValueError('Original helper call/veneer literal/Thumb-tag chain differs')


def standalone(image,address,seed):
    thumb=address==TYPE;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB if thumb else un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);word=1<<seed if seed<32 else ((seed*0x9e3779b1)^0x67234891)&0xffffffff;payload=struct.pack('<III',word,0x12345678,0x23456789) if thumb else bytes(((i*137+seed)%255)+1 for i in range(seed%33))+bytes([0])+bytes([0x61])*4;pointer=LIST+(seed%4 if not thumb else 0);cpu.mem_write(pointer,payload);initial=[0x64700000+i*0x101+seed for i in range(15)];initial[-2:]=[SP,STOP|1];initial[0]=pointer;cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|(0x30 if thumb else 0x10))
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    stopped=False;nested=[]
    def code(machine,at,length,user):
        nonlocal stopped
        if at==STOP:stopped=True;machine.emu_stop();return
        for start,(mode,hexadecimal) in EXPECTED.items():
            if start<=at<start+len(bytes.fromhex(hexadecimal)):
                if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Original helper mode differs')
                if at in [MASK,WORD]:nested.append(hex(at))
                return
        raise ValueError('Original helper escaped canonical chain')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.emu_start(address|int(thumb),STOP+4,count=10000);regs=[cpu.reg_read(r) for r in C.REGISTERS];result=(word>>11)&3 if thumb else seed%33
    if not stopped or regs[0]!=result or regs[4:12]!=initial[4:12] or regs[13]!=SP or bytes(cpu.mem_read(pointer,len(payload)))!=payload or nested!=([hex(MASK),hex(WORD)] if thumb else []):raise ValueError(('Original helper independent type/strlen/ABI model differs',hex(address),seed))
    return dict(address=hex(address),seed=seed,completeOriginalReturn=True,returnValue=result,originalNestedCalleeEntries=nested,calleeSavedAndStackPassed=True,readOnlyMemoryPassed=True)


def execute():
    assert_owned(LANE,SOURCE,WORK);value=read_json(LANE/'helpers.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text();validate(value,image,inventory,records);observations=[standalone(image,a,seed) for a in [TYPE,STRLEN] for seed in range(64)];negative=[]
    for index in range(4):
        for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm' if value['helpers'][index]['mode']=='thumb' else 'thumb'),('address',hex(int(value['helpers'][index]['address'],0)+2)),('bytes',value['helpers'][index]['bytes']-2),('targetSha256','0'*64),('canonicalInventoryRecord','wrong'),('originalHex','00'*value['helpers'][index]['bytes'])]:
            bad=copy.deepcopy(value);bad['helpers'][index][key]=wrong
            try:validate(bad,image,inventory,records)
            except ValueError:negative.append(dict(helper=index,field=key,rejected=True))
            else:raise ValueError('Wrong canonical helper contract accepted')
        bad=bytearray(image);bad[int(value['helpers'][index]['address'],0)-0x2000000]^=1
        try:validate(value,bytes(bad),inventory,records)
        except ValueError:negative.append(dict(helper=index,field='actual-original-byte',rejected=True))
        else:raise ValueError('Changed complete original helper body accepted')
    for key,wrong in [('typeWordOffset',4),('typeShift',10),('typeMask',7)]:
        bad=copy.deepcopy(value);bad[key]=wrong
        try:validate(bad,image,inventory,records)
        except ValueError:negative.append(dict(field=key,rejected=True))
        else:raise ValueError('Wrong original field extraction accepted')
    proof=dict(status='passed',root=str(ROOT),standaloneOriginalEntries=len(observations),originalNestedCalleeEntries=sum(len(r['originalNestedCalleeEntries']) for r in observations),observations=observations,negativeCases=negative,originalTypeVeneerSourceCredit=0,calleeBodySourceCredit=0,originalStorageAuthorshipCredit=0);write_json(LANE/'helpers-proof.json',proof);return proof
