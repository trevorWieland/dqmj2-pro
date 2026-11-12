"""The C-first screen for the ov001 closing population: seven plausible bodies per row.

Practice from the ov006 sweeps: a row ships as transcribed assembly only after
plausible C bodies were compiled through the row's own rule and diffed against the
measured extent.  Six bodies are the shared screen the earlier sweeps used -- a field
read, a copy loop, a block-struct copy, an ``M2C_FIELD`` global read, a
post-call rematerialised pointer and a one-bit flag field -- and the seventh is
generated per row because this population's dominant shape is a *call sequence*:
the measured ``mov``/``bl`` argument setup is re-expressed as named calls so a row
that really is a call chain has a C form to match.

    python ops/probe_ov001_close.py --record     # 7 x rows compilations
    python ops/probe_ov001_close.py --resume --record
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import disasm  # noqa: E402
import disasm_capstone  # noqa: E402
import probe_c  # noqa: E402
import source_units  # noqa: E402
import transcribe_chunk  # noqa: E402

PLAN = ROOT / 'ops/ov001_close_plan.json'
RESULT = ROOT / 'ops/ov001_close_cattempts.json'

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

extern u8 data_021d73e4[];

u32 probe(u32 a0)
{
    return M2C_FIELD(data_021d73e4, u32, 0x34) + M2C_FIELD(a0, u16, 0x2);
}
''',
    'rematerialise': TYPES + '''
extern u32 fn_021d7f68(u32 a0, u32 a1, u32 a2);

u32 probe(u32 a0)
{
    u16 *const record = (u16 *)(a0 + 6);

    fn_021d7f68(a0, record[3], record[1]);
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


def call_chain_body(row, module='ov001'):
    """Re-express the measured call sequence as C: named calls, measured immediates."""
    address = int(row['address'], 16)
    size = int(row['bytes'])
    code = (ROOT / ('extract/arm9_overlays/%s.bin' % module)).read_bytes()
    body = transcribe_chunk.parse(
        disasm.disassemble(ROOT, module, address, size, 'arm'))
    slots = transcribe_chunk.arm_literal_slots(
        code[int(row['binaryOffset']):int(row['binaryOffset']) + size], address)
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    body = [item for item in body if item[0] < code_end]
    lines = []
    names = []
    for index, (at, mnemonic, operands) in enumerate(body):
        if not mnemonic.startswith(('bl', 'blx')):
            continue
        target = transcribe_chunk.branch_target(mnemonic, operands)
        if target is None:
            continue
        args = {}
        for back in range(max(0, index - 6), index):
            prior_at, prior_mnemonic, prior_operands = body[back]
            if prior_mnemonic != 'mov':
                continue
            parts = [part.strip() for part in prior_operands.split(',')]
            if len(parts) == 2 and parts[0].startswith('r') and parts[1].startswith('#'):
                args[parts[0]] = int(parts[1][1:], 0)
        ordered = [args['r%d' % register] for register in range(4)
                   if 'r%d' % register in args]
        name = 'native_fn_%08x' % target
        names.append(name)
        lines.append('    %s(%s);' % (name, ', '.join('0x%x' % value for value in ordered)))
    if not lines:
        return None
    externs = '\n'.join('extern int %s();' % name for name in dict.fromkeys(names))
    return (TYPES + '\n' + externs + '\n\nu32 probe(u32 a0)\n{\n' +
            '\n'.join(lines) + '\n    return 0;\n}\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--resume', action='store_true',
                        help='keep rows already in the pinned result and probe only new ones')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args(argv)
    disasm_capstone.install()
    config = source_units.load_config(ROOT)
    plan = json.loads(PLAN.read_text())
    probes = ROOT / 'work/ov001-close/cprobes'
    probes.mkdir(parents=True, exist_ok=True)
    ledger = probe_c.ledger_rows(ROOT)
    # probe_c re-reads the 32 MB ledger on every probe; the cached map is the same
    # data and keeps 4,700 compilations linear instead of quadratic.
    probe_c.ledger_rows = lambda root: ledger
    original_modes = probe_c.form_search.TargetModes
    modes_cache = {}

    def cached_modes(root, module=None):
        key = (str(root), module)
        if key not in modes_cache:
            modes = original_modes(root, module)
            modes._load()
            modes_cache[key] = modes
        return modes_cache[key]

    probe_c.form_search.TargetModes = cached_modes
    keys = plan['asmTranscribed'] + plan.get('asmDataCarrier', [])
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
        row = ledger[('ov001', address)]
        profile = 'p033' if row.get('mode') == 'thumb' else 'p003'
        candidates = dict(BODIES)
        chain = call_chain_body(row)
        if chain is not None:
            candidates['call-chain'] = chain
        entry = {}
        for name, body in candidates.items():
            path = probes / ('probe_ov001_%s_%s.c' % (key, name))
            path.write_text(body, encoding='ascii')
            try:
                result = probe_c.probe(config, 'ov001', address, path,
                                       list(config['profiles'][profile]))
            except SystemExit:
                # A body the row's rule will not compile is still a probed body;
                # record it as such instead of aborting the screen.
                entry[name] = {'compileFailed': True, 'length': 0,
                               'bytes': int(row['bytes']), 'relocations': 0,
                               'diffBytes': int(row['bytes']), 'firstDiff': []}
                total += 1
                continue
            total += 1
            off = len(result['diff']) + abs(result['length'] - result['bytes'])
            exact += 1 if not off else 0
            entry[name] = {'length': result['length'], 'bytes': result['bytes'],
                           'relocations': result['relocations'],
                           'diffBytes': off, 'firstDiff': result['diff'][:6]}
        rows[key] = entry
        if len(rows) % 50 == 0:
            print('... %d rows, %d compilations' % (len(rows), total), flush=True)
            if args.record:
                RESULT.write_text(json.dumps({'summary': {'partial': True},
                                              'rows': rows}, indent=1) + '\n')
    closest = min(min(body['diffBytes'] for body in entry.values())
                  for entry in rows.values()) if rows else 0
    closest_key = min(rows, key=lambda k: min(b['diffBytes'] for b in rows[k].values()))
    closest_body = min(rows[closest_key], key=lambda k: rows[closest_key][k]['diffBytes'])
    summary = {'rows': len(rows), 'bodies': len(BODIES) + 1,
               'compilations': sum(len(entry) for entry in rows.values()),
               'exact': exact, 'closestDiffBytes': closest,
               'closestRow': closest_key, 'closestBody': closest_body}
    print(json.dumps(summary))
    if args.record:
        RESULT.write_text(json.dumps({'summary': summary, 'rows': rows}, indent=1) + '\n')
        print('written', RESULT.relative_to(ROOT))
    return 0 if not exact else 1


if __name__ == '__main__':
    sys.exit(main())
