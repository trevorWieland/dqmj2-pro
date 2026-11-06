import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure
import wave20261104_ov005_package as P

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005-second'
CLONE = ROOT / 'work/w4o5b/copy'
PRODUCER = 'wave20261104_ov005_second_proof.py'
ADDRESSES = ('021db6f8', '021db808')


def pin(path, role=None):
    row = dict(path=path, sha256=sha256(ROOT / path))
    if role:
        row['role'] = role
    return row


def prepare():
    P.LANE, P.CLONE, P.PRODUCER, P.ADDRESSES = LANE, CLONE, PRODUCER, ADDRESSES
    P.prepare()


def execute():
    subprocess.run([sys.executable, str(ROOT / PRODUCER)], cwd=ROOT, check=True)
    P.LANE, P.CLONE, P.PRODUCER, P.ADDRESSES = LANE, CLONE, PRODUCER, ADDRESSES
    P.copied_root()
    report = json.loads((LANE / 'match.json').read_text())
    inputs = json.loads((LANE / 'inputs.json').read_text())
    identities = []
    for row in report['matches']:
        item = {key: row[key] for key in ['processor', 'program', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']}
        item['id'] = report['romSha256'] + '/arm9/ov005/arm/' + format(int(row['address'], 0), '08x')
        identities.append(item)
    descriptor = LANE / 'canonical-packet.json'
    canonical = ROOT / 'evidence/matches/parallel-wave20261104-ov005-second.json'
    frozen = [pin((LANE / 'inputs.json').relative_to(ROOT).as_posix())]
    frozen += [{k: p[k] for k in ['path', 'sha256']} for p in inputs['files'] if p['role'] == 'frozen-input']
    write_json(descriptor, dict(romSha256=report['romSha256'], producer=[PRODUCER],
               workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=canonical.relative_to(ROOT).as_posix(),
               frozenInputs=frozen, identities=identities))
    subprocess.run([sys.executable, str(ROOT / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()], cwd=ROOT, check=True)
    for name in code_closure(['replay_parallel_packet.py']) + [descriptor.relative_to(ROOT).as_posix()]:
        target = CLONE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha256(target) != sha256(ROOT / name):
            raise ValueError('Copied canonical source conflict')
        shutil.copyfile(ROOT / name, target)
    command = [sys.executable, str(CLONE / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()]
    process = subprocess.run(command, cwd=CLONE, capture_output=True, text=True, timeout=180)
    (LANE / 'canonical-copied-root.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError(('Copied canonical replay failed', process.stdout, process.stderr))
    original = json.loads(canonical.read_text())
    second = json.loads((CLONE / canonical.relative_to(ROOT)).read_text())
    if original['generatedTrace']['uncompressedSha256'] != second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Copied canonical traces differ')
    for a, b in zip(original['matches'], second['matches']):
        if a['address'] != b['address'] or a['sourceSha256'] != b['sourceSha256'] or not b['realLink']['exactCallerBytes']:
            raise ValueError('Copied canonical caller contract differs')
    write_json(LANE / 'canonical-copied-root.json', dict(status='passed', sourceCredit=0, command=command,
               processExitCode=process.returncode, functions=len(identities), bytes=report['canonicalMatchedBytes'],
               descriptor=pin(descriptor.relative_to(ROOT).as_posix()), independentNativeAndSourceCallerReturns=second['actualNativeAndSourceCallerReturns'],
               traceSha256=second['generatedTrace']['uncompressedSha256'], workProductsCopied=False,
               log=pin((LANE / 'canonical-copied-root.log').relative_to(ROOT).as_posix())))
    files = list(inputs['files'])
    files += [pin(name, role) for name, role in
              [((LANE / 'inputs.json').relative_to(ROOT).as_posix(), 'input-manifest'),
               (canonical.relative_to(ROOT).as_posix(), 'produced-report'),
               (descriptor.relative_to(ROOT).as_posix(), 'canonical-descriptor'),
               ((LANE / 'traces.json.gz').relative_to(ROOT).as_posix(), 'produced-trace'),
               ((LANE / 'copied-root.json').relative_to(ROOT).as_posix(), 'diagnostic-proof'),
               ((LANE / 'canonical-copied-root.json').relative_to(ROOT).as_posix(), 'diagnostic-proof'),
               ((LANE / 'copied-root.log').relative_to(ROOT).as_posix(), 'diagnostic-log'),
               ((LANE / 'canonical-copied-root.log').relative_to(ROOT).as_posix(), 'diagnostic-log'),
               ('evidence/lanes/parallel-wave20261104/ov005/claim.json', 'ownership'),
               (Path(__file__).name, 'diagnostic-generator')]]
    write_json(LANE / 'ready.json', dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=150,
               functions=len(identities), bytes=report['canonicalMatchedBytes'], sourceCreditPendingIntegrator=report['canonicalMatchedBytes'],
               romSha256=report['romSha256'], packets=[dict(report=canonical.relative_to(ROOT).as_posix(), producer=[PRODUCER])],
               canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()), identities=identities, files=files,
               generatorSources=[p for p in inputs['files'] if p['role'] == 'generator'],
               frozenInputManifest=pin((LANE / 'inputs.json').relative_to(ROOT).as_posix()),
               limits=report['limits'] + ['Disjoint second subset of the original fifteen-function claim; first frozen packet remains unchanged.']))
    print(dict(ready=pin((LANE / 'ready.json').relative_to(ROOT).as_posix()), functions=len(identities), bytes=report['canonicalMatchedBytes']), flush=True)


if __name__ == '__main__':
    {'prepare': prepare, 'execute': execute}[sys.argv[1]]()
