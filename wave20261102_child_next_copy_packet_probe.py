import json
import shutil
import subprocess
import sys
from project import ROOT, sha256, write_json


def main():
    target = ROOT.parent / 'child-next-replay-20261102'
    target.mkdir(exist_ok=False)
    report_relative = 'evidence/lanes/parallel-wave20261102/utility-child-next/packet-ready.json'
    report = json.loads((ROOT / report_relative).read_text())
    pins = json.loads((ROOT / report['inputManifest']).read_text())
    names = {p['path'] for p in pins['generatorSources']}
    names.update(e['source'] for e in pins['entries'])
    names.update([report_relative, report['inputManifest'], 'wave20261102_child_next_replay_first.py',
        'project.json', 'evidence/utility/ghidra-arm9.json', 'evidence/utility/ghidra-arm7.json',
        'evidence/matches/utility-arm9-startup01.json', 'tools/mwccarm.zip',
        'tools/mwccarm/mwccarm/license.dat', 'extract/files/dwc/utility.bin'])
    startup = json.loads((ROOT / 'evidence/matches/utility-arm9-startup01.json').read_text())
    names.update(e['source'] for e in startup['matches'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'extract/utility/runtime').glob('*.bin'))
    for directory in ['tools/mwccarm/mwccarm/2.0/base', 'tools/mwccarm/mwccarm/1.2/sp4', 'tools/mwccarm/mwccarm/1.2/base']:
        names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / directory).iterdir() if p.suffix.lower() in ('.dll', '.exe'))
    copies = []
    for name in sorted(names):
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
        copies.append(dict(path=name, sha256=sha256(destination)))
    shutil.copytree(ROOT / 'deps/native', target / 'deps/native', ignore=shutil.ignore_patterns('__pycache__'))
    command = [sys.executable, str(target / 'wave20261102_child_next_replay_first.py'), '--report', report_relative,
        '--producer', 'wave20261102_child_next_packet.py', '--inputs-sha256', report['inputManifestSha256']]
    process = subprocess.run(command, cwd=target.parent, capture_output=True, text=True, timeout=600)
    result = dict(generator=__file__, generatorSha256=sha256(__file__), copiedRoot=str(target),
        independentSourceAndToolCopies=True, originalWorkObjectsCopied=False, originalBuildProductsCopied=False,
        command=command, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr, copiedFiles=copies)
    if process.returncode == 0:
        fresh = json.loads((target / report_relative).read_text())
        original = {e['name']: e for e in report['matches']}
        result.update(functions=len(fresh['matches']), bytes=sum(e['bytes'] for e in fresh['matches']),
            objectHashesChanged=sum(e['objectSha256'] != original[e['name']]['objectSha256'] for e in fresh['matches']),
            allMetadataNamesCopiedRoot=all(e['realLink']['linkerAttempt']['cwd'].startswith(str(target)) for e in fresh['matches']),
            freshlyPublishedCanonicalReportSha256=sha256(target / report_relative),
            sourceAndNativeContractsIdentical=all(e['sourceSha256'] == original[e['name']]['sourceSha256'] and
                e['targetSha256'] == original[e['name']]['targetSha256'] for e in fresh['matches']))
    output = ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-next/copied-root-replay-proof.json'
    write_json(output, result)
    print({k: v for k, v in result.items() if k != 'copiedFiles'})
    if process.returncode:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
