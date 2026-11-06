import struct
SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
FRAME=0x02714000
OUT=0x02718000
MAC=0x02716000
IE=0x0271d000
GAME=0x0271e000
SLOT=0x0380fff4
VTSF=0x0380fff0


def p16(n):return struct.pack('<H',n&65535)
def p32(n):return struct.pack('<I',n&0xffffffff)


def fixtures():
    rows=[]
    for pattern in ['empty','match-first','match-late','oldest','no-slot','mixed']:
        for length in [0,3,32,33]:rows.append(dict(entry=0x027f4b88,kind='cache',pattern=pattern,length=length,channel=0x8123,signal=0xa5b6))
    for status in [0,1,65535]:
        for aid in [0,1,2007]:
            for length in [None,0,3,16]:rows.append(dict(entry=0x027f1888,kind='assoc',status=status,aid=aid,length=length,allocated=True))
    rows.append(dict(entry=0x027f1888,kind='assoc',status=0,aid=1,length=None,allocated=False))
    for length in [0,1,8,16]:
        for align in [0,1,3]:rows.append(dict(entry=0x027f1be8,kind='probe',gameLength=length,align=align,enabled=True,allocated=True,race=align==3))
    rows.extend([dict(entry=0x027f1be8,kind='probe',gameLength=8,align=0,enabled=False,allocated=True,race=False),dict(entry=0x027f1be8,kind='probe',gameLength=8,align=0,enabled=True,allocated=False,race=False)])
    for kind in [0,0xb0,0x10,0x30,0xa0,0xc0]:
        for failed in [False,True]:
            for flag in [0,2]:rows.append(dict(entry=0x027f0484,kind='txdone',frameType=kind,failed=failed,flag=flag,cam=1,stationState=0x30,frameStatus=0,algo=0,seq=2,multicast=flag==2,moreData=flag==2,wep=not failed,ps=flag==0,remaining=1 if flag else 0))
    extra=next(dict(row)for row in rows if row['kind']=='txdone'and row['frameType']==0 and not row['failed']and row['flag']==2);extra['ps']=True;rows.append(extra)
    return rows


def scenario(f,ordinal):
    initial={};regions={};actions=[];allowed=[];context=bytearray((ordinal*7+i*13)&255 for i in range(1684));frame=bytearray((ordinal*3+i*11)&255 for i in range(256));out=bytearray((ordinal*17+i*5)&255 for i in range(512));mac=bytes.fromhex('0203456789ab');args=[];returned=None;entry=f['entry'];stack={0x027f4b88:40,0x027f1888:32,0x027f1be8:32,0x027f0484:40}[entry]
    def area(at,raw):initial[at]=bytes(raw);regions[at]=bytes(raw)
    def u16(raw,offset,value):struct.pack_into('<H',raw,offset,value&65535)
    def u32(raw,offset,value):struct.pack_into('<I',raw,offset,value&0xffffffff)
    def r16(raw,offset):return int.from_bytes(raw[offset:offset+2],'little')
    def r32(raw,offset):return int.from_bytes(raw[offset:offset+4],'little')
    def action(at,values=(),result=0,checks=(),mutations=()):actions.append(dict(address=at,args=[v&0xffffffff for v in values],returned=result&0xffffffff,checks=list(checks),mutations=list(mutations)))
    def output_write(at,raw):
        if not (OUT<=at and at+len(raw)<=OUT+len(out)):raise ValueError('Synthetic constructor output escaped buffer')
        out[at-OUT:at-OUT+len(raw)]=raw
    def byte_write(at,value,mutations=()):output_write(at,bytes([value&255]));action(0x027ead30,[at,value&255],mutations=[(at,bytes([value&255])),*mutations])
    def byte_read(at,value):action(0x027ead5c,[at],value)
    def header(destination):
        raw=bytearray(44);u16(raw,16,2);raw[24:30]=destination;raw[30:36]=bytes.fromhex('061122334455');raw[36:42]=bytes.fromhex('0a66778899aa');output_write(OUT+16,raw);action(0x027f1fb4,[OUT+16,MAC],mutations=[(OUT+16,bytes(raw))])
    area(SLOT,p32(CTX));area(VTSF,p16(0x8123));area(MAC,mac)
    if f['kind']=='cache':
        cache=572;length=f['length'];element=bytes([0xdd,length])+bytes((i*7+0x81)&255 for i in range(34));area(IE,element);u16(frame,18,f['signal']);frame[36:42]=mac;u16(frame,52,0x1234);u16(frame,54,0xa581);area(FRAME,frame);args=[f['channel'],FRAME,IE];lifetimes=[4,2,2,1024]
        for i in range(4):
            offset=cache+50*i;context[offset:offset+50]=bytes((i+j)&255 for j in range(50));u16(context,offset,0 if f['pattern']=='empty'or f['pattern']=='mixed'and i in [0,3]else 0x90);context[offset+6:offset+12]=bytes([i+0x20])*6;u16(context,offset+48,1024 if f['pattern']=='no-slot'else lifetimes[i])
        if f['pattern']=='match-first':context[cache+6:cache+12]=mac
        if f['pattern']=='match-late':context[cache+50*2+6:cache+50*2+12]=mac
        area(CTX,context);allowed.append((CTX+cache,CTX+cache+200));byte_read(IE+1,length)
        if length<=32:
            empty=oldest=4;life=1024;chosen=None
            for i in range(4):
                offset=cache+50*i
                if r16(context,offset):
                    equal=context[offset+6:offset+12]==mac;action(0x027ea480,[CTX+offset+6,FRAME+36],int(equal))
                    if equal:chosen=i;break
                    if r16(context,offset+48)<life:life=r16(context,offset+48);oldest=i
                else:empty=i
            if chosen is None:chosen=empty if empty!=4 else oldest if oldest!=4 else None
            if chosen is not None:
                offset=cache+chosen*50;context[offset:offset+50]=bytes(50);action(0x037fdf74,[0,CTX+offset,50],mutations=[(CTX+offset,bytes(50))]);u16(context,offset+48,1024);u16(context,offset,f['signal']&255);u16(context,offset+2,f['channel']);context[offset+6:offset+12]=mac;action(0x027ea0ec,[CTX+offset+6,FRAME+36],mutations=[(CTX+offset+6,mac)]);byte_read(IE+1,length);u16(context,offset+12,length)
                for j in range(length):byte_read(IE+2+j,element[2+j]);context[offset+14+j]=element[2+j];action(0x027ead30,[CTX+offset+14+j,element[2+j]],mutations=[(CTX+offset+14+j,bytes([element[2+j]]))])
                u16(context,offset+46,0x1234);u16(context,offset+4,0xa581)
        regions[CTX]=bytes(context)
    elif f['kind']=='assoc':
        u16(context,960,0xa581);area(CTX,context);area(OUT,out);allowed.append((OUT,OUT+96));status=f['status'];aid=0;args=[3,status,IE if f['length']is not None else 0];element=bytes([0xdd,f['length']or 0])+bytes((i+0x80)&255 for i in range(32));area(IE,element);action(0x037f886c,[CTX+392,96],OUT if f['allocated']else 0)
        if not f['allocated']:action(0x027eb078,[2]);returned=0
        else:
            u16(out,12,0xffff)
            if status==0:
                aid=f['aid'];action(0x027ebebc,[3],aid)
                if not aid:status=19
            action(0x027ec04c,[3],MAC);header(mac);u16(out,60,0xa581);u16(out,62,status);u16(out,64,(aid|0xc000)if aid else 0);rates=bytes([1,2,0x82,0x84]);output_write(OUT+66,rates);action(0x027f20dc,[OUT+66],4,mutations=[(OUT+66,rates)]);u16(out,22,10);u16(out,34,38);u16(out,36,0x10);destination=OUT+74
            if f['length']is None:byte_write(destination,0);byte_write(destination+1,0)
            else:
                byte_read(IE+1,f['length']);byte_read(IE,element[0]);byte_write(destination,element[0]);byte_write(destination+1,f['length'])
                for i in range(f['length']):byte_read(IE+2+i,element[2+i]);byte_write(destination+2+i,element[2+i])
            returned=OUT+16
        regions[OUT]=bytes(out)
    elif f['kind']=='probe':
        length=f['gameLength'];u16(context,946,0x1234);u16(context,960,0xa581);u16(context,958,11);u16(context,996,length);u32(context,992,GAME);u16(context,998,f['align']);u16(context,828,0xabcd);area(CTX,context);game=bytes((i*7+0x80)&255 for i in range(64));area(GAME,game);area(OUT,out);allowed.append((OUT,OUT+120+length));args=[MAC];action(0x027f1680,result=int(f['enabled']))
        if not f['enabled']:returned=0
        else:
            action(0x037f886c,[CTX+392,120+length],OUT if f['allocated']else 0)
            if not f['allocated']:action(0x027eb078,[2]);returned=0
            else:
                u16(out,12,0xffff);header(mac);u16(out,68,0x1234);u16(out,70,0xa581);ssid=bytes([0,2,0x51,0x5a]);rates=bytes([1,2,0x82,0x84]);output_write(OUT+72,ssid);action(0x027f2068,[OUT+72],4,mutations=[(OUT+72,ssid)]);output_write(OUT+76,rates);action(0x027f20dc,[OUT+76],4,mutations=[(OUT+76,rates)])
                for i,value in enumerate([3,1,11]):byte_write(OUT+80+i,value)
                tsf=0x8123;vendor=[221,length+8,0,9,0xbf,0,0xcd,0xab]
                for i,value in enumerate(vendor):
                    changed=[(VTSF,p16(0x4567))]if f['race']and i==7 else[];byte_write(OUT+83+i,value,changed)
                if f['race']:tsf=0x4567
                byte_write(OUT+91,tsf&255,[(VTSF,p16(0xbeef))]if f['race']else[]);byte_write(OUT+92,tsf>>8)
                if f['race']:regions[VTSF]=p16(0xbeef)
                at=GAME+(f['align']&1)
                for i in range(length):byte_read(at+i,game[(f['align']&1)+i]);byte_write(OUT+93+i,game[(f['align']&1)+i])
                u16(out,22,33+length);u16(out,34,61+length);u16(out,36,0x50);returned=OUT+16
        regions[OUT]=bytes(out)
    elif f['kind']=='txdone':
        control=f['frameType']|(0x4000 if f['wep']else 0)|(0x2000 if f['moreData']else 0);u16(frame,2,f['cam']);u16(frame,0,0);u16(frame,8,2 if f['failed']else 0);u16(frame,12,0xab05);u16(frame,18,64);u16(frame,20,control);frame[24:30]=bytes([3 if f['multicast']else 2,3,4,5,6,7]);u16(frame,44,f['algo']);u16(frame,46,f['seq']if f['frameType']==0xb0 else f['frameStatus']);u16(frame,48,0 if f['frameType']==0xb0 else 0xc003);u16(context,848,1);u16(context,1028,0);u16(context,424,2 if f['remaining']else 1);u16(context,1088,7)
        for offset in [1340,1344,1348,1356,1360,1364]:u32(context,offset,0xffffffff)
        area(CTX,context);area(FRAME,frame);args=[FRAME,f['flag']];allowed.extend([(CTX+1340,CTX+1368),(CTX+1088,CTX+1090)])
        def increment(offset,value=1):u32(context,offset,(r32(context,offset)+value)&0xffffffff)
        if not f['failed']:
            increment(1340);increment(1360 if f['multicast']else 1356);action(0x027ec02c,[f['cam']],int(f['ps']))
            if f['ps']and not f['moreData']:action(0x027ebdb4,[f['cam']])
        else:increment(1344)
        if f['wep']:increment(1364)
        increment(1348,5);typ=f['frameType']
        if typ==0xb0 and f['cam']and not f['failed']:
            if f['algo']==0 and f['seq']==2:action(0x027ebc50,[f['cam'],0x30]);action(0x027edb74,[FRAME+24,0])
        elif typ in [0x10,0x30]and f['cam']:
            if not f['failed']and f['frameStatus']==0:
                action(0x027ebfec,[f['cam']],f['stationState'])
                if f['stationState']==0x30:action(0x027ebc50,[f['cam'],0x40]);action(0x027edc6c if typ==0x10 else 0x027edd64,[FRAME+24,0xc003,FRAME+84])
            elif f['failed']:action(0x027ebf6c,[f['cam']]);action(0x027f1ec8,[FRAME+24,1,0],0)
        elif typ in [0xa0,0xc0]:
            action(0x027ebfec,[f['cam']],f['stationState'])
            if f['stationState']>(0x30 if typ==0xa0 else 0x20):action(0x027ebc50,[f['cam'],0x30 if typ==0xa0 else 0x20])
        action(0x027ebbe0,[FRAME]);u16(context,424,f['remaining']);action(0x037f8908,[CTX+416,FRAME-16],mutations=[(CTX+424,p16(f['remaining']))]);u16(context,1088,0)
        if f['flag']and f['remaining']:action(0x027eff00,[1])
        regions[CTX]=bytes(context)
    else:raise ValueError('Unknown independent WL model family')
    return dict(args=args,initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=stack,returnValue=returned)
