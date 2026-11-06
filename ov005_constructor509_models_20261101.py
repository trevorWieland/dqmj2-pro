from ov005_constructor509_machine_20261101 import BASE,STACK,OBJECTS


def profiles():
    return[dict(name=f'input{n}',flags=flags,ioByte=(n*31)&255,objectByte=(n*17+1)&255,sizes=[0,16,0xFFFF,0x80000000]if n%2 else[0x600,0x800,1,0xFFFFFFFF],returnWord=[0,1,0x80000000,0xFFFFFFFF][n%4])for n,flags in enumerate([0,2,0xFFFFFFFF,0x80000000,0x7FFFFFFD,0x12345678,0xAAAA5555,0x5555AAAA])]


def model(result):
    p=result['profile'];expected=bytearray(result['before']);io=bytearray(result['ioBefore'])
    def put(a,v,n):expected[a-BASE:a-BASE+n]=(v&((1<<(n*8))-1)).to_bytes(n,'little')
    put(0x021E9820,1,1);put(0x021E9868,0,4)
    for address in OBJECTS:put(address,0,4)
    for address in OBJECTS:
        value=int.from_bytes(expected[address-BASE+0x7C:address-BASE+0x80],'little');put(address+0x7C,value|2 if address in[0x021E9EA8]+OBJECTS[6:]else value&~2,4)
    for offset,first,priority in[(8,0x4004,2),(10,0x4210,1),(12,0x404,3),(14,0x518,0)]:
        initial=int.from_bytes(io[offset:offset+2],'little');value=((initial&0x43)|first)&~3|priority;io[offset:offset+2]=value.to_bytes(2,'little')
    for offset in[0x10,0x14,0x18,0x1C]:io[offset:offset+4]=bytes(4)
    initial=int.from_bytes(io[:4],'little');io[:4]=((initial&~0x1F00)|0x1F00).to_bytes(4,'little')
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError('509 independent nonstack model differs')
    if bytes(io)!=result['ioAfter']or result['vramAfter']!=bytes(0x80000):raise ValueError('509 mapped IO/VRAM storage model differs')
    if result['returnedR0']!=p['returnWord']:raise ValueError('509 last physical R0 differs')
    if(result['strings'],result['loads'],result['sizes'])!=(4,4,2):raise ValueError('509 descriptor provider sequence differs')
    return dict(independentlyModeled=True,lastPhysicalR0=p['returnWord'],suppliedDescriptorWrites=4,nativeDependencies=0)
