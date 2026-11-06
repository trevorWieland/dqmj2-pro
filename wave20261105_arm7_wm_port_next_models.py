from project import ROOT,read_json
from wave20261105_arm7_wm_port_next_build import LANE
SP=0x027fc000
STOP=0x02010000
STATUS=0x02300000
SEND=0x02302000
DATA=0x02304000
CB=0x02306000
RESULT=0x02307000
RECV=0x02308000
FRAME={0x027e7c20:16,0x027e637c:8,0x027e6434:648,0x027e692c:752,0x027e72d4:560,0x027e73c4:32,0x027e74f8:96,0x027e7828:56,0x027e7a1c:64}
GEOMETRY=read_json(LANE/'layout-baseline.json')['fields']
CONSTANTS=GEOMETRY['constants']


def packed(value,size=2):return(int(value)&((1<<(size*8))-1)).to_bytes(size,'little')


def timer(length,txop,poll,target,vcount):
    txop=(txop&0x7fff) if txop&0x8000 else 96+(txop+28)*4+6
    duration=(96+(34+length)*4+670+txop*(poll&0xffffffff).bit_count()+234)&0xffffffff
    delta=(target-2-vcount)&0xffffffff
    if delta&0x80000000:delta-=0x100000000
    while delta<0:delta+=263
    value=delta*127//20
    return value&0xffff if value*10>=duration else 0


def fixtures():
    rows=[]
    for i in range(128):rows.append(dict(entry=0x027e7c20,kind='timer',length=[0,2,32,512][i%4],txop=[0,24,0x8000,0x80d6][i//4%4],poll=[0,1,3,0xffff][i//16%4],target=[0,2,100,262][i//32],vcount=[0,1,100,262][i%4]))
    rows += [dict(entry=0x027e637c,kind='init',seed=i) for i in range(8)]
    for i in range(48):rows.append(dict(entry=0x027e73c4,kind='put',size=[0,4,516,515][i%4],port=[0,8,15][i//4%3],priority=i%4,free=['empty','single','pair'][i//12%3],ready=bool(i//24),retry=[0,2,65535][i%3]))
    for state in [0,9,10]:
        for use in [0,1]:
            for timeout in [0,1]:rows.append(dict(entry=0x027e74f8,kind='flush-empty',state=state,use=use,timeout=timeout))
    for i in range(32):rows.append(dict(entry=0x027e74f8,kind='flush-one',state=[9,10][i%2],aid=i%2,timeout=i//2%2,port=[0,8][i//4%2],rest=[0,2,3,1][i//8%4],retry=[0,2][i//16],poll=[0,2][i%2],ready=bool(i//8%2)))
    for i in range(16):rows.append(dict(entry=0x027e7828,kind='clean',aidMask=[0,1,2,3][i%4],rest=[2,3][i//4%2],aid=i//8,ready=bool(i%2)))
    for i,(aid,length) in enumerate([(0,0),(16,2),(1,0),(1,517),(1,3),(0,2),(1,2)]):rows.append(dict(entry=0x027e7a1c,kind='parse-invalid',aid=aid,length=length,myAid=0,header=4))
    for i in range(32):rows.append(dict(entry=0x027e7a1c,kind='parse',aid=1,myAid=[0,2][i%2],size=[2,4][i//2%2],port=[0,3,8,15][i//4%4],dest=bool(i//16),allowed=bool(i%2),fresh=bool(i//2%2)))
    for i in range(16):rows.append(dict(entry=0x027e6434,kind='key',branch=['child-zero','small-buffer','bad-aid','bad-state','queue-busy','empty','empty','empty'][i%8],code=[0,8,5][i%3],vsync=i%2))
    for i in range(24):rows.append(dict(entry=0x027e692c,kind='mp',branch=['small-buffer','bad-aid','bad-state','queue-busy','empty','ping'][i%6],code=[0,8,5][i%3],vsync=i%2,count=i%2,newFrame=i//6%2,minMode=i//12))
    for i in range(8):rows.append(dict(entry=0x027e6434,kind='key',branch='packet',code=[0,8,5][i%3],vsync=i%2))
    for i in range(8):rows.append(dict(entry=0x027e692c,kind='mp',branch='packet',code=0,vsync=0,count=i%2,newFrame=i//2%2,minMode=i//4))
    for i in range(16):rows.append(dict(entry=0x027e72d4,kind='resume',small=bool(i%2),count=i//2%2,header=[0x8001,0x1001][i//4%2],poll=[1,3][i//8]))
    return rows


def scenario(f,ordinal):
    fields=GEOMETRY['WMStatus'];qfields=GEOMETRY['WMPortSendQueueData'];s=bytearray((i*17+ordinal*11)&255 for i in range(2000));cb=bytearray((i*7+ordinal)&255 for i in range(80));send=bytearray((i*13+ordinal)&255 for i in range(1024));data=bytearray((i*19+ordinal)&255 for i in range(1024));actions=[];args=[];expectedReturn=None;initial={};endRegions={};constants=CONSTANTS
    def put(typ,buf,name,value,base=0):buf[base+GEOMETRY[typ][name]:base+GEOMETRY[typ][name]+GEOMETRY[typ][name+'.width']]=packed(value,GEOMETRY[typ][name+'.width'])
    def setf(name,value):put('WMStatus',s,name,value)
    def getf(name):return int.from_bytes(s[fields[name]:fields[name]+fields[name+'.width']],'little')
    def qput(index,name,value):put('WMPortSendQueueData',s,name,value,fields['sendQueueData']+32*index)
    def qget(index,name):at=fields['sendQueueData']+32*index+qfields[name];return int.from_bytes(s[at:at+qfields[name+'.width']],'little')
    def queue(name,prio,head,tail):at=fields[name]+4*prio;s[at:at+4]=packed(head)+packed(tail)
    def action(address,args=(),result=0,checks=(),mutations=()):actions.append(dict(address=address,args=list(args),returned=result,checks=list(checks),mutations=list(mutations)))
    def lock():action(0x037fc888,[STATUS+1820])
    def unlock():action(0x037fc90c,[STATUS+1820],checks=[(STATUS,bytes(s))])
    def irq():action(0x037fdd00,result=0x80);action(0x037fdd14,[0x80],result=0x80)
    def publish(index,error):
        action(0x038073f0,result=CB,checks=[(STATUS,bytes(s))]);values=dict(apiid=129,errcode=error,state=20,port=qget(index,'port'),destBitmap=qget(index,'destBitmap'),restBitmap=qget(index,'restBitmap'),sentBitmap=qget(index,'sentBitmap'),size=qget(index,'size'),data=qget(index,'data'),callback=qget(index,'callback'),arg=qget(index,'arg'),seqNo=qget(index,'seqNo'),maxSendDataSize=getf('mp_parentSize') if getf('aid')==0 else getf('mp_childSize'),maxRecvDataSize=getf('mp_childSize') if getf('aid')==0 else getf('mp_parentSize'))
        for name,value in values.items():put('WMPortSendCallback',cb,name,value)
        action(0x038073a4,[CB],checks=[(CB,bytes(cb))])
    def appendFree(index):
        tail=getf('sendQueueFreeList')>>16
        if tail==65535:s[fields['sendQueueFreeList']:fields['sendQueueFreeList']+2]=packed(index)
        else:qput(tail,'next',index)
        s[fields['sendQueueFreeList']+2:fields['sendQueueFreeList']+4]=packed(index);qput(index,'next',65535)
    for name,value in dict(state=9,aid=0,sendQueueInUse=0,mp_current_defaultRetryCount=2,child_bitmap=3,mp_readyBitmap=3,mp_sendSize=16,mp_sendBuf=SEND,mp_sendBufSize=32,mp_recvSize=16,mp_recvBufSize=4096,mp_count=0,mp_limitCount=0,mp_current_minPollBmpMode=0,mp_current_singlePacketMode=0,mp_newFrameFlag=0,mp_pingFlag=0,mp_parentVCount=200,mp_prevPollBitmap=0,mp_prevWmHeader=0x8001,mp_prevTxop=18,mp_prevDataLength=4,mp_setDataFlag=0,VSyncFlag=0,mp_parentSize=512,mp_childSize=128).items():setf(name,value)
    for name in ['readyQueue','sendQueue']:
        for p in range(4):queue(name,p,65535,65535)
    s[fields['sendQueueFreeList']:fields['sendQueueFreeList']+4]=packed(3)+packed(3)
    for i in range(32):
        for name,value in dict(next=65535,port=0,destBitmap=3,restBitmap=3,sentBitmap=0,sendingBitmap=2,data=DATA,size=4,callback=0x027e0898,arg=0x12345678,seqNo=0xffff,retryCount=2).items():qput(i,name,value)
    entry=f['entry'];kind=f['kind'];vcount=f.get('vcount',100);tsf=(0x1234+ordinal)&65535
    if kind=='put':
        setf('mp_current_defaultRetryCount',f['retry']);s[fields['sendQueueFreeList']:fields['sendQueueFreeList']+4]=packed(65535 if f['free']=='empty' else 2)+packed(65535 if f['free']=='empty' else 2 if f['free']=='single' else 3);qput(2,'next',3 if f['free']=='pair' else 65535)
        if f['ready']:queue('readyQueue',f['priority'],0,1);qput(0,'next',1)
    if kind.startswith('flush'):
        setf('state',f['state']);setf('sendQueueInUse',f.get('use',1));setf('aid',f.get('aid',0))
        if kind=='flush-one':
            queue('sendQueue',0,2,2)
            for name in ['port','restBitmap','retryCount']:qput(2,name,f[{'restBitmap':'rest','retryCount':'retry'}.get(name,name)])
            if f['ready']:queue('readyQueue',0,0,1);qput(0,'next',1)
    if kind=='clean':
        setf('aid',f['aid']);queue('sendQueue',0,1,1)
        if f['ready']:queue('readyQueue',0,2,2)
        qput(2,'restBitmap',f['rest'])
    if kind.startswith('parse'):
        setf('aid',f['myAid'])
        if kind=='parse':
            header=(f['size']//2)|(f['port']<<8)|(0x1000 if f['dest'] else 0);length=f['size']+(2 if f['port']&8 else 0)+(2 if f['dest'] else 0);at=f['size'];seq=41
            if f['port']&8:data[at:at+2]=packed(seq);at+=2;s[fields['portSeqNo']+f['aid']*16+(f['port']&7)*2:fields['portSeqNo']+f['aid']*16+(f['port']&7)*2+2]=packed(65535 if f['fresh'] else seq*2)
            if f['dest']:data[at:at+2]=packed((1<<f['myAid']) if f['allowed'] else 0)
            f=dict(f,header=header,length=length)
    if kind in ['key','mp']:
        setf('VSyncFlag',f['vsync']);branch=f['branch'];setf('child_bitmap',0 if branch=='child-zero' else 3);setf('aid',16 if branch=='bad-aid' else 1);setf('state',0 if branch=='bad-state' else 10 if kind=='key' else 9);setf('mp_sendBufSize',0 if branch=='small-buffer' else 32);setf('sendQueueInUse',1 if branch=='queue-busy' else 0)
        if branch=='packet':queue('readyQueue',0,2,2)
        if kind=='mp':setf('mp_pingFlag',1 if branch=='ping' else 0);setf('mp_count',f['count']);setf('mp_limitCount',f['count']);setf('mp_newFrameFlag',f['newFrame']);setf('mp_current_minPollBmpMode',f['minMode'])
    if kind=='resume':setf('mp_recvBufSize',0 if f['small'] else 4096);setf('mp_count',f['count']);setf('mp_prevWmHeader',f['header'])
    initial[STATUS]=bytes(s);initial[SEND]=bytes(send);initial[DATA]=bytes(data);initial[CB]=bytes(cb);result=bytearray(64);result[4:6]=packed(f.get('code',0));initial[RESULT]=bytes(result);work=bytearray((i*23+ordinal)&255 for i in range(5520));work[5456:5460]=packed(STATUS,4);initial[0x027f7884]=bytes(work);initial[0x04000006]=packed(vcount);initial[0x048080f8]=packed(tsf)
    if kind=='timer':args=[f['length'],f['txop'],f['poll'],f['target']];action(0x03803830,[f['poll']],result=f['poll'].bit_count());expectedReturn=timer(*args,vcount)
    elif kind=='init':
        args=[];lock();action(0x037fdf74,[0,STATUS+760,1024],mutations=[(STATUS+760,bytes(1024))]);s[760:1784]=bytes(1024)
        for i in range(32):qput(i,'next',i+1 if i<31 else 65535)
        s[1784:1788]=packed(0)+packed(31)
        for name in ['readyQueue','sendQueue']:
            for p in range(4):queue(name,p,65535,65535)
        unlock()
    elif kind=='put':
        args=[0x0f0f,f['priority'],f['port'],0xdeadf3f3,DATA,f['size'],0x027e0898,0x12345678];expectedReturn=6
        if f['size'] and f['size']+(2 if f['port']&8 else 0)<=516:
            lock();expectedReturn=10
            if f['free']!='empty':
                s[1784:1788]=packed(3 if f['free']=='pair' else 65535)+packed(3 if f['free']=='pair' else 65535)
                for name,value in dict(port=f['port'],destBitmap=0xf3f3,restBitmap=0x0303,sentBitmap=0,sendingBitmap=0,data=DATA,size=f['size'],callback=0x027e0898,arg=0x12345678,next=65535,seqNo=65535,retryCount=f['retry']).items():qput(2,name,value)
                if f['ready']:qput(1,'next',2);queue('readyQueue',f['priority'],0,2)
                else:queue('readyQueue',f['priority'],2,2)
                expectedReturn=2
            unlock()
    elif kind.startswith('flush'):
        args=[f['timeout'],f.get('poll',0)];expectedReturn=0
        if f['state'] in [9,10]:
            lock()
            if getf('sendQueueInUse'):
                if f['state']==9:irq()
                if kind=='flush-one':
                    rest=f['rest'];sent=0
                    if not f['timeout']:sent=2&~f['poll'];rest&=~sent
                    rest&=3 if f['state']==9 else 1;qput(2,'sentBitmap',sent);qput(2,'restBitmap',rest);qput(2,'sendingBitmap',0)
                    if rest and (f['port']&8 or f['retry']):
                        expectedReturn=1;qput(2,'retryCount',max(f['retry']-1,0));qput(2,'next',0 if f['ready'] else 65535);queue('readyQueue',0,2,1 if f['ready'] else 2)
                    else:publish(2,0 if rest==0 else 15);appendFree(2)
                    queue('sendQueue',0,65535,65535)
                setf('sendQueueInUse',0)
            unlock()
    elif kind=='clean':
        args=[f['aidMask']];lock()
        if f['ready']:
            remaining=f['rest']&(~f['aidMask']&3);qput(2,'restBitmap',remaining);qput(2,'sendingBitmap',2&(~f['aidMask']&3))
            if remaining==0:publish(2,0);queue('readyQueue',0,65535,65535);appendFree(2)
        unlock()
    elif kind.startswith('parse'):
        args=[f['aid'],f['header'],DATA,f['length'],RECV]
        if kind=='parse':
            valid=True;seq=65535
            if f['port']&8:
                seq=41;at=fields['portSeqNo']+f['aid']*16+(f['port']&7)*2
                if f['fresh']:s[at:at+2]=packed(seq*2)
                else:valid=False;seq*=2
            if f['dest'] and not f['allowed']:valid=False
            if valid:
                action(0x038073f0,result=CB,checks=[(STATUS,bytes(s))]);values=dict(apiid=130,errcode=0,state=21,port=f['port'],recvBuf=RECV,data=DATA,length=f['size'],aid=f['aid'],myAid=f['myAid'],seqNo=seq,maxSendDataSize=512 if f['myAid']==0 else 128,maxRecvDataSize=128 if f['myAid']==0 else 512)
                for name,value in values.items():put('WMPortRecvCallback',cb,name,value)
                action(0x038073a4,[CB],checks=[(CB,bytes(cb))])
    elif kind in ['key','mp']:
        args=[] if kind=='key' else [3];branch=f['branch']
        if kind=='mp':irq()
        if kind=='mp' and f['newFrame']:setf('mp_newFrameFlag',0)
        failed=branch in ['small-buffer','bad-aid','bad-state','queue-busy']
        if kind=='key' and branch=='child-zero':pass
        else:
            if kind=='key':setf('mp_setDataFlag',1)
            if branch=='ping':
                setf('mp_pingFlag',0);irq();setf('mp_count',f['count']+1);setf('mp_limitCount',f['count']+1);txop=0x80d6;poll=3;tmptt=0;header=0
            else:
                if branch not in ['small-buffer','bad-aid','bad-state']:
                    lock()
                    if branch!='queue-busy':setf('sendQueueInUse',1)
                    if branch=='packet':
                        action(0x037fdf9c,[DATA,SEND,4],mutations=[(SEND,bytes(data[:4]))]);send[:4]=data[:4]
                        if kind=='mp':send[4:6]=packed(3)
                        qput(2,'sendingBitmap',1 if kind=='key' else 3);queue('readyQueue',0,65535,65535);queue('sendQueue',0,2,2)
                    unlock()
                if failed:
                    if kind=='key':setf('mp_setDataFlag',0)
                    else:setf('mp_count',0);setf('mp_limitCount',0)
                elif kind=='key':action(0x027e22ac,['frame-buffer',4 if branch=='packet' else 0,(2 if branch=='packet' else 0)|(0x8000 if f['vsync'] else 0),SEND],result=RESULT);setf('mp_setDataFlag',0 if f['code'] not in [0,8] else 1)
                else:
                    txop=18;poll=0 if f['minMode'] and branch!='packet' else 3;action(0x03803830,[poll],result=poll.bit_count());tmptt=0;header=0x1002 if branch=='packet' else 0
                    if f['count']==1:tmptt=timer(6 if branch=='packet' else 0,txop,poll,200,vcount);action(0x027e7c20,[6 if branch=='packet' else 0,txop,poll,200],result=tmptt);header|=0x8000
            if kind=='mp' and not failed:
                action(0x027e2314,['frame-buffer',0,0,txop,poll,tmptt,tsf,6 if branch=='packet' else 0,header,SEND],result=RESULT);setf('mp_prevPollBitmap',poll);setf('mp_prevWmHeader',header);setf('mp_prevTxop',txop);setf('mp_prevDataLength',6 if branch=='packet' else 0)
    elif kind=='resume':
        args=[f['poll']];irq();poll=f['poll']&3;action(0x03803830,[poll],result=poll.bit_count())
        if f['small']:action(0x037fc468,[2]);action(0x027e1a54)
        else:
            header=f['header'];tmptt=0
            if f['count']:tmptt=timer(4,18,poll,200,vcount);action(0x027e7c20,[4,18,poll,200],result=tmptt);header|=0x8000
            else:header&=~0x8000
            action(0x027e2314,['frame-buffer',0x800c,0,0,poll,tmptt,tsf,0,header,0],result=RESULT)
    else:raise ValueError('Unmodeled WM port fixture')
    endRegions={STATUS:bytes(s),CB:bytes(cb),SEND:bytes(send),DATA:bytes(data),0x027f7884:bytes(work),RESULT:bytes(result)}
    return dict(args=args,initial=initial,regions=endRegions,actions=actions,returnValue=expectedReturn,allowedWriteRanges=[(STATUS,STATUS+2000),(CB,CB+80),(SEND,SEND+1024),(SP,SP+max(0,len(args)-4)*4)],frame=FRAME[entry],entry=entry)
