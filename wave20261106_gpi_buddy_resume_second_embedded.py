import os
import re
import shutil
import subprocess
from pathlib import Path
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
from link_runtime_unit import LINKER,LINKER_HASH
from wave20261106_gpi_buddy_resume_second_paths import assert_compile


def inspect(path,row,expected):
    address=int(row['address'],0);size=row['compiledBytes']
    with path.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());entry=next(s for s in symbols if s.name==row['name'])
        if(entry['st_info']['type'],entry['st_value'],entry['st_size'])!=('STT_FUNC',address,size):raise ValueError('Actual embedded ELF function entry/extent/type differs')
        if not any(s.name=='$t'and s['st_value']==address for s in symbols):raise ValueError('Actual embedded ELF Thumb mapping absent')
        sections=[(i,s)for i,s in enumerate(elf.iter_sections())if s['sh_type']=='SHT_PROGBITS'and s['sh_size']and s['sh_addr']<=address and address+size<=s['sh_addr']+s['sh_size']]
        if len(sections)!=1:raise ValueError('Actual embedded caller file storage is ambiguous/absent')
        index,section=sections[0]
        if(entry['st_shndx'],section['sh_addr'],section['sh_size'],section['sh_flags'])!=(index,address,size,0x10000000):raise ValueError('Actual vendor caller section mapping/extent/flags differ')
        body=section.data()
        if body!=expected:raise ValueError('Actual embedded ELF caller bytes differ from independently linked flat output')
        segments=[s for s in elf.iter_segments()if s['p_type']=='PT_LOAD'and s['p_filesz']and s['p_vaddr']<=address and address+size<=s['p_vaddr']+s['p_filesz']]
        if len(segments)!=1:raise ValueError('Actual embedded caller file-backed load mapping is ambiguous/absent')
        segment=segments[0]
        if(segment['p_vaddr'],segment['p_paddr'],segment['p_filesz'],segment['p_memsz'],segment['p_offset'],segment['p_flags'])!=(address,address,size,size,section['sh_offset'],0x80000000)or segment.data()!=body:raise ValueError('Actual embedded load/section/flat bytes differ')
        return body,dict(sectionIndex=index,sectionName=section.name,type='SHT_PROGBITS',address=hex(address),fileOffset=section['sh_offset'],fileBytes=size,vendorSectionFlags=hex(section['sh_flags']),vendorSegmentFlags=hex(segment['p_flags']),standardExecutableFlagClaimed=False,loadSegmentAddress=hex(segment['p_vaddr']),loadSegmentFileBytes=segment['p_filesz'],allThreePayloadsIdentical=True)


def link(row,flat_proof,directory,expected):
    target=directory/'embedded';assert_compile(ROOT/row['source'],target);target.mkdir(parents=True,exist_ok=True)
    originals=[Path(p)for p in flat_proof['linkerAttempt']['command']if str(p).endswith('.o')];copies=[]
    if not originals or originals[0].name!='caller.o'or any(p.parent.resolve()!=directory.resolve()for p in originals):raise ValueError('Exact genuine flat-link input object set differs')
    for path in originals:
        out=target/path.name;shutil.copyfile(path,out)
        if sha256(path)!=sha256(out):raise ValueError('Unmodified compiler/split/mode anchor copy differs')
        copies.append(dict(path=out.relative_to(ROOT).as_posix(),sha256=sha256(out)))
    text=(directory/'unit.lcf').read_text();normal,count=re.subn(r' > (?:caller|binding[0-9]+)\.bin','',text)
    if count!=len(originals):raise ValueError('Only explicit external output redirections may change')
    lcf=target/'unit.lcf';lcf.write_text(normal,encoding='utf-8');elf=target/'linked.elf'
    command=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm946e','-main',row['name'],str(lcf),*[str(ROOT/p['path'])for p in copies],'-o',str(elf)]
    if sha256(LINKER)!=LINKER_HASH:raise ValueError('Pinned original genuine MW linker changed')
    process=subprocess.run(command,cwd=target,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=30);attempt=dict(command=command,cwd=str(target),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)
    if process.returncode:raise ValueError(('Genuine embedded normal MW link failed',attempt))
    body,storage=inspect(elf,row,expected);(target/'caller.bin').write_bytes(body)
    result=dict(flat_proof,linkedElf=elf.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(elf),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),linkerAttempt=attempt,legacyExternalOutputLink=flat_proof,embeddedCallerStorage=storage,unmodifiedLinkInputCopies=copies,normalEmbeddedLinkMatchesIndependentFlatOutput=True,callerBinExtractedFromActualEmbeddedSection=True)
    write_json(target/'embedded-proof.json',result);return result
