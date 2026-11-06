import ctypes
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from check_save_core_draw_windows353_20261102 import CLANG_SHA,LD_SHA
SOURCE='nonmatching/save-core/20261102-record-width355/raw_forwarded/source.c'
STORAGE='ports/windows-native/record357_storage.c'
LIBRARY='src/mechanics_save/library.c'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def generate(folder,wrong):
 text=(ROOT/SOURCE).read_text();body=text[text.index('u32 native_main_0206c88c'):];body_hash=sha(body[body.index('{'):].encode())
 globals=re.findall(r'^extern (?:u8|s8|ObservedFields_021c4af4) (native_data_[0-9a-f]+)(?:\[\])?;$',text,re.M);assert len(globals)==8
 text=re.sub(r'^extern (?:u8|s8|ObservedFields_021c4af4) native_data_[0-9a-f]+(?:\[\])?;\n','',text,flags=re.M)
 macros=['extern unsigned char record_context[];']
 for name in globals:
  offset=int(name.removeprefix('native_data_'),16)-0x021C4AF4
  macros.append('#define '+name+(' (*(ObservedFields_021c4af4 *)(record_context))' if offset==0 else f' (record_context+{offset})'))
 text='\n'.join(macros)+'\n'+text
 if wrong:text=text.replace('u32 arg1, u32 arg2, s32 arg3','u32 arg1, s8 arg2, s32 arg3')
 assert text[text.index('u32 native_main_0206c88c'):].split('{',1)[1]==body.split('{',1)[1]
 text+='\nu32 record_call(u32 a0,u32 a1,u32 a2,s32 a3,s32 a4) { return native_main_0206c88c(a0,a1,a2,a3,(s8)a4); }\n'
 source=folder/'mapped_parent.c';source.write_text(text)
 library=(ROOT/LIBRARY).read_text();prefix=library[:library.index('u32 saved_native_id_alias')];function=re.search(r'^u8 saved_native_category\([^\n]*$',library,re.M).group();helper=folder/'selected_category.c';helper.write_text(prefix+function+'\n')
 assert 'u16 category:4;' in prefix and ' / 3;' in function
 return [source,helper,ROOT/STORAGE],dict(source=SOURCE,sourceSha256=sha((ROOT/SOURCE).read_bytes()),unchangedBodySha256=body_hash,library=LIBRARY,librarySha256=sha((ROOT/LIBRARY).read_bytes()),libraryFunction=function,globals=globals,wrongNarrowThirdFormal=wrong)


def build(key,wrong):
 local=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';fallback=ROOT.parents[1]/'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';tools=local if local.is_dir() else fallback;clang,ld=tools/'clang.exe',tools/'ld.lld.exe';assert sha(clang.read_bytes())==CLANG_SHA and sha(ld.read_bytes())==LD_SHA
 folder=ROOT/'work/save-core/record-windows357'/key;folder.mkdir(parents=True,exist_ok=True);paths,adaptation=generate(folder,wrong);objects=[];rows=[]
 for index,path in enumerate(paths):
  obj=folder/(str(index)+'.obj');command=[str(clang),'--driver-mode=cl','--target=x86_64-pc-windows-msvc','/TC','/std:c11','/O2','/Brepro','/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-stack-protector','/clang:-fno-strict-aliasing','/c',str(path),'/Fo'+str(obj)];p=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert p.returncode==0,p.stdout+p.stderr;assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0;objects.append(str(obj));rows.append(dict(source=path.relative_to(ROOT).as_posix(),sourceSha256=sha(path.read_bytes()),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha(obj.read_bytes()),command=command))
 dll=folder/'record.dll';command=[str(ld),'-flavor','link','/dll','/noentry','/nodefaultlib','/machine:x64','/timestamp:0','/out:'+str(dll),'/export:record_call','/export:record_reset',*['/export:'+n+',DATA' for n in ('record_context','record_words','record_metric_calls','record_lower_calls')],*objects];p=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert p.returncode==0,p.stdout+p.stderr
 m=ctypes.CDLL(str(dll));m.record_reset.argtypes=[ctypes.c_uint32]*5;m.record_reset.restype=None;m.record_call.argtypes=[ctypes.c_uint32]*3+[ctypes.c_int32]*2;m.record_call.restype=ctypes.c_uint32
 return m,dict(objects=rows,binary=dll.relative_to(ROOT).as_posix(),binarySha256=sha(dll.read_bytes()),linkCommand=command,adaptation=adaptation)


def invoke(m,p):
 m.record_reset(p['species'],p['nibble'],p['index'],p['y'],p['base']);ret=m.record_call(p['species'],p['style'],p['kind'],p['position'],p['flag'])
 return dict(returnWord=ret,contextSha256=sha(bytes((ctypes.c_uint8*0x1000).in_dll(m,'record_context'))),provider=[list((ctypes.c_uint32*7).in_dll(m,'record_words'))],metricCalls=ctypes.c_uint32.in_dll(m,'record_metric_calls').value,lowerCalls=ctypes.c_uint32.in_dll(m,'record_lower_calls').value)


def main():
 path=ROOT/'evidence/application/save-core-record-width356-20261102.json';native=json.loads(path.read_text());s=native['sidecar'];raw=gzip.decompress((ROOT/s['path']).read_bytes());assert sha(raw)==s['caseSha256'];cases=json.loads(raw);assert len(cases)==512
 good,gb=build('preferred',False);bad,bb=build('wrong-narrow-kind',True);rows=[];rejects=positives=0
 for vector in cases:
  p=vector['profile'];gold=vector['result'];expected=dict(returnWord=gold['returnWord'],contextSha256=sha(bytes.fromhex(gold['context'])),provider=gold['provider'],metricCalls=3,lowerCalls=1);actual=invoke(good,p);wrong=invoke(bad,p);assert actual==expected,(p,actual,expected);rejects+=wrong!=expected;positives+=wrong==expected;rows.append(dict(profile=p,result=actual,wrong=wrong,wrongRejected=wrong!=expected))
 assert (rejects,positives)==(384,128)
 raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-record-windows357-20261102.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));out=dict(schema=1,sourceCredit=0,netNewFunctions=0,netNewBytes=0,preferred=gb,wrong=bb,pairs=512,actualPublicCalls=1024,recoveredParentBodyExecutions=1024,actualRecoveredCategoryCalls=3072,suppliedLowerCalls=1024,wrongRejects=rejects,wrongPositives=positives,nativeCaseSha256=s['caseSha256'],sidecar=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),caseSha256=sha(raw)),generatorSha256=sha(Path(__file__).read_bytes()),limits=['Actual Windows64 C calls reuse unchanged preferred function body and unchanged selected category function/prefix. The port maps eight original globals into one4096-byte backing using explicit data-view macros after removing their extern declarations;it is a platform adapter,not native source matching or game execution.', 'Synthetic32-record descriptor backing and seven-word6D2E0 provider follow the native356 matrix. All512 preferred effects/providerwords/results equal the original native golden. Physical high bits of incoming third word are consumed by the lower call despite a low8 store to the record.', 'Complete wrong source changes only third formal to signed8;its body is unchanged.384 vectors reject and128 canonical127 inputs remain positives. This is source-language ABI evidence;the old ARM compiler could preserve rawR2 despite a guessed signed8 formal.', 'Library bitfield layout is exercised by all16 nibbles and all four bounded species-index profiles;no ROMasset,ordinary caller eligibility,table capacity,bank selection,Windows game or Android execution follows.'])
 path=ROOT/'evidence/ports/save-core-record-windows357-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(publicCalls=1024,categoryCalls=3072,wrongRejects=rejects,positives=positives,sourceCredit=0,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
