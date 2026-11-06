import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261106_socl_continuation_next_seventh_compiler import COMPILER
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

NATIVE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/seventh/native-inputs.json'
NATIVE_SHA='3da31932c22a548fae398ea194f5ffe311b84969ff78805575683b027d009b0c'
VIEWS={0x021d1748:dict(type='four-session-field-access-view',width=4,minimumBytes=367,layoutBytes=368,recordBytes=92,records=4,storage='bss',initializedBytes=0)}
CALLBACKS={}


def bss_view(row,image,view):
    if (view['type'],view['width'],view['minimumBytes'],view['layoutBytes'],view['recordBytes'],view['records'],view['storage'],view['initializedBytes'])!=('four-session-field-access-view',4,367,368,92,4,'bss',0):raise ValueError('Exact measured session access/layout view differs')
    origins={'0x20909c8':(0x2090a28,0x2090a2a),'0x2090a3c':(0x2090aaa,0x2090aac),'0x2090ae8':(0x2090b1c,0x2090b1e)}
    if row['address'] not in origins:raise ValueError('BSS access qualifier escaped original caller set')
    evidence=[]
    for origin,mnemonic,immediate in [(origins[row['address']][0],'adds','#0x5c'),(origins[row['address']][1],'cmp','#4')]:
        decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(image[origin-0x02000000:origin-0x02000000+2],origin))
        if len(decoded)!=1 or decoded[0].mnemonic!=mnemonic or not decoded[0].op_str.endswith(', '+immediate):raise ValueError('Original loop record stride/count instruction differs')
        evidence.append(dict(origin=hex(origin),bytes=decoded[0].bytes.hex(),mnemonic=decoded[0].mnemonic,operands=decoded[0].op_str))
    return dict(loopEvidence=evidence,minimumAccessedSpanBytes=367,chosenArrayLayoutBytes=368,originalCompleteAllocationBytes=None,initializedBytes=0,storageSourceCredit=0,fields=dict(session=[0,32],master=[32,48],when=[80,4],ip=[84,4],port=[88,2],valid=[90,1]),lastPaddingByteAuthorshipCredit=0)


def inputs():
    if sha256(NATIVE)!=NATIVE_SHA:raise ValueError('Immutable Thumb native/import contract changed')
    value=read_json(NATIVE)
    for key in ['image','inventory','relocations']:
        p=value[key]
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Original Thumb image/inventory changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),dict(mapping={},compilerSha256=sha256(COMPILER))


def validate(row,relocation,binding,value,image,inventory,records,imports):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb'):raise ValueError('Exact Thumb caller namespace differs')
    caller=next((r for r in value['entries'] if r['address']==row['address']),None)
    if caller is None or (row['bytes'],row['targetSha256'])!=(caller['bytes'],caller['targetSha256']):raise ValueError('Full original Thumb extent/identity differs')
    address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or caller['canonicalInventoryRecord'] not in inventory.splitlines():raise ValueError('Full original Thumb caller body/boundary changed')
    origin=address+relocation['offset'];matches=[x for x in caller['originalRelocationRecords'] if x.startswith(f'from:0x{origin:08x} ')]
    if len(matches)!=1 or matches[0] not in records.splitlines():raise ValueError('Unique original Thumb relocation origin absent')
    record=matches[0];m=re.fullmatch(r'from:0x[0-9a-f]+ kind:(thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main',record)
    if m is None:raise ValueError('Original Thumb relocation kind/module differs')
    kind,target=m[1],int(m[2],0)
    if (binding.get('program') or '',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','main',target&~1 if target in CALLBACKS else target):raise ValueError('Original Thumb import CPU/program/module/entry differs')
    if int(relocation['target'],0)!=target:raise ValueError('Unchanged generated Thumb target differs')
    word=image[origin-0x2000000:origin-0x2000000+4]
    if kind=='load':
        if relocation['type']!=2 or relocation['addend']!=0 or struct.unpack('<I',word)[0]!=target:raise ValueError('Exact original Thumb load/addend/literal word differs')
        if target in CALLBACKS:
            if (binding['kind'],binding['mode'])!=('function','thumb') or not target&1:raise ValueError('Original callback Thumb tag/function kind differs')
            base=target&~1
            canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%base,x)),None)
            if canonical is None:raise ValueError('Original callback lacks genuine canonical Thumb entry')
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),canonicalInventoryRecord=canonical,canonicalEntry=hex(base),preservedOriginalThumbTag=1,typedCallback=CALLBACKS[target],calleeSourceCredit=0)
        else:
            if (binding['kind'],binding['mode'])!=('data','data') or target not in VIEWS:raise ValueError('Exact original data kind/view differs')
            view=VIEWS[target];storage=view['storage'];pattern=r'\S+ kind:bss addr:0x%08x'%target if storage=='bss' else r'\S+ kind:data(?:\(any\))? addr:0x%08x'%target
            canonical=next((x for x in inventory.splitlines() if re.fullmatch(pattern,x)),None)
            if canonical is None:raise ValueError('Original data/BSS inventory kind absent')
            if storage=='bss':
                if target!=0x021d1748:raise ValueError('Uninitialized view escaped exact canonical base')
                proof=bss_view(row,image,view);raw=b''
            else:
                raw=image[target-0x2000000:target-0x2000000+view['minimumBytes']]
                if len(raw)!=view['minimumBytes'] or hashlib.sha256(raw).hexdigest()!=view['sha256']:raise ValueError('Exact original initialized semantic prefix changed')
                proof=None
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),dataRecord=canonical,typedView=view,minimumDataSha256=hashlib.sha256(raw).hexdigest() if raw else None,bssAccessView=proof,storageExtentAuthorshipCredit=0)

    else:
        mode='arm' if kind=='thumb_call_arm' else 'thumb'
        if relocation['type']!=10 or relocation['addend']!=-4 or (binding['kind'],binding['mode'])!=('function',mode):raise ValueError('Original THM_CALL/addend/target mode differs')
        decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(word,origin))
        if len(decoded)!=1 or decoded[0].size!=4 or decoded[0].mnemonic!=('blx' if mode=='arm' else 'bl') or decoded[0].op_str!='#'+hex(target):raise ValueError('Actual original Thumb BL/BLX opcode/entry differs')
        canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,target),x)),None)
        if canonical is None:raise ValueError('Actual target lacks same-program canonical mode/entry')
        if relocation['symbol'].startswith('_'):
            expected=imports['mapping'].get(relocation['symbol'])
            if expected is None or any(binding.get(k,'')!=expected.get(k,'') for k in ['processor','module','mode','kind','address']) or '-thumb' not in row['compilerFlags'] or row['compilerSha256']!=imports['compilerSha256']:raise ValueError('Exact Thumb compiler-helper target/profile differs')
        result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,nativeInstruction=word.hex(),actualMnemonic=decoded[0].mnemonic,targetMode=mode,canonicalInventoryRecord=canonical,calleeSourceCredit=0)
    verify_binding(relocation['symbol'],binding)
    return result


def validate_caller(row,value,image,inventory,records):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb'):raise ValueError('Exact original caller namespace differs')
    caller=next((r for r in value['entries'] if r['address']==row['address']),None)
    if caller is None or (caller['bytes'],caller['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('Unadmitted original full caller identity')
    address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']]
    if len(native)!=row['bytes'] or hashlib.sha256(native).hexdigest()!=row['targetSha256'] or caller['canonicalInventoryRecord'] not in inventory.splitlines():raise ValueError('Full original body/hash/mode/inventory differs')
    actual=[x for x in records.splitlines() if (m:=re.match(r'from:(0x[0-9a-f]+)',x)) and address<=int(m[1],0)<address+row['bytes']]
    if actual!=caller['originalRelocationRecords']:raise ValueError('Complete actual original relocation set differs')
    return caller


def verify_original(row,bindings):
    value,image,inventory,records,imports=inputs();witnesses=[];caller=validate_caller(row,value,image,inventory,records)
    expected={int(re.match(r'from:(0x[0-9a-f]+)',r)[1],0)-int(row['address'],0) for r in caller['originalRelocationRecords']}
    if {r['offset'] for r in row['relocations']}!=expected or len(row['relocations'])!=len(expected):raise ValueError('Complete original relocation origin set differs')
    for relocation in row['relocations']:
        if relocation['symbol'] not in bindings:raise ValueError('Missing actual Thumb binding')
        witnesses.append(validate(row,relocation,bindings[relocation['symbol']],value,image,inventory,records,imports))
    return dict(witnesses=witnesses,actualNativeThumbOpcodesAndEntriesChecked=True,unchangedOldNormalizer=True,originalStorageExtentAuthorshipCredit=0,calleeSourceCredit=0)


def negative_controls(rows):
    value,image,inventory,records,imports=inputs();rejected=[]
    for row in rows:
        for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('address',hex(int(row['address'],0)+2)),('bytes',row['bytes']+2),('targetSha256','0'*64)]:
            bad=dict(row);bad[key]=wrong
            try:validate_caller(bad,value,image,inventory,records)
            except (ValueError,KeyError) as error:rejected.append(dict(caller=row['address'],case='caller-'+key,rejected=True,reason=str(error)))
            else:raise ValueError('Incorrect complete original caller identity admitted:'+key)
        changed=bytearray(image);changed[int(row['address'],0)-0x02000000]^=1;caller=next(r for r in value['entries'] if r['address']==row['address'])
        for label,raw,inv,recs in [('full-original-body',bytes(changed),inventory,records),('original-canonical-entry',image,inventory.replace(caller['canonicalInventoryRecord'],''),records),('extra-original-relocation',image,inventory,records+'\nfrom:'+row['address']+' kind:load to:0x02000000 module:main')]:
            try:validate_caller(row,value,raw,inv,recs)
            except ValueError as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Incorrect original caller physical evidence admitted:'+label)
        if row['relocations']:
            wrong=dict(row,relocations=row['relocations'][:-1])
            try:verify_original(wrong,row['nativeSymbolEntries'])
            except ValueError as error:rejected.append(dict(caller=row['address'],case='missing-original-relocation',rejected=True,reason=str(error)))
            else:raise ValueError('Incomplete original relocation set admitted')
        for rel in row['relocations']:
            binding=row['nativeSymbolEntries'][rel['symbol']]
            cases=[('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb' if binding['mode']!='thumb' else 'arm'),('entry-plus2','binding','address',hex(int(binding['address'],0)+2)),('kind','binding','kind','data' if binding['kind']=='function' else 'function'),('origin','rel','offset',rel['offset']+2),('addend-plus8','rel','addend',rel['addend']+8),('type','rel','type',1),('caller-mode','row','mode','arm')]
            for label,owner,key,wrong in cases:
                objs={k:copy.deepcopy(v) for k,v in [('row',row),('rel',rel),('binding',binding)]};objs[owner][key]=wrong
                try:validate(objs['row'],objs['rel'],objs['binding'],value,image,inventory,records,imports)
                except (ValueError,KeyError) as error:rejected.append(dict(caller=row['address'],origin=rel['offset'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Invalid scoped Thumb binding admitted:'+label)
            changed=bytearray(image);changed[int(row['address'],0)-0x2000000+rel['offset']]^=1
            for label,raw,inv,recs in [('original-instruction-or-literal',bytes(changed),inventory,records),('original-record',image,inventory,records.replace(next(x for x in records.splitlines() if x.startswith('from:0x'+format(int(row['address'],0)+rel['offset'],'08x')+' ')),''))]:
                try:validate(row,rel,binding,value,raw,inv,recs,imports)
                except ValueError as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Changed scoped native Thumb evidence admitted')
            if rel['type']==2 and VIEWS.get(int(rel['target'],0),{}).get('storage')!='bss':
                changed=bytearray(image);changed[int(rel['target'],0)-0x02000000]^=1
                try:validate(row,rel,binding,value,bytes(changed),inventory,records,imports)
                except ValueError as error:rejected.append(dict(caller=row['address'],case='initialized-prefix-mutation',rejected=True,reason=str(error)))
                else:raise ValueError('Changed original semantic initialized prefix admitted')
    return dict(status='passed',negativeCases=rejected,oldNormalizerAndHelperParsersUnchanged=True,sourceCredit=0)
