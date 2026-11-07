import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261106_ov001_state_controllers_source_first_bindings import inputs

ENTRIES = [(0x021f1414, 36, 'e9b9856ca88360f389deea68f2543a807384b0c939b44c4d074113161e66b635'),
           (0x021f1438, 108, '056bd9c36130fa967835b1d7580974c80c33071e3313423eb1a942679b18681e')]


def execute():
    value, image, inventory, records, main_inventory = inputs()
    cases = []
    for entry, size, expected_hash in ENTRIES:
        body = image[entry - int(value['base'], 0):entry - int(value['base'], 0) + size]
        if C.sha(body) != expected_hash:
            raise ValueError('Original complete mapping/sink helper changed')
        if not any(f'kind:function(arm,size=0x{size:x}) addr:0x{entry:08x}' in line
                   for line in inventory.splitlines()):
            raise ValueError('Original helper ARM boundary absent')
        for argument in [0, 1, 2, 3, 127, 128, 255, 0xffffffff]:
            vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
            vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
            vm.mem_map(0x02000000, 0x800000)
            vm.mem_write(entry, body)
            sp, stop, handle = 0x027f0000, 0x02000f00, 0x04560000
            vm.mem_write(0x02238f5c, handle.to_bytes(4, 'little'))
            initial = [0x12340000 + i * 256 for i in range(15)]
            initial[0], initial[13], initial[14] = argument, sp, stop
            vm.reg_write(R.UC_ARM_REG_CPSR, 0x10)
            for register, content in zip(C.REGISTERS, initial):
                vm.reg_write(register, content)
            calls = []

            def code(uc, address, width, unused):
                if address == stop:
                    uc.emu_stop()
                elif address == 0x02085320:
                    actual = [uc.reg_read(r) for r in C.REGISTERS[:3]]
                    if entry != 0x021f1438 or argument > 2 or actual != [handle, 0, argument + 4]:
                        raise ValueError('Actual sink provider words differ')
                    calls.append(dict(address=hex(address), arguments=actual, modeledBody=True))
                    lr = uc.reg_read(R.UC_ARM_REG_LR)
                    for register in C.REGISTERS[:4] + [R.UC_ARM_REG_R12]:
                        uc.reg_write(register, 0xcafeabcd)
                    uc.reg_write(R.UC_ARM_REG_R0, 0x600d0000 + argument)
                    uc.reg_write(R.UC_ARM_REG_PC, lr)
                elif not entry <= address < entry + size:
                    raise ValueError('Unqualified helper/provider execution escaped')

            vm.hook_add(unicorn.UC_HOOK_CODE, code)
            vm.emu_start(entry, stop + 4, count=128)
            actual = [vm.reg_read(r) for r in C.REGISTERS]
            expected = argument if argument < 2 else 2
            if entry == 0x021f1438:
                expected = 0x600d0000 + argument if argument <= 2 else argument
            if vm.reg_read(R.UC_ARM_REG_PC) != stop or actual[0] != expected or actual[13] != sp or actual[4:12] != initial[4:12]:
                raise ValueError('Actual helper result/callee-save/SP contract differs')
            cases.append(dict(entry=hex(entry), argument=argument, returned=actual[0],
                              actualOriginalTopReturn=True, calls=calls))
    return dict(status='passed', sourceCredit=0, actualOriginalEntryReturns=len(cases),
                cases=cases, importedProviderBodiesExecuted=0,
                limits='Two existing accepted original helpers execute independently. No additional helper/storage/source credit. The downstream provider remains a modeled ABI boundary.')
