import concurrent.futures
import re
import draft_runtime as drafting
import draft_main_large_breadth13_20261031 as previous
from draft_main_breadth_lane_20261030 import options
from ledger_state import collect_matches
from project import ROOT, configuration, read_json, write_json, sha256, now
from seal_recovery_evidence_20261031 import code_closure

WORK = ROOT / 'work/main-breadth14-20261101'
REPORT = ROOT / 'evidence/attempts/main-breadth14-20261101.json'


def worker(spec):
    previous.WORK = WORK
    return previous.worker(spec)


def main():
    selected, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and not REPORT.exists()
    histories = sorted((ROOT / 'evidence/attempts').glob('main-*breadth*.json'))
    used = set()
    for path in histories:
        document = read_json(path)
        for row in document.get('results', []):
            address = row.get('address')
            if address is not None:
                used.add((row.get('mode', 'arm'), int(address, 0) if isinstance(address, str) else address))
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    queue = []
    for mode in ['arm', 'thumb']:
        drafting.FUNCTION_INPUTS = {}
        drafting.FUNCTION_ADDRESSES = {}
        drafting.SOURCE_RETURNS = {}
        drafting.OPTIONS = options()
        drafting.OPTIONS.thumb = mode == 'thumb'
        drafting.WORK = WORK / ('input-' + mode)
        drafting.inputs()
        candidates = []
        pattern = r'^(\S+) kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)'
        for name, length, location in re.findall(pattern, symbols, re.M):
            address, size = int(location, 0), int(length, 0)
            owned = 0x02000800 <= address < 0x02040000 or address >= 0x020D0000
            if not owned or address == 0x0202A8E0 or not 64 <= size <= 4096:
                continue
            if (mode, address) in used or ('main', mode, address) in selected:
                continue
            if name not in drafting.FUNCTION_INPUTS:
                continue
            assembly, context = drafting.FUNCTION_INPUTS[name]
            candidates.append((name, address, size, mode, assembly, context, dict(drafting.SOURCE_RETURNS)))
        candidates.sort(key=lambda row: (-row[2], row[1]))
        queue.extend(candidates[:128])
    queue.sort(key=lambda row: (-row[2], row[1]))
    report = dict(createdUtc=now(), generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in code_closure([__file__.split('\\')[-1]])],
        previousAttemptReports=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in histories],
        queueFunctions=len(queue), queueNativeBytes=sum(row[2] for row in queue), compilerProcesses=3,
        queue=[dict(name=row[0], address=hex(row[1]), bytes=row[2], mode=row[3]) for row in queue],
        results=[], acceptedSourceChanged=False, sourceCredit=0, state='running',
        limitations=['Generated contexts and C are hypotheses', 'Compilation is not genuine linking or semantic validation',
                    'No new accepted function, byte, module or ROM credit'])
    write_json(REPORT, report)
    print(dict(queueFunctions=len(queue), queueNativeBytes=report['queueNativeBytes']), flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(worker, spec): spec for spec in queue}
        for future in concurrent.futures.as_completed(futures):
            spec = futures[future]
            try:
                row = future.result()
            except Exception as error:
                row = dict(name=spec[0], address=hex(spec[1]), bytes=spec[2], mode=spec[3], error=str(error), sourceCredit=0)
            report['results'].append(row)
            report['draftedFunctions'] = sum(bool(row.get('attempts')) for row in report['results'])
            report['compilableFunctions'] = sum(bool(row.get('compilable')) for row in report['results'])
            report['compilableNativeBytes'] = sum(row['bytes'] for row in report['results'] if row.get('compilable'))
            write_json(REPORT, report)
            print(dict(completed=len(report['results']), drafted=report['draftedFunctions'], compilable=report['compilableFunctions']), flush=True)
    report.update(state='finished', finishedUtc=now())
    write_json(REPORT, report)


if __name__ == '__main__':
    main()
