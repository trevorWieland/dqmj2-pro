import argparse
import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import utility_code as matcher
from utility_shapes import reverse_register_locals
from wave20261102_child_research import setup
from wave20261102_child_prepare import ROOT, WORK, LANE
from project import write_json

SCALAR = False


def repaired(text):
    text = text.replace('NULL', '0')
    if SCALAR:
        text = text.replace('void **', 'u32 *').replace('void *', 'u32 ')
        names = set(re.findall(r'\b(?:u32|s32)\s+([A-Za-z_]\w*)', text))
    lines = []
    for line in text.splitlines():
        if not line.startswith('#'):
            line = re.sub(r'(?<!\w)\*\((?=[A-Za-z_])', '*(u32 *)(', line)
            if SCALAR and not re.match(r'\s*(?:u\d+|s\d+|void|struct)\b', line):
                line = re.sub(r'\*([A-Za-z_]\w*)', lambda m: '*(u32 *)' + m[1] if m[1] in names else m[0], line)
        lines.append(line)
    return '\n'.join(lines) + '\n'


def sweep(spec):
    stage = 'sweeps-scalar' if SCALAR else 'sweeps'
    path = LANE / stage / ('%08x.json' % spec['address'])
    if path.exists():
        old = json.loads(path.read_text())
        if old.get('match'):
            return old
    result = dict(address=hex(spec['address']), module=spec['module'], bytes=spec['bytes'], attempts=[])
    directory = WORK / 'sweep-sources' / ('%08x' % spec['address'])
    directory.mkdir(parents=True, exist_ok=True)
    drafts = WORK / 'drafts' / spec['module'] / ('%08x' % spec['address'])
    sources = []
    for source in sorted(drafts.glob('*-draft-*.c')):
        text = repaired(source.read_text())
        for variant in (text, reverse_register_locals(text, spec['name'])):
            dest = directory / (matcher.utility_runtime.sha(variant.encode())[:16] + '.c')
            if dest not in sources:
                dest.write_text(variant)
                sources.append(dest)
    profiles = ['1.2/sp4', '1.2/sp3', '1.2/sp2p3', '1.2/sp2', '2.0/sp1p5', '1.2/base', '2.0/base']
    for source in sources:
        for profile in profiles:
            for level, speed, inline in [('4,p', False, 'on,noauto'), (2, True, 'off'), (4, True, 'off')]:
                try:
                    row, code = matcher.compile_compare(source, dict(spec,
                        compilerPath=ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')), level, inline, speed)
                    result['attempts'].append(row)
                    if code is not None:
                        result.update(match=row, draftSource=source.relative_to(ROOT).as_posix())
                        write_json(path, result)
                        print(dict(address=result['address'], bytes=spec['bytes'], exact=True, compiler=profile), flush=True)
                        return result
                except Exception as error:
                    result['attempts'].append(dict(profile=profile, failure=str(error)))
    write_json(path, result)
    valid = [r for r in result['attempts'] if 'matchingBytes' in r]
    best = max(valid, key=lambda r: r['matchingBytes'], default={})
    print(dict(address=result['address'], bytes=spec['bytes'], exact=False,
               bestMatching=best.get('matchingBytes'), compiledBytes=best.get('compiledBytes')), flush=True)
    return result


def main():
    global SCALAR
    p = argparse.ArgumentParser()
    p.add_argument('--start', type=lambda s: int(s, 0), default=0)
    p.add_argument('--end', type=lambda s: int(s, 0), default=0xffffffff)
    p.add_argument('--scalar', action='store_true')
    args = p.parse_args()
    SCALAR = args.scalar
    specs = [s for s in setup() if args.start <= s['address'] < args.end]
    matcher.WORK = WORK / 'sweep-compiled'
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(sweep, specs))
    write_json(LANE / ('sweep-summary-%08x.json' % args.start), dict(functions=len(results),
        matches=sum('match' in r for r in results), matchedBytes=sum(r['bytes'] for r in results if 'match' in r)))


if __name__ == '__main__':
    main()
