"""Enumerate the inline pc-relative jump-table class in one module.

Some rows dispatch through a table that lives inside their own measured extent.
This scanner finds them from the image and the ledger and proves the dispatch:
it decodes the ARM ``add pc, pc, rN, lsl #2`` form and the Thumb
``add rD, pc; ldrh rD, [rD, #n]; add pc, rD`` form, resolves the table address
from the instruction semantics, and only reports a row when a table entry names a
target inside the row.  A plain ``mov pc, lr`` return or a tail call through a
register is not a table and is not reported.

The two PC values differ and both matter:

* ARM ``add pc, pc, rN, lsl #2``: entry ``n`` is at ``site + 8 + 4n`` and is a
  branch word (``b target``), so it is still an instruction.
* Thumb ``add rD, pc`` (high registers): ``rD = rD + (site + 4)`` -- no alignment.
  The 16-bit entries that follow are *data*: signed byte offsets added to
  ``site + 4`` by ``add pc, rD``.
* Thumb ``add rD, pc, #imm``: ``rD = Align(site + 4, 4) + imm * 4``, then a
  ``ldrb``/``ldrh`` reads the entry.

    python ops/scan_jump_tables.py --module ov006
    python ops/scan_jump_tables.py --module ov006 --unclaimed work/unclaimed-ov006.json \
        --json work/jump-tables.json
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

CONDITIONS = ('eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc',
              'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al')


def ledger_rows(module):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module:
            yield row


def image_for(module):
    import source_units
    config = source_units.load_config(ROOT)
    entry = config['modules'][module]
    return (ROOT / entry['originalImage']).read_bytes()


def arm_branch_target(word, address):
    if (word & 0x0E000000) != 0x0A000000:
        return None
    immediate = word & 0xFFFFFF
    if immediate & 0x800000:
        immediate -= 0x1000000
    return address + 8 + (immediate << 2)


def arm_dispatch_offset(data):
    """Find an ARM ``add pc, pc, rN, <shift>`` dispatch word; return its offset."""
    for offset in range(0, len(data) - 3, 4):
        word = int.from_bytes(data[offset:offset + 4], 'little')
        if (word & 0x0C000000) != 0 or (word & 0x01100000):
            continue
        if ((word >> 21) & 0xF) != 4:            # ADD
            continue
        if ((word >> 16) & 0xF) != 15 or ((word >> 12) & 0xF) != 15:
            continue
        return offset, word
    return None, None


def thumb_halfwords(data):
    return [int.from_bytes(data[i:i + 2], 'little')
            for i in range(0, len(data) - 1, 2)]


def thumb_pc_base(halfword, address):
    """The table base established by ``add Rd, pc`` or ``add Rd, pc, #imm``."""
    if (halfword & 0xFF00) == 0x4400 and ((halfword >> 3) & 0xF) == 15:
        register = (halfword & 0x7) | ((halfword >> 4) & 0x8)
        return register, address + 4
    if (halfword & 0xF800) == 0xA000:
        register = (halfword >> 8) & 0x7
        return register, ((address + 4) & ~3) + (halfword & 0xFF) * 4
    return None


def thumb_pc_write(halfword):
    """The source register of ``add pc, Rm`` / ``mov pc, Rm``."""
    kind = halfword & 0xFF00
    if kind not in (0x4400, 0x4600):
        return None
    destination = (halfword & 0x7) | ((halfword >> 4) & 0x8)
    if destination != 15:
        return None
    return (halfword >> 3) & 0xF


def thumb_table(halfwords, dispatch_index, address, end, data):
    """Resolve the table address read before one Thumb pc write."""
    source = thumb_pc_write(halfwords[dispatch_index])
    site = address + dispatch_index * 2
    for look in range(dispatch_index - 1, max(-1, dispatch_index - 6) - 1, -1):
        load = halfwords[look]
        if (load & 0xF800) == 0x8800 and ((load >> 3) & 0x7) == source:
            offset, width = ((load >> 6) & 0x1F) * 2, 2
        elif (load & 0xF800) == 0x7800 and ((load >> 3) & 0x7) == source:
            offset, width = (load >> 6) & 0x1F, 1
        else:
            continue
        for back in range(look - 1, max(-1, look - 8) - 1, -1):
            base = thumb_pc_base(halfwords[back], address + back * 2)
            if base is None or base[0] != source:
                continue
            table = base[1] + offset
            if not (address <= table and table + width <= end):
                return None
            value = int.from_bytes(data[table - address:table - address + width],
                                   'little')
            if width == 2 and value & 0x8000:
                value -= 0x10000
            if width == 1:
                value &= 0xFF
            return dict(table=table, width=width, value=value,
                        target=site + 4 + value, site=site,
                        base=address + back * 2)
        return None
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--unclaimed', type=Path,
                        help='ops/unclaimed.py JSON report; only its unclaimed rows are scanned')
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    image = image_for(args.module)
    wanted = None
    if args.unclaimed:
        report = json.loads(args.unclaimed.read_text())
        wanted = {int(row['address'], 16) for row in report['rows']
                  if row['status'] == 'unclaimed'}
    found = []
    for row in ledger_rows(args.module):
        address, size = int(row['address'], 16), int(row['bytes'])
        if wanted is not None and address not in wanted:
            continue
        end = address + size
        data = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
        if row['mode'] == 'arm':
            offset, word = arm_dispatch_offset(data)
            if offset is None:
                continue
            site = address + offset
            table = site + 8
            entries = []
            at = table
            while at + 4 <= end:
                word_at = int.from_bytes(data[at - address:at - address + 4], 'little')
                target = arm_branch_target(word_at, at)
                if target is None or not (address <= target < end):
                    break
                entries.append(dict(at=at, target=target, word=word_at))
                at += 4
            if len(entries) < 2:
                continue
            found.append(dict(address=row['address'], bytes=size, mode='arm',
                              dispatch=site, table=table,
                              tableBytes=len(entries) * 4, entries=entries,
                              form='arm-add-pc-pc'))
            print('arm   %s %5d B dispatch=%08x table=%08x %3d B %2d entries' % (
                row['address'], size, site, table, len(entries) * 4, len(entries)))
        else:
            halfwords = thumb_halfwords(data)
            seen = set()
            for index, halfword in enumerate(halfwords):
                if thumb_pc_write(halfword) is None:
                    continue
                entry = thumb_table(halfwords, index, address, end, data)
                if entry is None or not (address <= entry['target'] < end):
                    continue
                key = (entry['table'], entry['site'])
                if key in seen:
                    continue
                seen.add(key)
                found.append(dict(address=row['address'], bytes=size, mode='thumb',
                                  dispatch=entry['site'], table=entry['table'],
                                  tableBytes=entry['width'],
                                  entries=[dict(at=entry['table'],
                                                target=entry['target'],
                                                word=entry['value'])],
                                  base=entry['base'], width=entry['width'],
                                  form='thumb-add-pc'))
                print('thumb %s %5d B dispatch=%08x table=%08x width=%d target=%08x' % (
                    row['address'], size, entry['site'], entry['table'],
                    entry['width'], entry['target']))
    total = sum(item['tableBytes'] for item in found)
    print('\n%d candidate(s), %d table byte(s)' % (len(found), total))
    if args.json:
        args.json.write_text(json.dumps(found, indent=1) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
