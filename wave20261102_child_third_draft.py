import json
from concurrent.futures import ThreadPoolExecutor
import wave20261102_child_next_research as research
import wave20261102_child_next_expand as expand
from wave20261102_child_third_prepare import ROOT, LANE, WORK
from project import write_json


def main():
    research.LANE, research.WORK = LANE, WORK
    specs = research.setup()
    research.draft.OPTIONS.batch = 'parallel-wave20261102-child-third-large'
    expand.LANE, expand.WORK, expand.STAGE = LANE, WORK, 'expanded'
    selected = sorted([s for s in specs if s['bytes'] >= 96], key=lambda s: -s['bytes'])
    def run(spec):
        result = research.research(spec)
        if 'match' not in result:
            result = expand.research(spec)
        return result
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, selected))
    write_json(LANE / 'large-draft-summary.json', dict(functions=len(results),
        exactFunctions=sum('match' in r for r in results), exactBytes=sum(r['bytes'] for r in results if 'match' in r),
        acceptedSourceCredit=0, method='secondary large-unit draft hypotheses after accepted-source fingerprint catalog'))


if __name__ == '__main__':
    main()
