from project import read_json
from wave20261106_arm7_wm_residual_next_second_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
MESSAGE=0x02302000
CB=0x02304000
RESULT=0x02306000
INFO=0x02308000
SCAN=0x0230a000
WM7=0x0230c000
RECV=0x02310000
SEND=0x02312000
WORK=0x027f7884
FRAME={0x027e386c:1264,0x027e3ed0:616,0x027e4be0:552}
LAYOUT=read_json(LANE/'layout-baseline.json')
STATUS_FIELDS={}
for row in LAYOUT.values():STATUS_FIELDS.update(row['fields'].get('WMStatus',{}))


def pack(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def fixtures():
    rows=[]
    def scan(**values):rows.append(dict(dict(entry=0x027e386c,kind='scan',state=2,channels=3,enabled=65535,pointer=SCAN,size=512,misc=0,scanType=2,match=16,preamble=1,station=16,fail='none',code=5,found=0,ssidLength=4,validSSID=False),**values))
    for state in [0,1,65535]:scan(state=state)
    for values in [dict(channels=0),dict(enabled=0),dict(pointer=0),dict(pointer=SCAN+2),dict(size=63),dict(misc=1,scanType=0)]:scan(**values)
    for stage in ['station','params','class1','power','preamble','mask','scan']:scan(fail=stage)
    for typ in [0,1,2,3]:
        for found in [0,1,2]:scan(scanType=typ,found=found,station=16 if typ%2 else 32,match=[0,16,32,33][typ],validSSID=bool(found%2))
    def connect(**values):rows.append(dict(dict(entry=0x027e3ed0,kind='connect',state=2,misc=0,gameLength=16,attribute=1,channel=1,enabled=65535,rate=1,basic=1,capability=32,fail='params',period=100,power=2,code=5),**values))
    for state in [0,3,8,65535]:connect(state=state)
    for values in [dict(misc=1),dict(attribute=0),dict(channel=0),dict(channel=15),dict(enabled=0)]:connect(**values)
    for rate,basic in [(1,0),(1,1),(2,0),(2,2)]:connect(rate=rate,basic=basic,capability=0 if basic==0 else 32)
    for stage in ['nullkey','class1','power']:
        for gameLength in [0,16]:connect(fail=stage,gameLength=gameLength)
    for period in [0,1,100,65535]:connect(fail='beacon',gameLength=0,period=period)
    def mp(**values):rows.append(dict(dict(entry=0x027e4be0,kind='mp',state=8,ignore=0,small=False,mode=2,allowed=0x3fff,clean=1,code=0,mask=0,tick=0x123456789abcdef0),**values))
    for state in [0,2,9,10]:mp(state=state)
    mp(small=True);mp(allowed=0)
    for state in [7,8]:
        for code in [0,5]:
            for mask in [0,0x1e07]:mp(state=state,code=code,mask=mask,mode=0 if state==7 else 2,clean=bool(mask),tick=0 if mask else 0x123456789abcdef0)
    mp(ignore=2,small=True,mode=0)
    return rows


class Plan:
    def __init__(self,f,ordinal):
        self.f=f;self.frame=FRAME[f['entry']];self.stack=SP-self.frame;self.regions={address:bytearray((i*17+ordinal*11+address//256)&255 for i in range(size))for address,size in [(STATUS,2000),(MESSAGE,128),(CB,256),(RESULT,512),(INFO,192),(SCAN,512),(WM7,720),(WORK,5520),(RECV,1024),(SEND,1024)]};self.actions=[];self.initial=None;self.regions[WORK][5452:5456]=pack(WM7,4);self.regions[WORK][5456:5460]=pack(STATUS,4)
    def write(self,address,offset,value,size=2):self.regions[address][offset:offset+size]=pack(value,size)
    def setf(self,name,value):self.write(STATUS,STATUS_FIELDS[name],value,STATUS_FIELDS[name+'.width'])
    def seal(self):self.initial={a:bytes(r)for a,r in self.regions.items()}
    def action(self,address,args=(),result=0,checks=(),mutations=(),high=None):
        row=dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations))
        if high is not None:row['returnedHigh']=high
        self.actions.append(row)
    def getcb(self):self.action(0x038073f0,result=CB)
    def cbfield(self,name,value):
        typ=dict(scan='WMStartScanExCallback',connect='WMStartConnectCallback',mp='WMStartMPCallback')[self.f['kind']];fields=LAYOUT[format(self.f['entry'],'08x')]['fields'][typ];self.write(CB,fields[name],value,fields[name+'.width'])
    def publish(self):self.action(0x038073a4,[CB],checks=[(a,bytes(r))for a,r in self.regions.items()if a!=RESULT])
    def callback(self,api,error,state):self.getcb();self.cbfield('apiid',api);self.cbfield('errcode',error);self.cbfield('state',state)
    def copy(self,source,dest,payload):self.action(0x037fe12c,[source,dest,len(payload)],checks=[(source,bytes(payload))],mutations=[(dest,bytes(payload))])
    def response(self,code,state=0):
        raw=bytearray(self.initial[RESULT]);raw[4:6]=pack(code);raw[6:8]=pack(state);return bytes(raw)
    def wl(self,address,args,stage,state=0):
        code=self.f['code']if self.f['fail']==stage else 0;self.action(address,args,result=RESULT,mutations=[(RESULT,self.response(code,state))]);return code
    def error(self,command,code):self.action(0x027e3d80 if self.f['kind']=='scan'else 0x027e4474,[command,code,1 if self.f['kind']=='scan'else 0])
    def finish(self):return dict(args=[MESSAGE],initial=self.initial,regions={a:bytes(r)for a,r in self.regions.items()if a!=RESULT},actions=self.actions,returnValue=None,frame=self.frame,entry=self.f['entry'],allowedWriteRanges=[(a,a+len(self.regions[a]))for a in [STATUS,CB,SCAN,WM7]])


def scan_plan(p):
    f=p.f;stack=p.stack;buf=stack+112;bssid=stack+24;ssid=stack+78;mask=stack+46;channels=stack+30;p.setf('state',f['state']);p.setf('enableChannel',f['enabled']);p.setf('miscFlags',f['misc']);p.setf('preamble',f['preamble']);p.write(MESSAGE,2,f['channels']);p.write(MESSAGE,4,f['pointer'],4);p.write(MESSAGE,8,f['size']);p.write(MESSAGE,10,91);p.write(MESSAGE,12,0x1235);p.write(MESSAGE,18,f['scanType']);p.write(MESSAGE,20,f['ssidLength']);p.write(MESSAGE,54,f['match']);p.seal()
    if f['state']not in [2,3,5]:p.callback(38,3,4);p.publish();return
    p.setf('pInfoBuf',f['pointer']);p.setf('scan_channel',f['channels']);rawBssid=bytearray(p.initial[MESSAGE][12:18]);rawSsid=p.initial[MESSAGE][22:54];p.copy(MESSAGE+12,bssid,rawBssid);p.copy(MESSAGE+22,ssid,rawSsid);rawBssid[0]&=254;typ=f['scanType']-2 if f['scanType']in [2,3]else f['scanType'];channelBits=(f['channels']<<1)&f['enabled']&65535
    if not channelBits or(f['misc']&1 and typ!=1)or not f['pointer']or f['pointer']&3 or f['size']<64:p.callback(38,6,4);p.publish();return
    p.setf('mode',2);code=p.wl(0x027e2924,[buf],'station',f['station'])
    if code:p.error(0x308,code);return
    if f['station']==16:
        p.action(0x027e03d0,[38,buf],result=0 if f['fail']=='params'else 1)
        if f['fail']=='params':return
        code=p.wl(0x027e28b0,[buf],'class1')
        if code:p.error(0x303,code);return
        p.setf('state',3);code=p.wl(0x027e1dbc,[buf,1,0,1],'power')
        if code:p.error(1,code);return
        p.setf('pwrMgtMode',1)
    required=0 if typ==0 else 1
    if f['preamble']!=required:
        code=p.wl(0x027e2584,[buf,required],'preamble')
        if code:p.error(0x20e,code);return
        p.setf('preamble',required)
    if f['scanType']in [2,3]:
        maskBytes=bytearray(b'\xff'*32);p.action(0x037fe070,[mask,255,32],mutations=[(mask,bytes(maskBytes))])
        if f['match']<=32:maskBytes[:f['match']]=bytes(f['match']);p.action(0x037fe070,[mask,0,f['match']],mutations=[(mask,bytes(maskBytes))])
        code=p.wl(0x027e2510,[buf,mask],'mask');p.actions[-1]['checks']=[(mask,bytes(maskBytes))]
        if code:p.error(0x20d,code);return
    p.setf('state',5);channelBytes=bytes([i for i in range(1,15)if channelBits&(1<<i)]).ljust(16,b'\x00');p.action(0x037fe070,[channels,0,16],mutations=[(channels,bytes(16))]);dividend=f['size']-64;p.action(0x03806e44,[dividend,66],result=dividend//66,high=dividend%66);bufSize=f['size']-(dividend//66)*2+94;response=bytearray(p.response(f['code']if f['fail']=='scan'else 0));response[8:10]=pack(f['found']);descriptors=[]
    for i in range(f['found']):
        d=bytearray((k*29+i*17)&255 for k in range(66+2*i));d[0:2]=pack(len(d)//2);d[2:4]=pack(0x1234+i);d[10:12]=pack(4 if f['validSSID']else 0);d[12:44]=(b'TEST'+bytes(28))if f['validSSID']else bytes(32);descriptors.append(bytes(d))
    response[10:10+sum(map(len,descriptors))]=b''.join(descriptors);p.action(0x027e1e1c,[buf,bufSize,bssid,f['ssidLength'],ssid,typ,channels,91],result=RESULT,checks=[(bssid,bytes(rawBssid)),(ssid,rawSsid),(channels,channelBytes)],mutations=[(RESULT,bytes(response))])
    if f['fail']=='scan':p.error(2,f['code']);return
    p.getcb()
    if f['found']:
        p.action(0x037fdf74,[0,SCAN,f['size']],mutations=[(SCAN,bytes(f['size']))]);p.regions[SCAN][:f['size']]=bytes(f['size']);source=RESULT+10;dest=SCAN
        for i,raw in enumerate(descriptors):
            p.copy(source,dest,raw);offset=dest-SCAN;p.regions[SCAN][offset:offset+len(raw)]=raw
            if f['ssidLength']and not f['validSSID']:
                p.write(SCAN,offset+10,f['ssidLength']);p.copy(ssid,dest+12,rawSsid);p.regions[SCAN][offset+12:offset+44]=rawSsid
            p.write(CB,16+4*i,dest,4);p.action(0x027e383c,[(0x1234+i)&255],result=70+i);p.action(0x027e05d8,[70+i],result=2+i);p.write(CB,80+2*i,2+i);p.action(0x027e3850,[70+i]);source+=len(raw);dest=(dest+len(raw)+3)&~3
    p.cbfield('apiid',38);p.cbfield('errcode',0);p.cbfield('state',5 if f['found']else 4);p.cbfield('bssDescCount',f['found']);p.cbfield('channelList',channelBits>>1);p.publish()


def connect_plan(p):
    f=p.f;buf=p.stack+80;p.setf('state',f['state']);p.setf('miscFlags',f['misc']);p.setf('enableChannel',f['enabled']);p.setf('rate',f['rate']);p.write(MESSAGE,4,INFO,4);p.write(MESSAGE,32,f['power'],4);p.write(INFO,44,f['capability']);p.write(INFO,46,f['basic']);p.write(INFO,50,f['period']);p.write(INFO,54,f['channel']);p.write(INFO,60,f['gameLength']);p.write(INFO,75,f['attribute'],1);p.seal()
    if f['state']!=2 or f['misc']&1:p.callback(12,3,6);p.publish();return
    payload=p.initial[INFO];p.copy(INFO,WM7+16,payload);p.regions[WM7][16:208]=payload
    if f['gameLength']>=16 and not f['attribute']&1:p.callback(12,11,6);p.publish();return
    if not((1<<f['channel'])&f['enabled'])or not(((1<<f['channel'])>>1)&0x1fff):p.callback(12,6,6);p.publish();return
    p.callback(12,0,6);p.publish();rate=(1 if f['basic']&1 else 2)if f['rate']==1 else(2 if f['basic']&2 else 1);p.setf('rate',rate);p.setf('preamble',1 if f['capability']&32 else 0);p.setf('mode',3 if f['gameLength']==0 else 2);p.action(0x027e03d0,[12,buf],result=0 if f['fail']=='params'else 1)
    if f['fail']=='params':return
    code=p.wl(0x027e2700,[buf,0],'nullkey')
    if code:p.error(0x216,code);return
    if f['gameLength']<16:
        period=f['period']
        if period:p.action(0x03806c38,[10000,period],result=10000//period,high=10000%period)
        threshold=min((10000//period+1)&65535,255)if period else 1;code=p.wl(0x027e24b4,[buf,threshold],'beacon')
        if code:p.error(0x20b,code);return
    code=p.wl(0x027e28b0,[buf],'class1')
    if code:p.error(0x303,code);return
    p.setf('state',3);code=p.wl(0x027e1dbc,[buf,1 if f['power']else 0,0,1],'power')
    if code:p.error(1,code);return
    raise ValueError('This bounded connect-prefix model does not execute join/authenticate/associate success')


def mp_plan(p):
    f=p.f;stack=p.stack
    for name,value in dict(state=f['state'],mp_ignoreSizePrecheckMode=f['ignore'],mp_maxSendSize=96,mp_maxRecvSize=64,aid=0,mode=f['mode'],allowedChannel=f['allowed'],mp_flag=f['clean'],mp_maxFreq=3,mp_minFreq=1,mp_freq=2,mp_count=5,mp_defaultRetryCount=4,mp_minPollBmpMode=1,mp_singlePacketMode=2,mp_ignoreFatalErrorMode=3).items():p.setf(name,value)
    p.write(STATUS,248,2);p.write(WM7,70,1);size=0 if f['small']else 1024
    for offset,value in [(4,RECV),(8,size),(12,SEND),(16,size),(48,f['mask'])]:p.write(MESSAGE,offset,value,4)
    for offset,value,width in [(52,20,2),(54,0,2),(56,5,2),(58,8,2),(60,2,1),(61,3,1),(62,4,1)]:p.write(MESSAGE,offset,value,width)
    p.seal()
    if(not f['ignore']and f['small'])or(f['mode']==2 and not f['allowed']&1):p.callback(14,6,10);p.publish();return
    if f['clean']:p.setf('mp_flag',0);p.action(0x027e7828,[65535])
    p.action(0x027e637c);p.action(0x037fdd00,result=0x80);p.action(0x027e8428,[MESSAGE+20,0],result=6)
    if f['state']not in [9,10]:
        p.action(0x037fdd00,result=0x40);maxFreq=5 if f['mask']else 3;minFreq=5 if f['mask']else 1;freq=5 if f['mask']else 2
        for name,value in dict(mp_current_maxFreq=maxFreq,mp_current_minFreq=minFreq,mp_current_freq=freq,mp_count=min(5,maxFreq),mp_current_defaultRetryCount=8 if f['mask']else 4,mp_current_minPollBmpMode=2 if f['mask']else 1,mp_current_singlePacketMode=3 if f['mask']else 2,mp_current_ignoreFatalErrorMode=4 if f['mask']else 3).items():p.setf(name,value)
        p.action(0x037fdd14,[0x40],checks=[(STATUS,bytes(p.regions[STATUS]))])
    if f['state']not in [7,8]:p.action(0x037fdd14,[0x80]);p.callback(14,3,10);p.publish();return
    for name,value in dict(mp_waitAckFlag=0,mp_vsyncOrderedFlag=0,mp_vsyncFlag=1,mp_newFrameFlag=0,mp_pingFlag=0,mp_pingCounter=60,sendQueueInUse=0,mp_setDataFlag=0,mp_sentDataFlag=0,mp_bufferEmptyFlag=0,mp_isPolledFlag=0,mp_resumeFlag=0,mp_recvBufSize=size,mp_recvBufSel=0,mp_sendBuf=SEND,mp_sendBufSize=size,mp_count=0,mp_limitCount=0,mp_prevPollBitmap=0,mp_prevWmHeader=0,minRssi=65535,rssiCounter=1).items():p.setf(name,value)
    at=STATUS_FIELDS['mp_recvBuf'];p.regions[STATUS][at:at+8]=pack(RECV,4)+pack(RECV+size,4);p.action(0x037fd21c,result=f['tick']&0xffffffff,high=f['tick']>>32,checks=[(STATUS,bytes(p.regions[STATUS]))]);at=STATUS_FIELDS['mp_lastRecvTick'];p.regions[STATUS][at:at+128]=pack(f['tick']|1,8)*16;p.action(0x027e06a0);p.setf('valarm_queuedFlag',0);p.action(0x027e5bac,checks=[(STATUS,bytes(p.regions[STATUS]))]);p.setf('state',10 if f['state']==8 else 9);p.callback(14,0,10);p.publish();p.setf('mp_flag',1);p.action(0x037fdd14,[0x80],checks=[(STATUS,bytes(p.regions[STATUS]))]);p.action(0x027e2700,[stack+4,1],result=RESULT,mutations=[(RESULT,p.response(f['code']))])
    if f['code']:p.getcb();p.cbfield('apiid',14);p.cbfield('errcode',1);p.write(CB,4,0x216);p.write(CB,6,f['code']);p.publish()


def scenario(f,ordinal):
    p=Plan(f,ordinal);dict(scan=scan_plan,connect=connect_plan,mp=mp_plan)[f['kind']](p);return p.finish()
