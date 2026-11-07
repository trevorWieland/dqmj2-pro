from wave20261106_arm7_wl_followon_source_receive_fixture import Plan, SP, STOP, p16, p32

FIRST = 0x02720000
SECOND = 0x02721000
CHILD = 0x02724000
OTHER_CHILD = 0x02724400
NEW_CHILD = 0x02724800
RECORDS = 0x02730000
OUT = 0x0271a000
COUNT = 0x022388ec
FRAMES = {0x021dbd3c:8,0x021dbd8c:16,0x021e2b1c:32,0x021f07dc:40,
          0x02218430:0,0x022189cc:32,0x02218c34:32,0x02218cf8:32}


def word(value):
    return value & 0xffffffff


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def fixtures():
    result=[dict(entry=entry,seed=n)for entry in FRAMES for n in range(48)]
    result.extend(dict(entry=0x02218430,seed=0,listMode=1,listCount=6,listCapacity=cap)for cap in[0,1,3,4,5,20,24,25])
    result.extend(dict(entry=0x02218430,seed=0,listMode=0,listCount=count,listCapacity=cap)for count in[0,1,6]for cap in[0,1,4,5,23,24])
    result.extend(dict(entry=0x02218430,seed=0,listMode=2,listCount=3,listCapacity=cap)for cap in[0,12])
    result.extend(dict(entry=0x021e2b1c,seed=0,pairCount=count,pairHit=hit,pairA=a,pairB=b)for count in[1,3,4]for hit in[-1,0,count-1]for a,b in[(-128,127),(127,-128),(0,0)])
    return result


def scenario(f, ordinal):
    entry, n = f['entry'], f['seed']
    p = Plan(ordinal, FRAMES[entry])
    p.buffers.clear();p.initial.clear();p.regions.clear()
    for address,size in [(FIRST,0x440),(SECOND,0x440),(CHILD,512),
                         (OTHER_CHILD,512),(NEW_CHILD,512),(RECORDS,256*40),(OUT,256)]:
        p.buffer(address,size,(ordinal*17+address//256)&255)
    p.u32(FIRST+0x1e8,CHILD)
    p.u32(SECOND+0x1e8,OTHER_CHILD)
    p.constant(0x021c6748,p32(RECORDS))
    reads,regions=[],[]

    def typed(address,width):
        value=int.from_bytes(p.read(address,width),'little')
        reads.append((address,width,value))
        return value

    if entry==0x02218430:
        mode=f.get('listMode',[0,1,2][n%3]);count=f.get('listCount',n%7)
        capacity=f.get('listCapacity',[0,1,3,4,5,7,8,11,12,20,24,200][n%12])
        p.args=[FIRST,OUT,capacity]
        p.write(FIRST+0x322,bytes([mode,count]))
        p.write(FIRST+0x35e,bytes([(n*13+i*41)&255 for i in range(6)]))
        p.write(CHILD+8,bytes([(255-n*7-i*19)&255 for i in range(6)]))
        regions=[(FIRST+0x322,2),(FIRST+0x35e,6),(CHILD+8,6)]
        p.allowed.append((OUT,OUT+24))
        p.capture();typed(FIRST+0x322,1);i=0
        while True:
            limit=6 if mode==1 else typed(FIRST+0x323,1)
            if i>=limit or capacity<=i*4:break
            value=typed(CHILD+8+i if mode==1 else FIRST+0x35e+i,1)
            p.u32(OUT+4*i,value);i+=1
        p.returned=i
    elif entry in[0x021dbd3c,0x021dbd8c]:
        first=entry==0x021dbd3c
        offset=0x220 if first else 0x222
        base=[-32768,-1,0,1,9998,9999,10000,32767][n%8]
        addition=[-20000,-1,0,1,20000][n%5]
        adjusted=[-0x80000000,-1,0,1,9998,9999,10000,0x7fffffff][n%8]
        flag=[0,1,128,255][(n//8)%4]
        p.args=[FIRST];p.u16(FIRST+offset,base);p.write(FIRST+0x238,b'\0')
        regions=[(FIRST+offset,2)]+([]if first else[(FIRST+0x238,1)])
        p.capture();typed(FIRST+offset,2)
        changes=[(FIRST+offset,p16(-base)),(FIRST+0x1e8,p32(NEW_CHILD))]
        p.action(0x0207c424 if first else 0x0207c52c,
                 [FIRST+0x1ec,CHILD+0x46],word(addition),mutations=changes)
        p.u16(FIRST+offset,-base);p.u32(FIRST+0x1e8,NEW_CHILD)
        value=base+addition
        if not first:
            p.action(0x021dbc64,[FIRST,2,word(value)],word(adjusted),
                     mutations=[(FIRST+0x238,bytes([flag]))])
            p.write(FIRST+0x238,bytes([flag]));typed(FIRST+0x238,1)
            value=1 if flag else adjusted
        p.returned=max(1,min(value,9999))
    elif entry==0x021e2b1c:
        total=f.get('pairCount',[-128,-1,0,1,3,4][n%6])
        after=[-1,0,1,3,4][n%5]
        targetA=f.get('pairA',[-129,-128,-1,0,1,127,128,255][n%8])
        targetB=f.get('pairB',[127,0,-1,-128,1,128,255,-129][n%8])
        p.args=[word(targetA),word(targetB)]
        p.buffer(COUNT,32,0x6a);p.write(COUNT+0x12,bytes([total&255]))
        p.buffer(SP-32,2,0x83)
        regions=[(COUNT+0x12,1),(SP-32,2)]
        p.capture();p.write(SP-32,b'\0\0');limit=signed(typed(COUNT+0x12,1),8);i=0;p.returned=0
        while i<limit:
            a=[-128,-1,0,127][(n+i)%4]
            b=[127,0,-1,-128][(n+i)%4]
            if n%3==0 and i==max(0,limit-1):a,b=targetA,targetB
            if 'pairHit'in f:a,b=(targetA,targetB)if i==f['pairHit']else(targetA^1,targetB^1)
            changes=[(SP-31,bytes([a&255])),(SP-32,bytes([b&255]))]
            if i==0 and n%2 and 'pairHit'not in f:changes.append((COUNT+0x12,bytes([after&255])))
            p.action(0x021e8178,[i,SP-31,SP-32],mutations=changes)
            for at,raw in changes:p.write(at,raw)
            actualA=signed(typed(SP-31,1),8)
            if actualA==targetA:
                actualB=signed(typed(SP-32,1),8)
                if actualB==targetB:p.returned=1;break
            limit=signed(typed(COUNT+0x12,1),8);i+=1
    elif entry==0x021f07dc:
        values=[FIRST,SECOND,word(0x81234567+n),word(0xffffffff-n),
                [0,1,0x80000000,0xffffffff][n%4],word(n*113),word(-n)]
        returned=[0,1,0x80000000,0xffffffff,0x12345678][n%5]
        p.args=values;p.buffer(SP-40,28,0xa5)
        for i,value in enumerate(values[4:]):p.constant(SP+4*i,p32(value))
        regions=[(SP,12)]
        p.capture()
        for i,value in enumerate(values[4:]):reads.append((SP+4*i,4,value))
        args=[*values[:4],0,values[4],values[5],0,values[6],0,0]
        for i,value in enumerate(args[4:]):p.u32(SP-40+4*i,value)
        p.action(0x021f0578,args,returned)
        p.returned=returned
    elif entry==0x022189cc:
        value=n%16;a=[0,1,31,127,255][n%5];b=[0,1,2,127,255][n%5]
        mode=[0,1,0x80000000,0xffffffff][n%4]
        firstValue=[0,1,128,255][n%4];otherValue=[255,128,1,0][n%4]
        returned=[0,1,0x80000000,0xffffffff][(n//4)%4]
        p.args=[FIRST,SECOND,value,mode]
        p.write(RECORDS+40*value+31,bytes([a,b]))
        p.write(OTHER_CHILD+0x86+a,bytes([firstValue]))
        p.write(OTHER_CHILD+0x86+b,bytes([otherValue]))
        p.buffer(SP-32,4,0xa5)
        regions=[(RECORDS,256*40),(OTHER_CHILD+0x86,256)]
        p.capture();p.action(0x0207afec,[value],RECORDS+40*value)
        a=typed(RECORDS+40*value+31,1)
        p.action(0x0207afec,[value],RECORDS+40*value)
        b=typed(RECORDS+40*value+32,1)
        firstValue=typed(OTHER_CHILD+0x86+a,1)
        otherValue=typed(OTHER_CHILD+0x86+b,1)if b else 0
        if mode:
            p.u32(SP-32,otherValue)
            p.action(0x0220e3a8,[FIRST,a,b,firstValue,otherValue],returned)
            p.returned=returned
        else:p.returned=min(firstValue,otherValue)if b else firstValue
    else:
        value=n%16;kind=[0,1,2,15][n%4]
        factor=[0,1,128,255][(n//4)%4];updated=[255,128,1,0][(n//3)%4]
        base=[-32769,-32768,-1,0,32767,32768,65535,0x7fffffff][(n//4)%8]
        scalar=[-32768,-1,0,32767][n%4]
        returned=[-1000,-1,0,1,9999][n%5]
        mode=1 if entry==0x02218c34 else 2
        p.args=[FIRST,SECOND,value]
        bits=(n*1737&0xfff0)|kind
        p.u16(RECORDS+40*value+8,bits)
        p.write(FIRST+0x356,bytes([factor]))
        p.buffer(SP-32,12,0xa5)
        regions=[(RECORDS,256*40),(FIRST+0x356,1)]
        p.allowed.append((FIRST+0x356,FIRST+0x357))
        p.capture();p.action(0x0207afec,[value],RECORDS+40*value)
        typed(RECORDS+40*value+8,2)
        if kind==1:
            typed(FIRST+0x356,1)
            if factor==0:p.write(FIRST+0x356,b'\1')
            for i,v in enumerate([0,mode,0]):p.u32(SP-32+4*i,v)
            p.action(0x021f07dc,[FIRST,SECOND,value,0,0,mode,0],word(returned),
                     checks=[(FIRST+0x356,p.read(FIRST+0x356,1))],mutations=[(FIRST+0x356,bytes([updated]))])
            p.write(FIRST+0x356,bytes([updated]));typed(FIRST+0x356,1)
            p.returned=word(updated*returned)
        else:
            p.action(0x021dbd30,[FIRST],word(scalar),
                     mutations=[(FIRST+0x1e8,p32(NEW_CHILD))])
            p.u32(FIRST+0x1e8,NEW_CHILD)
            p.action(0x0207b244,[value,word(scalar),NEW_CHILD+0x46],word(base))
            for i,v in enumerate([0,0,mode]):p.u32(SP-32+4*i,v)
            p.action(0x021f0858,[FIRST,SECOND,word(signed(base&65535,16)),value,0,0,mode],word(returned))
            p.returned=word(returned)
    result=p.finish()
    result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=[],
                  faultRegisters=[],spiReadScript=[],instructionBudget=10000,
                  typedReadRegions=regions,expectedTableReads=[],expectedFlagReads=reads)
    return result
