from project import read_json
from wave20261106_arm7_wm_residual_next_third_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
BUFFER=0x02302000
CB=0x02304000
RESULT=0x02306000
WORK=0x027f7884
SYSTEM=0x027ffc00
VTSF=0x0380fff0
VIDEO=0x04000000
WIFI=0x04808000
ALARM=0x0380b4bc
FRAME={0x027e03d0:16,0x027e0520:0,0x027e5c5c:16,0x027e5dc0:8,0x027e5e80:16,0x027e5f98:8}
LAYOUT=read_json(LANE/'layout-baseline.json')
FIELDS={}
for row in LAYOUT.values():FIELDS.update(row['fields'].get('WMStatus',{}))
T1=1000000*355*6//33513982
T2=1000000*2*355*6//33513982
T5=1000000*5*355*6//33513982
TF=1000000*263*355*6//33513982


def pack(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def fixtures():
    rows=[]
    for api in [12,38]:
        for wep in [0,1,2]:
            for mode in [1,2]:
                for code in [0,5]:rows.append(dict(entry=0x027e03d0,kind='params',api=api,wep=wep,mode=mode,code=code))
    for index in [0,1,30,31]:
        for rssi,pool in [(0,0),(1,1),(127,0x8000),(255,65535)]:rows.append(dict(entry=0x027e0520,kind='rssi',index=index,rssi=rssi,pool=pool))
    for tsf,bak,remain in [(1,1,0),(1,1,T2),(1,1,T2+1),(0,1,0),(1,0,0),(65535,0,0)]:
        for rollover in [False,True]:rows.append(dict(entry=0x027e5c5c,kind='child1',tsf=tsf,bak=bak,remain=remain,vcount=208,rollover=rollover,child=0x8000))
    for count in [207,208,209,210]:
        for remain in [0,T2-1,T2,T2+T1,T2+T1*7,0xffffffff]:rows.append(dict(entry=0x027e5dc0,kind='child2',vcount=count,remain=remain,child=65535))
    for flag in [0,2]:rows.append(dict(entry=0x027e5e80,kind='childmp',flag=flag,lifetime=0,last=0,now=0,allocated=False,sent=0,child=210))
    for lifetime,last,now in [(0,100,101),(1,0,101),(1,100,100),(1,100,102),(2,0xfffffffffffffffe,0),(0x100000000,1,0x100000001),(7,100,1)]:
        for allocated,sent in [(False,0),(True,0),(True,1)]:rows.append(dict(entry=0x027e5e80,kind='childmp',flag=1,lifetime=lifetime,last=last,now=now,allocated=allocated,sent=sent,child=210))
    for counter in [0,59,60,65535]:
        for count in [202,203,209,210]:
            for rollover in [False,True]:rows.append(dict(entry=0x027e5f98,kind='parent',counter=counter,vcount=count,rollover=rollover,parent=32768))
    return rows


class Plan:
    def __init__(self,f,ordinal):
        self.f=f;self.frame=FRAME[f['entry']];self.args=[];self.returnValue=None;self.actions=[];self.reads=[];self.regions={a:bytearray((i*13+ordinal*19+a//256)&255 for i in range(size))for a,size in [(STATUS,2000),(BUFFER,256),(CB,80),(RESULT,32),(WORK,5520),(SYSTEM,1024),(VTSF,2),(VIDEO,4096),(WIFI,4096)]};self.write(WORK,5456,STATUS,4)
    def write(self,address,offset,value,size=2):self.regions[address][offset:offset+size]=pack(value,size)
    def setf(self,name,value):self.write(STATUS,FIELDS[name],value,FIELDS[name+'.width'])
    def action(self,address,args=(),result=0,checks=(),mutations=(),high=None):
        row=dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations))
        if high is not None:row['returnedHigh']=high
        self.actions.append(row)
    def seal(self):self.initial={a:bytes(r)for a,r in self.regions.items()}
    def alarm(self,count,handler,arg):self.action(0x037fd898,[ALARM,(count-65536 if count&32768 else count)&0xffffffff,263,handler,arg],checks=[(STATUS,bytes(self.regions[STATUS]))])
    def publish(self):self.action(0x038073a4,[CB],checks=[(a,bytes(r))for a,r in self.regions.items()if a!=RESULT])
    def read_clock(self):
        rollover=self.f['rollover'];low0=65534 if rollover else 0x1234;low1=1 if rollover else low0;high0=0x12 if rollover else 2;high1=0x13 if rollover else high0;sequence=[(0x048080f8,low0),(0x048080fa,high0),(0x048080f8,low1)]
        if rollover:sequence.append((0x048080fa,high1))
        self.reads=[dict(address=a,size=2,value=v)for a,v in sequence];self.write(WIFI,248,low1);self.write(WIFI,250,high1);return(high1<<16)|low1
    def finish(self):return dict(args=self.args,initial=self.initial,regions={a:bytes(r)for a,r in self.regions.items()if a!=RESULT},actions=self.actions,reads=self.reads,returnValue=self.returnValue,frame=self.frame,entry=self.f['entry'],allowedWriteRanges=[(a,a+len(self.regions[a]))for a in [STATUS,BUFFER,CB,WORK,SYSTEM,VTSF,VIDEO]])


def params(p):
    f=p.f;p.args=[f['api'],BUFFER]
    for name,value in dict(enableChannel=0x3ffe,rate=2,mode=f['mode'],wep_flag=f['wep'],wepMode=3,wepKeyId=2,preamble=1).items():p.setf(name,value)
    p.seal();fields=LAYOUT['027e03d0']['fields']['WlParamSetAllReq'];buffer=p.regions[BUFFER]
    def field(name,value):p.write(BUFFER,fields[name],value,fields[name+'.width'])
    mac=p.initial[STATUS][224:230];p.action(0x037fe12c,[STATUS+224,BUFFER+fields['staMacAdrs'],6],checks=[(STATUS+224,mac)],mutations=[(BUFFER+fields['staMacAdrs'],mac)]);buffer[fields['staMacAdrs']:fields['staMacAdrs']+6]=mac
    for name,value in dict(retryLimit=7,enableChannel=0x3ffe,rate=2,mode=f['mode'],wepMode=3 if f['wep']else 0,wepKeyId=2 if f['wep']else 0).items():field(name,value)
    at=fields['wepKey'];key=p.initial[STATUS][412:492]if f['wep']else bytes(80)
    if f['wep']:p.action(0x037fe12c,[STATUS+412,BUFFER+at,80],mutations=[(BUFFER+at,key)])
    else:p.action(0x037fdf74,[0,BUFFER+at,80],mutations=[(BUFFER+at,key)])
    buffer[at:at+80]=key
    for name,value in dict(authAlgo=1 if f['wep']else 0,beaconType=1,probeRes=1,beaconLostTh=0 if f['mode']==1 else 16,activeZoneTime=10).items():field(name,value)
    at=fields['ssidMask'];raw=bytes(32)if f['api']==38 else bytes(8)+b'\xff'*24
    if f['api']==38:p.action(0x037fdf74,[0,BUFFER+at,32],mutations=[(BUFFER+at,raw)])
    else:p.action(0x037fdf74,[0,BUFFER+at,8],mutations=[(BUFFER+at,bytes(8))]);p.action(0x037fdf74,[65535,BUFFER+at+8,24],mutations=[(BUFFER+at+8,b'\xff'*24)])
    buffer[at:at+32]=raw;field('preambleType',1);response=bytearray(p.initial[RESULT]);response[4:6]=pack(f['code']);p.action(0x027e2404,[BUFFER],result=RESULT,checks=[(BUFFER,bytes(buffer))],mutations=[(RESULT,bytes(response))]);p.returnValue=0 if f['code']else 1
    if f['code']:
        p.action(0x038073f0,result=CB)
        for offset,value in [(0,f['api']),(2,1),(4,0x200),(6,f['code'])]:p.write(CB,offset,value)
        p.publish()


def rssi(p):
    f=p.f;p.args=[f['rssi']];p.write(WORK,5492,f['index'],4);p.write(SYSTEM,920,f['pool']);p.seal();p.write(WORK,5460+f['index'],f['rssi'],1);p.write(WORK,5492,(f['index']+1)%32,4);value=(f['pool']<<1)^f['rssi'];p.write(SYSTEM,920,value^(value>>16))


def child1(p):
    f=p.f;p.args=[2]
    for name,value in dict(v_tsf_bak=f['bak'],v_remain=f['remain'],VSyncFlag=0,mp_childVCount=f['child']).items():p.setf(name,value)
    p.write(VTSF,0,f['tsf']);p.write(VIDEO,6,f['vcount']);p.seal();value=f['tsf'];remain=f['remain'];p.setf('v_tsf',value)
    if f['bak']!=value:
        p.setf('v_tsf_bak',value);value<<=6;p.setf('v_tsf',value);cur=p.read_clock()&0x3fffc0;nextLine=((((cur<<1)+((263-f['vcount'])*127))&0xffffffff)>>1)&0x3fffc0;remain=0
        if value<=nextLine:
            for i in range(1,30):
                value=(value+TF)&0xffffffff
                if value>nextLine:remain=value-nextLine;remain=0 if remain>TF-T5 else remain;break
            p.setf('v_tsf',value)
        p.setf('v_remain',remain)
    if remain>T2:p.alarm(208,0x027e5dc0,2)
    else:p.setf('VSyncFlag',1);p.alarm(f['child'],0x027e5e80,4)


def child2(p):
    f=p.f;p.args=[2];p.setf('v_remain',f['remain']);p.setf('VSyncFlag',1);p.setf('mp_childVCount',f['child']);p.write(VIDEO,6,f['vcount']);p.seal();remain=f['remain']
    if 208<=f['vcount']<210 and remain>=T2:
        for i in range(1,7):
            if remain<T2+T1*i:break
        else:i=7
        p.write(VIDEO,6,f['vcount']+1-i);remain=(remain-T1*i)&0xffffffff;p.setf('v_remain',remain)
    if remain>=T2:p.setf('VSyncFlag',0)
    p.alarm(f['child'],0x027e5e80,4)


def childmp(p):
    f=p.f;p.args=[4];p.setf('mp_flag',f['flag']);p.setf('mp_lifeTimeTick',f['lifetime']);p.setf('mp_childVCount',f['child']);at=FIELDS['mp_lastRecvTick'];p.write(STATUS,at,f['last'],8);p.seal()
    if f['flag']!=1:return
    p.alarm(200,0x027e5c5c,1)
    if f['lifetime']:
        p.action(0x037fd21c,result=f['now']&0xffffffff,high=f['now']>>32);elapsed=((f['now']|1)-f['last'])&0xffffffffffffffff
        if f['last']and elapsed>f['lifetime']:
            p.write(STATUS,at,0,8);p.action(0x027e0700,result=BUFFER if f['allocated']else 0)
            if f['allocated']:
                for offset,value in [(0,37),(4,0),(8,32769)]:p.write(BUFFER,offset,value,4)
                p.action(0x037fc6d4,[WORK+136,BUFFER,0],result=f['sent'],checks=[(BUFFER,bytes(p.regions[BUFFER]))])
            if not f['allocated']or not f['sent']:
                p.action(0x038073f0,result=CB)
                for offset,value in [(0,128),(2,8),(4,22),(6,37)]:p.write(CB,offset,value)
                p.publish()
            return
    p.action(0x027e609c)


def parent(p):
    f=p.f;p.args=[5];p.setf('valarm_counter',f['counter']);p.setf('mp_parentVCount',f['parent']);p.write(VIDEO,6,f['vcount']);p.seal()
    if f['counter']>=60:
        if 203<=f['vcount']<210:p.write(VIDEO,6,f['vcount']);p.setf('valarm_counter',0)
    else:p.setf('valarm_counter',f['counter']+1)
    cur=p.read_clock();value=((((cur<<1)&0xffffffff)-f['vcount']*127)&0xffffffff)>>7;p.write(VTSF,0,value&65535);p.alarm(f['parent'],0x027e6050,5)


def scenario(f,ordinal):
    p=Plan(f,ordinal);dict(params=params,rssi=rssi,child1=child1,child2=child2,childmp=childmp,parent=parent)[f['kind']](p);return p.finish()
