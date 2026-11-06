import math
import struct

BASE=0x04000000


class JointMathHardware:
    def __init__(self,machine):
        self.machine=machine;self.expected=bytearray(4096);self.div_dirty=False;self.sqrt_dirty=False;self.operations=[]
        machine.mem_write(BASE,bytes(self.expected))

    def write(self,address,size,value):
        offset=address-BASE
        assert(offset in[0x280,0x2B0]and size==2)or(offset in[0x290,0x294,0x298,0x29C,0x2B8,0x2BC]and size==4),(hex(address),size)
        self.expected[offset:offset+size]=value.to_bytes(size,'little')
        if 0x290<=offset<0x2A0:self.div_dirty=True
        if 0x2B8<=offset<0x2C0:self.sqrt_dirty=True

    def read(self,address,size):
        offset=address-BASE;assert 0x280<=offset and offset+size<=0x2C0
        if self.div_dirty and(offset==0x280 or 0x2A0<=offset<0x2B0):
            mode=int.from_bytes(bytes(self.machine.mem_read(BASE+0x280,2)),'little');assert mode==2
            numerator=int.from_bytes(bytes(self.machine.mem_read(BASE+0x290,8)),'little',signed=True)
            denominator=int.from_bytes(bytes(self.machine.mem_read(BASE+0x298,8)),'little',signed=True)
            assert numerator>=0 and denominator>0
            quotient,remainder=divmod(numerator,denominator);output=struct.pack('<QQ',quotient,remainder)
            self.machine.mem_write(BASE+0x2A0,output);self.expected[0x2A0:0x2B0]=output
            self.operations.append(dict(kind='division',mode=mode,numerator=numerator,denominator=denominator,quotient=quotient,remainder=remainder))
            self.div_dirty=False
        if self.sqrt_dirty and offset in[0x2B0,0x2B4]:
            mode=int.from_bytes(bytes(self.machine.mem_read(BASE+0x2B0,2)),'little');assert mode==1
            value=int.from_bytes(bytes(self.machine.mem_read(BASE+0x2B8,8)),'little');result=math.isqrt(value)
            output=struct.pack('<I',result);self.machine.mem_write(BASE+0x2B4,output);self.expected[0x2B4:0x2B8]=output
            self.operations.append(dict(kind='square-root',mode=mode,value=value,result=result));self.sqrt_dirty=False

    def verify(self):
        assert not self.div_dirty and not self.sqrt_dirty
        assert bytes(self.machine.mem_read(BASE,4096))==bytes(self.expected)
