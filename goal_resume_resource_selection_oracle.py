import hashlib
import struct
import unicorn
from unicorn import arm_const as R
import match_runtime as compiler

SP,STOP,FLAGS,CONTEXT=0x027f0000,0x027d0000,0x021b9bc8,0x021b9bd4
BUFFERS,ALTERNATE,HEAP,VIDEO,PALETTE_VIDEO=0x02600000,0x02610000,0x02620000,0x02680000,0x02690000
HEAP_TABLE,HEAP_STATUS,FILE_STATUS,PALETTE=0x020edd64,0x020edd54,0x020edec8,0x020fb8e8
HELPERS={0x0201d444:(44,44,2),0x0202a8e0:(116,112,1),0x0203cc3c:(16,12,2),0x02008c14:(20,20,3),
    0x02008ca4:(56,56,3),0x020625bc:(16,12,0),0x0202a498:(132,124,2),0x020481b8:(84,80,3),
    0x02048308:(88,72,0),0x0204540c:(132,132,4)}
PIXELS=[0x02004e58,0x02004f18,0x02004fd8,0x02005098]
FLUSH=[0x020048a0,0x0200494c,0x020048f4,0x020049a4]
PALETTES=[PALETTE,0x020fb6e8,0x020fb2e8,0x020fb4e8]
SERVICES={0x0201d3dc:4,0x0200bd04:1,0x0200bfe4:2,0x0200c02c:1,0x0203cb8c:3,0x0202b4e8:2,**{a:3 for a in PIXELS+FLUSH}}
SPECIAL=[0x020ddde0,0x020dddf8,0x020dde10,0x020dde28,0x020dde3c,0x020dde50]


def fixtures():
    rows=[]
    for i,code in enumerate([-128,-2,-1,0,4,5,6,119,120,121,122,123,124,125,126,127]):
        for n,flow in enumerate(['missing','zero','copied','late']if code!=-1 else['clear']):
            rows.append(dict(address=0x02061088,code=code,selection=2+i,group=n//2,lane=n%2,mode=n%2,
                length=None if flow=='missing'else 0 if flow in('zero','clear')else 4 if flow=='copied'else 36,mutate=flow=='late',flow=flow))
    for group,lane in [(0,1),(1,0),(1,1)]:rows.append(dict(rows[8],group=group,lane=lane))
    for palette in [None,0,2,34,512,514]:
        for bitmap in [None,0,2304]:
            rows.append(dict(address=0x02061470,palette=palette,bitmap=bitmap,flag=[0,1,128][len(rows)%3]))
    rows.extend(dict(address=0x02061470,palette=514,bitmap=2304,flag=flag)for flag in[0,1,128])
    return rows


def text(image,pointer):
    return image[pointer-0x02000000:pointer-0x02000000+32].split(b'\0',1)[0]


def plan(f,image,ordinal):
    if f['address']==0x02061088:
        code=f['code']
        fmt=SPECIAL[code-120]if 120<=code<=125 else 0x020dde60 if code==5 and f['mode']else 0x020dde78 if code==5 else 0x020dde94
        name=text(image,fmt)
        name=name%code if b'%'in name else name
        return dict(formats=[]if code==-1 else[fmt],names=[]if code==-1 else[name],lengths=[]if code==-1 else[f['length']],cell=CONTEXT+8*f['group']+4*f['lane'],destination=BUFFERS+0x1000*(2*f['group']+f['lane']))
    return dict(formats=[0x020ddeb0,0x020ddec4],names=[text(image,p)for p in[0x020ddeb0,0x020ddec4]],lengths=[f['palette'],f['bitmap']],bg1=ordinal%4,bg2=(ordinal+1)%4)


def payload(ordinal,index):
    return bytes((ordinal*7+index*43+i*11+5)&255 for i in range(0xa00))


def run(body,f,image,ordinal,code_span=None):
    address=f['address'];wanted=plan(f,image,ordinal)
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,image);vm.mem_write(address,body)
    for n in range(4):
        vm.mem_write(CONTEXT+4*n,struct.pack('<I',BUFFERS+0x1000*n))
        vm.mem_write(BUFFERS+0x1000*n,bytes((i*13+n+ordinal)&255 for i in range(0x800)))
    for n,base in enumerate(PALETTES):vm.mem_write(base,bytes((i*13+n*17+ordinal)&255 for i in range(512)))
    vm.mem_write(VIDEO,bytes((i*3+ordinal)&255 for i in range(0x4000)))
    vm.mem_write(PALETTE_VIDEO,bytes(2048));vm.mem_write(FLAGS,bytes([17,0x55,31,0,0]))
    vm.mem_write(HEAP_TABLE+40,bytes(20));vm.mem_write(HEAP_TABLE+40,struct.pack('<I',1))
    vm.mem_write(HEAP_TABLE+56,struct.pack('<I',0x026f0000));vm.mem_write(FILE_STATUS,struct.pack('<I',9))
    vm.mem_write(SP-512,bytes((i*19+ordinal)&255 for i in range(1024)))
    if address==0x02061088:
        vm.mem_write(0x020dac3c+2*f['selection']+f['lane'],bytes([f['code']&255]));vm.mem_write(FLAGS+4,bytes([f['mode']]))
    else:
        vm.mem_write(CONTEXT+0x273,bytes([f['flag']]));vm.mem_write(0x021b9bd0+1,bytes([wanted['bg1'],wanted['bg2']]))
    initial=[0x11220000+i*0x1234+ordinal for i in range(15)]
    if address==0x02061088:initial[:3]=[f['selection'],f['group'],f['lane']]
    initial[13:]=[SP,STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for reg,value in zip(compiler.REGISTERS,initial):vm.reg_write(reg,value)
    before_buffers=[bytes(vm.mem_read(BUFFERS+0x1000*n,0x800))for n in range(4)]
    before_palette=[bytes(vm.mem_read(p,512))for p in PALETTES];before_video=bytes(vm.mem_read(VIDEO,0x4000))
    calls,returns,writes,frames,failures=[],[],[],[],[];live={};allocations=0;returned=False
    formatted=[];opened=[];loaded=[];freed=[];draws=[];flushes=[]
    push=struct.unpack_from('<I',body)[0]
    if push&0xffff0000!=0xe92d0000:raise ValueError('Caller lacks a measured save frame')
    ending=struct.pack('<I',0xe8bd0000|((push&0xffff)&~0x4000)|0x8000)
    code_bytes=body.rfind(ending)+4
    if code_bytes<4:raise ValueError('Caller return boundary missing')
    def string(pointer):
        value=bytes(vm.mem_read(pointer,32)).split(b'\0',1)[0]
        if len(value)>=32:raise ValueError('Resource path exceeds the measured32-byte buffer')
        return value
    def put(pointer,data):
        vm.mem_write(pointer,data)
    def memory(uc,kind,location,size,value,user):
        if SP-0x10000<=location<SP:
            if location<SP-512 or location+size>SP:raise ValueError('Unexpected private stack extent')
        else:writes.append([location,size,value])
    def code(uc,location,size,user):
        nonlocal allocations,returned
        while frames and location==frames[-1][0]:
            frame=frames.pop();returns.append(dict(address=hex(frame[1]),value=uc.reg_read(R.UC_ARM_REG_R0)))
        if location==STOP:
            returned=True;uc.emu_stop();return
        if location in HELPERS:
            width=HELPERS[location][2];args=[uc.reg_read(r)for r in compiler.REGISTERS[:width]]
            frames.append((uc.reg_read(R.UC_ARM_REG_LR),location));calls.append(dict(address=hex(location),arguments=args))
        if location in SERVICES:
            args=[uc.reg_read(r)for r in compiler.REGISTERS[:SERVICES[location]]];result=1
            call=dict(address=hex(location),arguments=args)
            if location==0x0201d3dc:
                buffer,capacity,fmt,arguments=args;index=len(formatted)
                if index>=len(wanted['formats'])or fmt!=wanted['formats'][index]or capacity!=0xffffffff:raise ValueError('Wrong distinct formatter identity or bounded format route')
                pattern=string(fmt);value=struct.unpack('<i',bytes(uc.mem_read(arguments,4)))[0]
                data=pattern%value if b'%'in pattern else pattern
                if data!=wanted['names'][index]or len(data)>=32:failures.append('Independent signed formatter argument/path')
                put(buffer,data+b'\0');formatted.append(fmt);result=len(data)
                call['formattedSha256']=hashlib.sha256(data).hexdigest()
            elif location==0x0200bd04:put(args[0],bytes(72))
            elif location==0x0200bfe4:
                name=string(args[1]);index=len(opened)
                if index>=len(wanted['names'])or name!=wanted['names'][index]:raise ValueError('File-size backend saw an unexpected actual formatted path')
                length=wanted['lengths'][index];opened.append(index);result=int(length is not None)
                if result:put(args[0]+36,struct.pack('<II',0x1000,0x1000+length))
            elif location==0x0200c02c:pass
            elif location==0x0203cb8c:
                name=string(args[0])
                if name not in wanted['names']or args[1:]!=[2,1]:raise ValueError('Real archive wrapper path/heap/unpack words differ')
                index=wanted['names'].index(name)
                if not wanted['lengths'][index]:raise ValueError('Archive load after missing/zero file')
                result=HEAP+allocations*0x1000;allocations+=1
                if allocations>2:raise ValueError('Unexpected third allocation')
                put(result,payload(ordinal,index));live[result]=index;loaded.append(index)
                count=struct.unpack('<I',bytes(uc.mem_read(HEAP_TABLE+52,4)))[0];put(HEAP_TABLE+52,struct.pack('<I',count+1))
            elif location==0x0202b4e8:
                if args[0]!=0x026f0000 or args[1]not in live:raise ValueError('Real heap-free wrapper lost owned context/allocation')
                index=live.pop(args[1]);freed.append(index)
                if address==0x02061088 and f['mutate']:put(wanted['cell'],struct.pack('<I',ALTERNATE))
            elif location in PIXELS:
                pointer,destination,length=args;channel=PIXELS.index(location)
                if pointer not in live or destination!=0 or length!=0x900:raise ValueError('Real BG dispatcher exceeded bounded bitmap/destination')
                put(VIDEO+channel*0x1000,bytes(uc.mem_read(pointer,length)));draws.append(channel)
            elif location in FLUSH:
                channel=FLUSH.index(location)
                if args!=[PALETTES[channel],0,512]:raise ValueError('Real four-channel palette flush contract differs')
                put(PALETTE_VIDEO+512*channel,bytes(uc.mem_read(args[0],512)));flushes.append(channel)
            calls.append(call)
            for i,reg in enumerate(compiler.REGISTERS[:4]):uc.reg_write(reg,result if i==0 else 0xa5000000+ordinal*64+len(calls)*4+i)
            uc.reg_write(R.UC_ARM_REG_R12,0xbb000000+ordinal*64+len(calls))
            uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10)
            uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR));return
        if address<=location<address+code_bytes or any(start<=location<start+v[1]for start,v in HELPERS.items()):return
        raise ValueError(('Unexpected unowned instruction/literal',hex(location)))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    vm.emu_start(address,STOP+4,count=40000)
    if not returned or frames:raise ValueError('Actual source/native caller or helper failed to return')
    regs=[vm.reg_read(r)for r in compiler.REGISTERS]
    if regs[4:12]!=initial[4:12]or regs[13]!=SP:failures.append('Preserved C ABI registers/stack')
    if live or loaded!=freed:failures.append('Owned archive allocations freed exactly once')
    if formatted!=wanted['formats']or opened!=list(range(len(wanted['names']))):failures.append('Every selected distinct path opens exactly once')
    expected_buffers=list(before_buffers);expected_palette=list(before_palette);expected_video=bytearray(before_video)
    if address==0x02061088:
        cell_index=2*f['group']+f['lane'];length=f['length']
        if f['code']==-1:expected_buffers[cell_index]=bytes(0x800);expected_return=0
        else:
            if length:
                count=(length+3)&~3;expected_buffers[cell_index]=payload(ordinal,0)[:count]+expected_buffers[cell_index][count:]
            expected_return=ALTERNATE if length and f['mutate']else wanted['destination']
        if regs[0]!=expected_return or bytes(vm.mem_read(FLAGS+3,1))[0]!=(f['code']&255):failures.append('Independent sentinel/late-word-return/signed-global model')
        if [bytes(vm.mem_read(BUFFERS+0x1000*n,0x800))for n in range(4)]!=expected_buffers:failures.append('Actual clear/rounded-word-copy and row/lane stride model')
    else:
        if f['palette']:
            size=min(f['palette'],512)&~1;data=bytearray(expected_palette[0]);data[:size]=payload(ordinal,0)[:size];data[:2]=bytes(2);expected_palette[0]=bytes(data)
            if flushes!=[0,1,2,3]:failures.append('Palette upload flush sequence')
            if bytes(vm.mem_read(PALETTE_VIDEO,2048))!=b''.join(expected_palette):failures.append('Independent uploaded palette bytes and zero entry')
        elif flushes:failures.append('Unexpected palette flush for missing/zero file')
        expected_draws=([wanted['bg1']]if f['flag']else[])+[wanted['bg2']]if f['bitmap']else[]
        for channel in expected_draws:expected_video[channel*0x1000:channel*0x1000+0x900]=payload(ordinal,1)[:0x900]
        if draws!=expected_draws or bytes(vm.mem_read(VIDEO,0x4000))!=bytes(expected_video):failures.append('Independent signed flag/BG choice/fixed0x900 copy model')
        if [bytes(vm.mem_read(p,512))for p in PALETTES]!=expected_palette:failures.append('Independent palette clamp/halfword-copy model')
        if regs[0]!=FLAGS or bytes(vm.mem_read(FLAGS+1,1))!=b'\x01':failures.append('Independent final flag byte/address return')
    if struct.unpack('<I',bytes(vm.mem_read(HEAP_TABLE+52,4)))[0]!=0:failures.append('Actual native heap wrapper allocation counter')
    expected_status=9 if not wanted['lengths']else 1 if wanted['lengths'][-1]is None else 3 if wanted['lengths'][-1]==0 else 0
    if struct.unpack('<I',bytes(vm.mem_read(FILE_STATUS,4)))[0]!=expected_status:failures.append('Independent actual file-size helper status word')
    ram=bytearray(vm.mem_read(0x02000000,0x800000));span=code_span or max(432 if address==0x02061088 else 268,len(body))
    ram[address-0x02000000:address-0x02000000+span]=bytes(span);ram[SP-512-0x02000000:SP-0x02000000]=bytes(512)
    observation=dict(returned=regs[0],preserved=regs[4:12],sp=regs[13],calls=calls,writes=writes,actualHelperReturns=returns,observableRamSha256=hashlib.sha256(ram).hexdigest())
    return dict(modelFailures=failures,observation=observation,rawRegisters=regs,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),callerClobberedNotPromised=['r1','r2','r3','r12','lr','NZCV'],privateStackBytes=512)
