import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from replay_save_core_large275_20261101 import compiler_replay


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    sources, profiles, functions, reports, duplicates = {}, {}, {}, [], []
    drafted_native_bytes, compiled_native_bytes = 0, 0
    for name in ('app-large276', 'app-large277'):
        path = 'evidence/lanes/save-core/' + name + '-20261101.json'
        report = json.loads((ROOT / path).read_text())
        assert report['complete']
        sidecar = report['fullProvenanceSidecar']
        packed = (ROOT / sidecar['path']).read_bytes()
        assert sha(packed) == sidecar['sha256']
        raw = gzip.decompress(packed)
        assert sha(raw) == sidecar['uncompressedSha256']
        rows = json.loads(raw)
        for row in rows:
            identity = row['module'], row['processor'], row['program'], row['mode'], row['address']
            if identity in functions:
                assert not row.get('drafted') and not functions[identity].get('drafted')
                duplicates.append(dict(identity=identity, sourceDrafted=False, newCoverage=0))
            functions[identity] = row
            if row.get('drafted'):
                assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
                sources[row['source']] = row['sourceSha256']
                drafted_native_bytes += row['bytes']
            for part in row.get('decompilation', {}).get('flatFragments', []):
                assert sha((ROOT / part['path']).read_bytes()) == part['sha256']
            if row.get('realLinked'):
                compiled_native_bytes += row['bytes']
            for attempt in row['compileAttempts']:
                if attempt.get('realLinkSucceeded'):
                    key = attempt['source'], tuple(attempt['flags']), attempt['compilerPath']
                    profiles[key] = attempt
        reports.append(dict(path=path, sha256=sha((ROOT / path).read_bytes()), sidecar=sidecar))
    assert len(functions) == 37 and len(duplicates) == 1 and len(sources) == 28 and len(profiles) == 28
    assert len({row['source'] for row in profiles.values()}) == 14
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        current = list(pool.map(compiler_replay, profiles.values()))
    raw = (json.dumps(current, sort_keys=True, indent=2) + '\n').encode()
    sidecar = ROOT / 'evidence/vectors/save-core-application-drafts285-compiler-20261101.json.gz'
    sidecar.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schema=1, selectedAttempts=38, uniqueSelectedFunctions=37, selectedNativeBytes=35360, sourceHypotheses=28,
        draftNativeBytes=drafted_native_bytes, compiledSourceHypotheses=14, compiledNativeBytes=compiled_native_bytes,
        genuineLinkedProfiles=28, exactSourceFunctions=0, nativeSemanticallyQualified=0, acceptedBytes=0,
        compilerWorkers=2, repeatedFailedAttempts=duplicates, sources=[dict(path=path, sha256=digest) for path, digest in sorted(sources.items())],
        archivedSelectionReports=reports, currentCompilerProvenance=dict(path=sidecar.relative_to(ROOT).as_posix(),
            sha256=sha(sidecar.read_bytes()), uncompressedSha256=sha(raw)), generatorSha256=sha(Path(__file__).read_bytes()),
        limits=['Existing drafts are refinements;no new accepted function/code coverage follows from compiling them.',
            'This cold-safe replay uses committed source/native/profile hashes andcurrent genuine links;it never depends onhistorical debug object paths.',
            'Archival selection/decompilation producers inspect prior selected sources andexclusions;they are not required toregenerate a source-identical corpus frommutable current selection.',
            'Noncompiling andfailed-conversion candidates remain explicit backlog,with no invented arities,source suppression,assembly orbyte patching.',
            'Preparation/identity/skill call anchors prioritize the queue only;they establish no scene/prerequisite/consumption meaning.'])
    output = ROOT / 'evidence/lanes/save-core/application-drafts285-replay-20261101.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('uniqueSelectedFunctions', 'sourceHypotheses', 'compiledSourceHypotheses', 'genuineLinkedProfiles', 'exactSourceFunctions', 'acceptedBytes')}))


if __name__ == '__main__':
    main()
