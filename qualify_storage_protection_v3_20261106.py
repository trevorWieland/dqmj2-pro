import ast
import hashlib
import json
from unittest.mock import patch
from project import ROOT, read_json, sha256, write_json
import initialized_storage_protection_v2_20261106 as old
import initialized_storage_protection_v3_20261106 as new


def main():
    original = (ROOT / 'initialized_storage_protection_v2_20261106.py').read_text(encoding='utf-8')
    candidate = (ROOT / 'initialized_storage_protection_v3_20261106.py').read_text(encoding='utf-8')
    assert original.count('cohort16*-*specification.json') == 1
    assert ast.dump(ast.parse(candidate.replace('cohort*-*specification.json', 'cohort16*-*specification.json'))) == ast.dump(ast.parse(original))
    revision = 'fcd3d2bad860d0e83b6de21c8bfb24f7d02f8bb8'
    fixture = ROOT / 'cohort170-storage-protection-fixture-specification.json'
    assert not fixture.exists()
    path_type, real_glob = type(ROOT), type(ROOT).glob

    def fixture_glob(path, pattern, **kwargs):
        found = list(real_glob(path, pattern, **kwargs))
        if path == ROOT and pattern == 'cohort*-*specification.json':
            found.append(fixture)
        return iter(found)

    outcomes = []
    for program, processor, module, expected in [('', 'arm9', 'ov006', True),
            ('other/child.srl', 'arm9', 'ov006', False), ('', 'arm7', 'ov006', False),
            ('', 'arm9', 'ov000', False)]:
        doc = dict(functions=[dict(program=program, processor=processor, module=module,
            address='0x02ffff00', bytes=64)])
        digest = hashlib.sha256(json.dumps(doc, sort_keys=True).encode()).hexdigest()

        def fixture_read(path):
            return doc if path == fixture else read_json(path)

        def fixture_sha(path):
            return digest if path == fixture else sha256(path)

        with patch.object(path_type, 'glob', fixture_glob), patch.object(new, 'read_json', fixture_read), patch.object(new, 'sha256', fixture_sha):
            intervals, pins = new.protected(('', 'arm9', 'ov006'), revision)
        observed = (0x02ffff00, 0x02ffff40) in intervals
        assert observed == expected
        assert any(pin.get('path') == fixture.name and pin['sha256'] == digest for pin in pins)
        outcomes.append(dict(program=program, processor=processor, module=module,
            expectedExcludedFromAdmission=expected, observedExcludedFromAdmission=observed))
    with patch.object(path_type, 'glob', fixture_glob):
        old_intervals, old_pins = old.protected(('', 'arm9', 'ov006'), revision)
    assert (0x02ffff00, 0x02ffff40) not in old_intervals
    assert not any(pin.get('path') == fixture.name for pin in old_pins)
    write_json(ROOT / 'evidence/verification/storage-protection-v3-all-cohort-fixture-qualification-20261106.json',
        dict(passed=True, sourceCredit=0, fixtureWasNeverWritten=True, allOriginalChecksAstRetained=True,
            all170PlusSpecificationNamespaceControls=outcomes, oldNarrowGlobDemonstrablyMisses170Fixture=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in
                ['initialized_storage_protection_v2_20261106.py', 'initialized_storage_protection_v3_20261106.py',
                 'qualify_storage_protection_v3_20261106.py']]))
    print(dict(passed=True, namespaceControls=4, sourceCredit=0))


if __name__ == '__main__':
    main()
