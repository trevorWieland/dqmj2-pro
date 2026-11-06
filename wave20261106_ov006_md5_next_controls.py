import os,re,shutil,subprocess
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_md5_next_build import build
from wave20261106_ov006_md5_next_fixtures import run
from wave20261106_ov006_md5_next_model import cases

def compile_probe(row,path,obj):
 command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)]
 return subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);text=(ROOT/row['source']).parent.joinpath('context.h').read_text()
 if wrong:text,n=re.subn(r'count\[2\]',r'count[3]',text);assert n==1
 (directory/'context.h').write_text(text);source=directory/'layout.c';source.write_text('#include "context.h"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\n#define OFF(f) ((unsigned long)&(((MD5_CTX*)0)->f))\nCHECK(word,sizeof(UINT4)==4);CHECK(context,sizeof(MD5_CTX)==88);CHECK(state,OFF(state)==0);CHECK(count,OFF(count)==16);CHECK(buffer,OFF(buffer)==24);CHECK(padding,sizeof(PADDING)==64);\nint layout(void);int layout(void){return sizeof(MD5_CTX);}\n');result=compile_probe(row,source,directory/'layout.o')
 if wrong:
  if result.returncode==0:raise ValueError('Wrong MD5 context accepted')
 elif result.returncode:raise ValueError(('MD5 actual layout rejected',result.stdout,result.stderr))
 return dict(allPassed=True,wrongContextLayoutRejected=wrong,positiveActualTypesCompiled=not wrong,wordBytes=4,contextBytes=88,stateOffset=0,countOffset=16,bufferOffset=24,paddingBytes=64,diagnostics=result.stdout+result.stderr,executionCredit=0)

def wrong_source(row,directory,compiled):
 address=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();start=re.search(r'void '+row['name']+r'\s*\(',text).start();end=text.find('\nvoid native_',start+1);end=len(text)if end<0 else end;part=text[start:end];old,new={0x21f152c:('partLen = 64 - index','partLen = 63 - index'),0x21f15a4:('index < 56','index < 55'),0x21f15f8:('0xfde5380c','0xfde5380d')}[address]
 if old not in part:raise ValueError(('Intended MD5 semantic mutation absent',address,old))
 changed=text[:start]+part.replace(old,new,1)+text[end:];directory.mkdir(parents=True,exist_ok=True);copy=directory/'mutant.c';copy.write_text(changed);shutil.copyfile(source.parent/'context.h',directory/'context.h');bad,body=build(copy,directory/'build',address,negative=True)
 if bad['realLink']['exactCallerBytes']or body==(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes():raise ValueError('Wrong MD5 body accepted')
 state=next(v for v in cases(address)if address==0x21f15f8 or address==0x21f152c and v['prefix']==0 and v['length']==64 or address==0x21f15a4 and v['length']==55);image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();observed=run(address,body,image,compiled,state,0)
 if observed['modelPassed']:raise ValueError('Wrong MD5 source passed independent model')
 return dict(caller=row['address'],allPassed=True,changedCStatement=dict(original=old,mutant=new),changedSourceSha256=sha256(copy),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentModelRejected=True,observed=observed,originalActualRelocationBindingsRetained=True,extraSourceCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context.h';(directory/'context.h').write_bytes(header.read_bytes());probe=directory/'probe.c';probe.write_text('#include "context.h"\nvoid declaration_probe(unsigned char*out,UINT4*in,unsigned int n);void declaration_probe(unsigned char*out,UINT4*in,unsigned int n){native_ov006_021f1e40(out,in,n);}\n');good=compile_probe(row,probe,directory/'positive.o');assert good.returncode==0
 text,n=re.subn(r'extern void native_ov006_021f1e40\([^;]*;','',header.read_text());assert n==1;(directory/'context.h').write_text(text);bad=compile_probe(row,probe,directory/'negative.o')
 if bad.returncode==0:raise ValueError('Missing MD5 helper declaration accepted by strict diagnostic')
 return dict(allPassed=True,positiveDeclaredCallCompiled=True,negativeMissingDeclarationRejected=True,negativeDiagnostic=bad.stdout+bad.stderr,diagnosticOnly=True,actualCompleteSourceStrictObjectProofSeparate=True,sourceOrExecutionCredit=0)
