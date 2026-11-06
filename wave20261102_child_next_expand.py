import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor
import utility_code as matcher
from capstone.arm import ARM_OP_MEM, ARM_REG_PC, ARM_REG_SP
from utility_shapes import reverse_register_locals
from wave20261102_child_next_prepare import ROOT, LANE, WORK
from project import write_json

STAGE = 'expanded2'


def widths(spec):
    result = set()
    for instruction in spec['instructions']:
        if not instruction.mnemonic.startswith(('ldr', 'str')):
            continue
        operands = [o for o in instruction.operands if o.type == ARM_OP_MEM]
        if not operands or operands[0].mem.base in (ARM_REG_PC, ARM_REG_SP):
            continue
        m = instruction.mnemonic
        result.add('s8' if m.startswith('ldrsb') else 's16' if m.startswith('ldrsh') else
                   'u8' if m.startswith(('ldrb', 'strb')) else 'u16' if m.startswith(('ldrh', 'strh')) else 'u32')
    return result


def corrected(text, spec):
    text = re.sub(r'\*\((?=\()', '*(u32 *)(', text)
    text = re.sub(r'\*\*\s*(native_utility_child_arm9_data_[0-9a-f]+)', r'*(u32 *)(*\1)', text)
    lines = []
    for line in text.splitlines():
        if not line.startswith('#') and not line.startswith('extern '):
            line = re.sub(r'(?<![\w*])(native_utility_child_arm9_data_[0-9a-f]+)(?![\w\[])', r'(u32)\1', line)
        lines.append(line)
    text = '\n'.join(lines) + '\n'
    sizes = widths(spec)
    if len(sizes) == 1:
        scalar = next(iter(sizes))
        if scalar != 'u32':
            text = text.replace('*(u32 *)', '*(' + scalar + ' *)')
            signature = re.search(r'\b' + re.escape(spec['name']) + r'\([^\n]*\)', text)
            if signature:
                revised = signature[0].replace('u32 *', scalar + ' *')
                text = text[:signature.start()] + revised + text[signature.end():]
    return text


def research(spec):
    path = LANE / STAGE / ('%08x.json' % spec['address'])
    if path.exists():
        return json.loads(path.read_text())
    old_path = LANE / 'research' / ('%08x.json' % spec['address'])
    old = json.loads(old_path.read_text())
    result = dict(address=hex(spec['address']), module=spec['module'], bytes=spec['bytes'], attempts=[])
    if 'match' in old:
        return result
    directory = WORK / 'expanded' / ('%08x' % spec['address'])
    directory.mkdir(parents=True, exist_ok=True)
    drafts = WORK / 'drafts' / spec['module'] / ('%08x' % spec['address'])
    sources = sorted(drafts.glob('u32-*.c')) + sorted(drafts.glob('void-*.c'))
    sources = [p for p in sources if '-context' not in p.name]
    outputs = set()
    profiles = [('1.2/sp4', '4,p', False, 'on,noauto'), ('1.2/base', 2, False, 'off'),
                ('2.0/base', 2, False, 'off'), ('1.2/sp3', '4,p', False, 'on,noauto')]
    for source in sources:
        text = corrected(source.read_text(), spec)
        variants = [text]
        extra_read = re.sub(r'^(\s*)\*(native_utility_child_arm9_data_040[0-9a-f]+) = ((?:temp|var)_[^;]+);',
                            r'\1(void)*\2;\n\1*\2 = \3;', text, flags=re.M)
        variants.append(extra_read)
        for variant in variants:
            digest = matcher.utility_runtime.sha(variant.encode())
            if digest in outputs:
                continue
            outputs.add(digest)
            candidate = directory / (digest[:16] + '.c')
            candidate.write_text(variant)
            for profile, level, speed, inline in profiles:
                try:
                    row, code = matcher.compile_compare(candidate, dict(spec,
                        compilerPath=ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')), level, inline, speed)
                except Exception as error:
                    row, code = dict(failure=str(error)), None
                result['attempts'].append(row)
                if code is not None:
                    result.update(match=row, draftSource=candidate.relative_to(ROOT).as_posix())
                    write_json(path, result)
                    print(dict(address=hex(spec['address']), bytes=spec['bytes'], exact=True), flush=True)
                    return result
    write_json(path, result)
    print(dict(address=hex(spec['address']), bytes=spec['bytes'], exact=False,
        bestMatching=max((r.get('matchingBytes', 0) for r in result['attempts']), default=0)), flush=True)
    return result


def main():
    global STAGE
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', default='expanded2', choices=['expanded2'])
    args = parser.parse_args()
    STAGE = args.stage
    wanted = {int(r['address'], 0) for r in json.loads((LANE / 'claim.json').read_text())['functions']}
    specs = [s for s in matcher.candidates() if s['module'] == 'utility-child-arm9-main' and s['address'] in wanted]
    matcher.WORK = WORK / 'expanded-compiled'
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(research, specs))
    write_json(LANE / 'expanded-summary.json', dict(exactFunctions=sum('match' in r for r in results),
        exactBytes=sum(r['bytes'] for r in results if 'match' in r)))


if __name__ == '__main__':
    main()
