import hashlib
import json
import re
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from elftools.elf.elffile import ELFFile
import link_arm7_bulk_20261030 as base
from project import ROOT,sha256

BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk402-cam-bootstrap-final/profile.json'
PROFILE_SHA='b90840ed3d6ab9f4fb0fb62f13e94aea608f4aa353d07d058179733460b715cd'

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen engine or two-caller source profile changed')
    fields=('program','processor','module','mode','address','bytes');seed=next((r for r in json.loads(PROFILE.read_text())['units']if tuple(r.get(k,'')for k in fields)==tuple(entry.get(k,'')for k in fields)),None)
    if seed is None:raise ValueError('Only the two exact complete CAM bootstrap definitions are qualified')
    for key in('codeBytes','base','binary','name','source','sourceSha256','sourceDependencies','compiler','compilerSha256','compilerFlags','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','initializedOriginalTables','nativeInterfaceContract','authoritativeExclusionSnapshot'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact source/compiler/native contract changed:'+key)
    for row in[dict(path=seed['source'],sha256=seed['sourceSha256']),*seed['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Complete ordinary-source closure changed')
    if sha256(ROOT/seed['binary'])!=seed['inputModuleSha256']:raise ValueError('Current native input module changed')
    image=(ROOT/seed['binary']).read_bytes();offset=int(seed['address'],0)-seed['base']
    if hashlib.sha256(image[offset:offset+seed['bytes']]).hexdigest()!=seed['targetSha256']:raise ValueError('Full original caller range changed')
    producer=seed['runtimePointerQualification']
    if sha256(ROOT/producer['report'])!=producer['sha256']:raise ValueError('Incoming descriptor producer proof changed')
    proof=json.loads((ROOT/producer['report']).read_text())
    if sha256(ROOT/proof['generator'])!=proof['generatorSha256']or proof['storage']!='0x0380fff4'or proof['storageBytes']!=4 or proof['origin']!='incoming descriptor word0'or proof['moduleBssOwnership']is not False or proof['constructorReturnCredit']!=0:raise ValueError('External runtime-word producer no longer qualifies')
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416':raise ValueError('Original initialized table module changed')
    for table in seed['initializedOriginalTables']:
        address=int(table['address'],0);start=address-0x027e0000
        if start<0 or start+table['bytes']>len(main)or table['bytes']!=table['elements']*table['elementBytes']or table['sourceDataCredit']!=0 or hashlib.sha256(main[start:start+table['bytes']]).hexdigest()!=table['valueSha256']:raise ValueError('Complete readonly original-table range/element count changed')
    return seed

def validate(entry,directory,qualify_runtime_word=True,qualify_tables=True):
    seed=qualified(entry);derive,data_binding=base.derive_bindings,base.data_binding
    text=(ROOT/seed['source']).read_text()+'\n'+'\n'.join((ROOT/r['path']).read_text()for r in seed['sourceDependencies']);tables={int(t['address'],0):t for t in seed['initializedOriginalTables']}
    def data(candidate,target,modules):
        if target!=0x0380fff4 or not qualify_runtime_word:return data_binding(candidate,target,modules)
        if candidate is not entry:raise ValueError('Runtime-word rule escaped exact pinned caller')
        return dict(program='',processor='arm7',module='external-arm7-runtime-pointer-word',kind='data',mode='data',address='0x380fff4',storageBytes=4,moduleBssOwnership=False,sourceCredit=0,producerQualification=seed['runtimePointerQualification'])
    def roles(candidate,native,functions,modules):
        if candidate is not entry:raise ValueError('Typed C role rule escaped exact pinned caller')
        with(ROOT/candidate['object']).open('rb')as stream:
            elf=ELFFile(stream);symbols=elf.get_section_by_name('.symtab');types={s.name:s['st_info']['type']for s in symbols.iter_symbols()};own=next(s for s in symbols.iter_symbols()if s.name==candidate['name']);start=own['st_value']&~1;raw=elf.get_section(own['st_shndx']).data()[start:start+own['st_size']];actual=[]
            for section in elf.iter_sections():
                if section['sh_type']not in('SHT_REL','SHT_RELA')or section['sh_info']!=own['st_shndx']:continue
                syms=elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    offset=rel['r_offset']-start
                    if 0<=offset<len(raw):
                        symbol=syms.get_symbol(rel['r_info_sym']);actual.append(dict(offset=offset,type=rel['r_info_type'],symbol=symbol.name,sourceSymbolType=symbol['st_info']['type'],format=section['sh_type'],explicitAddend=rel['r_addend']if section['sh_type']=='SHT_RELA'else None,originalEncodedWord=raw[offset:offset+4].hex()))
            if actual!=candidate['relocations']:raise ValueError('Actual unmodified relocation roles/addends/offsets differ')
        decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;address=int(candidate['address'],0);bindings={}
        for rel in candidate['relocations']:
            key,offset,kind=rel['symbol'],rel['offset'],rel['type'];symbol_type=types.get(key);is_function=False
            if kind==2:
                addend=rel['explicitAddend']if rel['format']=='SHT_RELA'else int.from_bytes(bytes.fromhex(rel['originalEncodedWord']),'little');target=(struct.unpack_from('<I',native,offset)[0]-addend)&0xffffffff;is_function=symbol_type=='STT_FUNC'
                if not is_function:
                    if key=='native_host_arm7_data_0380fff4':
                        if target!=0x0380fff4 or symbol_type not in('STT_OBJECT','STT_NOTYPE')or not re.search(r'extern\s+unsigned int\s+'+key+r'\s*;',text):raise ValueError('Measured runtime word requires exact complete typed extern')
                    elif target in tables and qualify_tables:
                        table=tables[target];suffix=f'{target:08x}';count=table['elements']
                        if key!='BC_ADRS'or symbol_type not in('STT_OBJECT','STT_NOTYPE'):raise ValueError('Read-only original-table identity/type changed')
                        if table['sourceName']!='BC_ADRS'or target!=0x027f74b0 or candidate['name']!='InitializeCAM'or count!=3 or table['elementBytes']!=2:raise ValueError('Only this exact read-only six-byte broadcast table caller is qualified')
                        declaration=r'extern\s+const\s+u16\s+BC_ADRS\s*\[\s*3\s*\]\s*;'
                        if not re.search(declaration,text):raise ValueError('Complete fixed-extent original-table C declaration missing')
                    else:raise ValueError('Unqualified ordinary-data/unknown-symbol role remains refused:'+key)
            elif kind in(1,28,29):
                ins=next(decoder.disasm(native[offset:offset+4],address+offset),None);declaration=r'(?m)^\s*(?!(?:return|if|for|while|switch)\b)(?:extern\s+)?(?:static\s+)?(?:inline\s+)?(?:[A-Za-z_]\w*\s+)+\**\s*'+re.escape(key)+r'\s*\([^;{}]*\)\s*[;{]'
                if ins is None or not ins.operands or ins.operands[0].type!=2 or symbol_type not in('STT_FUNC','STT_NOTYPE')or not re.search(declaration,text):raise ValueError('Complete C signature and original immediate call required:'+key)
                target=ins.operands[0].imm&0xffffffff;is_function=True
            else:raise ValueError('Unsupported original relocation')
            if is_function:
                if target&~1 not in functions:raise ValueError('Original function/entry guard remains refused:'+key)
                binding=dict(functions[target&~1])
                if kind==2 and bool(target&1)!=(binding['mode']=='thumb'):raise ValueError('Original function-pointer mode differs')
            else:binding=data(candidate,target,modules)
            encoded=re.search(r'_([0-9a-fA-F]{8})$',key)
            if encoded and int(encoded[1],16)!=(target&(~1 if is_function else 0xffffffff)):raise ValueError('Address-qualified C symbol conflicts with current native target')
            if key in bindings and bindings[key]!=binding:raise ValueError('Conflicting actual symbol identities')
            bindings[key]=binding
        return bindings
    base.derive_bindings,base.data_binding=roles,data
    try:
        result=base.validate(entry,directory);result['callerSpecificQualification']=dict(generator='link_arm7_sdk403_cam_bootstrap_20261102.py',generatorSha256=sha256(__file__),profile=PROFILE.relative_to(ROOT).as_posix(),profileSha256=sha256(PROFILE),defaultNamespaceAndAllOtherDataGuardsUnchanged=True,originalFunctionTablesAndCalleesSourceCredit=0);return result
    finally:base.derive_bindings,base.data_binding=derive,data_binding
