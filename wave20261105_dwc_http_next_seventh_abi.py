from project import ROOT
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB,CS_MODE_ARM
from wave20261105_dwc_http_next_seventh_bindings import inputs

def verify(rows):
 value,image,inventory,records,imports=inputs();decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);witnesses=[]
 for caller,offset,mnemonic,operands,meaning in [(0x2099df4,0x88,'bl','#0x2097dc4','Original Cal buffer import call'),(0x2099df4,0x8c,'cmp','r0, #0','Caller consumes a returned word despite comparative void spelling'),(0x2099df4,0x122,'ldr','r0, [r0, #4]','Current thread pointer from measured scheduler view'),(0x2099df4,0x124,'blx','#0x2006b74','Actual thread-priority import'),(0x2099df4,0x32,'blx','#0x2008430','Declared terminal import boundary; never classified as a returned caller')]:
  size=4 if mnemonic in ['bl','blx']else 2;raw=image[caller+offset-0x2000000:caller+offset-0x2000000+size];decoded=list(decoder.disasm(raw,caller+offset));assert len(decoded)==1 and(decoded[0].mnemonic,decoded[0].op_str)==(mnemonic,operands);assert any(int(row['address'],0)==caller for row in rows);witnesses.append(dict(caller=hex(caller),offset=offset,nativeBytes=raw.hex(),instruction=mnemonic+' '+operands,meaning=meaning))
 raw=image[0x6b74:0x6b7c];decoded=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(raw,0x2006b74));assert [(i.mnemonic,i.op_str)for i in decoded]==[('ldr','r0, [r0, #0x70]'),('bx','lr')]
 return dict(allPassed=True,witnesses=witnesses,originalPriorityProviderReadOnlyBytes=raw.hex(),originalPriorityProviderWasNotExecuted=True,CalScratchBytes=148,localParamBytes=28,errno=dict(address='0x20ec9b0',bytes=4,stickyValueComparedTo=34),scheduler=dict(address='0x20e33e4',bytes=8,currentThreadOffset=4),constructorRequiresNonNullWorkServiceAndResult=True,stopClassification='Declared stop at actual OS_Terminate ARM import entry; no callee body executes and no return credit assigned to that path.',calleeSourceOrExecutionCredit=0)
