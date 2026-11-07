import struct

SP=0x027fc000
STOP=0x02010000
GROUP=0x027f8e34
CLOCK=0x027ffde8
SCRATCH=SP-40
RECEIVE=0x037fc760
REPLY=0x027f6074
BOOL_COMMANDS=[0x13,0x14,0x15,0x23,0x24,0x25]


def p16(value):return struct.pack('<H',value&65535)
def p32(value):return struct.pack('<I',value&0xffffffff)


def fixtures():
    rows=[dict(command=c,result=1,format=0)for c in range(42)]
    rows.extend(dict(command=c,result=value,format=0)for c in BOOL_COMMANDS for value in[0,0x80000000])
    rows.extend([dict(command=42,result=1,format=0),dict(command=65535,result=1,format=0),dict(command=1,result=1,format=1),dict(command=0x29,result=1,format=0,initialCommand=0x10)])
    return rows


def scenario(f,ordinal):
    group=bytearray((i*17+ordinal*11)&255 for i in range(478));group[472:476]=p32(0x12340001);group[476:478]=p16(f.get('initialCommand',f['command']));clock=bytearray((i*19+ordinal*13)&255 for i in range(8));clock[0]=(clock[0]&~3)|(f['format']<<1);initial={GROUP:bytes(group),CLOCK:bytes(clock)};actions=[]
    def action(address,args,returned=0x87654321,checks=(),mutations=(),stop=False):actions.append(dict(address=address,args=list(args),returned=returned,checks=list(checks),mutations=list(mutations),stop=stop))
    changes=[(SCRATCH,p32(0xabcd0000+ordinal))]
    if'initialCommand'in f:group[476:478]=p16(f['command']);changes.append((GROUP+476,p16(f['command'])))
    action(RECEIVE,[GROUP+4,SCRATCH,1],1,mutations=changes);command=f['command'];result=0
    operations={0:(0x27f6638,[]),1:(0x27f667c,[f['format']]),0x10:(0x27f67a0,[CLOCK]),0x11:(0x27f6804,[CLOCK]),0x12:(0x27f6830,[CLOCK+4]),0x13:(0x27f6894,[CLOCK+4]),0x14:(0x27f6970,[CLOCK+4]),0x15:(0x27f6a44,[CLOCK+4]),0x16:(0x27f6b10,[CLOCK]),0x17:(0x27f6b74,[CLOCK+2]),0x18:(0x27f6bd8,[CLOCK+4]),0x19:(0x27f6c3c,[CLOCK+4]),0x20:(0x27f67cc,[CLOCK]),0x21:(0x27f67cc,[CLOCK]),0x22:(0x27f685c,[CLOCK+4]),0x23:(0x27f68fc,[CLOCK+4]),0x24:(0x27f69d4,[CLOCK+4]),0x25:(0x27f6aa4,[CLOCK+4]),0x26:(0x27f6b3c,[CLOCK]),0x27:(0x27f6ba0,[CLOCK+2]),0x28:(0x27f6c04,[CLOCK+4]),0x29:(0x27f6c68,[CLOCK+4])}
    read_parts={0x10:(0,8),0x11:(0,4),0x12:(4,4),0x13:(4,4),0x14:(4,4),0x15:(4,4),0x16:(0,2),0x17:(2,2),0x18:(4,4),0x19:(4,4)}
    def read_data(address,args,offset,size,returned):
        before=bytes(clock);raw=bytes((ordinal*7+index*31+0x52)&255 for index in range(size));clock[offset:offset+size]=raw;action(address,args,returned,checks=[(CLOCK,before)],mutations=[(CLOCK+offset,raw)])
    if command in operations:
        address,args=operations[command]
        if command==0x21:read_data(0x27f6830,[CLOCK+4],4,4,0x87654321)
        if command in read_parts:
            offset,size=read_parts[command];read_data(address,args,offset,size,f['result']if command in BOOL_COMMANDS else 0x87654321)
        else:action(address,args,f['result']if command in BOOL_COMMANDS else 0x87654321,checks=[(CLOCK,bytes(clock))])
        if command in BOOL_COMMANDS and f['result']==0:result=2
    else:result=1
    group[472:476]=p32(0);action(REPLY,[command,result],checks=[(GROUP,bytes(group)),(CLOCK,bytes(clock))]);action(RECEIVE,[GROUP+4,SCRATCH,1],checks=[(GROUP,bytes(group)),(CLOCK,bytes(clock))],stop=True)
    return dict(args=[0xdeadbeef],initial=initial,regions={GROUP:bytes(group),CLOCK:bytes(clock)},actions=actions,allowedWriteRanges=[(GROUP+472,GROUP+476)],frame=40,normalReturnsExpected=0,boundedIterationsExpected=1)
