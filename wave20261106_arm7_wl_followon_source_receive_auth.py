from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,CTX,FRAME,REQ,CFM,OUT,p16


def fixtures():
    base=dict(entry=0x027f35cc,mode=1,algo=0,seq=1,status=0,cam=1,oldState=32,challengeState=32,authConfig=0,seed=0x1234,mlme=0x31,requestAlgo=0,peer=True,duplicate=False,allocated=True,badIcv=False,length=5,challengeGood=True,oddHigh=False,hardware=False,txmap=0,busy0=0,busy1=0,busy2=0,rxBusy=0,random=0x1234)
    rows=[base]
    for overrides in [dict(duplicate=True),dict(cam=0),dict(cam=0,seq=65535,allocated=False),dict(oldState=64),dict(authConfig=1),dict(seq=0),dict(seq=2),dict(seq=65535),dict(badIcv=True),dict(algo=1,seq=1),dict(algo=1,seq=1,random=0),dict(algo=1,seq=1,allocated=False),dict(algo=1,seq=2),dict(algo=9),dict(algo=1,seq=3,challengeState=64),dict(algo=1,seq=3,seed=0)]:rows.append({**base,**overrides})
    for length in [0,1,4,5,128]:
        for good in [True,False]:
            if length==0 and not good:continue
            rows.append({**base,'algo':1,'seq':3,'length':length,'challengeGood':good})
    rows.append({**base,'algo':1,'seq':3,'length':5,'oddHigh':True})
    for overrides in [dict(mode=2,seq=2),dict(mode=2,seq=2,status=15),dict(mode=2,seq=2,peer=False),dict(mode=2,seq=2,requestAlgo=1),dict(mode=2,seq=2,mlme=0x30),dict(mode=2,seq=3),dict(mode=2,algo=9),dict(mode=2,algo=1,requestAlgo=1,seq=2,status=15),dict(mode=2,algo=1,requestAlgo=1,seq=2),dict(mode=2,algo=1,requestAlgo=1,seq=2,allocated=False),dict(mode=2,algo=1,requestAlgo=1,seq=4,mlme=0x33),dict(mode=2,algo=1,requestAlgo=1,seq=4,mlme=0x33,status=15),dict(mode=2,algo=1,requestAlgo=1,seq=4,mlme=0x31),dict(mode=2,algo=1,requestAlgo=0,seq=2),dict(mode=2,algo=1,requestAlgo=1,peer=False,seq=2)]:rows.append({**base,**overrides})
    for overrides in [dict(txmap=0),dict(txmap=1,busy0=1),dict(txmap=4,busy1=1),dict(txmap=8,busy2=1),dict(rxBusy=1),dict(txmap=13)]:rows.append({**base,'hardware':True,'duplicate':True,**overrides})
    return rows


def random_word(index):return (0x8123+0x1111*index)&65535


def scenario(f,ordinal):
    p=Plan(ordinal,40);p.args=[FRAME];p.u16(CTX+848,f['mode']);p.u16(CTX+818,f['authConfig']);p.u16(CTX+1028,f['mlme']);p.u32(CTX+1052,REQ);p.u32(CTX+1056,CFM);p.u16(REQ+22,f['requestAlgo']);peer=b'ABCDEF';p.write(REQ+16,peer);p.write(FRAME+30,peer if f['peer']else b'123456');p.u16(FRAME+2,f['cam']);p.u16(FRAME+6,8+f['length']);p.u16(FRAME+8,0x400 if f['badIcv']else 0);p.u16(FRAME+44,f['algo']);p.u16(FRAME+46,f['seq']);p.u16(FRAME+48,f['status']);p.write(FRAME+50,bytes([16,f['length']]));p.u16(CTX+1680,8 if f['hardware']else 0);p.u16(CTX+1068,f['busy0']);p.u16(CTX+1088,f['busy1']);p.u16(CTX+1108,f['busy2']);p.u16(CTX+1246,0x77ff);p.constant(0x048080b0,p16(f['txmap']));p.constant(0x0480819c,p16(f['rxBusy']));p.constant(0x04808032,p16(0x5a5a));p.constant(0x04808044,p16(f['random']))
    for i in range((f['length']+1)//2):p.u16(FRAME+52+2*i,random_word(i))
    if not f['challengeGood']and f['length']:
        index=(f['length']-1)//2;p.u16(FRAME+52+index*2,random_word(index)^1)
    if f['oddHigh']:p.u16(FRAME+52+(f['length']//2)*2,random_word(f['length']//2)^0xff00)
    p.capture();p.allowed.extend([(CTX+1028,CTX+1030),(CTX+1246,CTX+1248),(CTX+844,CTX+846),(FRAME+44,FRAME+46),(CFM+4,CFM+8),(OUT,OUT+512),(0x04808032,0x04808034)])
    if f['hardware']:
        clear=not(f['txmap']&1 and f['busy0'])and not(f['txmap']&4 and f['busy1'])and not(f['txmap']&8 and f['busy2'])and not f['rxBusy']&1
        if clear:p.u16(CTX+1246,0);p.regions[0x04808032]=p16(0x8000);p.mmio=[(0x04808032,2,0),(0x04808032,2,0x8000)]
    p.action(0x027f2000,[FRAME+30,0xb0],int(f['duplicate']))
    if f['duplicate']:return p.finish()
    def sta(value):p.u16(CTX+844,value);p.action(0x037f9238,[value],mutations=[(CTX+844,p16(value))])
    def factory(length,check):
        mutations=[]
        if f['allocated']:p.u16(OUT+20,0xb0);p.write(OUT+51,bytes([length]));mutations=[(OUT+20,p16(0xb0)),(OUT+51,bytes([length]))]
        p.action(0x027f1e08,[FRAME+30,length,check],OUT if f['allocated']else 0,mutations=mutations);return f['allocated']
    def send(algo,seq,status):p.u16(OUT+44,algo);p.u16(OUT+46,seq);p.u16(OUT+48,status);p.action(0x027f1088,[OUT],checks=[(OUT+44,p.read(OUT+44,6))])
    def common(status,seq):
        if factory(0,int(status!=0)):send(p.r16(FRAME+44),seq,status)
    def complete():
        p.action(0x027eabec)
        if f['status']==0:sta(48);p.u16(CFM+4,0);p.u16(CFM+6,0)
        else:p.u16(CFM+4,12);p.u16(CFM+6,f['status'])
        p.u16(CTX+1028,0x35);p.action(0x037f8598,[2,2],checks=[(CFM+4,p.read(CFM+4,4)),(CTX+1028,p16(0x35))])
    seq=(f['seq']+1)&65535
    if f['cam']==0:common(19,seq);return p.finish()
    if f['mode']==1:
        p.action(0x027ebfec,[f['cam']],f['oldState'])
        if f['oldState']>32:p.action(0x027ebc50,[f['cam'],32]);p.action(0x027edbf0,[FRAME+30,1])
        if f['badIcv']:
            p.action(0x027ec06c,[f['cam']],f['seed'])
            if f['seed']:p.u16(FRAME+44,1);p.action(0x027ebe78,[f['cam'],0]);common(15,4);return p.finish()
    if f['algo']==0:
        if f['mode']==1:
            if f['authConfig']==1:common(13,seq)
            elif f['seq']==1:common(0,seq)
            else:common(14,2)
        elif f['seq']==2 and f['requestAlgo']==0:
            p.action(0x027ea480,[REQ+16,FRAME+30],int(f['peer']))
            if f['peer']and f['mlme']==0x31:complete()
    elif f['algo']==1:
        if f['mode']==1:
            p.action(0x027ebc50,[f['cam'],32])
            if f['seq']==1:
                if factory(128,1):
                    p.u16(OUT+44,1);p.u16(OUT+46,seq);p.u16(OUT+48,0);seed=(f['random']+(f['random']<<8))&65535;seed=seed or 1;p.action(0x027eadac,[seed]);p.action(0x027ebe78,[f['cam'],seed]);length=p.byte_read(OUT+51)
                    for i in range(0,length,2):value=random_word(i//2);p.action(0x027eadc4,returned=value);p.u16(OUT+52+i,value)
                    p.action(0x027f1088,[OUT],checks=[(OUT+44,p.read(OUT+44,8+length))])
            elif f['seq']==3:
                p.action(0x027ebfec,[f['cam']],f['challengeState'])
                if f['challengeState']!=32:common(1,seq)
                else:
                    p.action(0x027ec06c,[f['cam']],f['seed'])
                    if not f['seed']:common(1,seq)
                    else:
                        p.action(0x027ec06c,[f['cam']],f['seed']);p.action(0x027eadac,[f['seed']]);length=p.byte_read(FRAME+51);matched=True
                        for i in range(length//2):
                            expected=random_word(i);p.action(0x027eadc4,returned=expected)
                            if p.r16(FRAME+52+2*i)!=expected:matched=False;break
                        if matched and length&1:
                            expected=random_word(length//2);p.action(0x027eadc4,returned=expected);matched=p.r16(FRAME+52+2*(length//2))&255==expected&255
                        p.action(0x027ebe78,[f['cam'],0]);common(0 if matched else 15,seq)
            else:p.action(0x027ebe78,[f['cam'],0]);common(14,2)
        elif f['requestAlgo']==1:
            p.action(0x027ea480,[REQ+16,FRAME+30],int(f['peer']))
            if f['peer']:
                if f['seq']==2 and f['mlme']==0x31:
                    if f['status']:
                        p.action(0x027eabec);p.u16(CTX+1028,0x35);p.u16(CFM+4,12);p.u16(CFM+6,f['status']);p.action(0x037f8598,[2,2]);sta(32)
                    else:
                        p.u16(CTX+1028,0x33);length=p.byte_read(FRAME+51)
                        if factory(length,1):p.u16(OUT+20,0x40b0);p.copy16(FRAME+44,OUT+44,9+f['length']);send(1,3,0)
                elif f['seq']==4 and f['mlme']==0x33:complete()
    elif f['mode']==1:common(13,seq)
    return p.finish()
