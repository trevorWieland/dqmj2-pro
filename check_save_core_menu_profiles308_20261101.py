import concurrent.futures
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module

VARIANTS = [
    ('baseline', 'src/mechanics_save/20261030_lane_menu_refresh/native_main_0206eaa0.c'),
    ('latch_u32', 'src/mechanics_save/20261101_lane_latch_word/native_main_0206eaa0.c'),
    ('input_s8', 'nonmatching/save-core/20261101-cursor-callers291/native_main_0206eaa0.c')]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(job):
    (name, source), speed = job
    spec = importlib.util.spec_from_file_location('menu308_' + name + str(speed), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ENTRY, builder.LENGTH, builder.NAME = 0x0206EAA0, 396, 'native_main_0206eaa0'
    builder.SOURCE, builder.WORK = source, 'work/save-core/menu-profile308/' + name + '/' + str(speed)
    if speed:
        builder.FLAGS = [*builder.FLAGS, '-opt', 'speed']
    arm = measured_module('main')[1]
    row, body = builder.build(arm[0x6EAA0:0x6EC2C])
    assert row['compiledBytes'] == (396 if speed else 392)
    assert row['exactByteEqual'] == speed
    assert row['sameOffsetBytes'] == (396 if speed else 282)
    return dict(variant=name, speed=speed, row=row)


def main():
    baseline = (ROOT / VARIANTS[0][1]).read_text()
    assert sha((ROOT / VARIANTS[0][1]).read_bytes()) == '5e06d09e97ac10fbfb4fbe1e5e4ae3a2b3f4d4a302e15592284bde73e063f183'
    assert (ROOT / VARIANTS[1][1]).read_text() == baseline.replace('extern void native_fn_02062358(u32 value);', 'extern u32 native_fn_02062358(u32 value);')
    assert (ROOT / VARIANTS[2][1]).read_text() == baseline.replace('extern u32 native_fn_0206238c(s8 *index,s32 lower,s32 upper);', 'extern s8 native_fn_0206238c(s8 *index,s32 lower,s32 upper);')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, [(variant, speed) for variant in VARIANTS for speed in (False, True)]))
    report = dict(schema=1, rows=rows, sourceCredit=0, newCoverageBytes=0,
        generatorSha256=sha(Path(__file__).read_bytes()),
        correctedClaim='The previous attribution of396-to392 shrinkage to a signed-byte return declaration is retracted. The unchanged baseline also produces392 under space. All three source variants reproduce396 under the accepted speed profile.',
        limits=['These controls isolate compiler-profile effects from declaration changes. They recover no original source/header declaration.',
            'The frozen297 primary remains u32(s8*,s32,s32), preserving the existing selected consumer view and measured full return words. Its byte/link/native semantic gates are unaffected.',
            'The latch-return declaration alternative is an unselected zero-credit candidate. Joint callee and overlay-header proofs remain necessary before migration.'])
    path = ROOT / 'evidence/attempts/menu-profile308-controlled-baseline-20261101.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(profiles=len(rows), exactSpeedProfiles=3, nonmatchingSpaceProfiles=3, sourceCredit=0, reportSha256=sha(path.read_bytes()))))


if __name__ == '__main__':
    main()
