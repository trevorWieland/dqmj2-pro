import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_more_build import build
from wave20261105_main_control_next_more_controls import original_helpers

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/more'
WORK=ROOT/'work/w5cn/more/fixtures'
SELECTION,CONTEXT,POINT_CONTEXT,INPUT,STOP,SP=0x21c6728,0x21c4f80,0x22459b4,0x2174000,0x27e0000,0x2701000


def signed16(value):return (value+32768)%65536-32768


def run(main,overlay,row,body,vector,seed,helpers):
    address=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,main);cpu.mem_write(0x21d7240,overlay);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);selection=bytearray(struct.pack('<hBB',vector.get('oldId',0),vector.get('oldSlot',0),0xa7));context=bytearray((seed*19+i*23)&255 for i in range(64));context[12]=vector.get('oldDirty',7);point_context=bytearray((seed*11+i*17)&255 for i in range(80));struct.pack_into('<I',point_context,44,0);inputs=struct.pack('<ii',vector.get('a',0),vector.get('b',0));regions={SELECTION:selection,CONTEXT:context,POINT_CONTEXT:point_context,INPUT:bytearray(inputs)}
    for at,data in regions.items():cpu.mem_write(at,bytes(data))
    initial=[(0x44550000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP]
    if address==0x207a2d0:initial[:2]=[vector['id']&0xffffffff,vector['slot']&0xffffffff];allowed=[0x206ea80]
    else:initial[0]=INPUT;allowed=[0x2215698,0x204b53c]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];entries={a:0 for a in allowed};points=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        if at==0x204b53c:
            pointer=machine.reg_read(ar.UC_ARM_REG_R1);points.append(dict(context=hex(machine.reg_read(ar.UC_ARM_REG_R0)),coordinates=list(struct.unpack('<hh',bytes(machine.mem_read(pointer,4))))))
        if not address<=at<address+row['bytes'] and not any(a<=at<a+helpers[a]['bytes'] for a in allowed):raise ValueError(('Fixture escaped exact caller/original helper graph',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if address==0x207a2d0 and (SELECTION<=at and at+size<=SELECTION+4 or CONTEXT<=at and at+size<=CONTEXT+64):return
        raise ValueError('Selection/point fixture wrote outside declared caller regions/stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=4000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual selection/point return ABI differs')
    expected={a:bytes(v) for a,v in regions.items()}
    if address==0x207a2d0:
        after=bytearray(selection);struct.pack_into('<hB',after,0,signed16(vector['id']),vector['slot']&255);expected[SELECTION]=bytes(after);state=bytearray(context)
        if vector['oldId']!=signed16(vector['id']) or vector['oldSlot']!=(vector['slot']&255):state[12]=1
        expected[CONTEXT]=bytes(state);model=registers[0]==CONTEXT and not points
    else:model=points==[dict(context=hex(POINT_CONTEXT+16),coordinates=[16,signed16(40+(vector['a']-vector['b'])*16)])]
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};model=model and actual==expected
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=model,returnValue=registers[0],pointArguments=points,memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):v for a,v in entries.items()},actualOriginalHelperInvocations=sum(entries.values()))


def execute(rows):
    helpers={int(r['address'],0):r for r in original_helpers()};main=(ROOT/'extract/arm9/arm9.bin').read_bytes();overlay=(ROOT/'extract/arm9_overlays/ov000.bin').read_bytes();records=[];negative=[]
    for row in rows:
        address=int(row['address'],0);native=main[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if address==0x207a2d0:cases=[dict(oldId=old,oldSlot=slot,oldDirty=dirty,id=new,slot=nextslot) for old,slot in [(0,0),(1,1),(-1,255)] for dirty in [0,7] for new,nextslot in [(old,slot),(old+1,slot),(old,slot+1),(old+65536,slot+256)]];wrong_vector=dict(oldId=0,oldSlot=0,oldDirty=7,id=1,slot=0);old,new='dirty=1','dirty=2'
        else:cases=[dict(a=a,b=b) for a,b in [(0,0),(1,0),(0,1),(100,-100),(-100,100),(2000,-2000),(-2000,2000)]];wrong_vector=dict(a=10,b=2);old,new='point.x=16','point.x=17'
        for seed,vector in enumerate(cases):
            original=run(main,overlay,row,native,vector,seed,helpers);source=run(main,overlay,row,linked,vector,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent selection/point model differs',original,source))
            records.append(original)
        folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError('Whole wrong selection/point C did not mutate')
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole wrong selection/point C changed complete extent')
        controls=[]
        for seed in range(16):
            actual=run(main,overlay,row,body,wrong_vector,seed,helpers)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Wrong complete C did not actually return a model violation')
            controls.append(actual)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    positive=2*sum(r['actualOriginalHelperInvocations'] for r in records);badcalls=sum(r['actualOriginalHelperInvocations'] for n in negative for r in n['records']);report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=positive,actualPositiveOriginalHelperInvocations=positive,actualWrongCOriginalHelperInvocations=badcalls,totalActualOriginalHelperInvocations=positive+badcalls,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=len(negative),wrongC=negative,limits=['Actual original main and ov000 helper images execute under original configured CPU/module/mode/boundaries. In-memory selection/context inputs are synthetic and explicit; no original input file changes.','Selection vectors cover exact/truncated id-slot equality, changed values, retained padding and existing dirty-byte values. Point vectors check actual stack-passed signed16 coordinates and context+16 at original helper entry; original point helper takes only its null-child early return.','Nonempty widget rendering children, nested graphics helpers, callbacks, hardware/game scenes and complete external context/storage extents remain unexecuted/uncredited. Source fields and labels describe measured widths/offsets rather than proven gameplay names.']);write_json(LANE/'caller-fixtures.json',report);return report
