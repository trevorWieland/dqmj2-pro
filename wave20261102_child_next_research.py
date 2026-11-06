import argparse
import json
import os
import re
import subprocess
import sys
import types
from concurrent.futures import ThreadPoolExecutor
import draft_utility as draft
import utility_code as matcher
from utility_abi import argument_hints
from utility_shapes import reverse_register_locals
from wave20261102_child_next_prepare import ROOT, LANE, WORK
from project import write_json


def setup():
    draft.WORK = WORK / 'drafts'
    matcher.WORK = WORK / 'compiled'
    draft.OPTIONS = types.SimpleNamespace(batch='parallel-wave20261102-child-next', scalar_globals=True,
        fixed_work_areas=True, register_order=True, reverse_register_order=False,
        direct_increments=True, typed_globals=True)
    specs = matcher.candidates()
    draft.FUNCTIONS = {cpu: {s['address']: s for s in specs if s['processor'] == cpu} for cpu in ('arm9', 'arm7')}
    draft.ARGUMENTS = {cpu: argument_hints(list(rows.values()), {})[0] for cpu, rows in draft.FUNCTIONS.items()}
    wanted = {(r['module'], int(r['address'], 0)) for r in json.loads((LANE / 'claim.json').read_text())['functions']}
    return [s for s in specs if (s['module'], s['address']) in wanted]


def repair(text, scalar):
    text = text.replace('NULL', '0')
    if scalar:
        text = text.replace('void **', 'u32 *').replace('void *', 'u32 ')
    names = set(re.findall(r'\b(?:u32|s32)\s+([A-Za-z_]\w*)', text))
    result = []
    for line in text.splitlines():
        if not line.startswith('#'):
            line = re.sub(r'(?<!\w)\*\((?=[A-Za-z_])', '*(u32 *)(', line)
            if scalar and not re.match(r'\s*(?:u\d+|s\d+|void|struct)\b', line):
                line = re.sub(r'\*([A-Za-z_]\w*)', lambda m: '*(u32 *)' + m[1] if m[1] in names else m[0], line)
        result.append(line)
    return '\n'.join(result) + '\n'


def research(spec):
    path = LANE / 'research' / ('%08x.json' % spec['address'])
    if path.exists():
        return json.loads(path.read_text())
    directory = WORK / 'drafts' / spec['module'] / ('%08x' % spec['address'])
    directory.mkdir(parents=True, exist_ok=True)
    result = dict(module=spec['module'], address=hex(spec['address']), bytes=spec['bytes'], variants=[], attempts=[])
    asm, targets, data, declarations = draft.assembly(spec)
    assembly = directory / 'native.s'
    assembly.write_text(asm)
    profiles = [('1.2/sp4', '4,p', False, 'on,noauto'), ('1.2/base', 2, False, 'off'),
                ('1.2/base', 2, True, 'off'), ('2.0/base', 2, False, 'off'),
                ('1.2/sp4', 2, True, 'off'), ('1.2/sp4', '4,p', False, 'off')]
    for returns in ['u32', 'void']:
        context = directory / (returns + '-context.c')
        context.write_text(draft.PRELUDE + '\n'.join(declarations) + '\nextern %s %s();\n' % (returns, draft.symbol(spec)))
        command = [sys.executable, str(draft.M2C), '--target', 'arm-mwcc-c', '--context', str(context),
            '--globals', 'none', '--no-cache', '--valid-syntax', '--comment-style', 'none', '-f', draft.symbol(spec), str(assembly)]
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / 'tools/m2c-python')),
            capture_output=True, text=True, timeout=45)
        variant = dict(returnAssumption=returns, command=command, exitCode=process.returncode,
                       stdout=process.stdout, stderr=process.stderr)
        result['variants'].append(variant)
        if process.returncode:
            continue
        try:
            original = draft.recovered_source(process.stdout, spec, targets, data)
        except Exception as error:
            variant['failure'] = str(error)
            continue
        seen = set()
        for scalar in [False, True]:
            repaired = repair(original, scalar)
            for text in [repaired, reverse_register_locals(repaired, spec['name'])]:
                digest = matcher.utility_runtime.sha(text.encode())
                if digest in seen:
                    continue
                seen.add(digest)
                source = directory / (returns + '-' + digest[:16] + '.c')
                source.write_text(text)
                for profile, level, speed, inline in profiles:
                    try:
                        row, code = matcher.compile_compare(source, dict(spec,
                            compilerPath=ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')), level, inline, speed)
                    except Exception as error:
                        row, code = dict(failure=str(error), compilerProfile=profile), None
                    result['attempts'].append(row)
                    if code is not None:
                        result.update(match=row, draftSource=source.relative_to(ROOT).as_posix())
                        write_json(path, result)
                        print(dict(address=hex(spec['address']), bytes=spec['bytes'], exact=True, profile=profile), flush=True)
                        return result
    write_json(path, result)
    best = max((r.get('matchingBytes', 0) for r in result['attempts']), default=0)
    print(dict(address=hex(spec['address']), bytes=spec['bytes'], exact=False, bestMatching=best), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    specs = setup()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(research, specs))
    write_json(LANE / 'research-summary.json', dict(functions=len(results),
        exactFunctions=sum('match' in r for r in results),
        exactBytes=sum(r['bytes'] for r in results if 'match' in r)))


if __name__ == '__main__':
    main()
