import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
CLANG_SHA='6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LD_SHA='b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
SOURCE='src/mechanics_save/20261102_lane_draw_forward/native_main_02061c1c.c'
STORAGE='ports/windows-native/draw353_storage.c'
HELPERS=[('src/runtime/runtime07/native_main_02061dcc.c','native_main_02061dcc=draw_real_61dcc'),('src/runtime/runtime08/native_main_02049ad0.c','native_main_02049ad0=draw_real_49ad0')]


def sha(raw):return hashlib.sha256(raw).hexdigest()


def build(source,key):
 local=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';fallback=ROOT.parents[1]/'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';tools=local if local.is_dir() else fallback
 clang,ld=tools/'clang.exe',tools/'ld.lld.exe';assert sha(clang.read_bytes())==CLANG_SHA and sha(ld.read_bytes())==LD_SHA
 folder=ROOT/'work/save-core/draw-windows353'/key;folder.mkdir(parents=True,exist_ok=True);objects=[];rows=[]
 for index,(path,alias) in enumerate([(source,None),*HELPERS,(STORAGE,None)]):
  obj=folder/(str(index)+'.obj');command=[str(clang),'--driver-mode=cl','--target=x86_64-pc-windows-msvc','/TC','/std:c11','/O2','/Brepro','/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-stack-protector','/clang:-fno-strict-aliasing','/clang:-Wno-deprecated-non-prototype','/clang:-Wno-pointer-to-int-cast']
  if alias:command+=['/D'+alias]
  command+=['/c',str(ROOT/path),'/Fo'+str(obj)];p=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert p.returncode==0,p.stdout+p.stderr;assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0;objects.append(str(obj));rows.append(dict(source=path,sourceSha256=sha((ROOT/path).read_bytes()),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha(obj.read_bytes()),symbolAlias=alias,command=command))
 dll=folder/'draw.dll';exports=['native_main_02061c1c','draw_reset']+[name+',DATA' for name in ['native_data_021b9bd4','native_data_02102a18','draw_seen_index','draw_seen_selector','draw_helper_calls','draw_lower_calls','draw_words']]
 command=[str(ld),'-flavor','link','/dll','/noentry','/nodefaultlib','/machine:x64','/timestamp:0','/out:'+str(dll),*['/export:'+n for n in exports],*objects];p=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert p.returncode==0,p.stdout+p.stderr
 m=ctypes.CDLL(str(dll));m.draw_reset.argtypes=[ctypes.c_int32]*3;m.draw_reset.restype=None;m.native_main_02061c1c.argtypes=[ctypes.c_uint32]+[ctypes.c_int32]*4+[ctypes.c_int8]*2;m.native_main_02061c1c.restype=ctypes.c_uint32
 base=ctypes.addressof((ctypes.c_uint8*0x1000).in_dll(m,'native_data_02102a18'))&0xFFFFFFFF;signed=base-(1<<32) if base&0x80000000 else base;assert -(1<<31)+1536<=signed<=(1<<31)-1537
 return m,base,dict(objects=rows,binary=dll.relative_to(ROOT).as_posix(),binarySha256=sha(dll.read_bytes()),linkCommand=command)


def invoke(m,base,p):
 m.draw_reset(p['left'],p['right'],p['mode']);ret=m.native_main_02061c1c(p['index'],p['x'],p['y'],p['w'],p['h'],p['style'],p['side']);words=list((ctypes.c_uint32*11).in_dll(m,'draw_words'));words[0]=(words[0]-base)&0xFFFFFFFF
 return dict(slotOffset=(ret-base)&0xFFFFFFFF,seenIndex=ctypes.c_uint32.in_dll(m,'draw_seen_index').value,seenSelector=ctypes.c_uint32.in_dll(m,'draw_seen_selector').value,helperCalls=ctypes.c_uint32.in_dll(m,'draw_helper_calls').value,lowerCalls=ctypes.c_uint32.in_dll(m,'draw_lower_calls').value,provider=words,afterSha256=sha(bytes((ctypes.c_uint8*0x280).in_dll(m,'native_data_021b9bd4'))))


def main():
 assert sys.platform=='win32' and ctypes.sizeof(ctypes.c_void_p)==8
 native=json.loads((ROOT/'evidence/application/save-core-draw-forward352-20261102.json').read_text());s=native['sidecar'];packed=(ROOT/s['path']).read_bytes();raw=gzip.decompress(packed);assert sha(packed)==s['sha256'] and sha(raw)==s['caseSha256'];cases=json.loads(raw)
 wrong=ROOT/'nonmatching/save-core/20261102-draw-forward353-controls/source.c';wrong.parent.mkdir(parents=True,exist_ok=True);text=(ROOT/SOURCE).read_text();assert text.count('native_fn_02061dcc((s32)arg0)')==1;expected=text.replace('native_fn_02061dcc((s32)arg0)','native_fn_02061dcc(0)')
 if wrong.exists():assert wrong.read_text()==expected
 else:wrong.write_text(expected)
 good,base,built=build(SOURCE,'preferred');bad,badbase,wrong_built=build(wrong.relative_to(ROOT).as_posix(),'wrong-zero');native_base=0x02102A18;results=[];rejects=semantic_rejects=0
 for row in cases:
  p,a=row['profile'],row['observed'];actual=invoke(good,base,p);wanted=dict(slotOffset=(a['returnWord']-native_base)&0xFFFFFFFF,seenIndex=p['index'],seenSelector=a['logicalHelperEntries'][1][1],helperCalls=1,lowerCalls=1,provider=list(a['provider']),afterSha256=a['afterSha256']);wanted['provider'][0]=(wanted['provider'][0]-native_base)&0xFFFFFFFF;assert actual==wanted,(p,actual,wanted);control=invoke(bad,badbase,p);rejected=control!=actual;semantic=any(control[k]!=actual[k] for k in ('slotOffset','provider','afterSha256'));rejects+=rejected;semantic_rejects+=semantic;results.append(dict(index=row['index'],profile=p,actual=actual,wrong=control,rejected=rejected,semanticEffectsRejected=semantic))
 assert len(cases)==1024 and rejects==1023 and semantic_rejects==1020
 raw=(json.dumps(results,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-draw-windows353-20261102.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,actualPreferredPublicCalls=1024,actualWrongPublicCalls=1024,totalActualPublicCalls=2048,actualRecoveredHelperCalls=4096,providedLowerCalls=2048,wrongContractRejects=rejects,wrongContractPositives=1024-rejects,wrongSemanticRejects=semantic_rejects,wrongSemanticPositives=1024-semantic_rejects,nativeCaseSha256=s['caseSha256'],preferred=built,wrong=wrong_built,sidecar=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),caseSha256=sha(raw)),generatorSha256=sha(Path(__file__).read_bytes()),limits=['Unchanged reconstructed61C1C,61DCC and49AD0 C bodies execute in Windows64. Passive ABI shims record inputs;only49BE4 lowerUI behavior is supplied. No game/device or Android execution is claimed.', 'The getter returns a raw32-bit address word. Returned/provider addresses are normalized to the DLL global base;they are never dereferenced as truncated Windows64 pointers. Actual base is checked to avoid signed pointer-word addition overflow.', 'A complete typed wrong-zero source has1023 contract rejects/one full positive;four high-word aliases share low-byte output behavior,so semantic output rejection is1020 withfour positives. These counts are distinct.', 'Profiles retain the bounded non-overflow geometry and signed-helper-addition domain of native352. No arbitrary index/scene/renderer state guarantee.'])
 path=ROOT/'evidence/ports/save-core-draw-windows353-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(actualPublicCalls=2048,recoveredHelperCalls=4096,contractRejects=rejects,semanticRejects=semantic_rejects,caseSha256=out['sidecar']['caseSha256'])))


if __name__=='__main__':main()
