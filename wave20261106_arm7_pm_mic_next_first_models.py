import struct
SP=0x027fc000
STOP=0x02010000
WORK=0x0380b258
SYSTEM=0x027ffc00
TIMER_L=0x0400010c
TIMER_H=TIMER_L+2


def p16(n):return struct.pack('<H',n&65535)
def p32(n):return struct.pack('<I',n&0xffffffff)


def fixtures():
    rows=[dict(entry=0x038053d0,kind='initialize',word=value)for value in [0,0x80,0xffff,0x1234]]
    def receive(**fields):
        value=dict(entry=0x03805418,kind='receive',command=0x41,type=3,state=0,start=False,end=True,index=0,buffer=0x02010000,size=0x1234,rate=0x10203040,timer=True,queued=True);value.update(fields);rows.append(value)
    for command in [0x40,0x41,0x42,0x43,0xff]:
        for state in [0,1,2,3,4,0xffffffff]:receive(command=command,state=state)
    for command in [0x40,0x41]:
        for queued in [False,True]:
            for start in [False,True]:receive(command=command,queued=queued,start=start)
    for address in [0x01ffffff,0x02000000,0x023fffff,0x02400000]:receive(buffer=address,size=1)
    for size in [0,0x003f0000,0x003f0001,0xffffffff]:receive(size=size)
    for command in [0x41,0x42,0x43]:
        for value in [False,True]:receive(command=command,state=0 if command==0x41 else 2,timer=value,queued=value)
    for index in [1,7,15]:receive(index=index,end=False)
    for typ in [0,1,2,3,0xffff]:receive(type=typ)
    for command in [0x40,0x41,0x42,0x43,0xffff0040]:
        for state in [0,1,2,3,4]:
            for available in [False,True]:rows.append(dict(entry=0x03805784,kind='execute',command=command,state=state,available=available,type=(state%4),sample=0xd3 if not(state%2)else 0xd3a5))
    return rows


def scenario(f,ordinal):
    initial={};regions={};actions=[];allowed=[];entry=f['entry'];frame={0x038053d0:0,0x03805418:8,0x03805784:16}[entry];state=bytearray((ordinal*13+i*7)&255 for i in range(60));sys=bytearray((ordinal*5+i*3)&255 for i in range(1024));timer_l=0x4567;timer_h=0xabcd
    def area(at,raw):initial[at]=bytes(raw);regions[at]=bytes(raw)
    def action(address,args=(),returned=0,checks=(),mutations=()):actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=list(checks),mutations=list(mutations)))
    def result(command,code):action(0x03803a48,[command&65535,code])
    def set16(offset,value):struct.pack_into('<H',state,offset,value&65535)
    def set32(offset,value):struct.pack_into('<I',state,offset,value&0xffffffff)
    def clear_system():sys[912:918]=bytes(6)
    def get16(offset):return int.from_bytes(state[offset:offset+2],'little')
    def get32(offset):return int.from_bytes(state[offset:offset+4],'little')
    allowed.extend([(WORK,WORK+60),(SYSTEM+912,SYSTEM+918),(TIMER_L,TIMER_H+2)])
    if f['kind']=='initialize':
        args=[];area(WORK,state);area(TIMER_H,p16(f['word']));state[0:36]=bytes(36);timer_h=f['word']&~0x80;regions[TIMER_H]=p16(timer_h)
    elif f['kind']=='receive':
        set32(32,f['state']);set16(0,(f['command']<<8)|(f['type']&255))
        for offset,value in [(2,f['buffer']>>16),(4,f['buffer']),(6,f['size']>>16),(8,f['size']),(10,f['rate']>>16),(12,f['rate'])]:set16(offset,value)
        area(WORK,state);area(SYSTEM,sys);area(TIMER_L,p16(timer_l));area(TIMER_H,p16(timer_h));data=(0x02000000 if f['start']else 0)|(0x01000000 if f['end']else 0)|(f['index']<<16)|((f['command']<<8)|(f['type']&255)if f['index']==0 else 0x7654);args=[data]
        if f['start']:state[0:32]=bytes(32)
        set16(f['index']*2,data);command=state[1]
        if f['end']:
            if command==0x40:
                action(0x03803b7c,[2,command,1,state[0]],int(f['queued']))
                if not f['queued']:result(command,4)
                clear_system()
            elif command==0x41:
                if get32(32)!=0:result(command,3)
                else:
                    set16(36,state[0]);buffer=(get16(2)<<16)|get16(4);size=(get16(6)<<16)|get16(8);rate=(get16(10)<<16)|get16(12)
                    if not 0x02000000<=buffer<0x02400000:result(command,2)
                    else:
                        set32(40,buffer)
                        if (buffer+size)&0xffffffff>0x02400000:result(command,2)
                        else:
                            set32(48,size);changes=[(WORK+52,p16(0x1234)+p16(2))]if f['timer']else[];action(0x038056e0,[rate],int(f['timer']),mutations=changes)
                            if not f['timer']:result(command,2)
                            else:
                                set16(52,0x1234);set16(54,2);set32(44,0);set16(38,get16(36)&7);action(0x03803b7c,[2,command,0],int(f['queued']))
                                if not f['queued']:result(command,4)
                                else:clear_system();set32(32,1)
            elif command==0x42:
                if get32(32)!=2:result(command,3)
                else:
                    action(0x03803b7c,[2,command,0],int(f['queued']))
                    if not f['queued']:result(command,4)
                    else:set32(32,3);timer_h&=~0x80
            elif command==0x43:
                if get32(32)!=2:result(command,3)
                else:
                    rate=(get16(2)<<16)|get16(4);action(0x038056e0,[rate],int(f['timer']),mutations=[(WORK+52,p16(0x1234)+p16(2))]if f['timer']else[])
                    if not f['timer']:result(command,2)
                    else:
                        set16(52,0x1234);set16(54,2);action(0x037fdd00,returned=0x60000080);timer_l=0x1234;timer_h=0xc2;action(0x037fdd14,[0x60000080],checks=[(TIMER_L,p16(timer_l)),(TIMER_H,p16(timer_h))]);result(command,0)
            else:result(command,1)
        regions[SYSTEM]=bytes(sys);regions[TIMER_L]=p16(timer_l);regions[TIMER_H]=p16(timer_h)
    elif f['kind']=='execute':
        args=[0x02710000];set32(32,f['state']);set16(52,0x2345);set16(54,3);area(WORK,state);area(SYSTEM,sys);area(TIMER_L,p16(timer_l));area(TIMER_H,p16(timer_h));area(args[0],struct.pack('<6I',0x12345678,f['command'],f['type'],0x89abcdef,0x31415926,0x27182818));command=f['command'];old_irq=0x60000080
        if command==0x40:
            action(0x037fdd00,returned=old_irq);action(0x03803b0c,[2],int(f['available']))
            if not f['available']:action(0x037fdd14,[old_irq]);result(command,4)
            else:
                action(0x03803b28,[2]);action(0x037fdd14,[old_irq]);is12=f['type']&1;sample=f['sample'];action(0x03805cd4 if is12 else 0x03805b80,returned=sample)
                if f['type']&2:sample^=0x8000 if is12 else 0x80
                struct.pack_into('<I',sys,912,0x027fff94);struct.pack_into('<H',sys,916,sample);result(command,0);action(0x03803b40,[2])
        elif command==0x41:
            if f['state']!=1:result(command,3)
            else:
                set16(56,0);set16(58,0);action(0x037fdd00,returned=old_irq);action(0x037fb8f0,[0x40]);action(0x03805e08,[0x40,0x038059ac]);action(0x03805e30);timer_l=0x2345;timer_h=0xc3;action(0x037fdd14,[old_irq],checks=[(TIMER_L,p16(timer_l)),(TIMER_H,p16(timer_h))]);result(command,0);set32(32,2)
        elif command==0x42:
            if f['state']not in [3,4]:result(0x51,3)
            else:
                timer_h&=~0x80;action(0x037fdd00,returned=old_irq,checks=[(TIMER_H,p16(timer_h))]);action(0x03805e08,[0x40,0]);action(0x03805e90);action(0x037fdd14,[old_irq]);result(0x42 if f['state']==3 else 0x51,0);set32(32,0)
        regions[SYSTEM]=bytes(sys);regions[TIMER_L]=p16(timer_l);regions[TIMER_H]=p16(timer_h)
    else:raise ValueError('Unknown MIC caller state machine')
    regions[WORK]=bytes(state)
    return dict(args=args,initial=initial,regions=regions,actions=actions,allowedWriteRanges=allowed,frame=frame,returnValue=None)
