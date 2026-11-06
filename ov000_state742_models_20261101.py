import itertools
import struct
import ov000_state742_machine_20261101 as M

def profiles():
    result=[];signed=[-65537,-17,-9,-1,0,1,9,17];dim=[0,31,32,33,255]
    for seed,(active,secondary,case)in enumerate(itertools.product([0,1,0x80000000,0xFFFFFFFF],[0,1,0x80000000,0xFFFFFFFF],range(8))):
        width,height=dim[seed%5],dim[(seed+2)%5];max_x=(max(width,32)*8-128)*4096;max_z=(max(height,24)*8-96)*4096
        x=[-0x8000000,0,0x7FFFF,0x80000,0x80001,max_x-1,max_x,max_x+1][case];z=[-0x8000000,0x5FFFF,0x60000,0x60001,max_z-1,max_z,max_z+1,0x8000000][(case+3)%8];cx=min(max(x,0x80000),max_x);cz=min(max(z,0x60000),max_z)
        result.append(dict(name=f'tracking-{seed}',seed=seed,index=[0,1,127,255][seed%4],rowX=0,rowZ=0,width=width,height=height,count=1,offset=[-32768,32767],active=active,secondary=secondary,vector=[x,0x12345678,z],reference=[cx-signed[case],-2147483648,cz-signed[(case+2)%8]],source=[0,0,0]))
    return result

def model(result):
    p=result['profile'];before=result['before'];expected=bytearray(before)
    shift=0 if p['active']!=0 else 3 if p['secondary']!=0 else 4;max_x=(max(p['width'],32)*8-128)*4096;max_z=(max(p['height'],24)*8-96)*4096
    x=min(max(p['vector'][0],0x80000),max_x);z=min(max(p['vector'][2],0x60000),max_z);rx,ry,rz=p['reference'];dx=x-rx;dz=z-rz
    if not all(-0x80000000<=v<=0x7FFFFFFF for v in[dx,dz,rx+(dx>>shift),rz+(dz>>shift)]):raise ValueError('742 profile violates bounded signed32 domain')
    values=[rx+(dx>>shift),rz+(dz>>shift)];writes=[]
    for offset,value in zip([0x40,0x48],values):
        address=M.STATE+offset;word=value&0xFFFFFFFF;expected[address-M.BASE:address-M.BASE+4]=struct.pack('<I',word);writes.append([address,4,word])
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError(('742 independent full nonstack model differs',p['name']))
    if[row[1:]for row in result['nonstackWrites']]!=writes:raise ValueError('742 independent exact ordered two-word updates differ')
    if result['coreRegistersAndCpsr'][0]!=M.STATE:raise ValueError('742 physical nonsemantic state-address R0 differs')
    calls=result['nativeCalls']
    if[len(calls),calls[0]['entry'],calls[0]['preparedWords']]!=[3,0x02219CE4,[M.STACK-16]]:raise ValueError(('742 local12-byte clamp/native helper sequence differs',calls))
    if calls[1]['entry']!=0x021DF1F0 or calls[2]['entry']!=0x021DF3BC or calls[2]['preparedWords']!=[p['index']]:raise ValueError('742 native selected-byte forwarding differs')
    return dict(shift=shift,clampedLocalTarget=[x,z],expectedReference=values,orderedNonstackWrites=2,completeNonstackRamChecked=True,globalInputVectorUnchanged=True,rawR0=M.STATE,actualNativeDependencyReturns=3)
