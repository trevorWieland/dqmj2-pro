import json
import shutil
import subprocess
import sys
from project import ROOT, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005'
CLONE = ROOT / 'work/w4o5/copy'


def pin(path, role=None):
    row = dict(path=path, sha256=sha256(ROOT / path))
    if role:
        row['role'] = role
    return row


def execute():
    original = pin((LANE / 'ready.json').relative_to(ROOT).as_posix())
    ready = json.loads((LANE / 'ready.json').read_text())
    inputs = json.loads((LANE / 'inputs.json').read_text())
    descriptor = LANE / 'canonical-packet.json'
    canonical = ROOT / 'evidence/matches/parallel-wave20261104-ov005-first.json'
    worker = LANE / 'match.json'
    frozen = [pin((LANE / 'inputs.json').relative_to(ROOT).as_posix())]
    frozen += [{k: p[k] for k in ['path', 'sha256']} for p in inputs['files'] if p['role'] == 'frozen-input']
    document = dict(romSha256=ready['romSha256'], producer=['wave20261104_ov005_proof.py'],
                    workerReport=worker.relative_to(ROOT).as_posix(), canonicalReport=canonical.relative_to(ROOT).as_posix(),
                    frozenInputs=frozen, identities=ready['identities'])
    if descriptor.exists() and json.loads(descriptor.read_text()) != document:
        raise ValueError('Prior immutable descriptor differs')
    write_json(descriptor, document)
    command = [sys.executable, str(ROOT / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()]
    subprocess.run(command, cwd=ROOT, check=True)
    bridge_sources = code_closure(['replay_parallel_packet.py'])
    for name in bridge_sources + [descriptor.relative_to(ROOT).as_posix()]:
        target = CLONE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha256(target) != sha256(ROOT / name):
            raise ValueError('Copied helper/descriptor conflict')
        shutil.copyfile(ROOT / name, target)
    copied_command = [sys.executable, str(CLONE / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()]
    process = subprocess.run(copied_command, cwd=CLONE, capture_output=True, text=True, timeout=180)
    (LANE / 'canonical-copied-root.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError(('Canonical copied replay failed', process.stdout, process.stderr))
    first = json.loads(canonical.read_text())
    second = json.loads((CLONE / canonical.relative_to(ROOT)).read_text())
    if first['generatedTrace']['uncompressedSha256'] != second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Canonical copied fixtures differ')
    for row, copied in zip(first['matches'], second['matches']):
        if row['address'] != copied['address'] or not copied['realLink']['exactCallerBytes'] or row['sourceSha256'] != copied['sourceSha256']:
            raise ValueError('Canonical copied caller contract differs')
    receipt = dict(status='passed', sourceCredit=0, originalReady=original,
                   canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()),
                   originalCommand=command, copiedCommand=copied_command, copiedExitCode=process.returncode,
                   canonicalGeneratorSources=len(first['generatorSources']), functions=len(first['matches']), bytes=first['canonicalMatchedBytes'],
                   originalHelperSourceInputPinsPreserved=True, freshCopiedRootCanonicalReplay=True,
                   traceSha256=first['generatedTrace']['uncompressedSha256'],
                   log=pin((LANE / 'canonical-copied-root.log').relative_to(ROOT).as_posix()))
    write_json(LANE / 'canonical-normalization.json', receipt)
    result = dict(ready)
    result['originalReady'] = original
    result['canonicalDescriptor'] = pin(descriptor.relative_to(ROOT).as_posix())
    result['canonicalReplayCommand'] = ['replay_parallel_packet.py', descriptor.relative_to(ROOT).as_posix()]
    result['packets'] = [dict(report=canonical.relative_to(ROOT).as_posix(), producer=document['producer'])]
    result['files'] = [p for p in ready['files'] if p['path'] != worker.relative_to(ROOT).as_posix()]
    result['files'] += [pin(name, role) for name, role in
                        [(canonical.relative_to(ROOT).as_posix(), 'produced-report'),
                         (descriptor.relative_to(ROOT).as_posix(), 'canonical-descriptor'),
                         ((LANE / 'canonical-normalization.json').relative_to(ROOT).as_posix(), 'diagnostic-proof'),
                         ((LANE / 'canonical-copied-root.log').relative_to(ROOT).as_posix(), 'diagnostic-log'),
                         ('wave20261104_ov005_normalize.py', 'diagnostic-generator')]]
    result['limits'] += ['Coordinator wrapper adds the standard canonical descriptor without modifying the original frozen handoff.']
    write_json(LANE / 'coordinator-ready.json', result)
    if sha256(ROOT / original['path']) != original['sha256']:
        raise ValueError('Original frozen READY changed')
    print(dict(coordinatorReady=pin((LANE / 'coordinator-ready.json').relative_to(ROOT).as_posix()), sourceCredit=0), flush=True)


if __name__ == '__main__':
    execute()
