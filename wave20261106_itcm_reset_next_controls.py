import os
import shutil
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json
from wave20261106_itcm_reset_next_paths import SOURCE,WORK,EVIDENCE,assert_owned
from wave20261106_itcm_reset_next_compiler import COMPILER
from wave20261106_itcm_reset_next_bindings import verify_original,negative_controls


def execute(rows):
    assert_owned();row=rows[0];verify_original(row,row['nativeSymbolEntries']);folder=WORK/'layout';folder.mkdir(parents=True,exist_ok=True);header=folder/'context.h';original=(SOURCE/'context.h').read_text();header.write_text(original);checks=['sizeof(void*)==4','sizeof(u32)==4','sizeof(s32)==4','sizeof(OSIntrMode)==4','(s32)-1<0','(u32)-1>0'];source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join(f'typedef char Geometry{i}[({expr})?1:-1];'for i,expr in enumerate(checks)));env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(folder/'layout.o')];positive=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if positive.returncode:raise ValueError(('Actual reset ABI geometry rejected',positive.stdout,positive.stderr))
    header.write_text(original.replace('unsigned long u32','unsigned short u32'));negative=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if not negative.returncode:raise ValueError('Wrong consumed reset word geometry accepted')
    def allocated(path):
        with path.open('rb')as f:return [(s.name,s['sh_flags'],s.data().hex())for s in ELFFile(f).iter_sections()if s['sh_flags']&2]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];strict=folder/'explicit.o';p=subprocess.run([str(COMPILER),*flags,'-c',str(ROOT/row['source']),'-o',str(strict)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if p.returncode or allocated(strict)!=allocated(ROOT/row['object']):raise ValueError(('Explicit reset prototype diagnostic failed or changed executable sections',p.stdout,p.stderr))
    header.write_text(original.replace('native_fn_02007ff4(','missing_actual_irq_declaration('));missing=folder/'missing.c';shutil.copyfile(ROOT/row['source'],missing);q=subprocess.run([str(COMPILER),*flags,'-c',str(missing),'-o',str(folder/'missing.o')],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if not q.returncode or 'no prototype'not in q.stdout:raise ValueError(('Missing actual reset provider declaration admitted',q.stdout,q.stderr))
    with(ROOT/row['object']).open('rb')as f:
        e=ELFFile(f);s=next(s for s in e.get_section_by_name('.symtab').iter_symbols()if s.name==row['name']);section=e.get_section(s['st_shndx'])
        if s['st_info']['type']!='STT_FUNC'or section['sh_type']!='SHT_PROGBITS'or section['sh_flags']!=6 or s['st_size']!=168:raise ValueError('Actual complete ordinary-C ARM ELF entry/section differs')
        if any(s['sh_flags']&2 and s['sh_size']and not s['sh_flags']&4 for s in e.iter_sections()):raise ValueError('Unowned reset data/BSS context emitted')
    value=dict(status='passed',actualLayoutChecks=checks,wrongWordLayoutRejected=True,prototypeDiagnostic=dict(flags=flags,actualAllocatedSectionsUnchanged=True,missingActualDeclarationRejected=True,negativeDiagnostic=q.stdout),nativeBoundaryControls=negative_controls(rows),actualStandaloneOriginalEntryExecutions=0,originalObjectAndRelocationsUnchanged=True,sourceCredit=0);write_json(EVIDENCE/'binding-layout-controls.json',value);return value
