import os,re,shutil,subprocess
import match_runtime
from project import ROOT,sha256
from wave20261106_ov006_crypto_utility_next_first_build import build
from wave20261106_ov006_crypto_utility_next_first_fixtures import run
from wave20261106_ov006_crypto_utility_next_first_model import cases

def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);text=(ROOT/row['source']).parent.joinpath('context.h').read_text()
 if wrong:text=text.replace('u32 x,y;','unsigned short x,y;')
 (directory/'context.h').write_text(text);p=directory/'layout.c';p.write_text('#include "context.h"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\n#define OFF(f) ((unsigned long)&(((Stream*)0)->f))\nCHECK(word,sizeof(u32)==4);CHECK(state,sizeof(Stream)==16);CHECK(x,OFF(x)==0);CHECK(y,OFF(y)==4);CHECK(ptr,OFF(state)==8);CHECK(n,OFF(size)==12);\nint layout(void);int layout(void){return sizeof(Stream);}\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:
  if r.returncode==0:raise ValueError('Wrong stream layout accepted')
 elif r.returncode:raise ValueError(('Actual stream layout rejected',r.stdout,r.stderr))
 return dict(allPassed=True,wrongLayoutRejected=wrong,targetContextBytes=16,x=0,y=4,statePointer=8,size=12,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def wrong_source(row,directory,compiled):
 address=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();start=re.search(r'(?:void|u32) '+row['name']+r'\s*\(',text).start();end=text.find('\n',start);end=len(text)if end<0 else end;part=text[start:end];old,new={0x21ed86c:('c->y=0','c->y=1'),0x21ed8d0:('in[i]^key','in[i]|key'),0x21ed8fc:('c->x+1','c->x+2'),0x21ed964:('crc>>8','crc>>7'),0x21f08fc:('a[0]^b[0]','a[0]|b[0]')}[address];assert old in part;changed=text[:start]+part.replace(old,new,1)+text[end:];directory.mkdir(parents=True,exist_ok=True);p=directory/'wrong.c';p.write_text(changed);shutil.copyfile(source.parent/'context.h',directory/'context.h');bad,body=build(p,directory/'build',address,negative=True);v=cases(address)[{0x21ed86c:0,0x21ed8d0:2,0x21ed8fc:1,0x21ed964:2,0x21f08fc:0}[address]];observed=run(address,body,compiled,v,0)
 if observed['modelPassed']or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong crypto C accepted')
 return dict(caller=row['address'],allPassed=True,changedCStatement=dict(original=old,mutant=new),changedSourceSha256=sha256(p),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentModelRejected=True,observed=observed,sourceOrExecutionCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context.h';(directory/'context.h').write_bytes(header.read_bytes());p=directory/'probe.c';p.write_text('#include "context.h"\nu32 declaration_probe(Stream*c);u32 declaration_probe(Stream*c){return native_ov006_021ed8fc(c);}\n');good=compile_probe(row,p,directory/'positive.o');assert good.returncode==0;new,n=re.subn(r'extern u32 native_ov006_021ed8fc\([^;]*;','',header.read_text());assert n==1;(directory/'context.h').write_text(new);bad=compile_probe(row,p,directory/'negative.o');assert bad.returncode!=0
 return dict(allPassed=True,actualDeclaredCallPositive=True,missingDeclarationRejected=True,diagnosticOnly=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
