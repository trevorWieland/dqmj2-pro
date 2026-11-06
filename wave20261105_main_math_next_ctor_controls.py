import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_main_math_next_ctor_compiler import COMPILER
from wave20261105_main_math_next_ctor_bindings import verify_original,negative_controls


def execute(rows):
    row=rows[0];verify_original(row,row['nativeSymbolEntries']);folder=ROOT/'work/w5mn/ctor/controls';folder.mkdir(parents=True,exist_ok=True)
    for item in row['sourceDependencies']:shutil.copyfile(ROOT/item['path'],folder/(ROOT/item['path']).name)
    checks=['sizeof(Constructor)==4','sizeof(Constructor*)==4','sizeof(native_data_020dcb30[0])==4'];source=folder/'layout.c';source.write_text('\n'.join('#include "'+(ROOT/p['path']).name+'"' for p in row['sourceDependencies'])+'\n'+'\n'.join('typedef char Layout'+str(i)+'[('+x+')?1:-1];' for i,x in enumerate(checks)));obj=folder/'layout.o';cmd=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Constructor compiler geometry failed',positive.stdout,positive.stderr))
    positive_hash=sha256(obj);header=next(folder.glob('context*.h'));text=header.read_text();changed=text.replace('typedef void (*Constructor)(void);','typedef unsigned long long Constructor;')
    if changed==text:raise ValueError('Actual wrong pointer-width type did not mutate')
    header.write_text(changed);wrong=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if wrong.returncode==0 or 'illegal constant expression' not in wrong.stdout:raise ValueError('Wrong pointer width passed native geometry')
    return dict(status='passed',actualCompilerGeometry=dict(checks=checks,objectSha256=positive_hash,wrongWidthRejected=True,negativeExitCode=wrong.returncode),negativeLiteralCases=negative_controls(row),originalStorageExtentAuthorshipCredit=0)
