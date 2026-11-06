import struct

BASE=0x04000280


class PositiveDivider:
    def __init__(self,machine,hardware):
        self.machine=machine
        self.expected=bytearray(hardware)
        self.expected[0x280:0x2B0]=bytes(0x30)
        machine.mem_write(BASE,bytes(0x30))
        self.dirty=False
        self.operations=[]

    def write(self,address,size,value):
        assert address==BASE and size in[2,4]or BASE+0x10<=address and address+size<=BASE+0x20,(hex(address),size)
        self.expected[address-0x04000000:address-0x04000000+size]=value.to_bytes(size,'little')
        if address==BASE:self.dirty=False
        else:self.dirty=True

    def read(self,address,size):
        assert BASE<=address and address+size<=BASE+0x30
        if not self.dirty:return
        mode=int.from_bytes(bytes(self.machine.mem_read(BASE,2)),'little')&3
        assert mode in[0,1,2],mode
        numerator_bits=32 if mode==0 else 64
        denominator_bits=64 if mode==2 else 32
        numerator=int.from_bytes(bytes(self.machine.mem_read(BASE+0x10,numerator_bits//8)),'little',signed=True)
        denominator=int.from_bytes(bytes(self.machine.mem_read(BASE+0x18,denominator_bits//8)),'little',signed=True)
        assert numerator>=0 and denominator>0,(mode,numerator,denominator)
        quotient,remainder=divmod(numerator,denominator)
        output=struct.pack('<QQ',quotient,remainder)
        self.machine.mem_write(BASE+0x20,output);self.machine.mem_write(BASE,struct.pack('<H',mode))
        self.expected[0x2A0:0x2B0]=output;self.expected[0x280:0x282]=struct.pack('<H',mode)
        self.operations.append(dict(mode=mode,numerator=numerator,denominator=denominator,quotient=quotient,remainder=remainder))
        self.dirty=False
