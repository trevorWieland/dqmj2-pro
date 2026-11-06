import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
import match_runtime as c
from project import ROOT,write_json,sha256
from link_runtime_unit import measured_module
WORK=ROOT/'build/ghidra864'
TARGETS={'ov000':[(0x021DA5E4,2080),(0x021DBC18,1884)]}


def inventory(directory):
    rows=[]
    for path in sorted(directory.rglob('*')):
        if path.is_symlink()or path.is_junction():raise ValueError('864 project junction/link dependency rejected')
        if path.is_file():rows.append(dict(path=path.relative_to(directory).as_posix(),sha256=sha256(path),bytes=path.stat().st_size))
    return rows


def run(toolroot):
    toolroot=toolroot.resolve();sourceprojects=toolroot/'work/tool-validation/projects';source=sourceprojects/'j2p-private.rep';gpr=sourceprojects/'j2p-private.gpr';snapshot=0
    while(WORK/'snapshots'/('run%03d'%snapshot)).exists():snapshot+=1
    projects=WORK/'snapshots'/('run%03d'%snapshot);replica=projects/'j2p-private.rep';gprhash=sha256(gpr)
    before=inventory(source);projectbytes=sum(r['bytes']for r in before)+gpr.stat().st_size;free=shutil.disk_usage(ROOT).free
    if free<projectbytes+1024**3:raise ValueError('864 insufficient free space for isolated project')
    projects.mkdir(parents=True,exist_ok=True)
    if not replica.exists():shutil.copytree(source,replica);shutil.copy2(gpr,projects/'j2p-private.gpr')
    copied=inventory(replica)
    if copied!=before or sha256(gpr)!=sha256(projects/'j2p-private.gpr'):raise ValueError('864 project snapshot identity differs')
    java=toolroot/'tools/jdk/jdk-25.0.5+8/bin/java.exe';ghidra=toolroot/'tools/ghidra/ghidra_12.2_PUBLIC';utility=ghidra/'Ghidra/Framework/Utility/lib/Utility.jar';properties=ghidra/'Ghidra/application.properties'
    if'application.version=12.2'not in properties.read_text():raise ValueError('864 pinned Ghidra release differs')
    lockpath=toolroot/'tools.lock.json';lock=json.loads(lockpath.read_text());pins={}
    for name in['jdk','ghidra']:
        entry=lock['tools'][name]
        for relative,expected in entry['files'].items():
            if relative.endswith(('/java.exe','/java.dll','/jvm.dll','/modules','/Utility.jar','/Decompiler.jar','/decompile.exe','/application.properties','/ARM.ldefs')):
                actual=sha256(toolroot/relative)
                if actual!=expected:raise ValueError(('864 pinned tool dependency differs',relative))
                pins[relative]=actual
    version=subprocess.run([str(java),'-version'],capture_output=True,text=True,timeout=30)
    if version.returncode or'25.0.5+8'not in version.stderr+version.stdout:raise ValueError('864 pinned JDK release differs')
    validated=json.loads((toolroot/'evidence/tools/validation.json').read_text());original=next(r['command']for r in validated['checks']if r['name']=='ghidra-main');entry=original.index('ghidra.app.util.headless.AnalyzeHeadless');base=original[:entry+1]
    profile=WORK/'profile'
    for folder in['settingsdir','cachedir','tempdir']: (profile/folder).mkdir(parents=True,exist_ok=True)
    for index,value in enumerate(base):
        if value.startswith('-Duser.home='):base[index]='-Duser.home='+str(profile)
        for name in['settingsdir','cachedir','tempdir']:
            if value.startswith('-Dapplication.'+name+'='):base[index]='-Dapplication.'+name+'='+str(profile/name)
    base[0]=str(java);base[base.index('-cp')+1]=str(utility)
    records=[]
    for module,targets in TARGETS.items():
        metadata,image,symbols=measured_module(module);actual=[]
        for address,size in targets:
            line=next(x for x in symbols.splitlines()if('addr:0x%08x'%address)in x.lower());measured=int(line.split('size=')[1].split(')')[0],0)
            if size!=measured:size=measured
            actual.extend([hex(address),hex(size)])
        output=WORK/'generated'/module;output.mkdir(parents=True,exist_ok=True);program='arm9.bin'if module=='main'else module+'.bin'
        inputfile=WORK/'input'/program;inputfile.parent.mkdir(parents=True,exist_ok=True);inputfile.write_bytes(image)
        command=base+[str(projects),'j2p-private','-import',str(inputfile),'-loader','BinaryLoader','-loader-baseAddr','0x021d7240','-processor','ARM:LE:32:v5t','-cspec','default','-readOnly','-noanalysis','-scriptPath',str(ROOT/'evidence/ghidra864'),'-postScript','J2PExport864.java',module,metadata['sha256'],str(output),*actual,'-max-cpu','2','-log',str(WORK/(module+'.log')),'-scriptlog',str(WORK/(module+'-script.log'))]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=420)
        (WORK/(module+'.stdout.txt')).write_text(result.stdout,encoding='utf-8');(WORK/(module+'.stderr.txt')).write_text(result.stderr,encoding='utf-8')
        records.append(dict(module=module,command=command,returncode=result.returncode,stdoutSha256=c.sha(result.stdout.encode()),stderrSha256=c.sha(result.stderr.encode()),exportPath=str((output/'export.json').relative_to(ROOT)),exportExists=(output/'export.json').is_file()))
        write_json(ROOT/'evidence/attempts/ghidra864-run-progress-20261102.json',dict(sourceCredit=0,records=records))
        if result.returncode or not(output/'export.json').is_file():raise ValueError(('864 headless module failed',module,result.stderr[-2000:],result.stdout[-4000:]))
        print(json.dumps(dict(module=module,functions=len(targets),exportPath=str((output/'export.json').relative_to(ROOT)))),flush=True)
    after=inventory(source)
    if before!=after or sha256(gpr)!=gprhash:raise ValueError('864 original project changed;do notclaimisolation')
    write_json(ROOT/'evidence/verification/ghidra864-independent-frontend-20261102.json',dict(schemaVersion=1,sourceCredit=0,nativeExecutions=0,toolRoot=str(toolroot),toolLockSha256=sha256(lockpath),checkedPinnedDependencies=pins,ghidraArchiveSha256=lock['tools']['ghidra']['sha256'],jdkArchiveSha256=lock['tools']['jdk']['sha256'],ghidraVersion='12.2',javaVersion=version.stderr+version.stdout,javaSha256=sha256(java),utilityJarSha256=sha256(utility),applicationPropertiesSha256=sha256(properties),scriptSha256=sha256(ROOT/'evidence/ghidra864/J2PExport864.java'),generatorSha256=sha256(__file__),projectSource=str(source),projectSnapshot=str(replica),projectBytes=projectbytes,freeBytesBefore=free,projectSnapshotFiles=before,projectGprSha256=gprhash,originalProjectUnchanged=True,headlessReadOnly=True,records=records,limits=['Generated Ghidra C/p-code/types/stackobjects are independent hypotheses,not decompiled source credit','A separate fresh ov000 program uses the measured 0x021D7240 raw mapping; other overlay programs remain isolated','Only private copied project ischanged in memory;no M2C oraccepted-source prototypes seeded','Cross-module calls outside anoverlay program lack main memory/type context andneedexplicit native-chain comparison','Function boundaries are suppliedfrommeasured module ledger andnotvalidatedby successful decompilation'],reproductionCommand='python run_ghidra864_20261102.py --tool-root '+str(toolroot)))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--tool-root',type=Path,required=True);run(parser.parse_args().tool_root)
