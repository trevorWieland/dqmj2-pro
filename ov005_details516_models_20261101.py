import hashlib
from ov005_details516_machine_20261101 import BASE,STACK,OBJECTS,HANDLES


def profiles():
    return[dict(name=f'mode{mode}-inputs{n}',mode=mode,count=[0,0xFFFFFFFF][n],otherCount=[998,0xFFFF][n],flags=[0,0xFFFFFFFF][n],ioByte=[0xA5,0x5A][n],objectByte=[0x3C,0xC3][n],sizes=[0,1,16,0xFFFFFFFF,0x80000000],returnWord=[0x12345678,0xFFFFFFFF][n],message=0x1357+n)for mode in list(range(7))+[255]for n in range(2)]


def model(result):
    p=result['profile'];expected=bytearray(result['before']);io=bytearray(result['ioBefore'])
    def put(a,v,n):expected[a-BASE:a-BASE+n]=(v&((1<<(n*8))-1)).to_bytes(n,'little')
    for offset,value,size in[(0x2C,0,4),(0x34,0,4),(8,3,1),(0x10,0,2)]:put(0x021E9818+offset,value,size)
    for address in OBJECTS:put(address,0,4)
    for address in OBJECTS:
        value=int.from_bytes(expected[address-BASE+0x7C:address-BASE+0x80],'little');put(address+0x7C,value|2 if address==OBJECTS[0]else value&~2,4)
    for index,address in enumerate(HANDLES):
        put(0x021E992C+index*4,address,4)
        value=int.from_bytes(expected[address-BASE+0x18:address-BASE+0x1C],'little');put(address+0x18,value|2,4)
    for offset,first,priority in[(8,0x110,3),(10,0x4210,1),(12,0x4410,0),(14,0x618,2)]:
        initial=int.from_bytes(io[offset:offset+2],'little');value=((initial&0x43)|first)&~3|priority;io[offset:offset+2]=value.to_bytes(2,'little')
    for offset,value in[(0x10,0),(0x14,0x100),(0x18,0x100),(0x1C,0)]:io[offset:offset+4]=value.to_bytes(4,'little')
    initial=int.from_bytes(io[:4],'little');io[:4]=((initial&~0x1F00)|0x1F00).to_bytes(4,'little')
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError('516 independent complete nonstack model differs')
    if bytes(io)!=result['ioAfter']or result['vramAfter']!=bytes(0x80000):raise ValueError('516 mapped IO/VRAM storage model differs')
    if result['returnedR0']!=p['returnWord']:raise ValueError('516 physical R0 differs')
    if(result['strings'],result['loads'],result['sizes'],result['handles'])!=(5,5,5,9):raise ValueError('516 provider counts differ')
    count=2 if p['mode']in[3,6]else 4
    if len(result['formats'])!=count or len(result['draws'])!=count:raise ValueError('516 format/draw count differs')
    formats=result['formats'];draws=result['draws']
    expectedValues=[result['nativeMessagePointer'],min(p['count'],999)]
    if count==4:expectedValues.extend([0x026020B0,min(p['otherCount'],999)])
    wantedIndices=[1,4,5,8][:count]
    for index,(f,d,value,slot)in enumerate(zip(formats,draws,expectedValues,wantedIndices)):
        seen=f['words'][1]if index%2==0 else f['words'][0]
        if seen!=value or d['index']!=slot or d['dataSha256']!=f['outputSha256']:raise ValueError('516 clamped/raw format value orcopied output differs')
    last=0x021DDDEC if p['mode']in[3,6]else 0x021DDEC4
    if result['providedEvents'][-1]['address']!=last:raise ValueError('516 state-specific final boundary differs')
    return dict(independentlyModeled=True,physicalR0=p['returnWord'],formats=count,fullWordResultHandles=9,mappedHardwareOnly=True)
