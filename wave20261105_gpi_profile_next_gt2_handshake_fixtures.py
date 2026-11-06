import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_gt2_handshake_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_gt2_handshake_build import build

CONNECTION,MESSAGE,CALLBACKS,CHECK,STRLEN,HEAP,CHALLENGE,ACCEPT,REJECT,STOP,SP=0x2170000,0x2171000,0x2172000,0x20b6094,0x201d69c,0x20a927c,0x20b39c4,0x20b55d4,0x20b5614,0x27e0000,0x2701000
START,ACCEPT_CALLER,REJECT_CALLER=0x20b402c,0x20b409c,0x20b40d8


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();relocs=(ROOT/'config/arm9/relocs.txt').read_text();out={}
    for a,n,mode in [(CHECK,48,'thumb'),(STRLEN,28,'arm')]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),x)),None)
        if record is None:raise ValueError('Actual canonical handshake normalization helper differs')
        out[a]=dict(address=hex(a),mode=mode,bytes=n,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+n]).hexdigest(),sourceCredit=0)
    empty=struct.unpack('<I',image[CHECK-0x2000000+44:CHECK-0x2000000+48])[0];original=f'from:0x020b60c0 kind:load to:0x{empty:08x} module:main';data=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x%08x'%empty,x)),None)
    if original not in relocs.splitlines() or data is None or image[empty-0x2000000]!=0:raise ValueError('Original MessageCheck empty-literal kind/target/byte differs')
    out[CHECK]['emptyStringLiteral']=dict(origin='0x20b60c0',target=hex(empty),actualAbs32Word=image[CHECK-0x2000000+44:CHECK-0x2000000+48].hex(),originalRecord=original,canonicalDataRecord=data,minimumBytes=1,minimumSha256=hashlib.sha256(bytes(1)).hexdigest(),storageExtentAuthorshipCredit=0)
    return out,empty


def vector(a,seed):return dict(state=seed%8,freeFlag=(seed//8)&1,callbackPresent=seed%3!=0,messagePresent=seed%4!=0,length=[-1,0,1,12][(seed//4)%4])


def run(image,row,body,v,seed,allowed,empty):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);conn=bytearray([0x66]*160);put=lambda off,value:struct.pack_into('<I',conn,off,value);put(12,v['state']);put(20,v['freeFlag']);cpu.mem_write(CONNECTION,bytes(conn));message=b'handshake-message\0';cpu.mem_write(MESSAGE,message);callbacks=struct.pack('<4I',0x20b2d51,0x200616c,0,0x20b2d51);cpu.mem_write(CALLBACKS,callbacks);expected_conn=bytearray(conn);pointer=MESSAGE if v['messagePresent'] else 0;cb=CALLBACKS if v['callbackPresent'] else 0;normalized=pointer if pointer else empty;length=(len(message) if v['length']==-1 else v['length']) if pointer else 0;provider_args=[]
    if a==START:
        args=[CONNECTION,pointer,v['length'],cb]
        if length>0:expected=dict(kind='provider',address=hex(HEAP));provider_args=[length]
        else:
            if cb:expected_conn[40:56]=callbacks
            expected=dict(kind='provider',address=hex(CHALLENGE))
    elif a==ACCEPT_CALLER:
        args=[CONNECTION,cb];struct.pack_into('<I',expected_conn,20,0)
        if v['freeFlag'] or v['state']!=4:expected=dict(kind='return',value=0)
        else:expected=dict(kind='provider',address=hex(ACCEPT));provider_args=[CONNECTION]
    else:
        args=[CONNECTION,pointer,v['length']];struct.pack_into('<I',expected_conn,20,0)
        if v['state']!=4:expected=dict(kind='return')
        else:expected=dict(kind='provider',address=hex(REJECT));provider_args=[CONNECTION,normalized,length&0xffffffff]
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Handshake actual return ABI differs')
            observed=dict(kind='return',value=regs[0]) if 'value' in expected else dict(kind='return');machine.emu_stop();return
        if at in [HEAP,CHALLENGE,ACCEPT,REJECT]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Handshake actual provider target mode differs')
            observed=dict(kind='provider',address=hex(at));regs=[machine.reg_read(r) for r in C.REGISTERS];interface=regs[:len(provider_args)]==provider_args
            if at==CHALLENGE:interface=interface and SP-0x4000<=regs[0]<SP and regs[0]+32<=SP
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed:calls.append(at)
        wanted='thumb' if a<=at<a+row['bytes'] else helper['mode'] if helper else None;mode='thumb' if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else 'arm'
        if wanted is None or mode!=wanted:raise ValueError(('Handshake escaped bounded original normalization helper/mode',hex(at),mode,wanted))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP) and not(CONNECTION<=at and at+size<=CONNECTION+160):raise ValueError(('Handshake unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Handshake did not reach actual return/provider')
    memory=bytes(cpu.mem_read(CONNECTION,160))==bytes(expected_conn) and bytes(cpu.mem_read(MESSAGE,len(message)))==message and bytes(cpu.mem_read(CALLBACKS,16))==callbacks
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and memory and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=memory,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed,empty=helpers(image);records=[];negative=[];variants={START:('if(callbacks)','if(!callbacks)'),ACCEPT_CALLER:('if(connection->freeAtAcceptReject)','if(!connection->freeAtAcceptReject)'),REJECT_CALLER:('connection->state != GTI2AwaitingAcceptReject','connection->state != GTI2Connected')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(64):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed,empty);source=run(image,row,linked,v,seed,allowed,empty)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent handshake normalization/state/frame differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole handshake wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong handshake C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v.update(state=4,freeFlag=1,callbackPresent=True,messagePresent=False,length=0);result=run(image,row,body,v,seed,allowed,empty)
            if result['modelPassed']:raise ValueError('Wrong handshake C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Three complete ordinary C GT2 start/accept/reject functions genuinely match complete extents and original native imports. Compiler geometry independently proves160-byte connection and16-byte callbacks including state12/freeFlag20/callbacks40/initialMessage56/len60/response104 and state enum values.','192paired actual entry vectors independently model flags/state gates,16-byte callback copying on zero-length start paths, normalization and provider argument frames. Original MessageCheck48 and ARMstrlen28 execute unchanged. Measured NULLmessage rewrites to exact original empty literal and len0; nonnull len-1 becomes strlen+1 includingNUL. Original helper/literal boundaries/kinds/words validated;0helper/data storage or source credit.','Heap/challenge generation/sendAccept/sendReject stop BEFORE bodies;0synthetic returns,allocations,random/challenge/network operations. Successful accept/reject post-send state transitions and start final state remain byte-exact yet runtime-unexecuted. All real no-send early returns modeled.','Three same-extent whole wrong-C variants genuinely link and violate48 independent frame/mutation/state models.3wrong layouts plus original call namespace/mode/kind/addend/entry/opcode controls reject. No complete game/nativeWindows/hardware execution inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
