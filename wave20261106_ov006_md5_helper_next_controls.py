import os,re,shutil,subprocess
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_md5_helper_next_build import build
from wave20261106_ov006_md5_helper_next_fixtures import run,cases

def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);text=(ROOT/row['source']).parent.joinpath('context.h').read_text()
 if wrong:text=text.replace('unsigned int UINT4','unsigned short UINT4')
 (directory/'context.h').write_text(text);p=directory/'layout.c';p.write_text('#include "context.h"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\nCHECK(word,sizeof(UINT4)==4);CHECK(pointer,sizeof(POINTER)==4);CHECK(byte,sizeof(unsigned char)==1);\nint layout(void);int layout(void){return sizeof(UINT4);}\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:
  if r.returncode==0:raise ValueError('Wrong MD5 helper word width accepted')
 elif r.returncode:raise ValueError(('Actual helper ABI widths rejected',r.stdout,r.stderr))
 return dict(allPassed=True,wordBytes=4,pointerBytes=4,byteBytes=1,wrongWordWidthRejected=wrong,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def wrong_source(row,directory):
 address=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();m=re.search(r'void '+row['name']+r'\s*\([^;]+?\)\s*\{',text);assert m;end=m.end();depth=1
 while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
 part=text[m.start():end];old,new={0x21f1e40:('>> 8','>> 7'),0x21f1e6c:('<< 8','<< 7'),0x21f1e98:('input[i]','input[i+1]'),0x21f1eb0:('(char)value','(char)(value+1)')}[address];assert old in part;changed=text[:m.start()]+part.replace(old,new,1)+text[end:];directory.mkdir(parents=True,exist_ok=True);p=directory/'wrong.c';p.write_text(changed);shutil.copyfile(source.parent/'context.h',directory/'context.h');bad,body=build(p,directory/'build',address,negative=True);observed=run(address,body,cases(address)[1],0)
 if observed['modelPassed']or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong leaf helper C accepted')
 return dict(caller=row['address'],allPassed=True,changedCStatement=dict(original=old,mutant=new),changedSourceSha256=sha256(p),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentAliasMemoryModelRejected=True,observed=observed,sourceOrExecutionCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context.h';(directory/'context.h').write_bytes(header.read_bytes());p=directory/'probe.c';p.write_text('#include "context.h"\nvoid declaration_probe(unsigned char*out,UINT4*in,unsigned int n);void declaration_probe(unsigned char*out,UINT4*in,unsigned int n){native_ov006_021f1e40(out,in,n);}\n');good=compile_probe(row,p,directory/'positive.o');assert good.returncode==0;text,n=re.subn(r'extern void native_ov006_021f1e40\([^;]*;','',header.read_text());assert n==1;(directory/'context.h').write_text(text);bad=compile_probe(row,p,directory/'negative.o');assert bad.returncode!=0
 return dict(allPassed=True,explicitCallPositive=True,missingCallDeclarationRejected=True,diagnosticOnly=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
