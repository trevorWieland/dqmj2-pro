"""Rank unmatched ledger rows by how much of their body is an aggregate-copy shape.

Round 6 closed a small aggregate-copy/chunking class (7 rows, 556 B) that was found
by looking at the *image* instead of a parked failure table. This scanner does that
look exhaustively over every module: it decodes each unmatched row's measured bytes
and counts the instruction shapes a C compiler would not emit for a struct copy:

* a multi-register block transfer with base writeback (ARM ``ldmia rN!`` /
  ``stmia rN!``, Thumb ``ldmia rN!`` / ``stmia rN!``), because mwccarm keeps them
  only in specific copy idioms;
* a *predicated* multi-register transfer (``ldmneia`` / ``stmltia`` / ...), which
  no C expression produces at all on this target;
* a run-group of at least four consecutive word ``str``/``ldr`` off one base with a
  regular stride, which is what an unrolled copy looks like when C emits a loop.

Ranking is by shape-instruction count, then by row size, exactly as the round-6
triage ordered its candidates.

Thumb rows are decoded in their own mode (``--thumb`` restricts the scan to them):
the 16-bit ``ldm``/``stm`` register-list forms are the writeback blocks, word
``ldr``/``str`` immediates form the run groups, and ``push``/``pop`` are decoded
but not scored because an ``sp`` frame is not a copy. Run adjacency uses a 2-byte
stride for Thumb and 4 for ARM. ``--pool`` keeps only rows matching the copy
triage pool (predicated block, two or more writeback blocks, or a word run) and the
JSON/console summary reports pool and Thumb totals separately.

    python ops/scan_chunk_shapes.py                     # every module, ranked table
    python ops/scan_chunk_shapes.py --module main --top 40
    python ops/scan_chunk_shapes.py --thumb --pool --json work/chunk-thumb.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARM_BLOCK = 0x08000000      # bits 27..25 == 100
ARM_BLOCK_MASK = 0x0E000000
ARM_WRITEBACK = 0x00200000
ARM_LOAD = 0x00100000
ARM_REGCOUNT = 16
# A run group is a chain of word loads/stores off one base with a fixed stride.
RUN_MINIMUM = 4


def popcount(value):
    return bin(value).count('1')


def arm_decode(code, address):
    """Yield (offset, word, shape) for each ARM instruction in the measured body."""
    for offset in range(0, len(code) - 3, 4):
        word = int.from_bytes(code[offset:offset + 4], 'little')
        condition = word >> 28
        shape = None
        if (word & ARM_BLOCK_MASK) == ARM_BLOCK:
            registers = word & 0xFFFF
            base = (word & 0x000F0000) >> 16
            if popcount(registers) >= 2 and base != 13:   # sp! frames are not a copy
                load = bool(word & ARM_LOAD)
                writeback = bool(word & ARM_WRITEBACK)
                kind = 'ldm' if load else 'stm'
                if condition != 0xE:
                    shape = ('predicated-block', kind, condition, popcount(registers))
                elif writeback:
                    shape = ('writeback-block', kind, condition, popcount(registers))
        elif ((word & 0x0C000000) == 0x04000000 and (word & 0x02000000) == 0
              and (word & 0x00000010) == 0 and (word & 0x00400000) == 0):
            # ldr/str, immediate offset, word sized (bit 22 clear), no byte transfer.
            load = bool(word & 0x00100000)
            base = (word & 0x000F0000) >> 16
            shape = ('word-group', 'ldr' if load else 'str', base, word & 0xFFF,
                     bool(word & 0x00800000), bool(word & 0x00200000))
        yield offset, word, shape


def thumb_decode(code, address):
    """Yield (offset, halfword-size, shape) for each Thumb instruction.

    Thumb-1 has no predicated block transfers, so the only shapes are the
    16-bit ``ldmia rN!``/``stmia rN!`` (register list r0-r7, base writeback) and
    the word ``ldr``/``str`` immediate forms. ``push``/``pop`` are the
    ``stmdb sp!``/``ldmia sp!`` equivalents and are decoded but deliberately not
    scored: an ``sp`` frame is not a copy. The 32-bit ``BL``/``BLX`` pair is
    skipped as one instruction; treating the second halfword as an opcode is the
    bug the first Thumb scan run hit.
    """
    offset = 0
    while offset < len(code) - 1:
        halfword = int.from_bytes(code[offset:offset + 2], 'little')
        size = 2
        shape = None
        if (halfword & 0xF800) == 0xC000 or (halfword & 0xF800) == 0xC800:
            registers = halfword & 0xFF
            if popcount(registers) >= 2:
                kind = 'ldm' if (halfword & 0x0800) else 'stm'
                shape = ('writeback-block', kind, 0xE, popcount(registers))
        elif (halfword & 0xF800) == 0x6800 or (halfword & 0xF800) == 0x6000:
            base = (halfword >> 3) & 0x7
            shape = ('word-group', 'ldr' if (halfword & 0xF800) == 0x6800 else 'str',
                     base, (halfword & 0x7F) * 4, False, False)
        elif (halfword & 0xF800) == 0xF000:
            # First half of a 32-bit BL/BLX; its second half is not an opcode.
            size = 4
        yield offset, size, shape
        offset += size


def body_shapes(code, address, mode):
    """Count the copy shapes in one measured body and return the evidence rows."""
    found = []
    instructions = 0
    if mode == 'arm':
        decoded = list(arm_decode(code, address))
        stride = 4
    else:
        decoded = list(thumb_decode(code, address))
        stride = 2
    for offset, word, shape in decoded:
        instructions += 1
        if shape is None:
            continue
        if shape[0] == 'predicated-block':
            found.append((offset, shape[0], shape[1], shape[3]))
        elif shape[0] == 'writeback-block':
            found.append((offset, shape[0], shape[1], shape[3]))
    # Run groups: adjacent word ldr/str off one base with a fixed +4 stride.
    words = [(offset, shape[1], shape[2], shape[3], shape[4]) for offset, _word, shape in decoded
             if shape and shape[0] == 'word-group']
    chain = []
    previous = None
    for offset, operation, base, immediate, up in words:
        if base == 13:
            continue
        if previous is not None:
            p_offset, p_operation, p_base, p_immediate, p_up = previous
            if (base == p_base and operation == p_operation and up and p_up
                    and immediate == p_immediate + 4 and offset == p_offset + stride):
                chain.append(offset)
                previous = (offset, operation, base, immediate, up)
                continue
            if len(chain) + 1 >= RUN_MINIMUM:
                found.extend((item, 'word-run', operation, 0) for item in chain)
            chain = []
        previous = (offset, operation, base, immediate, up)
    if previous is not None and len(chain) + 1 >= RUN_MINIMUM:
        found.extend((item, 'word-run', previous[1], 0) for item in chain)
    return instructions, found


def classify(shapes):
    """Fold the shape evidence into the three class hints the triage ranks on."""
    predicated = sum(1 for shape in shapes if shape[1] == 'predicated-block')
    writeback = sum(1 for shape in shapes if shape[1] == 'writeback-block')
    runs = sum(1 for shape in shapes if shape[1] == 'word-run')
    return predicated, writeback, runs


def load_rows(root):
    rows = []
    for line in (root / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if not row.get('bytes'):
            continue
        rows.append(row)
    return rows


def module_images(root):
    config = json.loads((root / 'config/source_units.json').read_text(encoding='utf-8-sig'))
    images = {}
    for name, module in config['modules'].items():
        path = root / module['originalImage']
        if path.is_file():
            images[name] = (path, int(str(module['loadAddressBase']), 0), module['processor'])
    return images


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--module', default=None)
    parser.add_argument('--top', type=int, default=25)
    parser.add_argument('--thumb', action='store_true',
                        help='only scan rows whose ledger mode is thumb')
    parser.add_argument('--pool', action='store_true',
                        help='only rows that pass the copy triage pool '
                             '(predicated block, >=2 writeback blocks, or a word run)')
    parser.add_argument('--class-hint', choices=('predicated', 'writeback', 'run'),
                        default=None, help='only rows carrying that shape')
    parser.add_argument('--max-bytes', type=int, default=None)
    parser.add_argument('--json', dest='json_path', type=Path, default=None)
    parser.add_argument('--all-rows', action='store_true',
                        help='scan matched rows too (default: unmatched only)')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    images = module_images(root)
    rows = load_rows(root)
    scanning = sorted(images)
    if args.module:
        scanning = [name for name in scanning if name == args.module]
        if not scanning:
            parser.error('unknown module: ' + args.module)
    summary = {}
    ranked = []
    for name in scanning:
        path, base, processor = images[name]
        image = path.read_bytes()
        module_rows = [row for row in rows if row['module'] == name
                       and (args.all_rows or not row['states'].get('functionMatched'))
                       and (not args.thumb or row['mode'] == 'thumb')]
        ranked_module = []
        for row in module_rows:
            offset = int(row['binaryOffset'])
            size = int(row['bytes'])
            if args.max_bytes is not None and size > args.max_bytes:
                continue
            code = image[offset:offset + size]
            if len(code) != size:
                continue
            instructions, shapes = body_shapes(code, int(row['address'], 16), row['mode'])
            if not shapes:
                continue
            predicated, writeback, runs = classify(shapes)
            if args.class_hint == 'predicated' and not predicated:
                continue
            if args.class_hint == 'writeback' and writeback < 2:
                continue
            if args.class_hint == 'run' and runs < RUN_MINIMUM:
                continue
            in_pool = bool(predicated) or writeback >= 2 or runs > 0
            if args.pool and not in_pool:
                continue
            ranked_module.append({
                'module': name, 'address': row['address'], 'bytes': size,
                'mode': row['mode'], 'instructions': instructions,
                'score': len(shapes), 'predicatedBlocks': predicated,
                'writebackBlocks': writeback, 'runInstructions': runs,
                'pool': in_pool,
                'density': round(len(shapes) / instructions, 3),
            })
        # Predicated transfers first (C cannot express them), then writeback runs,
        # then shape count, then the smaller row: the round-6 triage order.
        ranked_module.sort(key=lambda item: (-item['predicatedBlocks'],
                                             -item['writebackBlocks'],
                                             -item['score'], item['bytes'],
                                             item['address']))
        pool = [item for item in ranked_module if item['pool']]
        summary[name] = {
            'unmatchedRows': len(module_rows),
            'candidates': len(ranked_module),
            'shapeInstructions': sum(item['score'] for item in ranked_module),
            'shapeBytes': sum(item['bytes'] for item in ranked_module),
            'predicatedRows': sum(1 for item in ranked_module if item['predicatedBlocks']),
            'writebackRows': sum(1 for item in ranked_module if item['writebackBlocks'] >= 2),
            'runRows': sum(1 for item in ranked_module if item['runInstructions']),
            'thumbRows': sum(1 for item in ranked_module if item['mode'] == 'thumb'),
            'thumbBytes': sum(item['bytes'] for item in ranked_module
                              if item['mode'] == 'thumb'),
            'poolRows': len(pool),
            'poolBytes': sum(item['bytes'] for item in pool),
            'thumbPoolRows': sum(1 for item in pool if item['mode'] == 'thumb'),
            'thumbPoolBytes': sum(item['bytes'] for item in pool
                                  if item['mode'] == 'thumb'),
            'top': ranked_module[:args.top],
        }
        ranked.extend(ranked_module)
        print(f'{name:6s} unmatched={len(module_rows):5d} candidates={len(ranked_module):4d} '
              f'pool={len(pool):4d} thumbPool={summary[name]["thumbPoolRows"]:4d} '
              f'predicated={summary[name]["predicatedRows"]:4d} '
              f'writeback={summary[name]["writebackRows"]:4d} '
              f'runs={summary[name]["runRows"]:4d} '
              f'bytes={summary[name]["shapeBytes"]:6d} '
              f'thumbBytes={summary[name]["thumbBytes"]:6d}')
        for item in ranked_module[:args.top]:
            print(f'   {item["address"]:>10s} {item["bytes"]:4d} B {item["mode"]:5s} '
                  f'score={item["score"]:2d} wb={item["writebackBlocks"]:2d} '
                  f'pred={item["predicatedBlocks"]:2d} run={item["runInstructions"]:2d} '
                  f'pool={int(item["pool"])} density={item["density"]:.2f}')
    ranked.sort(key=lambda item: (-item['predicatedBlocks'], -item['writebackBlocks'],
                                  -item['score'], item['bytes']))
    print(f'\n{sum(value["candidates"] for value in summary.values())} candidate rows, '
          f'{sum(value["shapeBytes"] for value in summary.values())} bytes, '
          f'{sum(value["predicatedRows"] for value in summary.values())} predicated rows, '
          f'{sum(value["poolRows"] for value in summary.values())} pool rows '
          f'({sum(value["poolBytes"] for value in summary.values())} bytes), '
          f'{sum(value["thumbRows"] for value in summary.values())} thumb rows '
          f'({sum(value["thumbBytes"] for value in summary.values())} bytes)')
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps({'modules': summary, 'ranked': ranked}, indent=1) + '\n',
                                  encoding='utf-8')
        print(f'report written: {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
