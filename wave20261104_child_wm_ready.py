import argparse
import json
from pathlib import Path
from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/child-arm7-wm'
CANONICAL = 'evidence/matches/utility-child-wm-parallel-wave20261104.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    worker = LANE / 'packet-ready.json'
    report = read_json(worker)
    manifest = read_json(ROOT / report['inputManifest'])
    if sha256(ROOT / report['inputManifest']) != report['inputManifestSha256']:
        raise ValueError('Frozen packet input changed')
    producer = ['wave20261104_child_wm_packet.py', '--verify', '--inputs-sha256', report['inputManifestSha256']]
    identities = []
    for row in report['matches']:
        identity = {key: row[key] for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']}
        identity['id'] = '/'.join([report['romSha256'], row['program'], row['processor'], row['module'], row['mode'], '%08x' % int(row['address'], 0)])
        identities.append(identity)
    descriptor = LANE / 'canonical-packet.json'
    value = dict(schemaVersion=1, romSha256=report['romSha256'], producer=producer,
        workerReport=worker.relative_to(ROOT).as_posix(), canonicalReport=CANONICAL,
        frozenInputs=[dict(path=report['inputManifest'], sha256=report['inputManifestSha256'])], identities=identities)
    if descriptor.exists() and read_json(descriptor) != value:
        raise ValueError('Canonical bridge descriptor is already frozen')
    if not descriptor.exists():
        write_json(descriptor, value)
    claim = read_json(LANE / 'claim.json')
    selected = {r['address'] for r in identities}
    remaining = [dict(r, state='unaccepted', sourceCredit=0) for r in claim['functions'] if r['address'] not in selected]
    for row in remaining:
        if row['address'] == '0x27e44a8':
            row['qualificationFailure'] = 'Unselected original function; see residual diagnostics for actual refusal'
    write_json(LANE / 'remaining-queue.json', dict(functions=remaining, remainingFunctions=len(remaining),
        remainingBytes=sum(r['bytes'] for r in remaining), sourceCredit=0, sealedSubsetIsIndependent=True))
    if args.prepare:
        print(dict(descriptor=descriptor.relative_to(ROOT).as_posix(), functions=len(identities), bytes=sum(r['bytes'] for r in identities)))
        return
    canonical = read_json(ROOT / CANONICAL)
    proof = read_json(LANE / 'copied-root-canonical-bridge-proof.json')
    if proof.get('exitCode') != 0 or not proof.get('canonicalReportFresh') or not proof.get('sourceAndNativeContractsIdentical'):
        raise ValueError('Full copied-root canonical bridge has not passed')
    expected = {r['name']: r for r in report['matches']}
    if len(canonical['matches']) != len(expected) or any(r['sourceSha256'] != expected[r['name']]['sourceSha256'] for r in canonical['matches']):
        raise ValueError('Fresh canonical report source identity differs')
    names = {p['path'] for p in manifest['generatorSources']}
    names.update(p['path'] for p in canonical['generatorSources'])
    names.update(p['path'] for p in manifest['mandatoryExternalInputs'])
    names.update(r['source'] for r in canonical['matches'])
    names.update(p['path'] for r in canonical['matches'] for p in r['sourceDependencies'])
    names.update([worker.relative_to(ROOT).as_posix(), report['inputManifest'],
        descriptor.relative_to(ROOT).as_posix(), Path(__file__).name,
        'wave20261104_child_wm_copy_probe.py', 'wave20261104_child_wm_bridge_probe.py',
        'wave20261104_child_wm_controls.py'])
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['whole-c-controls.json', 'arm7-index-equivalence.json',
        'remaining-queue.json', 'copied-root-replay-proof.json',
        'copied-root-canonical-bridge-proof.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)]
    ready = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', romSha256=report['romSha256'],
        functions=len(identities), bytes=sum(r['bytes'] for r in identities), sourceCreditPendingIntegrator=sum(r['bytes'] for r in identities),
        packets=[dict(report=worker.relative_to(ROOT).as_posix(), producer=producer, producerargv=producer)],
        frozenInputManifest=dict(path=report['inputManifest'], sha256=report['inputManifestSha256']),
        canonicalDescriptor=dict(path=descriptor.relative_to(ROOT).as_posix(), sha256=sha256(descriptor)),
        canonicalReplayCommand=['replay_parallel_packet.py', descriptor.relative_to(ROOT).as_posix()],
        identities=identities, files=files, actualNativeFunctionReturns=0, nativeAndRecompiledCalls=0,
        relocationsPreserved=sum(len(r['relocations']) for r in canonical['matches']),
        copiedRootCanonicalReplayPassed=True, remainingFunctions=len(remaining), remainingBytes=sum(r['bytes'] for r in remaining),
        wholeCNegativeControlsRejected=1, arm9StartupAssociationReportRequired=False,
        limits=['Complete ordinary C configured extents, relocation encoding/addends, pinned compilation and genuine MW linking are exact.',
            'Independent SDK behavioral fixtures, device execution and complete scene execution remain unproved; actual execution credit is zero.',
            'Original external data, constants, local callbacks and other callees retain zero recovered storage/function/source credit.',
            'Public reconstructed SDK names, types and revision are comparative evidence and do not establish original game authorship or SDK revision.',
            'The ARM7-only candidate/binding index preserves explicit original CPU/program/mode identities without widening original inventories or consuming ARM9 startup metadata.',
            'Remaining functions and all failed source/link experiments remain uncredited. The mutable claim and research products are not replay dependencies.',
            'Shared registry, whole-module/ROM regressions and source acceptance remain coordinator owned.'])
    write_json(LANE / 'ready.json', ready)
    print(dict(ready=(LANE / 'ready.json').relative_to(ROOT).as_posix(), files=len(files), functions=ready['functions'], bytes=ready['bytes']))


if __name__ == '__main__':
    main()
