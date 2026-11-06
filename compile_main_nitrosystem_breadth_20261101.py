import concurrent.futures
import os
import subprocess
from pathlib import Path
import match_runtime as base
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256

REF=ROOT/'deps/reference/NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85'
SDK=ROOT/'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840'
WORK=ROOT/'work/main-nitrosystem-breadth-20261101'
PROFILES=[('base','base4p',['-O4,p','-ipa','file','-inline','on,noauto']),
    ('base','base2space',['-O2','-inline','off']),
    ('base','base2speed',['-O2','-opt','speed','-inline','off']),
    ('sp1p5','sp2space',['-O2','-inline','off'])]


def build(item):
    source,version,label,opt=item
    relative=source.relative_to(REF).as_posix();unit=relative.removesuffix('.c').replace('/','-')
    directory=WORK/unit/label;directory.mkdir(parents=True,exist_ok=True)
    compiler=ROOT/f'tools/mwccarm/mwccarm/2.0/{version}/mwccarm.exe';obj=directory/'compiled.o'
    flags=[*base.FLAGS,*opt,'-lang','c99','-DSDK_CW_FORCE_EXPORT_SUPPORT','-DSDK_TS','-DSDK_4M',
        '-DSDK_ARM9','-DSDK_CW','-DSDK_FINALROM','-DSDK_CODE_ARM','-DNNS_FINALROM']
    includes=[REF/'include',SDK/'include',ROOT/'generated/sdk-reference/20261101/parse-only-headers',
        ROOT/'generated/sdk-reference/20261101/include']
    includes.extend(folder for folder in (REF/'libraries').glob('*/include')if folder.is_dir())
    for folder in includes:flags.extend(['-i',folder.as_posix()])
    command=[str(compiler),*flags,'-c',str(source),'-o',str(obj)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120,
        env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    row=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),profile=label,
        compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,
        command=command,cwd=str(ROOT),exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr,
        parseOnly=True,provisionalHeadersNotAdopted=True,sourceCredit=0)
    if result.returncode==0:
        row.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
        with obj.open('rb')as stream:
            elf=ELFFile(stream)
            row['functions']=[dict(name=s.name,bytes=s['st_size'],section=s['st_shndx'],offset=s['st_value'])
                for s in elf.get_section_by_name('.symtab').iter_symbols()
                if s['st_info']['type']=='STT_FUNC'and isinstance(s['st_shndx'],int)and s['st_size']]
    write_json(directory/'result.json',row)
    return row


def main():
    sources=sorted((REF/'libraries').rglob('*.c'))
    queue=[(source,*profile)for source in sources for profile in PROFILES]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        for index,row in enumerate(pool.map(build,queue)):
            results.append(row)
            if(index+1)%32==0:print(dict(completed=index+1,total=len(queue),successful=sum(r['exitCode']==0 for r in results)),flush=True)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),sourceCredit=0,
        referenceRevision='d636fb5d2b212e8736f09859fff447be2bd0ac85',originalDependenciesUnmodified=True,
        compilerJobs=2,sourceUnits=len(sources),profiles=len(PROFILES),results=results,
        sourceTypeCallerClosureNativeAndLinkProofsPending=True)
    write_json(WORK/'report.json',report)
    print(dict(units=len(sources),attempts=len(results),successful=sum(row['exitCode']==0 for row in results),
        compiledFunctionRows=sum(len(row.get('functions',[]))for row in results),sourceCredit=0))


if __name__=='__main__':
    main()
