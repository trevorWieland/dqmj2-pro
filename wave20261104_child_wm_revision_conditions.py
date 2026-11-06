import os
import struct
import subprocess
from pathlib import Path
import utility_code
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wm/revision'
WORK = ROOT / 'work/wm1104rev/conditions'
BASE, STATUS = 0x027e0000, 0x02400000


def machine(image, address, body):
    cpu = un.Uc(un.UC_ARCH_ARM, un.UC_MODE_ARM)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_map(STATUS, 0x10000)
    cpu.mem_write(BASE, image)
    cpu.mem_write(address, body)
    cpu.reg_write(ar.UC_ARM_REG_CPSR, 0xf0000010)
    return cpu


def admission(image, address, body, state, flags):
    cpu = machine(image, address, body)
    cpu.mem_write(STATUS, struct.pack('<H', state))
    cpu.mem_write(STATUS + 0xc8, struct.pack('<I', flags))
    if address == 0x027e3538:
        start, allowed, error, register = 0x027e354c, 0x027e357c, 0x027e3558, ar.UC_ARM_REG_R4
    else:
        start, allowed, error, register = 0x027e44c4, 0x027e44f4, 0x027e44d0, ar.UC_ARM_REG_R5
    cpu.reg_write(register, STATUS)
    pcs, reads = [], []

    def code(machine, at, size, user):
        if at in (allowed, error):
            machine.emu_stop()
        else:
            pcs.append(at)

    cpu.hook_add(un.UC_HOOK_CODE, code)
    cpu.hook_add(un.UC_HOOK_MEM_READ, lambda machine, access, at, size, value, user: reads.append((at, size)))
    cpu.emu_start(start, 0, count=8)
    expected = allowed if state == 2 else error
    if cpu.reg_read(ar.UC_ARM_REG_PC) != expected or reads != [(STATUS, 2)]:
        raise ValueError('Original admission condition or halfword read differs')
    return dict(state=state, suppliedUnrelatedStatusWord=hex(flags), observedAllowed=expected == allowed,
                originalInstructionPcs=[hex(p) for p in pcs], reads=reads,
                noStatusOffsetC8Read=True, importsExecuted=0, fullCallerExecutions=0)


def limit(image, body, child_size, maximum):
    cpu = machine(image, 0x027e13e4, body)
    cpu.mem_write(STATUS + 0x36, struct.pack('<H', maximum))
    cpu.reg_write(ar.UC_ARM_REG_R5, STATUS)
    cpu.reg_write(ar.UC_ARM_REG_R1, child_size)
    pcs, reads = [], []

    def code(machine, at, size, user):
        if at == 0x027e1594:
            machine.emu_stop()
        else:
            pcs.append(at)

    cpu.hook_add(un.UC_HOOK_CODE, code)
    cpu.hook_add(un.UC_HOOK_MEM_READ, lambda machine, access, at, size, value, user: reads.append((at, size)))
    cpu.emu_start(0x027e1588, 0, count=8)
    actual = cpu.reg_read(ar.UC_ARM_REG_R1)
    expected = min(child_size, maximum)
    if cpu.reg_read(ar.UC_ARM_REG_PC) != 0x027e1594 or actual != expected or reads != [(STATUS + 0x36, 2)]:
        raise ValueError('Original dynamic unsigned-halfword limit condition differs')
    return dict(suppliedChildSize=child_size, suppliedStatusHalfword=maximum, actual=actual, expected=expected,
                originalInstructionPcs=[hex(p) for p in pcs], reads=reads, fullCallerExecutions=0)


def layout(entry):
    directory = WORK / 'layout'
    directory.mkdir(parents=True, exist_ok=True)
    headers = []
    for pin in entry['sourceDependencies']:
        source = ROOT / pin['path']
        target = directory / source.name
        target.write_bytes(source.read_bytes())
        headers.append(target)
    text = ''.join('#include "' + p.name + '"\n' for p in headers)
    text += 'typedef char a[((u32)&((WMStatus*)0)->state==0 && sizeof(((WMStatus*)0)->state)==2)?1:-1];\n'
    text += 'typedef char b[((u32)&((WMStatus*)0)->miscFlags==0xc8 && sizeof(((WMStatus*)0)->miscFlags)==4)?1:-1];\n'
    text += 'typedef char c[((u32)&((WMStatus*)0)->mp_childMaxSize==0x36 && sizeof(((WMStatus*)0)->mp_childMaxSize)==2)?1:-1];\n'
    text += 'typedef char d[((u32)&((WMSPWork*)0)->status==0x1550)?1:-1];\n'
    cases = [('correct', text), ('wrong-status-offset', text.replace('==0xc8', '==0xcc')),
             ('wrong-child-offset', text.replace('==0x36', '==0x34')),
             ('wrong-work-member-offset', text.replace('==0x1550', '==0x550'))]
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    results = []
    for label, payload in cases:
        source, obj = directory / (label + '.c'), directory / (label + '.o')
        source.write_text(payload)
        command = [str(ROOT / entry['compiler']), *entry['compilerFlags'], '-c', str(source), '-o', str(obj)]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30, env=env)
        results.append(dict(label=label, exitCode=process.returncode, source=source.relative_to(ROOT).as_posix(),
                            sourceSha256=sha256(source), stdout=process.stdout, stderr=process.stderr))
    if results[0]['exitCode'] != 0 or any(r['exitCode'] == 0 for r in results[1:]):
        raise ValueError(('Correct/wrong typed-layout controls differ', results))
    return results


def main():
    report = read_json(LANE / 'packet-ready.json')
    rows = {int(r['address'], 0): r for r in report['matches']}
    image = (ROOT / 'extract/utility/runtime/utility-child-arm7-main.bin').read_bytes()
    bodies = {}
    for address, row in rows.items():
        native = image[address - BASE:address - BASE + row['bytes']]
        linked_path = (ROOT / row['realLink']['linkedElf']).with_name('caller.bin')
        linked = linked_path.read_bytes()
        if native != linked or sha256(linked_path) != row['targetSha256']:
            raise ValueError('Actual complete linked caller differs from original native extent')
        bodies[address] = (native, linked)
    records = []
    for address in [0x027e3538, 0x027e44a8]:
        for state in [0, 1, 2, 3, 65535]:
            for flags in [0, 1, 2, 0x80000000]:
                original, compiled = [admission(image, address, b, state, flags) for b in bodies[address]]
                if original != compiled:
                    raise ValueError('Original and linked state admission fragments differ')
                records.append(dict(address=hex(address), original=original, recompiled=compiled))
    for child_size in [0, 1, 127, 511, 512, 513, 1024, 65535]:
        for maximum in [0, 128, 511, 512, 1024, 65535]:
            original, compiled = [limit(image, body, child_size, maximum) for body in bodies[0x027e13e4]]
            if original != compiled:
                raise ValueError('Original and linked dynamic child-size limit fragments differ')
            records.append(dict(address='0x27e13e4', original=original, recompiled=compiled))
    layouts = layout(rows[0x027e13e4])
    write_json(LANE / 'native-condition-controls.json', dict(status='passed', fragments=len(records) * 2,
        records=records, sourceLayoutControls=layouts, fullCallerExecutions=0, fullCallerReturns=0,
        actualNativeHelperExecutions=0, unicornVersion=un.__version__,
        workStatusMemberOffset=0x1550, originalWorkSymbolRelocationAddend=0x1000, originalStatusLoadDisplacement=0x550,
        independentConditions=['Original initial admission accepts exactly state halfword2 without reading status+0xc8',
                               'Original limit uses unsigned halfword at status+0x36, including values above512'],
        limitation='Only original/linked instruction fragments execute with modeled status state/register inputs; complete wireless handlers, helpers and device behavior remain unproved'))
    print(dict(nativeAndLinkedFragments=len(records) * 2, sourceLayoutPositive=True,
               wrongLayoutOffsetsRejected=3, fullCallerExecutions=0))


if __name__ == '__main__':
    main()
