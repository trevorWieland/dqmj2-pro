import re,shutil,os,subprocess
from project import ROOT,sha256
from wave20261106_g3d_blendvis_next_build import build
from wave20261106_g3d_blendvis_next_fixtures import run

def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def copy_source(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source']
 for p in[source,*source.parent.glob('*.h')]:shutil.copyfile(p,directory/p.name)
 return directory/source.name

def layout(row,directory,wrong=False):
 copy_source(row,directory);h=directory/'context.h'
 if wrong:h.write_text(h.read_text().replace('u8 numMapData;','u16 numMapData;'))
 p=directory/'layout.c';p.write_text('#include "context.h"\n#define OFF(t,m) ((unsigned long)&(((t*)0)->m))\n#define CHECK(n,x) typedef char n[(x)?1:-1]\nCHECK(word,sizeof(u32)==4);CHECK(ptr,sizeof(void*)==4);CHECK(boolean,sizeof(BOOL)==4);CHECK(result,sizeof(NNSG3dVisAnmResult)==4);CHECK(frame,OFF(NNSG3dAnmObj,frame)==0);CHECK(resource,OFF(NNSG3dAnmObj,resAnm)==8);CHECK(callback,OFF(NNSG3dAnmObj,funcAnm)==12);CHECK(next,OFF(NNSG3dAnmObj,next)==16);CHECK(count,OFF(NNSG3dAnmObj,numMapData)==25);CHECK(map,OFF(NNSG3dAnmObj,mapData)==26);CHECK(size,sizeof(NNSG3dAnmObj)==28);\nint layout(void);int layout(void){return sizeof(NNSG3dAnmObj); }\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:assert r.returncode!=0
 elif r.returncode:raise ValueError((r.stdout,r.stderr))
 return dict(allPassed=True,objectBytes=28,resultBytes=4,targetWordPointerBooleanBytes=4,actualFieldOffsetsVerified=True,wrongMapCountWidthRejected=wrong,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def wrong_source(row,directory):
 p=copy_source(row,directory);text=p.read_text();assert'if(dataIdx&0x0100)'in text;p.write_text(text.replace('if(dataIdx&0x0100)','if((dataIdx&0x0300)==0x0100)',1));bad,body=build(p,directory/'build',0x202e260,negative=True);indices=[i for i in range(32)if any(c['tag']&0x300==0x300 for c in run(None,i)['callbacks'])];assert indices;observed=run(body,indices[0]);assert not observed['modelPassed']and not bad['realLink']['exactCallerBytes'];return dict(allPassed=True,changedCStatement='Replace measured EXIST-only predicate with current public EXIST-and-not-DISABLED predicate',changedSourceSha256=sha256(p),genuineMutantLinked=True,completeNativeEqualityRejected=True,independentTagListMaskModelRejected=True,actualCaseIndex=indices[0],observed=observed,sourceOrExecutionCredit=0)

def prototype_negative(row,directory):
 p=copy_source(row,directory);h=directory/'context.h';good=compile_probe(row,p,directory/'good.o');assert good.returncode==0;text=h.read_text();old='NNSG3dVisAnmResult*,const NNSG3dAnmObj*,u32);';assert old in text;h.write_text(text.replace(old,'NNSG3dVisAnmResult*,const NNSG3dAnmObj*);',1));bad=compile_probe(row,p,directory/'bad.o');assert bad.returncode!=0;return dict(allPassed=True,explicitThreeArgumentCallbackPositive=True,twoArgumentCallbackPrototypeRejected=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
