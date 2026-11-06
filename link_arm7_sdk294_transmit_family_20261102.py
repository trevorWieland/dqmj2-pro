import json
import re
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from elftools.elf.elffile import ELFFile
import link_arm7_bulk_20261030 as base
import validate_arm7_sdk291_pspoll_scope_20261102 as scope
from project import ROOT,sha256

BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk294-transmit-family-final/profile.json'
PROFILE_SHA='a5caabc4a2f871f50b35381c463777ad7cb7adca3e573777bcd64b497cb67f7c'

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen engine or exact family profile changed')
    seeds=json.loads(PROFILE.read_text())['units'];keys=('program','processor','module','mode','address','bytes');identity=tuple(entry.get(k,'')for k in keys);seed=next((r for r in seeds if tuple(r.get(k,'')for k in keys)==identity),None)
    if seed is None:raise ValueError('Only seven complete host transmit identities are qualified')
    for key in('name','source','sourceSha256','sourceDependencies','compiler','compilerSha256','compilerFlags','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','nativeScopeQualification','nativeInterfaceContract'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact source/compiler/boundary/interface changed:'+key)
    for row in[dict(path=seed['source'],sha256=seed['sourceSha256']),*seed['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Complete ordinary source closure changed')
    witness,install=scope.current();scope.verify(scope.IDENTITY,witness,install);proof=seed['runtimePointerQualification']
    if sha256(ROOT/proof['report'])!=proof['sha256']:raise ValueError('Runtime descriptor producer changed')
    report=json.loads((ROOT/proof['report']).read_text())
    if sha256(ROOT/report['generator'])!=report['generatorSha256']or report['storage']!='0x0380fff4'or report['storageBytes']!=4 or report['origin']!='incoming descriptor word0'or report['constructorReturnCredit']!=0 or report['moduleBssOwnership']is not False:raise ValueError('Incoming runtime word proof no longer qualifies')
    table=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()[0x1787c:0x17882]
    if table!=bytes.fromhex('010004000800'):raise ValueError('Initialized six-byte priority dependency changed')
    return seed

def validate(entry,directory,qualify_callback=True,qualify_runtime_word=True):
    seed=qualified(entry);namespace,derive,data_binding=base.namespace,base.derive_bindings,base.data_binding
    def scoped_namespace(program):
        modules,functions=namespace(program)
        if seed['name']=='InitTxCtrl'and qualify_callback:
            if program!=''or 0x027f0950 in functions:raise ValueError('Callback supplement escaped original host namespace')
            functions[0x027f0950]=dict(program='',processor='arm7',module='arm7-main',mode='arm',kind='function',address='0x27f0950',boundarySource='frozen-sdk291-complete-original-callback-witness',sourceCredit=0)
        return modules,functions
    def scoped_data(candidate,target,modules):
        if target!=0x0380fff4 or not qualify_runtime_word:return data_binding(candidate,target,modules)
        if candidate is not entry:raise ValueError('Runtime word rule escaped exact validated source caller')
        return dict(program='',processor='arm7',module='external-arm7-runtime-pointer-word',kind='data',mode='data',address='0x380fff4',storageBytes=4,region='descriptor-produced-absolute-pointer-no-module-ownership',sourceCredit=0,producerQualification=seed['runtimePointerQualification'])
    def roles(candidate,native,functions,modules):
        if candidate is not entry:raise ValueError('Typed binding rule escaped exact caller')
        with(ROOT/candidate['object']).open('rb')as stream:
            elf=ELFFile(stream);table=elf.get_section_by_name('.symtab');symbols={s.name:s['st_info']['type']for s in table.iter_symbols()};own=next(s for s in table.iter_symbols()if s.name==candidate['name']);start=own['st_value']&~1;raw=elf.get_section(own['st_shndx']).data()[start:start+own['st_size']];actual=[]
            for section in elf.iter_sections():
                if section['sh_type']not in('SHT_REL','SHT_RELA')or section['sh_info']!=own['st_shndx']:continue
                syms=elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    offset=rel['r_offset']-start
                    if 0<=offset<len(raw):
                        symbol=syms.get_symbol(rel['r_info_sym']);actual.append(dict(offset=offset,type=rel['r_info_type'],symbol=symbol.name,sourceSymbolType=symbol['st_info']['type'],format=section['sh_type'],explicitAddend=rel['r_addend']if section['sh_type']=='SHT_RELA'else None,originalEncodedWord=raw[offset:offset+4].hex()))
            if actual!=candidate['relocations']:raise ValueError('Declared relocation roles/offsets/addends differ from unchanged actual object')
        address=int(candidate['address'],0);decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;bindings={};source_text=(ROOT/seed['source']).read_text()+'\n'+'\n'.join((ROOT/r['path']).read_text()for r in seed['sourceDependencies'])
        for rel in candidate['relocations']:
            name,offset,kind=rel['symbol'],rel['offset'],rel['type'];symbol_type=symbols.get(name)
            if symbol_type!=rel['sourceSymbolType']:raise ValueError('Current ELF function/data role disagrees with declared relocation')
            if kind==2:
                addend=rel['explicitAddend']if rel['format']=='SHT_RELA'else int.from_bytes(bytes.fromhex(rel['originalEncodedWord']),'little');target=(struct.unpack_from('<I',native,offset)[0]-addend)&0xffffffff;is_function=symbol_type=='STT_FUNC'
                if symbol_type not in('STT_FUNC','STT_OBJECT')and not(symbol_type=='STT_NOTYPE'and name in('native_host_arm7_data_0380fff4','native_host_arm7_priority_bits_027f787c')):raise ValueError('Unknown absolute C symbol role cannot receive a scope exception')
                if symbol_type=='STT_NOTYPE':
                    declaration=r'extern\s+unsigned int\s+native_host_arm7_data_0380fff4\s*;'if name.endswith('0380fff4')else r'extern\s+const\s+u16\s+native_host_arm7_priority_bits_027f787c\s*\[3\]\s*;'
                    if not re.search(declaration,source_text):raise ValueError('Exact complete typed extern declaration missing')
            elif kind in(1,28,29):
                ins=next(decoder.disasm(native[offset:offset+4],address+offset),None)
                declaration=r'(?m)^\s*(?!(?:return|if|for|while|switch)\b)(?:extern\s+)?(?:static\s+)?(?:inline\s+)?(?:[A-Za-z_]\w*\s+)+\**\s*'+re.escape(name)+r'\s*\([^;{}]*\)\s*[;{]'
                if ins is None or not ins.operands or ins.operands[0].type!=2 or symbol_type not in('STT_FUNC','STT_NOTYPE')or not re.search(declaration,source_text):raise ValueError('Original relocated call and complete typed function declaration required:'+name)
                target=ins.operands[0].imm&0xffffffff;is_function=True
            else:raise ValueError('Unsupported untouched relocation')
            if is_function:
                canonical=target&~1
                if canonical not in functions:raise ValueError('Unqualified original function pointer/call:'+name+' '+hex(target))
                if canonical==0x027f0950 and(seed['name']!='InitTxCtrl'or name!='TxqEndPsPoll'or kind!=2):raise ValueError('Single callback dependency escaped its actual initializer pointer role')
                binding=dict(functions[canonical])
                if kind==2 and bool(target&1)!=(binding['mode']=='thumb'):raise ValueError('Function pointer mode mismatch')
            else:
                binding=scoped_data(candidate,target,modules)
                if name=='native_host_arm7_priority_bits_027f787c'and(seed['name']!='ResetTxqPri'or target!=0x027f787c):raise ValueError('Typed six-byte table escaped its own reset caller')
            encoded=re.search(r'_([0-9a-fA-F]{8})$',name)
            if encoded and(int(encoded[1],16)&(~1 if is_function else 0xffffffff))!=(target&(~1 if is_function else 0xffffffff)):raise ValueError('Address-qualified typed symbol conflicts with original target')
            if name in bindings and bindings[name]!=binding:raise ValueError('Conflicting original symbol targets')
            bindings[name]=binding
        return bindings
    base.namespace,base.derive_bindings,base.data_binding=scoped_namespace,roles,scoped_data
    try:
        proof=base.validate(entry,directory);proof['callerSpecificQualification']=dict(generator='link_arm7_sdk294_transmit_family_20261102.py',generatorSha256=sha256(__file__),profile=PROFILE.relative_to(ROOT).as_posix(),profileSha256=sha256(PROFILE),scopeReportSha256=sha256(scope.SCOPE),installationReportSha256=sha256(scope.INSTALL),allOtherNamespaceAndDataGuardsPreserved=True,callbackAndTableSourceCredit=0);return proof
    finally:base.namespace,base.derive_bindings,base.data_binding=namespace,derive,data_binding
