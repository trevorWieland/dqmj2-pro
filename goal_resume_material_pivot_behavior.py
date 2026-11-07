import hashlib
import struct
import match_runtime as compiler
import unicorn
from unicorn import arm_const as R
from project import ROOT,sha256

BASE,RS,RO,RESOURCE,SBC,SP,STOP,CALLBACK=0x02000000,0x02600000,0x02601000,0x02602000,0x02603000,0x027f0000,0x027d0000,0x027c0000


def fixtures():
    material=[dict(kind='material',low=low,high=high,pattern=pattern)for low in range(8)for high in range(8)for pattern in range(2)]
    pivot=[dict(kind='pivot',pivot=p,signs=signs,a=a,b=b)for p in range(9)for signs in range(8)for a,b in[(17,-23),(-32768,32767),(0,0),(4096,-8192)]]
    return material+pivot


def validate(f):
    if f['kind']=='pivot'and not 0<=f['pivot']<9:raise ValueError('Unsupported compressed-node pivot; no native/C execution is allowed for9..15')
    if f['kind']=='material'and not(0<=f['low']<8 and 0<=f['high']<8):raise ValueError('Unsupported material selector')


def run(image,f,ordinal):
    validate(f);vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(BASE,0x800000);vm.mem_write(BASE,image)
    def put(address,data):vm.mem_write(address,data)
    def word(address,value):put(address,struct.pack('<I',value&0xffffffff))
    def get(address):return struct.unpack('<I',bytes(vm.mem_read(address,4)))[0]
    word(RS,SBC);word(RS+4,RO);word(RS+8,0x100);put(SBC,bytes([6,0,0,0,0,0,0,0]));put(SP-512,bytes((i*17+ordinal)&255 for i in range(512)));put(RS+0x12c,b'\xa5'*88)
    if f['kind']=='material':
        address=0x0202fde0;word(RS+0xd8,RESOURCE);put(RESOURCE+5,b'\x01');put(RESOURCE+10,struct.pack('<H',0x10));put(RESOURCE+0x14,struct.pack('<H',4));word(RESOURCE+0x18,0x40)
        material=RESOURCE+0x40;flags=(f['low']<<6)|(f['high']<<9);put(material+0x1e,struct.pack('<H',flags));global0=0x13579bdf^(0xffffffff*f['pattern']);global1=0xfdb97531^(0xffffffff*f['pattern']);local0=0x2468ace0^(0xffffffff*f['pattern']);local1=0x10203040^(0xffffffff*f['pattern']);word(material+4,local0);word(material+8,local1);word(0x020edf90+0x94,global0);word(0x020edf90+0x98,global1);word(0x020edf90+0x9c,0);args=[RS,0,material,0]
    else:
        address=0x0203048c;word(RS+0xd4,RESOURCE);word(RS+0xe8,CALLBACK);put(RESOURCE+1,b'\x01');put(RESOURCE+6,struct.pack('<H',0x10));put(RESOURCE+0x10,struct.pack('<H',4));word(RESOURCE+0x14,0x40);node=RESOURCE+0x40;flags=1|4|8|(f['pivot']<<4)|((f['signs']&1)<<8)|((f['signs']&2)<<8)|((f['signs']&4)<<8);put(node,struct.pack('<HHhh',flags,0,f['a'],f['b']));args=[RS,0]
    initial=[0x11000000+i*0x1234+ordinal for i in range(15)];initial[:len(args)]=args;initial[13:]=[SP,STOP];vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for reg,value in zip(compiler.REGISTERS,initial):vm.reg_write(reg,value)
    returned=False;reads=[];callbacks=[];helpers=[];frames=[];failures=[];writes=[]
    def code(uc,location,size,user):
        nonlocal returned
        while frames and frames[-1]==location:frames.pop();helpers.append(dict(address='0x02008f3c',actualThumbReturn=True,value=uc.reg_read(R.UC_ARM_REG_R0)))
        if location==STOP:returned=True;uc.emu_stop();return
        if location==0x02008f3c:
            if not uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Actual zero-matrix helper lost Thumb mode')
            frames.append(uc.reg_read(R.UC_ARM_REG_LR))
        if location==CALLBACK:
            values=[uc.reg_read(reg)for reg in compiler.REGISTERS[:4]];callbacks.append(values)
            if f['kind']!='pivot'or values!=[RS+0x12c,node+8,SBC,flags]:failures.append('Supplied scale-one callback argument contract')
            word(values[0],get(values[0])|1);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR));return
        if not BASE<=location<0x020d3fe0:raise ValueError(('Unexpected original/native instruction',hex(location)))
    def memory(uc,kind,location,size,value,user):
        if max(location,0x020d9068)<min(location+size,0x020d90ac):
            if kind!=unicorn.UC_MEM_READ:raise ValueError('Original reader writes immutable lookup data')
            reads.append([location,size])
        if kind==unicorn.UC_MEM_WRITE and not SP-512<=location<SP:writes.append([location,size,value])
    hooks=[vm.hook_add(unicorn.UC_HOOK_CODE,code),vm.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)];vm.emu_start(address,STOP+4,count=30000)
    if not returned or frames:raise ValueError('Complete reader or actual Thumb helper failed to return')
    registers=[vm.reg_read(reg)for reg in compiler.REGISTERS]
    if registers[4:12]!=initial[4:12]or registers[13]!=SP:failures.append('Preserved C ABI registers/stack')
    if f['kind']=='material':
        mask=lambda i:(0x7fff if i&1 else 0)|(0x7fff0000 if i&2 else 0)|(0x8000 if i&4 else 0)
        wanted0=(global0&~mask(f['low']))|(local0&mask(f['low']));wanted1=(global1&~mask(f['high']))|(local1&mask(f['high']))
        if get(RS+0xf4+4)!=wanted0 or get(RS+0xf4+8)!=wanted1 or get(RS+0xb0)!=RS+0xf4:failures.append('Independent material bitfield blend model')
        if reads!=[[0x020d9068+4*f['low'],4],[0x020d9068+4*f['high'],4]]:failures.append('Actual bounded selector-word read addresses/widths')
        if callbacks or helpers:failures.append('Unexpected material callback/helper route')
    else:
        matrix=[0]*9;p=f['pivot'];matrix[p]=-4096 if f['signs']&1 else 4096;positions=[3*r+c for r in range(3)if r!=p//3 for c in range(3)if c!=p%3];values=[f['a'],f['b'],-f['b']if f['signs']&2 else f['b'],-f['a']if f['signs']&4 else f['a']]
        for position,value in zip(positions,values):matrix[position]=value
        actual=list(struct.unpack('<9i',bytes(vm.mem_read(RS+0x12c+0x28,36))))
        if actual!=matrix or get(RS+0x12c)!=5:failures.append('Independent pivot/sign/zero-matrix model')
        if get(RS)!=SBC+4 or get(RS+0xb4)!=0 or len(callbacks)!=1 or len(helpers)!=1:failures.append('Complete reader command advance/result/callback/helper lifecycle')
        if reads!=[[0x020d9088+4*p+i,1]for i in range(4)]:failures.append('Actual bounded pivot-byte lanes/stride')
    observation=dict(modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),reads=reads,writes=writes,callbacks=callbacks,actualHelperReturns=helpers,ownedStateSha256=hashlib.sha256(bytes(vm.mem_read(RS,0x4000))).hexdigest(),actualTopReturn=True)
    for hook in hooks:vm.hook_del(hook)
    vm.mem_unmap(BASE,0x800000)
    return observation
