import struct
SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
FRAME=0x02714000
GAME=0x02718000
TABLE=0x0271a000
SLOT=0x0380fff4
VTSF=0x0380fff0
DTIM=0x04808084
BROADCAST=0x027f74b0


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


def fixtures():
    rows=[]
    for mode in [1,2]:
        for index in [0,3,255]:
            for state in [32,64]:rows.append(dict(entry=0x027f0e64,multicast=False,maximum=16,mode=mode,index=index,state=state,race=False))
    for maximum in [1,2,16]:rows.append(dict(entry=0x027f0e64,multicast=True,maximum=maximum,mode=1,index=0,state=64,race=False))
    rows.append(dict(entry=0x027f0e64,multicast=True,maximum=16,mode=1,index=0,state=64,race=True))
    for aid in [0,1,0x3fff,0x4000,0x7fff,65535]:rows.append(dict(entry=0x027f1f5c,aid=aid))
    for included,length,game,power,bug in [(True,0,0,1,False),(True,1,0,1,True),(True,1,1,1,False),(True,1,8,0,True),(True,2,1,0,False),(True,2,8,1,True),(True,32,8,1,True),(False,32,0,1,False),(False,32,1,0,True),(False,0,8,1,True)]:rows.append(dict(entry=0x027f1210,included=included,length=length,game=game,power=power,bug=bug,race=False))
    rows.append(dict(entry=0x027f1210,included=True,length=1,game=8,power=1,bug=True,race=True));return rows


def scenario(f,ordinal):
    context=bytearray((ordinal*7+i*13)&255 for i in range(1684));frame=bytearray((ordinal*3+i*11)&255 for i in range(512));game=bytearray((ordinal*5+i*17)&255 for i in range(64));initial={SLOT:p32(CTX),VTSF:p16(0x8123),DTIM:p16(0xa5b6),BROADCAST:b'\xff'*6};regions=dict(initial);actions=[];allowed=[];args=[];entry=f['entry'];stack={0x027f0e64:16,0x027f1210:32,0x027f1f5c:8}[entry];mac=bytes.fromhex('061122334455');bssid=bytes.fromhex('0a66778899aa');context[804:810]=mac;context[936:942]=bssid
    def u16(raw,offset,value):raw[offset:offset+2]=p16(value)
    def u32(raw,offset,value):raw[offset:offset+4]=p32(value)
    def action(at,values=(),returned=0,checks=(),mutations=()):actions.append(dict(address=at,args=list(values),returned=returned,checks=list(checks),mutations=list(mutations)))
    def byte_read(at,value):action(0x027ead5c,[at],value,checks=[(at,bytes([value]))])
    def byte_write(at,value,mutations=()):
        if FRAME<=at<FRAME+512:frame[at-FRAME]=value&255
        elif GAME<=at<GAME+64:game[at-GAME]=value&255
        else:raise ValueError('Independent beacon byte model escaped borrowed buffers')
        action(0x027ead30,[at,value&255],mutations=[(at,bytes([value&255])),*mutations])
    if entry==0x027f0e64:
        u16(context,802,f['maximum']);u16(context,814,f['mode']);u32(context,796,TABLE);u16(frame,0,3 if f['multicast']else 2);args=[FRAME]
    elif entry==0x027f1f5c:u32(context,1116,FRAME);args=[f['aid']];allowed.append((FRAME,FRAME+64))
    else:
        u32(context,1196,FRAME);u16(context,826,0xa5a4|int(not f['included']));u16(context,828,0xabcd);u16(context,946,0x1234);u16(context,960,0xa581);u16(context,866,f['length']);context[868:900]=bytes((i*7+0x81)&255 for i in range(32));u16(context,958,0x010b);u16(context,952,0x1234);u16(context,996,f['game']);u32(context,992,GAME);u16(context,998,0x8123);u16(context,850,f['power']);u16(context,1000,0x7777);u16(context,1680,0x8000|(4 if f['bug']else 0));allowed.extend([(FRAME,FRAME+512),(CTX+982,CTX+988),(CTX+998,CTX+1002),(GAME,GAME+64),(DTIM,DTIM+2)])
    initial.update({CTX:bytes(context),FRAME:bytes(frame),GAME:bytes(game)})
    if entry==0x027f0e64:
        if f['multicast']:
            for i in range(1,f['maximum']):
                changed=[]
                if f['race']and i==1:u16(context,802,2);changed=[(CTX+802,p16(2))]
                action(0x027f0d6c,[i],mutations=changed)
                if f['race']:break
        else:
            action(0x027eb90c,[FRAME],f['index'])
            if f['index']!=255:action(0x027f0d6c,[f['index']])
            if f['mode']==1:
                action(0x027ebfec,[f['index']],f['state'])
                if f['state']==64:action(0x027ebc50,[f['index'],32]);action(0x027f0b0c)
    elif entry==0x027f1f5c:
        for offset in [0,2,4]:u16(frame,offset,0)
        u16(frame,10,20);u16(frame,12,0xa4);u16(frame,14,0xc000|f['aid']);frame[16:28]=bssid+mac;action(0x027ea108,[FRAME+16,CTX+936,CTX+804],mutations=[(FRAME+16,bssid+mac)])
    else:
        frame[0:8]=bytes(8);u16(frame,8,2);action(0x027ea584,returned=2,checks=[(FRAME,bytes(8))]);u16(frame,12,0x80);u16(frame,14,0);frame[16:34]=b'\xff'*6+mac+mac;action(0x027ea13c,[FRAME+16,BROADCAST,CTX+804,CTX+804],checks=[(BROADCAST,b'\xff'*6),(CTX+804,mac)],mutations=[(FRAME+16,b'\xff'*6+mac+mac)]);u16(frame,34,0);frame[36:44]=bytes(8);u16(frame,44,0x1234);u16(frame,46,0xa581);cursor=FRAME+48
        if f['included']:
            u16(context,982,12);byte_write(cursor,0);byte_write(cursor+1,f['length']);cursor+=2
            for i in range(f['length']):value=context[868+i];byte_read(CTX+868+i,value);byte_write(cursor,value);cursor+=1
            byte_write(cursor-f['length']-1,f['length'])
        else:u16(context,982,0)
        rates=bytes([1,2,0x82,0x84]);frame[cursor-FRAME:cursor-FRAME+4]=rates;action(0x027f20dc,[cursor],4,mutations=[(cursor,rates)]);cursor+=4
        for value in [3,1,11]:byte_write(cursor,value);cursor+=1
        offset=cursor-(FRAME+36);u16(context,984,offset);regions[DTIM]=p16(offset+2)
        for value in [5,5,0,0x34,0,0,0]:byte_write(cursor,value);cursor+=1
        offset=cursor-(FRAME+36);u16(context,986,offset);align=offset&1;u16(context,998,align);active=[0xcd,0xab]if f['power']==1 else[255,255]
        for i,value in enumerate([221,f['game']+8,0,9,0xbf,0,*active]):byte_write(cursor,value,[(VTSF,p16(0x4567))]if f['race']and i==7 else[]);cursor+=1
        tsf=0x4567 if f['race']else 0x8123;byte_write(cursor,tsf&255,[(VTSF,p16(0xbeef))]if f['race']else[]);cursor+=1;byte_write(cursor,tsf>>8);cursor+=1
        if f['race']:regions[VTSF]=p16(0xbeef)
        for i in range(f['game']):value=game[i];byte_read(GAME+i,value);byte_write(cursor,value);cursor+=1
        if align:
            for i in range(f['game']-1,-1,-1):value=game[i];byte_read(GAME+i,value);byte_write(GAME+i+1,value)
        if f['bug']:
            marker=((cursor+3)&~3)-FRAME;frame[marker:marker+4]=p16(0xb6b8)+p16(0x1d46)
        u16(context,1000,0);u16(frame,10,24+cursor-(FRAME+36)+4)
    regions.update({CTX:bytes(context),FRAME:bytes(frame),GAME:bytes(game)})
    return dict(args=args,initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=stack,returnValue=None)
