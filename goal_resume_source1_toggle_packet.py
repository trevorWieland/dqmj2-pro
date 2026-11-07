import shutil
import subprocess
import sys
import uuid
from project import ROOT, sha256, read_json, write_json
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261106/goal-resume-source-1/first-toggle'
PRODUCER = 'goal_resume_source1_toggle_proof.py'
CANONICAL = 'evidence/matches/goal-resume20261106-source1-toggle-first.json'


def pin(name, role=None):
    result = dict(path=name, sha256=sha256(ROOT / name))
    if role:
        result['role'] = role
    return result


def main():
    if (LANE / 'ready.json').exists():
        raise ValueError('READY toggle packet is immutable')
    inputs = read_json(LANE / 'inputs.json')
    subprocess.run([sys.executable, str(ROOT / PRODUCER)], cwd=ROOT, check=True)
    report = read_json(LANE / 'match.json')
    row = report['matches'][0]
    identity = {k: row[k] for k in ('program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256')}
    identity['id'] = report['romSha256'] + '/arm9/main/arm/02072ea0'
    descriptor = LANE / 'canonical-packet.json'
    write_json(descriptor, dict(romSha256=report['romSha256'], producer=[PRODUCER],
        workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=CANONICAL,
        frozenInputs=[pin((LANE / 'inputs.json').relative_to(ROOT).as_posix()), *inputs['mandatoryExternalInputs']], identities=[identity]))
    command = [sys.executable, str(ROOT / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()]
    subprocess.run(command, cwd=ROOT, check=True)
    clone = ROOT / 'work/copied-root-replays' / ('s1t-' + uuid.uuid4().hex[:4])
    if clone.exists():
        raise ValueError('Independent source replay directory already exists')
    paths = {p['path'] for p in inputs['files']}
    paths.update(code_closure(['replay_parallel_packet.py']))
    paths.update([(LANE / 'inputs.json').relative_to(ROOT).as_posix(), descriptor.relative_to(ROOT).as_posix()])
    for name in sorted(paths):
        target = clone / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        if sha256(target) != sha256(ROOT / name):
            raise ValueError('Copied immutable source/input hash differs')
    copied_command = [sys.executable, str(clone / 'replay_parallel_packet.py'), descriptor.relative_to(ROOT).as_posix()]
    process = subprocess.run(copied_command, cwd=clone, capture_output=True, text=True, timeout=240)
    (LANE / 'copied-root.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError('Independent copied-root canonical source proof failed')
    first, second = read_json(ROOT / CANONICAL), read_json(clone / CANONICAL)
    if first['generatedTrace']['uncompressedSha256'] != second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Fresh independent caller/model trace differs')
    if len(second['matches']) != 1 or not second['matches'][0]['realLink']['exactCallerBytes'] or second['actualNativeAndSourceCallerReturns'] != 96:
        raise ValueError('Fresh complete source link or actual fixture returns missing')
    copied = dict(status='passed', sourceCredit=0, copiedRoot=clone.relative_to(ROOT).as_posix(),
        command=copied_command, processExitCode=0, functions=1, bytes=52, frozenInputFiles=len(paths),
        workProductsCopied=False, originalRepositoryUsedAsRuntimeRoot=False,
        actualNativeAndSourceCallerReturns=96, traceSha256=second['generatedTrace']['uncompressedSha256'],
        originalObjectSha256=first['matches'][0]['objectSha256'], freshObjectSha256=second['matches'][0]['objectSha256'],
        log=pin((LANE / 'copied-root.log').relative_to(ROOT).as_posix()))
    write_json(LANE / 'copied-root.json', copied)
    files = list(inputs['files'])
    files.extend(pin((LANE / name).relative_to(ROOT).as_posix(), role) for name, role in [
        ('inputs.json', 'input-manifest'), ('match.json', 'produced-report'), ('canonical-packet.json', 'canonical-descriptor'),
        ('traces.json.gz', 'produced-trace'), ('binding-controls.json', 'produced-controls'),
        ('prototype-control.json', 'produced-controls'), ('copied-root.json', 'diagnostic-proof'), ('copied-root.log', 'diagnostic-log')])
    files.extend([pin(CANONICAL, 'produced-report'), pin('goal_resume_source1_toggle_packet.py', 'diagnostic-generator')])
    write_json(LANE / 'ready.json', dict(schemaVersion=1, status='ready-for-coordinator-acceptance',
        acceptedBaselineCohort=172, functions=1, bytes=52, sourceCreditPendingIntegrator=52,
        romSha256=report['romSha256'], packets=[dict(report=CANONICAL, producer=[PRODUCER])],
        canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()), identities=[identity], files=files,
        generatorSources=[p for p in inputs['files'] if p['role'] == 'generator'],
        frozenInputManifest=pin((LANE / 'inputs.json').relative_to(ROOT).as_posix()),
        admissionProvenance=pin('evidence/lanes/parallel-wave20261106/goal-resume-source-1/claim.json'),
        limits=report['limits']))
    print(dict(ready=pin((LANE / 'ready.json').relative_to(ROOT).as_posix()), functions=1, bytes=52, copiedRoot=copied['copiedRoot']), flush=True)


if __name__ == '__main__':
    main()
