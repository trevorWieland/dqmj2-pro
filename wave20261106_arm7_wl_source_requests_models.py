import struct
SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
REQ=0x02714000
CFM=0x02716000
SLOT=0x0380fff4


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


def fixtures():
    join=dict(entry=0x027ec938,mode=2,sta=0x40,bssid=2,ssid=1,beacon=10,dtim=1,channel=1,enabled=1,basic=1,support=1,timeout=10,flash=0,capa=0)
    rows=[join]
    for field,values in [('mode',[0,1,3,65535]),('sta',[0,31,32,65535]),('bssid',[3]),('ssid',[0,32,33]),('beacon',[9,1000,1001]),('dtim',[0,255,256]),('channel',[0,15,16,65535]),('enabled',[0]),('basic',[0,4095,4096]),('support',[0,4095,4096]),('timeout',[0,2000,2001]),('flash',[1]),('capa',[0x20,65535])]:
        rows.extend([{**join,field:value}for value in values])
    for mode in [0,1,2,3,4,65535]:
        for length in [0,1508,1509]:
            for rate in [0xab00,0xab05]:rows.append(dict(entry=0x027ef5f8,mode=mode,length=length,appRate=rate,cam=3,sta=0x40,returnedRate=0x8123,wep=1,power=3,notClass3=1))
    base=next(dict(row)for row in rows if row['entry']==0x027ef5f8 and row['mode']==1 and row['length']==1508 and row['appRate']==0xab00)
    for cam,sta,power,mask in [(255,0x40,0,0),(3,0x30,0,0),(0,0x40,0,0),(0,0x40,3,3),(0,0x40,3,1)]:rows.append({**base,'cam':cam,'sta':sta,'power':power,'notClass3':mask})
    rows.append({**base,'wep':0});return rows


def scenario(f,ordinal):
    context=bytearray((ordinal*7+i*13)&255 for i in range(1684));request=bytearray((ordinal*3+i*11)&255 for i in range(256));confirm=bytearray((ordinal*5+i*19)&255 for i in range(64));initial={SLOT:p32(CTX)};regions={SLOT:p32(CTX)};actions=[];allowed=[]
    def u16(raw,offset,value):raw[offset:offset+2]=p16(value)
    def u32(raw,offset,value):raw[offset:offset+4]=p32(value)
    def action(at,args=(),result=0,checks=(),mutations=()):actions.append(dict(address=at,args=list(args),returned=result,checks=list(checks),mutations=list(mutations)))
    u16(context,814,f['mode'])
    if f['entry']==0x027ec938:
        frame=16;u16(context,844,f['sta']);u16(request,16,f['timeout']);u16(request,24,f['bssid']);u16(request,30,f['ssid']);u16(request,64,f['capa']);u16(request,66,f['basic']);u16(request,68,f['support']);u16(request,70,f['beacon']);u16(request,72,f['dtim']);u16(request,74,f['channel']);initial.update({CTX:bytes(context),REQ:bytes(request),CFM:bytes(confirm)});u16(confirm,2,5);allowed.extend([(CFM+2,CFM+4),(CTX+1028,CTX+1030),(CTX+1052,CTX+1060)])
        returned=0x80
        if f['mode']not in [2,3]:returned=11
        elif f['sta']<32:returned=1
        else:
            u16(context,844,32);action(0x037f9238,[32],mutations=[(CTX+844,p16(32))])
            if f['bssid']&1 or f['ssid']==0 or f['ssid']>32 or f['beacon']<10 or f['beacon']>1000 or f['dtim']>255 or f['channel']&0xfff0:returned=5
            else:
                action(0x027ea4b0,[f['channel']],f['enabled'])
                if not f['enabled']or f['basic']&~4095 or f['support']&~4095 or f['basic']==0 or (f['basic']|f['support'])==0 or f['timeout']>2000:returned=5
                else:
                    action(0x027f4d38,[0],f['flash'])
                    if f['flash']:returned=14
                    else:
                        action(0x027e929c,[int(bool(f['capa']&32))]);action(0x027e9578,[REQ+24]);action(0x027e95dc,[f['ssid'],REQ+32]);action(0x027e96ec,[f['beacon']]);action(0x027e990c,[f['channel'],0]);action(0x027e9b98,[REQ+66]);u32(context,1052,REQ);u32(context,1056,CFM);u16(context,1028,32);action(0x037f8598,[2,1],checks=[(CTX+1028,p16(32)),(CTX+1052,p32(REQ)),(CTX+1056,p32(CFM))])
    else:
        frame=24;u16(context,820,f['wep']);u16(context,972,3);u32(context,1004,0xa5b61234);u16(context,974,0x4108);context[936:942]=bytes.fromhex('0a1122334455');u16(context,1326,f['power']);u16(context,1330,f['notClass3']);u16(request,22,f['length']);u16(request,30,f['appRate']);request[40:46]=bytes.fromhex('0203456789ab');request[46:52]=bytes.fromhex('06446688aacc');initial.update({CTX:bytes(context),REQ:bytes(request),CFM:bytes(confirm)});allowed.append((REQ+16,REQ+64));returned=0x81;cam=3
        if f['length']>1508:returned=5
        else:
            if f['mode']==1:
                cam=f['cam'];action(0x027eb90c,[REQ+40],cam)
                if cam==255:returned=10
                else:
                    action(0x027ebfec,[cam],f['sta'])
                    if f['sta']!=0x40:returned=10
            if returned==0x81:
                u16(request,18,cam);u16(request,20,0x1234)
                if f['appRate']&255:u16(request,32,f['appRate']);u16(request,30,0)
                else:action(0x027ec0ac,[cam],f['returnedRate']);u16(request,32,f['returnedRate'])
                u16(request,36,0x0148 if f['length']==0 else 0x4108);u16(request,34,28 if f['length']==0 else 28+f['length']+(8 if f['wep']else 0))
                def copy(destination,source,raw):request[destination-REQ:destination-REQ+6]=raw;action(0x027ea0ec,[destination,source],mutations=[(destination,raw)])
                if f['mode']==1:
                    copy(REQ+52,REQ+46,bytes(request[46:52]));copy(REQ+46,CTX+936,bytes(context[936:942]))
                    if cam==0:
                        action(0x027ebaf4,[CTX+512,REQ])
                        if not f['power']&~f['notClass3']:action(0x027eff00,[2])
                    else:action(0x027ebb50,[REQ+16]);action(0x037f8988,[CTX+512,CTX+404,REQ]);action(0x027eff00,[0])
                elif f['mode']in [2,3]:
                    copy(REQ+52,REQ+40,bytes(request[40:46]));copy(REQ+40,CTX+936,bytes(context[936:942]));action(0x027ebb50,[REQ+16]);action(0x037f8988,[CTX+512,CTX+404,REQ]);action(0x027eff00,[0])
    regions.update({CTX:bytes(context),REQ:bytes(request),CFM:bytes(confirm)})
    return dict(args=[REQ,CFM],initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=frame,returnValue=returned)
