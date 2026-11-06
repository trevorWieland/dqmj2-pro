import argparse
import json
import re
import types
from concurrent.futures import ThreadPoolExecutor
import draft_utility as draft
import utility_code
import wave20261102_child_next_research as research
import wave20261102_child_next_expand as expand
from wave20261102_child_third_abi import derive, controls
from wave20261102_child_third_prepare import ROOT, LANE, WORK
from project import write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', default='cfg2', choices=['cfg2'])
    args = parser.parse_args()
    controls()
    functions, profiles, analyses = derive()
    research.LANE, research.WORK = LANE / args.stage, WORK / args.stage
    expand.LANE, expand.WORK, expand.STAGE = LANE / args.stage, WORK / args.stage, 'expanded'
    draft.WORK = WORK / args.stage / 'drafts'
    utility_code.WORK = WORK / args.stage / 'compiled'
    draft.OPTIONS = types.SimpleNamespace(batch='parallel-wave20261102-child-third-cfg', scalar_globals=True,
        fixed_work_areas=True, register_order=True, reverse_register_order=False,
        direct_increments=True, typed_globals=True)
    draft.FUNCTIONS = functions
    draft.ARGUMENTS = profiles
    old_assembly, old_source = draft.assembly, draft.recovered_source
    def assembly(spec):
        text, targets, data, declarations = old_assembly(spec)
        for label, (target, mode) in targets.items():
            if target & ~1 not in profiles[spec['processor']]:
                declarations = [re.sub(r'^extern u32 ' + re.escape(label) + r'\([^;]*\);$',
                    'extern u32 ' + label + '();', line) for line in declarations]
        return text, targets, data, declarations
    def recovered(text, spec, targets, data):
        result = old_source(text, spec, targets, data)
        for label, (target, mode) in targets.items():
            if target & ~1 not in profiles[spec['processor']]:
                name = 'native_utility_child_%s_%s_%08x' % (spec['processor'], mode, target)
                result = re.sub(r'^extern u32 ' + re.escape(name) + r'\([^;]*\);$',
                    'extern u32 ' + name + '();', result, flags=re.M)
        return result
    draft.assembly, draft.recovered_source = assembly, recovered
    wanted = {int(e['address'], 0) for e in json.loads((LANE / 'claim.json').read_text())['functions']}
    specs = sorted([s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'
                    and s['address'] in wanted and s['bytes'] >= 96], key=lambda s: -s['bytes'])
    def run(spec):
        result = research.research(spec)
        if 'match' not in result:
            result = expand.research(spec)
        return result
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, specs))
    write_json(LANE / 'cfg-draft-summary.json', dict(functions=len(results),
        exactFunctions=sum('match' in r for r in results), exactBytes=sum(r['bytes'] for r in results if 'match' in r),
        generator=__file__, generatorSha256=sha256(__file__), abiContext='cfg-abi-context.json',
        sourceCredit=0, unresolvedCalleeDeclarations='unspecified C prototypes; no guessed fixed or variadic arity'))


if __name__ == '__main__':
    main()
