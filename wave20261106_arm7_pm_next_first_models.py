import struct
from project import ROOT
SP=0x027fc000
STOP=0x02010000
SHARED=0x03809eac
WORDS=SHARED+4
STATUS=SHARED+36
BLINK=0x03809edc
LED=0x038075dc
RECORDS=LED+4
IME=0x04000208
KEY=0x04000132
SERIAL=0x04000134
POWER=0x04000304


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)
def w32(raw,offset):return int.from_bytes(raw[offset:offset+4],'little')


def fixtures():
    rows=[]
    for i in range(24):rows.append(dict(entry=0x03804b80,kind='response',command=[0,0x60,0x61,127,128,255,256,0xffffffff][i%8],value=[0,255,256,0xabcdef01][i%4],error=[0,1,0xffffffff][i%3],results=[0xffffffff,0x80000000,3]if i%2 else[0]))
    for i in range(12):rows.append(dict(entry=0x03804bc4,kind='notification',command=[0,0x63,127,128,0x180,0xffffffff][i%6],value=[0,255,256,0x12345678][i%4],results=[1,0xffffffff,0]if i%2 else[0]))
    for command in [0x60,0x61,0x62,0x64,0xff]:
        for start in [False,True]:
            for queued in [False,True]:rows.append(dict(entry=0x038048e0,kind='receiver',command=command,start=start,end=True,index=0,queued=queued))
    for index in [1,3,15]:
        for end in [False,True]:rows.append(dict(entry=0x038048e0,kind='receiver',command=0x61,start=False,end=end,index=index,queued=False))
    for command in [0x61,0x62,0x64,0x63,0x12340061]:
        for available in [False,True]:
            for operation in [0x0e,0xffff0081]:rows.append(dict(entry=0x03804a20,kind='dispatcher',command=command,available=available,operation=operation,value=0x89abcdef,result=0x12345678))
    for pattern in [0,1,2,3,-1,-2147483648]:
        for led in [1,2]:rows.append(dict(entry=0x0380516c,kind='blink',pattern=pattern,counter=7,led=led,queued=led==1))
    image=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();data=image[RECORDS-0x037f8000:RECORDS-0x037f8000+144]
    for pattern in range(4,16):
        bits,length,resolution=struct.unpack_from('<QHH',data,(pattern-4)*12)
        for counter in [0,length*resolution-1,length*resolution]:rows.append(dict(entry=0x0380516c,kind='blink',pattern=pattern,counter=counter,led=1 if counter else 2,queued=True))
    for word in [0,1,2,3,0xffff,0x8002]:rows.append(dict(entry=0x038052fc,kind='power',word=word))
    for triggers in range(32):rows.append(dict(entry=0x03804fbc,kind='sleep',triggers=triggers,flags=(triggers%4)<<6,keys=0x8123,ime=triggers%2,serial=0x9345,control=0xd3))
    for flags in [0,0x40,0x80,0xc0]:rows.append(dict(entry=0x03804fbc,kind='sleep',triggers=2,flags=flags,keys=0x12345678,ime=0x8001,serial=0xcafe,control=0x7f))
    return rows


def scenario(f,ordinal):
    initial={};regions={};allowed=[];actions=[];entry=f['entry'];frame={0x038048e0:24,0x03804a20:24,0x03804b80:16,0x03804bc4:16,0x03804fbc:40,0x0380516c:16,0x038052fc:8}[entry]
    def area(at,raw,mutable=False):
        initial[at]=bytes(raw);regions[at]=bytes(raw)
        if mutable:allowed.append((at,at+len(raw)))
    def action(at,args=(),returned=0,checks=(),mutations=(),high=None):
        row=dict(address=at,args=[a&0xffffffff for a in args],returned=returned&0xffffffff,checks=list(checks),mutations=list(mutations))
        if high is not None:row['returnedHigh']=high&0xffffffff
        actions.append(row)
    def fifo(data,error,results):
        for returned in results:action(0x037fe410,[8,data,error],returned)
    if f['kind']in ['response','notification']:
        command,value=f['command'],f['value'];args=[command,value]
        if f['kind']=='response':args.append(f['error']);data=0x03000000|(((command&255)|128)<<8)|(value&255);error=f['error']
        else:data=((command<<8)&0x7f00)|(value&255);error=0
        fifo(data,error,f['results'])
    elif f['kind']=='receiver':
        shared=bytearray((ordinal*3+i*7)&255 for i in range(64));struct.pack_into('<HH',shared,4,(f['command']<<8)|0x35,0xcafe);area(SHARED,shared);allowed.append((WORDS,WORDS+32))
        data=(0x02000000 if f['start']else 0)|(0x01000000 if f['end']else 0)|(f['index']<<16)|((f['command']<<8)|0x35 if f['index']==0 else 0x8765);args=[data]
        if f['start']:shared[4:36]=bytes(32)
        struct.pack_into('<H',shared,4+f['index']*2,data&65535);regions[SHARED]=bytes(shared)
        command=shared[5]
        if f['end']:
            if command==0x60:fifo(0x0300e000,0,[0xfffffffe,5])
            elif command in [0x61,0x62]:
                action(0x03803b7c,[3,command,2,shared[4],int.from_bytes(shared[6:8],'little')],int(f['queued']))
                if not f['queued']:action(0x03804b80,[command,65535,1])
            else:action(0x03804b80,[command,1,0])
    elif f['kind']=='dispatcher':
        shared=bytearray((ordinal*7+i*3)&255 for i in range(64));area(SHARED,shared);allowed.append((STATUS,STATUS+4));message=0x02710000;area(message,struct.pack('<6I',0x98765432,f['command'],f['operation'],f['value'],0x31415926,0x27182818));args=[message];state=0x60000080
        action(0x037fdd00,returned=state);action(0x03803b0c,[3],int(f['available']))
        if not f['available']:
            action(0x037fdd14,[state]);action(0x03804b80,[f['command']&65535,65535,1])
        else:
            action(0x03803b28,[3]);action(0x037fdd14,[state]);command=f['command']
            if command==0x62:
                fifo(0x0300e200,0,[0xffffffff,0]);struct.pack_into('<I',shared,36,1);action(0x03804fbc,[f['operation']&31,f['value'],f['operation']&0xc0],checks=[(STATUS,p32(1))])
            elif command==0x61:
                struct.pack_into('<I',shared,36,2)
                if f['operation']==14:fifo(0x0300e100,0,[0x80000000,0])
                action(0x03804d40,[f['operation'],f['value']&65535],f['result'],checks=[(STATUS,p32(2))]);action(0x03804b80,[0x61,f['result'],0])
            elif command==0x64:action(0x03804f54,[f['operation']])
            else:action(0x03804b80,[command&65535,1,0])
            action(0x03803b40,[3])
        regions[SHARED]=bytes(shared)
    elif f['kind']=='blink':
        args=[];counter,pattern,led=f['counter'],f['pattern'],f['led'];area(BLINK,p32(counter)+p32(pattern));area(LED,p32(led));allowed.append((BLINK,BLINK+8))
        if pattern==0:
            action(0x03803b7c,[3,0x64,1,1],int(f['queued']))
            if f['queued']:action(0x0380528c,[1],mutations=[(BLINK,p32(0)+p32(1))]);regions[BLINK]=p32(0)+p32(1)
        elif pattern<4:
            if pattern!=led:action(0x03803b7c,[3,0x64,1,pattern])
        else:
            image=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();raw=image[RECORDS-0x037f8000:RECORDS-0x037f8000+144];area(RECORDS,raw);bits,length,resolution=struct.unpack_from('<QHH',raw,(pattern-4)*12)
            if not resolution or counter//resolution>=64:raise ValueError('Fixture outside defined64-bit shift/division domain')
            quotient,remainder=divmod(counter,resolution);action(0x03806e44,[counter,resolution],quotient,high=remainder);next_led=1 if bits&(1<<(63-quotient))else 2;counter=(counter+1)&0xffffffff
            if counter>=length*resolution:counter=0
            regions[BLINK]=p32(counter)+p32(pattern)
            if next_led!=led:action(0x03803b7c,[3,0x64,1,next_led])
    elif f['kind']=='power':
        args=[];area(POWER,p16(f['word']),True);regions[POWER]=p16(f['word']&~2);action(0x0380528c,[1],checks=[(POWER,regions[POWER])]);action(0x03804f54,[1],checks=[(POWER,regions[POWER])])
    elif f['kind']=='sleep':
        args=[f['triggers'],f['keys'],f['flags']];area(IME,p16(f['ime']),True);area(KEY,p16(0x2134),True);area(SERIAL,p16(f['serial']),True);shared=bytearray((ordinal+i*11)&255 for i in range(64));area(SHARED,shared);allowed.append((STATUS,STATUS+4));state,mask=0x60000080,0x8abc1234
        action(0x037fdd00,returned=state,checks=[(IME,p16(0))]);action(0x037fb928,[0x1ffffff],mask);action(0x03804c7c,[0],f['control']);action(0x0380528c,[2]);action(0x03804f54,[2]);action(0x03804f54,[2]);action(0x037fe708);action(0x03804d14,[1])
        if f['triggers']&1:regions[KEY]=p16(0x4000|f['keys']);action(0x037fb8f0,[0x1000],checks=[(KEY,regions[KEY])])
        if f['triggers']&4:action(0x037fb8f0,[0x400000])
        if f['triggers']&2:action(0x037fe5a8,[0x8000],mutations=[(SERIAL,p16(0x8000))]);action(0x037fe588,[0x40,0]);action(0x037fe588,[0x100,0x100]);action(0x037fb8f0,[0x80])
        if f['triggers']&8:action(0x037fb8f0,[0x100000])
        if f['triggers']&16:action(0x037fb8f0,[0x2000])
        action(0x037fdd14,[state]);action(0x03805160,checks=[(IME,p16(1))],mutations=[(SERIAL,p16(0x5a5a))]);action(0x03804c00,[0,f['control']]);action(0x03804d40,[6 if f['flags']&0x40 else 7,0]);action(0x03804d40,[4 if f['flags']&0x80 else 5,0]);regions[SERIAL]=p16(f['serial']if f['triggers']&2 else 0x5a5a)
        action(0x03804cf0,[1],checks=[(SERIAL,regions[SERIAL])]);action(0x037fe760);struct.pack_into('<I',shared,36,0);regions[SHARED]=bytes(shared);action(0x03804bc4,[0x63,0],checks=[(STATUS,p32(0))]);action(0x037fdd00);action(0x037fb8a4,[mask]);action(0x037fdd14,[state])
    else:raise ValueError('Unknown independent PM family model')
    return dict(args=args,initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=frame,returnValue=None)
