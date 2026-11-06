import concurrent.futures
import os
import re
import subprocess
from project import ROOT,read_json,write_json,sha256,now

SNAPSHOT=ROOT/'evidence/verification/accepted-cohort80-identities-20261031.json'
CLANG=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
WORK=ROOT/'work/selected-c-initialization80-20261031'
REPORT=ROOT/'evidence/verification/selected-c-initialization80-20261031.json'


def worker(item):
    relative,expected=item;path=ROOT/relative
    assert sha256(path)==expected
    command=[str(CLANG),'--target=armv5te-none-eabi','-std=c99','-fsyntax-only','-O1','-fno-builtin','-Wno-everything',
        '-Wuninitialized','-Wconditional-uninitialized','-ferror-limit=4','-I',str(ROOT),str(path)]
    try:
        process=subprocess.run(command,cwd=ROOT,stdin=subprocess.DEVNULL,capture_output=True,timeout=40)
        output=process.stderr.decode('utf-8',errors='replace')
        log=WORK/(expected+'.txt');log.write_text(output,encoding='utf-8')
        warnings=[line for line in output.splitlines() if re.search(r'\[-W(?:conditional-|sometimes-)?uninitialized\]',line)]
        result=dict(source=relative,sourceSha256=expected,exitCode=process.returncode,initializationDiagnostics=warnings,
            frontendAccepted=process.returncode==0,log=log.relative_to(ROOT).as_posix(),logSha256=sha256(log))
    except subprocess.TimeoutExpired:
        result=dict(source=relative,sourceSha256=expected,frontendAccepted=False,timeoutSeconds=40,initializationDiagnostics=[])
    assert sha256(path)==expected
    return result


def main():
    snapshot=read_json(SNAPSHOT);assert snapshot['acceptedCohort']==80
    sources={}
    for row in snapshot['functions']:
        path=row['source']
        if not path.endswith(('.c','.cpp')):continue
        assert path not in sources or sources[path]==row['sourceSha256']
        sources[path]=row['sourceSha256']
    WORK.mkdir(parents=True,exist_ok=True)
    version=subprocess.run([str(CLANG),'--version'],capture_output=True,text=True,check=True).stdout
    report=dict(createdUtc=now(),state='running',pid=os.getpid(),sourceCredit=0,acceptedCohort=80,selectedSourceFiles=len(sources),
        snapshotSha256=sha256(SNAPSHOT),clang=dict(path=CLANG.relative_to(ROOT).as_posix(),sha256=sha256(CLANG),version=version),
        generatorSha256=sha256(__file__),compilerProcesses=3,results=[],limitations=[
            'Clang is an independent scalar-initialization diagnostic frontend, not the matching compiler or a replacement build',
            'Diagnostics require review; unsupported vendor syntax or headers are reported as frontend failures, never as clean analysis',
            'A clean warning result does not prove all memory initialized, complete domains, historical prototypes or source correctness',
            'Only accepted80 source files are analyzed; no original or reconstructed source is modified'])
    write_json(REPORT,report)
    def update():
        rows=report['results'];report.update(completedSourceFiles=len(rows),frontendAccepted=sum(row['frontendAccepted']for row in rows),
            filesWithInitializationDiagnostics=sum(bool(row['initializationDiagnostics'])for row in rows),
            initializationDiagnosticCount=sum(len(row['initializationDiagnostics'])for row in rows))
        write_json(REPORT,report)
        print({key:report[key]for key in ['completedSourceFiles','frontendAccepted','filesWithInitializationDiagnostics']},flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        for row in pool.map(worker,sorted(sources.items())):
            report['results'].append(row)
            if len(report['results'])%50==0:update()
    report['state']='diagnostic-audit-complete';report['finishedUtc']=now();update()


if __name__=='__main__':main()
