import copy
import os
import re
import struct
import subprocess
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,sha256
from link_runtime_unit import relocation_rows
from wave20261106_ov001_command_controller_source_first_paths import SOURCE,EVIDENCE,WORK,assert_compile
from wave20261106_ov001_command_controller_source_first_compiler import COMPILER
from wave20261106_ov001_command_controller_source_first_build import build
from wave20261106_ov001_command_controller_source_first_bindings import negative_controls as binding_controls

FIELDS={'021fe4ac':{'EntryView':['field0','field4','field5','field6'],'Field58View':['field58']},'021fe618':{'EntryView':['field0','field6'],'s32':[],'u8':[]},'0220aba0':{'EntryView':['field0','field6'],'LinkView':['field4'],'ResourceView':['field18'],'StateView':['field0','field4']},'0220ac9c':{'EntryView':['field0'],'LinkView':['field4'],'u16':[],'s16':[]},'0220afe4':{'Record10View':['field10'],'Half18View':['field18'],'Half4View':[],'u16':[]},'0220b3e4':{'SwitchView':['field0','field4','field10','field1c','field28','field30']}}


def compile_unit(source,obj,flags,strict=False):
    assert_compile(source,obj.parent);obj.parent.mkdir(parents=True,exist_ok=True);argv=[str(COMPILER),*flags,*(['-requireprotos','-w','error']if strict else[]),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')));return dict(command=argv,exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr)


def body(path,name):
    with path.open('rb')as stream:
        elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name);return elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]


def copy_source(tag,directory,changes=None):
    directory.mkdir(parents=True,exist_ok=True)
    for p in(SOURCE/tag).iterdir():
        if p.is_file():(directory/p.name).write_text((changes or{}).get(p.name,p.read_text()))


def geometry(tag,directory,flags,changes=None):
    copy_source(tag,directory,changes);labels=[];values=[]
    for typ,fields in FIELDS[tag].items():
        labels.append(typ+'.sizeof');values.append('sizeof('+typ+')')
        for field in fields:labels.extend([typ+'.'+field+'.offset',typ+'.'+field+'.bytes']);values.extend(['(u32)&(('+typ+'*)0)->'+field,'sizeof((('+typ+'*)0)->'+field+')'])
    source=directory/'g.c';obj=directory/'g.o';source.write_text('#include "main.c"\nu32 geometry[]={'+','.join(values)+'};\n');p=compile_unit(source,obj,flags)
    if p['exitCode']:raise ValueError(('Actual owned field geometry failed',p))
    actual=struct.unpack('<'+'I'*len(labels),body(obj,'geometry'));return dict(fields=dict(zip(labels,actual)),sourceSha256=sha256(source),objectSha256=sha256(obj))


def layouts(rows):
    flags=rows[0]['compilerFlags'];positive={tag:geometry(tag,WORK/'g'/tag,flags)for tag in FIELDS};negative=[]
    for tag,label,old,new in [('0220aba0','resource-flags-offset','unknown0[24]','unknown0[28]'),('021fe4ac','record-byte-width','s8 field6;','s16 field6;'),('0220aba0','state-counter-width','u32 field4; } StateView','u16 field4; } StateView'),('0220afe4','record-id-offset','unknown0[16]','unknown0[17]')]:
        headers={p.name:p.read_text()for p in(SOURCE/tag).glob('*.h')};count=sum(t.count(old)for t in headers.values())
        if count!=1:raise ValueError(('Exact typed geometry negative ambiguous',label,count))
        changed={name:text.replace(old,new)for name,text in headers.items()}
        try:
            bad=geometry(tag,WORK/'gn'/label,flags,changed)
            if bad['fields']==positive[tag]['fields']:raise RuntimeError('Wrong field geometry admitted')
        except ValueError:pass
        negative.append(dict(case=label,rejected=True))
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=negative,limits='Views are consumed prefixes,not complete unknown object/storage extents; EntryView8 and independently proven record stride12 remain separate.')


def prototypes(rows):
    positive=[];negative=[];used=set()
    for number,row in enumerate(rows):
        tag=format(int(row['address'],0),'08x');directory=WORK/'p'/tag;copy_source(tag,directory);obj=directory/'ok.o';p=compile_unit(directory/'main.c',obj,row['compilerFlags'],True)
        if p['exitCode']or body(obj,row['name'])!=body(ROOT/row['object'],row['name'])or relocation_rows(obj,row['name'])!=relocation_rows(ROOT/row['object'],row['name']):raise ValueError(('Actual strict C99/prototypes failed or changed full object',p))
        positive.append(dict(function=row['name'],objectSha256=sha256(obj),completeBodyAndRelocationsIdentical=True))
        names=[row['name']]+[n for n,b in row['nativeSymbolEntries'].items()if b['kind']=='function'and n not in used]
        for n,name in enumerate(names):
            target=directory/str(n);headers={p.name:p.read_text()for p in directory.glob('*.h')};count=0;changed={}
            for h,text in headers.items():changed[h],found=re.subn(r'^[ \t]*(?:extern[ \t]+)?[A-Za-z_][\w \t*]*[ \t*]+\b'+re.escape(name)+r'\s*\([^;{}]*\);[ \t]*$','',text,flags=re.M);count+=found
            if not count:raise ValueError(('Required prototype omitted nothing',name))
            copy_source(tag,target,changed);p=compile_unit(target/'main.c',target/'bad.o',row['compilerFlags'],True);text=(p['stdout']+p['stderr']).lower()
            lines=(target/'main.c').read_text().splitlines();locations=[int(n)for n in re.findall(r'main\.c:(\d+): function has no prototype',text)];identified=any(0<n<=len(lines)and re.search(r'\b'+re.escape(name)+r'\b',lines[n-1])for n in locations)
            if p['exitCode']==0 or not(name.lower()in text or identified)or not any(s in text for s in['no prototype','undefined identifier']):raise ValueError(('Actual missing prototype admitted',name,p))
            negative.append(dict(function=name,rejected=True,omittedActualDeclarations=count,diagnosticActualSourceLines=locations,diagnosticNamesExactOmittedUse=identified,attempt=p));used.add(name)
    return dict(status='passed',positive=positive,negativeControls=negative)


def actual_c99(rows):
    results=[]
    for row in rows:
        flags=row['compilerFlags']
        if flags.count('-lang')!=1 or flags[flags.index('-lang')+1]!='c99':raise ValueError('Actual production frontend is not C99')
        fresh,output=build(ROOT/row['source'],WORK/'c99'/format(int(row['address'],0),'08x'))
        if fresh['outputSha256']!=row['targetSha256']or relocation_rows(ROOT/fresh['object'],fresh['name'])!=relocation_rows(ROOT/row['object'],row['name']):raise ValueError('Fresh full C99/genuine source link differs')
        results.append(dict(function=fresh['name'],bytes=fresh['bytes'],sourceObjectSha256=fresh['objectSha256'],wholeNativeHash=fresh['outputSha256'],genuineEmbeddedLink=fresh['realLink']['normalEmbeddedLinkMatchesIndependentFlatOutput']))
    directory=WORK/'lang';directory.mkdir(parents=True,exist_ok=True);source=directory/'lang.c';source.write_text('int witness(void *p){int *q=p;return *q;}\n');attempts=[]
    for lang in['c99','c++']:
        flags=list(rows[0]['compilerFlags']);flags[flags.index('-lang')+1]=lang;p=compile_unit(source,directory/(lang.replace('+','p')+'.o'),flags)
        if(lang=='c99')!=(p['exitCode']==0):raise ValueError('Actual C99/C++ frontend witness differs')
        attempts.append(dict(language=lang,attempt=p))
    return dict(status='passed',functions=results,frontendWitness=attempts)


def primitive_abi(rows):
    flags=rows[0]['compilerFlags'];directory=WORK/'abi';directory.mkdir(parents=True,exist_ok=True);tag='0220afe4';copy_source(tag,directory);probes=[('signed16','return(s16)value;','return(u16)value;',lambda v:((v&65535)-65536 if v&32768 else v&65535)&0xffffffff),('signed8','return(s8)value;','return(u8)value;',lambda v:((v&255)-256 if v&128 else v&255)&0xffffffff),('unsigned8','return(u8)value;','return(u16)value;',lambda v:v&255),('nibble','Half4View view;*(u16*)((u8*)&view+4)=(u16)value;return(u8)view.field4high;','Half4View view;*(u16*)((u8*)&view+4)=(u16)value;return(u8)view.field4low;',lambda v:v>>4&15)];positive=[];negative=[]
    for label,good,bad,expected in probes:
        for state,text in[('good',good),('wrong',bad)]:
            source=directory/(label+'-'+state+'.c');obj=directory/(label+'-'+state+'.o');source.write_text('#include "context.h"\nu32 abi(u32 value){'+text+'}\n');p=compile_unit(source,obj,flags)
            if p['exitCode']:raise ValueError(('Actual field ABI witness failed',p))
            code=body(obj,'abi');failed=[];returns=0
            for value in[0,1,127,128,255,32767,32768,65535,0x1234abcd,0xffffffff]:
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,code);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,value);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=128);actual=vm.reg_read(R.UC_ARM_REG_R0)
                if actual!=expected(value)or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x0200f000:failed.append(dict(input=value,expected=expected(value),actual=actual))
                returns+=1
            if state=='good':
                if failed:raise ValueError(('Actual field signedness/nibble ABI differs',label,failed))
                positive.append(dict(case=label,actualFreshReturns=returns,sourceSha256=sha256(source),objectSha256=sha256(obj)))
            else:
                if not failed:raise ValueError('Wrong typed field ABI admitted')
                negative.append(dict(case=label,rejected=True,mismatches=failed,sourceSha256=sha256(source),objectSha256=sha256(obj)))
    return dict(status='passed',sourceCredit=0,actualFreshReturns=sum(r['actualFreshReturns']for r in positive),positive=positive,negativeControls=negative)


def getter_abi(rows):
    value=read_json(EVIDENCE/'native-inputs.json');image=(ROOT/value['mainImage']['path']).read_bytes();native=image[0x49ad0:0x49ad0+20]
    if C.sha(native)!='4eea96428387267cd9c5afc97e0ff55526494794c4a828ccda819b5a1b8ff257':raise ValueError('Original accepted12-byte indexed-record getter changed')
    directory=WORK/'getter';directory.mkdir(parents=True,exist_ok=True);source=directory/'abi.c';obj=directory/'abi.o';source.write_text('typedef unsigned int u32;\nu32 abi(u32 index){return0x02102a18+index*12;}\n'.replace('return0x','return 0x'));attempt=compile_unit(source,obj,rows[0]['compilerFlags'])
    if attempt['exitCode']:raise ValueError(('Actual fresh getter ABI witness failed',attempt))
    fresh=body(obj,'abi');records=[]
    for label,code in[('original-accepted20',native),('fresh-ordinary-C',fresh)]:
        for index in[0,1,5,0xffffffff,0x80000000,0x7fffffff]:
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02049ad0,code);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,index);vm.reg_write(R.UC_ARM_REG_SP,0x027fc000);vm.reg_write(R.UC_ARM_REG_LR,0x02010000);vm.emu_start(0x02049ad0,0x02010000,count=64);expected=(0x02102a18+index*12)&0xffffffff
            if vm.reg_read(R.UC_ARM_REG_R0)!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02010000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x027fc000:raise ValueError('Actual getter stride/address/ARM return ABI differs')
            records.append(dict(kind=label,index=index,returned=expected))
    return dict(status='passed',sourceCredit=0,helperSourceCredit=0,storageCredit=0,actualOriginalGetterReturns=6,actualFreshGetterReturns=6,nativeBodySha256=C.sha(native),freshSourceSha256=sha256(source),freshObjectSha256=sha256(obj),records=records,limits='Separate bounded actual accepted getter entry executions only; all caller fixtures still intercept imported helpers and execute0 native callee bodies.')


def switch(image,base,at):
    compare,dispatch,default=struct.unpack_from('<III',image,at-base-4);assert compare&0xfff0f000==0xe3500000 and dispatch&0xfffffff0==0x908ff100 and default==0xe12fff1e;register=dispatch&15;assert register<15 and(compare>>16)&15==register and(compare&4095)==3;words=[struct.unpack_from('<I',image,at-base+8+4*i)[0]for i in range(4)];assert all(w>>24==0xea for w in words)


def boundaries():
    value=read_json(EVIDENCE/'native-inputs.json');image=(ROOT/value['image']['path']).read_bytes();base=int(value['base'],0);selected={int(p.parent.name,16)for p in SOURCE.glob('*/main.c')};positive=[];negative=[]
    def check(e):
        if(e['program'],e['processor'],e['module'],e['mode'])!=('','arm9','ov001','arm'):raise ValueError('Admitted complete source scope differs')
        a=int(e['address'],0);n=e['bytes'];flow=e['cfg'];code=set();data=set();loads=set()
        if C.sha(image[a-base:a-base+n])!=e['targetSha256']:raise ValueError('Original complete admitted body hash differs')
        for i in flow['instructions']:
            pc=int(i['address'],0)
            if pc&3 or not a<=pc<=a+n-4 or image[pc-base:pc-base+4].hex()!=i['bytes']:raise ValueError('Actual admitted instruction word/address differs')
            code.update(range(pc,pc+4));word=struct.unpack_from('<I',image,pc-base)[0]
            if(word&0x0f7f0000)==0x051f0000:loads.add(pc+8+((word&4095)if word&(1<<23)else-(word&4095)))
        for item in flow['literals']:
            pc=int(item['address'],0)
            if not a<=pc<=a+n-4 or image[pc-base:pc-base+4].hex()!=item['bytes']:raise ValueError('Actual admitted literal word/address differs')
            data.update(range(pc,pc+4))
        if code&data or code|data!=set(range(a,a+n))or loads!={int(i['address'],0)for i in flow['literals']}:raise ValueError('Complete admitted instruction/literal storage or origins differ')
        for item in flow['switches']:switch(image,base,int(item['dispatch'],0))
        return dict(address=e['address'],instructionBytes=len(code),literalBytes=len(data))
    for original in[value for value in value['entries']if int(value['address'],0)in selected]:
        positive.append(check(original))
        for label in['mode','hash','instruction','missing-literal','envelope']:
            if label=='missing-literal'and not original['cfg']['literals']:continue
            e=copy.deepcopy(original)
            if label=='mode':e['mode']='thumb'
            elif label=='hash':e['targetSha256']='0'*64
            elif label=='instruction':e['cfg']['instructions'][0]['bytes']='00000000'
            elif label=='missing-literal':e['cfg']['literals'].pop()
            else:e['bytes']+=4
            try:check(e)
            except(ValueError,AssertionError)as error:negative.append(dict(address=original['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError(('Wrong admitted physical inventory passed',label))
    at=0x0220b3e8-base
    for label,pos,mask in[('conditional-cmp',at-4,0x10000000),('missing-cmp-flags',at-4,1<<20),('other-index',at,1),('wrong-shift',at,1<<7),('wrong-condition',at,0x10000000),('wrong-default',at+4,1<<24),('case-call',at+8,1<<24),('upper',at-4,None)]:
        changed=bytearray(image);word=struct.unpack_from('<I',changed,pos)[0];struct.pack_into('<I',changed,pos,word^mask if mask is not None else(word&~4095)|4)
        try:switch(changed,base,base+at)
        except AssertionError:negative.append(dict(case=label,rejected=True))
        else:raise ValueError(('Malformed original4-case switch passed',label))
    return dict(status='passed',sourceCredit=0,admittedInstructionLiteralInventoriesRechecked=positive,negativeControls=negative,limits='Runtime rechecks immutable admitted instruction/literal words and exact whole storage; independent entry-reachable analysis was performed at source admission.')


def execute(rows):return dict(status='passed',sourceCredit=0,layout=layouts(rows),acceptedGetterABI=getter_abi(rows),primitiveABI=primitive_abi(rows),requiredPrototypes=prototypes(rows),originalBindings=binding_controls(rows),boundaries=boundaries(),actualC99=actual_c99(rows))
