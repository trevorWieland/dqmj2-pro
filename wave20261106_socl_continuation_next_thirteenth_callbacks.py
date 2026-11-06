import copy
import hashlib
from project import ROOT,sha256
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

TARGETS={('allocate','thumb'):0x02500100,('allocate','arm'):0x02500200,('release','thumb'):0x02500300,('release','arm'):0x02500400}
CONTRACTS={
 '02092380-allocate':dict(caller='02092380',literal=0x2092464,load=0x2092388,call=0x209238e,slot=0x21cfd0c,target='r1',argumentWords=1,returnWords=1,kind='allocate'),
 '02092380-release':dict(caller='02092380',literal=0x209246c,load=0x209245c,call=0x209245e,slot=0x21cfd38,target='r1',argumentWords=1,returnWords=0,kind='release')}
INSTRUCTIONS={
 '02092380-allocate':{0x2092384:('ldr','r1, [pc, #0xdc]'),0x2092388:('ldr','r1, [r1]'),0x209238a:('movs','r0, #0x83'),0x209238c:('ldr','r5, [r6, #0xc]'),0x209238e:('blx','r1'),0x2092390:('adds','r4, r0, #0')},
 '02092380-release':{0x2092458:('ldr','r1, [pc, #0x10]'),0x209245a:('adds','r0, r4, #0'),0x209245c:('ldr','r1, [r1]'),0x209245e:('blx','r1')}}


def verify_site(name,contract,image,entry):
    if name not in CONTRACTS or contract!=CONTRACTS[name]:raise ValueError('Exact original dynamic callback contract differs')
    address=int(contract['caller'],16);body=image[address-0x02000000:address-0x02000000+entry['bytes']]
    if hashlib.sha256(body).hexdigest()!=entry['targetSha256']or entry['address']!=hex(address)or entry['mode']!='thumb':raise ValueError('Whole original callback caller changed')
    decoded={i.address:(i.mnemonic,i.op_str)for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(body,address)}
    if any(decoded.get(a)!=pair for a,pair in INSTRUCTIONS[name].items()):raise ValueError('Original callback slot load/BLX/result flow differs')
    record=f"from:0x{contract['literal']:08x} kind:load to:0x{contract['slot']:08x} module:main"
    if record not in entry['originalRelocationRecords']or int.from_bytes(image[contract['literal']-0x02000000:contract['literal']-0x02000000+4],'little')!=contract['slot']:raise ValueError('Original callback data-slot literal/origin differs')
    if any(line.startswith('from:0x'+format(contract['call'],'08x')+' ')for line in entry['originalRelocationRecords']):raise ValueError('Dynamic callback is not an encoded original callee')
    return dict(caller=entry['address'],nativeSha256=entry['targetSha256'],contract=contract,instructions=[dict(address=hex(a),mnemonic=m,operands=o)for a,(m,o)in INSTRUCTIONS[name].items()],originalLiteralRecord=record,originalRuntimeTargetClaimed=False,calleeSourceCredit=0)


def execute(rows):
    from wave20261106_socl_continuation_next_thirteenth_bindings import inputs,VIEWS,callback_view
    from wave20261106_socl_continuation_next_thirteenth_controls import compile_source
    from wave20261105_socket_thumb_next_twelfth_callbacks import provider_probe
    import wave20261105_socket_thumb_next_twelfth_callbacks as old
    directory=ROOT/'work/w6sc/thirteenth-callback-controls';directory.mkdir(parents=True,exist_ok=True);value,image,inventory,records,imports=inputs();sites=[];negatives=[]
    for name,contract in CONTRACTS.items():
        entry=next(e for e in value['entries']if int(e['address'],0)==int(contract['caller'],16));sites.append(verify_site(name,contract,image,entry))
        for key,wrong in [('literal',contract['literal']+4),('slot',contract['slot']+4),('load',contract['load']+2),('call',contract['call']+2),('target','r2'),('argumentWords',2),('returnWords',1-contract['returnWords'])]:
            variant=dict(contract);variant[key]=wrong
            try:verify_site(name,variant,image,entry)
            except ValueError as error:negatives.append(dict(caller=name,case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong original dynamic callback interface admitted')
        changed=bytearray(image);changed[contract['call']-0x02000000]^=1
        try:verify_site(name,contract,bytes(changed),entry)
        except ValueError as error:negatives.append(dict(caller=name,case='original-code',rejected=True,reason=str(error)))
        else:raise ValueError('Changed original callback caller admitted')
    slot_negatives=[]
    for target,view in VIEWS.items():
        row=next(r for r in rows if any(int(rel['target'],0)==target for rel in r['relocations']))
        for key,wrong in [('width',2),('minimumBytes',8),('storage','data'),('initializedBytes',4),('interface','void*(void*)'),('type','original-callback-target')]:
            bad=dict(view);bad[key]=wrong
            try:callback_view(row,image,target,bad)
            except ValueError as error:slot_negatives.append(dict(slot=hex(target),case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong BSS callback access/interface admitted')
    source=directory/'providers.c';source.write_text('typedef unsigned long u32;\nvoid *fixture_allocate(u32 size){return (void *)(size^0x02405000);}\nvoid fixture_release(unsigned char *pointer){*pointer^=0x5a;}\nint fixture_handler(void *command){return (u32)command^0x89abcdef;}\n')
    previous=old.compile_source
    def pinned(unit,obj,mode):return compile_source(unit,obj,[f for f in rows[0]['compilerFlags']if f!='-thumb']+(['-thumb']if mode=='thumb'else []))
    try:
        old.compile_source=pinned;probes=[provider_probe(source,directory/(mode+'.o'),mode)for mode in ['thumb','arm']]
    finally:old.compile_source=previous
    text=(ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/thirteenth/context.h').read_text();bad=[]
    for label,oldtext,newtext,caller in [('allocator-argument','(*native_data_021cfd0c)(u32)','(*native_data_021cfd0c)(void)','02092380'),('allocator-return','void *(*native_data_021cfd0c)','void (*native_data_021cfd0c)','02092380'),('release-argument','(*native_data_021cfd38)(void *)','(*native_data_021cfd38)(void)','02092380')]:
        if text.count(oldtext)!=1:raise ValueError('Actual callback declaration mutation ambiguous')
        (directory/'context.h').write_text(text.replace(oldtext,newtext));unit=directory/(label+'.c');unit.write_text((ROOT/('src/runtime/parallel_wave20261105/socl-continuation-next/thirteenth/'+caller+'.c')).read_text());process=compile_source(unit,directory/(label+'.o'),rows[0]['compilerFlags'])
        if process.returncode==0:raise ValueError('Wrong actual callback declaration accepted')
        bad.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    return dict(status='passed',sourceCredit=0,originalSites=sites,negativeOriginalSiteControls=negatives,negativeSlotViewControls=slot_negatives,actualWrongCallableDeclarations=bad,actualFreshControlledProviderAbi=probes,originalCallbackIdentitiesClaimed=False,originalNativeCallbackBodiesExecuted=0,limits=['The reused frozen ABI probe also executes an unused controlled handler prototype as diagnostic collateral; it is not a native callback or credited source. Actual caller fixtures intercept controlled allocator/release providers before body execution.'])
