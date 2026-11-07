import shutil
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
from link_runtime_unit import verify_binding,relocation_rows
from wave20261106_mb_local_context_next_register_build import SOURCE,WORK,NAME,UPDATE,compile_source,inspect_object,build,link
from wave20261106_mb_local_context_next_register_fixtures import execute,cases

def variant(name,old,new):
 dest=WORK/'controls'/name
 if dest.resolve()!=WORK.resolve()/'controls'/name or not dest.resolve().is_relative_to(WORK.resolve()/'controls'):raise ValueError('Register variant escaped exact control output')
 dest.mkdir(parents=True,exist_ok=True);count=0
 for p in[SOURCE/'register.c',*sorted(SOURCE.glob('context_*.h'))]:
  text=p.read_text();count+=text.count(old);(dest/p.name).write_text(text.replace(old,new))
 if count!=1:raise ValueError(('Register mutation is not unique',name,count))
 return dest/'register.c',dest

def raw(path):
 with Path(path).open('rb')as stream:
  e=ELFFile(stream);s=next(s for s in e.get_section_by_name('.symtab').iter_symbols()if s.name==NAME);sec=e.get_section(s['st_shndx']);return sec.data()[s['st_value']:s['st_value']+s['st_size']],relocation_rows(path,NAME)

def prove():
 obj,record,proof,body=build();rows=[]
 for name,old,new,case_name in[('capacity','+ 1 > (16)','+ 1 > (15)','first-available-0-irq0'),('first-available','.active == 0','.active != 0','all-busy-irq0')]:
  source,dest=variant(name,old,new);mut,compiler=compile_source(source,dest/'compiler');_,linked,changed=link(mut,dest/'link')
  if linked['exactWholeSpan']:raise ValueError('Wrong Register C passed complete native match')
  case=next(c for c in cases()if c['name']==case_name)
  try:execute(changed,case)
  except ValueError as failure:
   if 'Independent Register state model failed'not in str(failure):raise
   rejected=dict(reason=str(failure),intendedCase=case_name)
  else:raise ValueError('Wrong Register C passed independent state model')
  rows.append(dict(name=name,sourceMutation=dict(before=old,after=new),objectSha256=sha256(mut),compiler=compiler,realLink=linked,independentModelRejected=rejected,sourceInstructionOrObjectPatches=0))
 strict,strict_flags=compile_source(SOURCE/'register.c',WORK/'controls/strict',strict=True);normal,normal_flags=compile_source(SOURCE/'register.c',WORK/'controls/normal',strict=False)
 if raw(strict)!=raw(normal):raise ValueError('Strict declaration diagnostics changed Register body or relocation signature')
 for name,old,new in[('missing-prototype','extern void MBi_MakeDownloadFileInfo(MbDownloadFileInfoHeader * mbdlFileInfop, const void * buf);',''),('wrong-prototype','extern void MBi_MakeDownloadFileInfo(MbDownloadFileInfoHeader * mbdlFileInfop, const void * buf);','extern void MBi_MakeDownloadFileInfo(void);')]:
  source,dest=variant(name,old,new)
  try:compile_source(source,dest/'compiler')
  except ValueError as failure:rows.append(dict(name=name,rejected=True,reason=str(failure)))
  else:raise ValueError('Wrong/missing Register provider declaration compiled')
 source,dest=variant('wide-static','static u8 update = 0;','static u16 update = 0;');wide,compiler=compile_source(source,dest/'compiler')
 try:inspect_object(wide)
 except ValueError as failure:
  if str(failure)!='Register source local byte section changed':raise
  rows.append(dict(name='wide-static',rejected=True,reason=str(failure),compiler=compiler,objectSha256=sha256(wide)))
 else:raise ValueError('Incorrect private storage width accepted')
 _,wrong_link,_=link(obj,WORK/'controls/wrong-bss-link',bss_address=UPDATE+1)
 if wrong_link['exactWholeSpan']:raise ValueError('Wrong source BSS address preserved native bytes')
 binding=dict(name='MBi_MakeDownloadFileInfo',program='',processor='arm9',module='main',mode='arm',kind='function',address='0x2015f00');bad=[]
 for key,value in[('processor','arm7'),('program','other'),('module','ov006'),('mode','thumb'),('address','0x2015f04')]:
  test=dict(binding);test[key]=value
  try:verify_binding(test['name'],test)
  except ValueError as failure:bad.append(dict(field=key,value=value,rejected=True,reason=str(failure)))
  else:raise ValueError('Wrong native Register provider identity accepted')
 return dict(sourceAndLinkControls=rows,strictPrototypeFlagsByteAndRelocationIdentical=True,normalCompiler=normal_flags,strictCompiler=strict_flags,wrongBssOriginGenuineLinkRejectedByWholeNativeMatch=wrong_link,wrongNativeBindingControls=bad,unchangedOriginalSplitterGuard=proof['unchangedOriginalSplitterGuard'],allInstructionAndObjectMutationCounts=0)

if __name__=='__main__':write_json(WORK/'controls.json',prove());print('Register controls passed')
