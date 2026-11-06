import itertools
import math
import struct
import ov000_motion738_machine_20261101 as M

def f(value):return struct.unpack('<f',struct.pack('<f',value))[0]
def s16(value):return((value+32768)&65535)-32768

def profiles():
    result=[];counts=[-128,-1,1,2,7,127];offsets=[-32768,-1,0,1,32767];dimensions=[0,23,24,31,32,33,255]
    for seed,(active,index,sign)in enumerate(itertools.product([0,1,0x80000000,0xFFFFFFFF],[0,1,127,255],range(4))):
        result.append(dict(name=f'caller-{seed}',seed=seed,index=index,rowX=offsets[seed%5],rowZ=offsets[(seed+2)%5],width=dimensions[seed%7],height=dimensions[(seed+3)%7],count=counts[seed%6],offset=[offsets[(seed+1)%5],offsets[(seed+4)%5]],active=active,vector=[0x12345678,-2147483648,0x7FFFFFFF],source=[[-65536,-1,0,65536][sign],0x456789AB,[-131072,0,1,131072][sign]]))
    return result

def direct_profiles():
    result=[]
    for seed,(width,height,kind)in enumerate(itertools.product([0,31,32,33,255],[0,23,24,25,255],range(8))):
        max_x=(max(width,32)*8-128)*4096;max_z=(max(height,24)*8-96)*4096
        xs=[-2147483648,0x80000-1,0x80000,0x80000+1,max_x-1,max_x,max_x+1,2147483647];zs=[-2147483648,0x60000-1,0x60000,0x60000+1,max_z-1,max_z,max_z+1,2147483647]
        result.append(dict(name=f'clamp-{seed}',seed=seed,index=[0,1,127,255][seed%4],rowX=0,rowZ=0,width=width,height=height,count=1,offset=[0,0],active=1,vector=[xs[kind],-2147483648,zs[(kind+3)%8]],source=[0,0,0]))
    return result

def model(result):
    p=result['profile'];initial=result['before'];expected=bytearray(initial);writes=[]
    def put(offset,size,value):
        address=M.STATE+offset;word=value&((1<<(size*8))-1);expected[address-M.BASE:address-M.BASE+size]=word.to_bytes(size,'little');writes.append([address,size,word])
    x,y,z=p['vector'];offset_x,offset_z=p['offset'];physical=None
    if not result['direct']:
        put(0x4C,4,p['rowX']);put(0x54,4,p['rowZ']);x=p['rowX']*4096;z=p['rowZ']*4096;put(0x4C,4,x);put(0x54,4,z)
        ratio=f(8.0/f(p['count']));x+=math.trunc(f(f(p['source'][0])*ratio));z+=math.trunc(f(f(p['source'][2])*ratio));put(0x4C,4,x);put(0x54,4,z)
        if p['active']==0:physical=0
        else:
            def adjustment(value):
                scaled=f(value*4096);return math.trunc(f(scaled+0.5)if value>0 else f(scaled-0.5))
            x-=adjustment(offset_x);z-=adjustment(offset_z);put(0x4C,4,x);put(0x54,4,z)
    if result['direct']or p['active']!=0:
        old_x,old_z=x,z;max_x=(max(p['width'],32)*8-128)*4096;max_z=(max(p['height'],24)*8-96)*4096
        if x<0x80000:x=0x80000;put(0x4C,4,x)
        if x>max_x:x=max_x;put(0x4C,4,x)
        if z<0x60000:z=0x60000;put(0x54,4,z)
        returned_z=z
        if z>max_z:z=max_z;put(0x54,4,z)
        if result['direct']:physical=returned_z&0xFFFFFFFF
        else:
            vx=math.trunc(f(f(offset_x)-f(f(x-old_x)/4096.0)));vz=math.trunc(f(f(offset_z)-f(f(z-old_z)/4096.0)));put(0x10,2,vx);put(0x12,2,vz);physical=vz&0xFFFFFFFF
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError(('738 independent complete nonstack model differs',p['name']))
    actual=[row[1:]for row in result['nonstackWrites']]
    if actual!=writes:raise ValueError(('738 independent ordered write model differs',p['name'],actual,writes))
    if result['coreRegistersAndCpsr'][0]!=physical:raise ValueError(('738 physical nonsemantic R0 differs',p['name'],result['coreRegistersAndCpsr'][0],physical))
    if any(c['preparedWords']!=[p['index']]for c in result['nativeCalls']if c['entry']==0x021DF3BC):raise ValueError('738 actual byte-index forwarding differs')
    return dict(expectedPhysicalR0=physical,orderedNonstackWrites=len(writes),completeNonstackModel=True,nativeIndexForwardingChecked=True,clampVectorAliasesStateMember=True)
