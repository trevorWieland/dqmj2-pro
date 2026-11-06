import copy
import subprocess
from project import ROOT, read_json, sha256


MANIFEST = 'provenance/cohort156-parallel-wave20261105-a-source-files.json'
PREFIX = 'work/w5mg/reference/xenoblade-ea25691b2029/libs/PowerPC_EABI_Support/src/'
APPROVED = {
    PREFIX + 'MSL_C/MSL_Common/strtold.c': 'f7a0b7709988b633b336af63ab9b9ba692cb2b83277d87a8ce4d0baba158f999',
    PREFIX + 'MSL_C/MSL_Common/strtoul.c': 'a5485631c8e2c51fafa06f84729fdcaeec1889c35764d4ac4882ac0a432e6eba',
    PREFIX + 'MSL_C/MSL_Common/wprintf.c': 'a995cb69529a44445df00f839b2c6d7a07832a41190a0ed1c0ee8a7a311a2f4b',
    PREFIX + 'MSL_C/MSL_Common_Embedded/Math/Double_precision/e_pow.c': '31dd44cec190caf3fd78c9941b0ebe792fc603738e40123a5073b7be37eaf662'}


def qualify(batches):
    manifest = ROOT / MANIFEST
    assert subprocess.check_output(['git', 'show', 'HEAD:' + MANIFEST], cwd=ROOT) == manifest.read_bytes()
    declared = {r['path']: r['sha256'] for r in read_json(manifest)['privateComparisonInputs']}
    references = {name: [] for name in APPROVED}
    projected = copy.deepcopy(batches)
    for batch in projected:
        selected = set(batch['sourceHashes']) & APPROVED.keys()
        if not selected:
            continue
        report = read_json(ROOT / batch['report'])
        for row in report.get('matches', report.get('functionMatches', [])):
            assert row['source'] not in APPROVED
            assert not any(r['path'] in APPROVED for r in row.get('sourceDependencies', []))
            assert not any(name in str(flag).replace('\\', '/') for name in APPROVED for flag in row.get('compilerFlags', []))
        for name in selected:
            expected = APPROVED[name]
            path = (ROOT / name).resolve()
            assert path.is_relative_to(ROOT / PREFIX) and path.suffix == '.c'
            assert batch['sourceHashes'][name] == declared[name] == expected == sha256(path)
            payload = path.read_bytes()
            assert b'\x00' not in payload and payload.decode('utf-8')
            references[name].append(batch['report'])
            del batch['sourceHashes'][name]
    assert all(references.values())
    proof = [dict(path=name, sha256=digest, role='Pinned external published MSL comparison/source-generation input',
        declaredBy=MANIFEST, declarationSha256=sha256(manifest), referencedBy=references[name],
        actualProductionCompilerSourceOrHeader=False, sourceCredit=0) for name, digest in APPROVED.items()]
    return projected, proof
