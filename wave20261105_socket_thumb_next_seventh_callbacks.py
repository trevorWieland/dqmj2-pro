import itertools
from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_seventh_bindings import inputs
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from elftools.elf.elffile import ELFFile

TARGETS={('allocate','thumb'):0x02500100,('allocate','arm'):0x02500200,('release','thumb'):0x02500300,('release','arm'):0x02500400,('handler','thumb'):0x02500500,('handler','arm'):0x02500600}
CONTRACTS={
 '0208eb34':dict(load=0x0208eb4e,call=0x0208eb50,field=24,target='r1',argumentWords=1,returnWords=1,kind='allocate'),
 '0208eb90':dict(load=0x0208eba8,call=0x0208ebaa,field=28,target='r1',argumentWords=1,returnWords=0,kind='release'),
 '0208eccc':dict(load=0x0208ece2,call=0x0208ece4,field=0,target='r1',argumentWords=1,returnWords=1,kind='handler')}
INSTRUCTIONS={
 '0208eb34':{0x0208eb4c:('ldr','r1, [r1]'),0x0208eb4e:('ldr','r1, [r1, #0x18]'),0x0208eb50:('blx','r1'),0x0208eb52:('adds','r6, r0, #0')},
 '0208eb90':{0x0208eba4:('ldr','r0, [r0]'),0x0208eba6:('ldr','r1, [r1]'),0x0208eba8:('ldr','r1, [r1, #0x1c]'),0x0208ebaa:('blx','r1')},
 '0208eccc':{0x0208ecdc:('ldr','r0, [sp]'),0x0208ecde:('cmp','r0, #0'),0x0208ece2:('ldr','r1, [r0]'),0x0208ece4:('blx','r1'),0x0208ece6:('adds','r4, r0, #0')}}


def verify_site(name,contract,image,entry):
    if name not in CONTRACTS or contract!=CONTRACTS[name]:raise ValueError('Exact original one-word indirect interface differs')
    address=int(name,16);body=image[address-0x02000000:address-0x02000000+entry['bytes']]
    if C.sha(body)!=entry['targetSha256'] or entry['address']!=hex(address) or entry['mode']!='thumb':raise ValueError('Whole original command caller changed')
    decoded={i.address:(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(body,address)}
    if any(decoded.get(a)!=pair for a,pair in INSTRUCTIONS[name].items()):raise ValueError('Original loaded interface/BLX/result flow differs')
    if any(line.startswith('from:0x'+format(contract['call'],'08x')+' ') for line in entry['originalRelocationRecords']):raise ValueError('Runtime indirection is not an encoded original target')
    return dict(caller=entry['address'],nativeSha256=entry['targetSha256'],contract=contract,instructions=[dict(address=hex(a),mnemonic=m,operands=o) for a,(m,o) in INSTRUCTIONS[name].items()],fixedOriginalTargetClaimed=False,calleeSourceCredit=0)


def execute(rows):
    directory=ROOT/'work/w5st/seventh-callback-controls';directory.mkdir(parents=True,exist_ok=True)
    value,image,inventory,records,imports=inputs();sites=[];negatives=[]
    for name,contract in CONTRACTS.items():
        entry=next(e for e in value['entries'] if int(e['address'],0)==int(name,16));sites.append(verify_site(name,contract,image,entry))
        for key,wrong in [('load',contract['load']+2),('call',contract['call']+2),('field',contract['field']+4),('target','r2'),('argumentWords',2),('returnWords',1-contract['returnWords'])]:
            variant=dict(contract);variant[key]=wrong
            try:verify_site(name,variant,image,entry)
            except ValueError as error:negatives.append(dict(caller=name,case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original indirect command interface admitted')
        changed=bytearray(image);changed[contract['call']-0x02000000]^=1
        try:verify_site(name,contract,bytes(changed),entry)
        except ValueError as error:negatives.append(dict(caller=name,case='original-code',rejected=True,reason=str(error)))
        else:raise ValueError('Changed original command call admitted')
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/seventh/context.h';original=header.read_text();(directory/'context.h').write_text(original)
    source=directory/'providers.c';source.write_text('#include "context.h"\nvoid *fixture_allocate(u32 size){return (void *)(size^0x02405000);}\nvoid fixture_release(u8 *pointer){*pointer^=0x5a;}\nint fixture_handler(void *command){return (u32)command^0x89abcdef;}\n')
    probes=[provider_probe(source,directory/(mode+'.o'),mode) for mode in ['thumb','arm']]
    badDeclarations=[]
    for name,old,new in [('allocate-argument','(*allocate18)(u32)','(*allocate18)(void)'),('handler-return','int (*handler0)(void *)','void (*handler0)(void *)')]:
        if original.count(old)!=1:raise ValueError('Actual command callable declaration mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));unit=directory/(name+'.c');unit.write_text((ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/seventh'/('0208eb34.c' if name.startswith('allocate') else '0208eccc.c')).read_text());process=compile_source(unit,directory/(name+'.o'),'thumb')
        if process.returncode==0:raise ValueError('Wrong minimum command callable declaration admitted')
        badDeclarations.append(dict(case=name,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,originalSites=sites,wrongSiteContracts=negatives,wrongCallableDeclarations=badDeclarations,typedFixtureProviders=probes,originalGameTargetsClaimed=False,originalGameOrImportedBodiesExecuted=0,limits=['Only controlled fresh one-word ARM/Thumb fixture providers are qualified; no original callback registrations, general allocator/scheduler/handler semantics or game/platform execution is claimed. Runtime caller fixtures intercept these providers before their bodies.'])


def provider_probe(source,output,mode):
    import unicorn
    from unicorn import arm_const as R
    process=compile_source(source,output,mode)
    if process.returncode:raise ValueError(('Actual one-word provider compile failed',mode,process.stdout,process.stderr))
    results=[]
    with output.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
        for kind in ['allocate','release','handler']:
            name='fixture_'+kind;symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];section=symbol['st_shndx'];body=elf.get_section(section).data()[start:start+symbol['st_size']];mapping='$t' if mode=='thumb' else '$a'
            if symbol['st_info']['type']!='STT_FUNC' or start&1 or not any(s.name==mapping and s['st_shndx']==section and s['st_value']==start for s in symbols):raise ValueError('Actual one-word provider mapping/type differs')
            if any(sec['sh_info']==section and any(start<=r['r_offset']<start+symbol['st_size'] for r in sec.iter_relocations()) for sec in elf.iter_sections() if hasattr(sec,'num_relocations')):raise ValueError('One-word fixture code unexpectedly has relocations')
            address=TARGETS[(kind,mode)];vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB if mode=='thumb' else unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02500000,0x10000);vm.mem_write(address,body);cases=[]
            values=[0,1,0x80000000,0xffffffff] if kind!='release' else [0,1,127,128,255]
            for value in values:
                argument=0x02501000 if kind=='release' else value
                if kind=='release':vm.mem_write(argument,bytes([value]))
                vm.reg_write(R.UC_ARM_REG_CPSR,0x30 if mode=='thumb' else 0x10);vm.reg_write(R.UC_ARM_REG_R0,argument);vm.reg_write(R.UC_ARM_REG_LR,0x02508001 if mode=='thumb' else 0x02508000);vm.reg_write(R.UC_ARM_REG_SP,0x0250f000);vm.emu_start(address|int(mode=='thumb'),0x02508000,count=100)
                actual=vm.mem_read(argument,1)[0] if kind=='release' else vm.reg_read(R.UC_ARM_REG_R0);expected=value^({'allocate':0x02405000,'handler':0x89abcdef,'release':0x5a}[kind])
                if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02508000:raise ValueError(('Actual one-word provider ABI differs',kind,mode,value,actual,expected))
                cases.append(dict(argument=argument,fixtureInput=value,observed=actual))
            results.append(dict(kind=kind,mode=mode,address=hex(address),pointerWord=hex(address|int(mode=='thumb')),ELFMapping=mapping,ELFType='STT_FUNC',actualFreshTestProviderReturns=len(cases),cases=cases,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameCallback=False,sourceCredit=0))
    return results
