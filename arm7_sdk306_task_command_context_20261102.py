import hashlib
import struct
import match_runtime
import arm7_sdk288_transmit_context_20261102 as base

TASK_TABLE=0x027f7248
TASK_TABLE_SHA='75e8f18186e1059a463ce9343e360790cfa5482181b90de3c2df2cf0147d16f7'
RECV=base.DATA+0x6500
SEND=base.DATA+0x6400

def setup(main,wram,index,mode=0,offset=0,initialize_tasks=True,heap=False,bodies=None,capacity=16):
    if hashlib.sha256(main[TASK_TABLE-base.MAIN:TASK_TABLE-base.MAIN+96]).hexdigest()!=TASK_TABLE_SHA:raise ValueError('Complete24-entry initialized task-pointer table changed')
    cpu,meta=base.setup(main,wram,index,mode,context_offset=offset);context=meta['context'];meta['sourceLinkedProducers']=[]
    for entry,body in(bodies or{}).items():
        original=main if base.MAIN<=entry<base.MAIN+len(main)else wram;origin=base.MAIN if original is main else base.WRAM
        if original[entry-origin:entry-origin+len(body)]!=body:raise ValueError('Source-linked producer must match its full original range')
        cpu.mem_write(entry,body);meta['sourceLinkedProducers'].append(dict(entry=hex(entry),bytes=len(body),sha256=hashlib.sha256(body).hexdigest()))
    meta['prerequisiteReturns'].append(dict(name='actual-receive-queue-initializer',**base.call(cpu,0x037fc6ac,[RECV,base.DATA+0x6900,capacity])))
    cpu.mem_write(context+0x308,struct.pack('<I',RECV));meta['syntheticBeforeEntryBindings']=[dict(field='context+0x308',address=hex(context+0x308),value=hex(RECV),meaning='Measured receive-queue pointer field, backed by original queue initialization; enclosing native binder unproved')]
    if initialize_tasks:meta['prerequisiteReturns'].append(dict(name='actual-task-initializer',sourceLinked=0x027e8bd0 in(bodies or{}),**base.call(cpu,0x027e8bd0)))
    if heap:
        for name,entry,args in [('os-heap-init',0x037fce24,[0,base.DATA+0x7400,base.DATA+0x8000,1]),('os-heap-create',0x037fcecc,[0,base.DATA+0x7800,base.DATA+0x8000]),('os-heap-current',0x037fcdf0,[0,0])]:meta['prerequisiteReturns'].append(dict(name=name,**base.call(cpu,entry,args)))
        cpu.mem_write(base.DATA+0x7100,bytes(12));meta['prerequisiteReturns'].append(dict(name='actual-heap-buffer-initializer',**base.call(cpu,0x027e8c78,[base.DATA+0x7100])))
    return cpu,meta

def task_state(cpu,context):
    half=lambda address:int.from_bytes(cpu.mem_read(address,2),'little');word=lambda address:int.from_bytes(cpu.mem_read(address,4),'little')
    return dict(heads=[half(context+2*i)for i in range(4)],tails=[half(context+8+2*i)for i in range(4)],nextPriority=half(context+16),taskPriority=half(context+18),currentTask=half(context+20),slots=[dict(next=half(context+188+8*i),flag=half(context+190+8*i),function=word(context+192+8*i))for i in range(24)])
