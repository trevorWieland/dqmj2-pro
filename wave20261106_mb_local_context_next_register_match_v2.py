import hashlib,re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_mb_local_context_next_register_build import SOURCE,WORK,NAME,ADDRESS,SIZE,COMPILER,build
from wave20261106_mb_local_context_next_register_fixtures import prove as fixtures
from wave20261106_mb_local_context_next_register_controls import prove as controls
LANE=ROOT/'evidence/lanes/parallel-wave20261106/mb-local-context-next/register-packet'
INPUT=LANE/'inputs-v2.json'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen Register input differs',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('Register ROM identity differs')
 item,=inputs['entries']
 claim=read_json(ROOT/inputs['scopeClaim']['path']);owned=next(r for r in claim['claimedFunctions']if r['id']==item['id']);symbols=(ROOT/'config/arm9/symbols.txt').read_text();relocs=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
 if owned['targetSha256']!=item['targetSha256']or owned['bytes']!=SIZE or owned['canonicalInventoryRecord']not in symbols:raise ValueError('Register admitted native span differs')
 if not all(r in relocs for r in owned['originalRelocationRecords']):raise ValueError('Original Register native relocation identity changed')
 for p in[SOURCE/'register.c',*sorted(SOURCE.glob('context_*.h'))]:
  text=p.read_text()
  if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Register ordinary-C source policy differs')
 obj,record,proof,body=build();link=proof['realLink'];digest=hashlib.sha256(body).hexdigest()
 if digest!=item['targetSha256']or record['bytes']!=SIZE:raise ValueError('Complete native Register extent differs')
 dependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(SOURCE.glob('context_*.h'))]
 if item['sourceSha256']!=sha256(SOURCE/'register.c')or item['sourceDependencies']!=dependencies or item['originalObjectRelocations']!=record['relocations']:raise ValueError('Frozen Register source or relocation contract differs')
 model=fixtures(body);negative=controls();bindings={}
 for pin in link['bindingOnlyProbes']+link['dataBindings']:bindings[pin['name']]={k:pin[k]for k in['program','processor','module','mode','kind','address']}
 measured=[]
 for r in record['relocations']:
  retained=r['symbol']=='.bss';target='0x20e68a4'if retained else bindings[r['symbol']]['address'];measured.append(dict(**r,target=target,addend=r['explicitAddend'],binding='retained-source-local-section'if retained else'measured-original-native-entry',originalNativeWitness=hex(ADDRESS+r['offset'])))
 if measured!=item['relocations']:raise ValueError('Frozen Register measured relocation contract differs')
 mode_probes=[]
 for p in link['bindingOnlyProbes']:
  output=ROOT/p['object'];mode_probes.append(dict(**p,initializedCodeBytes=0,linkedInitializedOutputBytes=0))
 real=dict(link);real.update(exactCallerBytes=True,sourceSha256=item['sourceSha256'],sourceObjectSha256=sha256(obj),nativeSpanSha256=digest,linkedCallerSha256=digest,wholeCompilerObjectRetainedWithoutSplit=True,splitPreservesRelocationTypesAddendsAndEncodedHBits=True,originalRelocations=record['relocations'],bindingOnlyProbes=mode_probes,calleeCodeOrSourceCredit=0,wholeModuleLinked=False)
 row=dict(name=NAME,sourceSymbol=NAME,nativeAlias='func_02015c70',program='',processor='arm9',module='main',mode='arm',address=hex(ADDRESS),bytes=SIZE,compiledBytes=record['bytes'],matchingBytes=SIZE,matchingBytesScope='Complete genuine MW-linked656B native ARM span',exactAfterDeclaredRelocation=True,targetSha256=digest,outputSha256=digest,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),source=item['source'],sourceSha256=item['sourceSha256'],sourceDependencies=dependencies,compilerPath=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=proof['compiler']['compilerSha256'],compilerFlags=proof['compiler']['flags'],relocations=measured,sectionIndex=record['symbol']['st_shndx'],sectionOffset=record['symbol']['st_value'],nativeSymbolEntries=bindings,realLink=real,linked=False,sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=SIZE,justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=inputs['sourceProvenance'],sourceOwnedLocalStorage=dict(**record['sourceLocal'],sourceSection='.bss',sourceSectionType='SHT_NOBITS',sourceSectionBytes=1,sourceSectionAlignment=1,nativeAddress='0x20e68a4',initializedByteCredit=0),sourceUnitConsumption='Unmodified whole compiler object with exactly one656B text function and its one-byte function-local BSS definition. Shared full-object consumer qualification remains mandatory.',actualNativeAndSourceCallerReturns=2*model['actualReturnsPerNativeOrSource'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,portableHostExecutionProven=False)
 closure=code_closure([Path(__file__).name]);limits=['Only complete Register656 ordinary-C code is proposed. Its genuine one-byte function-local static is retained as STB_LOCAL in source-generated SHT_NOBITS storage, with0initialized-byte credit. No serializer, instruction/object patches, local-to-ABS rebinding, synthetic storage aliases, receiver storage or supplied executable objects.','Intentional source TU-boundary change: complete published Register body/static byte are retained; original private MakeDownload helper is now a typed external declaration before compilation and binds to its already accepted canonical mainARM entry. Existing helper sources/choices stay unchanged and earn0new credit.','24bounded cases give48native/source runs:18early returns and6stops per side before MakeDownload. Independent capacity/started/duplicate/first-slot models, all GPR/CPSR/stack/ordered reads/writes and12actual-target layout assertions pass. Original IRQ helpers and IsStarted bodies execute as native oracles with0credit.','No MakeDownload/MakeBlock/GameInfo/list/task provider body executes in fixtures. Full registration success, update increment/wrap execution, IRQ hardware behavior, MB/network/device/service/game/portable-host execution and complete imported-callee ABI/type recovery remain unproved. Published MB_AddGameInfo void declaration is intentional; its existing accepted source return declaration remains explicit interface debt.','Original splitter rejection is retained as a negative control. Shared module/symbol/native BSS boundary qualification and original regression gates remain required; this isolated worker report does not assert module-ready or acceptance.']
 report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=[row],matchedFunctions=1,matchedBytes=SIZE,ordinaryCBytes=SIZE,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,boundedCallerModels=model,negativeEvidence=negative,sourceUnitConsumerEvidence=proof,abiInterfaceEvidence=[dict(path=(LANE/'interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'interface.json'))],generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,sourceCreditPendingSharedAcceptance=True,limits=limits)
 write_json(LANE/'match.json',report);print('Register656;24cases/48runs;full source object+BSS1;all controls passed',flush=True)

if __name__=='__main__':main()
