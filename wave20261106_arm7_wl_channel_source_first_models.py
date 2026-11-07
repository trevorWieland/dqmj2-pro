import struct

SP=0x027fc000
STOP=0x02010000
CTX=0x02710000
SLOT=0x0380fff4
POWER=0x0480803c
FORCE=0x04808040
SEQ=0x04808048
STATE=0x04808214
SCRATCH=SP-48


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


def fixtures():
    rows=[]
    for direct in[0,1]:
        for channel in[1,14]:
            for rf in[2,5]:
                for bk in[0,0x10000,0x18000]:rows.append(dict(channel=channel,direct=direct,rf=rf,bk=bk,bbp=0,chan=0,enabled=True))
        for bbp,chan in[(0,0),(1,0),(0,1),(2,3)]:rows.append(dict(channel=6,direct=direct,rf=3,bk=0,bbp=bbp,chan=chan,enabled=True))
        for rf in[0,7]:rows.append(dict(channel=6,direct=direct,rf=rf,bk=0,bbp=0,chan=0,enabled=True))
        for channel in[0,15,31]:rows.append(dict(channel=channel,direct=direct,rf=2,bk=0,bbp=0,chan=0,enabled=False))
    rows.append(dict(channel=7,direct=0xffffffff,rf=2,bk=0,bbp=0,chan=0,enabled=True,delayed=True,mutateBk=0x10000))
    return rows


def scenario(f,ordinal):
    state=bytearray((i*13+ordinal*7)&255 for i in range(1684));initial={SLOT:p32(CTX)};actions=[];expectedWrites=[];scratch={0:None,4:0};backup=[0,65535,0x5a03][ordinal%3]
    def u16(offset,value):state[offset:offset+2]=p16(value)
    def u32(offset,value):state[offset:offset+4]=p32(value)
    u16(812,1<<f['channel']if f['enabled']else 0);u16(958,0x1234);u16(1528,f['rf']);u16(1532,7);u16(1534,f['chan']);u16(1536,f['bbp']);u32(1540,f['bk']);initial[CTX]=bytes(state);initial[FORCE]=p16(backup);initial[SEQ]=p16(0x3579);initial[POWER]=p16(512);initial[STATE]=p16(0)
    def action(address,args,checks=(),mutations=()):actions.append(dict(address=address,args=list(args),returned=0x87654321,checks=list(checks),mutations=list(mutations)))
    def flash(offset,size,slot):
        value=bytes((offset*37+i*19+ordinal*11)&255 for i in range(size));old=scratch[slot]
        if old is None:raise ValueError('Scratch initialized-value model incomplete')
        action(0x27f4e7c if f['direct']else 0x27f4e1c,[offset,size,SCRATCH+slot],[(SCRATCH+slot,p32(old))],[(SCRATCH+slot,value)]);scratch[slot]=(old&~((1<<(size*8))-1))|int.from_bytes(value,'little');return scratch[slot]
    def rf(value,mutate=False):
        changes=[]
        if mutate and'mutateBk'in f:u32(1540,f['mutateBk']);changes=[(CTX+1540,p32(f['mutateBk']))]
        action(0x27ea62c,[value],mutations=changes)
    def bbp(address,value):action(0x27ea5fc,[address,value])
    if f['enabled']:
        u16(958,f['channel']);expectedWrites=[(FORCE,2,0x8001),(FORCE,2,backup),(SEQ,2,3)]
        if f['rf']in[2,5]:
            first=242+6*(f['channel']-1);rf(flash(first,3,4));rf(flash(first+3,3,4),True);scratch[4]=0;bk=f.get('mutateBk',f['bk'])
            if bk&0x10000:
                if not bk&0x8000:rf(bk|((flash(340+f['channel']-1,1,4)&31)<<10))
            else:bbp(30,flash(326+f['channel']-1,1,4))
        elif f['rf']==3:
            address=42+164+7+1
            for index in range(f['bbp']):
                scratch[0]=scratch[4]=0;reg=flash(address,1,0);value=flash(address+f['channel'],1,4);bbp(reg,value);address+=15
            for index in range(f['chan']):
                scratch[4]=0;flash(address,1,4);scratch[4]<<=8;value=flash(address+f['channel'],1,4);rf(value|5<<16);address+=15
    expected={SLOT:p32(CTX),CTX:bytes(state),FORCE:p16(backup),SEQ:p16(3 if f['enabled']else 0x3579)}
    return dict(args=[f['channel'],f['direct']],initial=initial,regions=expected,actions=actions,allowedWriteRanges=[(CTX+958,CTX+960)],frame=48,returnValue=0 if f['enabled']else 5,expectedMmioWrites=expectedWrites,polling=[(1,0),(2,4),(2,9)]if f.get('delayed')else[(2,0)],pollCount=3 if f.get('delayed')else 1)
