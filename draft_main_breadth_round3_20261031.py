import concurrent.futures
import re
from project import ROOT, configuration, read_json, write_json, now, sha256
import draft_main_breadth_lane_20261030 as base
import draft_runtime as drafting
from qualified_call_contexts_20261031 import apply, catalogue

WORK = ROOT / 'work/main-breadth-round3-20261031'
REPORT = ROOT / 'evidence/attempts/main-breadth-round3-20261031.json'


def worker(spec):
    import draft_main_breadth_lane_20261030 as unit
    unit.WORK = WORK
    name, address, size, assembly, context, returns = spec
    context, contracts = apply(context, "main", catalogue())
    result = unit.worker((name, address, size, assembly, context, returns))
    result["qualifiedContextContracts"] = contracts
    return result


def main():
    from ledger_state import collect_matches
    drafting.OPTIONS = base.options()
    drafting.WORK = WORK / 'input-index'
    drafting.inputs()
    selected, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    earlier = read_json(ROOT / 'evidence/attempts/main-breadth-lane-20261030.json')
    used = {int(row['address'], 0) for row in earlier['results']}
    previous = read_json(ROOT / 'evidence/attempts/main-breadth-round2-20261030.json')
    used |= {int(row['address'], 0) for row in previous['results']}
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    queue = []
    for name, length, location in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', symbols, re.M):
        address, size = int(location, 0), int(length, 0)
        if not 0x02000800 <= address < 0x02040000 or not 128 <= size <= 2400:
            continue
        if address in used or address == 0x0201F2C0 or ('main', 'arm', address) in selected or name not in drafting.FUNCTION_INPUTS:
            continue
        assembly, context = drafting.FUNCTION_INPUTS[name]
        queue.append((name, address, size, assembly, context, drafting.SOURCE_RETURNS))
    queue.sort(key=lambda row: (-row[2], row[1]))
    queue = queue[:40]
    report = {'createdUtc': now(), 'lane': 'integrator-main-round3', 'sourceCredit': 0,
              'queueFunctions': len(queue), 'queueNativeBytes': sum(row[2] for row in queue),
              'compilerProcesses': 2, 'results': [], 'acceptedSourceChanged': False,
              'generatorSha256': sha256(ROOT / 'draft_main_breadth_round3_20261031.py')}
    write_json(REPORT, report)
    print({'queueFunctions': len(queue), 'queueNativeBytes': report['queueNativeBytes']}, flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        tasks = [pool.submit(worker, spec) for spec in queue]
        for future in concurrent.futures.as_completed(tasks):
            report['results'].append(future.result())
            rows = report['results']
            for label, predicate in [('drafted', lambda row: 'draftSource' in row),
                                     ('compilable', lambda row: row['compilable']),
                                     ('compilerExact', lambda row: row['compilerExact'])]:
                report[label + 'Functions'] = sum(predicate(row) for row in rows)
                report[label + 'NativeBytes'] = sum(row['bytes'] for row in rows if predicate(row))
            write_json(REPORT, report)
            print({key: report[key] for key in ['draftedFunctions', 'compilableFunctions', 'compilerExactFunctions']}, flush=True)
    report['finishedUtc'] = now()
    write_json(REPORT, report)


if __name__ == '__main__':
    main()
