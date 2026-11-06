import gzip
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
CLANG_SHA='6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA='b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
DLLTOOL_SHA='d2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'
RUNNER='ports/windows-native/descriptor412_runner.c'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 assert sys.platform=='win32';native=json.loads((ROOT/'evidence/application/save-core-descriptor411-20261102.json').read_text());sidecar=ROOT/native['sidecar']['path'];raw=gzip.decompress(sidecar.read_bytes());assert sha(sidecar.read_bytes())==native['sidecar']['sha256'] and sha(raw)==native['sidecar']['caseSha256'];cases=json.loads(raw);items=json.loads((ROOT/'evidence/lanes/save-core/descriptor411-identities-20261102.json').read_text())['zeroCreditMigrations'];indices={x['address']:i for i,x in enumerate(items)};payload=bytearray(struct.pack('<II',0x4A324411,len(cases)))
 def digest(wrong):
  value=2166136261
  for case in cases:
   row=case['wrong' if wrong else 'original'];seen_index=0 if wrong else case['index']
   for word in (row['returnWord'],seen_index,row['arguments'][0]):value=(value^word)*16777619&0xFFFFFFFF
  return value
 for case in cases:
  n=case['original'];payload.extend(struct.pack('<6I',indices[case['entry']],case['index'],case['level'],n['returnWord'],n['arguments'][0],0))
 local=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';fallback=ROOT.parents[1]/'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';tools=local if local.is_dir() else fallback;clang,linker,dlltool=[tools/n for n in ('clang.exe','ld.lld.exe','llvm-dlltool.exe')];assert [sha(p.read_bytes()) for p in (clang,linker,dlltool)]==[CLANG_SHA,LINKER_SHA,DLLTOOL_SHA];folder=ROOT/'work/save-core/descriptor412';folder.mkdir(parents=True,exist_ok=True);steps=[]
 def run(command,data=None,expected=0):
  result=subprocess.run(list(map(str,command)),cwd=ROOT,input=data,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120);steps.append(dict(command=list(map(str,command)),exitCode=result.returncode,stdoutSha256=sha(result.stdout),stderr=result.stderr.decode(errors='replace')));assert result.returncode==expected,steps[-1];return result
 definition=folder/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nWriteFile@20\nReadFile@20\n');run([dlltool,'-m','i386','-k','-d',definition,'-l',folder/'kernel32.lib'])
 def compile_source(source,label,defines=()):
  obj=folder/(label+'.obj');run([clang,'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/Brepro','/GS-','/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-stack-protector','/clang:-fno-strict-aliasing','/c',ROOT/source,'/Fo'+str(obj),*defines]);assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0;return obj
 runner=compile_source(RUNNER,'runner');helpers=[compile_source('src/runtime/runtime08/native_main_020449d4.c','lookup',['-Dnative_main_020449d4=descriptor_lookup_impl']),compile_source('src/runtime/runtime08/native_main_02044e18.c','scale',['-Dnative_main_02044e18=descriptor_scale_impl'])];builds=[];receipts=[]
 for wrong in (False,True):
  sources=[('nonmatching/save-core/20261102-descriptor411-controls/'+Path(x['source']).name) if wrong else x['source'] for x in items];objects=[compile_source(source,str(wrong)+'-'+str(i)) for i,source in enumerate(sources)];exe=folder/('wrong.exe' if wrong else 'preferred.exe');run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry','/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',"/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(exe),*objects,runner,*helpers,folder/'kernel32.lib']);binary=exe.read_bytes();assert b'asInvoker' in binary;result=run([exe],bytes(payload),42 if wrong else 0);receipt=list(struct.unpack('<8I',result.stdout));expected_errors=1116 if wrong else 0;assert receipt==[0x4A324412,1,1152,expected_errors,1152,1152,1152,digest(wrong)],receipt;receipts.append(receipt);builds.append(dict(wrong=wrong,sources=[dict(path=s,sha256=sha((ROOT/s).read_bytes())) for s in sources],binarySha256=sha(binary),objects=[sha(p.read_bytes()) for p in objects]))
 report=dict(schema=1,sourceCredit=0,actualPreferredWindowsReturns=1152,actualWrongWindowsReturns=1152,wrongRejects=1116,wrongPositiveControls=36,actualLookupCAndScaleCReturns=4608,suppliedFinalCalls=2304,nativeCaseSha256=native['sidecar']['caseSha256'],payloadSha256=sha(bytes(payload)),runner=dict(path=RUNNER,sha256=sha((ROOT/RUNNER).read_bytes())),helperSources=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in ('src/runtime/runtime08/native_main_020449d4.c','src/runtime/runtime08/native_main_02044e18.c')],receipts=receipts,builds=builds,steps=steps,generatorSha256=sha(Path(__file__).read_bytes()),tools=dict(clang=CLANG_SHA,linker=LINKER_SHA,dlltool=DLLTOOL_SHA),limits=['Actual PE32 process executes six unchanged typed wrapper C sources,existing24B lookup C and28B scale C. Observer adapters record helper arguments;onlyfinal7B790 computation issupplied. No ROM code enters Windows process;synthetic backing only.','The domain is32 bounded100-byte records withfieldvalues1..999 andlevels0..100;lookup pointer arithmetic andsigned shifts staywithin testeddefined range. This establishes forwardingandboundedCinterop,notfinalstat formulas,gameeligibility,Android execution orwholeWindowsgame.','Six primaries andtwo existing helper C files arepreserved unchanged;newalternatives zero additional executablecredit. Native read-footprint rejectionatindex27 corresponds toWindows observedlookup argument despiteequal fieldvalue.']);p=ROOT/'evidence/ports/save-core-descriptor-windows412-20261102.json';p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(preferredWindowsReturns=1152,wrongWindowsReturns=1152,rejects=1116,positives=36,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
