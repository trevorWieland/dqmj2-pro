import gzip
import hashlib
import json
import random
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
import unicorn
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
import match_runtime as C
from project import configuration, sha256
from link_runtime_unit import validate, measured_module
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/overlay000'
WORK = ROOT / 'work/parallel-wave20261102/overlay000/proof'
SOURCE = ROOT / 'src/ov000/parallel_wave20261102'
ENTRY = 0x021DBBB8
CALLEE = 0x021DBB50
SP = 0x027F0000
STOP = 0x027E0000
CONTEXT = 0x02400000
MESH = 0x02500000
POINT = 0x02410000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def dump(name, data):
    LANE.mkdir(parents=True, exist_ok=True)
    (LANE / name).write_text(json.dumps(data, indent=2) + '\n')


def build(path, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(path, 'ov000', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=path.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(path.with_name('context.h')))]
    if origin is None:
        proof = validate(row, qualified_bindings(row), WORK / name / 'canonical')
        return dict(**row, realLink=proof), (WORK / name / 'canonical/caller.bin').read_bytes()
    try:
        proof = validate(row, qualified_bindings(row), WORK / name / 'canonical')
    except ValueError as error:
        proof = error.args[0]
    private, body = link_private(row, qualified_bindings(row), WORK / name / 'canonical', WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=proof, privateLink=private), body


def run(image, start, profile, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(start, image)
    rng = random.Random(profile['ordinal'])
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[0] = CONTEXT
    initial[1] = POINT
    initial[13] = SP
    initial[14] = STOP
    vm.reg_write(UC_ARM_REG_CPSR, 0x10 | ((profile['ordinal'] & 15) << 28))
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    vm.mem_write(SP - 0x1000, bytes([profile['ordinal'] & 255]) * 0x1000)
    vm.mem_write(CONTEXT, bytes([0xA5]) * 0x100)
    vm.mem_write(CONTEXT + 8, struct.pack('<I', profile['index']))
    vm.mem_write(CONTEXT + 0x10, bytes([profile['limit']]))
    vm.mem_write(0x0223142C + 0x79C, struct.pack('<I', MESH))
    vm.mem_write(MESH + 0xC, struct.pack('<I', 0x1234))
    vm.mem_write(MESH + 0x198, struct.pack('<II', 0x3210, 0xABCDEF01))
    calls = []
    writes = []
    pcs = []
    returned = []
    def memory(uc, access, address, size, value, user):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(uc, address, size, user):
        pcs.append(address)
        if address == STOP:
            returned.append(True)
            uc.emu_stop()
        elif address == CALLEE:
            words = [uc.reg_read(r) for r in REGS[:4]] + list(struct.unpack('<III', bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 12))))
            calls.append(words)
            writes.append([CONTEXT + 0x14, 4, profile['result'] ^ 0xA5A5A5A5])
            uc.mem_write(CONTEXT + 0x14, struct.pack('<I', profile['result'] ^ 0xA5A5A5A5))
            returnAddress = uc.reg_read(UC_ARM_REG_LR)
            for register in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
                uc.reg_write(register, 0xC0000000 + register)
            uc.reg_write(UC_ARM_REG_R0, profile['result'])
            uc.reg_write(UC_ARM_REG_CPSR, 0xA0000010)
            uc.reg_write(UC_ARM_REG_PC, returnAddress)
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(start, STOP + 4, count=500)
    if not returned:
        raise ValueError('Actual return sentinel not reached')
    registers = [vm.reg_read(r) for r in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved/SP contract changed')
    memoryImage = bytes(vm.mem_read(0x02000000, 0x800000))
    signedIndex = struct.unpack('<h', struct.pack('<H', profile['index'] & 65535))[0] & 0xFFFFFFFF
    signedLimit = struct.unpack('<b', bytes([profile['limit']]))[0] & 0xFFFFFFFF
    expected = [signedIndex, MESH + 0x3210, CONTEXT + 0x12, 0xABCDEF01, MESH + 0x1234, POINT, signedLimit]
    failures = []
    if calls != [expected]:
        failures.append('Independent seven-word physical call model')
    if registers[0] != profile['result'] or vm.mem_read(CONTEXT + 0x11, 1)[0] != (profile['result'] & 255):
        failures.append('Independent returned-word/count-byte model')
    if bytes(vm.mem_read(CONTEXT + 0x12, 2)) != struct.pack('<H', profile['index'] & 65535):
        failures.append('Independent truncated-index store model')
    return dict(registers=registers, cpsr=vm.reg_read(UC_ARM_REG_CPSR), calls=calls, writes=writes, memorySha256=hashlib.sha256(memoryImage).hexdigest(), pcs=pcs, modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned runtime differs')
    SOURCE.mkdir(parents=True, exist_ok=True)
    source = SOURCE / 'native_ov000_021dbbb8.c'
    pinsPath = LANE / 'proof-inputs.json'
    if pinsPath.exists():
        for row in json.loads(pinsPath.read_text())['files']:
            if sha256(ROOT / row['path']) != row['sha256']:
                raise ValueError(('Pinned proof input differs', row['path']))
    match, body = build(source, 'source')
    controls = []
    template = source.read_text()
    for index, (name, before, after) in enumerate([('unsigned-capacity', '*(s8 *) (context + 0x10)', '*(u8 *) (context + 0x10)'), ('wrong-context-index', '(context + 8)', '(context + 4)')]):
        directory = WORK / name
        directory.mkdir(parents=True, exist_ok=True)
        controlSource = directory / 'source.c'
        text = template.replace(before, after)
        if text == template:
            raise ValueError('Control site absent')
        controlSource.write_text(text)
        controlSource.with_name('context.h').write_text((SOURCE / 'context.h').read_text())
        origin = 0x02650000 + index * 0x2000
        proof, image = build(controlSource, name, origin)
        controls.append(dict(name=name, origin=origin, proof=proof, image=image, rejected=0, positive=0))
    info, overlay, unused = measured_module('ov000')
    native = overlay[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + 96]
    if native != body:
        raise ValueError('Source image not exact')
    profiles = []
    for indexWord, limit, result in itertools.product([0, 1, 0x7FFF, 0x8000, 0xFFFF, 0xABCD8001], [0, 1, 0x7F, 0x80, 0xFF], [0, 1, 0x12345678, 0xFFFFFFFF]):
        profiles.append(dict(ordinal=len(profiles), index=indexWord, limit=limit, result=result))
    traces = []
    for profile in profiles:
        a = run(native, ENTRY, profile, overlay)
        b = run(body, ENTRY, profile, overlay)
        if a != b or a['modelFailures']:
            raise ValueError(('Native/source physical comparison failed', profile, a, b))
        for control in controls:
            result = run(control['image'], control['origin'], profile, overlay)
            control['rejected' if result['modelFailures'] else 'positive'] += 1
        traces.append(dict(profile=profile, result=a))
    if any(not control['rejected'] for control in controls):
        raise ValueError('Negative controls failed to reject')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'wrapper-traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    for control in controls:
        del control['image']
    report = dict(schemaVersion=1, allPassed=True, romSha256=configuration()['romSha256'], module='ov000', processor='arm9', program='', moduleSha256=info['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=96, sourceCreditPendingIntegrator=96, cases=len(profiles), actualNativeAndSourceReturns=2 * len(profiles), completeRegistersCpsrCallsWritesAndRamEqual=True, ownInstructionPcs=sorted(set(pc for row in traces for pc in row['result']['pcs'] if ENTRY <= pc < ENTRY + 92)), negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)), limits=['One full-span ordinary C wrapper exact after declared relocations and real pinned MW linking; coordinator owns shared acceptance and whole-module/ROM checks.', 'Synthetic disjoint RAM only; callee BB50 supplied at its existing boundary with seven raw physical caller words and prescribed return/mutation/clobbers. No callee source credit, original formal arity, arbitrary alias domain, hardware or gameplay claim.', 'Signed8 capacity, signed16 low-word index, upper-word poison, returned count truncation and preserved register/SP behavior tested over120 cases. Wrong whole-C controls privately link without overwriting adjacent native code.', 'Six larger geometry functions remain nonmatching and retain zero source credit.'])
    dump('wrapper-match.json', report)
    print(dict(cases=len(profiles), exactBytes=96, negativeControls=[dict(name=c['name'], rejected=c['rejected']) for c in controls]), flush=True)


if __name__ == '__main__':
    import itertools
    execute()
