import re
from project import ROOT, configuration, now, sha256, write_json
from ledger_state import collect_matches

HELPERS = ('02062a10', '02049ad0', '020853c8')


def main():
    matches, unused = collect_matches(configuration()['romSha256'])
    sources = {}
    for (module, mode, address), unit in matches.items():
        sources.setdefault(unit['source'], []).append({'processor': unit.get('processor', 'arm9'),
            'module': module, 'mode': mode, 'address': hex(address), 'bytes': unit['size']})
    findings = []
    for source, identities in sorted(sources.items()):
        if not source.endswith(('.c', '.cpp')):
            continue
        text = (ROOT / source).read_text(encoding='utf-8-sig')
        masked = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
                        lambda match: ' ' * len(match.group()), text)
        occurrences = []
        for helper in HELPERS:
            for match in re.finditer(r'\bnative_fn_' + helper + r'\s*\(\s*\)', masked):
                prefix = masked[:match.start()]
                line_prefix = prefix[prefix.rfind('\n') + 1:]
                if prefix.count('{') <= prefix.count('}') or re.search(r'\bextern\b', line_prefix):
                    continue
                occurrences.append({'helper': '0x' + helper, 'line': text.count('\n', 0, match.start()) + 1})
        if occurrences:
            findings.append({'source': source, 'sourceSha256': sha256(ROOT / source),
                             'selectedFunctionIdentities': identities, 'emptyArgumentCalls': occurrences})
    report = {'createdUtc': now(), 'generator': __file__, 'generatorSha256': sha256(__file__),
              'sourceRegistrySha256': sha256(ROOT / 'recovery.json'),
              'sourcePreferenceSha256': sha256(ROOT / 'source-preferences.json'),
              'romSha256': configuration()['romSha256'], 'evidenceClass': 'heuristic-source-ABI-audit',
              'scope': 'Currently selected registered C/C++ sources; top-level declarations excluded',
              'sourcesFlagged': len(findings), 'findings': findings, 'sourceCredit': 0,
              'acceptedSourceChanged': False, 'reproductionCommand': 'python audit_empty_native_arguments_20261030.py',
              'limitations': ['No ABI defect is accepted from lexical occurrences alone',
                  'Source function ownership, native input liveness and measured callee contracts need independent review',
                  'Retained historical alternatives are excluded; block-scope declarations and unevaluated calls may remain']}
    write_json(ROOT / 'evidence/attempts/empty-native-argument-audit-20261030.json', report)
    print({'selectedSourcesFlagged': len(findings), 'emptyArgumentCalls': sum(len(r['emptyArgumentCalls']) for r in findings),
           'sourceCredit': 0})


if __name__ == '__main__':
    main()
