import concurrent.futures
import hashlib
import os
import subprocess
from project import ROOT,read_json,write_json,sha256
from compile_main_nitrosystem_breadth_20261101 import REF
from elftools.elf.elffile import ELFFile

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/more'
WORK=ROOT/'work/w5ml/more/reference-profiles'

def normalized(data,relocs):
    payload=bytearray(data)
    for r in relocs:
        offset=r['offset'];kind=r['type']
        if kind==1:payload[offset:offset+3]=bytes(3)
        elif kind==2:payload[offset:offset+4]=bytes(4)
        else:raise ValueError(('Unsupported reference relocation',kind))
    return hashlib.sha256(payload).hexdigest()

def build(item):
    relative,version,label,opt=item
    source=REF/relative;probe=next(r for r in read_json(ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk/reference-probes.json')['results'] if r['profile']=='base4p');directory=WORK/source.stem/label;directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';flags=list(probe['compilerFlags']);flags[flags.index('-i')+1]=(ROOT/'work/w5ml/more/parse-only').as_posix();flags[:]=flags[:flags.index('-O4,p')]+opt+flags[flags.index('-lang'):];compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+version+'/mwccarm.exe');command=[str(compiler),*flags,'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')));row=dict(referenceSource=source.relative_to(ROOT).as_posix(),referenceSha256=sha256(source),profile=label,compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,command=command,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr,sourceCredit=0)
    matches=[]
    if process.returncode==0:
        row.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
        image=(ROOT/'extract/arm9/arm9.bin').read_bytes();claims=read_json(LANE/'claim.json')['functions']
        with obj.open('rb') as stream:
            elf=ELFFile(stream)
            for symbol in elf.get_section_by_name('.symtab').iter_symbols():
                if symbol['st_info']['type']!='STT_FUNC' or not isinstance(symbol['st_shndx'],int) or not symbol['st_size']:continue
                start=symbol['st_value'];size=symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size];relocs=[]
                for section in elf.iter_sections():
                    if section['sh_type'] not in ('SHT_REL','SHT_RELA') or section['sh_info']!=symbol['st_shndx']:continue
                    table=elf.get_section(section['sh_link'])
                    for rel in section.iter_relocations():
                        offset=rel['r_offset']-start
                        if 0<=offset<size:relocs.append(dict(offset=offset,type=rel['r_info_type'],symbol=table.get_symbol(rel['r_info_sym']).name))
                for claim in claims:
                    if claim['bytes']!=size:continue
                    addr=int(claim['address'],0);native=image[addr-0x02000000:addr-0x02000000+size]
                    if normalized(body,relocs)==normalized(native,relocs):matches.append(dict(referenceFunction=symbol.name,address=claim['address'],bytes=size,referenceSource=row['referenceSource'],referenceObject=row['object'],profile=label,relocations=relocs,normalizedExact=True,comparison='Complete length SHA256 after declared relocation-field normalization; no source credit',sourceCredit=0))
    row['normalizedMatches']=matches;write_json(directory/'result.json',row);print(label,relative,process.returncode,[(r['referenceFunction'],r['bytes']) for r in matches],flush=True);return row

def main():
    sources=['libraries/snd/src/stream.c',*[p.relative_to(REF).as_posix() for p in sorted((REF/'libraries/gfd/src').rglob('*.c'))],*[p.relative_to(REF).as_posix() for p in sorted((REF/'libraries/fnd/src').glob('*.c'))]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(build,[(source,version,label,opt) for source in sources for version,label,opt in [('base','base2space',['-O2','-inline','off']),('base','base2speed',['-O2','-opt','speed','-inline','off']),('sp1p5','sp2space',['-O2','-inline','off'])]]))
    write_json(LANE/'additional-profile-probes.json',dict(status='bounded-unadopted-reference-fingerprints',results=rows,sourceCredit=0));print('matches',sum(len(r['normalizedMatches']) for r in rows),flush=True)

if __name__=='__main__':main()
