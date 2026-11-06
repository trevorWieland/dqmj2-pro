import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_first_build import build
from wave20261106_dwc_match_next_first_error_helper import execute as qualify_error

LOGIN,UPDATE,FRIENDS,SETCB,CLOSEALL,CLOSEONE,AID,VALID,STATE,SETSTATE,DELETE,BITMAP,UPDATED=0x209b898,0x209b940,0x209ba08,0x209bb10,0x209bb30,0x209bba0,0x209bbe4,0x209bc5c,0x209bc88,0x209be60,0x209be74,0x209beac,0x209c034
ERROR,ERRWORD,GLOBAL=0x209a9e4,0x21d19ac,0x21d19e0
CON,TEXT,NAME,PARAM,SOCKET,STOP,SP,CALLBACK=0x2171000,0x2176000,0x2176400,0x2177000,0x2178000,0x27e0000,0x2701000,0x27e0200
ISSTATUS,CLEAR16,INET,CLEARCON,STATUSCALL,CLOSEHARD,GETCON,VALIDCALL,GETLIST,CHANGESTATE=0x209ad08,0x2008be0,0x209ad08,0x209bd94,0x209d1c8,0x20b4540,0x209bd20,0x209be20,0x209f680,SETSTATE
PROVIDERS={CLEAR16:'arm',INET:'thumb',CLEARCON:'thumb',STATUSCALL:'thumb',CLOSEHARD:'thumb',GETCON:'thumb',VALIDCALL:'thumb',GETLIST:'thumb',SETSTATE:'thumb',CALLBACK:'thumb'}


def vector(seed):
    return dict(present=seed%4!=0,error=[0,0,1,0xffffffff,0x80000000][seed%5],state=[0,3,4,5,6,1,-1,0x7fffffff][seed%8],last=[4,0,3,5,-1][seed%5],newState=[0,3,4,5,6,-1,0x7fffffff][seed%7],aid=seed%32,bitmap=[0,0xffffffff,1<<(seed%32),1<<((seed+1)%32)][seed%4],count=seed%3,emptyName=seed%3==0,nullName=seed%5==0,values=[seed%32,seed%32,(seed+31)%32,0,31,4,8,16,7],length=[-1,0,1,2,5,9][seed%6])


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    present=v['present'] if a in [SETCB,AID,VALID,STATE,CLOSEALL,CLOSEONE] else True
    context=bytearray([0x6d])*0x800
    for offset,value in [(0,SOCKET),(0x24,v['state']),(0x28,v['last']),(0x70,CALLBACK|1),(0x74,PARAM+16),(0x78,CALLBACK|1),(0x7c,PARAM+32),(0x90,CALLBACK|1),(0x94,PARAM+48),(0x668,v['bitmap'])]:struct.pack_into('<I',context,offset,value&0xffffffff)
    context[0x2c]=v['aid'];context[0x2d]=seed%2;context[0x385]=v['count']
    text=bytes(v['values']);name=struct.pack('<H',0 if v['emptyName'] else [65,0xd800,0xffff,1][seed%4])+bytes(50)
    memory={GLOBAL:struct.pack('<I',CON if present else 0),ERRWORD:struct.pack('<I',v['error']&0xffffffff),CON:bytes(context),TEXT:text,NAME:name}
    for at,data in memory.items():cpu.mem_write(at,data)
    expected_memory=dict(memory);changed=bytearray(context);expected_helpers=0;args=[];expected_frame=None;expected=dict(kind='return')
    if a==LOGIN:
        args=[0 if v['nullName'] else NAME,PARAM+100,CALLBACK|1,PARAM]
        if v['nullName']:expected=dict(kind='return',value=0)
        else:
            expected_helpers=1
            if v['error'] or v['state']!=0:expected=dict(kind='return',value=0)
            else:
                struct.pack_into('<II',changed,0x70,CALLBACK|1,PARAM)
                if v['emptyName']:struct.pack_into('<H',changed,0x2e,0);expected=dict(kind='provider',address=hex(INET))
                else:expected=dict(kind='provider',address=hex(CLEAR16));expected_frame=[0,CON+0x2e,52]
    elif a==UPDATE:
        args=[PARAM+100,CALLBACK|1,PARAM,CALLBACK|1,PARAM+4,CALLBACK|1,PARAM+8];expected_helpers=1
        if v['error'] or v['state']<3 or v['state']==4:expected=dict(kind='return',value=0)
        else:struct.pack_into('<II',changed,0x78,CALLBACK|1,PARAM);expected=dict(kind='provider',address=hex(SETSTATE));expected_frame=[4]
    elif a==FRIENDS:
        args=[TEXT,3,4,1,CALLBACK|1,PARAM,CALLBACK|1,PARAM+4];expected_helpers=1;expected=dict(kind='return',value=0) if v['error'] or v['state']!=3 else dict(kind='provider',address=hex(CLEARCON))
    elif a==SETCB:
        args=[CALLBACK|1,PARAM];expected=dict(kind='return',value=int(present))
        if present:struct.pack_into('<II',changed,0x90,CALLBACK|1,PARAM)
    elif a in [CLOSEALL,CLOSEONE]:
        args=[] if a==CLOSEALL else [v['aid']];expected_helpers=int(present)
        if not present or v['error'] or v['state'] not in [5,6]:expected=dict(kind='return',value=0xffffffff)
        elif a==CLOSEONE:expected=dict(kind='provider',address=hex(GETCON));expected_frame=[v['aid']]
        elif v['count']==0:expected=dict(kind='provider',address=hex(STATUSCALL));expected_frame=[1,0x20e016c,0]
        else:changed[0x2d]=1;expected=dict(kind='provider',address=hex(CLOSEHARD));expected_frame=[SOCKET]
    elif a==AID:expected=dict(kind='return',value=v['aid'] if present else 0)
    elif a==STATE:expected=dict(kind='return',value=(v['state']&0xffffffff) if present else 0)
    elif a==SETSTATE:args=[v['newState']];struct.pack_into('<II',changed,0x24,v['newState']&0xffffffff,v['state']&0xffffffff)
    elif a==VALID:
        args=[v['aid']];expected=dict(kind='provider',address=hex(VALIDCALL)) if present and v['bitmap']&(1<<v['aid']) else dict(kind='return',value=0)
        if expected['kind']=='provider':expected_frame=[v['aid']]
    elif a==DELETE:args=[v['aid']];expected=dict(kind='provider',address=hex(GETLIST));expected_frame=[SP-16]
    elif a==BITMAP:
        args=[TEXT,v['length']];value=0
        for item in v['values'][:max(0,v['length'])]:value|=1<<item
        expected=dict(kind='return',value=value)
    else:
        args=[seed,seed%2,PARAM+100]
        if v['last']!=4:expected=dict(kind='provider',address=hex(SETSTATE));expected_frame=[v['last']&0xffffffff]
        else:expected=dict(kind='provider',address=hex(CALLBACK));expected_frame=[seed,seed%2,PARAM+32]
    expected_memory[CON]=bytes(changed);initial=[(0x61a00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args[:4]):initial[i]=arg&0xffffffff
    for i,arg in enumerate(args[4:]):cpu.mem_write(SP+i*4,struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;helper_count=0;helper_return=None;helper_saved=None;helper_checked=0
    def code(machine,at,size,user):
        nonlocal observed,interface,helper_count,helper_return,helper_saved,helper_checked
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[0]!=int(v['error']!=0) or regs[4:12]!=helper_saved[0] or regs[13]!=helper_saved[1]:raise ValueError('Actual original error leaf predicate/ABI failed inside caller')
            helper_checked+=1;helper_return=None
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual DWC caller return ABI differs')
            observed=dict(kind='return') if a==SETSTATE else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at==ERROR:helper_count+=1;helper_return=regs[14]&~1;helper_saved=(regs[4:12],regs[13])
        if ERROR<=at<ERROR+16:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual original error helper mode differs')
            return
        if at in PROVIDERS and at!=a:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual DWC provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=expected_frame is None or regs[:len(expected_frame)]==expected_frame;machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('DWC caller escaped bounded genuine body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if CON<=at and at+size<=CON+len(context):return
        raise ValueError('Unexpected DWC caller write outside scoped RAM/stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000)
    if observed is None:raise ValueError('DWC caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items());helpers=helper_count==helper_checked==expected_helpers
    return dict(address=row['address'],seed=seed,vector=v,expected=expected,observed=observed,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=helper_count,originalHelperBooleanAndAbiPassed=helpers,providerInstructionExecutions=0,modelPassed=observed==expected and interface and guards and helpers,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);helper=qualify_error();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={LOGIN:('ingamesn == NULL','ingamesn != NULL'),UPDATE:('state < DWC_STATE_ONLINE','state <= DWC_STATE_ONLINE'),FRIENDS:('state != DWC_STATE_ONLINE','state == DWC_STATE_ONLINE'),SETCB:('closedParam = param','closedParam = (void*)callback'),CLOSEALL:('return -1;','return -2;'),CLOSEONE:('return -1;','return -2;'),AID:('return 0;','return 1;'),STATE:('return DWC_STATE_INIT;','return (DWC_STATE_INIT+1);'),SETSTATE:('lastState = stpDwcCnt->state','lastState = state'),VALID:('return FALSE;','return TRUE;'),DELETE:('DWCi_GetAllAIDList(&pAidList)','DWCi_GetAllAIDList(&pAidList+1)'),BITMAP:('bitmap |=','bitmap ^='),UPDATED:('stpDwcCnt->updateServersParam','stpDwcCnt->loginParam')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent DWC state/mutation/provider model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole DWC wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True);failures=[]
        for seed in range(16):
            v=vector(seed);v.update(present=a==SETCB,nullName=True,error=0,state=3,last=4,newState=11,bitmap=0,values=[5,5,1,0,31,4,8,16,7],length=2)
            result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError(('Whole DWC wrong-C accepted independent model',row['address'],result))
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Thirteen complete ordinary C DWC main/control callers978B genuinely link at every original complete Thumb extent, BL/BLX origin/mode, callback Thumb tag and external BSS/data literal. Prefix declarations prove only used minimum fields; all external storage extent/authorship remains zero credit.','1664paired actual function entries independently model RAM-only null/getter/callback-store/state-update/bitmap returns, error/state gates and bounded original side effects before actual provider transfers. Only the original20-byte canonical Thumb nonzero-error predicate executes as a callee; its32 standalone original entries and12 identity/native negatives qualify the exact body. No synthetic returns are injected.','All other memory/string/Internet/state-transition/login/friend/GT2/provider/callback bodies and following control paths remain unexecuted; provider instructions execute0. Bitmap vectors restrict shift counts to0..31 and use explicit unsigned source1u.0network/device/game/nativeWindows execution.13complete genuinely linked wrong-C variants reject208independent models; actual used field/enum layout and unchanged native binding negatives qualify separately.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),standaloneOriginalErrorHelperEntries=helper['standaloneOriginalEntries'],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
