import struct
from wave20261105_socket_thumb_next_memory import Memory

CTX,DATA,OUT,TEXT,CONNECTION=0x02400000,0x02410000,0x02420000,0x02430000,0x02440000
SP,STOP=0x027f0000,0x027d0000
SPECS={'0209075c':16,'02090794':32,'0209088c':16,'0209302c':24,'020930ac':16,'020936f4':24,'02093774':16}
NAMES=list(SPECS)


def fixtures(name):
    if name=='0209075c':return [dict(host=n) for n in [0,1,0xffffffff,0x80000001,0x01020304,0xaabbccdd]]
    if name=='02090794':return [dict(family=f,length=n,octets=list(b),alias=a) for f,n,b,a in [(0,16,b'\x01\x02\x03\x04',False),(3,16,b'\x01\x02\x03\x04',False),(2,15,b'\x01\x02\x03\x04',False),(2,16,b'\x00\x00\x00\x00',False),(2,16,b'\xff\xff\xff\xff',False),(2,32,b'\xc0\x00\x02\x01',False),(2,16,b'\x80\x01\xfe\x00',True)]]
    if name=='0209088c':return [dict(invalid=bad,mode=mode,state=state,handle=handle,result=0x80000001) for bad,mode,state,handle in [(1,0,1,0),(1,0,1,0xffffffff),(1,0,1,CTX),(0,1,1,CTX),(0,2,1,CTX),(0,-1,1,CTX),(0,0,0,CTX),(0,4,0,CTX),(0,0,3,CTX),(0,4,1,CTX),(0,0,0x8001,CTX),(0,4,0xffff,CTX)]]
    if name in ['0209302c','020936f4']:
        rows=[dict(length=n,low=(0xfffffff8 if i in [2,7] else 0x12340000|([0,1,55,56,63][i%5]<<3)),high=[0,0xffffffff,0x80000000][i%3],seed=i) for i,n in enumerate([0,1,2,55,56,63,64,65,129,193])]
        return rows+[dict(length=64,low=0,high=0,seed=10),dict(length=1,low=0xfffffff8,high=0xffffffff,seed=11)]
    return [dict(low=0x23450000|(n<<3)|(i&7),high=[0,1,0xffffffff][i%3],seed=i) for i,n in enumerate([0,1,55,56,63,17])]


def words(raw,count):return list(struct.unpack_from('<'+'I'*count,raw))


def fold(state,block):
    total=sum(block)&0xffffffff
    return [((value+total+(i+1)*0x10203)^int.from_bytes(block[i*4:i*4+4],'little'))&0xffffffff for i,value in enumerate(state)]


def update(raw,data,count):
    raw=bytearray(raw);lowoff=16 if count==4 else 24;highoff=20;bufferoff=24 if count==4 else 28
    low,high=struct.unpack_from('<I',raw,lowoff)[0],struct.unpack_from('<I',raw,highoff)[0];total=(((high<<32)|low)+len(data)*8)&0xffffffffffffffff
    struct.pack_into('<I',raw,lowoff,total&0xffffffff);struct.pack_into('<I',raw,highoff,total>>32)
    index=(low>>3)%64;remaining=64-index;offset=0;operations=[]
    if len(data)>=remaining:
        raw[bufferoff+index:bufferoff+64]=data[:remaining];operations.append(('copy',0,bufferoff+index,remaining,bytes(raw)))
        state=fold(words(raw,count),bytes(raw[bufferoff:bufferoff+64]));struct.pack_into('<'+'I'*count,raw,0,*state);operations.append(('transform',None,bufferoff,64,bytes(raw)))
        offset=remaining
        while offset+64<=len(data):
            state=fold(words(raw,count),data[offset:offset+64]);struct.pack_into('<'+'I'*count,raw,0,*state);operations.append(('transform',offset,None,64,bytes(raw)));offset+=64
        index=0
    raw[bufferoff+index:bufferoff+index+len(data)-offset]=data[offset:];operations.append(('copy',offset,bufferoff+index,len(data)-offset,bytes(raw)))
    return bytes(raw),operations


def scenario(name,f,ordinal):
    memory=Memory({CTX:160,DATA:320,OUT:64,TEXT:64,CONNECTION:16},ordinal);actions=[]
    def action(address,args,returned=None,mutations=(),checks=(),stack=()):
        if returned is None:returned=0xa7000000+len(actions)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=list(checks),mutations=list(mutations),stackWords=list(stack)))
        for at,raw in mutations:
            if not SP-256<=at<SP+256:memory.put(at,raw)
    memory.put(TEXT,b'198.51.100.7\0');initial=memory.snapshot();result=None
    if name=='0209075c':
        args=[TEXT,OUT,0x12345678,0x87654321];action(0x209009c,[TEXT],f['host'])
        if f['host']:memory.put(OUT,f['host'].to_bytes(4,'big'));result=1
        else:result=0
    elif name=='02090794':
        source=OUT if f['alias'] else DATA;octets=bytes(f['octets']);memory.put(source,octets);initial=memory.snapshot();args=[f['family'],source,OUT,f['length']]
        if f['family']!=2 or f['length']<16:result=0
        else:
            word=int.from_bytes(octets,'little');action(0x2008e0c,[source,SP-16,4],mutations=[(SP-16,octets)])
            action(0x20907e4,[word,SP-20],mutations=[(SP-20,word.to_bytes(4,'big'))])
            text='.'.join(map(str,octets)).encode()+b'\0';action(0x20061ac,[OUT,16,0x20de81c,octets[0]],len(text)-1,[(OUT,text)],[(0x20de81c,b'%d.%d.%d.%d\0')],octets[1:]);result=OUT
    elif name=='0209088c':
        memory.set(CTX+0x70,f['state'],2);memory.set(CTX+0x73,f['mode'],1);initial=memory.snapshot();args=[f['handle'],CONNECTION,0x12345678,0x87654321];action(0x2090294,[f['handle']],f['invalid'])
        if f['invalid'] or f['mode'] not in [0,4]:result=0xffffffe4
        elif not f['state']&1:result=0xffffffd9
        elif f['state']&2:result=0xffffffe4
        else:action(0x20908f0,[CTX,CONNECTION],f['result']);result=f['result']
    else:
        count=4 if name in ['0209302c','020930ac'] else 5;lowoff=16 if count==4 else 24;bufferoff=24 if count==4 else 28;size=bufferoff+64
        memory.set(CTX+lowoff,f['low']);memory.set(CTX+20,f['high']);data=bytes((i*29+f['seed']*11)&255 for i in range(320));memory.put(DATA,data);initial=memory.snapshot();raw=memory.read(CTX,size)
        if name in ['0209302c','020936f4']:
            args=[CTX,DATA,f['length'],0x87654321];final,operations=update(raw,data[:f['length']],count);total=(((f['high']<<32)|f['low'])+f['length']*8)&0xffffffffffffffff;memory.set(CTX+lowoff,total&0xffffffff);memory.set(CTX+20,total>>32)
            for kind,source,destination,length,after in operations:
                if kind=='copy':action(0x2008e0c,[DATA+source,CTX+destination,length],mutations=[(CTX+destination,data[source:source+length])],checks=[(CTX,memory.read(CTX,size))])
                else:
                    block=(CTX+destination) if source is None else DATA+source;provider=0x2092cb8 if count==4 else 0x2093180
                    action(provider,[CTX,block],mutations=[(CTX,after[:count*4])],checks=[(CTX,memory.read(CTX,size))])
            if memory.read(CTX,size)!=final:raise ValueError('Independent update model/actions disagree')
        else:
            args=[CTX,OUT,0x12345678,0x87654321];endian='little' if count==4 else 'big';encode=0x2092c98 if count==4 else 0x2093128;updateAddress=0x209302c if count==4 else 0x20936f4;counteroff=16 if count==4 else 20
            bits=b''.join(memory.get(CTX+counteroff+i*4).to_bytes(4,endian) for i in range(2));action(encode,[OUT,CTX+counteroff,8],mutations=[(OUT,bits)],checks=[(CTX,raw)])
            index=(f['low']>>3)%64;padding=(56 if index<56 else 120)-index;padAddress=0x20de8d8 if count==4 else 0x20dea18;pad=b'\x80'+bytes(63);new,unused=update(memory.read(CTX,size),pad[:padding],count)
            action(updateAddress,[CTX,padAddress,padding],mutations=[(CTX,new)],checks=[(padAddress,pad),(CTX,memory.read(CTX,size))]);new,unused=update(memory.read(CTX,size),bits,count);action(updateAddress,[CTX,OUT,8],mutations=[(CTX,new)],checks=[(OUT,bits),(CTX,memory.read(CTX,size))])
            digest=b''.join(memory.get(CTX+i*4).to_bytes(4,endian) for i in range(count));action(encode,[OUT,CTX,count*4],mutations=[(OUT,digest)],checks=[(CTX,memory.read(CTX,size))])
    stateReads=(0 if f['invalid'] or f['mode'] not in [0,4] else 1 if not f['state']&1 else 2) if name=='0209088c' else None
    return dict(initial=initial,regions=memory.snapshot(),args=args,actions=actions,result=result,volatileStateReads=stateReads)
