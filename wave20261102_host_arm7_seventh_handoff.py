from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from wave20261102_host_arm7_seventh_prepare import LANE, WORK


def main():
    remaining = read_json(LANE / 'remaining-queue.json')
    research = [read_json(p) for p in sorted((WORK / 'sdk-probes-arm7-v5').rglob('result.json'))]
    exact = {r['address'] for r in read_json(LANE / 'packet-ready.json')['matches']}
    blockers = {}
    for unit in research:
        for row in unit.get('closedAttempts', []):
            if not row.get('exact') and row['address'] not in exact:
                blockers.setdefault(row['address'], []).append(dict(referenceFunction=row['referenceFunction'],
                    compiler=unit['compiler'], profile=unit['profileLabel'], refusal=row.get('refusal', ''),
                    sourceCredit=0, functionCredit=0))
    rows = [dict(row, observedSourceBlockers=blockers.get(row['address'], []),
        status='uncredited-source-backlog', behaviorExecutionCredit=0) for row in remaining['functions']]
    failed_units = [dict(source=u['referenceSource'], sourceSha256=u['referenceSourceSha256'],
        compiler=u['compiler'], profile=u['profileLabel'], exitCode=u['exitCode'],
        firstCompilerDiagnostic=(u['stdout'] + u['stderr'])[:800]) for u in research if u['exitCode']]
    task = dict(title='Resolve the remaining host ARM7 WRAM source/type/profile boundaries',
        executionStarted=False, program='', processor='arm7', module='arm7-wram',
        objective='Recover an independently closed ordinary-C subset from the remaining16 configured host-WRAM functions, preserving all accepted and frozen source.',
        instructions=['Create a new ownership/input packet and uniquely named helper/source/work roots before experiments; do not edit seventh or older pinned files.',
            'Start with the largest residual configured extents and compare their normalized instructions/relocations against the pinned reference profiles.',
            'Resolve the missing SysSubp.h reference dependency from sourced declarations and actual needed type closure; do not insert guessed declarations or empty compatibility headers.',
            'For compiler-generated division imports, require the measured original branch and an existing same-program, same-CPU/mode entry; keep unsupported imports uncredited.',
            'Test documented SDK conditional/profile hypotheses in isolated contexts; do not alter source meaning or replace unmatched code with assembly/data blobs.',
            'Every adopted function must pass full configured extent, relocation encoding/addends and genuine arm7tdmi links, plus copied-root canonical replay and unchanged accepted checks.'],
        sourceCreditUntilSharedAcceptance=0, expectedBehaviorExecutionCredit=0)
    result = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        remainingFunctions=len(rows), remainingBytes=sum(r['bytes'] for r in rows), functions=rows,
        failedReferenceUnits=failed_units, newRegionExpansionPerformed=False, nextTask=task,
        limitation='A missing direct source fingerprint is a failed search result, not proof of absent behavior or a recovered function.')
    write_json(LANE / 'residual-handoff.json', result)
    print(dict(remainingFunctions=len(rows), remainingBytes=result['remainingBytes'], nextTaskDispatched=False))


if __name__ == '__main__':
    main()
