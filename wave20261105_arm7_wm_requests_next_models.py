from project import read_json
from wave20261105_arm7_wm_requests_next_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
MESSAGE=0x02302000
CB=0x02304000
RESULT=0x02306000
BUFFER=0x02308000
COMMAND=0x0230a000
VALUE=0x0230a010
WORK=0x027f7884
FRAME={0x027e609c:16,0x027e614c:16,0x027e7cc8:648,0x027e7d58:544,0x027e8110:536,0x027e8320:528,0x027e83cc:48,0x027e87d8:584}
LAYOUT=read_json(LANE/'layout-baseline.json')
STATUS_FIELDS={}
for row in LAYOUT.values():STATUS_FIELDS.update(row['fields'].get('WMStatus',{}))


def pack(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def signed16(value):return((value+32768)&65535)-32768


def fixtures():
    rows=[]
    for flag in [0,1,2,65535]:
        for allocated in [False,True]:
            for sent in [0,1]:
                for wm7 in [False,True]:rows.append(dict(entry=0x027e609c,kind='enqueue',flag=flag,allocated=allocated,sent=sent,wm7=wm7))
    for i in range(72):rows.append(dict(entry=0x027e614c,kind='valarm',state=[0,9,10][i%3],rssi=[0,1,2][i//3%3],minRssi=[65535,0x180][i//9%2],child=[0,3][i//18%2],count=[-32768,-1,0,1,255,32767][i//3%6],limit=[0,1][i%2],freq=[0,1,10,32768][i//18%4],maxFreq=[0,2,65535][i//6%3],minMode=i%2,ping=[0,1,2][i//3%3],use=[0,1,2][i//6%3],link=[0,3,32768,65535][i%4]))
    for count,freq in [(255,10),(250,10),(-1,10),(1,65535)]:rows.append(dict(entry=0x027e614c,kind='valarm',state=9,rssi=2,minRssi=65535,child=3,count=count,limit=0,freq=freq,maxFreq=2,minMode=1,ping=1,use=0,link=3))
    for code in [0,7,12,5,65535]:
        for final in [0,7,5]:rows.append(dict(entry=0x027e7d58,kind='deauth',codes=[code,final]))
    for state in [0,1,2,9,65535]:
        for code in [0,5,65535]:rows.append(dict(entry=0x027e8320,kind='poweroff',state=state,code=code))
    for i in range(20):rows.append(dict(entry=0x027e7cc8,kind='entry',value=[0,1,65535,0xabcd8000][i%4],length=[0,8,112,65535][i//4%4],code=[0,5,65535][i%3]))
    for i in range(20):rows.append(dict(entry=0x027e83cc,kind='parameter',mask=[0,1,0xdeadbeef,0xffffffff][i%4],code=[0,1,6,65535,0xffffffff][i//4%5]))
    for fail in [-1,0,1,2,3,4,5,6]:
        for code in [1,7,65535]:rows.append(dict(entry=0x027e8110,kind='idle',fail=fail,code=code,channel=[0,0x3ffe,0xffff][code%3]))
    for state in [0,2,11,65535]:
        for power in [0,1,2,0xffffffff]:
            for stage in [-1,0,1]:rows.append(dict(entry=0x027e87d8,kind='power',state=state,power=power,fail=stage,code=7 if power%2 else 5,rate=2 if power%2 else 1))
    return rows


def scenario(f,ordinal):
    entry=f['entry'];tag=format(entry,'08x');frame=FRAME[entry];stack=SP-frame;s=bytearray((i*17+ordinal*11)&255 for i in range(2000));cb=bytearray((i*7+ordinal)&255 for i in range(80));work=bytearray((i*23+ordinal)&255 for i in range(5520));message=bytearray((i*19+ordinal)&255 for i in range(128));buffer=bytearray((i*13+ordinal)&255 for i in range(128));mmio=bytearray((i*3+ordinal)&255 for i in range(4096));initial={};actions=[];args=[MESSAGE];expectedReturn=None;outputs=bytearray(b'\x5a\xa5');value=bytearray(b'\x3c\xc3')
    def setf(name,val):at=STATUS_FIELDS[name];width=STATUS_FIELDS[name+'.width'];s[at:at+width]=pack(val,width)
    def getf(name,signed=False):at=STATUS_FIELDS[name];width=STATUS_FIELDS[name+'.width'];return int.from_bytes(s[at:at+width],'little',signed=signed)
    def action(address,args=(),result=0,checks=(),mutations=()):actions.append(dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations)))
    def getcb():action(0x038073f0,result=CB)
    def fields(**values):
        for name,val in values.items():offset=dict(apiid=0,errcode=2,wlCmdID=4,wlResult=6,state=4,reason=6)[name];cb[offset:offset+2]=pack(val)
    def publish():action(0x038073a4,[CB],checks=[(CB,bytes(cb))])
    def response(code,extra=b''):
        r=bytearray((i*5+ordinal)&255 for i in range(64));r[4:6]=pack(code);r[6:6+len(extra)]=extra;return bytes(r)
    def wl(address,arguments,code=0,extra=b''):action(address,arguments,result=RESULT,mutations=[(RESULT,response(code,extra))])
    setf('state',f.get('state',2));setf('valarm_queuedFlag',f.get('flag',0));work[5456:5460]=pack(STATUS,4);work[5452:5456]=pack(BUFFER if f.get('wm7',True) else 0,4)
    if f['kind']=='valarm':
        for name,val in dict(rssiCounter=f['rssi'],minRssi=f['minRssi'],linkLevel=2,child_bitmap=f['child'],mp_count=f['count'],mp_limitCount=f['limit'],mp_current_freq=f['freq'],mp_current_maxFreq=f['maxFreq'],mp_current_minPollBmpMode=f['minMode'],mp_pingCounter=f['ping'],mp_pingFlag=0,sendQueueInUse=f['use'],mp_vsyncFlag=1,mp_newFrameFlag=0).items():setf(name,val)
    if f['kind']=='entry':message[4:8]=pack(f['value'],4);s[236:238]=pack(f['length'])
    if f['kind']=='parameter':message[4:8]=pack(f['mask'],4)
    if f['kind']=='power':message[4:8]=pack(f['power'],4);setf('rate',f['rate'])
    initial.update({STATUS:bytes(s),CB:bytes(cb),WORK:bytes(work),MESSAGE:bytes(message),BUFFER:bytes(buffer),COMMAND:bytes(outputs),VALUE:bytes(value),RESULT:response(0),0x04808000:bytes(mmio)})
    kind=f['kind']
    if kind=='enqueue':
        args=[];action(0x037fdd00,result=0x80)
        if f['flag']==1:action(0x037fdd14,[0x80],result=0x80)
        else:
            setf('valarm_queuedFlag',1);action(0x037fdd14,[0x80],result=0x80,checks=[(STATUS,bytes(s))]);action(0x027e0700,result=BUFFER if f['allocated'] else 0)
            if f['allocated']:buffer[0:4]=pack(28,4);action(0x037fc6d4,[WORK+136,BUFFER,0],result=f['sent'],checks=[(BUFFER,bytes(buffer))])
            if not f['allocated'] or not f['sent']:
                setf('valarm_queuedFlag',0)
                if f['wm7']:getcb();fields(apiid=128,errcode=8,state=22,reason=28);publish()
    elif kind=='valarm':
        setf('valarm_queuedFlag',0);setf('mp_newFrameFlag',1);rssi=(f['rssi']-1)&65535;setf('rssiCounter',rssi)
        if rssi==0:
            raw=4 if f['minRssi']==65535 else f['minRssi'];setf('minRssi',raw);action(0x027e0520,[raw&255],checks=[(STATUS,bytes(s))]);action(0x027e059c,result=f['link']);setf('linkLevel',f['link']);setf('minRssi',65535);setf('rssiCounter',1)
        if f['state']==9:
            action(0x037fdd00,result=0x80)
            if not f['child']:setf('mp_count',0);action(0x037fdd14,[0x80],result=0x80,checks=[(STATUS,bytes(s))])
            else:
                sleeping=f['count']<=0 or f['limit']<=0;count=signed16(max(f['count'],0)+signed16(f['freq']));count=min(count,256);limit=signed16(f['maxFreq']);setf('mp_count',count);setf('mp_limitCount',limit);action(0x037fdd14,[0x80],result=0x80,checks=[(STATUS,bytes(s))])
                if sleeping and count>0 and limit>0:action(0x027e692c,[65535])
                if f['minMode']==1:
                    ping=(f['ping']-1)&65535;setf('mp_pingCounter',ping)
                    if ping==0:setf('mp_pingFlag',1);setf('mp_pingCounter',60)
        elif f['state']==10:
            action(0x037fdd00,result=0x80)
            if f['use']!=1:setf('mp_vsyncFlag',0)
            action(0x037fdd14,[0x80],result=0x80,checks=[(STATUS,bytes(s))])
            if f['use']!=1:action(0x027e6434)
    elif kind=='deauth':
        mac=bytes(message[4:10]);action(0x037fe12c,[MESSAGE+4,stack,6],mutations=[(stack,mac)]);last=0
        for code in f['codes']:
            wl(0x027e1fcc,[stack+8,stack,19],code);last=code
            if code not in [7,12]:break
        getcb();fields(apiid=34,errcode=0 if last==0 else 1)
        if last:fields(wlCmdID=5,wlResult=last)
        publish()
    elif kind=='poweroff':
        if f['state']!=2:getcb();fields(apiid=6,errcode=3);publish()
        else:
            wl(0x027e2880,[stack],f['code'])
            if not f['code']:setf('state',1)
            getcb();fields(apiid=6,errcode=1 if f['code'] else 0)
            if f['code']:fields(wlCmdID=0x301,wlResult=f['code'])
            publish()
    elif kind=='entry':
        s[246:248]=pack(f['value']);game=bytes((i*29+ordinal)&255 for i in range(128));action(0x027e030c,[stack,STATUS+232],checks=[(STATUS,bytes(s))],mutations=[(stack,game)]);wl(0x027e27b8,[stack+128,(16+f['length'])&65535,stack],f['code']);getcb();fields(apiid=33,errcode=1 if f['code'] else 0)
        if f['code']:fields(wlCmdID=0x245,wlResult=f['code'])
        publish()
    elif kind=='parameter':
        old=bytes((i*31+ordinal)&255 for i in range(28));action(0x027e8428,[MESSAGE+4,stack],result=f['code'],mutations=[(stack,old)]);getcb();fields(apiid=35,errcode=f['code']);cb[4:8]=pack(f['mask'],4);action(0x037fe12c,[stack,CB+8,28],mutations=[(CB+8,old)]);cb[8:36]=old;publish()
    elif kind=='idle':
        args=[COMMAND,VALUE];addresses=[0x027e28c8,0x027e2898,0x027e2854,0x027e25e0,0x027e28f4,0x027e283c,0x027e26a4];commands=[0x304,0x302,0x283,0,0x306,0x281,0x215];expectedReturn=1
        version=bytes((0x21+i+ordinal)&255 for i in range(16));mac=bytes((0x91+i+ordinal)&255 for i in range(6))
        for stage,address in enumerate(addresses):
            arguments=[stack];code=f['code'] if stage==f['fail'] else 0;extra=pack(f['channel']) if stage==2 else version if stage==4 else mac if stage==5 else b''
            if stage==3:arguments += [65535,40,5]
            if stage==6:arguments += [1]
            wl(address,arguments,code,extra)
            if stage==3:setf('mp_lifeTimeTick',2094625);setf('rate',2);setf('preamble',1)
            if code and stage!=3:outputs[:]=pack(commands[stage]);value[:]=pack(code);expectedReturn=0;break
            if stage==1:
                for offset,val in [(0x124,200),(0x128,2000),(0x150,0x202)]:mmio[offset:offset+2]=pack(val)
            if stage==2:setf('enableChannel',f['channel']);allowed=((f['channel']>>1)^0x1555)&65535;action(0x03807444,[f['channel']>>1],result=allowed);setf('allowedChannel',allowed)
            if stage==4:
                action(0x037fdf9c,[RESULT+6,STATUS+32,8],mutations=[(STATUS+32,version[:8])]);s[32:40]=version[:8];s[40:42]=version[8:10];s[44:48]=version[10:14];s[42:44]=version[14:16]
            if stage==5:action(0x037fe12c,[RESULT+6,STATUS+224,6],mutations=[(STATUS+224,mac)]);s[224:230]=mac
    elif kind=='power':
        getcb();fields(apiid=40)
        if f['state']!=11:fields(errcode=3);publish()
        else:
            code=f['code'] if f['fail']==0 else 0;wl(0x027e1dbc,[stack+48,1 if f['power']==1 else 0,0,1],code)
            if code:fields(errcode=1,wlCmdID=1,wlResult=code);publish()
            else:
                parent=bytes(s[394:400]);mac=bytes(s[224:230]);action(0x037fe12c,[STATUS+394,STATUS+162,6],mutations=[(STATUS+162,parent)]);s[162:168]=parent;setf('dcf_sendData',stack+48);setf('dcf_sendSize',0);setf('dcf_sendFlag',1);action(0x037fdf74,[0,stack,48],mutations=[(stack,bytes(48))]);tx=bytearray(48);tx[14]=0x14 if f['rate']==2 else 0xa;action(0x037fe12c,[STATUS+394,stack+24,6],mutations=[(stack+24,parent)]);tx[24:30]=parent;action(0x037fe12c,[STATUS+224,stack+30,6],mutations=[(stack+30,mac)]);tx[30:36]=mac;tx[44:48]=pack(stack+48,4);code=f['code'] if f['fail']==1 else 0;action(0x027e2200,[stack+48,stack],result=RESULT,checks=[(stack,bytes(tx)),(STATUS,bytes(s))],mutations=[(RESULT,response(code))]);fields(errcode=1 if code else 0)
                if code:fields(wlCmdID=0x100,wlResult=code)
                publish()
    else:raise ValueError('Unmodeled request fixture')
    regions={STATUS:bytes(s),WORK:bytes(work),CB:bytes(cb),MESSAGE:bytes(message),BUFFER:bytes(buffer),COMMAND:bytes(outputs),VALUE:bytes(value),0x04808000:bytes(mmio)}
    return dict(args=args,initial=initial,regions=regions,actions=actions,returnValue=expectedReturn,frame=frame,entry=entry,allowedWriteRanges=[(STATUS,STATUS+2000),(CB,CB+80),(BUFFER,BUFFER+128),(COMMAND,COMMAND+2),(VALUE,VALUE+2),(0x04808000,0x04809000)])
