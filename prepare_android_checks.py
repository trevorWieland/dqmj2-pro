import hashlib
import shutil
import struct
from project import ROOT, configuration, native_dependencies, now, sha256, write_json
from link_runtime_unit import measured_module
from reproduce import execute


def words_for(kind, seed, index, value):
    words = []
    state = seed
    for position in range(0x1c40):
        current = 0
        if kind == 1:
            current = 0xffffffff
        elif kind == 2:
            current = position * 0x9e3779b9 & 0xffffffff
        elif kind == 3:
            current = 0x55555555 if position & 1 else 0xaaaaaaaa
        elif kind == 4:
            state ^= state << 13 & 0xffffffff
            state ^= state >> 17
            state ^= state << 5 & 0xffffffff
            current = state
        elif kind == 5:
            current = value if position == index else 0
        words.append(current)
    return words


def main():
    config = configuration()
    native_dependencies(config)
    metadata, binary, symbols = measured_module('main')
    specs = [(0, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0), (3, 0, 0, 0)]
    specs += [(4, seed * 0x9e3779b9 & 0xffffffff, 0, 0) for seed in range(1, 33)]
    specs += [(5, 0, index, value) for index in [0, 0x22, 0x23, 0x24, 0x1c33, 0x1c34, 0x1c3f] for value in [0xffffffff, 0x80000000]]
    rows = []
    for kind, seed, index, value in specs:
        words = words_for(kind, seed, index, value)
        data = struct.pack('<' + 'I' * len(words), *words)
        expected = [sum(words[0x24:0x1c34]) & 0xffffffff, sum(words[:0x23]) & 0xffffffff]
        outputs = []
        for address, size in [(0x0207da70, 48), (0x0207daa0, 40)]:
            offset = address - int(metadata['base'], 0)
            outputs.append(execute(binary[offset:offset + size], address, data))
        if outputs != expected:
            raise ValueError('Independent synthetic model differs from an actually returning native checksum')
        rows.append({'kind': kind, 'seed': seed, 'index': index, 'value': value, 'payload': outputs[0], 'header': outputs[1],
                     'syntheticInputSha256': hashlib.sha256(data).hexdigest()})
    folder = ROOT / 'ports/android-native/generated'
    folder.mkdir(parents=True, exist_ok=True)
    header = ['typedef struct { unsigned int kind, seed, index, value, payload, header; } ChecksumVector;',
              f'#define CHECKSUM_VECTOR_COUNT {len(rows)}u', 'static const ChecksumVector checksum_vectors[] = {']
    header += ['    {' + ', '.join(f'0x{row[key]:08x}u' for key in ['kind', 'seed', 'index', 'value', 'payload', 'header']) + '},' for row in rows]
    header.append('};')
    (folder / 'checksum_vectors.h').write_text('\n'.join(header) + '\n', encoding='utf-8')
    bundle = ROOT / 'build/android-native-validation-bundle'
    files = ['src/save_checksum.c', 'ports/android-native/CMakeLists.txt', 'ports/android-native/checksum_runner.c',
             'ports/android-native/generated/checksum_vectors.h']
    artifacts = []
    for name in files:
        target = bundle / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
        artifacts.append({'path': name, 'sha256': sha256(target)})
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'], 'moduleInputSha256': metadata['sha256'],
              'sourceSha256': sha256(ROOT / 'src/save_checksum.c'), 'vectors': rows, 'nativeReturningExecutions': len(rows) * 2,
              'bundle': bundle.relative_to(ROOT).as_posix(), 'artifacts': artifacts,
              'androidCompileStatus': 'not-run-toolchain-unavailable', 'androidExecutionStatus': 'not-run-no-device',
              'hostNativeCompileStatus': 'not-run-no-host-C-compiler-found', 'realSaveOrRomPayloadInBundle': False,
              'sourceCredit': 0, 'limitations': ['Synthetic pure-checksum corpus only; no Android ABI, device, display/input or full-game proof',
                                                'Original ARM9 execution establishes golden outputs; Android AArch64 execution requires its own hashed report']}
    write_json(bundle / 'manifest.json', report)
    write_json(ROOT / 'evidence/portability/android-checksum-bundle-20261029.json', report)
    print({'vectors': len(rows), 'nativeReturningExecutions': len(rows) * 2, 'androidCompileStatus': report['androidCompileStatus'],
           'androidExecutionStatus': report['androidExecutionStatus'], 'bundle': str(bundle)})


if __name__ == '__main__':
    main()
