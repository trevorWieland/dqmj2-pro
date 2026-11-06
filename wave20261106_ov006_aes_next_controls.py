import os,re,shutil,subprocess,hashlib
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_aes_next_build import build
from wave20261106_ov006_aes_next_fixtures import run
from wave20261106_ov006_aes_next_model import cases
from wave20261106_ov006_aes_next_prototypes import function_bytes

def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context.h';text=header.read_text()
 if wrong:
  text,n=re.subn(r'uint32_t native_data_ov006_022094b8\[256\]',r'uint32_t native_data_ov006_022094b8[255]',text);assert n==1
 (directory/'context.h').write_text(text);source=directory/'layout.c';source.write_text('#include "context.h"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\nCHECK(word,sizeof(uint32_t)==4);CHECK(byte,sizeof(uint8_t)==1);CHECK(table,sizeof(Te0)==1024);CHECK(table4,sizeof(Td4)==1024);CHECK(constants,sizeof(rcon)==40);\nint layout(void);int layout(void){return sizeof(uint32_t);}\n');obj=directory/'layout.o';command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(obj)];result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 if wrong:
  if result.returncode==0:raise ValueError('Wrong AES table extent accepted')
 else:
  if result.returncode:raise ValueError(('AES actual type/layout rejected',result.stdout,result.stderr))
 return dict(allPassed=True,wrongTableExtentRejected=wrong,positiveActualTypesCompiled=not wrong,wordBytes=4,byteBytes=1,tableElements=256,rconElements=10,diagnostics=result.stdout+result.stderr,executionCredit=0)

def wrong_source(row,directory,compiled):
 address=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();start=text.index(('int 'if address in[0x21f0944,0x21f0bfc]else'void ')+row['name']+'(');end=text.find('\nint native_',start+1);nextvoid=text.find('\nvoid native_',start+1);end=min([i for i in[end,nextvoid,len(text)]if i>=0]);part=text[start:end]
 old,new={0x21f0944:('keyBits == 128','keyBits == 129'),0x21f0bfc:('j = 4*Nr','j = 4*Nr - 4'),0x21f0d8c:('^ rk[0]','^ rk[1]'),0x21f1148:('^ rk[0]','^ rk[1]')}[address]
 if old not in part:raise ValueError(('AES intended semantic mutation absent',address,old))
 part=part.replace(old,new,1);changed=text[:start]+part+text[end:];directory.mkdir(parents=True,exist_ok=True);copy=directory/'mutant.c';copy.write_text(changed);shutil.copyfile(source.parent/'context.h',directory/'context.h');bad,body=build(copy,directory/'build',address,negative=True)
 if bad['realLink']['exactCallerBytes']or body==(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes():raise ValueError('Wrong AES source body accepted')
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();state=cases(address)[0];observed=run(address,body,image,compiled,state,0)
 if observed['modelPassed']:raise ValueError('Wrong AES source passed independent GF/boundary model')
 return dict(caller=row['address'],allPassed=True,changedCStatement=dict(original=old,mutant=new),changedSourceSha256=sha256(copy),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentModelRejected=True,observed=observed,originalActualRelocationBindingsRetained=True,extraSourceCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context.h';(directory/'context.h').write_bytes(header.read_bytes());probe=directory/'probe.c';probe.write_text('#include "context.h"\nint declaration_probe(uint32_t*r,const uint8_t*k,int b);int declaration_probe(uint32_t*r,const uint8_t*k,int b){return native_ov006_021f0944(r,k,b);}\n');command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(probe),'-o',str(directory/'positive.o')];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));good=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60);assert good.returncode==0
 text,n=re.subn(r'extern int native_ov006_021f0944\([^;]*;','',header.read_text());assert n==1;(directory/'context.h').write_text(text);command[-1]=str(directory/'negative.o');bad=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
 if bad.returncode==0:raise ValueError('Missing AES call declaration accepted by strict diagnostic')
 return dict(allPassed=True,positiveDeclaredCallCompiled=True,negativeMissingDeclarationRejected=True,negativeDiagnostic=bad.stdout+bad.stderr,diagnosticOnly=True,actualCompleteSourceStrictObjectProofSeparate=True,sourceOrExecutionCredit=0)
