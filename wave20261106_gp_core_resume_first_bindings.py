import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261106_gp_core_resume_first_compiler import INPUT,INPUT_SHA
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

NATIVE=ROOT/'evidence/lanes/parallel-wave20261106/gp-core-resume-next/first/native-inputs.json'
NATIVE_SHA='590916aa34dc26db876a8a5d44a19280e1a95e56f691eab8a019056971f27fb9'
VIEWS={34474128: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 63, 'storage': 'data', 'bytesHex': '4142434445464748494a4b4c4d4e4f505152535455565758595a6162636465666768696a6b6c6d6e6f707172737475767778797a3031323334353637383900'}, 34474192: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 10, 'storage': 'data', 'bytesHex': '67616d65737079677000'}, 34474204: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 40, 'storage': 'data', 'bytesHex': '546865726520776173206572726f72207374617274696e672074686520554450206c617965722e00'}, 34474244: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 43, 'storage': 'data', 'bytesHex': '54686572652077617320616e206572726f72207374617274696e672074686520554450204c617965722e00'}, 34474288: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 38, 'storage': 'data', 'bytesHex': '54686572652077617320616e206572726f72206372656174696e67206120736f636b65742e00'}, 34474328: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 49, 'storage': 'data', 'bytesHex': '54686572652077617320616e206572726f72206d616b696e67206120736f636b6574206e6f6e2d626c6f636b696e672e00'}, 34474064: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 25, 'storage': 'data', 'bytesHex': '6770636d2e67732e6e696e74656e646f776966692e6e657400'}, 34474380: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 49, 'storage': 'data', 'bytesHex': '436f756c64206e6f74207265736f6c766520636f6e6e656374696f6e206d616e616e67657220686f7374206e616d652e00'}, 34474432: {'type': 'original-GP-core-character-object', 'width': 1, 'minimumBytes': 40, 'storage': 'data', 'bytesHex': '54686572652077617320616e206572726f7220636f6e6e656374696e67206120736f636b65742e00'}}
CALLBACKS={34253221: 'profile-map callback,three original incoming words;bodyunexecuted', 34277233: 'UDP accepted callback;original fnpointer passed inR3,bodyunexecuted', 34277049: 'UDP left callback;original firststackword,bodyunexecuted', 34277265: 'UDP ping callback;original secondstackword,bodyunexecuted', 34277073: 'UDP message callback;original thirdstackword,bodyunexecuted'}


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
            raw=image[target-0x2000000:target-0x2000000+view['minimumBytes']] if storage=='data' else b''
            if view.get('bytesHex') is not None and raw.hex()!=view['bytesHex']:raise ValueError('Original minimum hexadecimal data bytes changed')
            if target in (0x20e0320,0x20e0324,0x20e032c) and raw!={0x20e0320:b'\0',0x20e0324:b'%s%d\0',0x20e032c:b'splitnum\0'}[target]:raise ValueError('Original protocol string bytes changed')
            if target==0x20dc534:
                for pointer,expected in zip(struct.unpack('<II',raw),[b'queryid\0',b'final\0']):
                    if image[pointer-0x2000000:pointer-0x2000000+len(expected)]!=expected:raise ValueError('Original invalid-key pointer pair/string differs')
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),dataRecord=canonical,typedView=view,minimumDataSha256=hashlib.sha256(raw).hexdigest() if raw else None,storageExtentAuthorshipCredit=0)

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
