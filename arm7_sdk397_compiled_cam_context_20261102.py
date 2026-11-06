import hashlib
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE
import arm7_sdk306_task_command_context_20261102 as context

SIZES={0x027f2180:720,0x027eb90c:168,0x027eb9b4:320,0x027ec5a4:228}

def qualified(main,bodies):
    if bodies is None:return
    if set(bodies)!=set(SIZES):raise ValueError('Complete four-definition compiled CAM/receive closure required')
    for entry,body in bodies.items():
        if len(body)!=SIZES[entry]or main[entry-context.base.MAIN:entry-context.base.MAIN+len(body)]!=body:raise ValueError('Complete source-linked body differs from original qualified range')

def call(cpu,entry,args,meta,bodies=None):
    if bodies is None:return context.base.call(cpu,entry,args)
    active=[];returned=[]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));returned.append(row)
        if pc in bodies:active.append(dict(entry=hex(pc),bytes=len(bodies[pc]),compiledBodySha256=hashlib.sha256(bodies[pc]).hexdigest(),returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),sourceCreditFromSetup=0))
    token=cpu.hook_add(UC_HOOK_CODE,code)
    try:result=context.base.call(cpu,entry,args)
    finally:cpu.hook_del(token)
    if active:raise ValueError('Source-linked setup entry did not actually return')
    meta.setdefault('actualSourceLinkedSetupReturns',[]).extend(returned);return result
