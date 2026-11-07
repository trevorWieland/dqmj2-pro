import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps/native'))
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from capstone.arm import ARM_OP_IMM
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_CPSR

LANE=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1-modeflag-abi-audit'
ADDRESS=0x0206dc54
FIELDS=('id','program','processor','module','mode','address','bytes','inputModuleSha256','inputBytesSha256','sourceUnit','sourceSha256','sourceDependencies','object','objectSha256','compilerSha256','compilerFlags','dependencies','evidence','states')
THIRD='src/runtime/parallel_wave20261105/game-main-arm-next/third/context.h'
FIFTH='src/runtime/parallel_wave20261105/game-main-arm-next/fifth/context.h'
FUTURE='src/runtime/goal_resume20261106/source_1/tail/detail_display.h'


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def write(name,value):
    LANE.mkdir(parents=True,exist_ok=True)
    (LANE/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def disassemble(image,base,address,size):
    return [{'address':hex(i.address),'mnemonic':i.mnemonic,'operands':i.op_str}for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(image[address-base:address-base+size],address)]


def machine_check(payload):
    seeds=[0,1,0x021c4f60,0x02640000,0x80000000,0xffffffff]
    results=[]
    for flag in range(256):
        for incoming in seeds:
            cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
            cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
            for page in [ADDRESS&~4095,0x021c4000,0x027d0000]:cpu.mem_map(page,4096)
            cpu.mem_write(ADDRESS,payload)
            cpu.mem_write(0x021c4f8f,bytes([flag]))
            cpu.reg_write(UC_ARM_REG_CPSR,0xf000001f)
            cpu.reg_write(UC_ARM_REG_R0,incoming)
            for i in range(2,13):cpu.reg_write(UC_ARM_REG_R0+i,(0x12340000+0x100*i)&0xffffffff)
            cpu.reg_write(UC_ARM_REG_SP,0x027d1800)
            cpu.reg_write(UC_ARM_REG_LR,0x027d0000)
            reads=[];writes=[]
            cpu.hook_add(UC_HOOK_MEM_READ,lambda uc,kind,address,size,value,data:reads.append((address,size)))
            cpu.hook_add(UC_HOOK_MEM_WRITE,lambda uc,kind,address,size,value,data:writes.append((address,size,value)))
            cpu.emu_start(ADDRESS,0x027d0000,count=16)
            expected_flag=flag if flag<128 else flag|0xffffff00
            expected_cpsr=0x60000000 if not flag else (0xa0000000 if flag>=128 else 0x20000000)
            actual=[cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1),cpu.reg_read(UC_ARM_REG_CPSR)&0xf0000000]
            assert actual==[int(flag==0),expected_flag,expected_cpsr]
            assert reads==[(ADDRESS+24,4),(0x021c4f8f,1)] and not writes
            assert all(cpu.reg_read(UC_ARM_REG_R0+i)==0x12340000+0x100*i for i in range(2,13))
            assert cpu.reg_read(UC_ARM_REG_SP)==0x027d1800 and cpu.reg_read(UC_ARM_REG_LR)==0x027d0000
            results.append([flag,incoming,*actual])
    return {'originalOnly':True,'compiledSourceExecuted':False,'cases':len(results),'all256FlagBytes':True,'incomingR0Seeds':list(map(hex,seeds)),'allCasesPassed':True,'memoryReads':[['0x0206dc6c',4],['0x021c4f8f',1]],'memoryWrites':0,'preservedRegisters':['r'+str(i)for i in range(2,13)]+['sp','lr'],'resultsSha256':hashlib.sha256(json.dumps(results,separators=(',',':')).encode()).hexdigest()}


def native_scan(modules,rows):
    found=[];pointers=[];pins=[];configured=[]
    for module in modules:
        path=module['binary'];blob=(ROOT/path).read_bytes();base=int(module['base'],0)
        assert len(blob)==module['bytes'] and sha(path)==module['sha256']
        pins.append({'module':module['name'],'path':path,'sha256':sha(path),'bytes':len(blob),'base':hex(base)})
        for off in range(0,len(blob)-3,4):
            word=struct.unpack_from('<I',blob,off)[0]
            if word in (ADDRESS,ADDRESS|1):pointers.append({'module':module['name'],'address':hex(base+off),'value':hex(word)})
            if word&0x0e000000!=0x0a000000 or word>>28==15:continue
            displacement=(word&0xffffff)<<2
            if displacement&0x02000000:displacement-=0x04000000
            if (base+off+8+displacement)&0xffffffff==ADDRESS:
                found.append({'module':module['name'],'mode':'arm','address':hex(base+off),'instruction':disassemble(blob,base,base+off,4)[0]})
        decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);decoder.detail=True
        for off in range(0,len(blob)-3,2):
            first,last=struct.unpack_from('<HH',blob,off)
            if first&0xf800!=0xf000 or last&0xf800 not in (0xf800,0xe800):continue
            instructions=list(decoder.disasm(blob[off:off+4],base+off))
            if len(instructions)!=1:continue
            i=instructions[0]
            if i.mnemonic not in ('bl','blx') or not i.operands or i.operands[0].type!=ARM_OP_IMM:continue
            if i.operands[0].imm&~1==ADDRESS:found.append({'module':module['name'],'mode':'thumb','address':hex(base+off),'instruction':{'address':hex(i.address),'mnemonic':i.mnemonic,'operands':i.op_str}})
        relocs=Path(module['symbolsFile']).with_name('relocs.txt').as_posix()
        if (ROOT/relocs).exists():
            pins.append({'path':relocs,'sha256':sha(relocs)})
            for line in (ROOT/relocs).read_text().splitlines():
                if re.search(r'\bto:0x0?206dc54\b',line,re.I):configured.append({'module':module['name'],'path':relocs,'line':line})
    for item in found:
        containing=[r for r in rows if not r.get('program') and r['processor']=='arm9' and r['module']==item['module'] and int(r['address'],0)<=int(item['address'],0)<int(r['address'],0)+r['bytes']]
        assert len(containing)==1
        r=containing[0];item['enclosingIdentity']={k:r.get(k)for k in ('id','program','processor','module','mode','address','bytes','inputBytesSha256','states')}
    assert [(x['module'],x['mode'],int(x['address'],0))for x in found]==[('main','arm',x)for x in [0x206e83c,0x206e8f4,0x2071dc0,0x20721f0]]
    assert len(configured)==4 and not pointers
    return {'moduleCount':len(modules),'pins':pins,'directBranches':found,'configuredTargetRelocations':configured,'alignedWordPointers':pointers,'limits':['Direct ARM branches and Thumb BL/BLX immediate pairs are scanned across entire initialized host ARM9 module images; raw-data false positives remain possible and each found instruction was checked against its enclosing configured function.','Aligned words equal to the ARM entry or its Thumb-bit variant were scanned. Unaligned constants, split/computed addresses and runtime-mutated indirect-call targets are not exhausted.','Other physical programs and CPUs do not establish calls to this ARM9/main identity by equal virtual address.']}


def migration_plan(audit):
    source_root='src/runtime/goal_resume20261106/modeflag_abi'
    files=[]
    for row in audit['acceptedRowsAffectedByCanonicalABI']:
        helper=int(row['address'],0)==ADDRESS
        destination=source_root+('/runtime07/'if helper else'/third/')+Path(row['sourceUnit']).name
        files.append({'identity':row['physicalIdentity'],'previousSource':row['sourceUnit'],'previousSourceSha256':row['sourceSha256'],'proposedSourceView':destination,'bodyChange':False,'formalParameterChange':'(void) to (const void *detail)'if helper else None,'sourceBytesUnchanged':not helper,'acceptedCreditDelta':0})
    files.extend([
        {'previousSource':THIRD,'previousSourceSha256':sha(THIRD),'proposedSourceView':source_root+'/third/context.h','change':'Replace only native_fn_0206dc54(DetailPrefix*) with quoted inclusion of ../modeflag_api.h; retain every other declaration and type.'},
        {'proposedSourceView':source_root+'/modeflag_api.h','declarations':['extern unsigned int native_main_0206dc54(const void *);','extern unsigned int native_fn_0206dc54(const void *);'],'change':'Declaration-only canonical function ABI; existing measured absolute symbol binding remains responsible for alias resolution.'},
        {'previousSource':FUTURE,'previousSourceSha256':sha(FUTURE),'proposedSourceView':source_root+'/detail_display/detail_display.h','change':'Future packet only: replace its concrete pointer declaration with quoted inclusion of ../modeflag_api.h.'},
        {'previousSource':audit['futurePacket']['source'],'previousSourceSha256':audit['futurePacket']['sourceSha256'],'proposedSourceView':source_root+'/detail_display/020721b4.c','sourceBytesUnchanged':True,'acceptedCreditDelta':0,'change':'Future packet only: copy unchanged caller body, retaining its original quoted detail_display.h include and captured detail argument.'}
    ])
    assert all(not(ROOT/row['proposedSourceView']).exists()for row in files)
    return {
        'schemaVersion':1,
        'status':'proposal-only-no-source-views-created',
        'coordinatorOnly':True,
        'audit':{'path':str((LANE/'audit.json').relative_to(ROOT).as_posix()),'sha256':sha(LANE/'audit.json')},
        'migrationScope':{'acceptedRows':5,'preservedInitializedBytes':580,'acceptedFunctionCountDelta':0,'acceptedByteCreditDelta':0,'separateFromFrozenCohort174':True},
        'canonicalFunctionType':'unsigned int (const void *)',
        'canonicalPhysicalBinding':audit['canonicalIdentity'],
        'proposedSourceRoot':source_root,
        'proposedFiles':files,
        'rationale':[
            'Incoming R0 is a captured detail pointer at all 4 observed native direct calls, and the helper ignores it before its first use.',
            'The concrete DetailPrefix completed layouts differ across third, fifth and future headers. Their identical typedef spelling does not establish compatible pointed-to C types.',
            'A const void* parameter accepts these object pointer views without changing their layouts or adding casts, wrappers or machine code.',
            'Four accepted header consumers emit neither a helper call relocation nor a helper-related object symbol. Their canonical declarations still belong in the source ABI migration closure.',
            'native_main_0206dc54 and native_fn_0206dc54 are distinct C identifiers. Their same-address project alias contract must explicitly require the same canonical function type.'
        ],
        'alternatives':[
            {'choice':'Reuse the existing concrete DetailPrefix* proposal','assessment':'Its 28B object/link proof is preserved, but it only agrees with the future header exact type view. It does not close the accepted third header layout conflict.'},
            {'choice':'One canonical opaque named Detail tag','assessment':'Possible, but existing complete partial layouts cannot acquire the same tag while retaining differing members. Explicit conversions or a wider type-view migration would be required.'},
            {'choice':'Keep(void), use a nonprototype declaration, or cast a function pointer','assessment':'Does not establish a compatible one-argument definition and is not an acceptable migration.'},
            {'choice':'Remove the captured argument from callers','assessment':'Would discard the measured native callsite contract and risks removing the native R0 move. Not proposed.'}
        ],
        'requiredFreshProof':[
            'Review and admit only the new disjoint views; preserve the old selected sources, headers, reports and typed proposal byte-for-byte.',
            'Compile all 5 migrated views with each row exact existing compiler SHA and flags. Verify actual STT_FUNC identity/full size, every allocated section byte, defined/referenced symbol contract and raw relocation contract against the pinned previous objects.',
            'For the helper require 28B, unchanged data relocation at offset 24 to native_data_021c4f60, target SHA 1a62887d1cd479ebc3adfa04aa7b0711b1e80028204732569a0e33f0d287e390 and genuine native linked bytes.',
            'Verify the 4 copied accepted caller C files have exactly their previous source bytes and each new header reaches the same canonical declaration-only API header through a quoted include.',
            'Use proper-prototype compiler controls to reject a contradictory(void) declaration and wrong argument arity; do not rely on warnings suppressed by the normal -w off recipe.',
            'Run unchanged helper behavior and existing caller oracles/negative controls from a new immutable executable closure plus a copied-root replay.',
            'Prove all 20 actual native module outputs and existing binding/data/BSS/relocation gates unchanged. Preserve full 2512636 initialized denominator and 0 migration credit.',
            'Recompile and requalify the new future 456B view against its frozen READY contract with the canonical API; preserve its old packet and producer. Any 456B admission is separate from the580B zero-credit migration.'
        ],
        'explicitLimits':[
            'Generic const void* has not been compiled in this read-only task; all 5 new object contracts and combined prototype controls remain required.',
            'Existing partial native_data_021c4f60 array/structure views are inherited source-boundary contracts; this focused plan makes no claim to unify all global data declarations or complete whole-program ISO C typing.',
            'Whole ELF container hashes may differ because of source paths and debug information. Unchanged allocated code/symbol/relocation contracts must be established, not asserted from file-name hashes.',
            'No unconfigured computed indirect-call closure is claimed; the exact static scan limits remain pinned in the audit.'
        ]
    }


def main():
    ledger_bytes=(ROOT/'ledger/functions.jsonl').read_bytes()
    rows=[json.loads(line)for line in ledger_bytes.splitlines()]
    accepted=[r for r in rows if r['states']['functionMatched']]
    helper=next(r for r in accepted if r['module']=='main' and not r.get('program') and r['processor']=='arm9' and int(r['address'],0)==ADDRESS)
    seed=json.loads((ROOT/'provenance/seed-manifest.json').read_text())
    scan=native_scan(seed['modules'],rows)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();base=0x02000000
    payload=image[ADDRESS-base:ADDRESS-base+28]
    assert hashlib.sha256(payload).hexdigest()==helper['inputBytesSha256']
    closure=[];declarations=[];selected_refs=[];accepted_dependencies=[]
    for header in [THIRD,FIFTH,FUTURE]:
        text=(ROOT/header).read_text()
        definition=next(line for line in text.splitlines()if line.endswith(' DetailPrefix;'))
        users=[r for r in accepted if any(d['path']==header for d in r.get('sourceDependencies')or[])]
        declarations.append({'path':header,'sha256':sha(header),'prototype':next(line for line in text.splitlines()if 'native_fn_0206dc54(' in line),'detailDefinition':definition,'acceptedConsumers':[r['id']for r in users]})
        closure.extend(users)
    affected=[helper,*closure]
    assert len(affected)==5 and sum(r['bytes']for r in affected)==580
    inventory=[]
    for r in affected:
        item={k:r.get(k)for k in FIELDS}
        assert sha(r['sourceUnit'])==r['sourceSha256']
        assert sha(r['object'])==r['objectSha256']
        assert all(sha(d['path'])==d['sha256']for d in r.get('sourceDependencies')or[])
        item['reportSha256']=sha(r['evidence']);item['objectContainerPresentAndHashVerified']=True
        item['physicalIdentity']={'program':r.get('program')or'','processor':r['processor'],'module':r['module'],'mode':r['mode'],'address':r['address'],'bytes':r['bytes'],'romSha256':r['buildSha256']}
        item['helperRelocations']=[d for d in r.get('dependencies')or[] if int(d.get('target','0'),0)==ADDRESS]
        with (ROOT/r['object']).open('rb')as stream:
            table=ELFFile(stream).get_section_by_name('.symtab')
            item['helperRelatedObjectSymbols']=[{'name':s.name,'type':s['st_info']['type'],'binding':s['st_info']['bind'],'section':s['st_shndx'],'size':s['st_size'],'value':s['st_value']}for s in table.iter_symbols()if re.search('0206dc54',s.name,re.I)]
        inventory.append(item)
    for r in accepted:
        for d in r.get('dependencies')or[]:
            target=d.get('targetAddress',d.get('target','0'))
            try:target=int(target,0)
            except (TypeError,ValueError):
                match=re.search(r'_([0-9a-f]{8})$',str(target),re.I)
                target=int(match[1],16)if match else None
            if target is not None and ADDRESS<=target<ADDRESS+28:accepted_dependencies.append({'id':r['id'],'dependency':d})
        for path in [r['sourceUnit'],*[d['path']for d in r.get('sourceDependencies')or[]]]:
            if re.search('0206dc54',(ROOT/path).read_text(encoding='utf-8'),re.I):selected_refs.append({'id':r['id'],'path':path})
    assert not accepted_dependencies
    source_refs=[]
    for path in sorted((ROOT/'src').rglob('*')):
        if path.suffix.lower()not in ('.c','.h','.cpp','.cc','.cxx','.hpp')or not path.is_file():continue
        matches=[{'line':i+1,'text':line}for i,line in enumerate(path.read_text(encoding='utf-8').splitlines())if re.search('0206dc54',line,re.I)]
        if matches:source_refs.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'matches':matches})
    callsites=[]
    for address,register,origin,scope in [(0x206e83c,'r6',0x206e77c,0x206e73c),(0x206e8f4,'r6',0x206e77c,0x206e73c),(0x2071dc0,'r8',0x2071d8c,0x2071d78),(0x20721f0,'r6',0x20721d0,0x20721b4)]:
        r=next(r for r in rows if not r.get('program')and r['processor']=='arm9'and r['module']=='main'and int(r['address'],0)==scope)
        body=disassemble(image,base,scope,r['bytes'])
        loader,slot={0x206e73c:(0x206e764,0x206ea68),0x2071d78:(0x2071d84,0x2071fd8),0x20721b4:(0x20721c8,0x2072370)}[scope]
        assert struct.unpack_from('<I',image,slot-base)[0]==0x021c4f60
        capture=next(i for i in body if int(i['address'],0)==origin)
        assert capture['mnemonic']=='ldr'and capture['operands'].startswith(register+', [')and capture['operands'].endswith('#0x20]')
        callsites.append({'callAddress':hex(address),'enclosingIdentity':r['id'],'capturedDetailRegister':register,'captureAddress':hex(origin),'globalBaseLoadAddress':hex(loader),'globalBaseLiteralAddress':hex(slot),'globalBaseValue':'0x021c4f60','captureMeaning':'The 32-bit Menu+0x20 detail pointer is captured in a callee-saved register; subsequent calls preserve it under the measured native ABI.','capture':capture,'entry':body[:25],'callWindow':disassemble(image,base,address-20,28),'registerWrites':[{**i}for i in body if i['operands'].startswith(register+',')or i['mnemonic'].startswith('pop')and register in i['operands']]})
    proposal='evidence/lanes/parallel-wave20261106/goal-resume-source-1/detail-display-abi-proposal/proposal.json'
    old_proposal=json.loads((ROOT/proposal).read_text())
    future='evidence/lanes/parallel-wave20261106/goal-resume-source-1/detail-display/ready.json'
    future_report='evidence/matches/goal-resume20261106-source1-detail-display.json'
    future_data=json.loads((ROOT/future_report).read_text())
    future_entry=next(r for r in future_data['matches']if int(r['address'],0)==0x20721b4)
    alias_binding=future_data['nativeSymbolBindings']['native_fn_0206dc54']
    assert alias_binding=={'program':'','processor':'arm9','module':'main','address':'0x206dc54','mode':'arm','kind':'function'}
    assert sha(old_proposal['proposedSource']['path'])==old_proposal['proposedSource']['sha256']
    inputs={'ledger/functions.jsonl','provenance/seed-manifest.json',proposal,future,future_report,old_proposal['proposedSource']['path'],THIRD,FIFTH,FUTURE}
    for r in inventory:
        inputs.update([r['sourceUnit'],r['object'],r['evidence']])
        inputs.update(d['path']for d in r.get('sourceDependencies')or[])
    inputs.update(r['path']for r in source_refs)
    inputs.update(r['path']for r in scan['pins'])
    inputs.update(['deps/native/capstone/__init__.py','deps/native/capstone/arm.py','deps/native/capstone/lib/capstone.dll','deps/native/unicorn/__init__.py','deps/native/unicorn/unicorn_py3/unicorn.py','deps/native/unicorn/arm_const.py','deps/native/unicorn/lib/unicorn.dll'])
    audit={'schemaVersion':1,
        'status':'read-only-coordinator-review',
        'sourceCredit':0,
        'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],
            cwd=ROOT,
            text=True).strip(),
        'ledgerSha256':hashlib.sha256(ledger_bytes).hexdigest(),
        'romSha256':seed['rom']['sha256'],
        'canonicalIdentity':{k:helper.get(k)for k in ('id','program','processor','module','mode','address','bytes','inputBytesSha256')},
        'acceptedFunctionCount':len(accepted),
        'acceptedActualCallers':accepted_dependencies,
        'acceptedRowsAffectedByCanonicalABI':inventory,
        'acceptedPreservedBytes':580,
        'prototypes':declarations,
        'acceptedSourceOccurrences':selected_refs,
        'sourceSymbolAliases':{
            'originalConfiguredName':helper['symbol'],
            'acceptedDefinitionName':'native_main_0206dc54',
            'importName':'native_fn_0206dc54',
            'importBinding':alias_binding,
            'bindingAuthority':{'path':future_report,'sha256':sha(future_report)},
            'futureCallerRawRelocations':[d for d in future_entry['relocations']if d['symbol']=='native_fn_0206dc54'],
            'acceptedEmittedImports':0,
            'acceptedOtherDefinitionViews':helper.get('alternativeImplementations')or[],
            'languageAliasCaveat':'Different C identifiers do not alias by the C language alone. The measured project link binding maps this import to the accepted implementation at the same qualified physical identity.'},
        'allSourceTextOccurrences':source_refs,
        'inputFiles':[{'path':p,'sha256':sha(p)}for p in sorted(inputs)],
        'physicalNativeScan':scan,
        'callsiteDataflow':callsites,
        'helperDataflow':{'instructions':disassemble(image,base,ADDRESS,24),
            'incomingR0':'Overwritten by MOV r0,#1 at 0x0206dc58 before any read. Never dereferenced.',
            'return':'u32 1 exactly when signed byte at 0x021c4f8f is zero, otherwise 0.',
            'r1':'Sign-extended byte at 0x021c4f8f.',
            'flags':'Final NZCV from CMP signed flag byte,0; MOV and conditional MOV do not change flags.',
            'frame':'No stack access and no calls.',
            'originalMachineChecks':machine_check(payload)},
        'existingTypedProposal':{'path':proposal,
            'sha256':sha(proposal),
            'source':old_proposal['proposedSource'],
            'bodyUnchanged':old_proposal['bodyUnchanged'],
            'preserved':True,
            'scope':'Existing DetailPrefix* proof remains frozen and valid for its exact type view. It does not unify other incompatible completed DetailPrefix layouts.'},
        'futurePacket':{'path':future,
            'sha256':sha(future),
            'report':future_report,
            'reportSha256':sha(future_report),
            'identity':next(r['id']for r in rows if not r.get('program')and r['processor']=='arm9'and r['module']=='main'and int(r['address'],0)==0x20721b4),
            'bytes':456,
            'source':'src/runtime/goal_resume20261106/source_1/tail/020721b4.c',
            'sourceSha256':sha('src/runtime/goal_resume20261106/source_1/tail/020721b4.c'),
            'status':'Frozen READY; blocked by reviewed source ABI migration; zero accepted credit.'},
        'cLanguageBasis':{'source':'https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf',
            'clauses':['6.2.2 external linkage distinguishes identifiers; numeric linker aliases are project contracts, not an ordinary C language alias declaration.','6.2.7 compatible declarations and corresponding completed structure members.','6.3.2.3 object pointers convert to void pointers and may acquire const qualification.','6.5.2.2 argument counts and actual definition type must agree; removing a prototype or casting a function pointer is not a repair.','6.7.5.3 function parameter compatibility.'],
            'interpretation':'Native byte equivalence cannot itself prove canonical C function-type compatibility. Different partial anonymous DetailPrefix views are not made compatible by similar offsets.'},
        'auditLimitations':['No accepted source/header/report/ledger/registry or frozen proposal was modified.',
            'No new candidate was compiled and no native module was relinked. Generic const void* is a proposal, not yet a proven fresh object contract.',
            'Source text scan recognizes the numeric helper spelling; complete accepted relocation records independently cover other emitted import names.',
            'The static indirect-call limits in physicalNativeScan remain explicit.'],
        'executable':{'path':Path(__file__).name,
            'sha256':sha(Path(__file__).name)}}
    assert (ROOT/'ledger/functions.jsonl').read_bytes()==ledger_bytes
    write('audit.json',audit)
    write('migration-plan.json',migration_plan(audit))
    print(json.dumps({'acceptedRows':len(inventory),'preservedBytes':580,'acceptedCallers':len(accepted_dependencies),'directCallsites':len(scan['directBranches']),'nativeCases':audit['helperDataflow']['originalMachineChecks']['cases'],'audit':str((LANE/'audit.json').relative_to(ROOT))}))


if __name__=='__main__':main()
