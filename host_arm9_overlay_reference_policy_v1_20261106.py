import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from project import read_json, sha256
from qualify_arm9_reference_packets_v2_20261105 import qualify_report as qualify_main


CONTRACT = 'provenance/host-arm9-overlay-reference-v1-20261106-contract.json'
LEDGER = 'provenance/host-arm9-overlay-reference-v1-20261106-ledger.json'
CONTROLS = 'evidence/verification/host-arm9-overlay-reference-v1-controls-20261106.json'
CONTRACT_SHA = 'ef8fde2b277379aab81f563b7044c32b4fa57bb727f41cc69882288ff52295bf'
MUTABLE = {'recovery.json': 'current-committed-registry', 'manifest.json': 'generated-manifest-live-stable',
    'provenance/arm9-reference-only-consumers-20261101.json': 'append-only-qualified-main-consumers'}
ARCHIVE_ROOT = 'evidence/verification/host-arm9-overlay-reference-v1/'


def require(value, message):
    if not value:
        raise ValueError(message)


def committed_file(name, revision='HEAD'):
    actual = (ROOT / name).read_bytes()
    expected = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
    require(actual == expected, 'Committed qualification input differs: ' + name)
    return hashlib.sha256(actual).hexdigest()


def scope_roles(contract):
    require({pin['path']: pin['policy'] for pin in contract['scopePins'] if pin.get('policy')} == MUTABLE, 'Mutable scope roles differ from exactly the three reviewed paths')


def load_contract():
    require(sha256(ROOT / CONTRACT) == CONTRACT_SHA, 'Reviewed overlay qualification contract changed')
    contract = read_json(ROOT / CONTRACT)
    require(contract['schemaVersion'] == 1 and contract['sourceCredit'] == 0, 'Unexpected overlay qualification schema/credit')
    scope_roles(contract)
    require(len(contract['scopePins']) == 506 and len({pin['path'] for pin in contract['scopePins']}) == 506, 'Historical scope set differs')
    require(len(contract['consumers']) == 14 and sum(len(item['rows']) for item in contract['consumers']) == 39, 'Exact overlay contract membership differs')
    archives = contract['historicalPrototypeArchives']
    require(len(archives) == 3 and all(pin['path'].startswith('work/goal-resume-20261106/overlay-reference-proposal/') for pin in archives), 'Only the three frozen prototype tools may use inert archives')
    for pin in archives:
        require(pin['archivePath'].startswith(ARCHIVE_ROOT) and pin['archivePath'].endswith('.txt'), 'Historical prototype archive is not inert reviewed text')
        source = next(item for item in contract['scopePins'] if item['path'] == pin['path'])
        require(source['sha256'] == pin['sha256'] and source.get('archivePath') == pin['archivePath'], 'Historical path/hash archival mapping differs')
    historical = contract['historicalMainLedger']
    require(hashlib.sha256(historical['rawUtf8'].encode()).hexdigest() == historical['sha256'] and json.loads(historical['rawUtf8']) == historical['document'], 'Historical original26 ledger snapshot/hash differs')
    ledger = read_json(ROOT / LEDGER)
    require(ledger['contract'] == dict(path=CONTRACT, sha256=CONTRACT_SHA) and ledger['sourceCredit'] == 0, 'Separate overlay ledger contract differs')
    expected = [{key: copy.deepcopy(item[key]) for key in ['report', 'reportSha256', 'generator', 'generatorSha256', 'descriptor', 'comparisonInputs', 'rows']} for item in contract['consumers']]
    require(ledger['consumers'] == expected, 'Separate full-namespace overlay ledger membership differs')
    return contract


def validate_main_ledger(contract, directory):
    baseline = contract['historicalMainLedger']
    current = read_json(ROOT / baseline['path'])
    original = baseline['document']
    require({key: value for key, value in current.items() if key != 'consumers'} == {key: value for key, value in original.items() if key != 'consumers'}, 'Legacy main ledger metadata changed')
    require(len(original['consumers']) == 26 and current['consumers'][:26] == original['consumers'], 'An original main-only consumer record changed or moved')
    reports = [item['report'] for item in current['consumers']]
    require(len(set(reports)) == len(reports), 'Duplicate main-only consumer ledger record')
    proofs, files = [], {}
    for ordinal, consumer in enumerate(current['consumers'][26:]):
        require((consumer.get('program') or '', consumer['processor'], consumer['module'], consumer['mode']) == ('', 'arm9', 'main', 'arm'), 'Appended main ledger consumer crosses namespace')
        name = consumer['sourceOnlyCompilerInputQualification']
        require(name.startswith('evidence/verification/cohort') and name.endswith('-arm9-reference-packets-v2-20261105.json'), 'Append lacks the unchanged legacy qualifier receipt')
        receipt = read_json(ROOT / name)
        require(receipt['passed'] is True and receipt['registered'] is True and receipt['generatorSha256'] == sha256(ROOT / 'qualify_arm9_reference_packets_v2_20261105.py'), 'Main append is not registered by the unchanged qualified legacy producer')
        selected = [item for item in receipt['qualification'] if item['report'] == consumer['report']]
        require(len(selected) == 1, 'Main append lacks its unique original qualification')
        prior = selected[0]
        require(prior['reportSha256'] == sha256(ROOT / consumer['report']) and prior['expectedRanges'] == consumer['expectedRanges'], 'Main append receipt/report/extent differs')
        require(prior['producer'] == consumer['producer'] and prior['producerSha256'] == consumer['producerSha256'] == sha256(ROOT / consumer['producer']), 'Main append producer identity differs')
        for path in [name, consumer['report'], consumer['producer']]:
            files[path] = sha256(ROOT / path)
        report = read_json(ROOT / consumer['report'])
        for row in report['matches']:
            for path, digest in [(row['source'], row['sourceSha256']), (row['object'], row['objectSha256']),
                    (row.get('compiler') or row['compilerPath'], row['compilerSha256']),
                    *[(pin['path'], pin['sha256']) for pin in row['sourceDependencies']]]:
                require(sha256(ROOT / path) == digest, 'Appended main qualification input differs: ' + path)
                require(path not in files or files[path] == digest, 'Conflicting appended main input pin')
                files[path] = digest
        fresh = qualify_main(consumer['report'], consumer['expectedRanges'], directory / str(ordinal))
        require(fresh['producerSha256'] == consumer['producerSha256'] and fresh['freshSourceOnlyCompilerBoundaryProven'], 'Appended main consumer did not independently requalify')
        proofs.append(fresh)
    return dict(proofs=proofs, files=files)


def scope_snapshot(contract, directory, committed=False):
    scope_roles(contract)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() if committed else None
    result = {}
    for pin in contract['scopePins']:
        name = pin.get('archivePath', pin['path'])
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT), 'Scope pin escapes repository')
        digest = sha256(path)
        if pin['path'] not in MUTABLE:
            require(digest == pin['sha256'], 'Immutable qualification input changed: ' + pin['path'])
        else:
            require(pin.get('policy') == MUTABLE[pin['path']], 'Mutable path has the wrong narrowly reviewed role')
        if committed and (pin['path'] == 'recovery.json' or pin.get('archivePath')):
            committed_file(name, revision)
        result[name] = digest
    for name in [*contract['productionFiles'], CONTRACT, LEDGER]:
        result[name] = sha256(ROOT / name)
    main = validate_main_ledger(contract, directory)
    for name, digest in main['files'].items():
        require(name not in result or result[name] == digest, 'Appended main scope conflicts with frozen inputs')
        result[name] = digest
    ensure_scope(dict(files=result, revision=revision))
    return dict(files=result, revision=revision, independentlyRequalifiedMainAppends=main['proofs'],
        historicalMutablePins=[pin for pin in contract['scopePins'] if pin['path'] in MUTABLE])


def ensure_scope(snapshot):
    require(snapshot['files'] == {name: sha256(ROOT / name) for name in snapshot['files']}, 'Qualification live scope changed')
    if snapshot.get('revision'):
        require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == snapshot['revision'], 'Committed qualification revision changed during live proof')


def verify_committed_promotion(contract):
    names = [*contract['productionFiles'], CONTRACT, LEDGER, CONTROLS, *[pin['archivePath'] for pin in contract['historicalPrototypeArchives']]]
    require(len(names) == len(set(names)), 'Duplicate committed promotion input')
    for name in names:
        committed_file(name)
    control = read_json(ROOT / CONTROLS)
    require(control['passed'] is True and control['globalCommittedGatesRun'] is False, 'Focused qualification control receipt absent or misclassified')
    require(control['contract'] == dict(path=CONTRACT, sha256=CONTRACT_SHA), 'Control receipt uses a different contract')
    require(control['testsPassed'] >= 14 and control['freshNativeOverlayFunctions'] == 39, 'Required focused controls/fresh overlay proof incomplete')
    required = set(names) - {CONTROLS}
    require({pin['path'] for pin in control['files']} == required, 'Control receipt implementation/contract/archive file set differs')
    for pin in control['files']:
        require(sha256(ROOT / pin['path']) == pin['sha256'], 'Qualified promotion code/data changed: ' + pin['path'])
    return control
