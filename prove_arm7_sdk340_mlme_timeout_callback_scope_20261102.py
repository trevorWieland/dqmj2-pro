import hashlib
import gzip
import itertools
import json
import struct
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import arm7_sdk306_task_command_context_20261102 as context
import link_arm7_bulk_20261030 as strict
from project import ROOT,sha256,write_json,configuration

ENTRIES=[dict(name='MLME_ScanTimeOut',address=0x027ed410,bytes=100,instructionBytes=92,task=0,parent=0x027ed220,parentBytes=496),dict(name='MLME_JoinTimeOut',address=0x027ed514,bytes=60,instructionBytes=52,task=1,parent=0x027ed474,parentBytes=160),dict(name='MLME_MeasChanTimeOut',address=0x027edad4,bytes=44,instructionBytes=36,task=5,parent=0x027ed864,parentBytes=624)]

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
def gethalf(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def getword(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def setup(main,wram,case,index):
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset']);base=meta['context'];req=context.base.DATA+0x5200
    cpu.mem_write(req,bytes(160));word(cpu,base+0x41c,req);half(cpu,base+0x404,case['state']);half(cpu,base+0x408,case['seed']);half(cpu,base+0x40a,case['channel']);half(cpu,base+0x40e,case['elapsed']);half(cpu,base+0x410,case['period']);half(cpu,req+0x4a,case['maximum']);return cpu,meta

def execute(main,wram,entry,case,index):
    cpu,meta=setup(main,wram,case,index);base=meta['context'];original=context.task_state(cpu,base);stores=[];called=[];visited=[]
    def write(machine,access,a,width,value,user):
        if not context.base.STACK<=a<context.base.STACK+0x4000:stores.append([a,width,value&((1<<(8*width))-1)])
    def code(machine,pc,width,user):
        if entry['address']<=pc<entry['address']+entry['instructionBytes']:visited.append(pc)
        if pc==0x037f8598:called.append([machine.reg_read(REGISTERS[0]),machine.reg_read(REGISTERS[1])])
    hooks=[cpu.hook_add(UC_HOOK_MEM_WRITE,write),cpu.hook_add(UC_HOOK_CODE,code)]
    try:result=context.base.call(cpu,entry['address'],[case['argument']],10000)
    finally:
        for h in hooks:cpu.hook_del(h)
    expected=[];state=case['state']
    if entry['task']==0:
        elapsed=(case['elapsed']+case['period'])&65535;expected.append([base+0x40e,2,elapsed])
        if elapsed>=case['maximum']:state=17 if case['channel']<16 else 21;expected.append([base+0x404,2,state])
    elif entry['task']==1:expected.extend([[base+0x408,2,7],[base+0x404,2,37]]);state=37
    else:expected.append([base+0x404,2,131]);state=131
    reference,rmeta=setup(main,wram,case,index)
    for a,width,value in expected:reference.mem_write(a,value.to_bytes(width,'little'))
    api=context.base.call(reference,0x037f8598,[2,entry['task']],10000)
    same=all(bytes(cpu.mem_read(a,n))==bytes(reference.mem_read(a,n))for a,n in meta['regions'].items()if a!=context.base.STACK)
    task=context.task_state(cpu,base);checks=dict(actualCallbackReturn=result['actualReturn'],actualTailApiReturn=api['actualReturn'],orderedOwnWrites=stores[:len(expected)]==expected,independentAllNonstackMemory=same,forwardedTask=called==[[2,entry['task']]],state=gethalf(cpu,base+0x404)==state,actualEnqueuedSlot=task['slots'][entry['task']]['flag']==1,originalTaskGraphInitialized=original['slots'][entry['task']]['flag']==0)
    if not all(checks.values()):raise ValueError(dict(entry=entry['name'],case=case,checks=checks,stores=stores,expected=expected,task=task))
    return dict(case=case,checks=checks,passed=True,actualOwnReturn=result,independentTailApiReturn=api,visited=sorted(set(visited)),orderedNonstackStores=stores,expectedOwnStores=expected,taskState=task,setupReturns=len(meta['prerequisiteReturns'])+len(rmeta['prerequisiteReturns']),sourceCredit=0)

def boundaries(main,wram):
    inventory=ROOT/'evidence/arm7/ghidra-runtime-inventory.json';rows=json.loads(inventory.read_text())['functions'];unused,functions=strict.namespace('');out=[]
    for entry in ENTRIES:
        a=entry['address'];end=a+entry['bytes'];raw=main[a-context.base.MAIN:end-context.base.MAIN];overlaps=[r for r in rows if r['module']=='arm7-main'and int(r['minimumAddress'],0)<end and int(r['maximumAddress'],0)>=a]
        if overlaps or a in functions:raise ValueError('New complete callback overlap/default canonical refusal differs')
        literals=list(struct.unpack('<II',raw[entry['instructionBytes']:]))
        if literals!=[context.base.WORD,0x037f8598]:raise ValueError('Exact data-word and existing tail API literals required')
        refs=[];pointers=[]
        for module,binary,origin in [('arm7-main',main,context.base.MAIN),('arm7-wram',wram,context.base.WRAM)]:
            for off in range(0,len(binary)-3,4):
                w=struct.unpack_from('<I',binary,off)[0];pc=origin+off
                if a<=w<end:pointers.append(dict(module=module,address=hex(pc),target=hex(w),kind='aligned-word-candidate'))
                if w&0x0e000000==0x0a000000 and w>>28!=15:
                    delta=(w&0xffffff)<<2
                    if delta&0x02000000:delta-=0x04000000
                    target=(pc+8+delta)&0xffffffff
                    if a<=target<end:refs.append(dict(module=module,address=hex(pc),target=hex(target),insideOwnInstructions=a<=pc<a+entry['instructionBytes']))
        if any(not r['insideOwnInstructions']and int(r['target'],0)!=a for r in refs):raise ValueError('Unreconciled outside ARM candidate into callback interior')
        out.append(dict(entry,processor='arm7',program='',module='arm7-main',mode='arm',address=hex(a),targetSha256=hashlib.sha256(raw).hexdigest(),instructionSha256=hashlib.sha256(raw[:entry['instructionBytes']]).hexdigest(),literalBytes=8,literalWords=[hex(v)for v in literals],configuredOverlaps=overlaps,defaultCanonicalEntryAbsent=True,alignedArmBranchCandidates=refs,alignedPointerCandidates=pointers,parentSha256=hashlib.sha256(main[entry['parent']-context.base.MAIN:entry['parent']-context.base.MAIN+entry['parentBytes']]).hexdigest()))
    return out,dict(path=inventory.relative_to(ROOT).as_posix(),sha256=sha256(inventory))

def main():
    if sha256(configuration()['rom'])!='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':raise ValueError('Original ROM identity changed')
    mainpath=ROOT/'extract/arm7/runtime/arm7-main.bin';wrampath=ROOT/'extract/arm7/runtime/arm7-wram.bin';main=mainpath.read_bytes();wram=wrampath.read_bytes();scope,inventory=boundaries(main,wram);results=[]
    for entry in ENTRIES:
        if entry['task']==0:domains=itertools.product((0,1,65535),(0,1,65535),(0,1,65535),(0,15,16,65535),(0,2),(0,4))
        else:domains=itertools.product((0,1,65535),(0,2),(0,4),(0,1,0xffffffff))
        own=[]
        for values in domains:
            if entry['task']==0:elapsed,period,maximum,channel,mode,offset=values;seed=0x5555;argument=(len(own)*0x1234567)&0xffffffff
            else:seed,mode,offset,argument=values;elapsed=1;period=1;maximum=1;channel=0
            case=dict(elapsed=elapsed,period=period,maximum=maximum,channel=channel,mode=mode,offset=offset,seed=seed,argument=argument,state=0x13 if entry['task']==0 else 0xffff);own.append(execute(main,wram,entry,case,len(own)))
        results.append(dict(name=entry['name'],address=hex(entry['address']),actualOwnReturns=len(own),actualSeparateApiReturns=len(own),actualSetupReturns=sum(r['setupReturns']for r in own),cases=own,allPassed=True));print(entry['name']+': '+str(len(own))+' native callback returns',flush=True)
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0);trace=ROOT/'work/arm7-bulk-20261030/sdk340-mlme-timeout-scope/native-cases.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(compressed);summaries=[{k:v for k,v in r.items()if k!='cases'}for r in results]
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',inputMainSha256=sha256(mainpath),inputWramSha256=sha256(wrampath),inventory=inventory,scope=scope,results=summaries,nativeTrace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=hashlib.sha256(compressed).hexdigest(),rawSha256=hashlib.sha256(raw).hexdigest()),totalActualOwnReturns=sum(r['actualOwnReturns']for r in results),totalActualIndependentApiReturns=sum(r['actualSeparateApiReturns']for r in results),contextGenerator=dict(path=Path(context.__file__).name,sha256=sha256(context.__file__)),sourceCredit=0,denominatorIncrease=0,providers=[],prefixBoundaryNormalReturnCredit=0,limits=['Aligned ARM/word scan does not exclude arbitrary indirect or unaligned references','Direct synthetic callback execution proves isolated field/task effects only; actual alarm installation and launch remain separate','No source/linker namespace/configuration or shared registry changed','Current complete context view extent does not prove original physical allocation extent']);write_json(ROOT/'evidence/attempts/arm7-sdk340-mlme-timeout-callback-scope-20261102.json',report);print(json.dumps(dict(actualOwnReturns=report['totalActualOwnReturns'],sourceCredit=0)),flush=True)

if __name__=='__main__':main()
