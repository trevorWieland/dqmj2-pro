import copy
import hashlib
import re
import struct
from project import ROOT,sha256
from link_runtime_unit import verify_binding

RELOCS=ROOT/'config/arm9/itcm/relocs.txt'
RELOCS_SHA='f541e035c6c46247f15d2a546022138d8b8ba3f291283b52b56001064a9bc055'
SITES={32:(0x1ff8370,'itcm'),64:(0x2007ff4,'main'),72:(0x2007270,'main'),76:(0x2007264,'main'),84:(0x2008008,'main'),88:(0x2007338,'main'),92:(0x200732c,'main'),136:(0x1ff8370,'itcm'),152:(0x1ff8370,'itcm')}


def verify_original(row,bindings):
    if (row.get('program')or'',row['processor'],row['module'],row['mode'],row['address'],row['bytes'])!=('','arm9','itcm','arm','0x1ff82c8',168):raise ValueError('Exact ITCM reset caller namespace/extent differs')
    if sha256(RELOCS)!=RELOCS_SHA:raise ValueError('Pinned original ITCM branch inventory changed')
    image=ROOT/'extract/arm9/itcm.bin'
    if sha256(image)!='69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb':raise ValueError('Full original ITCM image changed')
    native=image.read_bytes()[0x2c8:0x370]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or struct.unpack('<II',native[160:])!=(0x27ffc2c,0x27ffe20):raise ValueError('Original full caller or physical reserved header pointer literals changed')
    records=set(RELOCS.read_text().splitlines());witnesses=[]
    if {r['offset']for r in row['relocations']}!=set(SITES) or len(row['relocations'])!=9:raise ValueError('Complete original reset branch set differs')
    for r in row['relocations']:
        target,module=SITES[r['offset']];binding=bindings[r['symbol']];origin=0x1ff82c8+r['offset'];record=f'from:0x{origin:08x} kind:arm_call to:0x{target:08x} module:{module}'
        if (r['type'],r['addend'],r['symbol'],r['target'])!=(1,-8,f'native_fn_{target:08x}',hex(target)) or record not in records:raise ValueError('Original ARM reset call origin/target/addend differs')
        if (binding.get('program')or'',binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=('','arm9',module,'arm','function',hex(target)):raise ValueError('Reset provider program/CPU/module/mode/kind/address differs')
        word=struct.unpack_from('<I',native,r['offset'])[0];disp=(word&0xffffff)<<2
        if disp&0x2000000:disp-=0x4000000
        if word>>24!=0xeb or origin+8+disp!=target:raise ValueError('Original full native call instruction differs')
        verify_binding(r['symbol'],binding)
        witnesses.append(dict(origin=hex(origin),target=hex(target),module=module,mode='arm',originalRecord=record,originalWordHex=native[r['offset']:r['offset']+4].hex(),calleeSourceCredit=0))
    return dict(originalRelocationsPath=RELOCS.relative_to(ROOT).as_posix(),originalRelocationsSha256=RELOCS_SHA,witnesses=witnesses,hardwareReservedPointers=[dict(literalOrigin='0x1ff8368',word='0x27ffc2c',meaning='original SDK reserved ROM-base word'),dict(literalOrigin='0x1ff836c',word='0x27ffe20',meaning='original ROM-header ARM9 source-word view')],originalHeaderOrHardwareStorageCredit=0)


def negative_controls(rows):
    row=rows[0];out=[]
    for rel in row['relocations']:
        for label,owner,key,value in [('origin','rel','offset',rel['offset']+4),('addend','rel','addend',0),('target','rel','target',hex(int(rel['target'],0)+4)),('address','binding','address',hex(int(rel['target'],0)+4)),('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb'),('kind','binding','kind','data')]:
            changed=copy.deepcopy(row);bindings=copy.deepcopy(row['nativeSymbolEntries']);item=next(r for r in changed['relocations']if r['offset']==rel['offset']);(item if owner=='rel'else bindings[rel['symbol']])[key]=value
            try:verify_original(changed,bindings)
            except (ValueError,KeyError)as error:out.append(dict(offset=rel['offset'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid ITCM provider boundary admitted:'+label)
    return dict(status='passed',cases=out,actualCalleeExecutions=0,calleeSourceCredit=0)
