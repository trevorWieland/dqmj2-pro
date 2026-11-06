import os,re,shutil,subprocess
import match_runtime
from project import ROOT,sha256
from wave20261106_g3d_context_next_first_build import build
from wave20261106_g3d_context_next_first_fixtures import run

def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def copy_source(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source']
 for p in[source,*source.parent.glob('*.h')]:shutil.copyfile(p,directory/p.name)
 return directory/source.name

def layout(row,directory,wrong=False):
 copy_source(row,directory);h=directory/'context_00.h'
 if wrong:
  text=h.read_text();assert'u16 origWidth, origHeight;'in text;h.write_text(text.replace('u16 origWidth, origHeight;','u8 origWidth, origHeight;'))
 p=directory/'layout.c';p.write_text('#include "context_00.h"\n#include "context_01.h"\n#define OFF(t,m) ((unsigned long)&(((t*)0)->m))\n#define CHECK(n,x) typedef char n[(x)?1:-1]\nCHECK(word,sizeof(u32)==4);CHECK(ptr,sizeof(void*)==4);CHECK(matrix,sizeof(MtxFx44)==64);CHECK(m00,OFF(MtxFx44,_00)==0);CHECK(m11,OFF(MtxFx44,_11)==20);CHECK(m30,OFF(MtxFx44,_30)==48);CHECK(m31,OFF(MtxFx44,_31)==52);CHECK(cmd,sizeof(native_data_main_020dd690)==8);CHECK(flag,OFF(NNSG3dRS,flag)==8);CHECK(cb,OFF(NNSG3dRS,cbVecFunc)==12);CHECK(timing,OFF(NNSG3dRS,cbVecTiming)==140);CHECK(material,OFF(NNSG3dRS,pMatAnmResult)==176);CHECK(resmat,OFF(NNSG3dRS,pResMat)==216);CHECK(tex,OFF(NNSG3dMatAnmResult,prmTexImage)==16);CHECK(width,OFF(NNSG3dMatAnmResult,origWidth)==44);CHECK(height,OFF(NNSG3dMatAnmResult,origHeight)==46);CHECK(widthtype,sizeof(((NNSG3dMatAnmResult*)0)->origWidth)==2);CHECK(baserot,OFF(NNSG3dGlb,prmBaseRot)==188);CHECK(basetrans,OFF(NNSG3dGlb,prmBaseTrans)==224);CHECK(glbflag,OFF(NNSG3dGlb,flag)==252);\nint layout(void);int layout(void){return sizeof(MtxFx44); }\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:assert r.returncode!=0
 elif r.returncode:raise ValueError((r.stdout,r.stderr))
 return dict(allPassed=True,typedMatrixCommandAndResourceOffsetsVerified=True,wrongMaterialWidthRejected=wrong,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def wrong_source(row,directory):
 p=copy_source(row,directory);text=p.read_text();old='width << (12 + 3)';assert old in text;p.write_text(text.replace(old,'width << (12 + 2)'));bad,body=build(p,directory/'build',0x2031b44,negative=True);assert len(body)==940;observed=run(body,6);assert not observed['modelPassed']and not bad['realLink']['exactCallerBytes'];return dict(allPassed=True,changedCStatement='Both matrix width terms shift15 -> shift14',changedSourceSha256=sha256(p),genuineMutantLinked=True,completeNativeEqualityRejected=True,independentMatrixMemoryModelRejected=True,observed=observed,sourceOrExecutionCredit=0)

def coalesced_context(row,directory):
 p=copy_source(row,directory);header=directory/'context_00.h';text=header.read_text();text=text.replace('extern MtxFx44 native_data_main_020dd6c0;','').replace('extern u32 native_data_main_020dd690[2];','');text+='\ntypedef struct{u32 cmd[2];u8 opaque[40];MtxFx44 mtx;}Coalesced;\nextern Coalesced native_data_main_020dd690;\n#define prj_cmd (native_data_main_020dd690.cmd)\n#define native_data_main_020dd6c0 (native_data_main_020dd690.mtx)\n';header.write_text(text);p.write_text(p.read_text().replace('native_data_main_020dd690','prj_cmd'));bad,body=build(p,directory/'build',0x2031b44,negative=True);assert not bad['realLink']['exactCallerBytes'];return dict(allPassed=True,sameAlgorithmAndNativeDataAddresses=True,individualObjectIdentityCollapsed=True,genuineMutantLinked=True,completeNativeEqualityRejected=True,nativeBytes=940,coalescedCompiledBytes=bad['compiledBytes'],sourceSha256=sha256(p),contextSha256=sha256(header),providerModelNotRunOnWrongExtent=True,sourceOrExecutionCredit=0)

def missing_prototype(row,directory):
 p=copy_source(row,directory);header=directory/'context_00.h';good=compile_probe(row,p,directory/'good.o');assert good.returncode==0;text,n=re.subn(r'void native_fn_main_02031ef0\([^;]*;','',header.read_text());assert n==1;header.write_text(text);bad=compile_probe(row,p,directory/'bad.o');assert bad.returncode!=0;return dict(allPassed=True,explicitCallPositive=True,missingActualCallDeclarationRejected=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
