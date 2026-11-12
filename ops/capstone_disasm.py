"""Capstone disassembly text in the pinned LLVM objdump's rendering.

``ops/transcribe_chunk.py`` reads the private disassembler text from
``ops/disasm.py``, which shells out to the pinned LLVM objdump. That toolchain is
not installed in this checkout, so this module produces the same text from the
Capstone binding instead: ``--no-show-raw-insn`` layout, one instruction per
line, address then mnemonic then operands. The dialect differences that matter to
the transcriber are normalised here (Capstone prefixes a branch target with ``#``
and names the IA block transfer ``ldm``); everything else is passed through and
corrected by ``transcribe_chunk``'s own spelling tables.
"""
import json
import re
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

ROOT = Path(__file__).resolve().parent.parent


def module_image(name, root=ROOT):
    manifest = json.loads((Path(root) / 'manifest.json').read_text(encoding='utf-8-sig'))
    for module in manifest['modules']:
        if module['name'] == name:
            return Path(root) / module['binary'], int(module['base'], 0)
    raise SystemExit('unknown module: ' + name)


def disassemble_text(root, name, address, size, mode='arm'):
    path, base = module_image(name, root)
    image = path.read_bytes()
    offset = address - base
    if offset < 0 or offset + size > len(image):
        raise SystemExit('range lies outside the module image')
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    aliases = {'sb': 'r9', 'sl': 'r10', 'fp': 'r11', 'ip': 'r12'}
    lines = []
    for ins in md.disasm(image[offset:offset + size], address):
        mnemonic, operands = ins.mnemonic, ins.op_str
        for alias, register in aliases.items():
            operands = re.sub(r'\b%s\b' % alias, register, operands)
        operands = re.sub(r'\b(r\d+)!', r'\1 !', operands)
        if operands.startswith('#'):
            operands = '#' + operands[1:]
        if mnemonic.startswith('b') and operands.startswith('#'):
            # LLVM prints a branch target bare; Capstone writes the immediate '#'.
            operands = operands[1:]
        if mnemonic in ('ldm', 'ldmib', 'ldmda', 'ldmdb'):
            # The transcriber's spelling table keys on the addressing mode that
            # LLVM prints in the mnemonic (``ldmia``); Capstone drops the IA.
            mnemonic = mnemonic + 'ia' if mnemonic == 'ldm' else mnemonic
        if mnemonic in ('stm', 'stmib', 'stmda', 'stmdb'):
            mnemonic = mnemonic + 'ia' if mnemonic == 'stm' else mnemonic
        lines.append('%8x:\t%s\t%s' % (ins.address, mnemonic, operands))
    return '\n'.join(lines) + '\n'


def install():
    """Point ``ops/disasm.py``'s ``disassemble`` at the Capstone renderer."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import disasm
    disasm.disassemble = disassemble_text
    return disasm
