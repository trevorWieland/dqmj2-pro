import hashlib
import json
import random
import struct
import match_runtime
from project import ROOT,read_json,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_slot_controller_first_paths import EVIDENCE
from wave20261106_ov000_slot_controller_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
HELPERS={0x02049ad0:20,0x02049be4:172}
ALLOCATOR=0x0205fe20
PROVIDER=0x0205fe74
BASE=0x021d7240
STACK=0x03030000
STOP=0x0303f000
LINK=0x03010000
RESOURCE=0x03011000
ARRAY=0x022461d4
SPECS={0x021ebdf0:(0x02236a98,2,False,False),0x021ef688:(0x02236c1c,6,True,True),0x021f2d24:(0x02236dbc,1,True,True),0x0221c758:(0x022461c4,2,False,True),0x0222b24c:(0x02247704,2,False,False)}


def words(values):return struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values])


def execute_one(row,body,case,main,image):
    address=int(row['address'],0);state,counter,checks,conditional=SPECS[address];selector=case['args'][0];slot=0x02102a18+12*selector
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000)
    uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body)
    uc.mem_write(0x021029c8,bytes([3,7,2,9,4,8,1,6]));uc.mem_write(0x021029d0,bytes([5,11,1,2,3,4,6,7]))
    view_words=4 if address==0x0221c758 else counter+1
    old_link=LINK if case['occupied']else 0
    entry=words([old_link,0xaabbccdd,0x87654321]);resource=bytes(range(24))+words([case['flags']]);state_words=case['stateWords'];array=bytes(range(64));link=bytes([case['first'],0xc1,0xc2,0xc3])+words([RESOURCE])
    uc.mem_write(slot,entry);uc.mem_write(LINK,link);uc.mem_write(RESOURCE,resource);uc.mem_write(state,words(state_words[:view_words]));uc.mem_write(ARRAY,array)
    args=case['args'];uc.mem_write(STACK,words(args[4:]));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REG,args[:4]):uc.reg_write(reg,value&0xffffffff)
    saved=[0x11110000+i*0x101 for i in range(8)]
    for reg,value in zip(SAVED,saved):uc.reg_write(reg,value)
    trace=[];services=[];helper_counts={a:0 for a in HELPERS};helper_instructions=0;done=False
    def hook(machine,pc,size,user):
        nonlocal helper_instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in HELPERS:helper_counts[pc]+=1
        if any(a<=pc<a+n for a,n in HELPERS.items()):helper_instructions+=1;return
        if pc in[ALLOCATOR,PROVIDER]:
            count=1 if pc==ALLOCATOR else 11;sp=machine.reg_read(UC_ARM_REG_SP);values=[machine.reg_read(reg)for reg in REG[:min(count,4)]]
            if count>4:values+=list(struct.unpack('<'+'I'*(count-4),machine.mem_read(sp,4*(count-4))))
            services.append(dict(address=hex(pc),args=values))
            machine.reg_write(UC_ARM_REG_R0,(0 if case['allocationFails']else LINK)if pc==ALLOCATOR else 0xdeadbeef)
            machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Execution left proven caller/helpers/services',hex(pc)))
        trace.append(pc-address)
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=2000)
    if not done:raise ValueError('Bounded complete caller did not return')
    if uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(reg)for reg in SAVED]!=saved:raise ValueError('Caller/helper callee-saved or SP contract differs')
    result=dict(returnWord=uc.reg_read(UC_ARM_REG_R0),entry=bytes(uc.mem_read(slot,12)).hex(),resource=bytes(uc.mem_read(RESOURCE,28)).hex(),state=bytes(uc.mem_read(state,4*view_words)).hex(),array=bytes(uc.mem_read(ARRAY,64)).hex(),link=bytes(uc.mem_read(LINK,8)).hex(),services=services,helpers={hex(a):n for a,n in helper_counts.items()})
    expected_entry=bytearray(entry);expected_resource=bytearray(resource);expected_words=state_words[:];expected_array=bytearray(array);expected_services=[]
    rejected=checks and case['occupied'];failed=case['allocationFails']and not rejected
    if not rejected:
        expected_services.append(dict(address=hex(ALLOCATOR),args=[1]))
        if not failed:
            expected_entry[:8]=words([LINK])+bytes([args[1]&255,args[2]&255,case['first'],0xaa])
            expected_services.append(dict(address=hex(PROVIDER),args=[LINK,1,7,11,args[3],args[4],args[5],args[6],state_words[counter],args[7]&0xffffffff,args[8]]))
            struct.pack_into('<I',expected_resource,24,case['flags']|2)
            if not conditional or args[8]:expected_words[counter]=(expected_words[counter]+args[5]*args[6])&0xffffffff
            if address==0x0221c758:expected_array[state_words[3]]=selector&255;expected_words[3]=(expected_words[3]+1)&0xffffffff
    returned=0 if rejected or failed else 1 if checks else state
    expected=dict(returnWord=returned,entry=bytes(expected_entry).hex(),resource=bytes(expected_resource).hex(),state=words(expected_words[:view_words]).hex(),array=bytes(expected_array).hex(),link=link.hex(),services=expected_services,helpers={hex(0x02049ad0):1,hex(0x02049be4):0 if rejected else 1})
    if result!=expected:raise ValueError(('Independent consumed-field/provider ABI model differs',row['address'],case,result,expected))
    return result,dict(helperInvocations=sum(helper_counts.values()),helperInstructions=helper_instructions,serviceEntries=len(services),callerInstructions=len(trace))


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();rng=random.Random(202611060912);records=[];helper_calls=0;helper_insns=0;service_calls=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(10):
            state_words=[rng.getrandbits(32)for i in range(7)];state_words[3]=index%8
            args=[index%4,0x80+index,0xff-index,[0,255,128][index%3],[0,255,128][(index+1)%3],[0,1,255][index%3],[255,2,0][index%3],[-128,-1,127][index%3],[0,1,0xffffffff][index%3]]
            case=dict(args=args,occupied=index%3==1,allocationFails=address==0x021f2d24 and index==8,first=[0,128,255][index%3],flags=[0,0xffffffff,0x80000000][index%3],stateWords=state_words)
            pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,main,image);pair.append(result);counts.append(count);helper_calls+=count['helperInvocations'];helper_insns+=count['helperInstructions'];service_calls+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Complete original/C native caller effects differ')
            records.append(dict(address=row['address'],case=index,arguments=args,occupied=case['occupied'],allocationFails=case['allocationFails'],returned=True,result=pair[0],executions=counts))
    trace_hash=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    limits=['Synthetic bounded font-table/slot/link/resource/BSS memory and valid narrow-argument ABI domains only; no gameplay/graphics/scene/device execution.', 'Actual original accepted main slot getter20B and initializer172B execute in each applicable native/C caller run; their deeper allocator/provider services supply results and execute0body instructions.', 'Unchecked-initializer callers are tested with successful allocation; only the measured checked208B caller tests allocation failure. Imported helper/source/storage extent credit remains0.', 'Caller semantic labels are inferred from measured fields; complete game purpose and nominal global interface unification remain unresolved.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helper_calls,actualOriginalHelperInstructions=helper_insns,suppliedServiceCalls=service_calls,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace_hash,limits=limits,records=records)
    write_json(EVIDENCE/'caller-fixtures.json',result);return result
