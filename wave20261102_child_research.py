import argparse
import json
import types
from concurrent.futures import ThreadPoolExecutor
import draft_utility as draft
import utility_code as matcher
from draft_arm7 import argument_counts
from utility_abi import argument_hints
from wave20261102_child_prepare import LANE, WORK, ROOT
from project import write_json, sha256


def setup():
    draft.WORK = WORK / 'drafts'
    matcher.WORK = WORK / 'compiled'
    draft.OPTIONS = types.SimpleNamespace(batch='parallel-wave20261102-child', scalar_globals=True,
        fixed_work_areas=True, register_order=True, reverse_register_order=False,
        direct_increments=True, typed_globals=True)
    specs = matcher.candidates()
    draft.FUNCTIONS = {cpu: {s['address']: s for s in specs if s['processor'] == cpu} for cpu in ('arm9', 'arm7')}
    draft.ARGUMENTS = {cpu: argument_hints(list(rows.values()), {})[0] for cpu, rows in draft.FUNCTIONS.items()}
    claim = json.loads((LANE / 'claim.json').read_text())
    wanted = {(r['module'], int(r['address'], 0)) for r in claim['functions']}
    return [s for s in specs if (s['module'], s['address']) in wanted]


def research(spec):
    result = draft.safe_research(spec)
    path = LANE / 'research' / ('%08x.json' % spec['address'])
    write_json(path, result)
    print(dict(address=result['address'], bytes=result['nativeBytes'], match='match' in result), flush=True)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--start', type=lambda s: int(s, 0), default=0)
    p.add_argument('--end', type=lambda s: int(s, 0), default=0xffffffff)
    args = p.parse_args()
    specs = [s for s in setup() if args.start <= s['address'] < args.end]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(research, specs))
    write_json(LANE / ('research-summary-%08x.json' % args.start), dict(functions=len(results),
        matches=sum('match' in r for r in results), matchedBytes=sum(r['nativeBytes'] for r in results if 'match' in r),
        generator=__file__, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
