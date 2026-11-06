from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import re
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from elftools.elf.elffile import ELFFile
import link_arm7_bulk_20261030 as base
import prove_arm7_sdk340_mlme_timeout_callback_scope_20261102 as scope
import validate_arm7_sdk341_mlme_timeout_scope_20261102 as witness
import probe_arm7_sdk342_mlme_timeout_installation_20261102 as installer
from project import ROOT,sha256

BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk348-mlme-tasks-timeouts-final/profile.json'
PROFILE_SHA='eafda1dd00f515f6044a81359f3644303b3ddb3050b170e3e293f3d3de311625'

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen engine or five-caller source profile changed')
    fields=('program','processor','module','mode','address','bytes');seed=next((r for r in json.loads(PROFILE.read_text())['units']if tuple(r.get(k,'')for k in fields)==tuple(entry.get(k,'')for k in fields)),None)
    if seed is None:raise ValueError('Only the five exact complete MLME callers/callbacks are qualified')
    for key in('name','source','sourceSha256','sourceDependencies','compiler','compilerSha256','compilerFlags','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','initializedOriginalTables','nativeInterfaceContract','authoritativeExclusionSnapshot','qualifiedCanonicalScope','relocationContract','codeBytes'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact source/compiler/native contract changed:'+key)
    for row in[dict(path=seed['source'],sha256=seed['sourceSha256']),*seed['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Complete ordinary-source closure changed')
    if sha256(ROOT/seed['binary'])!=seed['inputModuleSha256']:raise ValueError('Current native input module changed')
    image=(ROOT/seed['binary']).read_bytes();offset=int(seed['address'],0)-seed['base']
    if hashlib.sha256(image[offset:offset+seed['bytes']]).hexdigest()!=seed['targetSha256']:raise ValueError('Full original caller range changed')
    if entry.get('relocations')!=seed['relocationContract']:raise ValueError('Only the exact unchanged symbol-role/offset/type/addend contract is qualified')
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

def validate(entry,directory,qualify_runtime_word=True,qualify_tables=True,qualify_scope=True):
    seed=qualified(entry);derive,data_binding=base.derive_bindings,base.data_binding
    if _FRESH is None:prepare_scope()
    current_scope()
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
                if symbol_type=='STT_NOTYPE'and key=='AddTask'and seed['name']in('MLME_ScanTimeOut','MLME_JoinTimeOut','MLME_MeasChanTimeOut'):
                    if offset!=seed['bytes']-4 or target!=0x037f8598 or struct.unpack_from('<I',native,seed['codeBytes']-4)[0]!=0xe12fff1c or not re.search(r'void\s+AddTask\s*\(\s*s32\s+nPriority\s*,\s*u32\s+nTaskID\s*\)\s*;',text):raise ValueError('Only exact proved callback BX-IP tail literal with full AddTask signature is a function')
                    is_function=True
                if not is_function:
                    if key=='native_host_arm7_data_0380fff4':
                        if target!=0x0380fff4 or symbol_type not in('STT_OBJECT','STT_NOTYPE')or not re.search(r'extern\s+unsigned int\s+'+key+r'\s*;',text):raise ValueError('Measured runtime word requires exact complete typed extern')
                    elif target in tables and qualify_tables:
                        table=tables[target];suffix=f'{target:08x}';count=table['elements']
                        if key!=('native_host_arm7_table_'+table['sourceName'].lower()+'_'+suffix)or symbol_type not in('STT_OBJECT','STT_NOTYPE'):raise ValueError('Read-only original-table identity/type changed')
                        declaration=r'extern\s+void\s*\(\s*\*\s*const\s+'+key+r'\s*\[\s*24\s*\]\s*\)\s*\(\s*void\s*\)\s*;'if table['sourceName']=='pTaskFunc'else r'extern\s+const\s+WLLIB_CMD_TBL\s+'+key+r'\s*\[\s*'+str(count)+r'\s*\]\s*;'
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
        with installed(entry,qualify_scope):result=base.validate(entry,directory)
        result['qualifiedCanonicalScope']=dict(seed['qualifiedCanonicalScope'],adapter=Path(__file__).name,adapterSha256=sha256(__file__),freshOriginalScopeAndInstallWitness=True,namespaceRestored=base.namespace is BASE_NAMESPACE,originalUnknownGuardsOutsideExactlyThreeCallbacksUnchanged=True,sourceCreditFromScope=0,additionalInitializedDenominatorBytes=0)
        result['callerSpecificQualification']=dict(generator='link_arm7_sdk349_mlme_tasks_timeouts_20261102.py',generatorSha256=sha256(__file__),profile=PROFILE.relative_to(ROOT).as_posix(),profileSha256=sha256(PROFILE),defaultNamespaceRestoredAndOtherDataGuardsUnchanged=True,originalFunctionTablesAndCalleesSourceCredit=0);return result
    finally:base.derive_bindings,base.data_binding=derive,data_binding


BASE_NAMESPACE=base.namespace
_FRESH=None
SCOPE_PINS={'arm7_sdk306_task_command_context_20261102.py':'80eab13a72faa814de52f92ef1abb6682feea5467343892c025ef29a761f2a6a','arm7_sdk288_transmit_context_20261102.py':'23b8987790253a26e295b13bbb872000af39d3902be0a5bfb7f8e0fe5f5122b9','evidence/arm7/ghidra-runtime-inventory.json':'315dd84918b3f29e87e3fa52dec838b399b28dd2adb286d9c27ac2247624ecd6','prove_arm7_sdk340_mlme_timeout_callback_scope_20261102.py':'3c03b16b3b8ad6ffc513f6717a8d55dc3e37e4e24eeb74425a2d78644ba94f66','validate_arm7_sdk341_mlme_timeout_scope_20261102.py':'c069a93a9687c6195f98fdf746c775f2843536c4c495f278a0f58b992b2a55c9','probe_arm7_sdk342_mlme_timeout_installation_20261102.py':'dad0e1248625809c48b10426d4bd03bdca6c261bec423b031ce933ee0ee9d901','evidence/attempts/arm7-sdk340-mlme-timeout-callback-scope-20261102.json':'43b1318a7ba6a6f659053d26829434c2902fae9900a231bf804204774a5a443b','evidence/attempts/arm7-sdk342-mlme-timeout-installation-20261102.json':'22b94b1a3daaca8adafc194a8adafdb485d55095f52ae6a812833e341fbc8ebb','evidence/verification/arm7-sdk341-mlme-timeout-scope-controls-20261102.json':'201550901a426a06ff968ab31649889c3fe20e5c3a1cac0e4246a7359e0037c9','extract/arm7/runtime/arm7-main.bin':'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416','extract/arm7/runtime/arm7-wram.bin':'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'}

def current_scope():
    if _FRESH is None:raise ValueError('Fresh complete native scope/install/control replay must precede namespace installation')
    for path,digest in SCOPE_PINS.items():
        if not(ROOT/path).is_file()or sha256(ROOT/path)!=digest:raise ValueError('Exact complete native scope/install/input pin changed:'+path)
    if _FRESH!=SCOPE_PINS:raise ValueError('In-process fresh native witness marker changed')
    return json.loads((ROOT/'evidence/attempts/arm7-sdk340-mlme-timeout-callback-scope-20261102.json').read_text())

def prepare_scope():
    global _FRESH
    if base.namespace is not BASE_NAMESPACE:raise ValueError('Fresh scope requires untouched namespace')
    for path,digest in SCOPE_PINS.items():
        if path.endswith('.py')and sha256(ROOT/path)!=digest:raise ValueError('Frozen native witness generator changed')
    witness.main()
    report=json.loads(witness.REPORT.read_text());installation=json.loads(witness.INSTALL.read_text());witness.validate(report,installation);_FRESH=dict(SCOPE_PINS);current_scope()

def namespace(program):
    report=current_scope();modules,functions=BASE_NAMESPACE(program);modules,functions=dict(modules),dict(functions)
    if program!='':return modules,functions
    for row in report['scope']:
        address=int(row['address'],0)
        if any(value in functions for value in range(address,address+row['bytes'],4)):raise ValueError('Exact callback scope conflicts with default namespace')
        functions[address]=dict(program='',processor='arm7',module='arm7-main',mode='arm',kind='function',address=hex(address),bytes=row['bytes'],instructionBytes=row['instructionBytes'],boundarySource='complete-hash-qualified-mlme-timeout-callback',sourceCredit=0,initializedDenominatorDelta=0)
    return modules,functions

@contextmanager
def installed(entry,enabled=True):
    qualified(entry);current_scope()
    if base.namespace is not BASE_NAMESPACE:raise ValueError('Another namespace adapter is installed')
    if enabled:base.namespace=namespace
    try:yield
    finally:base.namespace=BASE_NAMESPACE
