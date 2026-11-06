import json
from pathlib import Path
import struct
import match_runtime
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
import arm7_runtime
import arm7_sdk288_transmit_context_20261102 as context
from project import ROOT,sha256,write_json

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();raw_path=ROOT/'extract/arm7/arm7.bin';raw=raw_path.read_bytes();layout=arm7_runtime.derive(raw);module=next(m for m in layout['modules']if m['id']=='arm7-main')
    if raw[module['inputFileOffset']:module['inputFileOffset']+module['inputBytes']]!=main:raise ValueError('Actual loader source mapping differs from executable')
    rows=[]
    for mode in range(4):
        for offset in(0,4):
            cpu,setup=context.setup(main,wram,mode*2+offset,mode,initialize_transmit=False,context_offset=offset);base=setup['context'];before=int.from_bytes(cpu.mem_read(base+0x464,4),'little');writes=[]
            def hook(machine,access,address,width,value,user):
                if base<=address<base+0x694:writes.append(dict(pc=hex(machine.reg_read(UC_ARM_REG_PC)),address=hex(address),width=width,value=hex(value&((1<<(width*8))-1))))
            token=cpu.hook_add(UC_HOOK_MEM_WRITE,hook)
            try:returned=context.call(cpu,0x037faec0)
            finally:cpu.hook_del(token)
            installed=int.from_bytes(cpu.mem_read(base+0x464,4),'little');own=[r for r in writes if int(r['address'],0)==base+0x464]
            if before!=0 or len(own)!=2 or any(r['width']!=4 for r in own)or int(own[0]['value'],0)!=0 or int(own[1]['value'],0)!=installed or not 0x037faec0<=int(own[1]['pc'],0)<0x037faec0+800:raise ValueError(dict(mode=mode,before=before,own=own,installed=hex(installed)))
            rows.append(dict(modeArgument=mode,context=hex(base),beforePointer=hex(before),installedPointer=hex(installed),actualInitializerReturn=returned,callbackStore=own,allContextStores=writes,prerequisiteReturns=setup['prerequisiteReturns'],prefixBoundaryNormalReturnCredit=0,pspollInstalled=installed==0x027f0950,sourceCredit=0))
    if sum(r['pspollInstalled']for r in rows)!=6:raise ValueError('Supported installation mode partition changed')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),contextGenerator=Path(context.__file__).name,contextGeneratorSha256=sha256(context.__file__),processor='arm7',program='',module='arm7-main',address='0x27f0950',mode='arm',bytes=104,inputMainSha256=context.MAIN_SHA,inputWramSha256=context.WRAM_SHA,loaderGenerator='arm7_runtime.py',loaderGeneratorSha256=sha256(ROOT/'arm7_runtime.py'),loaderInput=raw_path.relative_to(ROOT).as_posix(),loaderInputSha256=sha256(raw_path),loaderModule=module,callbackModuleFileOffset=0x027f0950-0x027e0000,callbackInputFileOffset=module['inputFileOffset']+0x027f0950-0x027e0000,actualInitializerReturns=len(rows),actualPrerequisiteReturns=sum(len(r['prerequisiteReturns'])for r in rows),realPspollInstallations=6,rows=rows,sourceCredit=0,denominatorByteIncrease=0,modeNamesAndGameReachabilityUnproved=True,sharedConfigurationUnchanged=True);write_json(ROOT/'evidence/attempts/arm7-sdk290-pspoll-installation-20261102.json',report);print(json.dumps({k:report[k]for k in('actualInitializerReturns','actualPrerequisiteReturns','realPspollInstallations','sourceCredit')}),flush=True)

if __name__=='__main__':main()
