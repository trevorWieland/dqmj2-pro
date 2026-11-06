import arm7_seq_neighbor_model_20261030 as memory

SQUARE = 0x0380704C
ATTACK_WINDOW, ATTACK_COEFFICIENTS = 0x038071E0, 0x03807260


class Model(memory.Model):
    def envelope(self,node,step):
        status = self.get(node+2,1)
        attenuation = self.get(node+0x10,4,True)
        if step:
            if status == 0:
                product = memory.signed((-attenuation*self.get(node+0x1C,1)) & 0xFFFFFFFF)
                attenuation = -(product >> 8)
                self.put(node+0x10,4,attenuation)
                if attenuation == 0:
                    self.put(node+2,1,1)
            elif status == 1:
                floor = self.get(SQUARE+2*self.get(node+0x1D,1),2,True)*128
                attenuation = memory.signed((attenuation-self.get(node+0x1E,2)) & 0xFFFFFFFF)
                self.put(node+0x10,4,attenuation)
                if attenuation <= floor:
                    attenuation = floor
                    self.put(node+0x10,4,attenuation)
                    self.put(node+2,1,2)
            elif status == 3:
                attenuation = memory.signed((attenuation-self.get(node+0x20,2)) & 0xFFFFFFFF)
                self.put(node+0x10,4,attenuation)
        return (attenuation >> 7) & 0xFFFFFFFF

    def attack(self,node,value):
        value = memory.signed(value)
        if value < 109:
            coefficient = 255-value
        else:
            if value > 255:
                raise ValueError('Positive attack index exceeds proved byte-producer and data-window domain')
            coefficient = self.get(ATTACK_COEFFICIENTS+127-value,1)
        self.put(node+0x1C,1,coefficient)

    def lfo(self,node):
        counter,delay = self.get(node+6,2),self.get(node+4,2)
        if counter < delay:
            self.put(node+6,2,counter+1)
        else:
            value = self.get(node+8,2)+self.get(node+1,1)*64
            self.put(node+8,2,value)
            self.put(node+8,2,value & 255)
            self.put(node+8,2,(value & 255) | (((value // 256) % 128)*256))
