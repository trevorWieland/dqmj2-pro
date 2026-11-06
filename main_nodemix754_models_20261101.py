import itertools
import struct
import main_nodemix754_machine_20261101 as M

def profiles():
    result=[]
    def add(indices,weights,cached,queue):
        seed=len(result);mask=[0,0]
        for index in cached:mask[index//32]|=1<<(index%32)
        matrix=lambda count,tag:[(-1 if(i+tag+seed)%2 else 1)*(1024+((i*977+tag*313+seed*11)%16000))for i in range(count)]
        result.append(dict(name=f'nodemix-{seed}',seed=seed,opcode=[9,255][seed%2],destination=[0,1,31][seed%3],entries=[[i%32,index,weight]for i,(index,weight)in enumerate(zip(indices,weights))],cachedWords=mask,cache=[matrix(25,index)for index in range(64)],inverse=[matrix(21,index+128)for index in range(64)],clip=matrix(16,256),normal=matrix(9,512),queueEnabled=seed%3!=0,queue=queue,ignoredWord=[0,1,0x80000000,0xFFFFFFFF][seed%4]))
    for index,weight,cached in itertools.product([0,1,31,32,63],[0,1,128,255],[False,True]):add([index],[weight],[index]if cached else[],[])
    for indices in[[0,0],[31,32],[63,63],[0,63]]:
        for mask in[[],indices[:1],indices]:add(indices,[1,255],mask,[0x12345678,0xFFFFFFFF,0])
    for count,pattern in itertools.product([3,8,16,64],[0,1,2]):
        indices=[[0,31,32,63][i%4]for i in range(count)];add(indices,[[0,1,128,255][(i+pattern)%4]for i in range(count)],[]if pattern==0 else set(indices)if pattern==1 else[0,32],[0x75000000+i for i in range(pattern*4)])
    return result

def model(result):
    p=result['profile'];expected=bytearray(result['before']);io=bytearray(result['ioBefore']);writes=[];cache=[row[:]for row in p['cache']];mask=p['cachedWords'][:];sumM=[0]*12;sumN=[0]*9;uncached=[]
    def put(address,value):
        word=value&0xFFFFFFFF;target,base=(io,M.IO)if address>=M.IO else(expected,M.BASE);target[address-base:address-base+4]=struct.pack('<I',word);writes.append([address,4,word])
    def send(command,words,increment=False):
        put(M.IO+0x400,command)
        for index,value in enumerate(words):put(M.IO+0x400+(index*4 if increment else(index%3)*4),value)
    if p['queueEnabled']and p['queue']:
        for word in p['queue']:put(M.IO+0x400,word)
        put(M.QUEUE,0)
    put(M.IO+0x440,0);put(M.IO+0x44C,1);put(M.IO+0x454,0);put(M.IO+0x440,2)
    for slot,index,byteWeight in p['entries']:
        present=bool(mask[index//32]&(1<<(index%32)))
        if not present:
            uncached.append(index);mask[index//32]|=1<<(index%32);put(M.RS+0xCC+4*(index//32),mask[index//32]);put(M.IO+0x450,slot);put(M.IO+0x440,1);send(0x19,p['inverse'][index][:12])
            cache[index][:16]=p['clip']
            for n,word in enumerate(p['clip']):put(M.CACHE+index*100+n*4,word)
            put(M.IO+0x440,2);send(0x1A,p['inverse'][index][12:],True)
            cache[index][16:]=p['normal']
            for n,word in enumerate(p['normal']):put(M.CACHE+index*100+64+n*4,word)
        weight=byteWeight*16;matrix=cache[index]
        for n,source in enumerate([0,1,2,4,5,6,8,9,10,12,13,14]):sumM[n]+=(weight*matrix[source])//4096
        for n,word in enumerate(matrix[16:]):sumN[n]+=(weight*word)//4096
    for word in sumM+sumN:
        if not -2147483648<=word<=2147483647:raise ValueError('754 independent signed32 sum outside supported domain')
    send(0x17,sumN+result['initialRegisters'][4:7]);put(M.IO+0x440,1);send(0x17,sumM);put(M.IO+0x440,0);put(M.IO+0x450,1);put(M.IO+0x440,2);put(M.IO+0x44C,p['destination']);put(M.RS,M.COMMAND+3+len(p['entries'])*3)
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]or io!=result['ioAfter']:raise ValueError(('754 complete nonstack/MMIO-shadow model differs',p['name']))
    if[row[1:]for row in result['nonstackWrites']]!=writes:raise ValueError(('754 ordered physical writes differ',p['name']))
    matrices=[row['matrixWordsAtEntry']for row in result['nativeCalls']if row['entry']==0x0200434C]
    if matrices!=[sumN+[(word+2147483648)%4294967296-2147483648 for word in result['initialRegisters'][4:7]],sumM]:raise ValueError('754 final matrix payload differs')
    if result['coreRegistersAndCpsr'][0]!=M.RS:raise ValueError('754 physical nonsemantic R0 differs')
    entries=[row['entry']for row in result['nativeCalls']]
    expectedCalls=[0x02008C58,0x0202E300]+([0x02008C40]if p['queueEnabled']and p['queue']else[])
    for index in uncached:expectedCalls.extend([0x02004368,0x02005994,0x02004668,0x02008D4C,0x02004384,0x02008D0C,0x02004698,0x02008D0C])
    expectedCalls.extend([0x0200434C,0x02005994,0x0200434C,0x02005994])
    if entries!=expectedCalls:raise ValueError(('754 native call sequence differs',entries,expectedCalls))
    return dict(sumM=sumM,sumN=sumN,uncachedIndices=uncached,actualNativeReturnInstructions=len(result['actualNativeReturnEvents']),completedNativeEntries=sum(len(row['completedNativeEntries'])for row in result['actualNativeReturnEvents']),orderedPhysicalWrites=len(writes),matrixNTrailingWords=result['initialRegisters'][4:7],completeNonstackAndIoShadowModel=True)
