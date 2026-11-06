import hashlib
from pathlib import Path
import match_runtime
from project import ROOT, configuration, read_json, sha256, write_json
from link_runtime_unit import measured_module


def matching_ranges(native, candidate, address):
    ranges, begin = [], None
    for offset in range(len(native) + 1):
        equal = offset < min(len(native), len(candidate)) and native[offset] == candidate[offset]
        if equal and begin is None:
            begin = offset
        if not equal and begin is not None:
            ranges.append(dict(start=hex(address + begin), endExclusive=hex(address + offset), bytes=offset - begin))
            begin = None
    return ranges


def main():
    sources = [
        ('evidence/attempts/main-heap-search-behavior-qualified-drafts-20261031.json', 'search'),
        ('evidence/attempts/main-heap-commit-measured-views-behavior-qualified-draft-20261101.json', 'single'),
        ('evidence/attempts/main-heap-region-return-behavior-qualified-draft-20261101.json', 'single'),
        ('evidence/attempts/ov001-action436-functional-near-20261101.json', 'overlay')]
    rows, identities = [], set()
    for relative, kind in sources:
        path = ROOT / relative
        report = read_json(path)
        if kind == 'search':
            units = [(value['compilerResult'], value['genuineLinkMismatch'], value['actualReturns']) for value in report['results']]
        elif kind == 'single':
            units = [(report['compilerResult'], report['linkMismatch'], report['actualReturns'])]
        else:
            units = [(report['compilation'], report['genuineLinkComparison'], report['actualTopReturns'])]
        for unit, comparison, own_returns in units:
            address = int(unit['address'], 0)
            identity = (configuration()['romSha256'], unit['processor'], unit.get('program', '') or '', unit['module'], address, unit['mode'])
            assert identity not in identities
            identities.add(identity)
            source = ROOT / unit['source']
            assert sha256(source) == unit['sourceSha256']
            assert sha256(ROOT / unit['object']) == unit['objectSha256']
            directory = Path(comparison['directory'])
            assert directory.resolve().is_relative_to(ROOT)
            candidate_path = directory / 'caller.bin'
            candidate = candidate_path.read_bytes()
            unused, module, unused = measured_module(unit['module'])
            base = 0x02000000 if unit['module'] == 'main' else 0x021D7240
            native = module[address - base:address - base + unit['bytes']]
            assert hashlib.sha256(native).hexdigest() == unit['targetSha256']
            assert len(candidate) == comparison['linkedBytes'] and candidate != native
            ranges = matching_ranges(native, candidate, address)
            assert sum(r['bytes'] for r in ranges) == comparison['matchingBytes']
            rows.append(dict(buildSha256=identity[0], processor=identity[1], program=identity[2], module=identity[3],
                address=hex(address), mode=unit['mode'], initializedBytes=unit['bytes'], source=unit['source'],
                sourceSha256=unit['sourceSha256'], object=unit['object'], objectSha256=unit['objectSha256'],
                compilerSha256=unit['compilerSha256'], compilerFlags=unit['compilerFlags'], dependencies=unit['relocations'],
                candidateArtifact=candidate_path.relative_to(ROOT).as_posix(), candidateArtifactSha256=sha256(candidate_path),
                nativeSha256=unit['targetSha256'], matchingRanges=ranges, matchingAtOriginalOffsetsBytes=comparison['matchingBytes'],
                linkedCandidateBytes=len(candidate), wholeFunctionBytesMatch=False, ordinaryAssemblyOrBlobCredit=0,
                states=dict(analyzed=True, drafted=True, boundedBehaviorQualified=True, functionMatched=False,
                    moduleLinked=False, wholeRomMatchedFromSource=False), actualTopReturnsInEvidence=own_returns,
                evidenceClass='bounded-original-versus-linked-C-draft', evidence=relative, evidenceSha256=sha256(path),
                reproductionCommand=report.get('reproductionCommand', ['python', report.get('generator',
                    'qualify_heap_search_drafts_20261031.py')]), acceptedSourceBytes=0,
                limitations=report.get('limitations', report.get('limits', []))))
    report = dict(schemaVersion=1, generator='make_behavior_draft_ledger_20261101.py', generatorSha256=sha256(__file__),
        buildSha256=configuration()['romSha256'], functions=rows, uniqueBehaviorQualifiedDraftFunctions=len(rows),
        uniqueDraftNativeInitializedBytes=sum(r['initializedBytes'] for r in rows), acceptedSourceBytes=0,
        doesNotModifyCanonicalAcceptedLedger=True, overallGameCompletionPercentage=None,
        limitations=['This version enumerates only its explicit measured packets, not every historical draft',
            'Matching ranges of a nonmatching function receive no accepted byte credit',
            'Alternative source views and supplementary connected executions do not duplicate function or byte totals',
            'Candidate objects and artifacts must be regenerated by the listed evidence producers on a clean checkout'])
    write_json(ROOT / 'ledger/behavior-drafts-20261101.json', report)
    print(dict(functions=len(rows), draftNativeBytes=report['uniqueDraftNativeInitializedBytes'], acceptedBytes=0))


if __name__ == '__main__':
    main()
