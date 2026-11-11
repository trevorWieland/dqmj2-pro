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


def main():
    parser = argparse.ArgumentParser(description='Disassemble one measured function from a module image.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--module', required=True, help='module name from manifest.json (e.g. main, ov006)')
    parser.add_argument('--address', required=True, help='function address, e.g. 0x21ec644')
    parser.add_argument('--bytes', type=int, required=True, help='function size in bytes (ledger row)')
    parser.add_argument('--mode', choices=sorted(TRIPLES), default='arm')
    args = parser.parse_args()
    try:
        print(disassemble(args.root.resolve(), args.module, int(args.address, 0), args.bytes, args.mode), end='')
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
