import concurrent.futures
import hashlib
import os
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large'
WORK=ROOT/'work/w5mg/probes'
PROFILES=[('base','base2',['-O2','-inline','off']),('base','base2speed',['-O2','-inline','off','-opt','speed']),('base','base4p',['-O4,p','-ipa','file','-inline','on,noauto']),('sp1p5','sp2speed',['-O2','-inline','off','-opt','speed'])]

def normalized(data,relocs):
    code=bytearray(data)
    for r in relocs:
        offset=r['offset']
        if r['type']==1:code[offset:offset+3]=bytes(3)
        elif r['type']==2:code[offset:offset+4]=bytes(4)
        else:raise ValueError(('Unqualified relocation normalization',r['type']))
    return bytes(code)

def build(item):
    source,version,label,opt=item;directory=WORK/source.stem/label;directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+version+'/mwccarm.exe');flags=[*C.FLAGS,*opt,'-lang','c99'];command=[str(compiler),*flags,'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')));result=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),profile=label,compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,command=command,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr,sourceCredit=0,functions=[]);claims={int(r['address'],0):r for r in read_json(LANE/'claim.json')['claimedFunctions']};image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if process.returncode==0:
        result.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
        with obj.open('rb') as stream:
            elf=ELFFile(stream)
            for symbol in elf.get_section_by_name('.symtab').iter_symbols():
                if symbol['st_info']['type']!='STT_FUNC' or not isinstance(symbol['st_shndx'],int) or not symbol.name.startswith('native_main_'):continue
                address=int(symbol.name[-8:],16);claim=claims[address];start=symbol['st_value'];body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']];relocs=[]
                for section in elf.iter_sections():
                    if section['sh_type'] not in ('SHT_REL','SHT_RELA') or section['sh_info']!=symbol['st_shndx']:continue
                    table=elf.get_section(section['sh_link'])
                    for rel in section.iter_relocations():
                        offset=rel['r_offset']-start
                        if 0<=offset<len(body):relocs.append(dict(offset=offset,type=rel['r_info_type'],symbol=table.get_symbol(rel['r_info_sym']).name))
                native=image[address-0x2000000:address-0x2000000+claim['bytes']];a=normalized(body,relocs);b=normalized(native,relocs);row=dict(address=hex(address),bytes=claim['bytes'],compiledBytes=len(body),normalizedExact=len(a)==len(b) and a==b,normalizedMatchingBytes=sum(x==y for x,y in zip(a,b)),relocations=relocs);result['functions'].append(row)
    write_json(directory/'result.json',result);print(source.stem,label,process.returncode,[(r['address'],r['compiledBytes'],r['bytes'],r['normalizedMatchingBytes'],r['normalizedExact']) for r in result['functions']],flush=True);return result

def main():
    sources=list((ROOT/'work/w5mg/candidates').glob('*.c'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(build,[(s,*p) for s in sources for p in PROFILES]))
    write_json(LANE/'candidate-profiles.json',dict(status='bounded-profile-native-comparison',results=rows,sourceCredit=0))

if __name__=='__main__':main()
