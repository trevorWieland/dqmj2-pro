import os,re,shutil,subprocess
import match_runtime
from project import ROOT,sha256
from wave20261106_g2d_canvas_next_first_build import build
from wave20261106_g2d_canvas_next_first_fixtures import run

def compile_probe(row,path,obj):
 return subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-requireprotos','-w','error','-c',str(path),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)

def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];text=source.read_text()
 if wrong:text=text.replace('int dstBpp;','short dstBpp;')
 (directory/'selected.c').write_text(text);p=directory/'layout.c';p.write_text('#include "selected.c"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\n#define OFF(t,m) ((unsigned long)&(((t*)0)->m))\nCHECK(word,sizeof(u32)==4);CHECK(ptr,sizeof(void*)==4);CHECK(info,sizeof(LC_INFO)==40);CHECK(reader,sizeof(NNSiG2dBitReader)==8);CHECK(available,OFF(NNSiG2dBitReader,availableBits)==4);CHECK(bits,OFF(NNSiG2dBitReader,bits)==5);CHECK(x,OFF(LC_INFO,ofs_x)==8);CHECK(width,OFF(LC_INFO,width)==16);CHECK(stride,OFF(LC_INFO,dsrc)==24);CHECK(srcbpp,OFF(LC_INFO,srcBpp)==28);CHECK(dstbpp,OFF(LC_INFO,dstBpp)==32);CHECK(dstwidth,sizeof(((LC_INFO*)0)->dstBpp)==4);CHECK(color,OFF(LC_INFO,cl)==36);\nint layout(void);int layout(void){return sizeof(LC_INFO); }\n');r=compile_probe(row,p,directory/'layout.o')
 if wrong:
  if r.returncode==0:raise ValueError('Wrong canvas word layout accepted')
 elif r.returncode:raise ValueError(('Actual G2D layout rejected',r.stdout,r.stderr))
 return dict(allPassed=True,LCInfoBytes=40,bitReaderBytes=8,wordPointerBytes=4,wrongFieldWidthRejected=wrong,diagnostic=r.stdout+r.stderr,sourceOrExecutionCredit=0)

def glyph_layout(row,directory):
 directory.mkdir(parents=True,exist_ok=True);shutil.copyfile((ROOT/row['source']).parent/'context_00.h',directory/'context_00.h');p=directory/'layout.c';p.write_text('#include "context_00.h"\n#define CHECK(n,x) typedef char n[(x)?1:-1]\n#define OFF(t,m) ((unsigned long)&(((t*)0)->m))\nCHECK(canvas,sizeof(NNSG2dCharCanvas)==24);CHECK(param,OFF(NNSG2dCharCanvas,param)==16);CHECK(vtable,OFF(NNSG2dCharCanvas,vtable)==20);CHECK(font,sizeof(NNSG2dFont)==8);CHECK(info,sizeof(NNSG2dFontInformation)==20);CHECK(glyph,OFF(NNSG2dFontInformation,pGlyph)==8);CHECK(fontbpp,OFF(NNSG2dFontGlyph,bpp)==6);CHECK(character,sizeof(NNSG2dGlyph)==8);CHECK(widths,sizeof(NNSG2dCharWidths)==3);CHECK(width,OFF(NNSG2dCharWidths,glyphWidth)==1);CHECK(lc,sizeof(LC_INFO)==40);\nint glyph_layout(void);int glyph_layout(void){return sizeof(NNSG2dCharCanvas); }\n');r=compile_probe(row,p,directory/'layout.o')
 if r.returncode:raise ValueError(('Actual font/canvas layout rejected',r.stdout,r.stderr))
 return dict(allPassed=True,canvasBytes=24,fontBytes=8,fontInfoBytes=20,glyphBytes=8,charWidthsBytes=3,sourceOrExecutionCredit=0)

def wrong_source(row,bodies,directory):
 address=int(row['address'],0);source=ROOT/row['source'];text=source.read_text();old,new={0x2087fa8:('cl + bits','cl + bits + 1'),0x20881e8:('cl - 1','cl + 1')}[address];assert old in text;directory.mkdir(parents=True,exist_ok=True);p=directory/source.name;p.write_text(text.replace(old,new,1))
 for h in source.parent.glob('*.h'):shutil.copyfile(h,directory/h.name)
 bad,body=build(p,directory/'build',address,negative=True);changed=dict(bodies);changed[address]=body;observed=run(address,changed,2)
 if observed['modelPassed']or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong G2D C accepted')
 return dict(allPassed=True,caller=row['address'],changedCStatement=dict(original=old,mutant=new),sourceSha256=sha256(p),genuineMutantLinked=True,fullNativeByteEqualityRejected=True,independentPixelModelRejected=True,observed=observed,sourceOrExecutionCredit=0)

def missing_prototype(row,directory):
 directory.mkdir(parents=True,exist_ok=True);header=(ROOT/row['source']).parent/'context_00.h';(directory/'context_00.h').write_bytes(header.read_bytes());p=directory/'probe.c';p.write_text('#include "context_00.h"\nvoid declaration_probe(LC_INFO*);void declaration_probe(LC_INFO*p){native_fn_main_02087fa8(p); }\n');good=compile_probe(row,p,directory/'positive.o');assert good.returncode==0;text,n=re.subn(r'void native_fn_main_02087fa8\s*\([^;]*;','',header.read_text());assert n==1;(directory/'context_00.h').write_text(text);bad=compile_probe(row,p,directory/'negative.o');assert bad.returncode!=0
 return dict(allPassed=True,explicitCallPositive=True,missingDeclarationRejected=True,diagnostic=bad.stdout+bad.stderr,sourceOrExecutionCredit=0)
