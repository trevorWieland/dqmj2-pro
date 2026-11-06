import json
import shutil
import subprocess
import sys
from project import ROOT, sha256, write_json


def main():
    target = ROOT.parent / 'wl1104-replay'
    target.mkdir(exist_ok=False)
    relative = 'evidence/lanes/parallel-wave20261104/child-arm7-wl/packet-ready.json'
    report = json.loads((ROOT / relative).read_text())
    pins = json.loads((ROOT / report['inputManifest']).read_text())
    names = {p['path'] for p in pins['generatorSources']}
    names.update(e['source'] for e in pins['entries'])
    names.update(p['path'] for e in pins['entries'] for p in e['sourceDependencies'])
    names.update(p['path'] for p in pins['mandatoryExternalInputs'])
    names.update([relative, report['inputManifest'],
        'tools/mwccarm.zip', 'tools/mwccarm/mwccarm/license.dat', 'extract/files/dwc/utility.bin'])
    names.add('extract/utility/runtime/utility-child-arm7-wram.bin')
    for directory in ['tools/mwccarm/mwccarm/2.0/base', 'tools/mwccarm/mwccarm/1.2/sp4', 'tools/mwccarm/mwccarm/1.2/base']:
        names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / directory).iterdir() if p.suffix.lower() in ('.dll', '.exe'))
    copies = []
    for name in sorted(names):
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
        copies.append(dict(path=name, sha256=sha256(destination)))
    shutil.copytree(ROOT / 'deps/native', target / 'deps/native', ignore=shutil.ignore_patterns('__pycache__'))
    command = [sys.executable, str(target / 'wave20261104_child_wl_packet.py'), '--verify', '--inputs-sha256', report['inputManifestSha256']]
    process = subprocess.run(command, cwd=target.parent, capture_output=True, text=True, timeout=600)
    result = dict(generator=__file__, generatorSha256=sha256(__file__), copiedRoot=str(target),
        independentSourceAndToolCopies=True, originalWorkObjectsCopied=False, originalBuildProductsCopied=False,
        unrelatedArm9InventoryPresent=False, startupAssociationReportPresent=False,
        command=command, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr, copiedFiles=copies,
        fullGameOrRomBuildProof=False, behaviorExecutionCredit=0)
    if process.returncode == 0:
        fresh = json.loads((target / relative).read_text())
        original = {e['name']: e for e in report['matches']}
        contract_keys = ['name', 'program', 'processor', 'module', 'address', 'mode', 'bytes', 'source',
            'sourceSha256', 'sourceDependencies', 'targetSha256', 'inputModuleSha256', 'compiler', 'compilerSha256', 'compilerFlags']
        result.update(functions=len(fresh['matches']), bytes=sum(e['bytes'] for e in fresh['matches']),
            objectHashesChanged=sum(e['objectSha256'] != original[e['name']]['objectSha256'] for e in fresh['matches']),
            allMetadataNamesCopiedRoot=all(e['realLink']['linkerAttempt']['cwd'].startswith(str(target)) for e in fresh['matches']),
            freshlyPublishedCanonicalReportSha256=sha256(target / relative),
            sourceAndNativeContractsIdentical=all(all(e.get(k) == original[e['name']].get(k) for k in contract_keys) for e in fresh['matches']))
        if not result['allMetadataNamesCopiedRoot'] or not result['sourceAndNativeContractsIdentical']:
            raise ValueError('Copied-root metadata or source/native contract mismatch')
    output = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wl/copied-root-replay-proof.json'
    write_json(output, result)
    print({k: v for k, v in result.items() if k not in ['copiedFiles', 'stdout', 'stderr']})
    if process.returncode:
        print(process.stdout[-3000:])
        print(process.stderr[-1000:])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
