import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261105_gamespy_thumb_next_sorting_compiler import INPUT,INPUT_SHA
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

NATIVE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/sorting/native-inputs.json'
NATIVE_SHA='60475dc0eb837d88bd3519af6c4626145629bffe58fc7fef1c61888bbeb95bca'
VIEWS={0x21d236c:dict(type='sort-global-aggregate-pointer-slot',width=4,fieldOffset=4,minimumBytes=8,storage='bss'),0x20e0350:dict(type='empty-string',width=1,minimumBytes=1,storage='data')}
CALLBACKS={a:dict(type='compare-two-pointers-return-int',incomingRegisters=['r0','r1']) for a in [0x20a6b11,0x20a6b5d,0x20a6c11,0x20a6c69]}


def qualify_sort_slot(row,origin,image,view):
    from capstone.arm import ARM_OP_REG,ARM_OP_MEM,ARM_REG_PC
    if (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb'):raise ValueError('Sort slot caller namespace differs')
    a=int(row['address'],0);raw=image[a-0x2000000:a-0x2000000+row['bytes']]
    if hashlib.sha256(raw).hexdigest()!=row['targetSha256'] or struct.unpack_from('<I',image,origin-0x2000000)[0]!=0x21d236c:raise ValueError('Original sort slot body/literal differs')
    if view['width']!=4 or view['storage']!='bss' or view['minimumBytes']<view['fieldOffset']+view['width']:raise ValueError('Typed sort slot width/storage/minimum view differs')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);decoder.detail=True;instructions=list(decoder.disasm(raw,a));witness=[]
    for i,ins in enumerate(instructions):
        op=ins.operands
        if ins.mnemonic!='ldr' or len(op)!=2 or op[0].type!=ARM_OP_REG or op[1].type!=ARM_OP_MEM or op[1].mem.base!=ARM_REG_PC or ((ins.address+4)&~3)+op[1].mem.disp!=origin:continue
        register=op[0].reg
        for consumer in instructions[i+1:i+4]:
            args=consumer.operands
            if consumer.mnemonic in ('ldr','str') and len(args)==2 and args[1].type==ARM_OP_MEM and args[1].mem.base==register and not args[1].mem.index and args[1].mem.disp==view['fieldOffset'] and not consumer.writeback:
                witness.append(dict(originalLiteralLoad=hex(ins.address),literalLoadBytes=ins.bytes.hex(),slotConsumer=hex(consumer.address),consumerBytes=consumer.bytes.hex(),consumerKind=consumer.mnemonic,fieldOffset=view['fieldOffset'],width=4));break
            if register in consumer.regs_access()[1]:break
    if not witness:raise ValueError('No measured bounded load/store consumes the typed sort slot offset')
    return dict(originalLiteral=hex(origin),aggregateBase='0x21d236c',typedFieldOffset=view['fieldOffset'],typedWidth=4,minimumBytes=view['minimumBytes'],nativeDataFlow=witness,externalStorageAuthorshipCredit=0)


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
            if target in (0x20e0320,0x20e0324,0x20e032c) and raw!={0x20e0320:b'\0',0x20e0324:b'%s%d\0',0x20e032c:b'splitnum\0'}[target]:raise ValueError('Original protocol string bytes changed')
            if target==0x20e0350 and raw!=b'\0':raise ValueError('Original empty comparison string changed')
            if target==0x20dc534:
                for pointer,expected in zip(struct.unpack('<II',raw),[b'queryid\0',b'final\0']):
                    if image[pointer-0x2000000:pointer-0x2000000+len(expected)]!=expected:raise ValueError('Original invalid-key pointer pair/string differs')
            result=dict(symbol=relocation['symbol'],origin=hex(origin),target=hex(target),originalRecord=record,originalLiteralWord=word.hex(),dataRecord=canonical,typedView=view,minimumDataSha256=hashlib.sha256(raw).hexdigest() if raw else None,storageExtentAuthorshipCredit=0)
            if target==0x21d236c:result['sortSlotNativeDataFlow']=qualify_sort_slot(row,origin,image,view)

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


def slot_negative_controls(rows):
    value,image,inventory,records,imports=inputs();rejected=[]
    for row in rows:
        for rel in row['relocations']:
            if int(rel['target'],0)!=0x21d236c:continue
            origin=int(row['address'],0)+rel['offset'];view=VIEWS[0x21d236c]
            for label,wrong in [('field-offset0',dict(view,fieldOffset=0)),('width2',dict(view,width=2)),('minimum4',dict(view,minimumBytes=4)),('initialized-kind',dict(view,storage='data'))]:
                try:qualify_sort_slot(row,origin,image,wrong)
                except ValueError as error:rejected.append(dict(address=row['address'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong typed sort slot admitted')
            try:qualify_sort_slot(row,origin+4,image,view)
            except ValueError as error:rejected.append(dict(address=row['address'],case='literal-origin-plus4',rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original sort slot origin admitted')
    return dict(status='passed',cases=rejected,sourceCredit=0)
