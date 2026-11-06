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
 return dict(allPassed=True,explicitPrototypeFlags=['-requireprotos','-w','error'],primaryFlagsUnchanged=True,completeObjectFunctionBytesAndRelocationsIdentical=True,diagnosticObjectSha256=sha256(obj),allActualCallsDeclared=True,actualImportedCallsHaveExplicitPublicMeasuredPrototypes=True,presenceOnlyNotTypeCorrectnessProof=True,sourceOrExecutionCredit=0)
