import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261106_wcm_manager_next_cps_first_compiler import INPUT,INPUT_SHA,LANE
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

NATIVE=LANE/'native-inputs.json'
NATIVE_SHA='1e377b0cb91210fb9ad016b4e5e88017b0bb003a85e027351c0b30a559ef1104'


def inputs():
    if sha256(NATIVE)!=NATIVE_SHA or sha256(INPUT)!=INPUT_SHA:raise ValueError('Frozen native/import contract changed')
    value=read_json(NATIVE)
    for key in ['image','inventory','relocations']:
        path=value[key]
        if sha256(ROOT/path['path'])!=path['sha256']:raise ValueError('Original module/inventory/relocations changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),read_json(INPUT)


def validate(row,rel,binding,value,image,inventory,records,imports):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb'):raise ValueError('Original full caller namespace differs')
    caller=next((item for item in value['entries'] if item['address']==row['address']),None)
    if caller is None or (row['bytes'],row['targetSha256'])!=(caller['bytes'],caller['targetSha256']):raise ValueError('Full native extent/identity differs')
    address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or caller['canonicalInventoryRecord'] not in inventory.splitlines():raise ValueError('Full native caller/boundary changed')
    origin=address+rel['offset'];matches=[line for line in caller['originalRelocationRecords'] if line.startswith(f'from:0x{origin:08x} ')]
    if len(matches)!=1 or matches[0] not in records.splitlines():raise ValueError('Unique original relocation origin absent')
    record=matches[0];match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main',record)
    if match is None:raise ValueError('Original Thumb relocation kind/module differs')
    kind,target=match[1],int(match[2],0)
    pointer=kind=='load'and hex(target)in imports['functionPointerViews']
    subobject=False
    expected_address=target&~1 if pointer else target
    if (binding.get('program') or '',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','main',expected_address):raise ValueError('Original binding CPU/program/module/entry differs')
    if int(rel['target'],0)!=target:raise ValueError('Generated target differs from actual original import')
    word=image[origin-0x2000000:origin-0x2000000+4]
    if kind=='load'and pointer:
        view=imports['functionPointerViews'][hex(target)]
        if row['address']not in view['callers']or rel['symbol']!='native_fn_%08x'%expected_address or rel['type']!=2 or rel['addend']!=0 or struct.unpack('<I',word)[0]!=target or(binding['kind'],binding['mode'])!=('function','thumb'):raise ValueError('Original exact typed Thumb callback pointer differs')
        canonical=view['canonicalInventoryRecord']
        if view['entry']!=hex(expected_address)or view['mode']!='thumb'or not(target&1)or canonical not in inventory.splitlines()or re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%expected_address,canonical)is None:raise ValueError('Original callback exact instruction entry/extent/mode absent')
        result=dict(symbol=rel['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),canonicalInstructionEntry=hex(expected_address),mode='thumb',actualLowBitSet=True,canonicalInventoryRecord=canonical,argumentRole='Measured control callback pointer; opaque helper does not execute its original body',calleeSourceCredit=0)
    elif kind=='load':
        if rel['type']!=2 or rel['addend']!=(target-expected_address if subobject else 0)or struct.unpack('<I',word)[0]!=target or (binding['kind'],binding['mode'])!=('data','data'):raise ValueError('Original ABS32 word/addend/kind differs')
        view=imports['dataViews'].get(hex(expected_address))
        if subobject:
            offset=target-expected_address
            if offset not in [0,4,12]or offset==4 and imports['dataViews'].get(hex(target),{}).get('type')!='cpsif-queue8'or offset==12 and imports['dataViews'].get(hex(target),{}).get('type')!='cpsif-mutex24':raise ValueError('Unqualified CPSIF storage subobject offset')
        if view is None:raise ValueError('Original scoped Http data view absent')
        if view['storage']=='data':
            size={'local-packet-prefix8':8}.get(view['type'])
            if size is None or view['minimumBytes']!=size or image[target-0x2000000:target-0x2000000+size]!=bytes.fromhex(view['expectedHex']):raise ValueError('Original exact WCM readonly array differs')
            canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x%08x'%target,line)),None)
        else:
            sizes={'cps-consumed-global-prefix84':84,'local-packet-address6':6}
            if view['storage']!='bss'or view['minimumBytes']!=sizes.get(view['type'])or view['expectedHex']or target<0x2000000+len(image):raise ValueError('Scoped WCM BSS view differs')
            canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:bss addr:0x%08x'%expected_address,line)),None)
        if canonical is None:raise ValueError('Original exact WCM storage entry absent')
        result=dict(symbol=rel['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),canonicalInventoryRecord=canonical,typedView=view,sourceStorageBase=hex(expected_address),sourceObjectAddend=rel['addend'],originalEffectiveLiteral=hex(target),storageExtentAuthorshipCredit=0)
    else:
        mode='arm' if kind=='thumb_call_arm' else 'thumb'
        if rel['type']!=10 or rel['addend']!=-4 or (binding['kind'],binding['mode'])!=('function',mode):raise ValueError('Original THM_CALL/addend/mode differs')
        decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(word,origin))
        if len(decoded)!=1 or decoded[0].size!=4 or decoded[0].mnemonic!=('blx' if mode=='arm' else 'bl') or decoded[0].op_str!='#'+hex(target):raise ValueError('Actual original Thumb branch opcode/entry differs')
        canonical=next((line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,target),line)),None)
        if canonical is None:raise ValueError('Same-program original target mode/entry absent')
        result=dict(symbol=rel['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,nativeInstruction=word.hex(),actualMnemonic=decoded[0].mnemonic,canonicalInventoryRecord=canonical,calleeSourceCredit=0)
    verify_binding(rel['symbol'],binding)
    return result


def verify_original(row,bindings):
    value,image,inventory,records,imports=inputs()
    witnesses=[validate(row,rel,bindings[rel['symbol']],value,image,inventory,records,imports) for rel in row['relocations']]
    return dict(witnesses=witnesses,actualNativeThumbOpcodesAndEntriesChecked=True,oldNormalizerAndHelperParsersUnchanged=True,calleeSourceCredit=0,originalStorageAuthorshipCredit=0)


def negative_controls(rows):
    value,image,inventory,records,imports=inputs();rejected=[]
    for row in rows:
        for rel in row['relocations']:
            binding=row['nativeSymbolEntries'][rel['symbol']]
            cases=[('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb' if binding['mode']!='thumb' else 'arm'),('interior','binding','address',hex(int(binding['address'],0)+2)),('kind','binding','kind','data' if binding['kind']=='function' else 'function'),('origin','rel','offset',rel['offset']+2),('addend','rel','addend',rel['addend']+8),('type','rel','type',1),('caller-mode','row','mode','arm')]
            for label,owner,key,wrong in cases:
                objects={key:copy.deepcopy(item) for key,item in [('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong
                try:validate(objects['row'],objects['rel'],objects['binding'],value,image,inventory,records,imports)
                except (ValueError,KeyError) as error:rejected.append(dict(caller=row['address'],origin=rel['offset'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original binding accepted:'+label)
            if binding['kind']=='data'and imports['dataViews'][binding['address']]['storage']=='data':
                altered_data=bytearray(image);altered_data[int(binding['address'],0)-0x2000000]^=1
                try:validate(row,rel,binding,value,bytes(altered_data),inventory,records,imports)
                except ValueError as error:rejected.append(dict(caller=row['address'],origin=rel['offset'],case='altered-imported-string-byte',rejected=True,reason=str(error)))
                else:raise ValueError('Altered imported string bytes accepted')
            altered=bytearray(image);altered[int(row['address'],0)-0x2000000+rel['offset']]^=1
            try:validate(row,rel,binding,value,bytes(altered),inventory,records,imports)
            except ValueError as error:rejected.append(dict(caller=row['address'],origin=rel['offset'],case='altered-original-byte',rejected=True,reason=str(error)))
            else:raise ValueError('Altered original relocation bytes accepted')
    return dict(status='passed',cases=rejected,sourceCredit=0)
