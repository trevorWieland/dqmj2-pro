import re,shutil,os,subprocess
from project import ROOT,sha256
def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
from wave20261106_g2d_canvas_next_third_build import build
from wave20261106_g2d_canvas_next_third_fixtures import run

def layout(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);h=(ROOT/row['source']).parent/'context.h';text=h.read_text()
 if wrong:text=text.replace('opaque4[47]','opaque4[46]')
 (directory/'context.h').write_text(text);p=directory/'layout.c';p.write_text('#include "context.h"\n#define OFF(t,m) ((unsigned long)&(((t*)0)->m))\n#define CHECK(n,x) typedef char n[(x)?1:-1]\nCHECK(word,sizeof(int)==4);CHECK(ptr,sizeof(void*)==4);CHECK(state,OFF(RawContext,state)==0);CHECK(a,OFF(RawContext,byte33)==0x33);CHECK(b,OFF(RawContext,byte35)==0x35);CHECK(pointer,OFF(RawContext,word44)==0x44);CHECK(c,OFF(RawContext,byte5d)==0x5d);CHECK(d,OFF(RawContext,byte5e)==0x5e);CHECK(e,OFF(RawContext,byte5f)==0x5f);\nint layout(void);int layout(void){return sizeof(RawContext); }\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:assert r.returncode!=0
 elif r.returncode:raise ValueError((r.stdout,r.stderr))
 return dict(allPassed=True,rawByteOffsetsVerified=True,wrongByteOffsetRejected=wrong,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def wrong_source(row,directory):
 directory.mkdir(parents=True,exist_ok=True);p=directory/'02087334.c';source=ROOT/row['source'];text=source.read_text();assert'mode=15;'in text;p.write_text(text.replace('mode=15;','mode=14;',1));shutil.copyfile(source.parent/'context.h',directory/'context.h');bad,body=build(p,directory/'build',0x2087334,negative=True);observed=run(body,1);assert not observed['modelPassed']and not bad['realLink']['exactCallerBytes'];return dict(allPassed=True,changedCStatement='mode=15 -> mode=14',changedSourceSha256=sha256(p),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentSixArgumentModelRejected=True,observed=observed,sourceOrExecutionCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];h=(source.parent/'context.h').read_text();p=directory/'probe.c';p.write_text(source.read_text());(directory/'context.h').write_text(h);good=compile_probe(row,p,directory/'good.o');assert good.returncode==0;h,n=re.subn(r'void native_fn_main_02087e58\([^;]*;','',h);assert n==1;(directory/'context.h').write_text(h);bad=compile_probe(row,p,directory/'bad.o');assert bad.returncode!=0;return dict(allPassed=True,explicitCallPositive=True,missingActualCallDeclarationRejected=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
