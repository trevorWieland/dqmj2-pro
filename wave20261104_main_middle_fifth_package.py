import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure
from wave20261104_main_middle_fifth_models import SPECS as GAME_CALLS
import wave20261104_ov005_package as copy_template

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/fifth'
CLONE = ROOT / 'work/w4mm/fifth-copy'
PRODUCER = 'wave20261104_main_middle_fifth_proof.py'
SOURCE = 'src/runtime/parallel_wave20261104/main-command-middle/eighth/'


def pin(name, role=None):
    row = dict(path=name, sha256=sha256(ROOT / name))
    if role:
        row['role'] = role
    return row


def prepare():
    path = LANE / 'inputs.json'
    if (LANE / 'ready.json').exists():
        raise ValueError('READY packet is frozen')
    claim = json.loads((LANE.parent / 'claim.json').read_text())
    selected = {name for name in GAME_CALLS}
    rows = [dict(row, source=SOURCE + format(int(row['address'], 0), '08x') + '.c',
                 sourceSha256=sha256(ROOT / (SOURCE + format(int(row['address'], 0), '08x') + '.c')))
            for row in claim['claimedFunctions'] if format(int(row['address'], 0), '08x') in selected]
    if len(rows) != len(selected):
        raise ValueError('Proposed family differs from exact ownership')
    names = set(code_closure([PRODUCER])) | {row['source'] for row in rows} | {SOURCE + 'context.h'}
    mandatory = ['project.json', 'provenance/seed-manifest.json', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt',
                 'config/arm9/overlays/ov000/symbols.txt',
                 'evidence/lanes/parallel-wave20261104/main-command-middle/fifth/data-inputs.json']
    names.update(mandatory)
    names.update(['extract/arm9/arm9.bin', 'extract/arm9_overlays/ov000.bin', 'tools/mwccarm/mwccarm/license.dat'])
    for profile, executable in [('2.0/base', 'mwldarm.exe'), ('2.0/sp1p5', 'mwccarm.exe')]:
        names.update('tools/mwccarm/mwccarm/' + profile + '/' + name for name in
                     [executable, 'ELFIO.dll', 'lmgr8c.dll', 'MSL_All-DLL80_x86.dll'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'deps/native').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    files = [pin(name, 'source' if name.startswith(SOURCE) else 'generator' if name.endswith('.py') and not name.startswith('deps/')
                 else 'private-runtime' if name.startswith(('tools/', 'deps/', 'extract/')) else 'frozen-input') for name in sorted(names)]
    write_json(path, dict(schemaVersion=1, romSha256=claim['claimedFunctions'][0]['id'].split('/')[0], entries=rows,
               files=files, mandatoryExternalInputs=[pin(name) for name in mandatory],
               limits=['Private measured native images, compiler/linker, DLL and Python support inputs are local runtime provenance only; zero source credit.']))
    print(dict(frozenFiles=len(files), functions=len(rows), bytes=sum(row['bytes'] for row in rows)), flush=True)


def execute():
    subprocess.run([sys.executable, str(ROOT / PRODUCER)], cwd=ROOT, check=True)
    copy_template.LANE, copy_template.CLONE, copy_template.PRODUCER = LANE, CLONE, PRODUCER
    copy_template.copied_root()
    report = json.loads((LANE / 'match.json').read_text())
    inputs = json.loads((LANE / 'inputs.json').read_text())
    identities = []
    for row in report['matches']:
        item = {key: row[key] for key in ['processor', 'program', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']}
        item['id'] = report['romSha256'] + '/arm9/main/arm/' + format(int(row['address'], 0), '08x')
        identities.append(item)
    descriptor = LANE / 'canonical-packet.json'
    canonical = ROOT / 'evidence/matches/parallel-wave20261104-main-command-middle-fifth.json'
    frozen = [pin((LANE / 'inputs.json').relative_to(ROOT).as_posix())] + inputs['mandatoryExternalInputs']
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
    process = subprocess.run(command, cwd=CLONE, capture_output=True, text=True, timeout=240)
    (LANE / 'canonical-copied-root.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError(('Copied canonical replay failed', process.stdout, process.stderr))
    original = json.loads(canonical.read_text())
    second = json.loads((CLONE / canonical.relative_to(ROOT)).read_text())
    if original['generatedTrace']['uncompressedSha256'] != second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Copied canonical fixture traces differ')
    for a, b in zip(original['matches'], second['matches']):
        if a['address'] != b['address'] or a['sourceSha256'] != b['sourceSha256'] or not b['realLink']['exactCallerBytes']:
            raise ValueError('Copied canonical caller identity differs')
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
               ((LANE / 'binding-layout-controls.json').relative_to(ROOT).as_posix(), 'produced-controls'),
               ((LANE / 'copied-root.json').relative_to(ROOT).as_posix(), 'diagnostic-proof'),
               ((LANE / 'canonical-copied-root.json').relative_to(ROOT).as_posix(), 'diagnostic-proof'),
               ((LANE / 'copied-root.log').relative_to(ROOT).as_posix(), 'diagnostic-log'),
               ((LANE / 'canonical-copied-root.log').relative_to(ROOT).as_posix(), 'diagnostic-log'),
               ((LANE.parent / 'claim.json').relative_to(ROOT).as_posix(), 'ownership'), (Path(__file__).name, 'diagnostic-generator')]]
    write_json(LANE / 'ready.json', dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=151,
               functions=len(identities), bytes=report['canonicalMatchedBytes'], sourceCreditPendingIntegrator=report['canonicalMatchedBytes'],
               romSha256=report['romSha256'], packets=[dict(report=canonical.relative_to(ROOT).as_posix(), producer=[PRODUCER])],
               canonicalDescriptor=pin(descriptor.relative_to(ROOT).as_posix()), identities=identities, files=files,
               generatorSources=[p for p in inputs['files'] if p['role'] == 'generator'],
               frozenInputManifest=pin((LANE / 'inputs.json').relative_to(ROOT).as_posix()),
               limits=report['limits'] + ['Fifth closed2-function family from67-function claim; cumulative19/3160B proposed, remaining48/9316B reserved/uncredited; cohort155or later only.']))
    print(dict(ready=pin((LANE / 'ready.json').relative_to(ROOT).as_posix()), functions=len(identities), bytes=report['canonicalMatchedBytes']), flush=True)


if __name__ == '__main__':
    {'prepare': prepare, 'execute': execute}[sys.argv[1]]()
