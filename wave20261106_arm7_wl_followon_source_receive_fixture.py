import struct
SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
BASE=0x02714000
FRAME=BASE+16
REQ=0x02716000
CFM=0x02717000
OUT=0x0271a000
GAME=0x0271c000
SLOT=0x0380fff4


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


class Plan:
    def __init__(self,ordinal,stack):
        self.buffers={address:bytearray((i*13+ordinal*7+index*19)&255 for i in range(size))for index,(address,size)in enumerate([(CTX,1684),(BASE,528),(REQ,256),(CFM,128),(OUT,512),(GAME,256)])};self.initial={SLOT:p32(CTX)};self.regions=dict(self.initial);self.actions=[];self.allowed=[];self.args=[];self.returned=None;self.stack=stack;self.mmio=[]
    def buffer(self,address,size,fill=0):self.buffers[address]=bytearray([fill])*size
    def view(self,address,size):
        for base,raw in self.buffers.items():
            if base<=address and address+size<=base+len(raw):return raw,address-base
        raise ValueError('Independent receive model escaped declared borrowed buffers')
    def read(self,address,size):raw,offset=self.view(address,size);return bytes(raw[offset:offset+size])
    def write(self,address,value):raw,offset=self.view(address,len(value));raw[offset:offset+len(value)]=value
    def u16(self,address,value):self.write(address,p16(value))
    def u32(self,address,value):self.write(address,p32(value))
    def r16(self,address):return int.from_bytes(self.read(address,2),'little')
    def r32(self,address):return int.from_bytes(self.read(address,4),'little')
    def constant(self,address,value):self.initial[address]=value;self.regions[address]=value
    def capture(self):self.initial.update({address:bytes(raw)for address,raw in self.buffers.items()})
    def action(self,address,args=(),returned=0,checks=(),mutations=()):self.actions.append(dict(address=address,args=list(args),returned=returned,checks=list(checks),mutations=list(mutations)))
    def byte_read(self,address):value=self.read(address,1)[0];self.action(0x027ead5c,[address],value,checks=[(address,bytes([value]))]);return value
    def byte_write(self,address,value):self.write(address,bytes([value&255]));self.action(0x027ead30,[address,value&255],mutations=[(address,bytes([value&255]))])
    def copy16(self,source,dest,size):raw=self.read(source,size&~1);self.write(dest,raw);self.action(0x037fdf9c,[source,dest,size],checks=[(source,raw)],mutations=[(dest,raw)])
    def finish(self):
        self.regions.update({address:bytes(raw)for address,raw in self.buffers.items()});return dict(args=self.args,initial=self.initial,regions=self.regions,actions=self.actions,allowedWriteRanges=self.allowed,frame=self.stack,returnValue=self.returned,expectedMmioWrites=self.mmio)
