import json
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/ov005'
CLONE = ROOT / 'work/w4o5/copy'
PRODUCER = 'wave20261104_ov005_proof.py'
SOURCE = 'src/overlays/parallel_wave20261104/ov005/'
ADDRESSES = ('021d755c', '021d87b4', '021da0bc', '021dbb80')


def pin(path, role):
    return dict(path=path, sha256=sha256(ROOT / path), role=role)


def prepare():
    names = set(code_closure([PRODUCER]))
    names.update(SOURCE + a + '.c' for a in ADDRESSES)
    names.update(['project.json', 'provenance/seed-manifest.json', 'config/arm9/symbols.txt',
                  'config/arm9/overlays/ov005/symbols.txt', 'config/arm9/overlays/ov005/relocs.txt',
                  'extract/arm9/arm9.bin', 'extract/arm9_overlays/ov005.bin'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'deps/native').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    names.update('tools/mwccarm/mwccarm/2.0/base/' + name for name in
                 ['mwccarm.exe', 'mwldarm.exe', 'ELFIO.dll', 'lmgr8c.dll', 'MSL_All-DLL80_x86.dll'])
    names.add('tools/mwccarm/mwccarm/license.dat')
    files = [pin(name, 'source' if name.startswith(SOURCE) else 'generator' if name.endswith('.py') and not name.startswith('deps/')
                 else 'private-runtime' if name.startswith(('tools/', 'deps/', 'extract/')) else 'frozen-input') for name in sorted(names)]
    write_json(LANE / 'inputs.json', dict(schemaVersion=1, files=files,
               mandatoryExternalInputs=[p for p in files if p['role'] == 'frozen-input'],
               limits=['Private executable/dependency/native inputs remain locally supplied and never receive source credit.']))
    print(dict(frozenFiles=len(files)), flush=True)


def copied_root():
    if CLONE.exists():
        raise ValueError('Independent root already exists')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    paths = [p['path'] for p in inputs['files']] + [(LANE / 'inputs.json').relative_to(ROOT).as_posix()]
    for name in paths:
        target = CLONE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        if sha256(target) != sha256(ROOT / name):
            raise ValueError('Copied input changed')
    process = subprocess.run([sys.executable, str(CLONE / PRODUCER)], cwd=ROOT.parent,
                             capture_output=True, text=True, timeout=180)
    (LANE / 'copied-root.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError(('Copied root failed', process.stdout, process.stderr))
    first = json.loads((LANE / 'match.json').read_text())
    second = json.loads((CLONE / LANE.relative_to(ROOT) / 'match.json').read_text())
    if first['generatedTrace']['uncompressedSha256'] != second['generatedTrace']['uncompressedSha256']:
        raise ValueError('Copied fixture traces differ')
    comparisons = []
    for old, new in zip(first['matches'], second['matches']):
        if old['address'] != new['address'] or not new['realLink']['exactCallerBytes'] or old['targetSha256'] != new['targetSha256']:
            raise ValueError('Copied caller identity differs')
        comparisons.append(dict(address=old['address'], bytes=old['bytes'], oldObjectSha256=old['objectSha256'],
                                freshObjectSha256=new['objectSha256'], objectPathChanged=old['object'] != new['object'],
                                objectHashChanged=old['objectSha256'] != new['objectSha256'], genuineCompleteLink=True))
    result = dict(status='passed', sourceCredit=0, copiedRoot=str(CLONE), command=[sys.executable, str(CLONE / PRODUCER)],
                  processExitCode=process.returncode, workProductsCopied=False, originalRepositoryUsedAsRuntimeRoot=False,
                  frozenInputs=len(paths), functions=len(comparisons), bytes=sum(r['bytes'] for r in comparisons),
                  independentFreshObjects=comparisons, fixtureTraceSha256=second['generatedTrace']['uncompressedSha256'],
                  copiedReportSha256=sha256(CLONE / LANE.relative_to(ROOT) / 'match.json'),
                  log=dict(path=(LANE / 'copied-root.log').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'copied-root.log')))
    write_json(LANE / 'copied-root.json', result)
    print(dict(status='copied-root-passed', functions=len(comparisons)), flush=True)


def ready():
    report = json.loads((LANE / 'match.json').read_text())
    inputs = json.loads((LANE / 'inputs.json').read_text())
    copied = json.loads((LANE / 'copied-root.json').read_text())
    if copied['status'] != 'passed' or not report['allPassed']:
        raise ValueError('Packet proof incomplete')
    identities = []
    for row in report['matches']:
        item = {key: row[key] for key in ['processor', 'program', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']}
        item['id'] = report['romSha256'] + '/arm9/ov005/arm/' + format(int(row['address'], 0), '08x')
        identities.append(item)
    files = list(inputs['files'])
    files += [pin((LANE / name).relative_to(ROOT).as_posix(), role) for name, role in
              [('inputs.json', 'input-manifest'), ('match.json', 'produced-report'), ('traces.json.gz', 'produced-trace'),
               ('copied-root.json', 'diagnostic-proof'), ('copied-root.log', 'diagnostic-log'), ('claim.json', 'ownership')]]
    write_json(LANE / 'ready.json', dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=150,
               functions=len(identities), bytes=report['canonicalMatchedBytes'], sourceCreditPendingIntegrator=report['canonicalMatchedBytes'],
               romSha256=report['romSha256'], packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
               identities=identities, files=files, generatorSources=[p for p in inputs['files'] if p['role'] == 'generator'],
               inputManifest=(LANE / 'inputs.json').relative_to(ROOT).as_posix(),
               limits=report['limits'] + ['Only four of fifteen claimed functions are eligible; eleven remain uncredited.']))
    print(dict(readySha256=sha256(LANE / 'ready.json'), functions=len(identities), bytes=report['canonicalMatchedBytes']), flush=True)


if __name__ == '__main__':
    {'prepare': prepare, 'copy': copied_root, 'ready': ready}[sys.argv[1]]()
