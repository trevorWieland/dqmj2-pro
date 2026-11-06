import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import prove_arm7_sdk340_mlme_timeout_callback_scope_20261102 as native
import probe_arm7_sdk342_mlme_timeout_installation_20261102 as installer
from project import ROOT,sha256,write_json,configuration

REPORT=ROOT/'evidence/attempts/arm7-sdk340-mlme-timeout-callback-scope-20261102.json'
INSTALL=ROOT/'evidence/attempts/arm7-sdk342-mlme-timeout-installation-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk341-mlme-timeout-scope-controls'

def validate(report,installation):
    mainpath=ROOT/'extract/arm7/runtime/arm7-main.bin';wrampath=ROOT/'extract/arm7/runtime/arm7-wram.bin';main=mainpath.read_bytes();wram=wrampath.read_bytes();expected,inventory=native.boundaries(main,wram)
    if report['scope']!=expected or report['inventory']!=inventory:raise ValueError('Exact complete three-entry code/pool/parent/reference/namespace scope differs')
    if report['generator']!=Path(native.__file__).name or report['generatorSha256']!=sha256(native.__file__) or report['inputMainSha256']!=sha256(mainpath) or report['inputWramSha256']!=sha256(wrampath):raise ValueError('Frozen witness/input identities changed')
    if report['contextGenerator']!=dict(path=Path(native.context.__file__).name,sha256=sha256(native.context.__file__)):raise ValueError('Native context changed')
    if report['romSha256']!=sha256(configuration()['rom']):raise ValueError('Original ROM changed')
    if report['sourceCredit']!=0 or report['denominatorIncrease']!=0 or report['providers']!=[] or report['prefixBoundaryNormalReturnCredit']!=0:raise ValueError('Scope-only credit/provider limits differ')
    t=report['nativeTrace'];path=(ROOT/t['path']).resolve();path.relative_to(ROOT.resolve())
    if not path.is_file() or sha256(path)!=t['compressedSha256']:raise ValueError('Current native evidence unavailable or changed')
    raw=gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=t['rawSha256']:raise ValueError('Raw native trace differs')
    rows=json.loads(raw);counts={'MLME_ScanTimeOut':432,'MLME_JoinTimeOut':36,'MLME_MeasChanTimeOut':36}
    if len(rows)!=3 or {r['name']:len(r['cases'])for r in rows}!=counts:raise ValueError('Complete per-entry physical domain missing')
    for row in rows:
        if row['actualOwnReturns']!=counts[row['name']]or row['actualSeparateApiReturns']!=counts[row['name']]or not row['allPassed']:raise ValueError('Own/API return counts differ')
        for c in row['cases']:
            if not c['passed']or not all(c['checks'].values())or not c['actualOwnReturn']['actualReturn']or not c['independentTailApiReturn']['actualReturn']or c['sourceCredit']!=0:raise ValueError('Actual return/independent state evidence failed')
        if row['actualSetupReturns']!=sum(c['setupReturns']for c in row['cases']):raise ValueError('Setup returns conflated')
    summaries=[{k:v for k,v in r.items()if k!='cases'}for r in rows]
    if report['results']!=summaries or report['totalActualOwnReturns']!=504 or report['totalActualIndependentApiReturns']!=504:raise ValueError('Measured callback totals differ')
    if installation['generatorSha256']!=sha256(installer.__file__)or installation['scopeGeneratorSha256']!=sha256(native.__file__)or installation['sourceCredit']!=0 or installation['providers']:raise ValueError('Complete original installer proof identity differs')
    if installation['actualParentTaskReturns']!=24 or installation['actualDirectTimeoutInstallerReturns']!=12 or installation['qualifiedInstalledPointers']!=36 or len(installation['results'])!=36:raise ValueError('Task returns and direct installer returns must remain separate')
    for r in installation['results']:
        e=next(e for e in native.ENTRIES if e['name']==r['name'])
        if not r['passed']or r['error']is not None or not r['result']['actualReturn']or r['installedWord']!=hex(e['address'])or not r['observedOriginalTimeoutCalls']or r['observedOriginalTimeoutCalls'][-1]['arguments'][1]!=e['address']or r['postFaultStateCredited']:raise ValueError('Actual producer/callback store witness missing')
    return dict(callbackEntries=3,existingInitializedBytes=204,actualCallbackReturns=504,independentTailApiReturns=504,actualParentTaskReturns=24,directOriginalInstallerReturns=12,providers=0,sourceCredit=0,denominatorIncrease=0)

def main():
    for p in(native.__file__,installer.__file__):
        r=subprocess.run([sys.executable,p],cwd=ROOT.parent,capture_output=True,text=True,timeout=120)
        if r.returncode:raise ValueError(r.stdout+r.stderr)
    report=json.loads(REPORT.read_text());installation=json.loads(INSTALL.read_text());positive=validate(report,installation);controls=[]
    def reject(name,mutate,which='scope'):
        a=copy.deepcopy(report);b=copy.deepcopy(installation);mutate(a if which=='scope'else b)
        try:validate(a,b)
        except Exception as exc:controls.append(dict(name=name,rejected=True,error=type(exc).__name__+':'+str(exc)));return
        raise ValueError('Negative control passed:'+name)
    for field,value in[('processor','arm9'),('program','utility-child'),('module','arm7-wram'),('mode','thumb'),('address','0x27ed414'),('bytes',96),('instructionBytes',88),('literalBytes',4),('targetSha256','0'*64),('parentSha256','0'*64),('literalWords',['0x380fff0','0x37f8598']),('configuredOverlaps',[{'address':'0x27ed410'}]),('defaultCanonicalEntryAbsent',False)]:reject('wrong-qualified-'+field,lambda r,f=field,v=value:r['scope'][0].__setitem__(f,v))
    reject('missing-entry',lambda r:r['scope'].pop());reject('duplicate-entry',lambda r:r['scope'].append(r['scope'][0]));reject('wrong-input-module',lambda r:r.__setitem__('inputMainSha256','0'*64));reject('wrong-generator',lambda r:r.__setitem__('generatorSha256','0'*64));reject('wrong-inventory',lambda r:r['inventory'].__setitem__('sha256','0'*64));reject('missing-native-product',lambda r:r['nativeTrace'].__setitem__('path','work/arm7-bulk-20261030/sdk341-mlme-timeout-scope-controls/missing.gz'));reject('wrong-native-product',lambda r:r['nativeTrace'].__setitem__('compressedSha256','0'*64));reject('wrong-raw-product',lambda r:r['nativeTrace'].__setitem__('rawSha256','0'*64));reject('invented-source-credit',lambda r:r.__setitem__('sourceCredit',204));reject('invented-denominator',lambda r:r.__setitem__('denominatorIncrease',204));reject('provider-introduced',lambda r:r['providers'].append('AddTask'));reject('prefix-as-return',lambda r:r.__setitem__('prefixBoundaryNormalReturnCredit',1));reject('inflated-own-count',lambda r:r.__setitem__('totalActualOwnReturns',1008));reject('false-complete-parent-count',lambda r:r.__setitem__('actualParentTaskReturns',36),'install');reject('missing-installer-record',lambda r:r['results'].pop(),'install');reject('wrong-installed-pointer',lambda r:r['results'][0].__setitem__('installedWord','0x27ed414'),'install');reject('fault-state-credit',lambda r:r['results'][0].__setitem__('postFaultStateCredited',True),'install');reject('installer-return-missing',lambda r:r['results'][0]['result'].__setitem__('actualReturn',False),'install')
    t=report['nativeTrace'];rows=json.loads(gzip.decompress((ROOT/t['path']).read_bytes()));rows[0]['cases'][0]['checks']['independentAllNonstackMemory']=False;raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode();bad=gzip.compress(raw,mtime=0);WORK.mkdir(parents=True,exist_ok=True);out=WORK/'wrong-native-case.gz';out.write_bytes(bad)
    reject('hash-consistent-failed-native-case',lambda r:r.__setitem__('nativeTrace',dict(path=out.relative_to(ROOT).as_posix(),compressedSha256=sha256(out),rawSha256=hashlib.sha256(raw).hexdigest())))
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),scopeReport=dict(path=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT)),installerReport=dict(path=INSTALL.relative_to(ROOT).as_posix(),sha256=sha256(INSTALL)),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,sourceCredit=0,defaultNamespaceAndDataGuardsUnchanged=True);write_json(ROOT/'evidence/verification/arm7-sdk341-mlme-timeout-scope-controls-20261102.json',result);print(json.dumps(dict(positive=positive,controls=len(controls))),flush=True)

if __name__=='__main__':main()
