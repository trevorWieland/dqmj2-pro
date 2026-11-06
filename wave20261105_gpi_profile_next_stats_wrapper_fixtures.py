import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_stats_wrapper_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_stats_wrapper_build import build

GAME,SET,PLAYERS,TEAMS,NAME,VALUE,GLOBAL,FUNCTION,ARRAY,FORMAT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x21d2514,0x20b2d50,0x20a8644,0x200616c,0x27e0000,0x2701000
DOUBLE={0x20b3780,0x20b3834,0x20b38e4};STRING={0x20b37c4,0x20b3874,0x20b3924};SERVER={0x20b3740,0x20b3780,0x20b37c4};TEAM={0x20b37fc,0x20b3834,0x20b3874};PLAYER={0x20b38ac,0x20b38e4,0x20b3924}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();out={}
    for a in [0x20b3700,0x20b3720]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x20\) addr:0x%08x'%a,x)),None)
        if record is None:raise ValueError('Stats index helper canonical original entry differs')
        out[a]=dict(address=hex(a),mode='thumb',bytes=32,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+32]).hexdigest(),sourceCredit=0)
    if not any(re.fullmatch(r'\S+ kind:function\(thumb,size=0x60\) addr:0x020b2d50',x) for x in inventory.splitlines()):raise ValueError('Stats fixture-supplied bucket function canonical entry differs')
    return out


def vector(a,seed):return dict(mode=seed%3,index=7+seed%9,intValue=(0x11223344+seed)&0xffffffff,doubleBits=[0,0x8000000000000000,0x3ff8000000000000,0x7ff0000000000000,0x7ff8000012345678,0x7ff0000000000001][seed%6])


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);game=bytearray([0x77]*48);struct.pack_into('<I',game,12,SET);struct.pack_into('<II',game,28,PLAYERS,TEAMS);cpu.mem_write(GAME,bytes(game));globals=bytearray([0xa7]*16);struct.pack_into('<I',globals,12,GAME if v['mode']==1 else 0);cpu.mem_write(GLOBAL,bytes(globals));cpu.mem_write(NAME,b'score\0');cpu.mem_write(VALUE,b'value\0');g=GAME if v['mode']==2 else 0;active=v['mode']!=0;fp=FUNCTION if v.get('wrongMode') else FUNCTION|1;scalar=VALUE if a in STRING else v['intValue'];args=[g,v['index']] if a in [0x20b3700,0x20b3720] else [g,NAME,fp,v['doubleBits']&0xffffffff,v['doubleBits']>>32,v['index']] if a in DOUBLE else [g,NAME,fp,scalar,v['index']];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    if a in [0x20b3700,0x20b3720]:expected=dict(kind='provider',address=hex(ARRAY)) if active else dict(kind='return',value=v['index'])
    elif a in SERVER:expected=dict(kind='provider',address=hex(FUNCTION)) if active else dict(kind='return',doubleBits=v['doubleBits']) if a in DOUBLE else dict(kind='return',value=scalar)
    else:expected=dict(kind='provider',address=hex(ARRAY if active else FORMAT))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Stats actual caller return ABI differs')
            observed=dict(kind='return',doubleBits=regs[0]|(regs[1]<<32)) if a in DOUBLE else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [FUNCTION,ARRAY,FORMAT]:
            expected_mode=at!=FORMAT
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=expected_mode:raise ValueError('Stats actual provider/function pointer target mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==ARRAY:
                team=a==0x20b3700 or a in TEAM;interface=regs[:2]==[TEAMS if team else PLAYERS,v['index']]
            elif at==FUNCTION:
                interface=regs[:2]==[SET,NAME]
                if a in STRING:interface=interface and regs[2]==VALUE
                else:
                    desired=struct.pack('<Q',v['doubleBits']) if a in DOUBLE else struct.pack('<I',v['intValue']);interface=interface and SP-0x4000<=regs[2]<SP+4 and bytes(machine.mem_read(regs[2],len(desired)))==desired
            else:
                desired=b'%s_t%d\0' if a in TEAM else b'%s_%d\0';interface=SP-0x4000<=regs[0]<SP and regs[0]+64<=SP and bytes(machine.mem_read(regs[1],len(desired)))==desired and regs[2:4]==[NAME,v['index']]
            machine.emu_stop();return
        helper=next((r for address,r in allowed.items() if address<=at<address+r['bytes']),None)
        if at in allowed and at!=a:calls.append(at)
        if (not a<=at<a+row['bytes'] and helper is None) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Stats escaped bounded actual caller/helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or at+size>SP+4*max(0,len(args)-4):raise ValueError(('Stats unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Stats caller did not reach actual return/provider')
    guards=bytes(cpu.mem_read(GAME,48))==bytes(game) and bytes(cpu.mem_read(GLOBAL,16))==bytes(globals) and bytes(cpu.mem_read(NAME,6))==b'score\0' and bytes(cpu.mem_read(VALUE,6))==b'value\0'
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,allGameGlobalAndInputGuardsPreserved=guards,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[];mode_negative=[]
    variants={0x20b3700:('game->teamnums','game->playernums'),0x20b3740:('#define DoFunc(f,g,n,v,t,r) if(g==NULL)','#define DoFunc(f,g,n,v,t,r) if(g!=NULL)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(36):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent stats game/index/typed parameter frame differs',original,source))
            records.append(original)
        if a in SERVER:
            v=vector(a,2);v['wrongMode']=True
            for label,codebytes in [('native',native),('genuine-source',linked)]:
                try:run(image,row,codebytes,v,2,allowed)
                except ValueError as error:
                    if 'function pointer target mode differs' not in str(error):raise
                    mode_negative.append(dict(caller=row['address'],version=label,rejectedBeforeFunctionBody=True,reason=str(error)))
                else:raise ValueError('Stats even input function pointer not rejected before target body')
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;old,new=variants[a];mutated=folder/'context.h' if a==0x20b3740 else wrong;text=mutated.read_text() if mutated!=wrong else source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError(('Whole stats C did not mutate',row['address'],old))
        mutated.write_text(changed)
        if mutated!=wrong:shutil.copyfile(source,wrong)
        bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong stats C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,2);result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong stats C did not violate independent array/value frame')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],mutatedConsumedHeaderSha256=sha256(mutated) if mutated!=wrong else None,actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Eleven complete ordinary C stats game/index/op wrappers genuinely link with original BL/BLX/data words. Source uses48-byte primary statsgame layout; actual g_statsgame pointer is4-byte field12 of canonical BSS base021d2514 minimum16-byte view, not a rebound base pointer. Five actual original LDR field instructions and compiler geometry revalidate.0storage/extent/authorship credit.','396 paired vectors test missing/default/explicit game selection, opaque team/player index and int/double/string argument/return frames against independent models. Double no-game fallback returns raw64bits including signed zero/NaN without numeric operations. Existing original32-byte index helpers execute; arrays, canonical bucket callback and ARM formatter stop BEFORE bodies.0synthetic provider returns/format/table/heap effects.','Two complete same-extent wrong-C variants genuinely link and violate32 actual frame models. Six even fixture function pointer negatives reject native/source mode BEFORE any target body; fixture inputs are not original callback storage evidence. Eleven wrong global-field-offset layouts reject under pinned compiler.','No array result, callback operation result, formatter output, network, hardware, whole game or native Windows execution is inferred. Primary source semantic names are comparative labels after exact full native caller proof.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,wrongFixturePointerModesRejected=mode_negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
