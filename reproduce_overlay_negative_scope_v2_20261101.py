import argparse
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
import match_main_reward437_20261101 as reward437
import match_ov001_clamp453_20261101 as clamp453
import match_ov001_reward458_20261101 as reward458
from project import ROOT, read_json, write_json, sha256
from recovery_order import references
from seal_recovery_sources_20261031 import seal_sources

FAMILIES = {
    'reward437': (reward437, 'main-20261101-reward437', 'compiledWrongModeControl'),
    'clamp453': (clamp453, 'ov001-20261101-clamp453', 'compiledReturningControls'),
    'reward458': (reward458, 'ov001-20261101-reward458', 'compiledReturningControls'),
}


def identities(document):
    fields = ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']
    return [{key: row.get(key) for key in fields} for row in document['matches']]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=FAMILIES, required=True)
    parser.add_argument('--prepare', action='store_true')
    options = parser.parse_args()
    producer, stem, field = FAMILIES[options.family]
    relative = 'evidence/matches/' + stem + '.json'
    canonical = ROOT / relative
    previous = canonical.read_bytes()
    original = read_json(canonical)
    path = ROOT / ('evidence/matches/negative-scope-v2-diagnostics/' + stem + '.json') if options.prepare else canonical
    relative = path.relative_to(ROOT).as_posix()
    try:
        def capture(target, document):
            assert Path(target).resolve() == canonical.resolve()
            write_json(path, document)
        if options.prepare:
            with patch.object(producer, 'write_json', capture):
                producer.run()
        else:
            producer.run()
        document = read_json(path)
        if options.prepare:
            assert [r['objectSha256'] for r in document['matches']] == [r['objectSha256'] for r in original['matches']]
        assert identities(document) == identities(original)
        oracle = document['oracle']
        controls = oracle.pop(field)
        artifacts = list(references(controls))
        assert artifacts and all(row['source'].startswith('nonmatching/') for row in artifacts)
        assert 'negativeEvidence' not in document
        document['negativeEvidence'] = {field: controls}
        oracle[field + 'EvidencePath'] = 'negativeEvidence.' + field
        document['negativeEvidenceClassification'] = dict(
            adapter=Path(__file__).name, adapterSha256=sha256(__file__),
            originalProducer=Path(producer.__file__).name,
            originalProducerSha256=sha256(producer.__file__),
            completeControlBlockSha256=digest(controls), negativeObjectRows=len(artifacts),
            allControlDetailsRetained=True, originalProducerUnmodified=True,
            positiveSourceAndTargetIdentitiesPreserved=True, newSourceOrByteCredit=0,
            scope='Compiled wrong bodies remain negative evidence; they are not positive oracle dependencies')
        write_json(path, document)
        seal_sources(relative, [Path(__file__).name, '--family', options.family])
        current = read_json(path)
        assert digest(current['negativeEvidence'][field]) == digest(controls)
        assert identities(current) == identities(original)
    except BaseException:
        if not options.prepare:
            canonical.write_bytes(previous)
        raise
    if options.prepare:
        assert canonical.read_bytes() == previous
    receipt = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        family=options.family, preparedOnly=options.prepare, report=canonical.relative_to(ROOT).as_posix(),
        normalizedReport=relative, previousReportSha256=hashlib.sha256(previous).hexdigest(),
        reportSha256=sha256(path), controlBlockSha256=digest(controls), negativeObjectRows=len(artifacts),
        originalProducerUnmodified=True, sourceAndTargetIdentitiesPreserved=True,
        sourceAndObjectIdentitiesPreserved=all(a['objectSha256'] == b['objectSha256'] for a,b in zip(original['matches'], current['matches'])),
        fullOriginalExecutionAndControlChecksRerun=True, newSourceOrByteCredit=0)
    write_json(ROOT / ('evidence/verification/' + options.family + '-negative-scope-v2-20261101.json'), receipt)
    print(dict(family=options.family, negativeObjectRows=len(artifacts), newSourceOrByteCredit=0), flush=True)


if __name__ == '__main__':
    main()
