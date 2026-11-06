import hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime
from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import measured_module


def execute():
    snapshot = ROOT / 'evidence/verification/accepted-cohort140-identities-v2-20261101.json'
    accepted = read_json(snapshot)['functions']
    specs = [('ov000', 'nonmatching/overlay-lane/20261102-geometry873/021da5e4/explicit-fx-divisor/results.json')]
    specs += [('ov000', f'nonmatching/overlay-lane/20261102-geometry871/{address}/qualified-ghidra-flags/results.json') for address in ['021dc374', '021db15c', '021dd54c', '021dea78']]
    specs += [('ov005', 'nonmatching/overlay-lane/20261102-controller861/021d8900/contiguous-two-word-callback-payload/results.json')]
    rows = []
    for module, path in specs:
        result = read_json(ROOT / path)['rows'][0]
        source, link = result['source'], result['genuineLink']
        rows.append(measure(module, source, link, path, False, accepted))
    behaviorPath = 'evidence/application/ov000-geometry874-behavior-20261102.json'
    behavior = read_json(ROOT / behaviorPath)
    rows.append(measure('ov000', behavior['candidate']['source'], behavior['candidate']['canonicalComparison'], behaviorPath, True, accepted))
    keys = [(row['module'], row['address']) for row in rows]
    if len(keys) != len(set(keys)) or len(rows) != 7 or sum(row['nativeBytes'] for row in rows) != 13256:
        raise ValueError('875 unique materialized backlog differs')
    report = dict(schemaVersion=1, sourceCredit=0, romSha256=configuration()['romSha256'], acceptedExclusion=dict(path=snapshot.relative_to(ROOT).as_posix(), sha256=sha256(snapshot), cohort=140), uniqueDraftedFunctions=len(rows), uniqueDraftedNativeBytes=sum(row['nativeBytes'] for row in rows), uniqueCompilableGenuinelyLinkedFunctions=len(rows), uniqueCompilableNativeBytes=sum(row['nativeBytes'] for row in rows), exactFunctions=0, exactBytes=0, scopedBehaviorQualifiedFunctions=1, scopedBehaviorQualifiedNativeBytes=1884, rows=sorted(rows, key=lambda row: (row['module'], row['address'])), limits=['Native extents are identified draft ranges, not newly accepted code/data boundaries. This census is derived from frozen compiler/link reports and remeasured source/input hashes; use the compiler producers for fresh builds.', 'Six new geometry C materializations cover11756 native bytes, plus one1500-byte callback controller. Historical860 M2C failures, incomplete866 types and870 origin-uniqueness rejection remain retained.', 'Only the separate874 source variant has scoped native/independent-model/private-C qualification. Others retain unqualified helpers, transitive inputs, types, arithmetic and callback domains. Compilable does not imply behavior or matching.', 'Per-PC INT_CARRY and signed borrow primitives qualify explicit operations, not generic M2C flag macros, arbitrary parent expressions or complete game routines.', 'No additive coverage versus earlier breadth censuses, accepted functions or parallel variants; zero function/module/ROM credit.'])
    write_json(ROOT / 'evidence/attempts/overlay-geometry875-breadth-20261102.json', report)
    print({key: report[key] for key in ['uniqueDraftedFunctions', 'uniqueDraftedNativeBytes', 'uniqueCompilableGenuinelyLinkedFunctions', 'scopedBehaviorQualifiedNativeBytes', 'exactFunctions', 'sourceCredit']})


def measure(module, source, link, reportPath, behavioral, accepted):
    address = int(source['address'], 0)
    size = source['bytes']
    for row in accepted:
        if row['processor'] == 'arm9' and row['program'] == '' and row['module'] == module:
            other = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
            if address < other + row['bytes'] and other < address + size:
                raise ValueError(('875 accepted overlap', module, source['address'], row['name']))
    sourcePath = ROOT / source['source']
    if sha256(sourcePath) != source['sourceSha256']:
        raise ValueError(('875 source changed', sourcePath))
    info, data, unused = measured_module(module)
    base = int(info['base'], 0) if isinstance(info['base'], str) else info['base']
    span = data[address - base:address - base + size]
    if len(span) != size or link['nativeBytes'] != size or link.get('exactCallerBytes'):
        raise ValueError('875 unexpected span/exactness')
    return dict(romSha256=configuration()['romSha256'], processor='arm9', program='', module=module, moduleSha256=info['sha256'], address=address, mode='arm', nativeBytes=size, nativeSpanSha256=hashlib.sha256(span).hexdigest(), source=source['source'], sourceSha256=sha256(sourcePath), context=dict(path=sourcePath.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(sourcePath.with_name('context.h'))), recordedReport=dict(path=reportPath, sha256=sha256(ROOT / reportPath)), compileStatus='compiled-and-genuinely-linked', linkedBytes=link['linkedBytes'], samePositionBytes=link['matchingBytes'], exact=False, behaviorQualifiedOnlyForPublishedScope=behavioral, sourceCredit=0, unresolved=['Original C types/formals and complete ordinary caller domain remain hypotheses.', 'Canonical module/source comparison fails; no matching credit.'] + ([] if behavioral else ['Actual whole-body native/candidate behavior not qualified; generated arguments may remain incomplete.']))


if __name__ == '__main__':
    execute()
