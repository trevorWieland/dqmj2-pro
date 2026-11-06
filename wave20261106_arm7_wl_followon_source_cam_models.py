import struct
SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
FRAME=0x02714000
TABLE=0x02718000
OUT=0x0271a000
SLOT=0x0380fff4
CLOSE=0x048080ac
OPEN=0x048080ae


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


def fixtures():
    rows=[]
    for cam in [1,15]:
        for state in [32,63,64,65535]:
            for mode in [1,2]:
                for aid in [0,3]:rows.append(dict(entry=0x027ebc50,cam=cam,state=state,mode=mode,aid=aid,power=bool(aid)))
        for mode in [1,2]:
            for count in [0,1,65535]:
                for skip in [False,True]:rows.append(dict(entry=0x027ebb50,cam=cam,mode=mode,count=count,skip=skip,race=False))
        for bitmap in [0,1,0xfffd,0xfffb,0x7fff,0xffff]:
            for connected in [0,65535]:rows.append(dict(entry=0x027ebebc,cam=cam,bitmap=bitmap,connected=connected))
        for state in [32,63,64,65]:rows.append(dict(entry=0x027ebdb4,cam=cam,state=state))
    rows.append(dict(entry=0x027ebb50,cam=1,mode=1,count=0,skip=False,race=True))
    for cam in [0,15]:
        for value in [0,1,3,65535]:
            for mask in [0,65535]:rows.append(dict(entry=0x027ebd58,cam=cam,value=value,mask=mask))
        for count in [0,1,65535]:rows.append(dict(entry=0x027ec438,cam=cam,count=count))
    for label,mode,records,allocate,ap,maximum,count in [
      ('empty',1,[],False,1,16,0),('no-entries',1,[(64,1)],False,1,1,1),
      ('zero-lifetime',1,[(64,0)],False,1,16,1),('infinite-lifetime',1,[(64,65535)],False,1,16,1),
      ('decrement',1,[(64,2)],False,1,16,1),('unassociated-expire',1,[(16,1)],False,1,16,1),
      ('class1-expire',1,[(32,1)],False,1,16,1),('parent-null',1,[(64,1)],False,1,16,1),
      ('parent-frame',1,[(64,1)],True,1,16,1),('child-null',2,[(64,1)],False,1,16,1),
      ('child-frame',2,[(64,1)],True,1,16,1),('other-peer',2,[(64,1)],False,2,16,1),
      ('hole-and-expire',1,[(0,0),(64,1),(32,2)],False,1,16,2),
      ('snapshot-bound',1,[(64,2),(0,0),(32,1),(64,1)],False,1,16,2)]:rows.append(dict(entry=0x027ec280,label=label,mode=mode,records=records,allocate=allocate,ap=ap,maximum=maximum,count=count))
    return rows


def scenario(f,ordinal):
    context=bytearray((ordinal*7+i*13)&255 for i in range(1684));table=bytearray((ordinal*3+i*11)&255 for i in range(16*28));frame=bytearray((ordinal*5+i*17)&255 for i in range(64));out=bytearray((ordinal*19+i*7)&255 for i in range(64));initial={SLOT:p32(CTX),CLOSE:p16(0x4a21),OPEN:p16(0x5b32)};regions=dict(initial);actions=[];allowed=[];returned=None;args=[];entry=f['entry'];stack={0x027ec280:40,0x027ebc50:16,0x027ebebc:24,0x027ebb50:16,0x027ebd58:0,0x027ec438:8,0x027ebdb4:8}[entry]
    def u16(raw,offset,value):raw[offset:offset+2]=p16(value)
    def u32(raw,offset,value):raw[offset:offset+4]=p32(value)
    def r16(raw,offset):return int.from_bytes(raw[offset:offset+2],'little')
    def action(address,values=(),result=0,checks=(),mutations=()):actions.append(dict(address=address,args=list(values),returned=result,checks=list(checks),mutations=list(mutations)))
    mask=0x81234567 if ordinal&1 else 0x01000000
    u32(context,796,TABLE);u16(context,802,16);u16(context,1328,0xa5a5);u16(context,1330,0x5a5a);u16(context,1332,0)
    cam=f.get('cam',1);offset=cam*28;bit=1<<cam
    if entry==0x027ebc50:
        u16(context,848,f['mode']);u16(context,1326,bit if f['power']else 0);u16(table,offset+2,f['aid']);args=[cam,f['state']];allowed.extend([(CTX+1328,CTX+1332),(TABLE+offset,TABLE+offset+2)])
    elif entry==0x027ebb50:
        u16(context,848,f['mode']);u16(context,1332,bit if f['skip']else 0);u16(table,offset+22,f['count']);u16(table,offset+24,123);u16(table,offset+26,0x8123);u16(frame,2,cam);args=[FRAME];allowed.extend([(TABLE+offset+22,TABLE+offset+26)])
    elif entry==0x027ebebc:
        u16(context,1338,f['bitmap']);u16(context,1336,f['connected']);args=[cam];allowed.extend([(CTX+1336,CTX+1340),(TABLE+offset+2,TABLE+offset+4)])
    elif entry==0x027ebd58:
        u16(context,1326,0x1234);u16(context,1330,f['mask']);args=[cam,f['value']];allowed.extend([(CTX+1326,CTX+1328),(CLOSE,CLOSE+2),(OPEN,OPEN+2)])
    elif entry==0x027ebdb4:u16(context,1328,65535);args=[cam];allowed.append((CTX+1328,CTX+1330))
    elif entry==0x027ec438:
        u16(context,1324,f['count']);u16(table,offset,64);args=[cam];allowed.extend([(TABLE+offset,TABLE+offset+2),(CTX+1324,CTX+1326)])
    else:
        u16(context,848,f['mode']);u16(context,972,f['ap']);u16(context,802,f['maximum']);u16(context,1324,f['count'])
        for pos in range(1,16):u16(table,pos*28,0);u16(table,pos*28+24,0)
        for pos,(state,life)in enumerate(f['records'],1):u16(table,pos*28,state);u16(table,pos*28+24,life)
        allowed.extend([(TABLE,TABLE+len(table)),(CTX+1324,CTX+1334),(CTX+844,CTX+846),(OUT,OUT+2)])
    initial.update({CTX:bytes(context),TABLE:bytes(table),FRAME:bytes(frame),OUT:bytes(out)})
    if entry==0x027ebc50:
        action(0x037fb928,[1<<24],mask)
        if f['state']<64:
            u16(context,1328,r16(context,1328)|bit);u16(context,1330,r16(context,1330)|bit)
            if f['mode']==1:
                action(0x027ec0d8,[cam],f['aid'])
                if f['aid']:action(0x027ebf6c,[cam])
        else:
            u16(context,1330,r16(context,1330)&~bit)
            if f['power']:action(0x027ebdb4,[cam])
        u16(table,offset,f['state']);action(0x037fb8f0,[mask],checks=[(TABLE+offset,p16(f['state']))])
    elif entry==0x027ebb50:
        action(0x037fb928,[1<<24],mask)
        if f['mode']==1 and f['count']==0:action(0x027ec118,[cam])
        u16(table,offset+22,f['count']+1);changed=[]
        if f['race']:u16(context,1332,bit);changed=[(CTX+1332,p16(bit))]
        action(0x037fb8f0,[mask],checks=[(TABLE+offset+22,p16(f['count']+1))],mutations=changed)
        if not r16(context,1332)&bit:u16(table,offset+24,0x8123)
    elif entry==0x027ebebc:
        action(0x037fb928,[1<<24],mask);returned=0
        for i in range(1,16):
            if not f['bitmap']&(1<<i):
                u16(context,1338,f['bitmap']|(1<<i));u16(context,1336,f['connected']+1)
                if (f['connected']+1)&65535==1:action(0x027e9eec,checks=[(CTX+1336,p16(1))])
                u16(table,offset+2,i);returned=i;break
        action(0x037fb8f0,[mask])
    elif entry==0x027ebd58:
        value=((0x1234&~bit)|(f['value']<<cam))&65535;u16(context,1326,value);regions[CLOSE if value&~f['mask']else OPEN]=p16(8)
    elif entry==0x027ebdb4:
        action(0x027ebfec,[cam],f['state'])
        if f['state']==64:u16(context,1328,r16(context,1328)&~bit)
    elif entry==0x027ec438:
        action(0x027f0d6c,[cam],checks=[(TABLE+offset,p16(64))]);u16(table,offset,0);u16(context,1324,f['count']-1)
    else:
        seen=0
        for pos in range(1,f['maximum']):
            offset=pos*28;state=r16(table,offset);life=r16(table,offset+24)
            if state:
                if life not in [0,65535]:
                    u16(table,offset+24,life-1)
                    if life==1:
                        retained=False
                        if state>=32:
                            action(0x027ebfec,[pos],state);u16(table,offset,32);action(0x027ebc50,[pos,32],checks=[(TABLE+offset+24,p16(0))],mutations=[(TABLE+offset,p16(32))]);action(0x027f0d6c,[pos])
                            deauth=False
                            if f['mode']==1 and state>32:
                                u16(context,1332,r16(context,1332)|(1<<pos));action(0x027ebd58,[pos,0]);u16(context,1328,r16(context,1328)|(1<<pos));deauth=True
                            elif f['mode']!=1 and pos==f['ap']:deauth=True
                            if deauth:
                                action(0x027f1ec8,[TABLE+offset+4,1,0],OUT if f['allocate']else 0)
                                if f['allocate']:
                                    u16(out,0,1);action(0x027f1088,[OUT],checks=[(OUT,p16(1))]);retained=True
                                else:
                                    if f['mode']!=1:u16(context,844,32);action(0x037f9238,[32],mutations=[(CTX+844,p16(32))]);action(0x027ea048)
                                    action(0x027edbf0,[TABLE+offset+4,1])
                        if not retained:u16(table,offset,0);u16(context,1324,r16(context,1324)-1)
                seen+=1
                if life==1 and state>=32 and f['allocate']and ((f['mode']==1 and state>32)or(f['mode']!=1 and pos==f['ap'])):continue
            if seen>=f['count']:break
    regions.update({CTX:bytes(context),TABLE:bytes(table),FRAME:bytes(frame),OUT:bytes(out)})
    return dict(args=args,initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=stack,returnValue=returned)
