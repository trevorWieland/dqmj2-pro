import struct
import ov000_motion738_machine_20261101 as B
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=B.BASE,B.OVERLAY,0x02219BA4,200,B.PRIVATE
STATE,VECTOR,STACK=B.STATE,B.VECTOR,B.STACK

class Machine(B.Machine):
    def __init__(self,original,profile,body=None,private=False):
        super().__init__(original,profile,{ENTRY:body}if body is not None and not private else None,False,body if private else None)
        self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        self.u.mem_write(STATE+0x28,struct.pack('<I',profile['secondary']))
        self.u.mem_write(STATE+0x40,struct.pack('<iii',*profile['reference']))
        self.before=bytes(self.u.mem_read(BASE,0x800000))
    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        if(address,size)not in[(STATE+0x40,4),(STATE+0x48,4),(VECTOR,4),(VECTOR+8,4)]:raise ValueError(('742 unsupported nonstack write',hex(address),size))
        self.writes.append([u.reg_read(B.UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])
