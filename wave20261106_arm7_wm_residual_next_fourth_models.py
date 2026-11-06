from project import read_json
from wave20261106_arm7_wm_residual_next_fourth_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
BUFFER=0x02302000
CB=0x02304000
RESULT=0x02306000
WORK=0x027f7884
SYSTEM=0x027ffc00
LAYOUT=read_json(LANE/'layout-baseline.json')
FIELDS=LAYOUT['027e2a90']['fields']['WMStatus']


def pack(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def fixtures():
    rows=[]
    def reset(**values):rows.append(dict(dict(entry=0x027e2a90,kind='reset',state=8,mp=0,children=1,station=0x40,mode=2,preamble=0,fail='none',codes=[0],mutateState=False,code=5),**values))
    for state,mp in [(7,0),(8,0),(9,1),(10,1),(8,2)]:
        for children in [0,1,0x8001]:reset(state=state,mp=mp,children=children)
    for station in [0,0x10,0x20,0x30,0x40,0x11,0x12,0xffff]:
        for mode in [0,1,2,3]:reset(station=station,mode=mode,preamble=station%2)
    for stage in ['station','mode','reset','idle','preamble','test']:reset(fail=stage,station=0x11 if stage=='test'else 0x40,mode=0 if stage=='test'else 2)
    for codes in [[7,0],[12,12],[5],[7,12]]:reset(codes=codes)
    reset(codes=[7],mutateState=True)
    for pool in [0,1,32767,32768,65535]:
        for rssi in [0,1,127,128,255]:rows.append(dict(entry=0x027e3850,kind='pool',pool=pool,rssi=rssi))
    return rows


def scenario(f,ordinal):
    frame=568 if f['kind']=='reset'else 0;stack=SP-frame;regions={a:bytearray((i*17+ordinal*13+a//256)&255 for i in range(size))for a,size in [(STATUS,2000),(BUFFER,256),(CB,80),(RESULT,32),(WORK,5520),(SYSTEM,1024)]};actions=[];args=[BUFFER];expectedReturn=None
    def write(address,offset,value,size=2):regions[address][offset:offset+size]=pack(value,size)
    def setf(name,value):write(STATUS,FIELDS[name],value,FIELDS[name+'.width'])
    def action(address,args=(),result=0,checks=(),mutations=()):actions.append(dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations)))
    def status():return(STATUS,bytes(regions[STATUS]))
    write(WORK,5456,STATUS,4)
    if f['kind']=='pool':
        args=[f['rssi']];write(SYSTEM,920,f['pool']);initial={a:bytes(r)for a,r in regions.items()};value=(f['pool']<<1)^f['rssi'];write(SYSTEM,920,value^(value>>16))
    else:
        for name,value in dict(state=f['state'],mp_flag=f['mp'],child_bitmap=f['children'],preamble=f['preamble'],wep_flag=1).items():setf(name,value)
        initial={a:bytes(r)for a,r in regions.items()};action(0x037fdd00,result=0x80);state=f['state'];clean=f['mp']==1
        if clean:
            setf('mp_flag',0);action(0x027e5b98,checks=[status()]);action(0x027e0640,checks=[status()]);state=8 if state==10 else 7 if state==9 else state;setf('state',state)
        if state not in [7,8]:raise ValueError('Independent Reset model intentionally requires source-initialized parent/child discriminator')
        parent=state==7;children=f['children']
        for name,value in dict(child_bitmap=0,mp_readyBitmap=0,ks_flag=0,dcf_flag=0,VSyncFlag=0,beaconIndicateFlag=0).items():setf(name,value)
        action(0x037fdd14,[0x80],checks=[status()])
        if clean:action(0x027e7828,[65535],checks=[status()])
        if parent:write(STATUS,246,0)
        for i in range(16):
            if children&(1<<i):
                offset=394 if i==0 else 296+(i-1)*6;action(0x027e4a94,[int(parent),i,STATUS+offset],checks=[(STATUS+offset,initial[STATUS][offset:offset+6])])
        action(0x037fe070,[STATUS+296,0,90],mutations=[(STATUS+296,bytes(90))]);regions[STATUS][296:386]=bytes(90)
        def response(code,value=0):
            raw=bytearray(initial[RESULT]);raw[4:6]=pack(code);raw[6:8]=pack(value);return bytes(raw)
        def wl(address,args,stage,value=0):
            code=f['code']if f['fail']==stage else 0;action(address,args,result=RESULT,mutations=[(RESULT,response(code,value))]);return code
        def error(command,code):action(0x027e2e7c,[command,code],checks=[status()])
        def process():
            nonlocal state
            code=wl(0x027e2924,[stack+16],'station',f['station'])
            if code:error(0x308,code);return
            code=wl(0x027e286c,[stack+16],'mode',f['mode'])
            if code:error(0x284,code);return
            station=f['station'];mode=f['mode']
            if station in [0x30,0x40]:
                if mode in [2,3]:
                    mac=initial[STATUS][394:400];action(0x037fe12c,[STATUS+394,stack+10,6],mutations=[(stack+10,mac)])
                    for n,code in enumerate(f['codes'][:2]):
                        if state!=8:break
                        mutations=[(RESULT,response(code))]
                        if f['mutateState']and n==0:state=2;setf('state',state);mutations.append((STATUS,bytes(regions[STATUS])))
                        action(0x027e1fcc,[stack+16,stack+10,3],result=RESULT,mutations=mutations)
                        if code==0:state=3;setf('state',state);break
                        if code not in [7,12]:break
                elif mode==1:
                    action(0x037fe070,[stack+4,255,6],mutations=[(stack+4,b'\xff'*6)]);code=f['codes'][0];action(0x027e1fcc,[stack+16,stack+4,3],result=RESULT,mutations=[(RESULT,response(code))])
                    if code==0:state=3;setf('state',state)
            if station in [0x20,0x30,0x40]:
                code=wl(0x027e1d68,[stack+16,1],'reset')
                if code:error(0,code);return
            if station in [0,0x20,0x30,0x40]:
                code=wl(0x027e2898,[stack+16],'idle')
                if code:error(0x302,code);return
            if station in [0,0x10,0x20,0x30,0x40]:
                if f['preamble']==0:
                    code=wl(0x027e2584,[stack+16,1],'preamble')
                    if code:error(0x20e,code);return
                    setf('preamble',1)
                setf('state',2);setf('wep_flag',0);action(0x027e076c,checks=[status()])
            elif station in [0x11,0x12]:
                if mode==0:
                    code=wl(0x027e2938,[stack+16,0,0,0x14,1],'test')
                    if code:error(0x309,code);return
                code=wl(0x027e2898,[stack+16],'idle')
                if code:error(0x302,code);return
                setf('state',2)
            else:error(0x308,0);return
            action(0x038073f0,result=CB);write(CB,0,1);write(CB,2,0);action(0x038073a4,[CB],checks=[(CB,bytes(regions[CB])),status()])
        process()
    return dict(args=args,initial=initial,regions={a:bytes(r)for a,r in regions.items()if a!=RESULT},actions=actions,returnValue=expectedReturn,frame=frame,entry=f['entry'],allowedWriteRanges=[(a,a+len(regions[a]))for a in [STATUS,BUFFER,CB,SYSTEM]])
