"""Prove ``ops/disasm_capstone.py`` renders the same stream as the pinned objdump.

A replay that has the module images and ``manifest.json`` but not the
``tools/android-ndk`` archive cannot regenerate any lane, because
``ops/transcribe_chunk.py`` decodes with the pinned ``llvm-objdump``.  The
capstone renderer is the documented fallback, and this is its acceptance test: it
regenerates **every committed ov006 sweep-1 and sweep-2 row** through the fallback
and re-verifies those rows against the lanes' own pinned fixtures, which pin the
relocation table, every ``R_ARM_ABS32`` image word and the negative control's
differing offsets.

Nothing about the check depends on the fallback's text matching LLVM's: a row that
renders a different spelling but assembles to the same measured extent passes, which
is the definition of a faithful transcription.  The regeneration is
deterministic, so the scratch lane is rebuilt from scratch on every run and removed
with the scratch rule fragment.

    python ops/verify_capstone_parity.py            # 247 rows, expect 0 failures
    python ops/verify_capstone_parity.py --keep     # keep the scratch lane
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import disasm_capstone  # noqa: E402

SCRATCH = ROOT / 'work/capstone-parity'
FRAGMENT = ROOT / 'config/rules.d/zz-capstone-parity.json'
LANES = (
    ('g1', 'gen_ov006_sweep1', 'ops/ov006_sweep1_plan.json', 'asm',
     ('ops/ov006_sweep1_arm_expectations.json', 'ops/ov006_sweep1_thumb_expectations.json')),
    ('g2', 'gen_ov006_sweep2', 'ops/ov006_sweep2_plan.json', 'asmSingleton+asmDuplicatePool',
     ('ops/ov006_sweep2_arm_expectations.json', 'ops/ov006_sweep2_thumb_expectations.json')),
)
PROFILES = {'ov006': ('p003', 'p033'), 'ov006_thumb': ('p033', 'p033')}
SHA = '89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca'


def fragment_entries():
    entries = []
    for label, _module, _plan, _key, _fixtures in LANES:
        for directory, (flags, mode) in PROFILES.items():
            entry = {'glob': 'work/capstone-parity/%s/%s/**' % (label, directory),
                     'module': 'ov006', 'compilerFlags': flags,
                     'compilerSha256': SHA}
            if mode == 'thumb':
                entry['mode'] = 'thumb'
            entries.append(entry)
    return entries


def regenerate():
    """Write the committed lanes again through the fallback renderer."""
    disasm_capstone.install()
    written = 0
    for label, name, plan_path, key, _fixtures in LANES:
        generator = __import__(name)
        plan = json.loads((ROOT / plan_path).read_text())
        keys = plan[key] if key in plan else plan['asmSingleton'] + plan['asmDuplicatePool']
        for key_value in keys:
            address = int(key_value, 16)
            row = generator.ledger_row('ov006', address)
            text = generator.asm_source(address)
            directory = SCRATCH / label / ('ov006_thumb' if row['mode'] == 'thumb' else 'ov006')
            directory.mkdir(parents=True, exist_ok=True)
            (directory / ('native_ov006_%08x.c' % address)).write_text(text, encoding='ascii')
            written += 1
    print('regenerated %d rows under %s' % (written, SCRATCH.relative_to(ROOT)))
    return written


def merge_fixtures(paths, destination):
    merged = {}
    for path in paths:
        for module, rows in json.loads((ROOT / path).read_text()).items():
            merged.setdefault(module, {}).update(rows)
    destination.write_text(json.dumps(merged, indent=1) + '\n', encoding='utf-8')
    return sum(len(rows) for rows in merged.values())


def verify(label, fixtures):
    destination = SCRATCH / ('%s-fixture.json' % label)
    merged = merge_fixtures(fixtures, destination)
    result = subprocess.run(
        [sys.executable, str(ROOT / 'ops/verify_asm_chunk_scan.py'),
         '--lane', 'work/capstone-parity/%s' % label,
         '--fixture', str(destination)],
        cwd=str(ROOT), capture_output=True, text=True)
    tail = [line for line in result.stdout.splitlines() if line.strip()][-1:]
    print('%-3s %3d pinned rows -> %s' % (label, merged, tail[0] if tail else 'no output'))
    if result.returncode != 0:
        sys.stdout.write(result.stdout[-4000:])
        sys.stderr.write(result.stderr[-2000:])
    return result.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--keep', action='store_true')
    args = parser.parse_args(argv)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    FRAGMENT.write_text(json.dumps(fragment_entries(), indent=1) + '\n', encoding='utf-8')
    try:
        total = regenerate()
        codes = [verify(label, fixtures) for label, _m, _p, _k, fixtures in LANES]
    finally:
        if not args.keep:
            FRAGMENT.unlink(missing_ok=True)
            shutil.rmtree(SCRATCH, ignore_errors=True)
    failures = sum(1 for code in codes if code)
    print('\n%d rows regenerated; %d lane(s) failed' % (total, failures))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
