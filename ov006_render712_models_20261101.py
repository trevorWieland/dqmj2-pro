import itertools
import struct
import ov006_render712_machine_20261101 as M


def profiles():
    result=[];values=[0,1,999998,999999,1000000,0xFFFFFFFF];stats=[0,1,9998,9999,10000,0xFFFFFFFF]
    for seed,(reset,name,index)in enumerate(itertools.product([0,1,0x80000000,0xFFFFFFFF],[0,65,128,255],range(6))):
        record=bytearray((offset*13+seed*7+1)&255 for offset in range(64));record[0x14]=name;struct.pack_into('<H',record,0x2C,[0,1,0x8000,0xFFFF][seed%4]);struct.pack_into('<3I',record,0x30,[0,1,0x80000000,0xFFFFFFFF][seed%4],values[index],values[(index+1)%6]);result.append(dict(name=f'render-{seed}',resetWord=reset,recordWord=[0,1,0x80000000,0xFFFFFFFF][seed%4],record=list(record),stats=[stats[index],stats[(index+2)%6],stats[(index+4)%6]],returnWord=[0,1,0x80000000,0xFFFFFFFF][seed%4]))
    return result


def model(result):
    p=result['profile'];record=bytes(p['record']);calls=[]
    def call(entry,*words):calls.append(dict(entry=entry,preparedWords=list(words)))
    call(0x020685F0,p['recordWord']);call(0x0206877C,p['recordWord'])
    if p['resetWord']!=0:
        call(0x021E75EC,41);call(0x021E749C,42,3,0,15,2)
        for index in range(43,47):call(0x021E75EC,index)
    for index in range(41,47):call(0x021E7B64,index)
    if record[0x14]!=0:call(0x021E7824,41,M.RECORD+0x14,0,0,19,1,0)
    else:call(0x021E791C,41,0x022084F8,0,0,19,1,0)
    identifier=struct.unpack_from('<H',record,0x2C)[0];kind=struct.unpack_from('<I',record,0x30)[0]
    call(0x021E796C,42,identifier,1,0);call(0x0220769C,identifier);call(0x021E791C,42,M.TEXT_A,3,0,15,1,0);call(0x021E92BC,kind);call(0x021E791C,43,M.TEXT_B,0,0,13,1,1)
    for slot,offset,fallback in[(44,0x34,0x0220D3D0),(45,0x38,0x0220D3D4)]:
        value=struct.unpack_from('<I',record,offset)[0]
        if value!=0:call(0x021E78AC,slot,min(value,999999),6,0,0,9,1,1)
        else:call(0x021E775C,slot,fallback,0,0,9,1,1)
        call(0x021E791C,slot,0x02208504,9,0,2,1,1)
    for value,x,label,label_x,width in zip(p['stats'],[4,11,18],[0x02208518,0x02208514,0x02208510],[9,16,23],[2,2,5]):
        call(0x021E78AC,46,min(value,9999),4,x,0,5,1,1);call(0x021E791C,46,label,label_x,0,width,1,0)
    actual=[dict(entry=item['entry'],preparedWords=item['preparedWords'])for item in result['providedCalls']]
    if actual!=calls:raise ValueError(('712 independently expected complete call order/full words differ',p['name'],actual,calls))
    if result['coreRegistersAndCpsr'][0]!=p['returnWord']:raise ValueError('712 last supplied rawR0 passthrough differs')
    before,after=result['before'],result['after'];lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if before[:lo]!=after[:lo]or before[hi:]!=after[hi:]:raise ValueError('712 independent nonstack RAM unchanged model differs')
    if any(item['ramEffects']for item in result['providedCalls']):raise ValueError('712 provided effect should be empty')
    return dict(providedCalls=len(calls),expectedPhysicalR0=p['returnWord'],allNonstackRamUnchanged=True,nameStackWord4=19,counterCaps=[999999,9999],allMinimum7And8WordViewsChecked=True)
