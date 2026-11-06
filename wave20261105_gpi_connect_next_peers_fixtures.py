import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peers_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_peers_build import build

DISPATCH,REMOVE=0x20b0250,0x20b02cc
INIT,ACCEPT,CONNECTED,ARRAYLEN=0x20afbc8,0x20afdcc,0x20affbc,0x20a8640
ARRAYS=0x2177000
FIND,CREATE,CONNECT,MESSAGE=0x20b03c4,0x20b0404,0x20b049c,0x20b0534
MALLOC,GETPROFILE,STRLEN=0x20a927c,0x20b0a50,0x201d69c
REFERENCE,CONNECTION,NODES,TEXT,STOP,SP=0x2170000,0x2171000,0x2173000,0x2176000,0x27e0000,0x2701000


def vector(seed):
    nodes=[dict(ip=[0x7f000001,0,0xffffffff,0x7f000001,0x12345678][i],port=[12345,0,65535,333,1][i]) for i in range(5)];count=seed%6;which=seed%5
    if which==0:ip,port=0,0
    elif which in [1,2] and count:ip,port=nodes[0 if which==1 else count-1]['ip'],nodes[0 if which==1 else count-1]['port']
    elif which==3:ip,port=0xabcdef11,65535
    else:ip,port=0x7f000001,333
    target=0 if seed%4==0 else NODES+6*80 if seed%4==1 else NODES+(seed%max(1,count))*80
    return dict(target=target,state=[100,101,105,106,999][seed%5],nodes=nodes,count=count,ip=ip,port=port,profileid=seed+1000,initiate=seed%2,peerPresent=seed%2!=0,messagePresent=(seed//2)%2!=0)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    connection=bytearray([0x77]*0x600);struct.pack_into('<I',connection,0x5d4,NODES if v['count'] else 0);nodes=bytearray()
    for i,node in enumerate(v['nodes']):
        data=bytearray([0x91+i]*80);struct.pack_into('<I',data,0,v['state']);struct.pack_into('<I',data,4,v['initiate']);struct.pack_into('<I',data,8,node['ip']);struct.pack_into('<H',data,12,node['port']);struct.pack_into('<i',data,16,v['profileid']);struct.pack_into('<I',data,60,ARRAYS+i*32);struct.pack_into('<I',data,76,NODES+(i+1)*80 if i+1<v['count'] else 0);nodes.extend(data)
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes(connection),NODES:bytes(nodes),ARRAYS:bytes([0xb4])*160,TEXT:b'peer-message\0'}
    for at,data in memory.items():cpu.mem_write(at,data)
    expected_connection=bytearray(connection);expected_nodes=bytearray(nodes)
    if a==DISPATCH:
        args=[REFERENCE,NODES];expected=dict(kind='return',value=3) if v['state']==100 else dict(kind='provider',address=hex(CONNECTED if v['state']==105 else INIT if v['initiate'] else ACCEPT))
    elif a==REMOVE:
        args=[REFERENCE,v['target']];idx=(v['target']-NODES)//80 if v['target']>=NODES and (v['target']-NODES)%80==0 else -1
        if 0<=idx<v['count']:
            nextnode=NODES+(idx+1)*80 if idx+1<v['count'] else 0
            if idx==0:struct.pack_into('<I',expected_connection,0x5d4,nextnode)
            else:struct.pack_into('<I',expected_nodes,(idx-1)*80+76,nextnode)
            expected=dict(kind='provider',address=hex(ARRAYLEN))
        else:expected=dict(kind='return')
    elif a==FIND:
        args=[REFERENCE,v['ip'],v['port']];expected=dict(kind='return',value=0)
        if v['ip'] or v['port']:
            for i,node in enumerate(v['nodes'][:v['count']]):
                if (node['ip'],node['port'])==(v['ip'],v['port']):expected['value']=NODES+i*80;break
    elif a==CREATE:args=[REFERENCE,v['profileid'],v['initiate']];expected=dict(kind='provider',address=hex(MALLOC))
    elif a==CONNECT:args=[REFERENCE,NODES];expected=dict(kind='provider',address=hex(GETPROFILE))
    else:args=[REFERENCE,NODES if v['peerPresent'] else 0,5,TEXT if v['messagePresent'] else 0];expected=dict(kind='provider',address=hex(STRLEN)) if v['peerPresent'] and v['messagePresent'] else dict(kind='return',value=3)
    initial=[(0x55ee0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual peer return ABI differs')
            observed=dict(kind='return') if a==REMOVE else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [MALLOC,GETPROFILE,STRLEN,INIT,ACCEPT,CONNECTED,ARRAYLEN]:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(at!=STRLEN):raise ValueError('Actual peer provider ARM/Thumb mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==MALLOC:interface=regs[0]==80
            elif at==GETPROFILE:interface=regs[:2]==[REFERENCE,v['profileid']] and SP-0x100<=regs[2]<SP
            elif at==STRLEN:interface=regs[0]==TEXT
            elif at==ARRAYLEN:
                index=(v['target']-NODES)//80;interface=0<=index<v['count'] and regs[0]==ARRAYS+index*32
            else:interface=regs[:2]==[REFERENCE,NODES]
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Peer caller escaped bounded original code/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==REMOVE and size==4 and (at==CONNECTION+0x5d4 or at in [NODES+i*80+76 for i in range(5)]):return
        raise ValueError('Unexpected peer caller RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Peer caller did not reach bounded return/provider')
    expected_memory=dict(memory);expected_memory[CONNECTION]=bytes(expected_connection);expected_memory[NODES]=bytes(expected_nodes);guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={DISPATCH:('peer->state == GPI_PEER_NOT_CONNECTED','peer->state == (GPI_PEER_NOT_CONNECTED+2)'),REMOVE:('iconnection->peerList == peer','iconnection->peerList != peer'),FIND:('pcurr->port == port','pcurr->port != port'),CREATE:('gsimalloc(sizeof(GPIPeer))','gsimalloc(sizeof(GPIPeer)+4)'),CONNECT:('gpiGetProfile(connection, peer->profile, &profile)','gpiGetProfile(connection, peer->state, &profile)'),MESSAGE:('return GP_NETWORK_ERROR;','return (GP_NETWORK_ERROR-1);')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent peer search/gate/provider model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole peer wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Whole wrong peer C changed extent',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(seed);v.update(state=100,target=NODES,count=1,ip=v['nodes'][0]['ip'],port=v['nodes'][0]['port'],peerPresent=False,messagePresent=True);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Whole wrong peer C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Six complete ordinary C peer callers698B genuinely match full native extents/imports and original tagged message-free callback020b03f5/canonicalThumb020b03f4.80-byte peer,24-byte message,4-byte time_t and connectionminimum600/list12/peer5d4 compiler-qualified;0external storage allocation/authorship credit.','768paired actual entries independently cover complete RAM-only address/port search including empty/bothzero/duplicateIP/differentport/highbitIP and nullpeer/nullmessage returns,state-dispatch returns/provider selection,absent-peer removal returns and actual head/previous-next unlink writes beforeArrayLength;allocator80/profileid/ARMstrlen pre-provider frames and independently expected RAM mutations/preserved other bytes.0synthetic returns.','Allmalloc/memset/time/ArrayNew/ArrayLength/ArrayNth/ArrayDeleteAt/UDP/profilelookup/strlen/append/callback bodies and post-provider mutation remain unexecuted.6sameextent complete wrong-C variants genuinely link and violate96independent search/error/frame models;6wrong peer layouts and unchanged original binding negatives reject.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
