import os,re,shutil,subprocess
from project import ROOT,sha256
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows

def function_bytes(path,name):
 with path.open('rb')as stream:
  elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name);start=s['st_value']&~1;return elf.get_section(s['st_shndx']).data()[start:start+s['st_size']]
def verify(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];obj=directory/'explicit-required.o';command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(obj)]
 run=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 if run.returncode:raise ValueError(('Explicit-interface preflight rejected selected source',row['address'],run.stdout,run.stderr))
 assert function_bytes(ROOT/row['object'],row['name'])==function_bytes(obj,row['name'])and relocation_rows(ROOT/row['object'],row['name'])==relocation_rows(obj,row['name'])
 wrong=directory/'missing';wrong.mkdir(parents=True,exist_ok=True)
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],wrong/(ROOT/pin['path']).name)
 copy=wrong/source.name;shutil.copyfile(source,copy);header=wrong/'context.h';text=header.read_text();name={0x209ab18:'native_fn_02090b60',0x209ab84:'native_fn_02094284',0x209ac5c:'native_fn_02096948',0x209ad08:'native_fn_02094420'}[int(row['address'],0)];text,n=re.subn(r'extern\s+[^;\n]*\b'+name+r'\s*\([^;]*\)\s*;','',text);assert n==1;header.write_text(text);bad=wrong/'missing.o'
 command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(copy),'-o',str(bad)];rejected=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 assert rejected.returncode!=0 and not bad.exists()
 return dict(allPassed=True,explicitPrototypeFlags=['-requireprotos','-w','error'],primaryFlagsUnchanged=True,positiveCompilerExit=run.returncode,completeObjectFunctionBytesAndRelocationsIdentical=True,negativeMissingActualImportDeclarationRejected=True,negativeDiagnostic=rejected.stdout+rejected.stderr,presenceOnlyNotTypeCorrectnessProof=True,diagnosticObjectSha256=sha256(obj),sourceOrExecutionCredit=0)
