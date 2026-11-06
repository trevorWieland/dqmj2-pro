from pathlib import Path
import argparse
import sys
sys.dont_write_bytecode = True
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', default='initial')
    phase = parser.parse_args().phase
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/host-arm7-seventh'
    ready = read_json(lane / 'ready.json')
    descriptor = read_json(lane / 'canonical-packet.json')
    produced = descriptor['workerReport']
    assert produced == (lane / 'packet-ready.json').relative_to(ROOT).as_posix()
    assert produced not in {pin['path'] for pin in descriptor['frozenInputs']}
    canonical = read_json(ROOT / descriptor['canonicalReport'])
    report = read_json(ROOT / produced)
    assert canonical['canonicalReportRefreshedFromFreshWorkerObjects'] and canonical['matches'] == report['matches']
    previous = next(pin['sha256'] for pin in ready['files'] if pin['path'] == produced)
    base = ROOT / 'audit_host_arm7_sixth_eligibility_parallel_wave20261102.py'
    expected = '9d5f8f8cb1602a0303ee9fa39e37e0cc14bbe0455a6df18376be0faed3321f18'
    assert sha256(base) == expected
    text = base.read_text().replace('host-arm7-sixth', 'host-arm7-seventh')
    text = text.replace('== 35', '== 13').replace('functions=35', 'functions=13').replace('8400', '3836')
    text = text.replace('sealed35/', 'sealed13/').replace("== 'arm7-main'", "== 'arm7-wram'")
    text = text.replace('== 44 and controls', '== 52 and controls').replace("['wrongLinkedMatchingBytes'] == 43", "['wrongLinkedMatchingBytes'] == 51").replace('== 265', '== 47')
    text = text.replace('Both parentSize+4 to parentSize+5 mutations', 'BBP poll bit0 to bit1 mutation')
    old = "pins = {row['path']: row['sha256'] for row in ready['files']}"
    new = "pins = {row['path']: row['sha256'] for row in ready['files'] if row['path'] != " + repr(produced) + "}"
    call = "    exec(compile(text, str(base), 'exec'), dict(__name__='__main__', __file__=str(base)))"
    assert call in text
    text = text.replace(call, '    text = text.replace(' + repr(old) + ', ' + repr(new) + ')\n' + call)
    text = text.replace('host-arm7-seventh-eligibility-initial.json', 'host-arm7-seventh-eligibility-' + phase + '.json')
    exec(compile(text, str(base), 'exec'), dict(__name__='__main__', __file__=str(base)))
    output = ROOT / ('evidence/verification/parallel-wave20261102/host-arm7-seventh-eligibility-' + phase + '.json')
    result = read_json(output)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        frozenUpstreamBaseAuditorSha256=result['frozenBaseAuditorSha256'], frozenBaseAuditorSha256=expected,
        producedReportFreshlyRegenerated=previous != sha256(ROOT / produced),
        historicalProducedReportPin=dict(path=produced, sha256=previous), actualProducedReportSha256=sha256(ROOT / produced),
        canonicalReportSha256=sha256(ROOT / descriptor['canonicalReport']),
        producedClassificationBasis='Declared descriptor.workerReport; absent from frozenInputs; fresh canonical matches and every actual source/compiler/native/link contract independently verified',
        originalReadyFilePins=len(ready['files']))
    write_json(output, result)
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
