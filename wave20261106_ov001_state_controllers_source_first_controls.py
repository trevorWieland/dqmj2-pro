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
from wave20261106_ov001_state_controllers_source_first_paths import SOURCE,EVIDENCE,WORK,assert_compile
from wave20261106_ov001_state_controllers_source_first_compiler import COMPILER
from wave20261106_ov001_state_controllers_source_first_build import build
from wave20261106_ov001_state_controllers_source_first_bindings import negative_controls as binding_controls

EXPECTED={
 '021ddd80':{'StateView':(28,{'state2':(2,1),'field7':(7,1),'field8':(8,1),'counterD':(13,1),'field1b':(27,1)})},
 '021df808':{'StateView':(76,{'field8':(8,1),'counter2d':(45,1),'state2e':(46,1),'actor48':(72,4)}),'ActorPrefix':(799,{'field31e':(798,1)})},
 '021edd10':{'StateView':(100,{'counter11':(17,1),'field13':(19,1),'state23':(35,1),'field36':(54,2),'actor60':(96,4)})},
 '021f8c50':{'StateView':(136,{'field1b':(27,1),'counter1d':(29,1),'state1e':(30,1),'actor84':(132,4)}),'ActorPrefix':(799,{'field31e':(798,1)})},
 '022146d4':{'StateView':(20,{'field2':(2,1),'counter8':(8,1),'state9':(9,1),'actor10':(16,4)}),'ActorPrefix':(799,{'field31e':(798,1)})},
 '02214e68':{'StateView':(12,{'state0':(0,1),'field1':(1,1),'counter2':(2,1),'field3':(3,1),'actor8':(8,4)})},
 '02216460':{'StateView':(12,{'counter0':(0,1),'state1':(1,1),'field8':(8,4)})},
 '0221671c':{'StateView':(12,{'field1':(1,1),'state2':(2,1),'counter3':(3,1),'field4':(4,2),'actor8':(8,4)})},
}
FIELDS={tag:{**{typ:list(fields)for typ,(size,fields)in types.items()},'u8':[],'s8':[],'u16':[],'s32':[]}for tag,types in EXPECTED.items()}
for tag in ['021ddd80','021edd10','02214e68','02216460','0221671c']:
 EXPECTED[tag]['ActorView']=(808,{'child1e8':(488,4),'field31e':(798,1),'field31f':(799,1),'field325':(805,1)})
 FIELDS[tag]['ActorView']=list(EXPECTED[tag]['ActorView'][1])



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
 for tag,result in positive.items():
  expected={'u8.sizeof':1,'s8.sizeof':1,'u16.sizeof':2,'s32.sizeof':4}
  for typ,(size,fields)in EXPECTED[tag].items():
   expected[typ+'.sizeof']=size
   for name,(offset,width)in fields.items():expected[typ+'.'+name+'.offset']=offset;expected[typ+'.'+name+'.bytes']=width
  if result['fields']!=expected:raise ValueError(('Actual complete state geometry differs',tag,result['fields'],expected))
 for tag,label,old,new in [('021df808','counter-offset','unknown9[0x2d-9]','unknown9[0x2e - 9]'),('021f8c50','state-width','u8 state1e;','u32 state1e;'),('022146d4','actor-offset','unknownA[6]','unknownA[10]'),('021edd10','halfword-width','u16 field36;','u32 field36;')]:
  headers={p.name:p.read_text()for p in(SOURCE/tag).glob('*.h')}
  if sum(text.count(old)for text in headers.values())!=1:raise ValueError(('Exact state geometry mutation absent',tag,label))
  bad=geometry(tag,WORK/'gn-v2'/label,flags,{name:text.replace(old,new)for name,text in headers.items()})
  if bad['fields']==positive[tag]['fields']:raise ValueError('Wrong state geometry admitted')
  negative.append(dict(case=label,rejected=True))
 return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=negative,limits='Measured consumed state/actor prefixes only; no complete game-object layout/storage/semantic-role credit.')


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
    flags=rows[0]['compilerFlags'];directory=WORK/'abi';copy_source('021df808',directory);results=[];negative=[]
    for label,good,bad,expected in [('signed8','return(s8)value;','return(u8)value;',lambda v:((v&255)-256 if v&128 else v&255)&0xffffffff),('unsigned8','return(u8)value;','return value;',lambda v:v&255)]:
        for state,text in [('good',good),('wrong',bad)]:
            source=directory/(label+'-'+state+'.c');obj=directory/(label+'-'+state+'.o');source.write_text('#include "context.h"\nu32 abi(u32 value){'+text+'}\n');attempt=compile_unit(source,obj,flags)
            if attempt['exitCode']:raise ValueError(('Actual typed ABI frontend failed',attempt))
            code=body(obj,'abi');mismatches=[]
            for value in [0,1,127,128,255,32767,32768,65535,0x1234abcd,0xffffffff]:
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,code);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,value);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=128)
                if vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x0200f000:raise ValueError('Typed ABI did not return normally')
                if vm.reg_read(R.UC_ARM_REG_R0)!=expected(value):mismatches.append(value)
            if state=='good':
                if mismatches:raise ValueError('Actual typed ABI differs')
                results.append(dict(case=label,actualFreshReturns=10,sourceSha256=sha256(source),objectSha256=sha256(obj)))
            else:
                if not mismatches:raise ValueError('Wrong typed ABI retained all boundary values')
                negative.append(dict(case=label,rejected=True,mismatches=mismatches))
    return dict(status='passed',sourceCredit=0,actualFreshReturns=20,positive=results,negativeControls=negative)




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
        for item in flow.get('switches',[]):switch(image,base,int(item['dispatch'],0))
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
    return dict(status='passed',sourceCredit=0,admittedInstructionLiteralInventoriesRechecked=positive,negativeControls=negative,limits='Runtime rechecks immutable admitted instruction/literal words and exact whole storage; independent entry-reachable analysis was performed at source admission.')


def execute(rows):
 from wave20261106_ov001_state_controllers_source_first_chain_abi import execute as chain
 return dict(status='passed',sourceCredit=0,layout=layouts(rows),mappingSinkABI=chain(),primitiveABI=primitive_abi(rows),requiredPrototypes=prototypes(rows),originalBindings=binding_controls(rows),boundaries=boundaries(),actualC99=actual_c99(rows))
