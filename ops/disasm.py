"""Disassemble a measured function from a module image, ARM or Thumb.

Authors need to read the original instruction stream before writing matching C.  The
image is a flat binary, so this wraps the pinned LLVM objdump from the private
toolchain: it slices the module image, wraps the slice in an ELF with its real load
address and disassembles it in the requested mode.

    python ops/disasm.py --module ov006 --address 0x21ec644 --bytes 24 --mode thumb
    python ops/disasm.py --module main --address 0x2000c90 --bytes 88

``--mode`` defaults to ``arm``; pass ``thumb`` for the Thumb population.  ``--root``
defaults to the current directory and must be a checkout with ``manifest.json`` and
the module image (``extract/...``) present, i.e. the private tree or an unpacked
replay.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

OBJDUMP = 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-objdump.exe'
OBJCOPY = 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-objcopy.exe'
TRIPLES = {'arm': 'armv5te-none-eabi', 'thumb': 'thumbv5te-none-eabi'}


def module_image(root, name):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8-sig'))
    for module in manifest['modules']:
        if module['name'] == name:
            return root / module['binary'], int(module['base'], 0)
    raise SystemExit('unknown module: ' + name)


def disassemble(root, name, address, size, mode='arm'):
    image_path, base = module_image(root, name)
    image = image_path.read_bytes()
    offset = address - base
    if offset < 0 or offset + size > len(image):
        raise SystemExit('range lies outside the module image')
    tool_dir = root / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    objcopy, objdump = root / OBJCOPY, root / OBJDUMP
    if not objcopy.is_file() or not objdump.is_file():
        raise SystemExit('pinned llvm tools are unavailable under ' + str(tool_dir))
    with tempfile.TemporaryDirectory() as scratch:
        raw = Path(scratch) / 'slice.bin'
        elf = Path(scratch) / 'slice.o'
        raw.write_bytes(image[offset:offset + size])
        subprocess.run([str(objcopy), '-I', 'binary', '-O', 'elf32-littlearm', '-B', 'arm',
                        '--change-section-address=.data=0x%08x' % address,
                        '--rename-section', '.data=.text,alloc,code', str(raw), str(elf)],
                       check=True, capture_output=True, text=True)
        result = subprocess.run([str(objdump), '-d', '--triple=' + TRIPLES[mode],
                                 '--no-show-raw-insn', str(elf)],
                                check=True, capture_output=True, text=True)
        return result.stdout


def pool_literals(root, name, address, size, mode='arm'):
    """Yield (instruction address, literal address, literal word) for PC-relative loads.

    Decoded from the raw instruction bytes rather than the rendered operand: the
    literal pool of a short accessor often lives outside the row, so the table must
    be read from the module image, not from the disassembled slice.
    """
    image_path, base = module_image(root, name)
    image = image_path.read_bytes()
    offset = address - base
    code = image[offset:offset + size]
    for index in range(0, len(code) - 1, 2 if mode == 'thumb' else 4):
        if mode == 'thumb':
            halfword = int.from_bytes(code[index:index + 2], 'little')
            if (halfword & 0xF800) != 0x4800:      # ldr Rt, [pc, #imm8 * 4]
                continue
            instruction = address + index
            literal_address = ((instruction + 4) & ~3) + (halfword & 0xFF) * 4
        else:
            word = int.from_bytes(code[index:index + 4], 'little')
            if (word & 0x0F7F0000) != 0x051F0000:  # ldr Rt, [pc, #+/-imm12]
                continue
            instruction = address + index
            immediate = word & 0xFFF
            literal_address = instruction + 8 + (immediate if word & 0x00800000 else -immediate)
        literal_offset = literal_address - base
        if 0 <= literal_offset and literal_offset + 4 <= len(image):
            literal = int.from_bytes(image[literal_offset:literal_offset + 4], 'little')
        else:
            literal = None
        yield instruction, literal_address, literal


def main():
    parser = argparse.ArgumentParser(description='Disassemble one measured function from a module image.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--module', required=True, help='module name from manifest.json (e.g. main, ov006)')
    parser.add_argument('--address', required=True, help='function address, e.g. 0x21ec644')
    parser.add_argument('--bytes', type=int, required=True, help='function size in bytes (ledger row)')
    parser.add_argument('--mode', choices=sorted(TRIPLES), default='arm')
    parser.add_argument('--resolve-pools', action='store_true',
                        help='also print the literal each PC-relative load reads')
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        address = int(args.address, 0)
        _, base_hint = module_image(root, args.module)
        print(disassemble(root, args.module, address, args.bytes, args.mode), end='')
        if args.resolve_pools:
            print('\n-- literal pools --')
            found = False
            for instruction, literal_address, literal in pool_literals(
                    root, args.module, address, args.bytes, args.mode):
                found = True
                rendered = 'unreadable' if literal is None else f'{literal:#010x}'
                note = ''
                if literal is not None and base_hint <= literal < base_hint + 0x10000000:
                    note = '  (address-like)'
                print(f'  {instruction:#010x}: pool {literal_address:#010x} -> {rendered}{note}')
            if not found:
                print('  (no PC-relative loads in this row)')
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
