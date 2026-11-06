from project import ROOT, read_json, write_json, sha256

NAMES = ['20261102-sequential844', '20261102-allocation845', '20261102-battle847', '20261102-battle848', '20261102-battle852', '20261102-battle853', '20261102-battle854', '20261102-profile855', '20261102-writer857', '20261102-writer858']


def execute():
    functions = {}
    attempts = failures = 0
    for name in NAMES:
        for path in (ROOT / 'nonmatching/overlay-lane' / name).rglob('*results.json'):
            data = read_json(path)
            for group in data.get('attempts', [data]):
                for value in group.get('rows', []):
                    attempts += 1
                    source = value['source']
                    proof = value.get('genuineLink', {})
                    if source.get('compileFailed'):
                        failures += 1
                        continue
                    key = tuple(source[k] for k in ['processor', 'module', 'mode', 'address'])
                    row = functions.setdefault(key, dict(identity={k: source[k] for k in ['processor', 'module', 'mode', 'address']}, nativeBytes=source['bytes'], compiled=True, genuinelyLinked=False, exactCandidate=False, bestMatchingBytes=0, bestOutputBytes=None, records=[]))
                    linked = proof.get('exactCallerBytes', False) or ('nativeBytes' in proof and 'linkedBytes' in proof)
                    exact = proof.get('exactCallerBytes', False)
                    matching = source['bytes'] if exact else proof.get('matchingBytes', 0)
                    if matching > row['bestMatchingBytes']:
                        row['bestMatchingBytes'] = matching
                        row['bestOutputBytes'] = source['bytes'] if exact else proof.get('linkedBytes')
                    row['genuinelyLinked'] |= bool(linked)
                    row['exactCandidate'] |= bool(exact)
                    row['records'].append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), source=source['source'], sourceSha256=source['sourceSha256'], genuinelyLinked=bool(linked), exactCandidate=bool(exact)))
    rows = list(functions.values())
    report = dict(schemaVersion=1, sourceCredit=0, attemptRows=attempts, compilerFailedRows=failures, functions=rows, uniqueCompiledFunctions=len(rows), uniqueCompiledNativeBytes=sum(r['nativeBytes'] for r in rows), uniqueGenuinelyLinkedFunctions=sum(r['genuinelyLinked'] for r in rows), uniqueGenuinelyLinkedNativeBytes=sum(r['nativeBytes'] for r in rows if r['genuinelyLinked']), uniqueExactCandidates=sum(r['exactCandidate'] for r in rows), uniqueExactCandidateBytes=sum(r['nativeBytes'] for r in rows if r['exactCandidate']), limits=['Unique reworked/frontier functions within this packet; overlaps earlier842 queue and is not additive project source coverage.', 'Only separately frozen846/849 have completed native/model/control proofs; all other compiler/Ghidra sources remain zero matching credit.'])
    write_json(ROOT / 'evidence/attempts/overlay850-followup-measurements-20261102.json', report)
    print({key: value for key, value in report.items() if key not in ['functions', 'limits']})


if __name__ == '__main__':
    execute()
