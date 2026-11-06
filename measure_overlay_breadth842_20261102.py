import json
from project import ROOT, read_json, sha256, write_json

BASES = ['nonmatching/overlay-lane/20261102-battle816', 'nonmatching/overlay-lane/20261102-battle825', 'nonmatching/overlay-lane/20261102-battle835']
FOLLOWUPS = {
    ('ov001', 0x021F7D70): ['nonmatching/overlay-lane/20261102-stack819/021f7d70/results.json'],
    ('ov001', 0x021F2878): ['evidence/matches/ov001-20261102-action822.json'],
    ('ov001', 0x021F35F0): ['evidence/matches/ov001-20261102-action830.json'],
    ('ov006', 0x021D85D4): ['nonmatching/overlay-lane/20261102-load-stack837/021d85d4/results.json'],
    ('ov006', 0x02204F6C): ['nonmatching/overlay-lane/20261102-load-stack837/02204f6c/results.json'],
    ('ov006', 0x021DB6A8): ['nonmatching/overlay-lane/20261102-ghidra-repair839/021db6a8/results.json'],
    ('ov006', 0x021DC878): ['nonmatching/overlay-lane/20261102-ghidra-repair839/021dc878/results.json'],
    ('ov006', 0x021DBE64): ['evidence/matches/ov006-20261102-row841.json'],
    ('ov006', 0x021EA7D8): ['nonmatching/overlay-lane/20261102-ghidra-repair839/021ea7d8/results.json'],
}


def compile_rows(report):
    rows = []
    for item in report.get('results', []):
        if 'source' in item:
            rows.append(item)
        else:
            rows.extend(compile_rows(item))
    for item in report.get('matches', []):
        rows.append(dict(source=item, genuineLink=item.get('realLink', {})))
    return rows


def execute():
    snapshot = next((ROOT / 'evidence/verification').glob('accepted-cohort136-identities-v2-*.json'))
    selected = read_json(snapshot)['functions']
    output = []
    for base in BASES:
        queue = read_json(ROOT / base / 'queue.json')
        for entry in queue['functions']:
            key = entry['module'], int(entry['address'], 0)
            path = ROOT / entry['directory'] / 'draft-results.json'
            initial = read_json(path)
            records = []
            compilerOnly = False
            materialized = False
            for profile in initial['results']:
                materialized |= profile.get('materialized', False)
                for attempt in profile.get('compilerAttempts', []):
                    records.extend(attempt.get('rows', []))
                    compilerOnly |= attempt.get('compilerOnlyObserved', False)
            history = [dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path))]
            behavioral = []
            for relative in FOLLOWUPS.get(key, []):
                followup = read_json(ROOT / relative)
                records.extend(compile_rows(followup))
                history.append(dict(path=relative, sha256=sha256(ROOT / relative)))
                if followup.get('allPassed') and followup.get('canonicalMatchedBytes') == entry['bytes']:
                    behavioral.append(dict(report=relative, reportSha256=sha256(ROOT / relative), totals=followup['totals']))
            compiled = compilerOnly or any(not row['source'].get('compileFailed') and row['source'].get('objectSha256') for row in records)
            linked = any(isinstance(row.get('genuineLink'), dict) and ('matchingBytes' in row['genuineLink'] or row['genuineLink'].get('exactCallerBytes')) for row in records)
            exact = [row for row in records if isinstance(row.get('genuineLink'), dict) and row['genuineLink'].get('exactCallerBytes')]
            sourceHashes = {row['source'].get('sourceSha256') for row in exact}
            accepted = [row for row in selected if row['processor'] == entry['processor'] and not row.get('program') and row['module'] == entry['module'] and row['mode'] == entry['mode'] and row['address'] == int(entry['address'], 0) and row['sourceSha256'] in sourceHashes]
            output.append(dict(identity={name: entry[name] for name in ['processor', 'program', 'module', 'mode', 'address']}, nativeBytes=entry['bytes'], nativeSpanSha256=entry['nativeSpanSha256'], moduleSha256=entry['moduleSha256'], originallyMaterialized=bool(materialized), currentCompilerObserved=bool(compiled), currentGenuineLinkObserved=bool(linked), exactCandidateObserved=bool(exact), exactSourceHashes=sorted(value for value in sourceHashes if value), nativeModelQualified=bool(behavioral), behaviorReports=behavioral, acceptedInFrozenSnapshot=bool(accepted), history=history, initialSourceClosures=[item.get('sourceClosure', []) for item in initial['results']]))
    def metric(field):
        rows = [row for row in output if row[field]]
        return dict(functions=len(rows), nativeBytes=sum(row['nativeBytes'] for row in rows))
    report = dict(schemaVersion=1, romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6', sourceCreditGrantedByThisLedger=0, snapshot=snapshot.relative_to(ROOT).as_posix(), snapshotSha256=sha256(snapshot), generatorSha256=sha256(__file__), selected=dict(functions=len(output), nativeBytes=sum(row['nativeBytes'] for row in output)), originallyMaterialized=metric('originallyMaterialized'), compiled=metric('currentCompilerObserved'), genuinelyLinked=metric('currentGenuineLinkObserved'), exactCandidates=metric('exactCandidateObserved'), nativeModelQualified=metric('nativeModelQualified'), alreadyAcceptedInSnapshot=metric('acceptedInFrozenSnapshot'), functions=output, limits=['Source/compiler/native/exact/accepted stages remain separate. Native-byte totals count unique selected identities, not code similarity.', 'Approximate source and generated Ghidra/M2C outputs grant no matched source credit. Only the frozen integrator acceptance snapshot determines accepted coverage.', 'Historical drafts for some identities predate these fresh typed contexts; this is a selected-frontier census, not a claim that every source identity was first drafted here.', 'Four816 paths remain unsupported frontend/inherited-register cases. No fake saved-register formals, opcode patches, assembly or byte-array logic acceptance.'])
    write_json(ROOT / 'evidence/attempts/overlay-breadth842-measured-ledger-20261102.json', report)
    print({name: report[name] for name in ['selected', 'originallyMaterialized', 'compiled', 'genuinelyLinked', 'exactCandidates', 'nativeModelQualified', 'alreadyAcceptedInSnapshot']})


if __name__ == '__main__':
    execute()
