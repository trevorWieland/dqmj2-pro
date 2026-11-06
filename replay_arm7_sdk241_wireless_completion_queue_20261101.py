import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

PROFILE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk241-wireless-completion-ready/profile.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk241-wireless-completion-ready-replay'
REPORT=ROOT/'evidence/attempts/arm7-sdk241-wireless-completion-ready-replay-20261101.json'

def compile_group(group):
    for row in[dict(path=group['source'],sha256=group['sourceSha256']),*group['sourceDependencies'],dict(path=group['compiler'],sha256=group['compilerSha256'])]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen compile-ready source/include/compiler differs')
    source=(ROOT/group['source']).resolve();declared={(ROOT/r['path']).resolve():r['sha256']for r in group['sourceDependencies']};pending=[source];seen=set();includes=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        seen.add(path);text=path.read_text()
        if re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Compile-ready queue has an undeclared system header')
        for name in re.findall(r'^\s*#\s*include\s*"([^"]+)"',text,re.M):
            child=(path.parent/name).resolve()
            if child.parent!=source.parent or child not in declared or sha256(child)!=declared[child]:raise ValueError('Unaccepted closed C/include hypothesis escaped its exact group')
            includes.add(child);pending.append(child)
    if includes!=set(declared):raise ValueError('Complete unaccepted C/include declaration closure differs')
    directory=WORK/group['label'];directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';argv=[str(ROOT/group['compiler']),*group['compilerFlags'],'-c',str(ROOT/group['source']),'-o',str(obj)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    results=[]
    with obj.open('rb')as stream:
        elf=ELFFile(stream);table=elf.get_section_by_name('.symtab')
        for target in group['targets']:
            symbol=next(s for s in table.iter_symbols()if s.name==target['name']);start=symbol['st_value']&~1;size=symbol['st_size'];raw=elf.get_section(symbol['st_shndx']).data()[start:start+size];mask=bytearray(b'\xff'*size);supported=True
            for section in elf.iter_sections():
                if section['sh_type']not in('SHT_REL','SHT_RELA')or section['sh_info']!=symbol['st_shndx']:continue
                for rel in section.iter_relocations():
                    offset=rel['r_offset']-start
                    if not 0<=offset<size:continue
                    if rel['r_info_type']==2:mask[offset:offset+4]=bytes(4)
                    elif rel['r_info_type']in(1,28,29):mask[offset:offset+3]=bytes(3)
                    else:supported=False
            data=(ROOT/target['binary']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=target['inputModuleSha256']:raise ValueError('Current qualified native module differs')
            offset=int(target['address'],0)-target['base'];native=data[offset:offset+target['bytes']]
            if hashlib.sha256(native).hexdigest()!=target['targetSha256']:raise ValueError('Current entire qualified target bytes differ')
            exact=bool(size==len(native)and supported and all((a^b)&m==0 for a,b,m in zip(raw,native,mask)))
            if exact!=target['expectedRelocationMaskMatch']:raise ValueError('Frozen compile-ready outcome changed')
            results.append(dict(identity={k:target[k]for k in('processor','program','module','mode','address','bytes')},name=target['name'],compiledBytes=size,maskedBitsEqual=exact,nonRelocatedSameOffsetBytes=sum(a==b for a,b in zip(raw,native)),sourceCredit=0,genuineLinkAndNativeAcceptanceRequired=True))
    return dict(label=group['label'],source=group['source'],sourceSha256=group['sourceSha256'],sourceDependencies=group['sourceDependencies'],object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),exitCode=0,results=results,sourceCredit=0)

def main():
    profile=json.loads(PROFILE.read_text())
    if profile['sourceCredit']!=0 or profile['allOutputsAreHypotheses']is not True:raise ValueError('Bulk queue cannot publish source credit')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:groups=list(pool.map(compile_group,profile['groups']))
    rows=[r for g in groups for r in g['results']];matched=[r for r in rows if r['maskedBitsEqual']]
    if len(rows)!=28 or len(matched)!=17:raise ValueError('Frozen broad compile queue count differs')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),profileSha256=sha256(PROFILE),groups=groups,compileReadyTargetRanges=len(rows),qualifiedNativeBytes=sum(r['identity']['bytes']for r in rows),relocationMaskedEqualTargets=len(matched),relocationMaskedEqualBytes=sum(r['identity']['bytes']for r in matched),sourceCredit=0,allResultsUnacceptedHypotheses=True,compilerInputsContainNoParseShimsOrAssembly=True,relocationMasksAreNotGenuineLinksOrNativeEvidence=True,sourceInputsNoWorkCaches=True)
    write_json(REPORT,report);print(json.dumps({k:report[k]for k in('compileReadyTargetRanges','qualifiedNativeBytes','relocationMaskedEqualTargets','relocationMaskedEqualBytes','sourceCredit')}),flush=True)
if __name__=='__main__':main()
