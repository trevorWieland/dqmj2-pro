import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import arm7_core133_large1272_native_20261101 as native
import qualify_arm7_core133_large1272_functional_20261101 as producer
from project import ROOT,sha256,write_json

PINS=producer.INPUT.parent/'generator-pins.json'
REPORT=ROOT/'evidence/attempts/arm7-core133-large1272-functional-controls-20261101.json'

def validate(report):
    profile=json.loads(producer.INPUT.read_text());seed=profile['units'][0]
    if report['generator']!=Path(producer.__file__).name or report['generatorSha256']!=sha256(producer.__file__):raise ValueError('Fresh current producer identity differs')
    for key in('processor','program','module','mode','address','bytes','inputModuleSha256','source','sourceSha256'):
        if report[key]!=seed[key]:raise ValueError('Qualified original/full-source identity differs:'+key)
    if report['profile']['sha256']!=sha256(producer.INPUT)or report['nativeModel']['sha256']!=sha256(native.__file__):raise ValueError('Current profile/model changed')
    if report['newSourceCredit']!=0 or report['initializedDenominatorDelta']!=0 or report['sourceAdmissionRequested']or report['wholeModuleLinked']or report['completeFunctionBehaviorProven']:raise ValueError('Research proof claimed unsupported acceptance')
    source=ROOT/seed['source']
    if not source.is_file()or sha256(source)!=seed['sourceSha256']:raise ValueError('Source-only C input missing or changed')
    build=report['realSourceOnlyBuild'];directory=Path(build['actualLinkerCwd']).resolve()
    if not directory.is_relative_to(producer.WORK)or not build['sourceAdmissionNotRequested']or build['sourceCredit']!=0:raise ValueError('Diagnostic build escaped declared work or requested credit')
    for path,digest in [(ROOT/build['source'],build['sourceSha256']),(ROOT/build['object'],build['objectSha256']),(directory/'linked.elf',build['linkedElfSha256']),(directory/'caller.bin',build['linkedBodySha256'])]:
        if not path.is_file()or sha256(path)!=digest:raise ValueError('Fresh C/object/linked product missing or changed')
    if len((directory/'caller.bin').read_bytes())!=report['compiledBytes']or report['compiledBytes']==report['bytes']:raise ValueError('Inexact functional body extent/credit differs')
    trace=ROOT/report['trace']['path']
    if not trace.is_file()or sha256(trace)!=report['trace']['compressedSha256']:raise ValueError('Native execution product missing or changed')
    raw=gzip.decompress(trace.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=report['trace']['rawSha256']or report['trace']['gzipMtime']!=0:raise ValueError('Native trace raw bytes or deterministic encoding differs')
    records=json.loads(raw)
    if [r['case']for r in records]!=native.cases()or report['supportedCases']!=len(records):raise ValueError('Full supported synthetic input domain changed')
    helpers=0;branches={}
    for row in records:
        for name in('original','compiled'):
            execution=row[name]
            if not execution['actualOwnReturn']or not execution['modelPassed']or not all(execution['modelChecks'].values())or execution['providers']:raise ValueError('Claimed actual return/state/ABI/native-only evidence differs')
            helpers+=len(execution['helpers'])
            if execution['actualNativeHelperReturns']!=len(execution['helpers'])or not all(h['actualReturn']and h['calleeSavedPreserved']for h in execution['helpers']):raise ValueError('Native nested returns were not separately observed')
        for field in('branch','rawResult','externalWrites','syntheticDataSha256','actualNativeHelperReturns'):
            if row['original'][field]!=row['compiled'][field]:raise ValueError('Original/compiled supported effects differ')
        branch=row['original']['branch'];branches[branch]=branches.get(branch,0)+1
    if report['actualOriginalAndCompiledOwnReturns']!=2*len(records)or report['actualOriginalAndCompiledNestedNativeReturns']!=helpers or report['branchCases']!=branches:raise ValueError('Return/state counts do not derive from current trace')
    if set(branches)!={'mode','active','length','payload','encoded-payload','empty-heap'}:raise ValueError('Required supported early branch outcomes absent')
    if {r['name']for r in report['wrongC']}!={'mode-return','length-equality'}or len(report['wrongC'])!=2:raise ValueError('Independent wrong-source controls absent')
    if any(r['actualOwnReturns']!=len(records)or not 0<r['independentModelRejections']<=len(records)for r in report['wrongC']):raise ValueError('Returning wrong-C bodies were not independently rejected')
    if len(report['prerequisiteControls'])!=3 or any(len(r['outcomes'])!=2 or any(x['actualReturnCredit']!=0 for x in r['outcomes'])for r in report['prerequisiteControls']):raise ValueError('Fault/exhaustion was counted as a supported return')
    return dict(cases=len(records),ownReturns=2*len(records),separateNativeHelperReturns=helpers,newSourceCredit=0)

def controls(report):
    results=[]
    changes=[('processor','arm9'),('program',''),('module','arm7-main'),('mode','thumb'),('address','0x27efd40'),('bytes',1268),('inputModuleSha256','0'*64),('source','missing.c'),('sourceSha256','0'*64),('generatorSha256','0'*64),('newSourceCredit',1272),('initializedDenominatorDelta',1272),('sourceAdmissionRequested',True),('wholeModuleLinked',True),('completeFunctionBehaviorProven',True),('supportedCases',207),('actualOriginalAndCompiledOwnReturns',413),('actualOriginalAndCompiledNestedNativeReturns',289),('compiledBytes',1272)]
    for key,value in changes:
        changed=copy.deepcopy(report);changed[key]=value
        try:validate(changed)
        except(ValueError,FileNotFoundError,KeyError)as error:results.append(dict(name=key,error=str(error),rejected=True))
        else:raise ValueError('Mutated research evidence escaped:'+key)
    directory=Path(report['realSourceOnlyBuild']['actualLinkerCwd']);path=directory/'caller.bin';original=path.read_bytes()
    try:
        path.write_bytes(bytes([original[0]^1])+original[1:])
        try:validate(report)
        except ValueError as error:results.append(dict(name='actual-linked-body-bit',error=str(error),rejected=True))
        else:raise ValueError('Corrupted linked body escaped')
    finally:path.write_bytes(original)
    path=ROOT/report['trace']['path'];held=path.with_name('held-native-records.json.gz')
    try:
        path.rename(held)
        try:validate(report)
        except ValueError as error:results.append(dict(name='actual-missing-native-product',error=str(error),rejected=True))
        else:raise ValueError('Missing native execution product escaped')
    finally:
        if held.is_file():held.rename(path)
    return results

def main():
    for row in json.loads(PINS.read_text())['files']:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=row['sha256']:raise ValueError('Complete frozen functional source/tool/model input changed')
    process=subprocess.run([sys.executable,str(Path(producer.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=240)
    if process.returncode:raise ValueError(process.stderr[-8000:])
    report=json.loads(producer.REPORT.read_text());positive=validate(report);negative=controls(report);restored=validate(report)
    if positive!=restored:raise ValueError('Positive functional evidence failed after controls')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReport=producer.REPORT.relative_to(ROOT).as_posix(),inputReportSha256=sha256(producer.REPORT),positive=positive,negativeControls=negative,controlCount=len(negative),restoredPositive=True,newSourceCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),controls=len(negative),**positive)),flush=True)
if __name__=='__main__':main()
