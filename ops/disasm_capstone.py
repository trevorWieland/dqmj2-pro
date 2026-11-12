"""Disassemble a measured function with capstone, rendering ``llvm-objdump`` text.

``ops/disasm.py`` shells out to the pinned LLVM ``llvm-objcopy``/``llvm-objdump``
from ``tools/android-ndk``.  A replay that has the module images and ``manifest.json``
but not that archive cannot regenerate a lane at all, and regeneration is what the
source-form rules require ("the body is the measured stream").  This module is the
documented fallback: same signature, same output shape, capstone as the decoder.

The text is deliberately *not* claimed to be byte-for-byte LLVM's.  What is claimed
is that feeding it to ``ops/transcribe_chunk.py`` reproduces the same instruction
stream: the acceptance test is the lane verifier, which compiles the emitted
``asm`` body and compares the whole measured extent with the image.  The renderer is
calibrated by regenerating every committed ``ov006`` sweep-1/sweep-2 row through it
and re-verifying against those lanes' pinned fixtures.

Spellings the transcriber depends on, and how each is rendered here:

* a branch operand is ``0x<target>`` with no ``#`` (``transcribe_chunk.branch_target``
  parses that form and substitutes the row-local label or the ``native_fn_`` symbol);
* ``push``/``pop`` keep capstone's alias spelling for both modes; the transcriber
  rewrites an ARM one to ``stmdb sp!``/``ldmia sp!``;
* a Thumb block transfer keeps its writeback ``!`` only when capstone printed it;
* immediates print as decimal for the data-processing forms and as hex inside a
  memory operand.  Both assemble identically; the split is only cosmetic.

    python ops/disasm_capstone.py --module ov006 --address 0x21ed198 --bytes 48 --mode thumb
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import disasm  # noqa: E402

BRANCH_MNEMONICS = frozenset((
    'b', 'bl', 'bx', 'blx', 'bxj',
    'beq', 'bne', 'bcs', 'bhs', 'bcc', 'blo', 'bmi', 'bpl', 'bvs', 'bvc',
    'bhi', 'bls', 'bge', 'blt', 'bgt', 'ble', 'bal', 'bnv',
    'blxeq', 'blxne', 'bleq', 'blne', 'blls', 'blhi', 'blgt', 'blle', 'bllt',
    'blge', 'blcs', 'blcc', 'blmi', 'blpl', 'blvs', 'blvc',
    'bxeq', 'bxne', 'bxlr',
))
IMMEDIATE = re.compile(r'#(-?)(0x[0-9a-f]+|\d+)(?![\dx])')
ALIASES = {'sl': 'r10', 'sb': 'r9', 'fp': 'r11', 'ip': 'r12'}
ALIAS = re.compile(r'\b(sl|sb|fp|ip)\b')
CONDITIONS = ('eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc',
              'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al')
# ``llvm-objdump``'s ARM printer formats a memory offset in hex for the addressing
# mode the plain word/byte loads use and in decimal for the halfword and
# signed-byte family; every data-processing immediate is decimal.  The choice is
# cosmetic (both spellings assemble to the measured word), so it is made only to
# keep a regenerated row textually identical to its shipped counterpart.
ADDRMODE3 = ('ldrh', 'strh', 'ldrsb', 'ldrsh')


def _root(mnemonic):
    for condition in CONDITIONS:
        if mnemonic.endswith(condition) and len(mnemonic) > len(condition) + 1:
            return mnemonic[:-len(condition)]
    return mnemonic


SHIFT = re.compile(r'(?:lsl|lsr|asr|ror|rrx)\s*$')
# The pinned objdump declines the multiply family (it prints ``<unknown>`` and
# ``ops/transcribe_chunk.decode_dataproc`` re-spells it from the raw word), which
# spells register 14 as ``r14`` rather than ``lr``.  Matching that keeps the
# regenerate-and-diff check exact; both spellings assemble to the same word.
MULTIPLY = ('mul', 'mla', 'smull', 'umull', 'smlal', 'umlal', 'smulbb', 'smulwb')


def _spell(mnemonic, operands):
    if _root(mnemonic) in MULTIPLY:
        return re.sub(r'\blr\b', 'r14', operands)
    return operands


def _arm_operands(mnemonic, operands):
    """ARM operand spelling: immediates as the pinned LLVM printer writes them."""
    hex_in_memory = _root(mnemonic) not in ADDRMODE3
    out = []
    depth = 0
    index = 0
    while index < len(operands):
        character = operands[index]
        if character == '[':
            depth += 1
        elif character == ']':
            depth -= 1
        if character == '#':
            match = IMMEDIATE.match(operands, index)
            if match:
                value = int(match.group(2), 0)
                sign = match.group(1) or ''
                if not sign and value > 0x7FFFFFFF:
                    sign, value = '-', 0x100000000 - value
                shift = bool(SHIFT.search(''.join(out)))
                if depth > 0 and hex_in_memory and not shift:
                    out.append('#%s0x%x' % (sign, value))
                else:
                    out.append('#%s%d' % (sign, value))
                index = match.end()
                continue
        out.append(character)
        index += 1
    return ''.join(out)


def _operands(instruction, mode='arm'):
    """capstone operands, rendered the way the pinned LLVM objdump renders them.

    The spelling never changes the encoding; it is matched so a regenerated row is
    textually identical to the shipped one, which makes the whole committed lane a
    free regression corpus for this renderer.
    """
    if instruction.mnemonic in BRANCH_MNEMONICS:
        return ALIAS.sub(lambda match: ALIASES[match.group(1)],
                         instruction.op_str.strip().lstrip('#'))
    operands = ALIAS.sub(lambda match: ALIASES[match.group(1)], instruction.op_str)
    operands = _spell(instruction.mnemonic, operands)
    if mode == 'arm':
        return _arm_operands(instruction.mnemonic, operands)
    return IMMEDIATE.sub(lambda match: '#%s0x%x' % (match.group(1) or '',
                                                   int(match.group(2), 0)),
                         operands)


def _machine(mode):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
    if mode == 'thumb':
        handle = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    else:
        handle = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
    handle.detail = False
    return handle


def instructions(code, address, mode='arm'):
    """Yield ``(address, mnemonic, operands)`` for every unit, past bad words too.

    ``llvm-objdump`` prints ``<unknown>`` and keeps decoding; capstone's ``disasm``
    stops the whole run at the first word it cannot decode.  The measured extent of
    a row includes its literal pool, and the transcriber's shape description reads
    the whole extent, so stopping early would silently change a row's header (a pool
    word that decodes as ``stmia`` becomes unreachable).  Decoding one unit at a
    time and advancing by the unit width keeps the two decoders aligned.
    """
    machine = _machine(mode)
    step = 2 if mode == 'thumb' else 4
    offset = 0
    while offset + step <= len(code):
        window = code[offset:offset + 4]
        found = next(iter(machine.disasm(window, address + offset)), None)
        if found is None:
            yield address + offset, '<unknown>', ''
            offset += step
            continue
        yield found.address, found.mnemonic, _operands(found, mode)
        offset += found.size
    if offset < len(code):
        # A trailing partial unit cannot be an instruction; render it as unknown so
        # a caller still sees that the extent does not divide evenly.
        yield address + offset, '<unknown>', ''


def disassemble(root, name, address, size, mode='arm'):
    """Render ``size`` bytes at ``address`` as ``llvm-objdump -d`` style text."""
    image_path, base = disasm.module_image(root, name)
    image = image_path.read_bytes()
    offset = address - base
    if offset < 0 or offset + size > len(image):
        raise SystemExit('range lies outside the module image')
    code = image[offset:offset + size]
    lines = ['%8x:\t%s\t%s' % (at, mnemonic, operands)
             for at, mnemonic, operands in instructions(code, address, mode)]
    return '\n'.join(lines) + '\n' if lines else ''


def install():
    """Point ``ops/transcribe_chunk.py``'s ``disasm`` module at this renderer.

    ``transcribe_chunk`` imports ``disasm`` as a module and calls
    ``disasm.disassemble``; replacing the attribute keeps the committed
    transcriber untouched while making generation possible without the archive.
    """
    disasm.disassemble = disassemble


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--bytes', type=int, required=True)
    parser.add_argument('--mode', choices=('arm', 'thumb'), default='arm')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    sys.stdout.write(disassemble(args.root.resolve(), args.module, int(args.address, 0),
                                args.bytes, args.mode))
    return 0


if __name__ == '__main__':
    sys.exit(main())
