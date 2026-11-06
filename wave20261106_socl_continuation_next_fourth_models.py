from wave20261105_socket_thumb_next_memory import Memory

CTX,OUT,INPUT,SP,STOP=0x02400000,0x02410000,0x02420000,0x027f0000,0x027d0000
SPECS={'020938b8':40,'02093930':16,'02093998':40,'02093a18':16,'02093a6c':8,'02093ac0':48,'02093b2c':24,'02093b7c':48}
NAMES=list(SPECS)


def fixtures(name):
    if name in ['020938b8','02093998']:items=[(0,0,'none',0),(1,1,'none',0),(4,0,'none',0),(4,2,'none',0),(4,3,'left',0),(4,4,'right',0)]
    elif name in ['02093930','02093a18']:items=[(0,0,'none',0),(-1,0,'none',1),(1,1,'none',65535),(4,2,'none',1),(4,4,'left',0),(4,4,'none',65535)]
    elif name=='02093a6c':items=[(0,0,'none',0),(-1,0,'none',0),(1,0,'none',0),(4,2,'none',0),(4,3,'none',0),(4,4,'none',0)]
    elif name=='02093ac0':items=[(0,0,'none',0),(1,1,'none',0),(4,0,'none',0),(4,2,'none',0),(4,4,'none',0),(4,4,'left',0)]
    elif name=='02093b2c':items=[(0,0,'none',0),(1,1,'none',65535),(4,0,'none',65535),(4,2,'none',1),(4,4,'left',65535)]
    else:items=[(0,0,'none',0),(1,1,'none',0),(4,0,'none',0),(4,4,'none',0),(4,5,'none',0),(4,6,'none',0),(3,4,'none',0)]
    if name=='020938b8':items.append((4,1,'none',0))
    if name=='02093930':items.append((4,1,'none',1))
    if name=='02093b2c':items.append((4,7,'none',65535))
    return [dict(digits=n,pattern=p,alias=a,scalar=s) for n,p,a,s in items]


def scenario(name,f,ordinal):
    memory=Memory({CTX:512,OUT:512,INPUT:512},ordinal);actions=[];n=f['digits'];extent=max(n,0);scalar=f['scalar'];result=None
    if f['pattern']==0:left=right=[0]*extent
    elif f['pattern']==1:left=right=[65535]*extent
    elif f['pattern']==2:left=[0]*extent;right=[1]+[0]*max(extent-1,0)
    elif f['pattern']==3:left=[1]+[0]*max(extent-1,0);right=[0]*max(extent-1,0)+[1]
    elif f['pattern'] in [5,6]:left=[65535 if f['pattern']==5 else 65534,32768+(f['pattern']-5)]+[0]*max(extent-2,0);right=[0]*extent
    elif f['pattern']==7:left=[65535]+[0]*max(extent-1,0);right=[0]*extent
    else:left=[(i*14713+19381)&65535 for i in range(extent)];right=[(i*3911+361)&65535 for i in range(extent)]
    for base,values in [(CTX,left),(INPUT,right)]:
        for i,value in enumerate(values[:extent]):memory.set(base+i*2,value,2)
    output=CTX if f['alias']=='left'else INPUT if f['alias']=='right'else OUT;initial=memory.snapshot()
    def integer(base):return sum(memory.get(base+2*i,2)<<(16*i) for i in range(extent))
    original_left,original_right=integer(CTX),integer(INPUT)
    def call(address,args,returned,mutations):
        checks=[(base,raw)for base,raw in memory.snapshot().items()];actions.append(dict(address=address,args=[a&0xffffffff for a in args],returned=returned,checks=checks,mutations=mutations,stackWords=[]))
        for base,raw in mutations:memory.put(base,raw)
    def count(base):
        answer=extent
        while answer and memory.get(base+2*(answer-1),2)==0:answer-=1
        call(0x2093874,[base,n],answer,[]);return answer
    def zero(base,amount):
        if amount<0 or amount>512:raise ValueError('Bounded zero provider span invalid')
        call(0x2008d78,[base,0,amount],0xa7000000+len(actions),[(base,bytes(amount))])
    def partial(term,index):
        changes=[];value=term
        while value and index<n:
            temporary=(memory.get(output+2*index,2)+value)&0xffffffff;changes.append((output+2*index,(temporary&65535).to_bytes(2,'little')));value=temporary>>16;index+=1
        call(0x2093aa0,[output,term,index-len(changes),n],0xa7000000+len(actions),changes)
    mathematical=None
    if name in ['020938b8','02093998']:
        used=max(count(CTX),count(INPUT));used+=used!=n;carry=index=0
        while index<used or (name=='02093998' and index<n and carry):
            a,b=memory.get(CTX+2*index,2),memory.get(INPUT+2*index,2);temporary=(a+b+carry if name=='020938b8'else a-b+carry)&0xffffffff;memory.set(output+2*index,temporary,2);carry=temporary>>16
            if name=='02093998' and carry&32768:carry-=65536
            index+=1
        if output not in [CTX,INPUT]:zero(output+index*2,(n-index)*2)
        mathematical=original_left+original_right if name=='020938b8'else original_left-original_right;args=[output,CTX,INPUT,n&0xffffffff]
    elif name in ['02093930','02093a18']:
        carry=scalar;index=0
        while index<n:
            current=memory.get(CTX+2*index,2);temporary=(current+carry if name=='02093930'else current-carry)&0xffffffff;memory.set(output+2*index,temporary,2);carry=temporary>>16
            if name=='02093a18':carry&=1
            if not carry:break
            index+=1
        if output!=CTX:
            index+=1
            while index<n:memory.set(output+2*index,memory.get(CTX+2*index,2),2);index+=1
        mathematical=original_left+scalar if name=='02093930'else original_left-scalar;args=[output,CTX,scalar,n&0xffffffff]
    elif name=='02093a6c':
        result=0
        for i in range(n-1,-1,-1):
            a,b=memory.get(CTX+2*i,2),memory.get(INPUT+2*i,2)
            if a!=b:result=1 if a>b else 0xffffffff;break
        if result!=(1 if original_left>original_right else 0xffffffff if original_left<original_right else 0):raise ValueError('Independent integer/word comparison models disagree')
        args=[CTX,INPUT,n&0xffffffff,0x33445566]
    elif name=='02093ac0':
        zero(output,n*2);left_count,right_count=count(CTX),count(INPUT)
        for j in range(right_count):
            for i in range(min(left_count,n-j)):partial(memory.get(CTX+2*i,2)*memory.get(INPUT+2*j,2),j+i)
        if output not in [CTX,INPUT]:mathematical=original_left*original_right
        args=[output,CTX,INPUT,n&0xffffffff]
    elif name=='02093b2c':
        used=count(CTX);carry=0
        for i in range(used):
            temporary=(memory.get(CTX+2*i,2)*scalar+carry)&0xffffffff;memory.set(output+2*i,temporary,2);carry=temporary>>16
        index=used
        if index<n:memory.set(output+2*index,carry,2);index+=1
        zero(output+2*index,(n-index)*2);mathematical=original_left*scalar;args=[output,CTX,scalar,n&0xffffffff]
    else:
        used=count(CTX)
        if 2*used<n:zero(output+4*used,(n-2*used)*2)
        for i in range(used):
            index=i*2
            if index>=n:break
            temporary=memory.get(CTX+2*i,2)**2;memory.set(output+2*index,temporary,2)
            if index==n-1:break
            memory.set(output+2*index+2,temporary>>16,2)
        for i in range(used):
            for j in range(i+1,min(used,n-i)):
                product=memory.get(CTX+2*j,2)*memory.get(CTX+2*i,2)
                if product<=0x7fff8000:partial(product*2,i+j)
                else:partial(product,i+j);partial(product,i+j)
        mathematical=original_left**2;args=[output,CTX,n&0xffffffff,0x33445566]
    if mathematical is not None and n>=0:
        mask=(1<<(16*n))-1
        if integer(output)!=(mathematical&mask):raise ValueError(('Independent scalar integer/word-array models disagree',name,f))
    return dict(initial=initial,regions=memory.snapshot(),args=args,actions=actions,result=result,volatileStateReads=None,readable=[(CTX,512),(INPUT,512),(OUT,512)],output=output,outputBytes=extent*2)
