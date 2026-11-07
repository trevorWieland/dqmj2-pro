import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261106_dwc_match_control_first_compiler import INPUT,INPUT_SHA
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

NATIVE=ROOT/'evidence/lanes/parallel-wave20261106/dwc-match-control-next/first/native-inputs.json'
NATIVE_SHA='3d77aa13a5ac7f676cb65cab9361c4c1aed156fea97e7dd2ab63d28b9582055e'
VIEWS={35462024: {'storage': 'bss', 'minimumBytes': 12, 'width': 4, 'meaning': 'Actual shared globals option pointer+0 and addFilter pointer+8; opaque word+4; no storage authorship'}, 34472344: {'storage': 'data', 'minimumBytes': 8, 'width': 1, 'bytesHex': '20616e6420282900', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472352: {'storage': 'data', 'minimumBytes': 1, 'width': 1, 'bytesHex': '00', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472356: {'storage': 'data', 'minimumBytes': 3, 'width': 1, 'bytesHex': '257500', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472360: {'storage': 'data', 'minimumBytes': 4, 'width': 1, 'bytesHex': '464d4500', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472364: {'storage': 'data', 'minimumBytes': 2, 'width': 1, 'bytesHex': '5900', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472368: {'storage': 'data', 'minimumBytes': 2, 'width': 1, 'bytesHex': '4e00', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472372: {'storage': 'data', 'minimumBytes': 4, 'width': 1, 'bytesHex': '4d444600', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472376: {'storage': 'data', 'minimumBytes': 4, 'width': 1, 'bytesHex': '56455200', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472380: {'storage': 'data', 'minimumBytes': 11, 'width': 1, 'bytesHex': '496e697420737461746500', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472392: {'storage': 'data', 'minimumBytes': 12, 'width': 1, 'bytesHex': '5365727665722066756c6c00', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}, 34472404: {'storage': 'data', 'minimumBytes': 24, 'width': 1, 'bytesHex': '556e6b6e6f776e20636f6e6e65637420617474656d707400', 'meaning': 'Complete original configured NUL character literal consumed by unchanged caller; no storage authorship'}}
CALLBACKS={34224045: 'DWCi_QR2ServerKeyCallback', 34224269: 'DWCi_QR2PlayerKeyCallback', 34224273: 'DWCi_QR2TeamKeyCallback', 34224277: 'DWCi_QR2KeyListCallback', 34224381: 'DWCi_QR2CountCallback', 34224385: 'DWCi_QR2AddErrorCallback', 34224393: 'DWCi_QR2PublicAddrCallback', 34224413: 'DWCi_QR2NatnegCallback', 34224565: 'DWCi_QR2ClientMsgCallback', 34222649: 'DWCi_SBCallback'}


def inputs():
    if sha256(NATIVE)!=NATIVE_SHA or sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable Thumb native/import contract changed')
    value=read_json(NATIVE)
    for key in ['image','inventory','relocations']:
        p=value[key]
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Original Thumb image/inventory changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),read_json(INPUT)


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
    table=(address==0x020a37ac and relocation['symbol']=='stGameMatchKeys' and kind=='load')
    if table and not(int(binding['address'],0)==0x021d1ba8 and relocation['offset'] in[212,216,220]and relocation['addend']=={212:0,216:1,220:8}[relocation['offset']]and target==0x021d1ba8+relocation['addend']):raise ValueError('Exact three typed key-record fields/addends differ')
    expected_base=0x021d1ba8 if table else(target&~1 if target in CALLBACKS else target)
    if (binding.get('program') or '',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','main',expected_base):raise ValueError('Original Thumb import CPU/program/module/entry differs')
    if int(relocation['target'],0)!=(expected_base if table else target):raise ValueError('Unchanged generated Thumb target differs')
    word=image[origin-0x2000000:origin-0x2000000+4]
    if kind=='load':
        if relocation['type']!=2 or(not table and relocation['addend']!=0)or struct.unpack('<I',word)[0]!=target:raise ValueError('Exact original Thumb load/addend/literal word differs')
        if target in CALLBACKS:
            if (binding['kind'],binding['mode'])!=('function','thumb') or not target&1:raise ValueError('Original callback Thumb tag/function kind differs')
            base=target&~1
            canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%base,x)),None)
            if canonical is None:raise ValueError('Original callback lacks genuine canonical Thumb entry')
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),canonicalInventoryRecord=canonical,canonicalEntry=hex(base),preservedOriginalThumbTag=1,typedCallback=CALLBACKS[target],calleeSourceCredit=0)
        else:
            if (binding['kind'],binding['mode'])!=('data','data') or expected_base not in VIEWS:raise ValueError('Exact original data kind/view differs')
            view=VIEWS[expected_base];storage=view['storage'];pattern=r'\S+ kind:bss addr:0x%08x'%expected_base if storage=='bss' else r'\S+ kind:data(?:\(any\))? addr:0x%08x'%target
            canonical=next((x for x in inventory.splitlines() if re.fullmatch(pattern,x)),None)
            if canonical is None:raise ValueError('Original data/BSS inventory kind absent')
            raw=image[target-0x2000000:target-0x2000000+view['minimumBytes']] if storage=='data' else b''
            if view.get('bytesHex') is not None and raw.hex()!=view['bytesHex']:raise ValueError('Original minimum hexadecimal data bytes changed')
            if target in (0x20e0320,0x20e0324,0x20e032c) and raw!={0x20e0320:b'\0',0x20e0324:b'%s%d\0',0x20e032c:b'splitnum\0'}[target]:raise ValueError('Original protocol string bytes changed')
            if target==0x20dc534:
                for pointer,expected in zip(struct.unpack('<II',raw),[b'queryid\0',b'final\0']):
                    if image[pointer-0x2000000:pointer-0x2000000+len(expected)]!=expected:raise ValueError('Original invalid-key pointer pair/string differs')
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),dataRecord=canonical,typedView=view,originalSymbolBase=hex(expected_base),originalFieldAddend=relocation['addend'],typedRecordField={0:'keyID/u8',1:'isStr/u8',8:'value/const-void-pointer'}.get(relocation['addend'])if table else None,minimumDataSha256=hashlib.sha256(raw).hexdigest() if raw else None,storageExtentAuthorshipCredit=0)

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


def verify_original(row,bindings):
    value,image,inventory,records,imports=inputs();witnesses=[]
    for relocation in row['relocations']:
        if relocation['symbol'] not in bindings:raise ValueError('Missing actual Thumb binding')
        witnesses.append(validate(row,relocation,bindings[relocation['symbol']],value,image,inventory,records,imports))
    return dict(witnesses=witnesses,actualNativeThumbOpcodesAndEntriesChecked=True,unchangedOldNormalizer=True,originalStorageExtentAuthorshipCredit=0,calleeSourceCredit=0)


def negative_controls(rows):
    value,image,inventory,records,imports=inputs();rejected=[]
    for row in rows:
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
    return dict(status='passed',negativeCases=rejected,oldNormalizerAndHelperParsersUnchanged=True,sourceCredit=0)
