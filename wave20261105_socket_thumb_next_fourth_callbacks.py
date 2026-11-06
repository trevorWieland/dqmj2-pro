import copy
import os
import struct
import subprocess
from project import ROOT,sha256,read_json
import match_runtime as C
from wave20261105_socket_thumb_next_compiler import COMPILER
from wave20261105_socket_thumb_next_fourth_bindings import inputs
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from elftools.elf.elffile import ELFFile

TARGETS={'thumb':0x02500100,'arm':0x02500200}
CONTRACT=dict(caller=0x0208d228,load=0x0208d348,call=0x0208d354,field=56,bufferField=64,lengthField=68,base='r4',target='r3',argumentWords=3,returnWords=1,nullGuard=True)


def verify_site(contract,image,entry):
    if contract!=CONTRACT:raise ValueError('Exact original indirect callback contract differs')
    start=contract['caller']-0x02000000;body=image[start:start+entry['bytes']]
    if C.sha(body)!=entry['targetSha256'] or entry['address']!=hex(contract['caller']) or entry['mode']!='thumb':raise ValueError('Whole original callback caller changed')
    decoded={i.address:(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(body,contract['caller'])}
    expected={0x0208d348:('ldr','r3, [r4, #0x38]'),0x0208d34a:('cmp','r3, #0'),0x0208d34c:('beq','#0x208d368'),0x0208d34e:('ldr','r0, [r4, #0x40]'),0x0208d350:('ldr','r1, [r4, #0x44]'),0x0208d352:('adds','r2, r4, #0'),0x0208d354:('blx','r3'),0x0208d356:('cmp','r0, #0'),0x0208d358:('beq','#0x208d368'),0x0208d35a:('movs','r0, #0'),0x0208d35c:('str','r0, [r4, #0x44]')}
    if any(decoded.get(address)!=value for address,value in expected.items()):raise ValueError('Original null/field/argument/result BLX-register flow differs')
    if any(line.startswith('from:0x0208d354 ') for line in entry['originalRelocationRecords']):raise ValueError('A dynamic callback must not be represented as an encoded original relocation target')
    return dict(originalCaller=entry['address'],originalCallerSha256=entry['targetSha256'],contract=contract,instructions=[dict(address=hex(a),mnemonic=m,operands=o) for a,(m,o) in expected.items()],originalFixedTargetClaimed=False,minimumCallable='int32(bytePointer,word32,borrowedSocketPointer)',originalStorageOrCalleeCredit=0)


def execute(row):
    directory=ROOT/'work/w5st/fourth-callback-controls';directory.mkdir(parents=True,exist_ok=True)
    native,image,inventory,records,imports=inputs();entry=native['entries'][0]
    site=verify_site(CONTRACT,image,entry);rejected=[]
    for key,value in [('caller',0x0208d22a),('load',0x0208d34a),('call',0x0208d352),('field',60),('bufferField',60),('lengthField',64),('base','r5'),('target','r2'),('argumentWords',2),('returnWords',0),('nullGuard',False)]:
        wrong=dict(CONTRACT);wrong[key]=value
        try:verify_site(wrong,image,entry)
        except ValueError as error:rejected.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original dynamic callback contract admitted')
    changed=bytearray(image);changed[0x0208d354-0x02000000]^=1
    try:verify_site(CONTRACT,bytes(changed),entry)
    except ValueError as error:rejected.append(dict(case='original-instruction',rejected=True,reason=str(error)))
    else:raise ValueError('Changed original indirect branch admitted')
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fourth/context.h'
    original=header.read_text();(directory/'context.h').write_text(original)
    signature='s32 (*callback38)(u8 *,u32,SocketView *);'
    if original.count(signature)!=1:raise ValueError('Closed measured callback prototype absent/ambiguous')
    source=directory/'provider.c';source.write_text('#include "context.h"\ns32 fixture_provider(u8 *buffer,u32 length,SocketView *socket){return (u32)buffer^length^(u32)socket;}\n')
    probes=[]
    for mode in ['thumb','arm']:probes.append(provider_probe(source,directory/(mode+'.o'),mode))
    layouts=[];unit=directory/'caller.c';unit.write_text((ROOT/row['source']).read_text())
    for label,wrong in [('missing-third-word','s32 (*callback38)(u8 *,u32);'),('missing-return-word','void (*callback38)(u8 *,u32,SocketView *);')]:
        (directory/'context.h').write_text(original.replace(signature,wrong));output=directory/(label+'.o');process=compile_source(unit,output,'thumb')
        if process.returncode==0:raise ValueError('Wrong minimum callback interface compiled successfully')
        layouts.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,originalSite=site,wrongSiteContracts=rejected,wrongCallableDeclarations=layouts,typedFixtureProviders=probes,originalGameCallbackIdentityClaimed=False,originalGameOrImportedBodiesExecuted=0,limits=['Fresh typed ARM/Thumb test providers qualify only the controlled fixture address/mode/three-word ABI. They are not original native callbacks or claims about actual game registrations. Runtime models intercept these scripted boundaries before their bodies; the separate compiler ABI probes execute only fresh test code.'])


def compile_source(source,output,mode):
    flags=C.FLAGS[:];flags[0]='-O4,p';flags[flags.index('-inline')+1]='on,noauto';flags+=['-ipa','file','-lang','c99']+(['-thumb'] if mode=='thumb' else [])
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(output)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)


def provider_probe(source,output,mode):
    import unicorn
    from unicorn import arm_const as R
    process=compile_source(source,output,mode)
    if process.returncode:raise ValueError(('Typed callback compiler probe failed',mode,process.stdout,process.stderr))
    with output.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name=='fixture_provider');start=symbol['st_value'];section=symbol['st_shndx'];body=elf.get_section(section).data()[start:start+symbol['st_size']]
        mapping='$t' if mode=='thumb' else '$a'
        if symbol['st_info']['type']!='STT_FUNC' or start&1 or not any(s.name==mapping and s['st_value']==start and s['st_shndx']==section for s in symbols):raise ValueError(('Actual typed callback ELF mapping/type differs',mode,[(s.name,s['st_value']) for s in symbols]))
        if any(sec['sh_info']==section and any(start<=rel['r_offset']<start+symbol['st_size'] for rel in sec.iter_relocations()) for sec in elf.iter_sections() if hasattr(sec,'num_relocations')):raise ValueError('Typed test callback code unexpectedly has relocations')
    address=TARGETS[mode];vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB if mode=='thumb' else unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02500000,0x10000);vm.mem_write(address,body);cases=[]
    triples=[(0,0,0),(0xffffffff,0xffffffff,0xffffffff),(0x02400000,3,0x02401000),(0x80000000,0x12345678,0x7fffffff)]+[(1<<bit,0x89abcdef,0x01234567) for bit in [0,7,15,16,23,31]]
    for args in triples:
        for reg,value in zip(C.REGISTERS,args):vm.reg_write(reg,value)
        vm.reg_write(R.UC_ARM_REG_CPSR,0x30 if mode=='thumb' else 0x10);vm.reg_write(R.UC_ARM_REG_LR,0x02508001 if mode=='thumb' else 0x02508000);vm.reg_write(R.UC_ARM_REG_SP,0x0250f000);vm.emu_start(address|(mode=='thumb'),0x02508000,count=100)
        actual=vm.reg_read(R.UC_ARM_REG_R0);expected=args[0]^args[1]^args[2]
        if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02508000:raise ValueError(('Actual typed callback ABI differs',mode,args,actual,expected))
        cases.append(dict(arguments=list(args),returned=actual))
    return dict(mode=mode,address=hex(address),pointerWord=hex(address|int(mode=='thumb')),compilerSha256=sha256(COMPILER),sourceSha256=sha256(source),objectSha256=sha256(output),ELFMapping=mapping,ELFType='STT_FUNC',sourceCredit=0,actualFreshTestProviderReturns=len(cases),cases=cases,originalGameCallback=False,originalGameOrImportedBodiesExecuted=0)
