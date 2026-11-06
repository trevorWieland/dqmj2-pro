from project import read_json
from wave20261106_arm7_wm_residual_next_first_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
MESSAGE=0x02302000
CB=0x02304000
RESULT=0x02306000
PARAM=0x02308000
WORK=0x027f7884
FRAME={0x027e2f5c:520,0x027e2eac:528,0x027e5790:528,0x027e5a98:520,0x027e5b00:528}
LAYOUT=read_json(LANE/'layout-baseline.json')
STATUS_FIELDS={}
for row in LAYOUT.values():STATUS_FIELDS.update(row['fields'].get('WMStatus',{}))


def pack(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def fixtures():
    rows=[]
    for channel in [0,1,13,15]:
        for enabled in [0,65535]:
            for code in [0,5]:rows.append(dict(entry=0x027e2f5c,kind='parent',channel=channel,enabled=enabled,code=code,maxEntry=[0,1,15,65535][channel%4]))
    for state in [0,1,2,9,65535]:
        for code in [0,7]:rows.append(dict(entry=0x027e2eac,kind='end',state=state,code=code))
    for lifetime in [0,1,65534,65535,0x12340002]:
        for code in [0,5]:
            for tick in [0,0x123456789abcdef0]:rows.append(dict(entry=0x027e5790,kind='life',lifetime=lifetime,code=code,tick=tick,table=0x89ab1234,cam=0xffff8000,frame=0xabcd0001))
    for code in [0,5,65535]:
        rows.append(dict(entry=0x027e5a98,kind='init',code=code));rows.append(dict(entry=0x027e5b00,kind='counter',code=code))
    return rows


def scenario(f,ordinal):
    entry=f['entry'];frame=FRAME[entry];stack=SP-frame;s=bytearray((i*17+ordinal*11)&255 for i in range(2000));cb=bytearray((i*7+ordinal)&255 for i in range(256));work=bytearray((i*23+ordinal)&255 for i in range(5520));message=bytearray((i*19+ordinal)&255 for i in range(128));param=bytearray((i*13+ordinal)&255 for i in range(64));initial={};actions=[]
    def setf(name,val):at=STATUS_FIELDS[name];width=STATUS_FIELDS[name+'.width'];s[at:at+width]=pack(val,width)
    def action(address,args=(),result=0,checks=(),mutations=(),high=None):
        row=dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations))
        if high is not None:row['returnedHigh']=high
        actions.append(row)
    def getcb():action(0x038073f0,result=CB)
    def fields(**values):
        for name,val in values.items():offset=dict(apiid=0,errcode=2,wlCmdID=4,wlResult=6)[name];cb[offset:offset+2]=pack(val)
    def publish():action(0x038073a4,[CB],checks=[(CB,bytes(cb)),(STATUS,bytes(s))])
    def response(code):
        r=bytearray((i*5+ordinal*3)&255 for i in range(256));r[4:6]=pack(code);return bytes(r)
    def wl(address,arguments):action(address,arguments,result=RESULT,mutations=[(RESULT,response(f['code']))])
    def failure(api,command):getcb();fields(apiid=api,errcode=1,wlCmdID=command,wlResult=f['code']);publish()
    work[5456:5460]=pack(STATUS,4)
    if f['kind']=='parent':
        setf('enableChannel',f['enabled']);message[4:8]=pack(PARAM,4);param[16:18]=pack(f['maxEntry']);param[50:52]=pack(f['channel'])
    elif f['kind']=='end':setf('state',f['state'])
    elif f['kind']=='life':
        for i,key in enumerate(['table','cam','frame','lifetime'],1):message[4*i:4*i+4]=pack(f[key],4)
    initial.update({STATUS:bytes(s),CB:bytes(cb),WORK:bytes(work),MESSAGE:bytes(message),PARAM:bytes(param),RESULT:response(0)})
    if f['kind']=='parent':
        action(0x037fe12c,[PARAM,STATUS+232,64],mutations=[(STATUS+232,bytes(param))]);s[232:296]=param
        if not((1<<f['channel'])&f['enabled']):getcb();fields(apiid=7,errcode=6);publish()
        else:
            wl(0x027e2648,[stack,f['maxEntry']])
            if f['code']:failure(7,0x212)
            else:getcb();fields(apiid=7,errcode=0);publish()
    elif f['kind']=='end':
        if f['state']!=2:getcb();fields(apiid=2,errcode=3);publish()
        else:
            wl(0x027e2880,[stack])
            if f['code']:failure(2,0x301)
            else:
                setf('state',1);action(0x0380528c,[1],checks=[(STATUS,bytes(s))]);setf('state',0);getcb();fields(apiid=2,errcode=0);publish()
    elif f['kind']=='life':
        wl(0x027e25e0,[stack,f['table']&65535,f['cam']&65535,f['frame']&65535])
        if f['code']:failure(29,0x211)
        else:
            lifetime=f['lifetime']&65535;setf('mp_lifeTimeTick',0 if lifetime==65535 else 1 if lifetime==0 else(33514*(lifetime*100))//64);action(0x037fd21c,result=f['tick']&0xffffffff,high=f['tick']>>32,checks=[(STATUS,bytes(s))]);at=STATUS_FIELDS['mp_lastRecvTick'];s[at:at+128]=pack(f['tick']|1,8)*16;getcb();fields(apiid=29,errcode=0);publish()
    elif f['kind']=='init':
        wl(0x027e28dc,[stack])
        if f['code']:failure(31,0x305)
        else:getcb();fields(apiid=31,errcode=0);publish()
    elif f['kind']=='counter':
        wl(0x027e290c,[stack])
        if f['code']:failure(32,0x307)
        else:
            getcb();fields(apiid=32,errcode=0);payload=response(0)[8:188];action(0x037fdf9c,[RESULT+8,CB+8,180],checks=[(CB,bytes(cb))],mutations=[(CB+8,payload)]);cb[8:188]=payload;publish()
    else:raise ValueError('Unmodeled admitted request fixture')
    return dict(args=[MESSAGE],initial=initial,regions={STATUS:bytes(s),WORK:bytes(work),CB:bytes(cb),MESSAGE:bytes(message),PARAM:bytes(param)},actions=actions,returnValue=None,frame=frame,entry=entry,allowedWriteRanges=[(STATUS,STATUS+2000),(CB,CB+256)])
