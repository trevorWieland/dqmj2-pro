#!/usr/bin/env python3
"""GNU-objdump-compatible disassembly shim for mwccarm ARM/Thumb objects.

decomp-permuter shells out to an ``objdump -drz``-style command and parses the
text: one row per instruction with the address, the raw bytes, the mnemonic and
the operands, plus relocation rows of the form ``<offset>: R_ARM_<kind> <symbol>``.
Nothing on this machine produces that output for an mwccarm object, so this shim
does it with Capstone and pyelftools.

    python ops/mwcc_objdump.py <object.o> [--mode thumb|arm]

The output is byte-for-byte shaped like ``arm-none-eabi-objdump -drz`` for a
relocatable object (the permuter slices two tab-separated fields off every row,
so the raw-bytes column is mandatory):

    target.o:     file format elf32-littlearm

    Disassembly of section .text:

    00000000 <.text>:
       0:   4909            ldr     r1, [pc, #0x24]
      28:   00000000        .word   0x0
                            28: R_ARM_ABS32  native_data_027fffa8

Why a shim instead of a real cross objdump: the pinned LLVM objdump in this tree
is x86-hosted and *does* disassemble ARM, but its ``-d`` output for a relocatable
object renders relocations the LLVM way (``R_ARM_ABS32`` inside a comment block on
the *next* line, no ``-r`` rows), which the permuter's parser rejects. Capstone is
already a dependency of ``ops/permuter_queue.py`` and ``ops/harvest_filter.py``.

Modelled on the sm64ds-decomp/pokeheartgold setup (mwccarm + ``compiler_type =
"mwcc"`` + a custom ``objdump_command``), adapted to this project's flat-module
layout: mwccarm emits ARM ELF mapping symbols (``$a``/``$t``/``$d``), so literal
pools are rendered as ``.word`` data instead of being misdecoded as instructions.
Both sides of a permuter comparison go through this same shim, which is what makes
the diff meaningful.

Exit status is 0 on success and 1 with a message on an object this shim cannot
describe (unknown relocation kind, missing .text, wrong endianness).
"""
import argparse
import sys
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile

# ARM ELF relocation kinds mwccarm emits for these single-function objects.
# 1  = R_ARM_PC24       (pre-EABI spelling of an ARM BL; 2.0/base emits this)
# 2  = R_ARM_ABS32      (literal pool / data pointer)
# 10 = R_ARM_THM_CALL   (Thumb BL)
# 28 = R_ARM_CALL       (ARM BL, newer EABI spelling)
# 29 = R_ARM_JUMP24     (ARM B)
# 30 = R_ARM_THM_JUMP24 (Thumb B.W / BLX)
# PC24 and CALL are rendered with the same name on purpose: both sides of a
# permuter diff go through this shim, and the permuter only needs one ARM call
# spelling to line the relocation rows up.
RELOCATION_NAMES = {
    1: 'R_ARM_CALL',
    2: 'R_ARM_ABS32',
    3: 'R_ARM_REL32',
    10: 'R_ARM_THM_CALL',
    28: 'R_ARM_CALL',
    29: 'R_ARM_JUMP24',
    30: 'R_ARM_THM_JUMP24',
}

# The permuter's ARM parser (src/objdump.py:process_arm32_reloc) only accepts these
# three spellings, so an object carrying another kind cannot be diffed at all.
SUPPORTED_RELOCATIONS = {'R_ARM_ABS32', 'R_ARM_THM_CALL', 'R_ARM_CALL'}

MAPPING_KINDS = {'$a': 'arm', '$t': 'thumb', '$d': 'data'}


def load_object(path):
    """Return (text, text_index, mapping, relocations) for the .text section."""
    with open(path, 'rb') as stream:
        elf = ELFFile(stream)
        if elf['e_ident']['EI_DATA'] != 'ELFDATA2LSB':
            raise SystemExit(f'{path}: only little-endian ARM objects are supported')
        text_section = elf.get_section_by_name('.text')
        if text_section is None or text_section['sh_type'] == 'SHT_NOBITS':
            raise SystemExit(f'{path}: no .text section')
        text = text_section.data()
        text_index = next(index for index, section in enumerate(elf.iter_sections())
                          if section.name == '.text')
        symtab = elf.get_section_by_name('.symtab')
        if symtab is None:
            raise SystemExit(f'{path}: no .symtab; cannot name relocation targets')

        mapping = []
        for symbol in symtab.iter_symbols():
            kind = MAPPING_KINDS.get(symbol.name)
            if kind and symbol['st_shndx'] == text_index and 0 <= symbol['st_value'] < len(text):
                mapping.append((symbol['st_value'], kind))
        mapping.sort()

        relocations = []
        for section in elf.iter_sections():
            if section.name not in ('.rel.text', '.rela.text'):
                continue
            rela = section.name == '.rela.text'
            for relocation in section.iter_relocations():
                offset = relocation['r_offset']
                if offset >= len(text):
                    continue
                kind = RELOCATION_NAMES.get(relocation['r_info_type'])
                if kind is None:
                    raise SystemExit(
                        f'{path}: relocation type {relocation["r_info_type"]} at '
                        f'offset {offset:#x} has no R_ARM_ name in this shim')
                if kind not in SUPPORTED_RELOCATIONS:
                    raise SystemExit(
                        f'{path}: relocation {kind} at offset {offset:#x} is not one of '
                        f'{sorted(SUPPORTED_RELOCATIONS)}; decomp-permuter cannot parse it')
                symbol = symtab.get_symbol(relocation['r_info_sym']).name
                if not symbol:
                    raise SystemExit(f'{path}: relocation at {offset:#x} has an unnamed symbol')
                relocations.append((offset, kind, symbol))
        relocations.sort()
    return text, text_index, mapping, relocations


def infer_mode(mapping):
    """Mapping symbols decide the mode of a region with no explicit $a/$t at its start."""
    for _, kind in mapping:
        if kind == 'thumb':
            return 'thumb'
        if kind == 'arm':
            return 'arm'
    return 'arm'


def regions(text, mapping, default_mode):
    """Split .text into (start, end, kind) code/data regions.

    mwccarm emits a mapping symbol at the start of the code and again where the
    literal pool begins, so the pool is rendered as data rather than disassembled
    into plausible-looking garbage.
    """
    if not mapping:
        return [(0, len(text), default_mode)]
    out = []
    if mapping[0][0] > 0:
        out.append((0, mapping[0][0], default_mode))
    for index, (start, kind) in enumerate(mapping):
        end = mapping[index + 1][0] if index + 1 < len(mapping) else len(text)
        if end > start:
            out.append((start, end, kind))
    return out


def hex_bytes(raw):
    if len(raw) == 2:
        return f'{int.from_bytes(raw, "little"):04x}'
    return raw.hex()


def render(path, mode_override=None):
    text, _, mapping, relocations = load_object(path)
    default_mode = mode_override or infer_mode(mapping)

    by_offset = {}
    for offset, kind, symbol in relocations:
        by_offset.setdefault(offset, []).append((kind, symbol))

    lines = [f'{Path(path).name}:     file format elf32-littlearm',
             '',
             'Disassembly of section .text:',
             '',
             '00000000 <.text>:']

    emitted = 0
    for start, end, kind in regions(text, mapping, default_mode):
        if kind == 'data':
            emitted += emit_data(lines, text, start, end, by_offset)
            continue
        cs_mode = CS_MODE_THUMB if kind == 'thumb' else CS_MODE_ARM
        engine = Cs(CS_ARCH_ARM, CS_MODE_LITTLE_ENDIAN | cs_mode)
        covered = start
        for instruction in engine.disasm(text[start:end], start):
            lines.append(f'  {instruction.address:4x}:\t'
                         f'{hex_bytes(instruction.bytes):<16}\t'
                         f'{instruction.mnemonic}\t{instruction.op_str}'.rstrip())
            emitted += 1
            covered = instruction.address + len(instruction.bytes)
            for reloc_kind, symbol in by_offset.pop(instruction.address, ()):
                lines.append(f'\t\t\t{instruction.address:4x}: {reloc_kind}\t{symbol}')
        # Capstone stops at an undecodable tail; emit it as data so offsets stay honest.
        if covered < end:
            emitted += emit_data(lines, text, covered, end, by_offset)

    for offset in sorted(by_offset):
        for reloc_kind, symbol in by_offset[offset]:
            lines.append(f'\t\t\t{offset:4x}: {reloc_kind}\t{symbol}')
    if emitted == 0:
        raise SystemExit(f'{path}: .text is empty')
    return '\n'.join(lines) + '\n'


def emit_data(lines, text, start, end, by_offset):
    """Render a data region one 32-bit word per row (mwcc pools are word-aligned)."""
    emitted = 0
    for offset in range(start, end, 4):
        word = text[offset:offset + 4]
        if len(word) < 4:
            word = word + b'\0' * (4 - len(word))
        value = int.from_bytes(word, 'little')
        lines.append(f'  {offset:4x}:\t{word.hex():<16}\t.word\t0x{value:x}')
        emitted += 1
        for reloc_kind, symbol in by_offset.pop(offset, ()):
            lines.append(f'\t\t\t{offset:4x}: {reloc_kind}\t{symbol}')
    return emitted


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('object', help='relocatable ARM ELF object produced by mwccarm')
    parser.add_argument('--mode', choices=('arm', 'thumb'),
                        help='force the instruction set (default: read mwcc mapping symbols)')
    args = parser.parse_args(argv)
    if not Path(args.object).is_file():
        print(f'{args.object}: not a file', file=sys.stderr)
        return 1
    try:
        sys.stdout.write(render(args.object, args.mode))
    except (SystemExit, OSError) as error:
        print(str(error) if not isinstance(error, SystemExit) else error.code,
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
