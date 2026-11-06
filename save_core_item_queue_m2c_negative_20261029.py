import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
import save_core_item_queue_build_20261029 as build
from link_runtime_unit import validate as link
from save_core_item_queue_oracle_20261029 import execute, ENTRY, PROVIDER, STATE, QUEUE, STACK, STOP, REGS


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    origin = ROOT / 'work/runtime-recovery/m2c/runtime09/drafts/func_02063a0c.c'
    source = ROOT / 'nonmatching/save-core/20261029-item-queue/legacy-m2c.c'
    raw = source.read_bytes()
    if sha(raw) != 'b9ebd3a762517a1a12b42c9ea331945a4ca12342f7e0bb5ac85da8361cf1c2b3':
        raise AssertionError('Preserved legacy source differs from known-bad identity')
    if origin.exists() and origin.read_bytes() != raw:
        raise AssertionError('Original draft changed; preserve and version its counterexample')
    build.SOURCE = str(source.relative_to(ROOT)).replace('\\', '/')
    build.SPECS = {'native_main_02063a0c': (ENTRY, 104)}
    build.GLOBALS = {'native_fn_02065d88': (PROVIDER, 'arm'),
                     'native_data_021bd51c': (0x021BD51C, 'data')}
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('Legacy counterexample native module changed')
    if sha((ROOT / build.COMPILER).read_bytes()) != build.COMPILER_HASH:
        raise AssertionError('Legacy counterexample compiler pin changed')
    rows, exact = build.compile_and_link(arm, 2, 'space')
    row = rows[0]
    try:
        proof = link(row, build.bindings())
    except ValueError as error:
        failure = ast.literal_eval(str(error))
        binary = Path(failure['directory']) / 'caller.bin'
    else:
        binary = (ROOT / proof['linkedElf']).parent / 'caller.bin'
    legacy = binary.read_bytes()
    state = bytearray(0x5000)
    state[QUEUE - STATE:QUEUE - STATE + 24] = bytes([44] * 24)
    table = bytes(88 * 256)
    registers = [0xA0020000 + index * 0x100 for index in range(len(REGS))]
    registers[0], registers[13], registers[14] = 45, STACK, STOP
    provider = arm[PROVIDER - 0x02000000:PROVIDER - 0x02000000 + 24]
    native = arm[ENTRY - 0x02000000:ENTRY - 0x02000000 + 104]
    results = []
    for name, body in [('native', native), ('legacy-m2c-C', legacy)]:
        output, visited = execute(body, provider, bytes(state), table, 45, registers, 0x10)
        results.append({'engine': name, 'returnWord': output['registers'][0],
                        'actualReturn': True, 'visitedInstructions': len(visited)})
    if [row['returnWord'] for row in results] != [0xFFFFFFFF, 255]:
        raise AssertionError(('Legacy sentinel counterexample changed', results))
    report = {
        'schemaVersion': 1, 'romSha256': '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',
        'identity': 'arm9:main:arm:0x02063a0c', 'nativeBytes': 104,
        'legacySource': str(origin.relative_to(ROOT)), 'legacySourceSha256': sha(raw),
        'preservedLegacyCopy': build.SOURCE, 'legacyObject': row['object'],
        'legacyObjectSha256': row['objectSha256'], 'linkedLegacyBinary': str(binary.relative_to(ROOT)),
        'linkedLegacyBinarySha256': sha(legacy), 'compiledLegacyBytes': len(legacy),
        'compilerSha256': build.COMPILER_HASH, 'arm9Sha256': sha(arm),
        'nativeSpanSha256': sha(native), 'counterexample': {
            'item': 45, 'categoryByte44': 0, 'queueBytes': bytes([44] * 24).hex(),
            'expectedAbsentReturnWord': 0xFFFFFFFF, 'results': results,
            'actualReturns': 2, 'freshMachinePerEngine': True, 'instructionLimit': 2000
        },
        'classification': 'known-incorrect-source-hypothesis',
        'reasons': ['u8 result narrows-1 to255 before u32 return, violating the native sentinel.',
                    'The item-record call has no explicit item argument. A retained native register value '
                    'is not a portable C argument contract; this separate ABI defect is source-inspected.'],
        'netNewMatchedBytes': 0, 'generator': str(Path(__file__).relative_to(ROOT)),
        'generatorSha256': sha(Path(__file__).read_bytes()),
        'oracleSourceSha256': sha((ROOT / 'save_core_item_queue_oracle_20261029.py').read_bytes())
    }
    output = ROOT / 'nonmatching/save-core/20261029-item-queue/legacy-counterexample.json'
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'legacySourceSha256': sha(raw), 'actualReturns': 2,
                      'nativeReturn': '0xffffffff', 'legacyReturn': '0xff', 'output': str(output)}))


if __name__ == '__main__':
    main()
