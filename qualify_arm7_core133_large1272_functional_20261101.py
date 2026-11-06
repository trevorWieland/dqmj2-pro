import argparse
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import match_runtime
import arm7_core133_large1272_native_20261101 as native
import compile_arm7_core133_large1272_virtual_20261101 as compiler
import match_arm7_main_spi276_20261101 as strict_compiler
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm_const import ARM_INS_BL,ARM_INS_BLX
from project import ROOT,sha256,write_json

INPUT=ROOT/'nonmatching/arm7-bulk/20261101/lane-core133-large1272-functional/profile.json'
WORK=ROOT/'work/arm7-bulk-20261030/core133-large1272-functional'
REPORT=ROOT/'evidence/attempts/arm7-core133-large1272-functional-20261101.json'
PROGRAM='dwc/utility.bin/move/child.srl'

def worker(limit):
    if sha256(INPUT)!='c2ea154e03b9b57038c1e4bf061ac2f2f46c2975d07e48bca4c0e5229330fa43':raise ValueError('Frozen complete source/profile closure changed')
    profile=json.loads(INPUT.read_text());seed=profile['units'][0];source=ROOT/seed['source']
    if sha256(source)!=seed['sourceSha256']:raise ValueError('Original full ordinary-C hypothesis changed')
    for item in [profile['wram'],profile['linker'],dict(path=seed['binary'],sha256=seed['inputModuleSha256']),dict(path=seed['compiler'],sha256=seed['compilerSha256']),dict(path='inputs/game.nds',sha256=profile['romSha256'])]:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Measured ROM/module/tool input changed')
    if (seed['processor'],seed['program'],seed['module'],seed['mode'],int(seed['address'],0),seed['bytes'])!=('arm7',PROGRAM,'utility-child-arm7-main','arm',native.TOP,1272):raise ValueError('Exact original qualified draft identity differs')
    main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/profile['wram']['path']).read_bytes();disassembler=Cs(CS_ARCH_ARM,CS_MODE_ARM);disassembler.detail=True;instructions=list(disassembler.disasm(main[native.TOP-native.MAIN:native.TOP-native.MAIN+1212],native.TOP));calls={int(i.operands[0].imm)&0xffffffff for i in instructions if i.id in(ARM_INS_BL,ARM_INS_BLX)and i.operands and i.operands[0].type==2}
    bindings={};text=source.read_text()
    for line in text.splitlines():
        if not line.startswith('extern '):continue
        match=re.search(r'(native_utility_child_arm7_(arm|data)_([0-9a-f]{8}))\b',line)
        if not match:raise ValueError('Unexpected draft dependency declaration')
        name,kind,address=match.groups();address=int(address,16)
        if kind=='arm'and address not in calls:raise ValueError('Draft callee absent from actual original immediate call references')
        bindings[name]=dict(address=hex(address),mode='arm',kind='function'if kind=='arm'else'data',program=PROGRAM,processor='arm7',sourceCredit=0,sourceAdmissionNotRequested=True)
    try:strict_compiler.compile_unit(seed,source,WORK/'original-strict-refusal',strict=True)
    except ValueError as error:strict_refusal=dict(errorType=type(error).__name__,error=str(error),sourceCredit=0)
    else:raise ValueError('Inexact draft unexpectedly passed unchanged strict source admission')
    body,build=compiler.build(dict(seed,address=hex(native.VIRTUAL)),text,WORK/'source',bindings)
    records=[];counts={};visited=set();scratch_differences={};total_helpers=0
    cases=native.cases()[:limit or None]
    for index,case in enumerate(cases):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if not original['modelPassed']or not compiled['modelPassed']:raise ValueError(dict(index=index,case=case,original=original,compiled=compiled))
        for field in('branch','rawResult','externalWrites','syntheticDataSha256','actualNativeHelperReturns'):
            if original[field]!=compiled[field]:raise ValueError('Original/compiled large1272 semantic state differs:'+field)
        counts[original['branch']]=counts.get(original['branch'],0)+1;visited.update(original['visited']);total_helpers+=original['actualNativeHelperReturns']+compiled['actualNativeHelperReturns']
        for register,(first,second)in enumerate(zip(original['rawRegisters'],compiled['rawRegisters'])):
            if first!=second:scratch_differences[str(register)]=scratch_differences.get(str(register),0)+1
        records.append(dict(case=case,original=original,compiled=compiled))
    prerequisite_controls=[];allocation_case=next(row['case']for row in records if row['original']['branch']=='empty-heap')
    for name,case in [('zero-runtime-word',dict(cases[0],zeroRuntimePointer=True)),('invalid-heap-context',dict(allocation_case,invalidHeapPointer=True))]:
        outcomes=[]
        for candidate in (None,body):
            try:native.run(main,wram,case,0,body=candidate)
            except Exception as error:outcomes.append(dict(errorType=type(error).__name__,error=str(error),actualReturnCredit=0))
            else:raise ValueError('Broken prerequisite acquired supported return credit')
        prerequisite_controls.append(dict(name=name,outcomes=outcomes,sourceCredit=0))
    exhausted=[]
    for candidate in(None,body):
        try:native.run(main,wram,cases[0],0,body=candidate,budget=1)
        except ValueError as error:exhausted.append(dict(error=str(error),actualReturnCredit=0))
        else:raise ValueError('Exhausted instruction budget acquired a return')
    prerequisite_controls.append(dict(name='instruction-budget-exhausted',outcomes=exhausted,sourceCredit=0))
    wrong=[]
    for name,old,new in [('mode-return','return 0xBU;','return 0xCU;'),('length-equality','> 0x204U','>= 0x204U')]:
        if old not in text:raise ValueError('Negative C mutation site missing')
        bad,badbuild=compiler.build(dict(seed,address=hex(native.VIRTUAL)),text.replace(old,new,1),WORK/('wrong-'+name),bindings);returned=rejected=0
        for index,case in enumerate(cases):
            result=native.run(main,wram,case,index,body=bad);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Wrong full C body escaped independent field/return model')
        wrong.append(dict(name=name,actualOwnReturns=returned,independentModelRejections=rejected,build=badbuild))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),profile=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT)),nativeModel=dict(path='arm7_core133_large1272_native_20261101.py',sha256=sha256(ROOT/'arm7_core133_large1272_native_20261101.py')),processor='arm7',program=PROGRAM,module='utility-child-arm7-main',mode='arm',address=hex(native.TOP),bytes=1272,originalCodeBytes=1212,originalLiteralBytes=60,inputModuleSha256=hashlib.sha256(main).hexdigest(),originalFunctionSha256=hashlib.sha256(main[native.TOP-native.MAIN:native.TOP-native.MAIN+1272]).hexdigest(),source=seed['source'],sourceSha256=sha256(source),compiledBytes=len(body),virtualCompiledAddress=hex(native.VIRTUAL),realSourceOnlyBuild=build,supportedCases=len(cases),actualOriginalAndCompiledOwnReturns=2*len(records),actualOriginalAndCompiledNestedNativeReturns=total_helpers,branchCases=counts,nativeOwnInstructionsVisited=sum(native.TOP<=pc<native.TOP+1212 for pc in visited),nativeHelperInstructionsVisited=sum(not native.TOP<=pc<native.TOP+1212 for pc in visited),rawScratchDifferenceCaseCounts=scratch_differences,wrongC=wrong,prerequisiteControls=prerequisite_controls,trace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0),namedBindings=bindings,providerReplacements=[],sourceAdmissionRequested=False,newSourceCredit=0,initializedDenominatorDelta=0,wholeModuleLinked=False,completeFunctionBehaviorProven=False,limitations=['Only mode/active/length/payload rejection and synthetic empty-heap-return paths are supported; success/hardware/concurrent/alias contexts remain unproved','The incoming runtime word and null heap-table entry are disposable synthetic prerequisites, not a native boot/producer/scene claim','Each execution checks ABI, full nonstack memory, ordered externally observable writes and independent raw field/return model; raw scratch/flags/private-frame effects are retained and not claimed identical','Helper storage is original byte scaffolding with zero callee source credit; unused bindings and callee prototypes remain draft hypotheses','The compiled body has a different size and is separately linked at a virtual address; strict source admission and original unknown-symbol/data guards are unchanged'])
    report['unchangedStrictRefusal']=strict_refusal
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),supportedCases=len(cases),actualOwnReturns=2*len(records),nestedReturns=total_helpers,sourceCredit=0)),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');parser.add_argument('--limit',type=int,default=0);args=parser.parse_args()
    if args.worker:worker(args.limit);return
    call=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker','--limit',str(args.limit)],cwd=Path.cwd(),capture_output=True,text=True,timeout=180)
    WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(call.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(call.stderr,encoding='utf-8')
    if call.returncode:raise ValueError(call.stderr[-10000:])
    print(call.stdout.strip(),flush=True)
if __name__=='__main__':main()
