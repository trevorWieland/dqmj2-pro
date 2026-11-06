from wave20261105_socket_thumb_next_memory import Memory

CTX,OUT,INPUT,SP,STOP=0x02400000,0x02410000,0x02420000,0x027f0000,0x027d0000
SPECS={'02090c18':8,'02090c60':8,'02090cac':16,'020937dc':16,'02093824':24}
NAMES=list(SPECS)


def fixtures(name):
    if name=='02090c18':return [dict(raw=r.hex(),alias=False) for r in [b'\x00',b'\x7f',b'\x80',b'\x81\xff',b'\x82\x01\x00',b'\x84\xff\xff\xff\xff',b'\x85\x00\x00\x00\x00\x01',b'\x85\x01\x00\x00\x00\x00']]+[dict(raw='',alias=True)]
    if name=='02090c60':return [dict(old=old,length=length,alias=alias) for old,length,alias in [(0,0,False),(0,4,False),(3,5,False),(253,4,False),(254,0,False),(255,4,False),(256,0,False),(0,-1,False),(4,8,True),(253,4,True)]]
    if name=='02090cac':return [dict(text=s.hex(),tag=t)for s,t in [(b'490101',23),(b'500101',23),(b'000101',23),(b'990231',23),(b'19001231',24),(b'00000101',0xffffffff),(b'99999999',24),(b'::::::::',23),(b'\xff'*8,24)]]
    if name=='020937dc':return [dict(length=n,alias=alias,pattern=p)for n,alias,p in [(0,False,0),(1,False,1),(3,False,2),(255,False,3),(256,False,4),(257,False,5),(-1,False,6),(16,True,7)]]
    return [dict(length=n,x=x,y=y,alias=alias,pattern=p)for n,x,y,alias,p in [(0,3,9,False,0),(-1,255,254,False,1),(1,255,255,False,2),(2,254,1,False,3),(17,0,0,False,4),(256,253,251,False,5),(17,1,128,True,6),(1,0,0,True,7)]]


def scenario(name,f,ordinal):
    memory=Memory({CTX:512,OUT:512,INPUT:512},ordinal);result=None;args=[];readable=[(CTX,512),(OUT,512),(INPUT,512)]
    if name=='02090c18':
        source=CTX if f['alias'] else INPUT;memory.set(CTX,source)
        if not f['alias']:memory.put(source,bytes.fromhex(f['raw']))
        initial=memory.snapshot();cursor=source+1;value=memory.get(source,1);overflow=False
        if value&128:
            count=value&127;value=0
            for i in range(count):
                if value&0xff000000:overflow=True;break
                value=((value<<8)+memory.get(cursor,1))&0xffffffff;cursor+=1
        if overflow:result=0xffffffff
        else:memory.set(CTX,cursor);result=value
        args=[CTX,0x11773355,0x22334455,0x33445566]
    elif name=='02090c60':
        memory.put(OUT,bytes(65+(i%26)for i in range(f['old']))+b'\0');memory.put(INPUT,bytes((i*17+3)&255 for i in range(512)));source=OUT+(254 if f['old']>=253 else 0)if f['alias']else INPUT
        initial=memory.snapshot();cursor=OUT;old=memory.get(cursor,1)
        if old:
            while memory.get(cursor,1):cursor+=1
        if not old or cursor-OUT<255:
            if old:memory.set(cursor,44,1);memory.set(cursor+1,32,1);cursor+=2
            count=f['length']&0xffffffff
            while count and cursor-OUT<255:memory.set(cursor,memory.get(source,1),1);cursor+=1;source+=1;count=(count-1)&0xffffffff
            memory.set(cursor,0,1)
        args=[OUT,OUT+(254 if f['old']>=253 else 0)if f['alias']else INPUT,f['length']&0xffffffff,0x33445566]
    elif name=='02090cac':
        text=bytes.fromhex(f['text']);memory.put(INPUT,text);initial=memory.snapshot();year=text[0]*10+text[1]-528;at=2
        if f['tag']==23:year+=2000 if year<50 else 1900
        else:year=year*100+text[2]*10+text[3]-528;at=4
        result=((year<<16)+((text[at]*10+text[at+1]-528)<<8)+(text[at+2]*10+text[at+3]-528))&0xffffffff;args=[INPUT,f['tag']&0xffffffff,0x22334455,0x33445566]
    elif name=='020937dc':
        memory.put(INPUT,bytes((i*23+f['pattern']*37)&255 for i in range(512)));key=CTX+2 if f['alias']else INPUT;initial=memory.snapshot();memory.set(CTX,0,1);memory.set(CTX+1,0,1)
        for i in range(256):memory.set(CTX+2+i,i,1)
        j=position=0
        for i in range(256):
            value=memory.get(CTX+2+i,1);j=(j+value+memory.get(key+position,1))&255;memory.set(CTX+2+i,memory.get(CTX+2+j,1),1);memory.set(CTX+2+j,value,1);position=(position+1)&255
            if position>=f['length']:position=0
        args=[CTX,key,f['length']&0xffffffff,0x33445566]
    else:
        memory.set(CTX,f['x'],1);memory.set(CTX+1,f['y'],1);memory.put(CTX+2,bytes((i*(2*f['pattern']+1)+f['pattern']*17)&255 for i in range(256)));memory.put(OUT,bytes((i*31+f['pattern']*13)&255 for i in range(512)));data=CTX+5 if f['alias']else OUT;initial=memory.snapshot();x,y=f['x'],f['y']
        for i in range(max(f['length'],0)):
            x=(x+1)&255;first=memory.get(CTX+2+x,1);y=(y+first)&255;second=memory.get(CTX+2+y,1);memory.set(CTX+2+x,second,1);memory.set(CTX+2+y,first,1);memory.set(data+i,memory.get(data+i,1)^memory.get(CTX+2+((first+second)&255),1),1)
        memory.set(CTX,x,1);memory.set(CTX+1,y,1);args=[CTX,data,f['length']&0xffffffff,0x33445566]
    return dict(initial=initial,regions=memory.snapshot(),args=args,actions=[],result=result,volatileStateReads=None,readable=readable,data=locals().get('data'),dataLength=max(f.get('length',0),0))
