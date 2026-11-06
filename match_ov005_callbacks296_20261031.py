import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
import match_runtime as compiler
from elf_units import split_symbol
from elftools.elf.elffile import ELFFile
from link_runtime_unit import LINKER,LINKER_HASH,measured_module,binding_object,relocation_rows,verify_binding
from recover_linked_runtime import qualified_bindings
from project import ROOT,configuration,sha256,write_json
SOURCE=ROOT/'src/overlays/ov005_20261031_callbacks296/callbacks.c'
WORK=ROOT/'work/ol296-proof'
REPORT=ROOT/'evidence/matches/ov005-20261031-callbacks296-data.json'
NAME='native_data_ov005_021e6ea4'
ADDRESS,SIZE=0x021E6EA4,24
TARGETS=[0x021E1600,0x021E19B8,0x021E1A6C]

def compile_data(source,directory):
    if sha256(compiler.COMPILER)!=compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]:
        raise ValueError('Callbacks296 compiler identity differs')
    directory.mkdir(parents=True,exist_ok=True)
    output=directory/'compiled.o'
    command=[str(compiler.COMPILER),*compiler.FLAGS,'-c',str(source),'-o',str(output)]
    p=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if p.returncode:
        raise ValueError(('Callbacks296 data compilation failed',p.stdout,p.stderr))
    with output.open('rb')as stream:
        elf=ELFFile(stream)
        symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==NAME)
        section=elf.get_section(symbol['st_shndx'])
        if elf['e_machine']!='EM_ARM'or elf.elfclass!=32 or symbol['st_info']['type']!='STT_OBJECT'or symbol['st_size']!=SIZE or section['sh_flags']&4:
            raise ValueError('Callbacks296 typed non-executable object differs')
        flags=elf['e_flags']
        split=directory/'data.o'
        split_symbol(elf,NAME,split,target_section='.authored_data')
    original=relocation_rows(output,NAME)
    if original!=relocation_rows(split,NAME)or len(original)!=3 or any(r['type']!=2 for r in original):
        raise ValueError('Callbacks296 data relocation preservation differs')
    return output,split,flags,original,dict(command=command,cwd=str(ROOT),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr)

def link_data(source,directory):
    output,split,flags,relocations,compilation=compile_data(source,directory)
    if sha256(LINKER)!=LINKER_HASH:
        raise ValueError('Callbacks296 linker identity differs')
    fake=dict(module='ov005',relocations=[dict(symbol=r['symbol'],target=hex(compiler.symbol_address(r['symbol'])),type=2)for r in relocations])
    bindings=qualified_bindings(fake)
    memories=[f'DATA: ORIGIN = {ADDRESS:#x} > data.bin']
    sections=['.authored_data: { data.o(.authored_data) } > DATA']
    objects=[split]
    anchors=[]
    for i,(name,binding)in enumerate(sorted(bindings.items())):
        address=verify_binding(name,binding)
        if binding['kind']!='function'or binding['mode']!='arm':
            raise ValueError('Callbacks296 callback address/mode differs')
        probe=directory/f'anchor{i}.o'
        binding_object(name,binding['mode'],flags,probe)
        objects.append(probe)
        memories.append(f'ANCHOR{i}: ORIGIN = {address:#x} > anchor{i}.bin')
        sections.append(f'.anchor{i}: {{ anchor{i}.o(.text) }} > ANCHOR{i}')
        anchors.append(dict(symbol=name,**binding,objectSha256=sha256(probe),initializedCalleeCodeBytes=0,calleeSourceCredit=0))
    control=directory/'data.lcf'
    control.write_text('MEMORY {\n'+'\n'.join(memories)+'\n}\nSECTIONS {\n'+'\n'.join(sections)+'\n}\n')
    linked=directory/'linked.elf'
    command=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm946e','-main',NAME,str(control),*map(str,objects),'-o',str(linked)]
    p=subprocess.run(command,cwd=directory,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=30)
    if p.returncode:
        raise ValueError(('Callbacks296 real data link failed',p.stdout,p.stderr))
    data=(directory/'data.bin').read_bytes()
    with linked.open('rb')as stream:
        elf=ELFFile(stream)
        symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
        symbol=next(s for s in symbols if s.name==NAME)
        section=elf.get_section(symbol['st_shndx'])
        if symbol['st_value']!=ADDRESS or symbol['st_size']!=SIZE or section['sh_flags']&4:
            raise ValueError('Callbacks296 linked non-executable placement differs')
        for anchor in anchors:
            address=int(anchor['address'],0)
            s=next(s for s in symbols if s.name==anchor['symbol'])
            if s['st_size']!=0 or s['st_value']!=address or not any(s.name=='$a'and s['st_value']==address for s in symbols):
                raise ValueError('Callbacks296 zero-code ARM anchor differs')
    for i in range(len(anchors)):
        pth=directory/f'anchor{i}.bin'
        if pth.exists()and pth.stat().st_size:
            raise ValueError('Callbacks296 anchor emitted callee bytes')
    return data,dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilerSha256=sha256(compiler.COMPILER),compilerFlags=compiler.FLAGS,compileAttempt=compilation,object=output.relative_to(ROOT).as_posix(),objectSha256=sha256(output),splitObject=split.relative_to(ROOT).as_posix(),splitObjectSha256=sha256(split),relocations=relocations,bindings=bindings,anchors=anchors,linkerSha256=LINKER_HASH,linkAttempt=dict(command=command,cwd=str(directory),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr),linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),control=control.relative_to(ROOT).as_posix(),controlSha256=sha256(control),linkedDataSha256=hashlib.sha256(data).hexdigest(),nonExecutable=True,functionSourceCredit=0,calleeCodeBytes=0)

def run():
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Callbacks296 measured ROM differs')
    metadata,native,symbols=measured_module('ov005')
    if not re.search(r'^'+NAME.replace('native_','')+r' kind:data\(any\) addr:0x021e6ea4$',symbols,re.M):
        raise ValueError('Callbacks296 first data boundary missing')
    if not re.search(r'^data_ov005_021e6ebc kind:data\(any\) addr:0x021e6ebc$',symbols,re.M):
        raise ValueError('Callbacks296 following data boundary missing')
    original=native[ADDRESS-0x021D7240:ADDRESS-0x021D7240+SIZE]
    linked,proof=link_data(SOURCE,WORK/'positive')
    if linked!=original or len(linked)!=SIZE:
        raise ValueError('Callbacks296 complete24-byte data comparison failed')
    negative=ROOT/'nonmatching/overlay-lane/20261031-callbacks296-swapped-negative/source.c'
    negative.parent.mkdir(parents=True,exist_ok=True)
    text=SOURCE.read_text().replace('native_fn_ov005_021e1600,native_fn_ov005_021e19b8,native_fn_ov005_021e1a6c','native_fn_ov005_021e1600,native_fn_ov005_021e1a6c,native_fn_ov005_021e19b8')
    if negative.exists()and negative.read_text()!=text:
        raise ValueError('Callbacks296 preserve earlier control')
    negative.write_text(text)
    bad,badproof=link_data(negative,WORK/'negative')
    if bad==original:
        raise ValueError('Callbacks296 swapped callback control unexpectedly matched')
    report=dict(schemaVersion=1,romSha256=config['romSha256'],processor='arm9',program='',module='ov005',mode='data',moduleSha256=metadata['sha256'],address=hex(ADDRESS),bytes=SIZE,symbol=NAME,nativeSpanSha256=hashlib.sha256(original).hexdigest(),exactAfterGenuineDataLink=True,typedSourceDataBytes=24,authoredExecutableCodeBytes=0,functionMatches=0,acceptedSourceCredit=0,proof=proof,negative=dict(expectedRejected=True,matchingBytes=sum(a==b for a,b in zip(bad,original)),proof=badproof),generatorSha256=sha256(__file__),limitations=['Only the24-byte initialized data span is proposed; no functions or callback bodies reconstructed','Adjacent configured data symbols and dispatcher12-byte indexing establish the bounded two-record view','Opaque callback pointer declarations identify only ARM addresses; original parameter/return typedefs and callback behavior remain unqualified','Zero-sized NOBITS mode anchors contain no initialized callee bytes and earn no native/source credit','This standalone ELF is a data-link container, not an executable program or module-completeness proof','Whole-module placement/integration and credit remain integrator-owned'])
    write_json(REPORT,report)
    print(json.dumps(dict(exactDataBytes=24,functionMatches=0,calleeCodeBytes=0,negativeMatchingBytes=report['negative']['matchingBytes'])))

if __name__=='__main__':
    run()
