import os
import subprocess
from project import ROOT,read_json,sha256,write_json
import match_runtime as C
import link_arm7_bulk_20261030 as original
from link_runtime_unit import binding_object,relocation_rows,LINKER,LINKER_HASH
from elf_units import split_symbol
from elftools.elf.elffile import ELFFile


def validate(entry,directory,negative=False):
    from wave20261106_arm7_wm_residual_next_second_build import WORK,LANE,CERTIFICATE_SHA
    if not directory.resolve().is_relative_to((ROOT/'work/w6wr/second').resolve()) or WORK!=ROOT/'work/w6wr/second':raise ValueError('Private genuine ARM7 linker output scope differs')
    certificate=next(r for r in read_json(LANE/'native-certificate-v3.json')['functions'] if r['name']==entry['name'])
    if sha256(LANE/'native-certificate-v3.json')!=CERTIFICATE_SHA or (entry.get('program') or '',entry['processor'],entry['module'],entry['mode'],entry['address'],entry['bytes'],entry['targetSha256'])!=('','arm7','arm7-main','arm',certificate['address'],certificate['bytes'],certificate['targetSha256']):raise ValueError('Exact selected ARM7 caller/certificate namespace differs')
    if sha256(LINKER)!=LINKER_HASH or sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:raise ValueError('Pinned source/object/linker identity changed')
    modules,functions=original.namespace('');extra={};module=modules['arm7-main'];image=(ROOT/module['binary']).read_bytes();base=int(module['base'],0);address=int(entry['address'],0);native=image[address-base:address-base+entry['bytes']]
    if C.sha(image)!=entry['inputModuleSha256'] or C.sha(native)!=entry['targetSha256']:raise ValueError('Original full ARM7 module/span changed')
    if not negative:bindings=original.derive_bindings(entry,native,functions,modules)
    else:
        fixed={w['renamed']:w for w in certificate['originalBindingWitnesses']};bindings={}
        for rel in entry['relocations']:
            name=rel['symbol'];w=fixed.get(name)
            if w is None:raise ValueError('Wrong-C case introduced an unqualified native binding')
            target=int(w['target'],0);bindings[name]=functions[target] if w['function'] else original.data_binding(entry,target,modules)
    if not negative:
        from wave20261106_arm7_wm_residual_next_second_bindings import verify
        for relocation in entry['relocations']:verify(entry,relocation,bindings[relocation['symbol']],certificate,image,functions,modules)
    directory.mkdir(parents=True,exist_ok=True);sourceObject=ROOT/entry['object'];caller=directory/'caller.o'
    with sourceObject.open('rb') as stream:
        elf=ELFFile(stream);flags=elf['e_flags'];split_symbol(elf,entry['name'],caller)
    before=relocation_rows(sourceObject,entry['name'])
    if before!=relocation_rows(caller,entry['name']):raise ValueError('ARM7 function split changed original ELF relocations/addends')
    required=set()
    with caller.open('rb') as stream:
        elf=ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] not in ['SHT_REL','SHT_RELA']:continue
            table=elf.get_section(section['sh_link'])
            for rel in section.iter_relocations():
                symbol=table.get_symbol(rel['r_info_sym'])
                if symbol['st_shndx']=='SHN_UNDEF':required.add(symbol.name)
    if required-set(bindings):raise ValueError('Unbound actual ARM7 extern after unchanged split')
    memory=[f'CALL: ORIGIN = {address:#x} > caller.bin'];sections=['.caller: { caller.o(.text) } > CALL'];objects=[caller];probes=[];assignments=[]
    for index,name in enumerate(sorted(required)):
        binding=bindings[name];target=int(binding['address'],0)
        if binding['kind']=='function':
            anchor=directory/f'anchor{index}.o';binding_object(name,binding['mode'],flags,anchor);objects.append(anchor);memory.append(f'BIND{index}: ORIGIN = {target:#x} > anchor{index}.bin');sections.append(f'.binding{index}: {{ anchor{index}.o(.text) }} > BIND{index}');probes.append({**binding,**dict(symbol=name,object=anchor.relative_to(ROOT).as_posix(),objectSha256=sha256(anchor),initializedCodeBytes=0,calleeSourceCredit=0)})
        else:assignments.append(name+' = '+hex(target)+';')
    lcf=directory/'unit.lcf';lcf.write_text('MEMORY {\n'+'\n'.join(memory)+'\n}\nSECTIONS {\n'+'\n'.join(sections+assignments)+'\n}\n');linked=directory/'linked.elf';argv=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main',entry['name'],str(lcf),*map(str,objects),'-o',str(linked)]
    process=subprocess.run(argv,cwd=directory,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')));attempt=dict(command=argv,cwd=str(directory),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr);write_json(directory/'attempt.json',attempt)
    if process.returncode:raise ValueError(('Fresh actual ARM7 linker rejected caller',attempt))
    output=(directory/'caller.bin').read_bytes();exact=output==native
    if not negative and not exact:raise ValueError(dict(nativeBytes=len(native),linkedBytes=len(output),matchingBytes=sum(a==b for a,b in zip(native,output))))
    if negative and exact:raise ValueError('Whole wrong C unexpectedly matches complete original ARM7 function')
    with linked.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());own=next(s for s in symbols if s.name==entry['name'])
        if own['st_info']['type']!='STT_FUNC' or own['st_value']!=address or own['st_size']!=entry['compiledBytes']:raise ValueError('Actual linked ARM7 caller symbol boundary differs')
        for probe in probes:
            symbol=next(s for s in symbols if s.name==probe['symbol']);target=int(probe['address'],0)
            if symbol['st_info']['type']!='STT_FUNC' or symbol['st_value']!=target or symbol['st_size'] or not any(s.name==('$a' if probe['mode']=='arm' else '$t') and s['st_value']==target and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual ARM7 binding type/entry/mode acquired wrong state/code')
    if any(p.stat().st_size for p in directory.glob('anchor*.bin')):raise ValueError('ARM7 binding supplied initialized callee code')
    proof=dict(exactCallerBytes=exact,exactLinkedBytes=exact,sourceCredit=0,calleeCodeOrSourceCredit=0,wholeModuleLinked=False,sourceObjectSha256=entry['objectSha256'],splitObjectSha256=sha256(caller),linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedCallerSha256=C.sha(output),originalRelocations=before,splitPreservesRelocationTypesAddendsAndEncodedHBits=True,linkerSha256=LINKER_HASH,linkerAttempt=attempt,lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),bindings=bindings,zeroCodeAnchors=probes,newOriginalCallableEntries=list(extra.values()),originalParserAndCoreVerifiersUnchanged=True)
    write_json(directory/'proof.json',proof);return proof,output
