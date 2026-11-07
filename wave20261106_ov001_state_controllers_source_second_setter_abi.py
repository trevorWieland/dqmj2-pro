import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261106_ov001_state_controllers_source_second_bindings import inputs


def execute():
    value, image, inventory, records, main_inventory = inputs()
    entry, size, variable = 0x021e9610, 24, 0x0222ec84
    body = image[entry - int(value['base'], 0):entry - int(value['base'], 0) + size]
    if C.sha(body) != '5a5db36586aecc3f7299662157f82d88723cbc79a1f4f21f187fe09bbb7a2676':
        raise ValueError('Original swap-byte entry changed')
    if 'func_ov001_021e9610 kind:function(arm,size=0x18) addr:0x021e9610' not in inventory.splitlines():
        raise ValueError('Original swap-byte ARM boundary absent')
    cases = []
    for old in [0, 1, 127, 128, 255]:
        for new in [0, 1, 128, 255, 256, 0xffffffff]:
            vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
            vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
            vm.mem_map(0x02000000, 0x800000)
            vm.mem_write(entry, body)
            vm.mem_write(variable, bytes([old, 0xa5, 0x5a, 0xd3]))
            vm.reg_write(R.UC_ARM_REG_CPSR, 0x10)
            initial = [0x10203040 + i * 256 for i in range(15)]
            initial[0], initial[13], initial[14] = new, 0x027f0000, 0x02000f00
            for register, content in zip(C.REGISTERS, initial):
                vm.reg_write(register, content)
            vm.emu_start(entry, initial[14], count=64)
            actual = [vm.reg_read(register) for register in C.REGISTERS]
            if vm.reg_read(R.UC_ARM_REG_PC) != initial[14] or actual[0] != old or actual[4:12] != initial[4:12] or actual[13] != initial[13]:
                raise ValueError('Actual swap-byte result/callee-save/SP differs')
            if bytes(vm.mem_read(variable, 4)) != bytes([new & 255, 0xa5, 0x5a, 0xd3]):
                raise ValueError('Actual swap-byte store width/truncation differs')
            cases.append(dict(old=old, new=new, returned=actual[0], writtenByte=new & 255, adjacentBytesPreserved=True))
    return dict(status='passed', sourceCredit=0, actualOriginalEntryReturns=len(cases),
                actualEntry=hex(entry), variable=hex(variable), cases=cases,
                importedProviderBodiesExecuted=0, additionalStorageCredit=0,
                limits='Existing accepted helper executes independently. Caller fixture providers remain modeled boundaries; no new helper/storage/source credit.')
