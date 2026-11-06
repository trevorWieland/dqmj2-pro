from pathlib import Path
from project import ROOT, read_json, write_json, sha256, configuration


def main():
    stems = ['main-breadth14', 'main-breadth-next15', 'main-breadth-next16',
             'main-breadth-next17', 'main-breadth-small18', 'main-breadth-small19']
    records, queues, inputs = [], set(), []
    for stem in stems:
        path = ROOT / f'evidence/attempts/{stem}-20261101.json'
        linked = ROOT / f'evidence/attempts/{stem}-genuine-links-20261101.json'
        draft, links = read_json(path), read_json(linked)
        assert draft['state'] == links['state'] == 'finished'
        inputs.extend(dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in [path, linked])
        proofs = {(row['mode'], row['address']): row for row in links['results']}
        for row in draft['queue']:
            key = row['mode'], int(row['address'], 0)
            assert key not in queues
            queues.add(key)
        for row in draft['results']:
            attempts = [item for item in row.get('attempts', []) if item.get('compiledBytes')]
            selected = max(attempts, key=lambda item: item.get('matchingBytes', 0)) if attempts else None
            source = selected['source'] if selected else row.get('draftSource')
            if not source or not (ROOT / source).is_file():
                continue
            source_path = (ROOT / source).resolve()
            assert source_path.is_relative_to(ROOT / 'work') and source_path.suffix == '.c'
            data = source_path.read_bytes()
            original_hash = sha256(source_path)
            if selected:
                assert original_hash == selected['sourceSha256']
            address, mode = int(row['address'], 0), row['mode']
            destination = ROOT / f'generated/recovery/20261101-root-breadth/{mode}-{address:08x}.c'
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                assert destination.read_bytes() == data
            else:
                destination.write_bytes(data)
            proof = proofs.get((mode, row['address']), {})
            records.append(dict(processor='arm9', program='', module='main', mode=mode,
                address=hex(address), initializedBytes=row['bytes'], source=destination.relative_to(ROOT).as_posix(),
                sourceSha256=sha256(destination), observedOriginalPath=source,
                originalSourceHashPinnedByCompiledProof=bool(selected),
                compiledInHistoricalProof=bool(selected), compilerFlags=selected['compilerFlags'] if selected else [],
                originalCompilerSha256=selected.get('compilerSha256') if selected else None,
                originalObjectSha256=selected.get('objectSha256') if selected else None,
                compilerMatchingBytes=selected.get('matchingBytes') if selected else None,
                genuineHistoricalLink=bool(proof.get('freshLinkedBinaryProduced')),
                exactHistoricalLinkedBytes=bool(proof.get('exact')), sourceCredit=0,
                sourceReport=path.relative_to(ROOT).as_posix(), sourceReportSha256=sha256(path),
                linkReport=linked.relative_to(ROOT).as_posix(), linkReportSha256=sha256(linked)))
    assert len({(r['mode'], r['address']) for r in records}) == len(records)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=configuration()['romSha256'], inputReports=inputs, records=records,
        queuedIdentities=len(queues), archivedDrafts=len(records),
        historicallyCompiledUnits=sum(r['compiledInHistoricalProof'] for r in records),
        historicallyCompiledInitializedBytes=sum(r['initializedBytes'] for r in records if r['compiledInHistoricalProof']),
        historicallyGenuinelyLinkedUnits=sum(r['genuineHistoricalLink'] for r in records),
        historicallyExactHypotheses=sum(r['exactHistoricalLinkedBytes'] for r in records),
        acceptedSourceCredit=0, freshArchiveRecompileProven=False,
        limitations=['Generated C hypotheses preserve unsafe or unproved types and signatures',
            'Historical byte matches are not semantic acceptance or additional current coverage',
            'Only original C texts are archived; no original ARM code, objects, or cached executable payloads',
            'Failed drafts without a historical source hash are explicitly snapshots of the currently observed artifact'])
    path = ROOT / 'evidence/attempts/root-breadth-source-archive-20261101.json'
    write_json(path, report)
    names = [r['source'] for r in records] + [path.relative_to(ROOT).as_posix(), Path(__file__).name]
    write_json(ROOT / 'provenance/root-breadth-generated-c-20261101.json', dict(
        schemaVersion=1, sourceCredit=0, generatedHypotheses=True,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print({key: report[key] for key in ['queuedIdentities', 'archivedDrafts', 'historicallyCompiledUnits',
        'historicallyCompiledInitializedBytes', 'historicallyGenuinelyLinkedUnits', 'historicallyExactHypotheses', 'acceptedSourceCredit']})


if __name__ == '__main__':
    main()
