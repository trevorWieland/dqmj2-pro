"""The C-first screen for the sweep-3 population: six plausible bodies per row.

Round 10-12 practice: a row ships as transcribed assembly only after plausible C
bodies were compiled through the row's own rule and diffed against the measured
extent.  This driver does that for the sweep-3 plan with six bodies: the three the
earlier sweeps used (a field read, a copy loop, a block-struct copy) plus three of
the form rules this round names, because each pins a shape the compiler can only
produce one way:

* ``m2c-field``      - ``extern u8`` array indexed through ``M2C_FIELD`` (a struct
                       view of a global), the project's ordinary measured-field form;
* ``rematerialise``  - ``u16 *const`` re-read after a call, which is how a post-call
                       rematerialised pointer is spelled;
* ``bitfield-flag``  - ``unsigned :1`` on a control word, the one-bit-flag form.

``volatile``/named-temp/declaration-order variants are how a *nearly* matching body
is nudged into place; they are worth spending only on a body that is already close,
and here the closest is 28 bytes off with every row's body a distinct call sequence,
so the C form of these rows is not recoverable from the extent in this round.

The per-row result is pinned in ``ops/ov006_sweep3_cattempts.json``; ``--resume``
keeps the rows already pinned and probes only the new ones.

    python ops/probe_ov006_sweep3.py --record     # 810 compilations, 0 exact
    python ops/probe_ov006_sweep3.py --resume --record
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

PLAN = ROOT / 'ops/ov006_sweep3_plan.json'
RESULT = ROOT / 'ops/ov006_sweep3_cattempts.json'

TYPES = ('typedef unsigned char u8;\ntypedef unsigned short u16;\n'
         'typedef unsigned int u32;\ntypedef signed int s32;\n')

BODIES = {
    'field-read': TYPES + '''
u32 probe(u32 a0)
{
    return *(volatile u32 *)(a0 + 4);
}
''',
    'copy-loop': TYPES + '''
void probe(u32 *dst, u32 *src, u32 count)
{
    do {
        *dst++ = *src++;
    } while (--count);
}
''',
    'block-struct': TYPES + '''
typedef struct {
    u32 words[8];
} Block;

void probe(Block *dst, Block *src)
{
    *dst = *src;
}
''',
    'm2c-field': TYPES + '''
#define M2C_FIELD(expr, type, offset) (*(type *)((char *)(expr) + (offset)))

extern u8 data_0221c05c[];

u32 probe(u32 a0)
{
    return M2C_FIELD(data_0221c05c, u32, 0x34) + M2C_FIELD(a0, u16, 0x2);
}
''',
    'rematerialise': TYPES + '''
extern u32 fn_021f37f0(u32 a0, u32 a1, u32 a2);

u32 probe(u32 a0)
{
    u16 *const record = (u16 *)(a0 + 6);

    fn_021f37f0(a0, record[3], record[1]);
    return record[2];
}
''',
    'bitfield-flag': TYPES + '''
typedef struct {
    u32 pad0 : 12;
    u32 flags : 2;
    unsigned enabled : 1;
    u32 pad1 : 17;
} Control;

u32 probe(volatile Control *control, u32 a1)
{
    if (!control->enabled) {
        return 0;
    }
    control->flags = (control->flags & ~3u) | 3u;
    return a1 + 0xc;
}
''',
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--resume', action='store_true',
                        help='keep rows already in the pinned result and probe only new ones')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args(argv)
    config = source_units.load_config(ROOT)
    plan = json.loads(PLAN.read_text())
    probes = ROOT / 'work/ov006-sweep3/cprobes'
    probes.mkdir(parents=True, exist_ok=True)
    ledger = probe_c.ledger_rows(ROOT)
    keys = (plan['asmTranscribed'] + plan.get('asmDataCarrier', []))
    keys = keys[:args.limit] if args.limit else keys
    rows = {}
    if args.resume and RESULT.is_file():
        rows = json.loads(RESULT.read_text())['rows']
    exact = 0
    total = 0
    for key in keys:
        if key in rows:
            continue
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
            off = len(result['diff']) + abs(result['length'] - result['bytes'])
            exact += 1 if not off else 0
            entry[name] = {'length': result['length'], 'bytes': result['bytes'],
                           'relocations': result['relocations'],
                           'diffBytes': off, 'firstDiff': result['diff'][:6]}
        rows[key] = entry
        if total % 60 == 0:
            print('... %d compilations' % total, flush=True)
    closest = min(min(body['diffBytes'] for body in entry.values())
                  for entry in rows.values()) if rows else 0
    closest_key = min(rows, key=lambda k: min(b['diffBytes'] for b in rows[k].values()))
    summary = {'rows': len(rows), 'bodies': len(BODIES),
               'compilations': len(rows) * len(BODIES),
               'exact': exact, 'closestDiffBytes': closest,
               'closestRow': closest_key}
    print(json.dumps(summary))
    if args.record:
        RESULT.write_text(json.dumps({'summary': summary, 'rows': rows}, indent=1) + '\n')
        print('written', RESULT.relative_to(ROOT))
    return 0 if not exact else 1


if __name__ == '__main__':
    sys.exit(main())
