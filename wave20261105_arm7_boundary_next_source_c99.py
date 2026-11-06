import os
import subprocess
from project import ROOT,sha256
from link_runtime_unit import relocation_rows
from wave20261105_arm7_boundary_next_source_build import build,SOURCE,WORK,COMPILER,FLAGS


def execute(baseline):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-boundary-next' or WORK!=ROOT/'work/w5ab-source':raise ValueError('Owned ARM7 C99 frontend proof scope differs')
    if FLAGS.count('-lang')!=1 or FLAGS[FLAGS.index('-lang')+1]!='c99':raise ValueError('Actual production compiler frontend is not explicitly C99')
    row,body=build(SOURCE/'027e0898.c',WORK/'c99-independent')
    if row['compilerFlags']!=baseline['compilerFlags'] or row['compilerFlags'].count('-lang')!=1 or row['compilerFlags'][row['compilerFlags'].index('-lang')+1]!='c99' or row['command'][1:1+len(FLAGS)]!=FLAGS:raise ValueError('Fresh C99 command/profile differs')
    before=relocation_rows(ROOT/baseline['object'],baseline['name']);after=relocation_rows(ROOT/row['object'],row['name'])
    if before!=after or row['outputSha256']!=baseline['targetSha256'] or row['compiledBytes']!=4464 or not row['realLink']['exactCallerBytes']:raise ValueError('Fresh actual C99 whole body/ELF relocation payload differs')
    directory=WORK/'c99-frontend-witness';directory.mkdir(parents=True,exist_ok=True);source=directory/'witness.c';source.write_text('int witness(void *p){int *value=p;return *value;}\n');results=[]
    for language in ['c99','c++']:
        flags=list(FLAGS);flags[flags.index('-lang')+1]=language;output=directory/(language.replace('+','p')+'.o');argv=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if (language=='c99')!=(process.returncode==0):raise ValueError(('Controlled actual compiler frontend witness failed to distinguish C99/C++',language,process.stdout,process.stderr))
        results.append(dict(language=language,command=argv,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr,sourceSha256=sha256(source),objectSha256=sha256(output) if process.returncode==0 else None))
    return dict(status='passed',sourceCredit=0,actualExplicitFrontend='c99',freshCaller=row,allOriginalRelocationPayloadsIdentical=True,originalRelocationCount=len(after),completeNativeBodyBytes=4464,completeNativeBodySha256=row['outputSha256'],genuineTwoThunkLink=True,frontendWitness=results,limits=['Production profile is unchanged except that this independently fresh object explicitly proves its already-selected C99 frontend. Controlled witness accepts implicit void-pointer conversion in C99 and rejects it in C++; no original data/algorithm ASM/binary compiler inputs.'])
