"""Compile three plausible C bodies per transcribed row: the C-first evidence.

Rounds 7 and 8 shipped a row as assembly only after compiling plausible C bodies
and diffing them against the measured extent.  This driver does the same for the
sweep-1 transcriptions: three bodies (a field read, a byte/word copy loop, and a
block-struct copy) are compiled through ``ops/probe_c.py`` on the row's own rule
and the whole extent is compared after relocation patching.  The per-row closest
result is pinned in ``ops/ov006_sweep1_cattempts.json``.

    python ops/probe_ov006_sweep1.py            # probe every transcribed row
    python ops/probe_ov006_sweep1.py --record   # refresh the pinned result
    python ops/probe_ov006_sweep1.py --plan ops/ov006_sweep2_plan.json \\
        --result ops/ov006_sweep2_cattempts.json --work work/ov006-sweep2/cprobes --record
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import probe_c  # noqa: E402
import source_units  # noqa: E402

PLAN = Path(__file__).resolve().parent / 'ov006_sweep1_plan.json'
RESULT = Path(__file__).resolve().parent / 'ov006_sweep1_cattempts.json'

BODIES = {
    'field-read': '''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

u32 probe(u32 a0)
{
    return *(volatile u32 *)(a0 + 4);
}
''',
    'copy-loop': '''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

void probe(u32 *dst, u32 *src, u32 count)
{
    do {
        *dst++ = *src++;
    } while (--count);
}
''',
    'block-struct': '''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

typedef struct {
    u32 words[8];
} Block;

void probe(Block *dst, Block *src)
{
    *dst = *src;
}
''',
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--plan', type=Path, default=PLAN,
                        help='plan JSON (default: ops/ov006_sweep1_plan.json)')
    parser.add_argument('--result', type=Path, default=RESULT,
                        help='pinned result JSON (default: ops/ov006_sweep1_cattempts.json)')
    parser.add_argument('--work', type=Path, default=ROOT / 'work/ov006-sweep1/cprobes',
                        help='scratch directory for the probe translation units')
    args = parser.parse_args(argv)
    config = source_units.load_config(ROOT)
    plan = json.loads(args.plan.read_text())
    probes = args.work
    probes.mkdir(parents=True, exist_ok=True)
    ledger = probe_c.ledger_rows(ROOT)
    rows = {}
    exact = 0
    total = 0
    keys = plan.get('asm') or (plan.get('asmSingleton', []) + plan.get('asmDuplicatePool', []))
    for key in keys:
        address = int(key, 16)
        row = ledger[('ov006', address)]
        profile = 'p033' if row.get('mode') == 'thumb' else 'p003'
        entry = {}
        for name, body in BODIES.items():
            path = probes / ('probe_ov006_%s_%s.c' % (key, name))
            path.write_text(body, encoding='ascii')
            result = probe_c.probe(config, 'ov006', address, path,
                                   list(config['profiles'][profile]))
            total += 1
            exact += not result['diff'] and result['length'] == result['bytes']
            entry[name] = {'length': result['length'], 'bytes': result['bytes'],
                           'relocations': result['relocations'],
                           'diffBytes': len(result['diff']) + abs(result['length'] - result['bytes']),
                           'firstDiff': result['diff'][:6]}
        rows[key] = entry
    closest = min(entry[min(entry, key=lambda name: entry[name]['diffBytes'])]['diffBytes']
                  for entry in rows.values())
    summary = {'rows': len(rows), 'compilations': total, 'exact': exact,
               'closestDiffBytes': closest}
    print('%d rows, %d compilations, %d exact; closest body %d bytes off'
          % (len(rows), total, exact, closest))
    if args.record:
        args.result.write_text(json.dumps({'summary': summary, 'rows': rows}, indent=1) + '\n')
        print('written', args.result)
    return 0 if exact == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
