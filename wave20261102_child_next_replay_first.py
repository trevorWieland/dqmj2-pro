import argparse
import json
import subprocess
import sys
from pathlib import Path
from project import ROOT, sha256, write_json, now

DEFAULT_REPORT = 'evidence/lanes/parallel-wave20261102/utility-child/packet-ready.json'
DEFAULT_INPUTS_SHA = '6e077b350eb633bb302c3e43b72316d7bc126dc62057969fd25d127518777172'


def replay(report_relative, producer, inputs_sha):
    report_path = (ROOT / report_relative).resolve()
    if not report_path.is_relative_to(ROOT) or report_path.suffix != '.json':
        raise ValueError('Report path must stay within this project root')
    if producer not in ['wave20261102_child_packet.py', 'wave20261102_child_next_packet.py']:
        raise ValueError('Unqualified frozen producer')
    original = json.loads(report_path.read_text())
    pins_path = ROOT / original['inputManifest']
    if sha256(pins_path) != inputs_sha or original['inputManifestSha256'] != inputs_sha:
        raise ValueError('Committed immutable input manifest differs')
    pins = json.loads(pins_path.read_text())
    for pin in pins['generatorSources']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Frozen source generator changed: ' + pin['path'])
    for entry in pins['entries']:
        if sha256(ROOT / entry['source']) != entry['sourceSha256'] or sha256(ROOT / entry['compiler']) != entry['compilerSha256']:
            raise ValueError('Frozen source/compiler changed')
    archive = report_path.with_name(report_path.stem + '-original.json')
    if not archive.exists():
        archive.write_bytes(report_path.read_bytes())
    command = [sys.executable, str(ROOT / producer), '--packet', report_path.name, '--verify']
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=600)
    attempt = dict(command=command, cwd=str(ROOT), exitCode=process.returncode,
                   stdout=process.stdout, stderr=process.stderr, finishedUtc=now())
    write_json(report_path.with_name(report_path.stem + '-replay-attempt.json'), attempt)
    if process.returncode:
        raise ValueError('Frozen producer replay failed')
    generated_path = report_path.with_name(report_path.stem + '-verification.json')
    generated = json.loads(generated_path.read_text())
    expected = {(e['module'], e['mode'], e['address']): e for e in pins['entries']}
    actual = {(e['module'], e['mode'], e['address']): e for e in generated['matches']}
    if len(actual) != len(generated['matches']) or set(actual) != set(expected) or generated.get('failed'):
        raise ValueError('Fresh identity set differs')
    keys = ['name', 'program', 'processor', 'module', 'mode', 'address', 'bytes', 'inputModuleSha256',
            'targetSha256', 'source', 'sourceSha256', 'sourceDependencies', 'compiler', 'compilerSha256', 'compilerFlags']
    for identity, entry in actual.items():
        if any(entry.get(k) != expected[identity].get(k) for k in keys):
            raise ValueError('Frozen source/target/compiler contract differs: ' + str(identity))
        if not entry.get('exactAfterDeclaredRelocation') or not entry.get('exactAfterRealMwLink'):
            raise ValueError('Fresh bytes or real link are unproved')
        if sha256(ROOT / entry['object']) != entry['objectSha256']:
            raise ValueError('Fresh source object is stale')
        link = entry['realLink']
        if not link.get('exactCallerBytes') or link['nativeSpanSha256'] != entry['targetSha256']:
            raise ValueError('Fresh link target differs')
        if sha256(ROOT / link['linkedElf']) != link['linkedElfSha256'] or sha256(ROOT / link['lcf']) != link['lcfSha256']:
            raise ValueError('Fresh link products are stale')
        if not Path(link['linkerAttempt']['cwd']).resolve().is_relative_to(ROOT):
            raise ValueError('Link metadata names another checkout root')
    producer_pins = {p['path']: p for p in generated['generatorSources']}
    producer_pins[Path(__file__).name] = dict(path=Path(__file__).name, sha256=sha256(__file__))
    generated.update(generatorSources=list(producer_pins.values()),
        reproduce=['python ' + Path(__file__).name + ' --report ' + report_relative +
                   ' --producer ' + producer + ' --inputs-sha256 ' + inputs_sha],
        replayCanonicalReportRefreshed=True, replayRoot=str(ROOT),
        originalReadyReportArchive=archive.relative_to(ROOT).as_posix(),
        originalReadyReportArchiveSha256=sha256(archive), sourceContractsUnchanged=True)
    write_json(report_path, generated)
    summary = dict(report=report_relative, inputManifestSha256=inputs_sha,
        exactFunctions=len(actual), exactInitializedBytes=sum(e['bytes'] for e in actual.values()),
        freshObjectHashesPublished=True, freshRootMetadataPublished=True, sourceContractsUnchanged=True,
        root=str(ROOT), canonicalReportSha256=sha256(report_path), finishedUtc=now())
    write_json(report_path.with_name(report_path.stem + '-canonical-replay.json'), summary)
    print(summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', default=DEFAULT_REPORT)
    parser.add_argument('--producer', default='wave20261102_child_packet.py')
    parser.add_argument('--inputs-sha256', default=DEFAULT_INPUTS_SHA)
    args = parser.parse_args()
    replay(args.report, args.producer, args.inputs_sha256)


if __name__ == '__main__':
    main()
