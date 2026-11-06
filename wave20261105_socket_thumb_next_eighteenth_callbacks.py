from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighteenth_bindings import inputs
from wave20261105_socket_thumb_next_eighteenth_models import TARGETS
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
CONTRACTS={
 'release':dict(caller=0x0208ff04,load=0x0208ff50,call=0x0208ff54,field=28,target='r1',argumentWords=1,returnWords=0),
 'socallocate':dict(caller=0x02090608,load=0x0209060e,call=0x02090614,field=12,target='r2',argumentWords=2,returnWords=1),
 'socrelease':dict(caller=0x02090624,load=0x02090630,call=0x02090634,field=4,target='r3',argumentWords=3,returnWords=0)}
INSTRUCTIONS={
 'release':{0x0208ff46:('ldr','r1, [r0]'),0x0208ff48:('ldr','r0, [r1, #0x28]'),0x0208ff50:('ldr','r1, [r1, #0x1c]'),0x0208ff52:('ldr','r0, [r0, #0x1c]'),0x0208ff54:('blx','r1')},
 'socallocate':{0x0209060c:('adds','r4, r0, #4'),0x0209060e:('ldr','r2, [r2, #0xc]'),0x02090610:('movs','r0, #0'),0x02090612:('adds','r1, r4, #0'),0x02090614:('blx','r2'),0x0209061a:('stm','r0!, {r4}')},
 'socrelease':{0x0209062c:('subs','r1, r1, #4'),0x0209062e:('ldr','r2, [r1]'),0x02090630:('ldr','r3, [r3, #4]'),0x02090632:('movs','r0, #0'),0x02090634:('blx','r3')}}


def verify_site(name,contract,image,entry):
    if name not in CONTRACTS or contract!=CONTRACTS[name]:raise ValueError('Measured named allocator/free minimum interface differs')
    address=contract['caller'];body=image[address-0x02000000:address-0x02000000+entry['bytes']]
    if C.sha(body)!=entry['targetSha256'] or int(entry['address'],0)!=address or entry['mode']!='thumb':raise ValueError('Whole original allocator/free body/namespace differs')
    decoded={i.address:(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(body,address)}
    if any(decoded.get(a)!=pair for a,pair in INSTRUCTIONS[name].items()):raise ValueError('Actual original callback field/argument/result flow differs')
    if any(line.startswith('from:0x'+format(contract['call'],'08x')+' ') for line in entry['originalRelocationRecords']):raise ValueError('Dynamic callback is not an original encoded function target')
    return dict(contract=contract,nativeSha256=entry['targetSha256'],instructions=[dict(address=hex(a),mnemonic=m,operands=o) for a,(m,o) in INSTRUCTIONS[name].items()],fixedOriginalTargetClaimed=False,calleeSourceCredit=0)


def execute(rows):
    sourceRoot=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth';evidenceRoot=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth'
    if sourceRoot!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth' or evidenceRoot!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth':raise ValueError('New eighteenth source/evidence materializer scope changed')
    directory=ROOT/'work/w5st/eighteenth-callback-controls';directory.mkdir(parents=True,exist_ok=True);value,image,inventory,records,imports=inputs();sites=[];negatives=[]
    for name,contract in CONTRACTS.items():
        entry=next(e for e in value['entries'] if int(e['address'],0)==contract['caller']);sites.append(verify_site(name,contract,image,entry))
        for key,bad in [('load',contract['load']+2),('call',contract['call']+2),('field',contract['field']+4),('target','r0'),('argumentWords',contract['argumentWords']+1),('returnWords',1-contract['returnWords'])]:
            variant=dict(contract);variant[key]=bad
            try:verify_site(name,variant,image,entry)
            except ValueError as error:negatives.append(dict(interface=name,case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong named allocator/free contract admitted')
        changed=bytearray(image);changed[contract['call']-0x02000000]^=1
        try:verify_site(name,contract,bytes(changed),entry)
        except ValueError as error:negatives.append(dict(interface=name,case='original-code',rejected=True,reason=str(error)))
        else:raise ValueError('Altered original runtime callback body admitted')
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth/context.h';original=header.read_text();(directory/'context.h').write_text(original)
    source=directory/'providers.c';source.write_text('#include "context.h"\nvoid fixture_release(u32 *p){*p^=0x5a;}\nvoid *fixture_socallocate(u32 name,s32 size){return(void *)(name^(u32)size^0x02405000);}\nvoid fixture_socrelease(u32 name,u32 *p,s32 size){*p=name^(u32)size^0x5a;}\n')
    probes=[provider_probe(source,directory/(mode+'.o'),mode) for mode in ['thumb','arm']]
    badDeclarations=[]
    for name,caller,old,new in [('allocate-one-arg','02090608','(*allocateC)(u32,s32)','(*allocateC)(u32)'),('allocate-three-arg','02090608','(*allocateC)(u32,s32)','(*allocateC)(u32,s32,u32)'),('free-two-arg','02090624','(*release4)(u32,void *,s32)','(*release4)(u32,void *)'),('free-four-arg','02090624','(*release4)(u32,void *,s32)','(*release4)(u32,void *,s32,u32)')]:
        if original.count(old)!=1:raise ValueError('Actual raw SOC callback declaration mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));unit=directory/(name+'.c');unit.write_text((header.parent/(caller+'.c')).read_text());process=compile_source(unit,directory/(name+'.o'),'thumb')
        if process.returncode==0:raise ValueError('Wrong raw SOC callback declaration admitted')
        badDeclarations.append(dict(case=name,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,originalSites=sites,wrongSiteContracts=negatives,wrongCallableDeclarations=badDeclarations,typedFixtureProviders=probes,originalGameTargetsClaimed=False,originalGameBodiesExecuted=0)


def provider_probe(source,output,mode):
    import unicorn
    from unicorn import arm_const as R
    process=compile_source(source,output,mode)
    if process.returncode:raise ValueError(('Fresh named allocator/free provider compile failed',mode,process.stdout,process.stderr))
    results=[]
    with output.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
        for kind in ['release','socallocate','socrelease']:
            symbol=next(s for s in symbols if s.name=='fixture_'+kind);start=symbol['st_value'];section=symbol['st_shndx'];body=elf.get_section(section).data()[start:start+symbol['st_size']];mapping='$t' if mode=='thumb' else '$a'
            if symbol['st_info']['type']!='STT_FUNC' or start&1 or not any(s.name==mapping and s['st_shndx']==section and s['st_value']==start for s in symbols):raise ValueError('Fresh named provider mapping/type differs')
            if any(sec['sh_info']==section and any(start<=r['r_offset']<start+symbol['st_size'] for r in sec.iter_relocations()) for sec in elf.iter_sections() if hasattr(sec,'num_relocations')):raise ValueError('Fresh provider unexpectedly relocates')
            address=TARGETS[kind,mode];vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB if mode=='thumb' else unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02500000,0x10000);vm.mem_write(address,body);cases=[]
            for name,size in [(0,0),(1,1),(0x12345678,0x87654321),(0x80000000,0x7fffffff),(0xffffffff,0xffffffff)]:
                pointer=0x02501000;vm.mem_write(pointer,size.to_bytes(4,'little'));args=[pointer] if kind=='release' else [name,size] if kind=='socallocate' else [name,pointer,size]
                vm.reg_write(R.UC_ARM_REG_CPSR,0x30 if mode=='thumb' else 0x10)
                for reg,value in zip(C.REGISTERS,args):vm.reg_write(reg,value)
                vm.reg_write(R.UC_ARM_REG_LR,0x02508000|int(mode=='thumb'));vm.reg_write(R.UC_ARM_REG_SP,0x0250f000);vm.emu_start(address|int(mode=='thumb'),0x02508000,count=100)
                actual=vm.reg_read(R.UC_ARM_REG_R0) if kind=='socallocate' else int.from_bytes(vm.mem_read(pointer,4),'little');expected=name^size^0x02405000 if kind=='socallocate' else size^0x5a if kind=='release' else name^size^0x5a
                if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02508000:raise ValueError(('Fresh named callback argument/return ABI differs',kind,mode,args,actual,expected))
                cases.append(dict(arguments=args,observed=actual))
            results.append(dict(kind=kind,mode=mode,address=hex(address),pointerWord=hex(address|int(mode=='thumb')),ELFMapping=mapping,ELFType='STT_FUNC',actualFreshTestProviderReturns=len(cases),cases=cases,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameCallback=False,sourceCredit=0))
    return results
