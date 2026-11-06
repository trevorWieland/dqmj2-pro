import struct
from joint_math_hardware_20261102 import JointMathHardware


class BlendMathHardware(JointMathHardware):
    def read(self,address,size):
        offset=address-0x04000000
        if self.div_dirty and(offset==0x280 or 0x2A0<=offset<0x2B0):
            mode=int.from_bytes(bytes(self.machine.mem_read(0x04000280,2)),'little')
            if mode==1:
                numerator=int.from_bytes(bytes(self.machine.mem_read(0x04000290,8)),'little',signed=True)
                denominator=int.from_bytes(bytes(self.machine.mem_read(0x04000298,4)),'little',signed=True)
                assert numerator>=0 and denominator>0
                quotient,remainder=divmod(numerator,denominator);output=struct.pack('<QQ',quotient,remainder)
                self.machine.mem_write(0x040002A0,output);self.expected[0x2A0:0x2B0]=output
                self.operations.append(dict(kind='division',mode=mode,numerator=numerator,denominator=denominator,quotient=quotient,remainder=remainder));self.div_dirty=False
        super().read(address,size)
