from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
HISTORY=0x03809ea8
SPI_CNT=0x040001c0
SPI_DATA=0x040001c2
KEY=0x04000136


def fixtures():
    rows=[dict(entry=0x038043a4,history=history,key1=first,key2=second,busy=busy)for history in[0,1,2,65535]for first,second in[(0xa5bf,0xa5ff),(0xa5ff,0xa5bf),(0xa5ff,0xa5ff)]for busy in[0,1]]
    rows.extend([dict(entry=0x038043a4,history=0,key1=0xa5ff,key2=0xa5bf,busy=1,historyUpdate=1),dict(entry=0x038043a4,history=1,key1=0xa5ff,key2=0xa5ff,busy=0,historyUpdate=0)])
    rows.extend(dict(entry=0x038046ac,first=0,second=0,range=distance,raw=raw,x=0,y=0,dx=0,dy=0,xvalid=0,yvalid=0)for raw in[0,0xffffffff,0xdeadbeef]for distance in[-7,0,65535])
    rows.extend(dict(entry=0x038046ac,first=first,second=second,range=distance,raw=0xdeadbeef,x=x,y=y,dx=dx,dy=dy,xvalid=xv,yvalid=yv)for first in[1,2]for second in[0,1,2]for distance in[-7,0]for x,y,dx,dy,xv,yv in[(0x1234,0xabcd,31,63,0,0),(65535,4096,99,8,1,2),(4095,17,0,0,3,3),(1,2,65535,65535,2,1)])
    return rows


def scenario(f,ordinal):
    p=Plan(ordinal,8 if f['entry']==0x038043a4 else 32);p.buffer(HISTORY,8,0xaa);p.write(HISTORY,p16(f.get('history',0xa5a5))+bytes.fromhex('887766554433'));p.constant(SPI_CNT,p16(0));p.constant(SPI_DATA,p16(0x7777));p.constant(KEY,p16(0x7777));p.allowed.extend([(HISTORY,HISTORY+2),(SPI_CNT,SPI_CNT+2),(SPI_DATA,SPI_DATA+2)]);script=[];historyReads=[]
    if f['entry']==0x038046ac:p.args=[OUT,f['range']&0xffffffff,CFM];p.u32(OUT,f['raw']);p.buffer(SP-32,8,0xa5);p.allowed.extend([(OUT,OUT+4),(CFM,CFM+2)])
    p.capture()
    if f['entry']==0x038043a4:
        p.action(0x037fe5a8,[0x8000])
        def wait(control):
            script.extend([(SPI_CNT,2,control|128)]*f['busy']);script.append((SPI_CNT,2,control))
        def burst(initial):
            if initial:wait(0)
            p.mmio.extend([(SPI_CNT,2,0x8a01),(SPI_DATA,2,0x84)]);wait(0x8a01);changes=[]
            if initial and'historyUpdate'in f:changes=[(HISTORY,p16(f['historyUpdate']))];p.u16(HISTORY,f['historyUpdate'])
            p.action(0x03804498,checks=[(SPI_CNT,p16(0x8a01))],mutations=changes);p.mmio.append((SPI_CNT,2,0x8201));p.action(0x03804498,checks=[(SPI_CNT,p16(0x8201))])
        burst(True);historyReads=[(HISTORY,2,p.r16(HISTORY))];script.append((KEY,2,f['key1']));key=f['key1'];p.returned=0 if key&64 else 1
        if p.r16(HISTORY)and key&64:burst(False);key=f['key2'];script.append((KEY,2,key));p.returned=0 if key&64 else 2
        p.regions[SPI_CNT]=p16(0x8201);p.regions[SPI_DATA]=p16(0x84);p.regions[KEY]=p16(key)
    else:
        p.u16(CFM,0);p.action(0x038043a4,[],f['first'],checks=[(CFM,p16(0))]);raw=f['raw']
        if f['first']==0:p.u32(OUT,(raw&0xf8000000)|0x06000000);p.u16(HISTORY,0)
        else:
            local=SP-32;position=local+4;rangeWord=abs(f['range'])&0xffffffff;p.action(0x038044bc,[position,rangeWord,0,local+2],f['xvalid'],checks=[(OUT,p32(raw))],mutations=[(position,p16(f['x'])),(local+2,p16(f['dx']))]);p.u16(position,f['x']);p.u16(local+2,f['dx']);raw=(raw&~0x06000fff)|((f['xvalid']&3)<<25)|(f['x']&4095)
            p.action(0x038044bc,[position,rangeWord,1,local],f['yvalid'],checks=[(OUT,p32(raw)),(position,p16(f['x'])),(local+2,p16(f['dx']))],mutations=[(position,p16(f['y'])),(local,p16(f['dy']))]);p.u16(position,f['y']);p.u16(local,f['dy'])
            if f['yvalid']==2:raw|=0x04000000
            raw=(raw&~0x00fff000)|((f['y']&4095)<<12);p.mmio.append((SPI_CNT,2,0x8a01))
            for i in range(12):p.action(0x03804498,checks=[(SPI_CNT,p16(0x8a01))])
            p.mmio.append((SPI_CNT,2,0x8201));p.action(0x03804498,checks=[(SPI_CNT,p16(0x8201))])
            if f['first']==2:raw|=0x06000000
            p.action(0x038043a4,[],f['second'],checks=[(OUT,p32(raw)),(CFM,p16(0))]);raw=(raw&~0x01000000)|(0x01000000 if f['second']else 0);p.u16(HISTORY,1 if f['second']==1 else 0)
            if f['second']==2:raw|=0x06000000
            if f['second']==1:p.u16(CFM,max(f['dx'],f['dy']))
            p.u32(OUT,raw);p.regions[SPI_CNT]=p16(0x8201)
    result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=list(script),faultRegisters=[],spiReadScript=script,scriptedReadAddresses=[SPI_CNT,SPI_DATA,KEY],expectedHistoryReads=historyReads,instructionBudget=20000);return result
