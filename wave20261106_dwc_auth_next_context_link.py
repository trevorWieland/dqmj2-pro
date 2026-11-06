import hashlib
import json
import os
import re
import shutil
import struct
from project import ROOT,read_json,sha256
import link_runtime_unit as L
from elftools.elf.elffile import ELFFile

CLAIM='evidence/lanes/parallel-wave20261106/auth-http-parameter-context/data-claim.json'
CLAIM_SHA='8933bdb5cb3a1c641523af9f085b353c4a2f99cfadd88dfbd7e5c3b5e64b6090'
SEMANTIC='src/runtime/parallel_wave20261106/auth-http-parameter-context/020deb2c.json'
DATA_ADDRESS=0x20deb2c
URL_ADDRESS=0x20deb48
DATA_SYMBOL='native_data_020deb2c'
URL_SYMBOL='native_data_020deb48'
IMAGE_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'


def context_contract():
    if sha256(ROOT/CLAIM)!=CLAIM_SHA:raise ValueError('Explicit context data admission changed')
    claim=read_json(ROOT/CLAIM);item=claim['claimedStorage'][0]
    if (len(claim['claimedStorage']),item['program'],item['processor'],item['module'],item['kind'],item['mode'],item['address'],item['bytes'],item['initializedSourceCredit'])!=(1,'','arm9','main','data','data',hex(DATA_ADDRESS),28,0):raise ValueError('Exact context data namespace/kind/mode/extent/credit differs')
    if item['semanticSource']!=SEMANTIC or sha256(ROOT/SEMANTIC)!=item['semanticSourceSha256']:raise ValueError('Original context semantic source changed')
    fields=read_json(ROOT/SEMANTIC)['fields']
    if fields['url']['address']!=hex(URL_ADDRESS) or fields['url']['text']!='https://nas.test.nintendowifi.net/ac' or fields['action']!='DWCHTTP_POST' or tuple(fields[k] for k in ['len_recvbuf','alloc','free','ignoreca','timeout'])!=(4096,None,None,False,20000):raise ValueError('Actual original context field contracts differ')
    native=struct.pack('<7I',URL_ADDRESS,0,4096,0,0,0,20000)
    if hashlib.sha256(native).hexdigest()!=item['targetSha256']:raise ValueError('Original semantic context extent hash differs')
    return item,native


def generated_definition():
    item,native=context_contract();fields=read_json(ROOT/SEMANTIC)['fields']
    values=[f'native_data_{int(fields["url"]["address"],0):08x}','0',str(fields['len_recvbuf']),'0','0','0',str(fields['timeout'])]
    return 'DWCHttpParam '+DATA_SYMBOL+'={'+','.join(values)+'};\n'


def inspect_object(path,entry,allow_wrong_context=False):
    item,native=context_contract()
    with path.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());function=next(s for s in symbols if s.name==entry['name']);data=[s for s in symbols if isinstance(s['st_shndx'],int) and elf.get_section(s['st_shndx'])['sh_flags']&2 and s['st_info']['type']=='STT_OBJECT'];allocated=[s for s in elf.iter_sections() if s['sh_flags']&2]
        if entry['address']!='0x209770c' or entry['bytes']!=192 or entry['mode']!='thumb' or entry.get('program') or entry['processor']!='arm9' or entry['module']!='main':raise ValueError('Context path only owns its exact admitted AuthStart caller')
        if function['st_info']['type']!='STT_FUNC' or len(data)!=1 or data[0].name!=DATA_SYMBOL or data[0]['st_info']['bind']!='STB_GLOBAL' or data[0]['st_size']!=28 or data[0]['st_value']!=0:raise ValueError('Exactly one genuine function and complete global28-byte STT_OBJECT required')
        data_section=elf.get_section(data[0]['st_shndx']);text_section=elf.get_section(function['st_shndx'])
        if len(allocated)!=2 or data_section.name!='.data' or data_section['sh_type']!='SHT_PROGBITS' or data_section['sh_size']!=28 or data_section['sh_flags']!=3 or text_section.name!='.text' or text_section['sh_type']!='SHT_PROGBITS' or text_section['sh_flags']!=6 or text_section['sh_size']!=function['st_size'] or function['st_value']&~1 or any(s.name not in ['.text','.data'] for s in allocated):raise ValueError('Extra exec/BSS/data or incomplete real context section')
        context_relocs=[];context_refs=[];all_required=set()
        for section in elf.iter_sections():
            if section['sh_type'] not in ['SHT_REL','SHT_RELA'] or not elf.get_section(section['sh_info'])['sh_flags']&2:continue
            table=elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                symbol=table.get_symbol(relocation['r_info_sym'])
                if symbol['st_shndx']=='SHN_UNDEF':all_required.add(symbol.name)
                if section['sh_info']==data[0]['st_shndx']:context_relocs.append(dict(offset=relocation['r_offset'],type=relocation['r_info_type'],symbol=symbol.name,explicit=section['sh_type']=='SHT_RELA',addend=relocation['r_addend'] if section['sh_type']=='SHT_RELA' else None))
                if section['sh_info']==function['st_shndx'] and symbol.name in ['.data',DATA_SYMBOL]:
                    context_refs.append(dict(offset=relocation['r_offset'],type=relocation['r_info_type'],symbol=symbol.name,symbolType=symbol['st_info']['type'],symbolBinding=symbol['st_info']['bind'],symbolSectionIndex=symbol['st_shndx'],symbolValue=symbol['st_value'],explicit=section['sh_type']=='SHT_RELA',addend=relocation['r_addend'] if section['sh_type']=='SHT_RELA' else None))
        if context_relocs!=[dict(offset=0,type=2,symbol=URL_SYMBOL,explicit=True,addend=0)]:raise ValueError('Original typed context URL pointer relocation changed')
        original=data_section.data();expected=bytes(4)+native[4:]
        if original!=expected and not allow_wrong_context:raise ValueError('Actual compiled semantic context words differ')
        if len(context_refs)!=2 or sorted((r['symbol'],r['symbolType'],r['symbolBinding'],r['symbolSectionIndex'],r['symbolValue'],r['type'],r['addend']) for r in context_refs)!=sorted([('.data','STT_SECTION','STB_LOCAL',data[0]['st_shndx'],0,2,0),(DATA_SYMBOL,'STT_OBJECT','STB_GLOBAL',data[0]['st_shndx'],0,2,0)]):raise ValueError('Actual local section plus global context object relocation identities differ')
        return dict(dataObject=DATA_SYMBOL,dataSection='.data',dataBytes=28,dataObjectType='STT_OBJECT',compiledDataHex=original.hex(),expectedUnrelocatedDataHex=expected.hex(),pointerRelocations=context_relocs,callerContextReferences=context_refs,required=sorted(all_required),originalCompilerObjectSha256=sha256(path),extraInitializedCodeOrBssOrData=False,contextStorageSourceCredit=0)


def validate(entry,bindings,directory,allow_wrong_context=False,negative_caller=False):
    item,context_native=context_contract();directory.mkdir(parents=True,exist_ok=True)
    if sha256(L.LINKER)!=L.LINKER_HASH:raise ValueError('Pinned genuine MW linker changed')
    original=ROOT/entry['object'];object_proof=inspect_object(original,entry,allow_wrong_context);caller=directory/'caller.o';shutil.copyfile(original,caller)
    if sha256(caller)!=sha256(original) or L.relocation_rows(original,entry['name'])!=L.relocation_rows(caller,entry['name']):raise ValueError('Compiler object or original text relocations were rewritten')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(image).hexdigest()!=IMAGE_SHA:raise ValueError('Complete pinned original main image changed')
    a=int(entry['address'],0);native=image[a-0x2000000:a-0x2000000+entry['bytes']]
    if hashlib.sha256(native).hexdigest()!=entry['targetSha256'] or image[DATA_ADDRESS-0x2000000:DATA_ADDRESS-0x2000000+28]!=context_native:raise ValueError('Original caller/context native extents changed')
    config=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text()
    if 'from:0x020deb2c kind:load to:0x020deb48 module:main' not in records.splitlines() or not any(re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x020deb48',s) for s in config.splitlines()):raise ValueError('Original external URL pointer/target data evidence absent')
    bindings=dict(bindings);bindings[URL_SYMBOL]=dict(program='',processor='arm9',module='main',kind='data',mode='data',address=hex(URL_ADDRESS));required=set(object_proof['required'])
    if required-set(bindings):raise ValueError(('Context object has unqualified genuine externs',sorted(required-set(bindings))))
    memories=[f'CALL: ORIGIN = {a:#x} > caller.bin',f'CONTEXT: ORIGIN = {DATA_ADDRESS:#x} > context.bin'];sections=['.caller: { caller.o(.text) } > CALL','.context: { caller.o(.data) } > CONTEXT'];objects=[caller];assignments=[];probes=[]
    with caller.open('rb') as stream:flags=ELFFile(stream)['e_flags']
    for index,name in enumerate(sorted(required)):
        binding=bindings[name];target=L.verify_binding(name,binding)
        if binding['kind']=='function':
            path=directory/f'binding{index}.o';L.binding_object(name,binding['mode'],flags,path);objects.append(path);memories.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin');sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}');probes.append(dict(name=name,**binding,object=path.relative_to(ROOT).as_posix(),objectSha256=sha256(path),initializedCodeBytes=0,nativeCalleeBytesUsed=0,calleeSourceCredit=0,functionSymbolSize=0))
        else:assignments.append(f'{name} = {target:#x};')
    lcf=directory/'unit.lcf';lcf.write_text('MEMORY {\n'+'\n'.join(memories)+'\n}\nSECTIONS {\n'+'\n'.join(sections+assignments)+'\n}\n');linked=directory/'linked.elf';command=[str(L.LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm946e','-main',entry['name'],str(lcf),*map(str,objects),'-o',str(linked)];process=L.subprocess.run(command,cwd=directory,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=30);attempt=dict(command=command,cwd=str(directory),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)
    if process.returncode:raise ValueError(('Genuine whole-object caller/context MW link failed',attempt))
    caller_bytes=(directory/'caller.bin').read_bytes();data_bytes=(directory/'context.bin').read_bytes();caller_exact=caller_bytes==native;data_exact=data_bytes==context_native
    with linked.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());function=next(s for s in symbols if s.name==entry['name']);data=next(s for s in symbols if s.name==DATA_SYMBOL)
        if function['st_value']!=a or function['st_size']!=entry['compiledBytes'] or data['st_value']!=DATA_ADDRESS or data['st_size']!=28 or data['st_info']['type']!='STT_OBJECT' or not any(s.name=='$t' and s['st_value']==a for s in symbols):raise ValueError('Genuine linked caller/context/mode extents differ')
        extras=[s.name for s in elf.iter_sections() if s['sh_flags']&2 and s['sh_type']!='SHT_NOBITS' and s['sh_size'] and s.name not in ['.caller','.context']]
        if extras:raise ValueError(('Additional initialized exec/data in context link',extras))
        for probe in probes:
            symbol=next(s for s in symbols if s.name==probe['name']);target=int(probe['address'],0);mapping='$t' if probe['mode']=='thumb' else '$a'
            if symbol['st_value']!=target or symbol['st_size']!=0 or not any(s.name==mapping and s['st_value']==target for s in symbols):raise ValueError('Original typed provider anchor changed')
    if not caller_exact and not negative_caller:raise ValueError('Context caller is not complete native-byte-exact')
    if not data_exact and not allow_wrong_context:raise ValueError('Jointly placed original28-byte context differs')
    return dict(exactCallerBytes=caller_exact,linkerSha256=L.LINKER_HASH,linkerAttempt=attempt,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),bindingProbes=probes,contextData=object_proof,contextExactOriginalBytes=data_exact,contextLinkedAddress=hex(DATA_ADDRESS),contextLinkedBytes=28,contextLinkedSha256=sha256(directory/'context.bin'),contextDataSourceCredit=0,unchangedWholeCompilerObject=True,compilerObjectRewritten=False,originalTextRelocationsUnchanged=True,originalContextPointerRelocationsUnchanged=True,isolatedUnitIncludesOnlyCallerAndAdmittedContext=True,wholeModuleLinked=False)
