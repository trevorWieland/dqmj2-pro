import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def main():
    lane = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wm/callbacks'
    copied_root = ROOT.parent / 'wm1104-cb-replay'
    if (copied_root / 'evidence/utility/ghidra-arm9.json').exists() or (copied_root / 'evidence/matches/utility-arm9-startup01.json').exists():
        raise ValueError('Fourth replay must demonstrate independence from unrelated ARM9 inventory/startup metadata')
    previous = read_json(lane / 'copied-root-replay-proof.json')
    if previous['exitCode'] != 0 or not previous['sourceAndNativeContractsIdentical']:
        raise ValueError('Independent copied-source packet replay must precede the bridge test')
    descriptor_relative = (lane / 'canonical-packet.json').relative_to(ROOT).as_posix()
    descriptor = read_json(ROOT / descriptor_relative)
    names = set(code_closure([descriptor['producer'][0], 'replay_parallel_packet.py']))
    names.add(descriptor_relative)
    copies = []
    for name in sorted(names):
        source, destination = ROOT / name, copied_root / name
        if destination.exists():
            if sha256(destination) != sha256(source):
                raise ValueError('Copied producer closure differs before bridge: ' + name)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        copies.append(dict(path=name, sha256=sha256(destination)))
    original = read_json(ROOT / descriptor['workerReport'])
    stale = dict(original, staleCanonicalNegativeControl=True)
    write_json(copied_root / descriptor['workerReport'], stale)
    write_json(copied_root / descriptor['canonicalReport'], stale)
    command = [sys.executable, str(copied_root / 'replay_parallel_packet.py'), descriptor_relative]
    process = subprocess.run(command, cwd=copied_root, capture_output=True, text=True, timeout=600)
    result = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), command=command,
        copiedRoot=str(copied_root), exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr,
        independentSourceAndToolCopies=True, originalWorkObjectsCopied=False, originalBuildProductsCopied=False,
        staleWorkerAndCanonicalMetadataNegativeControl=True, sourceAndNativeContractsIdentical=False,
        bridgeCopies=copies, nativeExecutionCredit=0, fullGameOrRomBuildProof=False)
    if process.returncode == 0:
        worker = read_json(copied_root / descriptor['workerReport'])
        canonical = read_json(copied_root / descriptor['canonicalReport'])
        baseline = {e['name']: e for e in original['matches']}
        contracts = ['name', 'program', 'processor', 'module', 'address', 'mode', 'bytes', 'source',
            'sourceSha256', 'sourceDependencies', 'targetSha256', 'inputModuleSha256', 'compiler', 'compilerSha256', 'compilerFlags']
        equal = len(canonical['matches']) == len(baseline) and all(all(e.get(k) == baseline[e['name']].get(k) for k in contracts) for e in canonical['matches'])
        current = {e['name']: e for e in worker['matches']}
        fresh = canonical.get('canonicalReportRefreshedFromFreshWorkerObjects') is True and canonical['matches'] == worker['matches']
        paths = all(e['realLink']['linkerAttempt']['cwd'].startswith(str(copied_root)) for e in canonical['matches'])
        object_hashes = all(sha256(copied_root / e['object']) == e['objectSha256'] for e in canonical['matches'])
        links = all(sha256(copied_root / e['realLink']['linkedElf']) == e['realLink']['linkedElfSha256'] and
            sha256(copied_root / e['realLink']['lcf']) == e['realLink']['lcfSha256'] for e in canonical['matches'])
        stale_removed = not worker.get('staleCanonicalNegativeControl') and not canonical.get('staleCanonicalNegativeControl')
        result.update(functions=len(current), bytes=sum(e['bytes'] for e in current.values()), canonicalReportFresh=fresh,
            allMetadataNamesCopiedRoot=paths, allFreshObjectHashesValid=object_hashes, allFreshLinkMetadataValid=links,
            sourceAndNativeContractsIdentical=equal, staleWorkerAndCanonicalReportsReplaced=stale_removed,
            objectHashesChanged=sum(e['objectSha256'] != baseline[e['name']]['objectSha256'] for e in canonical['matches']),
            canonicalReportSha256=sha256(copied_root / descriptor['canonicalReport']),
            workerReportSha256=sha256(copied_root / descriptor['workerReport']))
        if not all([fresh, paths, object_hashes, links, equal, stale_removed]):
            raise ValueError('Copied-root canonical replay retained stale metadata or changed a source/native contract')
        inventory = copied_root / 'evidence/utility/ghidra-arm7.json'
        original_inventory = inventory.read_bytes()
        objects_before = [(e['object'], sha256(copied_root / e['object']), (copied_root / e['object']).stat().st_mtime_ns) for e in canonical['matches']]
        try:
            inventory.write_bytes(original_inventory + b'\n')
            negative = subprocess.run([sys.executable, str(copied_root / descriptor['producer'][0]), *descriptor['producer'][1:]],
                cwd=copied_root, capture_output=True, text=True, timeout=60)
        finally:
            inventory.write_bytes(original_inventory)
        objects_after = [(e['object'], sha256(copied_root / e['object']), (copied_root / e['object']).stat().st_mtime_ns) for e in canonical['matches']]
        rejected = negative.returncode != 0 and 'Immutable inventory/configuration input changed' in negative.stderr
        if not rejected or objects_before != objects_after:
            raise ValueError('Mutated external inventory was not rejected before compilation')
        result.update(arm9InventoryPresent=False, arm9StartupReportPresent=False,
            immutableExternalInputMutationRejected=True, compilerObjectsUnchangedByRejectedInventory=True,
            inventoryNegativeControlExitCode=negative.returncode, inventoryNegativeControlStderr=negative.stderr)
    write_json(lane / 'copied-root-canonical-bridge-proof.json', result)
    print({k: v for k, v in result.items() if k not in ['stdout', 'stderr', 'bridgeCopies']})
    if process.returncode:
        print(process.stdout[-3000:])
        print(process.stderr[-1000:])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
