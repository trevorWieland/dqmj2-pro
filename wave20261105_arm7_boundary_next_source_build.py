import os
import re
import subprocess
from project import ROOT,read_json,sha256,write_json
import match_runtime as C
import match_lowlevel
from elftools.elf.elffile import ELFFile
SOURCE=ROOT/'src/arm7/parallel_wave20261105/arm7-boundary-next'
LANE=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next/source'
WORK=ROOT/'work/w5ab-source'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_SHA='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
CERTIFICATE_SHA='4bf294789741b07a9cf034f95563b260e5aba10bbe47ced395d07453c086c892'
FLAGS=[*match_lowlevel.FLAGS,'-ipa','file','-lang','c99']
FLAGS[0]='-O4,s'
FLAGS[FLAGS.index('-inline')+1]='on,noauto'
FLAGS[FLAGS.index('-proc')+1]='arm7tdmi'


def dependencies(source):
    pending=[source];seen=set();root=source.parent.resolve()
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        if not path.is_relative_to(root):raise ValueError('Owned ARM7 include escapes closed source directory')
        text=path.read_text()
        if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__|INCBIN)\b',text) or re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Owned ARM7 source/header is not bounded comment-free ordinary C with closed quoted includes')
        seen.add(path);pending += [path.parent/name for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M)]
    return [dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in sorted(seen) if p!=source.resolve()]


def build(source,directory,negative=False):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-boundary-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next/source' or WORK!=ROOT/'work/w5ab-source':raise ValueError('Owned ARM7 source/evidence/work compiler scope differs')
    if not directory.resolve().is_relative_to(WORK.resolve()) or not(source.resolve().is_relative_to(SOURCE.resolve()) or source.resolve().is_relative_to(WORK.resolve())):raise ValueError('ARM7 compiler output/source escapes unique owned scope')
    path=LANE/'native-certificate.json'
    if sha256(path)!=CERTIFICATE_SHA or sha256(COMPILER)!=COMPILER_SHA:raise ValueError('Pinned immutable ARM7 target/compiler differs')
    certificate=read_json(path)
    if (certificate['program'],certificate['processor'],certificate['module'],certificate['mode'],certificate['architecture'],certificate['address'],certificate['bytes'])!=('','arm7','arm7-main','arm','ARMv4T','0x27e0898',4464):raise ValueError('Exact original ARM7 target namespace/boundary differs')
    deps=dependencies(source);directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';argv=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)]
    process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Fresh owned ARM7 C compile failed',process.stdout,process.stderr))
    relocations=[]
    with obj.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name==certificate['name']);start=symbol['st_value'];size=symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size]
        if symbol['st_info']['type']!='STT_FUNC' or not any(s.name=='$a' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual owned ARM7 object entry/function/ARM mapping differs')
        for section in elf.iter_sections():
            if section['sh_type'] not in ['SHT_REL','SHT_RELA'] or section['sh_info']!=symbol['st_shndx']:continue
            table=elf.get_section(section['sh_link'])
            for r in section.iter_relocations():
                offset=r['r_offset']-start
                if 0<=offset<size:relocations.append(dict(offset=offset,type=r['r_info_type'],symbol=table.get_symbol(r['r_info_sym']).name,format=section['sh_type'],explicitAddend=r['r_addend'] if section['sh_type']=='SHT_RELA' else None,originalEncodedWord=body[offset:offset+4].hex()))
    row={k:certificate[k] for k in ['program','processor','module','mode','architecture','address','bytes','base','binary','inputModuleSha256','targetSha256','name','nativeAlias']}
    row.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=deps,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),compiledBytes=size,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_SHA,compilerFlags=FLAGS,relocations=relocations,sectionIndex=symbol['st_shndx'],sectionOffset=start,command=argv,cwd=str(ROOT),exitCode=0,stdout=process.stdout,stderr=process.stderr,sourceLanguage='C',ordinaryCBytes=4464,justifiedAssemblyBytes=0,hardwareAssemblyRanges=[],boundaryEvidence=dict(path=path.relative_to(ROOT).as_posix(),sha256=CERTIFICATE_SHA))
    from wave20261105_arm7_boundary_next_source_link import validate
    proof,output=validate(row,directory/'real-link',negative)
    row.update(realLink=proof,matchingBytes=4464 if not negative else sum(a==b for a,b in zip(output,(ROOT/certificate['binary']).read_bytes()[int(certificate['address'],0)-certificate['base']:int(certificate['address'],0)-certificate['base']+4464])),exactAfterDeclaredRelocation=not negative,outputSha256=C.sha(output),nativeSymbolEntries=proof['bindings'])
    write_json(directory/'row.json',row);return row,output
