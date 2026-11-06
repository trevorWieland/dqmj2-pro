import concurrent.futures
import re
from types import SimpleNamespace
from project import ROOT, configuration, now, sha256, write_json
import draft_runtime as drafting

WORK = ROOT / 'work/main-breadth-lane-20261030'
REPORT = ROOT / 'evidence/attempts/main-breadth-lane-20261030.json'


def options():
    enabled = {'word_args', 'abi_slots', 'register_order', 'direct_increments',
               'typed_globals', 'stack_buffers', 'pointer_returns', 'source_returns'}
    names = enabled | {'void', 'descending_regs', 'gotos_only', 'compiler_variants', 'thumb'}
    return SimpleNamespace(module='main', **{name: name in enabled for name in names})


def worker(spec):
    name, address, size, assembly, context, returns = spec
    import draft_runtime as unit
    import match_runtime as compiler
    unit.OPTIONS = options()
    unit.WORK = WORK / format(address, '08x')
    compiler.WORK = unit.WORK / 'compile'
    unit.FUNCTION_INPUTS = {name: (assembly, context)}
    unit.FUNCTION_ADDRESSES = {name: format(address, '08x')}
    unit.SOURCE_RETURNS = returns
    result = unit.one(name)
    attempts = result.get('attempts', [])
    compiled = [row for row in attempts if row.get('compiledBytes')]
    best = max(compiled, key=lambda row: row.get('matchingBytes', 0), default={})
    result.update(module='main', processor='arm9', mode='arm', address=hex(address), bytes=size,
                  sourceCredit=0, accepted=False, generatedHypothesis=True,
                  compilable=bool(compiled), compilerExact=any(row.get('exactAfterDeclaredRelocation') for row in compiled),
                  bestSameOffsetBytes=best.get('matchingBytes', 0),
                  reviewRequired=['argument ABI and object extents', 'source language semantics',
                                  'genuine linking', 'independent native contracts', 'module and ROM regression'])
    return result


def main():
    from ledger_state import collect_matches
    drafting.OPTIONS = options()
    drafting.WORK = WORK / 'input-index'
    drafting.inputs()
    accepted, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    queue = []
    for name, length, location in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', symbols, re.M):
        address, size = int(location, 0), int(length, 0)
        if not 0x02000800 <= address < 0x02040000 or not 256 <= size <= 2400:
            continue
        if ('main', 'arm', address) in accepted or name not in drafting.FUNCTION_INPUTS or address == 0x0201F2C0:
            continue
        assembly, context = drafting.FUNCTION_INPUTS[name]
        if not re.search(r'\bblx?\s', assembly, re.I):
            continue
        queue.append((name, address, size, assembly, context, drafting.SOURCE_RETURNS))
    queue.sort(key=lambda row: (-row[2], row[1]))
    queue = queue[:40]
    report = {'createdUtc': now(), 'lane': 'integrator-main-breadth', 'sourceCredit': 0,
              'queueFunctions': len(queue), 'queueNativeBytes': sum(row[2] for row in queue),
              'compilerProcesses': 3, 'results': [], 'acceptedSourceChanged': False,
              'generatorSha256': sha256(ROOT / 'draft_main_breadth_lane_20261030.py')}
    write_json(REPORT, report)
    print({'queueFunctions': len(queue), 'queueNativeBytes': report['queueNativeBytes'], 'compilerProcesses': 3}, flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        tasks = {pool.submit(worker, spec): spec for spec in queue}
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            report['results'].append(result)
            rows = report['results']
            report.update(draftedFunctions=sum('draftSource' in row for row in rows),
                          compilableFunctions=sum(row['compilable'] for row in rows),
                          compilerExactFunctions=sum(row['compilerExact'] for row in rows),
                          draftedNativeBytes=sum(row['bytes'] for row in rows if 'draftSource' in row),
                          compilableNativeBytes=sum(row['bytes'] for row in rows if row['compilable']),
                          compilerExactNativeBytes=sum(row['bytes'] for row in rows if row['compilerExact']))
            write_json(REPORT, report)
            print({key: report[key] for key in ['draftedFunctions', 'compilableFunctions', 'compilerExactFunctions']}, flush=True)
    report['finishedUtc'] = now()
    write_json(REPORT, report)


if __name__ == '__main__':
    main()
