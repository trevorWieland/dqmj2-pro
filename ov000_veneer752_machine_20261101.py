import ov000_flag750_machine_20261101 as B
import ov000_flag750_models_20261101 as P
BASE,ENTRY,SIZE,PRIVATE=B.BASE,0x022198E0,12,B.PRIVATE

def profiles():
    cases=[]
    words=[0,1,0x80000000,0xFFFFFFFF]
    for template in P.profiles():
        for rotation in range(4):
            profile=dict(template)
            profile.update(name=template['name']+'-rotation-'+str(rotation),poison=[words[(rotation+i)%4]for i in range(4)],poisonRotation=rotation)
            cases.append(profile)
    return cases

class Machine(B.Machine):
    def __init__(self,original,profile,body=None,private=False):
        super().__init__(original,profile)
        self.code=PRIVATE if private else ENTRY
        self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(self.code,body)
        self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.target=set()
    def observe(self,u,address,size,data):
        if B.ENTRY<=address<B.ENTRY+B.SIZE:
            code,extent=self.code,self.extent
            self.code,self.extent=B.ENTRY,B.SIZE
            super().observe(u,address,size,data)
            self.code,self.extent=code,extent
            self.target.add(address)
            return
        super().observe(u,address,size,data)
    def run(self):
        result=super().run()
        result['targetObserved']=sorted(self.target)
        result['veneerObserved']=[pc for pc in result['ownObserved']if self.code<=pc<self.code+self.extent]
        return result
