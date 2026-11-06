import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gp_api_next_compat_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_compat_build import build

CONN,OBJECT,PROFILE,LEGACY,EXTENDED,STATUS,S1,S2,MSG,PARAM,APP,STOP,SP=0x216f000,0x2170000,0x2171000,0x2172000,0x2172100,0x2173000,0x2174000,0x2175000,0x2176000,0x12345678,0x20acbcc,0x27e0000,0x2701000
PROVIDERS={APP,0x20ade3c,0x20af244,0x20b0c2c,0x20abfe4}


def helpers(image):
    text=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for a,mode,size in [(0x201b208,'arm',20),(0x201b288,'arm',176),(0x201d780,'arm',80),(0x20b2a38,'thumb',20),(0x20b2c88,'thumb',16)]:
        record=next((x for x in text.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,size,a),x)),None)
        if record is None:raise ValueError('Measured RAM memset/string helper canonical entry differs')
        result[a]=dict(address=hex(a),mode=mode,bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    canonical=next((x for x in text.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x5c\) addr:0x020acbcc',x)),None)
    if canonical is None:raise ValueError('Fixture-supplied application callback lacks actual canonical entry')
    return result,canonical


def vector(a,seed,suffix=False):
    case=seed%8
    return dict(case=case,connectionNull=case==0,objectNull=case==1,simulation=case==2,callbackNull=case==5,profile=0 if case==6 else 17,index=-1 if case==6 else 2,outputNull=case==7,disconnected=case==3,messageNull=case==6,extendedPresent=seed%3!=0,extendedState=0 if seed%2==0 else 3,stringNull=seed%4,sourceLength=[0,1,255,300][seed%4],suffix=suffix)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);suffix=v['suffix'];cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);obj=bytearray([0xa7]*0x5d8);struct.pack_into('<I',obj,0x108,int(v['simulation']));struct.pack_into('<I',obj,0x1f4,4 if v['disconnected'] else 3);struct.pack_into('<I',obj,0x5d0,4);cpu.mem_write(OBJECT,bytes(obj));cpu.mem_write(CONN,struct.pack('<I',0 if v['objectNull'] else OBJECT));output=bytearray([0xa6]*532);cpu.mem_write(STATUS,bytes(output));profile=bytearray([0x73]*44);struct.pack_into('<IIII',profile,0,0x1234,7,LEGACY,EXTENDED if v['extendedPresent'] else 0);cpu.mem_write(PROFILE,bytes(profile));legacy=bytearray([0x91]*28);struct.pack_into('<IIIIII',legacy,0,2,0x7007,0 if v['stringNull']==0 else S1,0 if v['stringNull']==1 else S2,0x01020304,0x0000abcd);struct.pack_into('<I',legacy,24,5);cpu.mem_write(LEGACY,bytes(legacy));extended=bytearray([0x81]*60);struct.pack_into('<I',extended,4,v['extendedState']);struct.pack_into('<I',extended,28,0x11223344);struct.pack_into('<H',extended,32,0xcdef);struct.pack_into('<I',extended,48,9);cpu.mem_write(EXTENDED,bytes(extended));s1=b'A'*v['sourceLength']+b'\0';s2=b'B'*v['sourceLength']+b'\0';cpu.mem_write(S1,s1);cpu.mem_write(S2,s2);cpu.mem_write(MSG,b'msg\0');c=0 if v['connectionNull'] else CONN;callback=0 if v['callbackNull'] else APP|1;status=0 if v['outputNull'] else STATUS;message=0 if v['messageNull'] else MSG;args={0x20aa068:[c],0x20aa100:[c,v['profile'],0x501,0x401,callback,PARAM],0x20aa3e0:[c,v['index'],status],0x20aa7c0:[c,17,message]}[a];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    saved=list(initial);start=a;expected_obj=bytearray(obj);expected_output=bytearray(output);error=None;expected=None
    if suffix:
        initial[4:7]=[PROFILE,STATUS,CONN];initial[13]=SP-16;cpu.mem_write(SP-16,struct.pack('<IIII',saved[4],saved[5],saved[6],STOP|1));start=a+0x6a;expected=dict(kind='suffix-epilogue',value=0)
        if v['extendedPresent'] and v['extendedState']==0:
            struct.pack_into('<II',expected_output,0,0x1234,0);expected_output[8]=0;expected_output[264]=0;struct.pack_into('<III',expected_output,520,0x11223344,0xcdef,9)
        else:
            struct.pack_into('<II',expected_output,0,0x1234,0x7007)
            for offset,string,isnull in [(8,s1,v['stringNull']==0),(264,s2,v['stringNull']==1)]:
                if isnull:expected_output[offset]=0
                else:expected_output[offset:offset+256]=string[:-1][:255].ljust(255,b'\0')+b'\0'
            struct.pack_into('<III',expected_output,520,0x01020304,0xabcd,5)
    elif v['connectionNull'] or v['objectNull']:expected=dict(kind='return',void=True) if a==0x20aa068 else dict(kind='return',value=2)
    elif a==0x20aa068:expected=dict(kind='return',void=True) if v['simulation'] else dict(kind='provider',address=hex(0x20ade3c))
    elif a==0x20aa100:
        if not v['profile']:expected=dict(kind='return',value=2)
        elif not callback:error=b'No callback.';expected=dict(kind='return',value=2)
        elif v['simulation']:expected=dict(kind='provider',address=hex(APP))
        elif v['disconnected']:error=b'The connection has already been disconnected.';expected=dict(kind='return',value=2)
        else:expected=dict(kind='provider',address=hex(0x20af244))
    elif a==0x20aa3e0:
        if v['simulation']:expected=dict(kind='return',value=0);expected_output[:]=bytes(532)
        elif not status:error=b'Invalid status.';expected=dict(kind='return',value=2)
        elif v['index']<0:error=b'Invalid index.';expected=dict(kind='return',value=2)
        else:expected=dict(kind='provider',address=hex(0x20b0c2c))
    else:
        if v['simulation']:expected=dict(kind='return',value=0)
        elif v['disconnected']:error=b'The connection has already been disconnected.';expected=dict(kind='return',value=2)
        elif not message:error=b'Invalid message.';expected=dict(kind='return',value=2)
        else:expected=dict(kind='provider',address=hex(0x20abfe4))
    if error is not None:expected_obj[:256]=error[:255].ljust(255,b'\0')+b'\0'
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=saved[4:12] or regs[13]!=SP:raise ValueError('Compatibility caller/suffix measured saved frame differs')
            observed=dict(kind='suffix-epilogue',value=regs[0]) if suffix else dict(kind='return',void=True) if a==0x20aa068 else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Compatibility actual provider/callback target mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==APP:interface=regs[0]==CONN and regs[2]==PARAM and bytes(machine.mem_read(regs[1],516))==bytes(516)
            elif at==0x20af244:interface=regs[:4]==[CONN,17,0x501,0x401] and bytes(machine.mem_read(regs[13],8))==struct.pack('<II',APP|1,PARAM)
            elif at==0x20ade3c:interface=regs[:2]==[CONN,1]
            elif at==0x20b0c2c:interface=regs[:2]==[CONN,2]
            elif at==0x20abfe4:interface=regs[:4]==[CONN,17,1,MSG] and bytes(machine.mem_read(regs[13],8))==bytes(8)
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed:calls.append(at)
        mode='thumb' if a<=at<a+row['bytes'] else helper['mode'] if helper else None
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError(('Compatibility escaped original caller/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4) or OBJECT<=at and at+size<=OBJECT+256 or STATUS<=at and at+size<=STATUS+532):raise ValueError(('Compatibility unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(start|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Compatibility did not reach actual return/suffix/provider')
    guards=bytes(cpu.mem_read(OBJECT,len(obj)))==bytes(expected_obj) and bytes(cpu.mem_read(STATUS,532))==bytes(expected_output) and bytes(cpu.mem_read(PROFILE,44))==bytes(profile) and bytes(cpu.mem_read(LEGACY,28))==bytes(legacy) and bytes(cpu.mem_read(EXTENDED,60))==bytes(extended)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',partialSuffixEpilogueReached=observed['kind']=='suffix-epilogue',entryAddress=hex(start),partialSuffixIsNotFunctionEntry=suffix,modelPassed=observed==expected and interface and guards,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,connectionOutputAndInputGuardsPreserved=guards,statusSha256=hashlib.sha256(bytes(cpu.mem_read(STATUS,532))).hexdigest(),objectSha256=hashlib.sha256(bytes(cpu.mem_read(OBJECT,len(obj)))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed,canonical=helpers(image);records=[];negative=[]
    context=read_json(LANE/'measured-suffix-context.json')
    if (context['program'],context['processor'],context['module'],context['mode'],context['parentEntry'],context['parentBytes'],context['suffixEntry'],context['suffixIsNotFunctionEntry'],context['addedBindingEntries'])!=('','arm9','main','thumb','0x020aa3e0',272,'0x020aa44a',True,0):raise ValueError('Explicit partial suffix namespace/frame identity differs')
    if context['moduleSha256']!=hashlib.sha256(image).hexdigest() or context['parentSha256']!=hashlib.sha256(image[0xaa3e0:0xaa3e0+272]).hexdigest() or context['lookupAndNonzeroJoinBytes']!=image[0xaa436:0xaa44a].hex() or context['originalPrologBytes']!=image[0xaa3e0:0xaa3e6].hex():raise ValueError('Explicit partial suffix original body/prolog/nonzero join changed')
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for suffix,count in [(False,48),*([(True,48)] if a==0x20aa3e0 else [])]:
            for seed in range(count):
                v=vector(a,seed,suffix);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
                if original!=source or not original['modelPassed']:raise ValueError(('Independent compatibility query/status/frame model differs',original,source))
                records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new={0x20aa068:('if(iconnection->simulation)return;','if(!iconnection->simulation)return;'),0x20aa100:('(profile == 0)','(profile != 0)'),0x20aa3e0:('statusState==0','statusState!=0'),0x20aa7c0:('connectState == GPI_DISCONNECTED','connectState != GPI_DISCONNECTED')}[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole compatibility C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong compatibility C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,4,a==0x20aa3e0)
            if a==0x20aa3e0:v.update(extendedPresent=True,extendedState=0,stringNull=0)
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong compatibility C did not violate independent query/status/frame model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] or r['partialSuffixEpilogueReached'] for r in failures),records=failures))
    limits=['Four ordinary C complete native extents genuinely link with original branches/data witnesses; full516-byte info response uses genuine C aggregate-zero initialization. Native compatibility branch preserves extended-status state0 fallback in the legacy532-byte output, absent later public source. Disconnect omits later public old-state restoration because original36-byte caller has no such path.','192 caller-entry vectors compare actual native/genuine source error/simulation/ABI/provider frames. Additional48 measured post-lookup suffix vectors at020aa44a compare real native/source compatibility field copies, string truncation/empty cases and original RAM helper bodies. Suffix executions start with explicitly supplied register/saved-stack preconditions after the original lookup and do NOT count as complete caller executions or recovered entrypoints.','Actual original canonical ARM memset20+176, strncpy80 and Thumb error/string16+20 execute on bounded RAM only. Allocation, lookup, connection/message/query and fixture-supplied canonical application callback entries stop BEFORE provider bodies, with0 synthetic returns/network/hardware. Callback argument516 bytes are checked all-zero before execution.','Four same-extent whole C variants violate64 independent simulation/profile/fallback/disconnect state models. Wrong legacy status-array layout rejects by actual compiler geometry. No object storage/helper-source credit, native Windows/game scenes, provider return semantics, complete network or callback behavior proved.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),nativeAndCompiledPartialSuffixExecutions=2*sum(r['partialSuffixEpilogueReached'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),fixtureSuppliedCanonicalCallbackEntry=canonical,fixtureCallbackPointerIsNotOriginalStorageEvidence=True,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
