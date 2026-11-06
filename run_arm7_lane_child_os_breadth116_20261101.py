import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path
import audit_arm7_bulk_20261030 as inventory
import arm7_host_pxi_three_word_context_20261101 as typed_pxi
import arm7_host_callee_word_context_v3_20261101 as typed_io
import draft_arm7_bulk_memory_widths_20261031_v1 as driver
import source_word_inputs_20261031 as words
from capstone import CS_GRP_CALL
from project import ROOT,sha256,write_json
BATCH='lane-child-os-breadth116-20261101'
WORK=ROOT/'work/arm7-bulk-20261030'/BATCH
SNAPSHOT=ROOT/'evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'
import audit_arm7_lane_scope107_20261101 as qualified
CATALOGUE=ROOT/'evidence/verification/source-word-inputs83-20261031.json'
HINTS=ROOT/'provenance/arm7-lane-predicate-hints-20261030.json'
PENDING=((0x037fb488,0x310),(0x037fc468,164))


def context(program,specs):
    driver.configure(specs,program)
    hints=json.loads(HINTS.read_text())
    analyzer=ROOT/'arm7_predicate_abi_20261030_v3.py'
    if sha256(analyzer)!=hints['analyzerSha256']:raise ValueError('Frozen predicate analyzer changed')
    for row in hints['functions']:
        if row['program']==program and row['analysis']['prototypeHintUsable']:
            driver.child.ARGUMENTS['arm7'][int(row['address'],0)]=row['newArgumentCountHypothesis']

    typed_pxi.apply(driver.child,program)
    typed_io.apply(driver.child,program)


def protects(spec,accepted):
    address=spec['address'];end=address+spec['bytes']
    for row in accepted:
        if row['processor']!='arm7' or (row['program'] or '')!=spec['program'] or row['module']!=spec['module']:continue
        first=int(str(row['address']),0);size=row.get('bytes')
        if type(size)is int and size>0 and first<end and address<first+size:return True
        if not(type(size)is int and size>0)and address<=first<end:return True
    if spec['program'] and any(a<end and address<a+n for a,n in ((0x027e944c,48),(0x027eadb8,92))):return True
    return not spec['program'] and any(a<end and address<a+n for a,n in PENDING)


def worker(index):
    queue=json.loads((WORK/'queue.json').read_text());pin=queue['queue'][index]
    specs=[x for x in inventory.specs() if x['program']==pin['program'] and x['mode']=='arm']
    spec=next(x for x in specs if x['module']==pin['module'] and x['address']==int(pin['address'],0))
    if spec['bytes']!=pin['bytes'] or spec['inputModuleSha256']!=pin['inputModuleSha256']:raise ValueError('Queued native identity changed')
    context(spec['program'],specs)
    directory=WORK/spec['module']/f"{spec['address']:08x}";directory.mkdir(parents=True,exist_ok=True)
    import match_runtime
    match_runtime.WORK=directory/'isolated-runtime'
    result=driver.draft(spec,BATCH,spec['program']);result['prototypeViewsAreNotProof']=True;result['qualifiedExistingCalleeContext']=[typed_pxi.apply(driver.child,spec['program']),typed_io.apply(driver.child,spec['program'])]
    write_json(directory/'result.json',result)


def invoke(index,row):
    directory=WORK/row['module']/f"{int(row['address'],0):08x}";directory.mkdir(parents=True,exist_ok=True)
    call=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(index)],cwd=ROOT,capture_output=True,text=True,timeout=240)
    (directory/'stdout.txt').write_text(call.stdout,encoding='utf-8');(directory/'stderr.txt').write_text(call.stderr,encoding='utf-8')
    if call.returncode:return dict(identity=row,failure=call.stderr,sourceCredit=0)
    return json.loads((directory/'result.json').read_text())


def summary(rows):
    return dict(processed=len(rows),drafted=sum(any(v.get('source') for v in r.get('variants',[])) for r in rows),
        compilable=sum(any(v.get('initialCompilerProbe',{}).get('compiledBytes') is not None for v in r.get('variants',[])) for r in rows),
        withWordHints=sum(any(v.get('selectedCWordInputHints') for v in r.get('variants',[])) for r in rows),
        relocationOnlyCandidates=sum(any(v.get('initialCompilerProbe',{}).get('relocationOnlyCandidate') for v in r.get('variants',[])) for r in rows),
        acceptedFunctions=0,sourceCredit=0)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=int);args=parser.parse_args()
    if args.worker is not None:worker(args.worker);return
    if (WORK/'queue.json').exists():raise ValueError('Refusing to restart an existing connected campaign')
    accepted=json.loads(SNAPSHOT.read_text())['functions']
    selected=[]
    for spec in inventory.specs():
        if spec['module']!='utility-child-arm7-wram'or spec['mode']!='arm'or spec['bytes']<32 or not 0x037f8800<=spec['address']<0x037fc000:continue
        if any(qualified.overlaps(accepted,('arm7',spec['program'],spec['module'],mode,spec['address'],spec['bytes']))for mode in('arm','thumb')):continue
        selected.append(dict(spec,selectionReason='Unresolved child ARM7 OS/utility ordinary-logic-sized region after prior accepted intervals',hintedEmptyCalleeViews=0))
    selected.sort(key=lambda x:x['address'])
    if not 20<=len(selected)<=40:raise ValueError('Connected queue count outside bounded breadth range')
    rows=[{key:value for key,value in x.items()if key!='instructions'}for x in selected]
    for row in rows:row['address']=hex(row['address'])
    WORK.mkdir(parents=True,exist_ok=True)
    write_json(WORK/'queue.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),queue=rows,
        inputs=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in(SNAPSHOT,HINTS,ROOT/'audit_arm7_lane_scope107_20261101.py',ROOT/'draft_arm7_bulk_memory_widths_20261031_v1.py',ROOT/'arm7_predicate_abi_20261030_v3.py',ROOT/'arm7_host_pxi_three_word_context_20261101.py',typed_pxi.REFERENCE,ROOT/'arm7_host_callee_word_context_v3_20261101.py',typed_io.REFERENCE)],
        functions=len(rows),nativeBytes=sum(x['bytes']for x in rows),acceptedSnapshotCohort=json.loads(SNAPSHOT.read_text())['acceptedCohort'],
        originalBoundariesAndAllInterfacesHypotheses=True,heldIdentitiesExcluded=[],acceptedByteOverlapsExcludedAcrossBothModes=True,sourceCredit=0))
    print(json.dumps(dict(status='running',functions=len(rows),nativeBytes=sum(x['bytes'] for x in rows),hintedEmptyViews=sum(x['hintedEmptyCalleeViews'] for x in rows),compilerSubprocessLimit=2)),flush=True)
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs={pool.submit(invoke,index,row):row for index,row in enumerate(rows)}
        for future in concurrent.futures.as_completed(jobs):
            try:result=future.result()
            except Exception as error:result=dict(identity=jobs[future],failure=str(error),sourceCredit=0)
            results.append(result);write_json(WORK/'progress.json',dict(summary=summary(results),results=results,sourceCredit=0))
            print(json.dumps(summary(results)),flush=True)
    write_json(WORK/'results.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),summary=summary(results),results=results,
        allInterfacesHypotheses=True,fullLinkNativeAndModuleProofStillRequired=True,sourceCredit=0))


if __name__=='__main__':main()
