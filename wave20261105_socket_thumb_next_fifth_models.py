import itertools
from wave20261105_socket_thumb_next_memory import Memory

ADDRESS=0x021cfcf8
TEXT=0x02404000
END=0x02405000
OUTPUT=0x02405100
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208d71c':8,'0208e7f8':8,'0208e820':32,'0208e878':24}
MASK64=(1<<64)-1


def fixtures(name):
    if name=='0208d71c':return [dict(seed=s,multiplier=m,increment=a,mutate=t) for s,m,a,t in itertools.product([0,1,0xffffffff,0x8000000000000000,0x0123456789abcdef,0xffffffffffffffff],[0,1,0xffffffff00000001,0x8000000080000000,0xffffffffffffffff],[0,1,0xffffffff,0x8000000000000000,0xffffffffffffffff],[False,True])]
    if name=='0208e7f8':
        texts=[bytes([value]) for value in range(256)]+[b'0',b'0000',b'12345x',b'255.',b'256',b'4294967295',b'4294967296',b'42949672960!',b'18446744073709551615',b'999999999999999999999999999999x']
        return [dict(text=text.hex()) for text in texts]
    if name=='0208e820':
        octets=[b'0',b'1',b'127',b'128',b'255',b'256',b'4294967296',b'0000000000000000000000000000001']
        texts=[b'.'.join(parts) for parts in itertools.product(octets,repeat=2) for parts in [(parts[0],b'2',parts[1],b'4')]]
        texts += [b'',b'1',b'1.2',b'1.2.3',b'1.2.3.4',b'1.2.3.4.',b'1.2.3.4x',b'.1.2.3',b'1..2.3',b'-1.2.3.4',b' 1.2.3.4',b'255.255.255.255',b'4294967296.1.2.3',b'1.2.3.256',b'1.2.3.4294967296']
        texts += [b'1.'+bytes([value])+b'.3.4' for value in [0,47,58,127,128,255]]
        return [dict(text=text.hex()) for text in texts]
    return [dict(server=s,transaction=t,returned=r,mutate=m) for s,t,r,m in itertools.product([0,1,0x7f000001,0xffffffff],[0,1,32767,32768,65535],[0,1,0x80000000,0xffffffff],[False,True])]


def scenario(name,f,ordinal):
    text=bytes.fromhex(f.get('text',b'example.invalid'.hex()))+b'\0'
    memory=Memory({ADDRESS:128,TEXT:len(text),END:4,OUTPUT:4},ordinal);setv,getv=memory.set,memory.get;memory.put(TEXT,text)
    if name=='0208d71c':
        for offset,key in [(104,'seed'),(112,'multiplier'),(120,'increment')]:setv(ADDRESS+offset,f[key],8)
    initial=memory.snapshot();actions=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None,stackArgs=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if at>=SP-128:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes,stackArgs=stackArgs or []));return returned
    arguments=[TEXT,END,0x55667788,0x99aabbcc];result=None
    if name=='0208d71c':
        first=f['multiplier'];second=f['seed'];product=(first*second)&MASK64
        changes=[word(ADDRESS+120,f['increment']^0x13579bdf2468ace0,8),word(ADDRESS+104,0xa5a5a5a55a5a5a5a,8)] if f['mutate'] else []
        call(0x02026124,[first&0xffffffff,first>>32,second&0xffffffff,second>>32],[product&0xffffffff,product>>32],changes)
        value=(product+getv(ADDRESS+120,8))&MASK64;setv(ADDRESS+104,value,8);result=value>>32
    elif name=='0208e7f8':
        position=0;value=0;setv(END,TEXT)
        while text[position] in b'0123456789':value=(value*10+text[position]-48)&0xffffffff;position+=1;setv(END,TEXT+position)
        result=value
    elif name=='0208e820':
        arguments[:2]=[TEXT,OUTPUT];position=0;address=0;result=1
        for part in range(4):
            start=position;value=0
            while text[position] in b'0123456789':value=(value*10+text[position]-48)&0xffffffff;position+=1
            call(0x0208e7f8,[TEXT+start,SP-28],value,[word(SP-28,TEXT+position)])
            if position==start:result=0;break
            if value>255:result=0;break
            if part<3:
                delimiter=text[position];position+=1
                if delimiter!=46:result=0;break
            elif text[position]!=0:result=0;break
            address=((address<<8)|value)&0xffffffff
        if result:setv(OUTPUT,address)
    else:
        arguments[:3]=[TEXT,f['server'],f['transaction']]
        if not f['server']:result=0xffffffff
        else:
            call(0x0208d7c0,[]);call(0x0208d764,[]);call(0x0208d780,[0,53,f['server']])
            result=call(0x0208e644,[TEXT,1,f['transaction'],0],f['returned'],[(TEXT,b'z')] if f['mutate'] else [],[0])
            call(0x0208d7e0,[])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result,args=arguments)
