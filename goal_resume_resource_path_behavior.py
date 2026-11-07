import hashlib
import struct
import match_runtime as compiler
import unicorn
from unicorn import arm_const as R
from project import ROOT,read_json,sha256
from goal_resume_resource_path_contracts import recipe

BASE,SP,STOP,PATH,BUFFER=0x02000000,0x027f0000,0x027d0000,0x026f1000,0x02600000
HELPERS={0x0202a8e0:116,0x0203cc3c:16,0x0203cb8c:160,0x0200bd04:40,0x0200bfe4:72,0x0200c02c:60,0x0203cc2c:16,0x0202a498:132}
CALLERS={0x02043018:88,0x022096f4:112,0x021d77f8:104,0x021e6bdc:104,0x020c55dc:156}
SERVICES={0x0200beec:2,0x0200bf74:3,0x0200b504:2,0x0202a250:0,0x0202a37c:3,0x0202a818:4,0x0202b4e8:2,0x0203cf9c:2,0x020481b8:3,0x0204820c:3,0x02048308:0,0x0204594c:4,0x02045654:1}


def fixtures():
    rows=[]
    base=dict(found=True,opened=True,length=37,allocated=True,read=True,closed=True,heap=2,selector=1,capacity=64,flags=0,index=0)
    def add(address,**changes):rows.append(dict(base,address=address,**changes))
    for length in[0,1,37,0xfffffff0]:
        for closed in[False,True]:add(0x0202a8e0,length=length,closed=closed)
    add(0x0202a8e0,found=False);add(0x0202a8e0,opened=False)
    for address in[0x0203cc3c,0x0203cb8c]:
        for selector in[0,1]:
            for route in['positive','missing','empty','allocation-failure','read-failure']:
                add(address,selector=selector,heap=0xffffffff if selector==0 else 2,found=route!='missing',length=0 if route=='empty'else 37,allocated=route!='allocation-failure',read=route!='read-failure')
    for capacity in[0,36,37,38]:
        for read in[False,True]:add(0x02043018,capacity=capacity,read=read)
    add(0x02043018,found=False)
    for flags in[0,1,2,3]:
        for allocated in[False,True]:add(0x022096f4,flags=flags,heap=1,allocated=allocated)
    for address in[0x021d77f8,0x021e6bdc]:
        add(address,index=-1)
        for index in range(4):add(address,index=index,length=32+index*4)
    for route in['positive','missing','empty','allocation-failure','read-failure']:add(0x020c55dc,length=0 if route=='empty'else 8+1399*44,found=route!='missing',allocated=route!='allocation-failure',read=route!='read-failure',heap=1)
    return rows


def payload(f,ordinal):
    if f['address']!=0x020c55dc:return bytes((i*13+ordinal*7+5)&255 for i in range(max(1,min(f['length'],0x10000))))
    data=bytearray(8+1399*44)
    for index in range(1399):
        struct.pack_into('<H',data,8+44*index,(index*37+ordinal*11)&0xffff)
        data[8+44*index+4]=(index*7+ordinal)&255
    return bytes(data)


def module_image(name):
    module=next(m for m in read_json(ROOT/'provenance/seed-manifest.json')['modules']if m['name']==name)
    if sha256(ROOT/module['binary'])!=module['sha256']:raise ValueError('Behavior original physical module changed')
    return int(module['base'],0),(ROOT/module['binary']).read_bytes()


def run(f,source_bodies,ordinal):
    address=f['address'];module='ov000'if address==0x022096f4 else'ov006'if address in(0x021d77f8,0x021e6bdc)else'main'
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(BASE,0x800000)
    for name in dict.fromkeys(['main',module]):
        start,data=module_image(name);vm.mem_write(start,data)
    for (name,target),body in source_bodies.items():
        if name in('main',module):vm.mem_write(target,body)
    vm.mem_write(PATH,b'migration/path.bin\0');vm.mem_write(SP-1024,bytes((i*19+ordinal)&255 for i in range(1024)))
    vm.mem_write(0x020edec8,struct.pack('<I',9));vm.mem_write(0x021d5404,struct.pack('<II',0xcccccccc,0xdddddddd));vm.mem_write(0x021d588c,b'\xa5'*2842)
    for heap in[1,2]:vm.mem_write(0x020edd64+20*heap,struct.pack('<IIIII',1,0,0,0,0x026f0000+heap*4))
    path=PATH
    if address in(0x021d77f8,0x021e6bdc)and f['index']>=0:
        table=0x0220c8a8 if address==0x021d77f8 else 0x0220d15c;path=struct.unpack('<I',bytes(vm.mem_read(table+4*f['index'],4)))[0]
    elif address==0x020c55dc:path=0x020e2e40
    def string(pointer):return b''if not pointer else bytes(vm.mem_read(pointer,128)).split(b'\0',1)[0]
    wanted_name=string(path);args=[PATH,f['heap'],f['selector']]
    if address==0x02043018:args=[PATH,BUFFER,f['capacity']]
    elif address==0x022096f4:args=[PATH,f['flags']]
    elif address in(0x021d77f8,0x021e6bdc):args=[f['index']&0xffffffff]
    elif address==0x020c55dc:args=[]
    initial=[0x11220000+i*0x1234+ordinal for i in range(15)];initial[:len(args)]=args;initial[13:]=[SP,STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for reg,value in zip(compiler.REGISTERS,initial):vm.reg_write(reg,value)
    calls,returns,frames,failures,writes=[],[],[],[],[];returned=False;allocations=[];read_calls=[];ui=[]
    def put(pointer,data):vm.mem_write(pointer,data)
    def code(uc,location,size,user):
        nonlocal returned
        while frames and frames[-1][0]==location:
            unused,target=frames.pop();returns.append(dict(address=hex(target),value=uc.reg_read(R.UC_ARM_REG_R0)))
        if location==STOP:returned=True;uc.emu_stop();return
        if location in HELPERS:frames.append((uc.reg_read(R.UC_ARM_REG_LR),location))
        if location in SERVICES:
            values=[uc.reg_read(reg)for reg in compiler.REGISTERS[:SERVICES[location]]];result=1;calls.append(dict(address=hex(location),arguments=values))
            if location==0x0200beec:
                if values[1]!=path or string(values[1])!=wanted_name:failures.append('Retained path word and exact filename bytes')
                put(values[0],struct.pack('<II',0x026e0000,42));result=int(f['found'])
            elif location==0x0200bf74:
                if values[1:]!=[0x026e0000,42]or not SP-1024<=values[0]<=SP-72:failures.append('Real SDK FSFileID by-value and owned72-byte record')
                if f['opened']:
                    put(values[0]+36,struct.pack('<II',0x1000,(0x1000+f['length'])&0xffffffff));put(values[0]+12,struct.pack('<I',0x30))
                result=int(f['opened'])
            elif location==0x0200b504:
                if values[1]!=8:failures.append('Real SDK close command')
                result=int(f['closed'])
            elif location==0x0202a250:result=2
            elif location==0x0202a37c:
                selector=f['selector']if address==0x0203cb8c else 1 if address in(0x0203cc3c,0x020c55dc)else 0
                heap=2 if f['heap']==0xffffffff else f['heap']
                if values!=[heap,(f['length']+3)&~3,4 if selector==0 else 0xfffffffc]:failures.append('Independent heap/rounded-size/signed-alignment model')
                result=BUFFER if f['allocated']else 0
                if result:
                    allocations.append(result);put(0x020edd64+20*heap+12,struct.pack('<I',len(allocations)))
            elif location==0x0202a818:
                expected_buffer=BUFFER;read_calls.append(values)
                read_length=f['length']if f['found']and f['opened']else 0
                if values!=[path,expected_buffer,read_length,0]:failures.append('Existing read word boundary')
                if f['read']:put(expected_buffer,payload(f,ordinal)[:read_length])
                result=int(f['read'])
            elif location==0x0202b4e8:
                if values[1]!=BUFFER or not allocations:failures.append('Actual native free ownership')
                else:allocations.pop()
            elif location==0x0203cf9c:
                if values!=[1,BUFFER]:failures.append('Retained original overlay release words')
                allocations.clear()
            elif location in(0x020481b8,0x0204820c,0x02048308):ui.append([location,values])
            elif location==0x0204594c:
                if values!=[0 if address==0x021d77f8 else 2,BUFFER,0,f['length']]:failures.append('Table word, owned buffer, and exact draw byte count')
                ui.append([location,values])
            elif location==0x02045654:
                if values!=[0 if address==0x021d77f8 else 2]:failures.append('Signed minus-one table sentinel route')
                result=0x17c7
            for index,reg in enumerate(compiler.REGISTERS[:4]):uc.reg_write(reg,result if index==0 else 0xa5000000+ordinal*64+len(calls)*4+index)
            uc.reg_write(R.UC_ARM_REG_R12,0xbb000000+ordinal*64+len(calls));uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR));return
        top_width=max(CALLERS.get(address,HELPERS.get(address,0)),len(source_bodies.get((module,address),b'')))
        if any(start<=location<start+width for start,width in{**HELPERS,address:top_width}.items()):return
        raise ValueError(('Unowned native instruction',hex(location)))
    def memory(uc,kind,location,size,value,user):
        if not SP-1024<=location<SP:writes.append([location,size,value])
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=100000)
    if not returned or frames:raise ValueError('Actual native/API helper failed to return')
    regs=[vm.reg_read(reg)for reg in compiler.REGISTERS]
    if regs[4:12]!=initial[4:12]or regs[13]!=SP:failures.append('Preserved C ABI registers/stack')
    valid=f['found']and f['opened'];length=f['length']if valid else 0;loaded=bool(length and f['allocated']and f['read'])
    expected_status=0 if length else 3 if valid else 1
    if address in(0x021d77f8,0x021e6bdc)and f['index']==-1:expected_status=9
    if struct.unpack('<I',bytes(vm.mem_read(0x020edec8,4)))[0]!=expected_status:failures.append('Independent file-size status')
    if address==0x0202a8e0 and regs[0]!=length:failures.append('Independent unsigned file-length model')
    if address in(0x0203cc3c,0x0203cb8c)and regs[0]!=(BUFFER if loaded else 0):failures.append('Independent archive-owned buffer result')
    if address==0x02043018:
        expected=bool(length<=f['capacity']and f['read'])
        if regs[0]!=int(expected):failures.append('Independent capacity/read result')
        if expected and(bytes(vm.mem_read(0x020f69b4,1))!=b'\x01'or struct.unpack('<I',bytes(vm.mem_read(0x020f69b4+12,4)))[0]!=BUFFER):failures.append('Independent read-state pointer/flag model')
    if address==0x022096f4:
        expected_ui=([[0x020481b8,[BUFFER,0,32]]]if f['flags']&1 else[])+([[0x0204820c,[BUFFER,0,32]]]if f['flags']&2 else[])+[[0x02048308,[]]]
        if regs[0]!=int(loaded)or ui!=(expected_ui if loaded else[]):failures.append('Independent original overlay flag/UI route')
    if address in(0x021d77f8,0x021e6bdc)and f['index']>=0:
        if regs[0]!=1 or allocations or struct.unpack('<I',bytes(vm.mem_read(0x020edd64+52,4)))[0]!=0:failures.append('Original owned-buffer free return/counter model')
    if address==0x020c55dc:
        manager=struct.unpack('<II',bytes(vm.mem_read(0x021d5404,8)))
        if regs[0]!=int(loaded)or manager!=((BUFFER,BUFFER+8)if loaded else(0,0xdddddddd)):failures.append('Native FieldFile result and records+8 model')
        expected=bytearray(b'\xa5'*2842)
        if loaded:
            data=payload(f,ordinal)
            for index in range(1399):struct.pack_into('<H',expected,2*index,(struct.unpack_from('<H',data,8+44*index)[0]&0xfff)|((data[8+44*index+4]&15)<<12))
        if bytes(vm.mem_read(0x021d588c,2842))!=bytes(expected):failures.append('Independent1399-record44-byte stride and compact bitfield model')
    return dict(modelFailures=failures,registers=regs,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,actualHelperReturns=returns,writes=writes,ramSha256=hashlib.sha256(bytes(vm.mem_read(BASE,0x800000))).hexdigest(),actualTopReturn=True)


def qualify(source_bodies):
    traces=[]
    for ordinal,fixture in enumerate(fixtures()):
        native=run(fixture,{},ordinal);fresh=run(fixture,source_bodies,ordinal)
        if native!=fresh or native['modelFailures']:raise ValueError(('Original/fresh typed API behavior differs',ordinal,fixture,native['modelFailures'],fresh['modelFailures']))
        traces.append(dict(fixture=fixture,result=native))
    return traces
