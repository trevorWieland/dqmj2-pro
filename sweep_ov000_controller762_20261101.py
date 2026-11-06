import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
from project import ROOT,sha256,write_json
BASE=ROOT/'nonmatching/overlay-lane/20261101-controller762'
ORIGINAL=ROOT/'nonmatching/overlay-lane/20261101-controller751/02218d30-arm'
COMPILERS=['2.0/base','2.0/sp1p5','2.0/sp1p6','1.2/base']

def prepare():
    if(BASE/'queue.json').exists():raise ValueError('762 queue exists')
    source=(ORIGINAL/'source.c').read_text();header=(ORIGINAL/'context.h').read_text();call='native_fn_0205fc10(native_data_ov000_02245f74, native_fn_ov000_0221930c, native_fn_ov000_0221938c, 0x12, 0x2000, 2, 0)'
    fixed='native_fn_0205fc10((u32)native_data_ov000_02245f74, (u32)native_fn_ov000_0221930c, (u32)native_fn_ov000_0221938c, 0, 0x12, 0x2000, 2, 0)'
    if source.count(call)!=1:raise ValueError('762 constructor call site differs')
    corrected=source.replace(call,fixed);typed=header.replace('extern u32 native_fn_0205fc10();','extern u32 native_fn_0205fc10(u32,u32,u32,u32,u32,u32,s32,u32);')
    variants=[('preserved-seven-word-hypothesis',source,header),('eight-word-native-view',corrected,typed)]
    block=re.search(r'            var_r4 = 0xD;\n            do \{.*?            \} while \(var_r4 != 0\);',corrected,re.S)
    if not block:raise ValueError('762 copy loop differs')
    aggregate=corrected[:block.start()]+'            *(NativeBlock208 *)var_r5 = *(NativeBlock208 *)var_r6;'+corrected[block.end():]
    variants.append(('eight-word-aggregate208',aggregate,typed+'\ntypedef struct NativeBlock208 {u32 words[52];} NativeBlock208;\n'))
    jobs=[]
    for name,text,context in variants:
        directory=BASE/name;directory.mkdir(parents=True,exist_ok=True);(directory/'source.c').write_text(text);(directory/'context.h').write_text(context)
        for compiler in COMPILERS:
            for speed in[False,True]:jobs.append(dict(variant=name,compiler=compiler,speed=speed,extraFlags=[]))
        jobs.append(dict(variant=name,compiler='2.0/base',speed=False,extraFlags=['-O4,p','-ipa','file','-inline','on,noauto','-lang','c99']))
    write_json(BASE/'queue.json',dict(schemaVersion=1,sourceCredit=0,module='ov000',processor='arm9',program='',mode='arm',address='0x02218d30',bytes=1500,jobs=jobs,sourceInput=dict(path=(ORIGINAL/'source.c').relative_to(ROOT).as_posix(),sha256=sha256(ORIGINAL/'source.c')),nativePreparedView=dict(callPc='0x02218DCC',r0='0x02245F74',r1='0x0221930C ARM callback',r2='0x0221938C ARM callback',r3=0,stackWords=[18,8192,2,0],callee='main ARM0x0205FC10',calleeReads=['incomingR3 retained and passed onward','entrySP+0 lowbyte','entrySP+4 word','entrySP+8 signed byte','entrySP+12 word']),semanticCaution='Do not change u8-versus0xFFFFFFFF comparison to255: native02219218 LDRB comparesagainstR4=-1,so the skip is unreachable for stable bytes. This exact native behavior is preserved.'))

def one(index):
    import match_runtime as c
    from link_runtime_unit import validate
    from recover_linked_runtime import qualified_bindings
    job=json.loads((BASE/'queue.json').read_text())['jobs'][index];source=BASE/job['variant']/'source.c';directory=ROOT/'work/ol762'/str(index);c.WORK=directory/'compile';c.FLAGS+=job['extraFlags'];compiler=ROOT/'tools/mwccarm/mwccarm'/job['compiler']/'mwccarm.exe';rows,unused=c.compare(source,'ov000','2','off',job['speed'],compiler=compiler);result=dict(job=job,sourceCredit=0,results=[])
    for row in rows:
        proof={}
        if not row.get('compileFailed'):
            try:proof=validate(row,qualified_bindings(row),directory/'link')
            except ValueError as error:proof=error.args[0]
        result['results'].append(dict(source=row,genuineLink=proof))
    write_json(BASE/f'job-{index:02d}.json',result)

def run():
    jobs=json.loads((BASE/'queue.json').read_text())['jobs'];completed=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        pending={pool.submit(subprocess.run,[sys.executable,__file__,'--one',str(index)],cwd=ROOT,capture_output=True,text=True,timeout=150):index for index in range(len(jobs))}
        for future in concurrent.futures.as_completed(pending):
            index=pending[future];process=future.result();result=json.loads((BASE/f'job-{index:02d}.json').read_text())if process.returncode==0 else dict(job=jobs[index],failure=process.stderr[-3000:]);completed.append(result)
    write_json(ROOT/'evidence/attempts/ov000-controller762-native-eight-word-view-20261101.json',dict(schemaVersion=1,sourceCredit=0,uniqueDraftedNativeFunctions=1,uniqueDraftedNativeBytes=1500,compilerJobs=len(jobs),results=completed))
    for result in completed:
        for row in result.get('results',[]):print(result['job'],row['source'].get('bytes'),row['source'].get('matchingBytes'),row['genuineLink'].get('exactCallerBytes'),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--run',action='store_true');parser.add_argument('--one',type=int);args=parser.parse_args()
    if args.prepare:prepare()
    if args.run:run()
    if args.one is not None:one(args.one)
