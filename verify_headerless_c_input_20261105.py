import copy
from unittest.mock import patch
import qualify_arm9_reference_consumer_v2_20261105 as qualified
from qualify_arm9_reference_packets_v2_20261105 import qualify_report
from project import ROOT, read_json, write_json, sha256, now


def main():
    report = 'evidence/matches/cohort157-parallel-wave20261105-b-main-control-next-first-0.json'
    rows = read_json(ROOT / report)['matches']
    row = next(r for r in rows if r['address'] == '0x207ba64')
    assert row['bytes'] == 60 and row['sourceDependencies'] == []
    before = {name: sha256(ROOT / name) for name in [report, 'recovery.json', 'source-preferences.json', row['source'], row['object']]}
    fixture = ROOT / 'work/integration/headerless-c-input-controls'
    source = fixture / row['source']
    source.parent.mkdir(parents=True, exist_ok=True)
    original = (ROOT / row['source']).read_bytes()
    source.write_bytes(original)
    bad = []
    for field, value in [('processor', 'arm7'), ('program', 'other.srl'), ('module', 'ov000'), ('mode', 'thumb'), ('sourceSha256', '0' * 64), ('sourceDependencies', None), ('source', 'extract/arm9/arm9.bin')]:
        changed = copy.deepcopy(row)
        changed[field] = value
        bad.append((field, changed, original))
    for flag in ['-include', '-prefix', '-Ihidden', '-ihidden', '@hidden.args', '-includehidden.h', 'extract/arm9/arm9.bin', 'hidden.s']:
        changed = copy.deepcopy(row)
        changed['compilerFlags'].append(flag)
        bad.append((flag, changed, original))
    for text in ['#include "hidden.h"\n', '??=include "hidden.h"\n', '\\\n#include "hidden.h"\n', 'asm void f(){}\n', '__asm void f(){}\n', '.incbin "hidden.bin"\n']:
        body = text.encode('utf-8') + original
        changed = copy.deepcopy(row)
        source.write_bytes(body)
        changed['sourceSha256'] = sha256(source)
        bad.append((text.splitlines()[0], changed, body))
    source.write_bytes(original)
    rejected = []
    with patch.object(qualified, 'ROOT', fixture):
        positive = qualified.compiler_inputs(row)
        assert positive['includes'] == [] and positive['originalCodeCompilerInput'] is False
        for label, changed, body in bad:
            source.write_bytes(body)
            try:
                qualified.compiler_inputs(changed)
            except (AssertionError, KeyError):
                rejected.append(label)
            else:
                raise ValueError('Invalid compiler boundary accepted: ' + label)
    source.write_bytes(original)
    expected = {r['address']: r['bytes'] for r in rows}
    proof = qualify_report(report, expected, ROOT / 'work/integration/headerless-c99-independent')
    assert len(proof['proofs']) == 8 and sum(p['bytes'] for p in proof['proofs']) == 856
    assert all(sha256(ROOT / name) == digest for name, digest in before.items())
    write_json(ROOT / 'evidence/verification/headerless-c-input-controls-20261105.json', dict(
        createdUtc=now(), passed=True, sourceCredit=0, positiveHeaderlessFunctionBytes=60,
        freshExplicitC99Functions=8, freshExplicitC99Bytes=856, negativeControls=rejected,
        originalSourceObjectsReportsRegistryAndPreferencesUnchanged=True,
        qualifierSha256=sha256(ROOT / 'qualify_arm9_reference_consumer_v2_20261105.py'),
        originalQualifierSha256=sha256(ROOT / 'qualify_arm9_reference_consumer_20261105.py'), proof=proof))
    print(dict(passed=True, freshExplicitC99Functions=8, negativeControls=len(rejected), sourceCredit=0))


if __name__ == '__main__':
    main()
