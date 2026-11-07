import hashlib,os,re,subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
from link_runtime_unit import LINKER,LINKER_HASH,binding_object,verify_binding,relocation_rows
from elf_units import split_symbol
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_SHA='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
FLAGS=['-O2','-enum','int','-char','signed','-str','noreuse','-proc','arm946e','-gccext,on','-fp','soft','-inline','off','-Cpp_exceptions','off','-RTTI','off','-interworking','-w','off','-sym','on','-gccinc','-nolink','-msgstyle','gcc','-O4,p','-ipa','file','-inline','on,noauto','-lang','c99']
SOURCE=ROOT/'src/runtime/parallel_wave20261106/mb-local-context-next/register'
WORK=ROOT/'work/w6mc/register'
ADDRESS=0x2015c70
SIZE=656
UPDATE=0x20e68a4
NAME='MB_RegisterFile'

def env():return dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))

def compile_source(source,directory,strict=True):
 source=Path(source).resolve();directory=Path(directory).resolve()
 if not(source.is_relative_to(SOURCE)or source.is_relative_to(WORK))or not directory.is_relative_to(WORK):raise ValueError('Register compile escaped owned paths')
 if sha256(COMPILER)!=COMPILER_SHA:raise ValueError('Register compiler pin changed')
 directory.mkdir(parents=True,exist_ok=True);obj=directory/'unit.o';flags=[*FLAGS,*(['-requireprotos','-w','error']if strict else[])];command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];run=subprocess.run(command,cwd=ROOT,env=env(),capture_output=True,text=True,timeout=60)
 if run.returncode:raise ValueError(('Register compilation failed',run.stdout,run.stderr))
 return obj,dict(command=command,flags=flags,compilerSha256=COMPILER_SHA,stdout=run.stdout,stderr=run.stderr)

def inspect_object(obj):
 with Path(obj).open('rb')as stream:
  e=ELFFile(stream);sy=e.get_section_by_name('.symtab');s=next(s for s in sy.iter_symbols()if s.name==NAME);text=e.get_section(s['st_shndx']);bss=e.get_section_by_name('.bss');locals=[s for s in sy.iter_symbols()if s['st_info']['type']=='STT_OBJECT'and s['st_shndx']==e.get_section_index('.bss')];functions=[s for s in sy.iter_symbols()if s['st_info']['type']=='STT_FUNC'and s['st_size']]
  if len(functions)!=1 or functions[0].name!=NAME or text['sh_type']!='SHT_PROGBITS':raise ValueError('Register source emitted unexpected executable sections')
  if bss['sh_type']!='SHT_NOBITS'or bss['sh_size']!=1 or bss['sh_addralign']!=1 or len(locals)!=1:raise ValueError('Register source local byte section changed')
  local=locals[0]
  if local['st_info']['bind']!='STB_LOCAL'or local['st_value']!=0 or local['st_size']!=1 or not re.fullmatch(r'update\$\d+',local.name):raise ValueError('Register genuine function-local update definition changed')
  if any(sec['sh_flags']&2 and sec['sh_type']=='SHT_PROGBITS'and sec['sh_size']and sec['sh_flags']&4==0 for sec in e.iter_sections()):raise ValueError('Register has unexpected initialized source data')
  return dict(body=text.data()[s['st_value']:s['st_value']+s['st_size']],bytes=s['st_size'],symbol=dict(s.entry),flags=e['e_flags'],sourceLocal=dict(name=local.name,value=local['st_value'],bytes=local['st_size'],binding=local['st_info']['bind'],type=local['st_info']['type'],sectionIndex=local['st_shndx']),bssSection=dict(bss.header),relocations=relocation_rows(obj,NAME))

def bindings(record):
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+SIZE];out={}
 for r in record['relocations']:
  offset=r['offset'];word=int.from_bytes(native[offset:offset+4],'little')
  if r['type']==1:
   if word>>24!=0xeb or r['explicitAddend']!=-8:raise ValueError('Register native branch witness changed')
   imm=word&0xffffff;imm=imm-(1<<24)if imm&(1<<23)else imm;address=ADDRESS+offset+8+(imm<<2);binding=dict(program='',processor='arm9',module='main',mode='arm',kind='function',address=hex(address));verify_binding(r['symbol'],binding)
   row=dict(name=r['symbol'],**binding,nativeCallsite=hex(ADDRESS+offset),nativeCallWord=hex(word),sourceRelocation=r)
   if r['symbol']in out and out[r['symbol']]['address']!=row['address']:raise ValueError('Register repeated callee identity differs')
   out.setdefault(r['symbol'],row)
  elif r['type']==2 and r['symbol']=='.bss':
   if offset!=652 or word!=UPDATE or r['explicitAddend']!=0:raise ValueError('Register native local-byte literal changed')
  elif r['type']==2 and r['symbol']=='mbc':
   if offset!=644:raise ValueError('Register core-slot literal moved')
   out['mbc']=dict(name='mbc',program='',processor='arm9',module='main',mode='data',kind='data',address=hex(word),nativeCallsite=hex(ADDRESS+offset),sourceRelocation=r)
  else:raise ValueError('Register has an unqualified relocation')
 return out,native

def link(obj,directory,bss_address=UPDATE):
 directory=Path(directory).resolve()
 if not directory.is_relative_to(WORK):raise ValueError('Register linker escaped owned work')
 if sha256(LINKER)!=LINKER_HASH:raise ValueError('Register linker pin changed')
 directory.mkdir(parents=True,exist_ok=True);record=inspect_object(obj);qualified,native=bindings(record);before=sha256(obj);objects=[obj];mem=[f'CALL: ORIGIN = {ADDRESS:#x} > caller.bin',f'PRIVATE: ORIGIN = {bss_address:#x}'];sections=[f'.caller: {{ {obj.name}(.text) }} > CALL',f'.private: {{ {obj.name}(.bss) }} > PRIVATE'];assign=[];probes=[]
 for i,(name,row)in enumerate(qualified.items()):
  if row['kind']=='function':
   p=directory/f'binding{i}.o';binding_object(name,row['mode'],record['flags'],p);objects.append(p);mem.append(f'BIND{i}: ORIGIN = {row["address"]} > binding{i}.bin');sections.append(f'.binding{i}: {{ {p.name}(.text) }} > BIND{i}');probes.append(dict(**row,object=p.relative_to(ROOT).as_posix(),objectSha256=sha256(p),nativeCalleeBytesUsed=0,calleeSourceCredit=0))
  else:assign.append(f'{name} = {row["address"]};')
 lcf=directory/'register.lcf';lcf.write_text('MEMORY {\n'+'\n'.join(mem)+'\n}\nSECTIONS {\n'+'\n'.join(assign+sections)+'\n}\n');elf=directory/'linked.elf';cmd=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm946e','-main',NAME,str(lcf),*map(str,objects),'-o',str(elf)];run=subprocess.run(cmd,cwd=directory,env=env(),capture_output=True,text=True,timeout=30)
 if run.returncode:raise ValueError(('Register genuine link failed',run.stdout,run.stderr))
 body=(directory/'caller.bin').read_bytes();assert sha256(obj)==before
 with elf.open('rb')as stream:
  e=ELFFile(stream);sy=e.get_section_by_name('.symtab');s=next(s for s in sy.iter_symbols()if s.name==NAME);local=next(s for s in sy.iter_symbols()if s.name==record['sourceLocal']['name']);assert s['st_value']==ADDRESS and s['st_size']==record['bytes'];assert local['st_value']==bss_address and local['st_size']==1 and local['st_info']['bind']=='STB_LOCAL'and isinstance(local['st_shndx'],int)
 proof=dict(exactWholeSpan=body==native,linkedBytes=len(body),expectedBytes=SIZE,matchingBytes=sum(a==b for a,b in zip(body,native)),object=obj.relative_to(ROOT).as_posix(),objectSha256=before,unmodifiedWholeCompilerObjectLinked=True,sourceLocal=record['sourceLocal'],sourceBssBytes=1,sourceBssAlignment=1,bssAddress=hex(bss_address),bssInitializedCredit=0,localAbsOrImportRebinding=0,sourceInstructionOrObjectPatches=0,linkedElf=elf.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(elf),linkedBinary=(directory/'caller.bin').relative_to(ROOT).as_posix(),linkedBinarySha256=sha256(directory/'caller.bin'),linkerCommand=cmd,linkerSha256=sha256(LINKER),bindingOnlyProbes=probes,dataBindings=[r for r in qualified.values()if r['kind']=='data'],sourceRelocations=record['relocations'])
 return record,proof,body

def build(source=None,directory=None,negative=False):
 directory=Path(directory or WORK/'build');obj,compiler=compile_source(source or SOURCE/'register.c',directory/'compiler');record,proof,body=link(obj,directory/'link')
 if not negative and not proof['exactWholeSpan']:raise ValueError(('Register complete native span differs',proof['matchingBytes'],proof['linkedBytes']))
 try:
  with obj.open('rb')as stream:split_symbol(ELFFile(stream),NAME,directory/'forbidden-old-split.o')
 except ValueError as error:
  if str(error)!='Source depends on a local symbol outside its section':raise
  guard=dict(rejected=True,reason=str(error))
 else:raise ValueError('Original local-source guard was weakened')
 return obj,record,dict(compiler=compiler,realLink=proof,unchangedOriginalSplitterGuard=guard),body

if __name__=='__main__':
 obj,record,proof,body=build();write_json(WORK/'initial-link.json',proof);print(len(body),proof['realLink']['exactWholeSpan'])
