import concurrent.futures
import os
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile
from compile_main_nitrosystem_breadth_20261101 import REF,SDK,PROFILES

WORK=ROOT/'work/w5ml/sdk'


def build(profile):
    version,label,opt=profile;directory=WORK/label;directory.mkdir(parents=True,exist_ok=True);compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+version+'/mwccarm.exe');source=REF/'libraries/snd/src/sndarc_stream.c';obj=directory/'compiled.o';stdlib=WORK/'parse-only'
    flags=[*C.FLAGS,*opt,'-lang','c99','-DSDK_CW_FORCE_EXPORT_SUPPORT','-DSDK_TS','-DSDK_4M','-DSDK_ARM9','-DSDK_CW','-DSDK_FINALROM','-DSDK_CODE_ARM','-DNNS_FINALROM']
    includes=[stdlib,REF/'include',SDK/'include',ROOT/'generated/sdk-reference/20261101/parse-only-headers',ROOT/'generated/sdk-reference/20261101/include',*[p for p in (REF/'libraries').glob('*/include') if p.is_dir()]]
    for folder in includes:flags.extend(['-i',folder.as_posix()])
    command=[str(compiler),*flags,'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    row=dict(referenceSource=source.relative_to(ROOT).as_posix(),referenceSourceSha256=sha256(source),profile=label,compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,command=command,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr,parseOnlyUnadopted=True,sourceCredit=0)
    if process.returncode==0:
        row.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
        with obj.open('rb') as stream:
            elf=ELFFile(stream);row['functions']=[dict(name=s.name,bytes=s['st_size'],section=s['st_shndx'],offset=s['st_value']) for s in elf.get_section_by_name('.symtab').iter_symbols() if s['st_info']['type']=='STT_FUNC' and isinstance(s['st_shndx'],int) and s['st_size']]
    write_json(directory/'result.json',row);print(label,process.returncode,[(r['name'],r['bytes']) for r in row.get('functions',[]) if r['name']=='MakeWaveData'],flush=True);return row


def main():
    stdlib=WORK/'parse-only';stdlib.mkdir(parents=True,exist_ok=True);(stdlib/'stddef.h').write_text('typedef unsigned int size_t;\n#define offsetof(type,member) ((unsigned int)&(((type*)0)->member))\n#ifndef NULL\n#define NULL ((void*)0)\n#endif\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(build,PROFILES))
    write_json(ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk/reference-probes.json',dict(status='bounded-comparative-context-investigation',profiles=len(rows),sourceUnit='sndarc_stream.c',results=rows,stdlibAdapter=dict(path=(stdlib/'stddef.h').relative_to(ROOT).as_posix(),sha256=sha256(stdlib/'stddef.h')),referencesUnmodified=True,sourceCredit=0))


if __name__=='__main__':main()
