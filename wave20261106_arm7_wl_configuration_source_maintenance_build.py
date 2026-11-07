import os
import re
import subprocess
from project import ROOT,read_json,sha256,write_json
import match_runtime as C
import match_lowlevel
from elftools.elf.elffile import ELFFile
SOURCE=ROOT/'src/arm7/parallel_wave20261106/wl-configuration-next/maintenance'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-configuration-next/maintenance'
WORK=ROOT/'work/w6wlg/maintenance'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
REFERENCE_FLAGS=['-lang','c99','-enum','int','-char','signed','-str','noreuse','-proc','arm7tdmi','-gccext,on','-fp','soft','-Cpp_exceptions','off','-RTTI','off','-interworking','-w','off','-sym','on','-gccinc','-nolink','-msgstyle','gcc','-O4','-inline','on']
COMPILER_SHA='89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca'
CERTIFICATE_SHA='3ad45ca890a3febbef30eb10b57c5fe0e4c0838bf9c358605da76ee72dc43e4b'
FLAGS=list(REFERENCE_FLAGS)+['-ipa','file']



def dependencies(source):
    pending=[source];seen=set();root=source.parent.resolve()
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        if not path.is_relative_to(root):raise ValueError('WL include escapes closed source directory')
        text=path.read_text()
        if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__|INCBIN)\b',text) or re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('WL source/header not closed bounded comment-free ordinary C')
        seen.add(path);pending += [path.parent/name for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M)]
    return [dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in sorted(seen) if p!=source.resolve()]


def build(source,directory,negative=False,only=None):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-configuration-next/maintenance' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-configuration-next/maintenance' or WORK!=ROOT/'work/w6wlg/maintenance':raise ValueError('New owned WL compiler scope differs')
    if not directory.resolve().is_relative_to(WORK.resolve()) or not(source.resolve().is_relative_to(SOURCE.resolve()) or source.resolve().is_relative_to(WORK.resolve())):raise ValueError('WL source/output escapes exact private scope')
    if sha256(LANE/'native-certificate.json')!=CERTIFICATE_SHA or sha256(COMPILER)!=COMPILER_SHA:raise ValueError('Frozen WL native/compiler identity differs')
    certificates=[c for c in read_json(LANE/'native-certificate.json')['functions'] if format(int(c['address'],0),'08x')==source.parent.name];boundary=read_json(LANE/'boundary-certificate.json');
    if sha256(LANE/'boundary-certificate.json')!='6bf20f4e46162b18e16be3ccb781f50dae598c10ba828071269677f1d2ed6cfd':raise ValueError('Immutable original ARMv4T instruction/literal certificate changed')
    from wave20261106_arm7_wl_configuration_source_maintenance_boundary import certificate as verify_boundary
    if len(boundary['functions'])!=4:raise ValueError('Exact admitted WL boundary count differs')
    for c in certificates:
        b=next(b for b in boundary['functions'] if b['address']==c['address']);identity=['program','processor','module','mode','address','bytes']
        if any(c[k]!=b[k] for k in identity) or c['targetSha256']!=b['nativeSpanSha256']:raise ValueError('Complete WL boundary namespace differs')
        verify_boundary(b['flow'],(ROOT/c['binary']).read_bytes(),c['base'],c['targetSha256'])
    deps=dependencies(source);directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';argv=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Fresh explicit C99 WL compilation failed',process.stdout,process.stderr))
    rows=[];outputs={}
    with obj.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
        for certificate in certificates:
            symbol=next(s for s in symbols if s.name==certificate['name']);start,size=symbol['st_value'],symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size];relocations=[]
            if symbol['st_info']['type']!='STT_FUNC' or symbol['st_info']['bind']!='STB_GLOBAL' or not any(s.name=='$a' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual WL exported function/ARM mapping differs')
            for section in elf.iter_sections():
                if section['sh_type'] not in ['SHT_REL','SHT_RELA'] or section['sh_info']!=symbol['st_shndx']:continue
                table=elf.get_section(section['sh_link'])
                for r in section.iter_relocations():
                    offset=r['r_offset']-start
                    if 0<=offset<size:relocations.append(dict(offset=offset,type=r['r_info_type'],symbol=table.get_symbol(r['r_info_sym']).name,format=section['sh_type'],explicitAddend=r['r_addend'] if section['sh_type']=='SHT_RELA' else None,originalEncodedWord=body[offset:offset+4].hex()))
            row={k:certificate[k] for k in ['program','processor','module','mode','architecture','address','bytes','base','binary','inputModuleSha256','targetSha256','name','nativeAlias']};row.update(sourceModule='arm7-main',source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=deps,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),compiledBytes=size,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_SHA,compilerFlags=FLAGS,relocations=relocations,sectionIndex=symbol['st_shndx'],sectionOffset=start,command=argv,cwd=str(ROOT),exitCode=0,stdout=process.stdout,stderr=process.stderr,sourceLanguage='C',ordinaryCBytes=certificate['bytes'],justifiedAssemblyBytes=0,hardwareAssemblyRanges=[],boundaryEvidence=dict(path=(LANE/'native-certificate.json').relative_to(ROOT).as_posix(),sha256=CERTIFICATE_SHA));rows.append(row)
    from wave20261106_arm7_wl_configuration_source_maintenance_link import validate
    rows=[r for r in rows if only is None or r['name'] in only]
    for row in rows:
        bad=negative is True or isinstance(negative,(set,list,tuple)) and row['name'] in negative;proof,output=validate(row,directory/format(int(row['address'],0),'08x'),bad);row.update(realLink=proof,matchingBytes=row['bytes'] if not bad else None,exactAfterDeclaredRelocation=not bad,outputSha256=C.sha(output),nativeSymbolEntries=proof['bindings']);outputs[row['name']]=output
    write_json(directory/'rows.json',rows);return rows,outputs


def build_all(directory,overrides=None,negative=None,only=None):
    rows=[];outputs={}
    for certificate in read_json(LANE/'native-certificate.json')['functions']:
        if only is not None and certificate['name'] not in only:continue
        source=(overrides or {}).get(certificate['name'],ROOT/certificate['source']);r,b=build(source,directory/format(int(certificate['address'],0),'08x'),(negative or []));rows+=r;outputs.update(b)
    return rows,outputs


if __name__=='__main__':
    rows,outputs=build_all(WORK/'pilot');print([(r['address'],r['compiledBytes'],len(r['relocations']),r['realLink']['exactCallerBytes']) for r in rows],flush=True)
