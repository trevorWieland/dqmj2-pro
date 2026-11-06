import hashlib
import re
from collections import defaultdict
from pathlib import Path
from project import ROOT, read_json, sha256, write_json

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next'
CLAIM_SHA = '48f458e9cb0ff2d65c2f12373236a036440be602b54d537d1f78f81c03f8b005'
PACKETS = {
    'first': '4f84935eff456c6179f6df43c16d21817a5983c79c207d59c26e1050d653c35d',
    'second': '496f40e97c810c532f9d45b1f179690219264eced9ac31c1551247c9b1dcbb71',
    'seventh': '751df2e196e3f363c7b860551fb42512004123e8af28ca41ec4aa065ca20a2e5',
    'tenth': '7fbe3515f3c5dc43e49c6a9c6d5079db94f044b93f96ec8a2ece9e20a1eedf67',
    'eleventh': 'f4628c860f37890c0fdcda773287390d6bce04cbf7c8b4a275eb86e89c2a6307',
}
BLOCKERS = {
    '02060600': 'Typed text rendering source remains smaller than native; width/control/compiler-context differences, no byte-exact credit.',
    '020607ec': 'Typed text rendering loop remains partial; no allocation sweep or source credit.',
    '020609dc': 'Regional glyph branch scheduling remains partial; actual locale provider returns5 but counterfactual branches must remain measured.',
    '02063a0c': 'Signedness/byte stride recovered; remaining register-context differences, no source credit.',
    '02063ad0': '36-byte matrix clear/copy ABI recovered; remaining offset/base register allocation difference, parked.',
    '02064038': '100 entries at stride132 and signed8 list iteration recovered; remaining loop/count register-context difference.',
    '020641ac': 'Three/six4-byte metadata keys and pairwise duplicate checks recovered; remaining final-loop context difference.',
    '02065818': '93-way grid renderer has recovered12-byte context, packed fields, two-byte tile buffer and four-word draw calls. Still partial; former two-word draft interfaces were insufficient.',
    '02066358': '1812-byte effect dispatcher compiles to full extent with1639 matching bytes after six-word stat-provider call boundaries, full signed-word minus-one/minus-two result and separate case recovery. Remaining register/context differences; no behavior/whole-link/source credit.',
    '02066b30': 'Halfword-gated edge/state transitions recovered; context access/extra reload shape remains partial.',
    '02066d48': 'Ten-byte record matching and signed16 optional output recovered; loop/register context remains partial.',
    '02066f18': '96-byte sorted lookup proves32-byte records, a pointer at state+8 and an incoming unsigned key. Source remains partial, with caller-valid table/count bounds required.',
    '02067024': '720-byte encounter caller passes an incoming key in R0 to02066f18, not an unused leading word. All post-prolog instructions align in bounded probes; aggregate prolog register context remains partial. Complete records are32-byte ABI views with two4-byte indexed groups and a7-byte weighted group; no original allocation/authorship claim.',
}


def execute():
    claim_path = LANE / 'claim.json'
    if sha256(claim_path) != CLAIM_SHA:
        raise ValueError('Original exclusive ownership claim changed')
    claim = read_json(claim_path)
    rows = {format(int(x['address'], 0), '08x'): x for x in claim['claimedFunctions']}
    image_cache = {}
    for row in rows.values():
        path = ROOT / row['binary']
        if row['binary'] not in image_cache:
            if sha256(path) != row['inputModuleSha256']:
                raise ValueError('Original full native module changed')
            image_cache[row['binary']] = path.read_bytes()
        start = int(row['address'], 0) - row['base']
        body = image_cache[row['binary']][start:start + row['bytes']]
        if hashlib.sha256(body).hexdigest() != row['targetSha256']:
            raise ValueError('An originally claimed whole native function changed')
    pins, identities, packets = {}, {}, []
    for name, expected_sha in PACKETS.items():
        path = LANE / name / 'ready.json'
        if sha256(path) != expected_sha:
            raise ValueError('Frozen READY lineage changed: ' + name)
        ready = read_json(path)
        manifest = ready['frozenInputManifest']
        if sha256(ROOT / manifest['path']) != manifest['sha256']:
            raise ValueError('Frozen input manifest changed')
        for pin in read_json(ROOT / manifest['path'])['files']:
            if pin['path'] in pins and pins[pin['path']] != pin['sha256']:
                raise ValueError('Conflicting immutable packet inputs')
            pins[pin['path']] = pin['sha256']
        for item in ready['identities']:
            key = format(int(item['address'], 0), '08x')
            if key not in rows or key in identities or item['targetSha256'] != rows[key]['targetSha256']:
                raise ValueError('READY identities overlap or differ from exclusive native claim')
            identities[key] = item
        packets.append(dict(name=name, ready=path.relative_to(ROOT).as_posix(), sha256=expected_sha, functions=ready['functions'], bytes=ready['bytes']))
    for name, expected in pins.items():
        if sha256(ROOT / name) != expected:
            raise ValueError('A frozen actual source/tool/runtime input changed: ' + name)
    drafts = defaultdict(list)
    source_root = ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next'
    for path in source_root.rglob('*.c'):
        if re.fullmatch('[0-9a-f]{8}', path.stem):
            if path.stem not in rows:
                raise ValueError('Authored C is outside the exclusive claim')
            if path.stem not in identities:
                drafts[path.stem].append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), headerSha256=sha256(path.with_name('context.h'))))
    partials, untouched = [], []
    for name, row in rows.items():
        if name in identities:
            continue
        item = {key: row[key] for key in ['id', 'program', 'processor', 'module', 'mode', 'address', 'bytes', 'targetSha256']}
        item.update(sourceCredit=0, remainsExclusivelyReserved=True)
        if name in drafts:
            item.update(drafts=drafts[name], blocker=BLOCKERS[name], behavioralQualification=False, byteExactQualification=False)
            partials.append(item)
        else:
            item.update(status='not-authored-in-this-claim', knownAddressNamedArtifacts=row['knownAddressNamedArtifacts'], absenceOfLocalAuthorshipDoesNotProveUntouched=True)
            untouched.append(item)
    total = lambda values: sum(x['bytes'] for x in values)
    if (len(identities), total(identities.values()), len(partials), total(partials), len(untouched), total(untouched)) != (20, 2160, 13, 5172, 24, 5008):
        raise ValueError('Expected exclusive claim reconciliation differs')
    output = dict(schemaVersion=1, status='bounded-checkpoint-residuals-parked', claim=dict(path=claim_path.relative_to(ROOT).as_posix(), sha256=CLAIM_SHA),
                  claimedFunctions=57, claimedBytes=12340, frozenPackets=packets, proposedExactFunctions=20, proposedExactBytes=2160,
                  remainingFunctions=37, remainingBytes=10180, partialFunctions=13, partialBytes=5172, notAuthoredFunctions=24, notAuthoredBytes=5008,
                  originalNativeTargetHashesVerified=57, uniqueFrozenActualInputsVerified=len(pins), partials=partials, notAuthored=untouched,
                  sourceCreditGrantedByThisCheckpoint=0, modifiedSharedState=False, ownedLongRunningProcessesRemaining=False,
                  producer=dict(path=Path(__file__).resolve().relative_to(ROOT).as_posix(), sha256=sha256(__file__)),
                  limits=['READY proposals require serialized coordinator acceptance. This checkpoint does not read transient live registries, infer current acceptance status or grant source credit.',
                          'All37 residual functions remain reserved; full native extent hashes are pinned. Draft file names/history and compilation measurements do not establish byte-exact or behavioral completion.',
                          'Bounded probes preserved type/interface findings without allocation sweeps, executable patches, ordinary-logic ASM or shared pipeline changes. No game/hardware/platform/source-only ROM execution is established.',
                          'The formerly unused-R0 encounter hypothesis is rejected by independently inspected callee key comparison. Physical six-word stat-provider caller ABI is measured, while original callee formal source declarations remain unproven.'])
    write_json(LANE / 'residual-checkpoint.json', output)
    print(dict(status=output['status'], proposedFunctions=20, proposedBytes=2160, remainingFunctions=37, remainingBytes=10180, verifiedStaticInputs=len(pins), checkpointSha256=sha256(LANE / 'residual-checkpoint.json')))


if __name__ == '__main__':
    execute()
