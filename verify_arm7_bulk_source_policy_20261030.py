from project import ROOT, read_json, sha256, write_json
import arm7_bulk_source_policy_20261030 as guard


def main():
    fixtures = [
        ('ordinary-500-lines', 'int f(void) { return 1; }\n' + '\n' * 499, '', True),
        ('quoted-comment-markers', 'const char *s = "https://local/*literal*/";', '', True),
        ('missing-return-diagnostic', 'int f(void) { return 0; }', 'Warning: missing bx return', False),
        ('block-comment', 'int f(void) { /* incomplete */ return 0; }', '', False),
        ('line-comment', 'int f(void) { return 0; }\n// unsupported', '', False),
        ('assembly', 'void f(void) { __asm("nop"); }', '', False),
        ('blob', 'INCBIN(payload);', '', False),
        ('line-501', 'int f(void) { return 1; }\n' + '\n' * 500, '', False),
        ('unsupported-operation', 'void f(void) { M2C_UNSUPPORTED(); }', '', False)]
    controls = []
    for name, source, diagnostics, allowed in fixtures:
        result = guard.inspect(source, diagnostics)
        assert result['ordinarySourceCandidate'] == allowed
        try:
            guard.require(source, diagnostics)
        except ValueError:
            assert not allowed
        else:
            assert allowed
        controls.append({'name': name, 'passed': True, 'allowed': allowed, 'result': result})
    archive = read_json(ROOT / 'evidence/verification/arm7-generated-rejection-archive-20261030.json')
    for row in archive['inputs']:
        path = ROOT / row['archivePath']
        assert sha256(path) == row['sha256']
        result = guard.inspect(path.read_text(encoding='utf-8-sig'))
        assert not result['ordinarySourceCandidate'] and result['generatedDiagnosticOrStubSourceCredit'] == 0
        controls.append({'name': row['originalPath'], 'archiveSha256': row['sha256'],
                         'passed': True, 'rejected': True, 'result': result})
    report = {'passed': True, 'controls': controls, 'generatedSourceCredit': 0,
              'generator': 'verify_arm7_bulk_source_policy_20261030.py',
              'generatorSha256': sha256(ROOT / 'verify_arm7_bulk_source_policy_20261030.py'),
              'guardSha256': sha256(ROOT / 'arm7_bulk_source_policy_20261030.py'),
              'archiveSha256': sha256(ROOT / 'evidence/verification/arm7-generated-rejection-archive-20261030.json'),
              'reproductionCommand': 'python verify_arm7_bulk_source_policy_20261030.py',
              'limitations': ['Candidate screening does not prove compilation, behavior, byte equality or decompilation']}
    write_json(ROOT / 'evidence/verification/arm7-bulk-source-policy-replay-20261030.json', report)
    print({'passed': True, 'controls': len(controls), 'sourceCredit': 0})


if __name__ == '__main__':
    main()
