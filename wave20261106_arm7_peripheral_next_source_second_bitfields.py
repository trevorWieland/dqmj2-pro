from project import ROOT,sha256
from wave20261106_arm7_peripheral_next_source_second_build import SOURCE,WORK


def execute():
    from wave20261106_arm7_peripheral_next_source_second_controls import compile_unit,function_body
    import unicorn
    from unicorn import arm_const as R
    rows=[('038046ac','SPITpData','e.x','e.y',4,0,12),('038046ac','SPITpData','e.y','e.x',4,12,12),('038046ac','SPITpData','e.touch','e.validity',4,24,1),('038046ac','SPITpData','e.validity','e.touch',4,25,2),('038046ac','SPITpData','e.dummy','e.x',4,27,5)];positive=[];negative=[]
    for tag,kind,member,badMember,size,shift,bits in rows:
        directory=WORK/'bitfield-abi'/member.replace('.','-');directory.mkdir(parents=True,exist_ok=True)
        for h in(SOURCE/tag).glob('*.h'):(directory/h.name).write_bytes(h.read_bytes())
        storage='u16'if size==2 else'u32';template='#include "context000.h"\nu32 abi(u32 raw,u32 value){'+kind+' state;*('+storage+'*)&state=('+storage+')raw;state.MEMBER=value;return *('+storage+'*)&state;}\n';proof=[]
        for label,field in [('positive',member),('wrong-field',badMember)]:
            source=directory/(label+'.c');obj=directory/(label+'.o');source.write_text(template.replace('MEMBER',field));attempt=compile_unit(source,obj)
            if attempt['exitCode']:raise ValueError(('Actual C bitfield ABI failed',attempt))
            body=function_body(obj,'abi');failures=[];count=0
            for raw in [0,0xffffffff,0xa5a55a5a]:
                for value in [0,1,(1<<bits)-1,0xffffffff]:
                    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,body);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,raw);vm.reg_write(R.UC_ARM_REG_R1,value);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=128);mask=((1<<bits)-1)<<shift;expected=((raw&~mask)|((value<<shift)&mask))&((1<<(size*8))-1);actual=vm.reg_read(R.UC_ARM_REG_R0);count+=1
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x0200f000:failures.append(dict(raw=raw,value=value,expected=expected,actual=actual))
            if label=='positive':
                if failures:raise ValueError(('Actual field mask/preservation differs',kind,member,failures))
                positive.append(dict(type=kind,member=member,storageBytes=size,mask=hex(mask),actualReturns=count,sourceSha256=sha256(source),objectSha256=sha256(obj)))
            else:
                if not failures:raise ValueError('Wrong typed field ABI admitted')
                negative.append(dict(type=kind,member=member,rejectedField=field,rejected=True,mismatches=failures,sourceSha256=sha256(source),objectSha256=sha256(obj)))
    return dict(status='passed',sourceCredit=0,actualFreshReturns=sum(r['actualReturns']for r in positive),positive=positive,negativeControls=negative)
