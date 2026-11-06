class Memory:
    def __init__(self,sizes,ordinal):
        self.regions={a-16:bytearray((i*31+ordinal*7+a)&255 for i in range(n+32)) for a,n in sizes.items()}

    def put(self,address,raw):
        for base,data in self.regions.items():
            if base<=address and address+len(raw)<=base+len(data):data[address-base:address-base+len(raw)]=raw;return
        raise ValueError('Borrowed socket model write escaped exact regions')

    def read(self,address,size):
        for base,data in self.regions.items():
            if base<=address and address+size<=base+len(data):return bytes(data[address-base:address-base+size])
        raise ValueError('Borrowed socket model read escaped exact regions')

    def set(self,address,value,size=4):self.put(address,int(value&((1<<(size*8))-1)).to_bytes(size,'little'))
    def get(self,address,size=4):return int.from_bytes(self.read(address,size),'little')
    def snapshot(self):return {base:bytes(raw) for base,raw in self.regions.items()}
