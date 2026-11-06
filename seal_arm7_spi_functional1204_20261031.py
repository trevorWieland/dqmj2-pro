import gzip
import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
PROFILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-spi-functional1204-v1/profile.json'
REPORT = ROOT / 'evidence/arm7/lane-spi-functional1204-20261031.json'
FILES = ['arm7_lane_spi_native_20261031.py', 'link_arm7_spi_hypotheses_20261031.py',
    'prove_arm7_spi_functional1204_20261031.py', 'probe_arm7_spi_profiles_20261031.py',
    'probe_arm7_spi_hardware_context_20261031_v2.py', 'seal_arm7_spi_functional1204_20261031.py',
    'nonmatching/arm7-bulk/20261031/lane-spi-functional1204-v1/profile.json',
    'nonmatching/arm7-bulk/20261031/lane-spi-hardware-pointer-context1204-v2/profile.json',
    'evidence/arm7/lane-spi-functional1204-20261031.json',
    'evidence/attempts/arm7-spi-functional1204-before-explicit-runtime-pin-20261031.json',
    'evidence/attempts/arm7-spi-bounded-profile-summary-20261031.json',
    'evidence/verification/arm7-spi-functional1204-replay-receipt-20261031.json',
    'docs/2026-10-31-arm7-child-port-functional1204.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = json.loads(REPORT.read_text())
    if sha(REPORT) != 'fe869a975798f8d9320b4530a8d377cc3ec4fd88d8ddbcf1c9ca64fb16f35162':
        raise ValueError('Frozen functional report changed')
    if report['generatorSha256'] != sha(ROOT / report['generator']) or report['sourceMatchedBytes'] != 0 or report['actualOriginalAndCompiledReturns'] != 816:
        raise ValueError('Complete source-only zero-match scope differs')
    if report['runtimeVersions'] != {'python': '3.13.5', 'unicorn': '2.1.4', 'pyelftools': '0.33'}:
        raise ValueError('Verified runtime pin differs')
    sources = json.loads(PROFILE.read_text())['results']
    for row in sources:
        FILES.extend([row['source'], row['priorHypothesis']])
        for name, expected in ((row['source'], row['sourceSha256']), (row['priorHypothesis'], row['priorHypothesisSha256'])):
            if sha(ROOT / name) != expected:
                raise ValueError('Current or preserved prior C changed')
    macro_profile = ROOT / FILES[7]
    for row in json.loads(macro_profile.read_text())['results']:
        FILES.append(row['source'])
    for row in report['results']:
        trace = ROOT / row['caseTrace']['path']
        data = trace.read_bytes()
        if sha(trace) != row['caseTrace']['sha256'] or hashlib.sha256(gzip.decompress(data)).hexdigest() != row['caseTrace']['rawSha256'] or data[4:8] != bytes(4):
            raise ValueError('Reproducible generated case trace changed')
        native_bytes = row['identity']['bytes'] - 8
        if row['actualOriginalInstructionOffsetsVisited'] != list(range(0, native_bytes, 4)):
            raise ValueError('Whole native entry instruction traversal missing')
    required = {row['path']: row['sha256'] for row in json.loads((ROOT / 'nonmatching/arm7-bulk/20261030/seq-main-final01/generator-pins.json').read_text())['files']}
    required.update({'inputs/game.nds': report['romSha256'], report['inputModule']: report['inputModuleSha256']})
    for row in report['results']:
        link = row['link']
        required[link['compiler']] = link['compilerSha256']
        required[Path(link['linkCommand'][0]).relative_to(ROOT).as_posix()] = link['linkerSha256']
    for name, expected in required.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Existing runtime or tool input changed: ' + name)
    for name in FILES:
        path = ROOT / name
        if name.startswith(('work/', 'inputs/', 'tools/')) or not path.is_file():
            raise ValueError('Unexpected source transport file')
        if path.suffix == '.py':
            text = path.read_text()
            if len(text.splitlines()) > 500 or any(token.type == tokenize.COMMENT for token in tokenize.generate_tokens(io.StringIO(text).readline)):
                raise ValueError('Authored code policy differs')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)),
        'files': [{'path': name, 'sha256': sha(ROOT / name), 'bytes': (ROOT / name).stat().st_size} for name in sorted(set(FILES))],
        'requiredExistingFiles': [{'path': name, 'sha256': value} for name, value in sorted(required.items())],
        'reproduce': ['prove_arm7_spi_functional1204_20261031.py'],
        'draftedAndCompiledHypotheses': 4, 'nativeInitializedBytesExamined': 1204, 'actualOriginalAndCompiledReturns': 816,
        'additionalDeclarationVariants': 4, 'additionalQualifiedImplementationFamilies': 0,
        'matchedNativeBytes': 0, 'acceptedSourceCredit': 0, 'cachedGeneratedProductsTransported': False,
        'sharedRegistryConfigLedgerOrPreferenceEdits': False, 'allPassed': True}
    destination = ROOT / 'provenance/arm7-spi-functional1204-handoff-20261031.json'
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'manifest': destination.relative_to(ROOT).as_posix(), 'sha256': sha(destination),
        'files': len(result['files']), 'existingInputs': len(required), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
