import argparse
import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from contextlib import ExitStack, contextmanager
from pathlib import Path, PurePosixPath
from unittest.mock import patch


sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'project.py').is_file())
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from project import configuration, read_json, sha256
from elftools.elf.elffile import ELFFile
from qualify_arm9_reference_consumer_v2_20261105 import compiler_inputs
from qualify_arm9_reference_packets_v2_20261105 import qualify_report
import qualify_arm9_reference_packets_v2_20261105 as main_packets
from qualify_arm9_thumb_reference_inputs_20261105 import derive as derive_main
import qualify_arm9_overlay_reference_inputs_20261105 as overlay
import link_runtime_unit as linker
import verify_committed_source_inputs_v14_20261105 as main_audit


SOURCE = '217601b0b0c11a5941c7b42d65228f6edf9c0b25'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
MAIN = 'extract/arm9/arm9.bin'
MAIN_SHA = 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
OV = 'extract/arm9_overlays/ov000.bin'
OV_SHA = '783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6'
LEDGER = 'provenance/arm9-reference-only-consumers-20261101.json'
EXPECTED = {0x2072ea0: 52, 0x207483c: 148, 0x20724f4: 116,
            0x2076440: 200, 0x20763cc: 96, 0x2078818: 164, 0x20771d4: 152,
            0x2078cbc: 284, 0x2078b30: 352, 0x2077e98: 536}
CONTRACT = Path(__file__).with_name('ten-consumer-contract-v2.json')
SOURCE1_REPORTS = {f'evidence/matches/cohort175-packet-0{i}.json' for i in (1, 2, 3)}
INVENTORY_DEPS = ('provenance/arm9-reference-only-consumers-20261101.json',
    'provenance/arm9-thumb-reference-only-consumers-20261105.json',
    'provenance/host-arm9-overlay-reference-v1-20261106-contract.json',
    'itcm_reset_source_audit_route_v1_20261106.py', 'qualify_itcm_reset_reference_v1_20261106.py')
DEPENDENCIES = ('project.py', 'project.json', 'tools.lock.json', 'match_runtime.py', 'match_lowlevel.py',
    'elf_units.py', 'link_runtime_unit.py', 'qualify_arm9_reference_consumer_v2_20261105.py',
    'qualify_arm9_reference_packets_v2_20261105.py', 'qualify_explicit_c_frontend_20261102.py',
    'qualify_arm9_overlay_reference_inputs_20261105.py', 'qualify_arm9_thumb_reference_inputs_20261105.py',
    'verify_committed_source_inputs_v14_20261105.py', 'verify_committed_source_inputs_v8_20261101.py',
    'provenance/seed-manifest.json')


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def blob(name, revision='HEAD'):
    return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)


def source_path(name):
    require(isinstance(name, str) and not any(c in name for c in ':\n\r\0'), 'Unsafe compiler input path')
    normal = name.replace('\\', '/')
    parts = PurePosixPath(normal)
    require(not parts.is_absolute() and '..' not in parts.parts and normal.startswith('src/'), 'Compiler input leaves SRC')
    require(parts.suffix in {'.c', '.h'} and normal == parts.as_posix(), 'Noncanonical C/header compiler input')
    path = (ROOT / normal).resolve()
    require(path.is_relative_to(ROOT / 'src'), 'Compiler input escapes SRC')
    return normal, path


def validate_flags(flags):
    require(isinstance(flags, list) and all(isinstance(f, str) for f in flags), 'Malformed production flags')
    require(flags.count('-lang') == 1 and flags.index('-lang') + 1 < len(flags) and flags[flags.index('-lang') + 1] == 'c99', 'Exactly one production C99 language required')
    require(flags.count('-proc') == 1 and flags.index('-proc') + 1 < len(flags) and flags[flags.index('-proc') + 1] == 'arm946e' and '-thumb' not in flags, 'Wrong ARM9 ARM profile')
    for flag in flags:
        low = flag.lower()
        require(not low.startswith(('@', '-include', '-prefix', '-i', '-d', '-u')) or low.startswith(('-inline', '-interworking', '-ipa')), 'Hidden production input or macro override')
        require(flag not in {'-c', '-o'} and not any(s in low for s in ('extract/', 'inputs/', 'asm/', '\\', '.bin', '.nds', '.o', '.inc')), 'File-bearing compiler option')


def producer_view(report, consumer):
    view, aliases = copy.deepcopy(report), []
    allowed = {'generator': 'producer', 'generatorSha256': 'producerSha256'} if consumer['report'] in SOURCE1_REPORTS else {}
    require(consumer['producerMetadataAliases'] == allowed, 'Unapproved producer alias mapping')
    for target, origin in allowed.items():
        require(target not in report and origin in report and isinstance(report[origin], str), 'Missing/ambiguous/conflicting producer metadata')
        expected = consumer[target]
        require(report[origin] == expected, 'Changed original producer metadata')
        view[target] = expected
        aliases.append(dict(target=target, origin=origin, value=expected, metadataOnly=True))
    require(view['generator'] == consumer['generator'] and view['generatorSha256'] == consumer['generatorSha256'], 'Producer identity differs')
    require([k for k in ('generator', 'generatorSha256') if k not in report] == consumer['explicitlyAbsentOriginalTopFields'], 'Original metadata presence changed')
    return view, aliases


def validate_report(raw, consumer):
    require(digest(raw) == consumer['reportSha256'], 'Frozen report changed')
    report = json.loads(raw)
    require(report['romSha256'] == ROM and report.get('allPassed') is True, 'Report ROM/acceptance differs')
    producer_view(report, consumer)
    require(isinstance(report['matches'], list) and len(report['matches']) == 1, 'Missing/extra consumer row')
    row = report['matches'][0]
    require((row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', 'arm'), 'Wrong full caller namespace')
    require(EXPECTED.get(int(row['address'], 0)) == row['bytes'] == row['compiledBytes'], 'Wrong complete caller extent')
    require(row == consumer['row'], 'Frozen source/header/object/compiler row differs')
    require([k for k in ('outputSha256',) if k not in row] == consumer['explicitlyAbsentOriginalRowFields'], 'Original output metadata presence changed')
    require(row.get('outputSha256', row['targetSha256']) == row['targetSha256'], 'Original output hash differs')
    require(row['sourceLanguage'] == 'C' and row['ordinaryCBytes'] == row['bytes'] and row.get('justifiedAssemblyBytes', 0) == 0, 'Incomplete ordinary C extent')
    require(row['exactAfterDeclaredRelocation'] and row['realLink']['exactCallerBytes'] and row['realLink']['linkedCallerSha256'] == row['targetSha256'], 'Original genuine match missing')
    validate_flags(row['compilerFlags'])
    return report, row


def closed_graph(row):
    inputs = compiler_inputs(row)
    raw_pins = [(row['source'], row['sourceSha256']), *[(h['path'], h['sha256']) for h in row['sourceDependencies']]]
    paths, documents, aliases = {}, {}, []
    for name, expected in raw_pins:
        normal, path = source_path(name)
        require(normal not in paths, 'Duplicate physical source/header input')
        require(sha256(path) == expected and path.read_bytes() == blob(normal, SOURCE), 'Committed source/header changed')
        paths[normal] = expected
        documents[normal] = path.read_text(encoding='utf-8')
        aliases.append(dict(original=name, canonical=normal, sha256=expected))
    edges = {}
    for name, text in documents.items():
        require(not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin|\\\r?\n|\?\?|%:', text), 'Ambiguous or executable preprocessing')
        edges[name] = []
        for line in text.splitlines():
            if re.match(r'^\s*#\s*(?:include|include_next|import|embed)\b', line):
                match = re.fullmatch(r'\s*#\s*include\s+"([^"<>]+)"\s*', line)
                require(match is not None, 'Unclosed compiler include')
                target = (PurePosixPath(name).parent / match[1]).as_posix()
                require(target in documents, 'Unpinned quoted header')
                edges[name].append(target)
    reached, active = set(), set()
    def visit(name):
        require(name not in active, 'Cyclic include closure')
        if name in reached:
            return
        active.add(name)
        for child in edges[name]:
            visit(child)
        active.remove(name)
        reached.add(name)
    visit(row['source'])
    require(reached == set(documents), 'Unreachable declared header')
    normalized = copy.deepcopy(inputs)
    normalized['includes'] = [dict(path=source_path(h['path'])[0], sha256=h['sha256']) for h in row['sourceDependencies']]
    return dict(original=inputs, comparison=normalized, rawHeaderAliases=aliases, graph=edges)


def object_contract(path, row):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        require(elf.elfclass == 32 and elf.little_endian and elf['e_machine'] == 'EM_ARM' and elf['e_type'] == 'ET_REL', 'Wrong fresh ELF identity')
        sections = [(i, s) for i, s in enumerate(elf.iter_sections()) if s['sh_flags'] & 2 and s['sh_size']]
        require(len(sections) == 1 and sections[0][1].name == '.text' and sections[0][1]['sh_size'] == row['bytes'], 'Extra/incomplete allocated object storage')
        index, text = sections[0]
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        function = [s for s in symbols if s.name == row['name']]
        require(len(function) == 1 and function[0]['st_info']['type'] == 'STT_FUNC' and function[0]['st_shndx'] == index and function[0]['st_value'] == 0 and function[0]['st_size'] == row['bytes'], 'Wrong ARM function extent')
        allocated = sorted((s.name, s['st_value'], s['st_size'], s['st_info']['type'], s['st_info']['bind']) for s in symbols if s['st_shndx'] == index)
        result = dict(flags=elf['e_flags'], sectionFlags=text['sh_flags'], alignment=text['sh_addralign'], bytes=text['sh_size'], bodySha256=digest(text.data()), symbols=allocated)
    result.update(mapping=overlay.arm_mapping(path, row['name']), relocations=linker.relocation_rows(path, row['name']))
    return result


def load_contract(path=CONTRACT):
    contract = read_json(path)
    return validate_contract(contract)


def validate_inventory(contract, audit, baseline):
    tree = ast.parse(blob('verify_committed_source_inputs_v8_20261101.py', SOURCE))
    legacy = next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'allowed_arm9' for t in n.targets))
    groups = {'legacy-static3': set(legacy),
        'unchanged-main-ledger26': {r['report'] for r in json.loads(blob(LEDGER, SOURCE))['consumers']},
        'existing-thumb-ledger78': {r['report'] for r in json.loads(blob(INVENTORY_DEPS[1], SOURCE))['consumers']},
        'existing174-overlay-route': {p for p in contract['historicalOverlayReferences'] if '/cohort174-' in p},
        'existing-itcm-reset-route': {'evidence/matches/cohort168-parallel-wave20261105-m-itcm-reset-first-0.json'},
        'explicit-new175-ten': {c['report'] for c in contract['consumers']}}
    actual = []
    for batch in baseline:
        if MAIN not in batch['sourceHashes']:
            continue
        labels = [key for key, reports in groups.items() if batch['report'] in reports]
        require(len(labels) == 1 and batch['sourceHashes'][MAIN] == MAIN_SHA, 'Unknown/ambiguous/changed current main consumer')
        actual.append(dict(report=batch['report'], route=labels[0], batchSha256=canonical(batch), nativeReferences={p: h for p, h in batch['sourceHashes'].items() if p.startswith('extract/')}))
    require(len(actual) == 130 and audit['rows'] == actual, 'Incomplete or altered130-consumer inventory')


def validate_contract(contract):
    require(contract.get('schemaVersion') == 1 and contract.get('sourceCredit') == 0 and contract.get('qualificationOnly') is True, 'Wrong contract schema/credit scope')
    require(contract['sourceCommit'] == SOURCE and contract['romSha256'] == ROM and len(contract['consumers']) == 10, 'Wrong contract scope')
    require(contract['consumerCount'] == contract['functionCount'] == 10 and contract['functionBytes'] == 2100 and contract['mainComparisonViewRecords'] == 36, 'Wrong declared qualification counts')
    require([int(c['row']['address'], 0) for c in contract['consumers']] == list(EXPECTED), 'Frozen consumer order changed')
    addresses, reports = set(), set()
    baseline = json.loads(blob('recovery.json', SOURCE))['batches']
    for item in contract['consumers']:
        require(item['report'] not in reports, 'Duplicate consumer report')
        reports.add(item['report'])
        raw = blob(item['report'], SOURCE)
        report, row = validate_report(raw, item)
        require(sha256(ROOT / item['generator']) == item['generatorSha256'] == digest(blob(item['generator'], SOURCE)), 'Frozen original producer changed')
        address = int(row['address'], 0)
        require(address not in addresses, 'Duplicate full function identity')
        addresses.add(address)
        batches = [b for b in baseline if b['report'] == item['report']]
        require(len(batches) == 1 and canonical(batches[0]) == item['batchSha256'], 'Frozen registered batch differs')
        expected_refs = {MAIN: MAIN_SHA} if item['report'] in SOURCE1_REPORTS else {MAIN: MAIN_SHA, OV: OV_SHA}
        require(item['referencePins'] == expected_refs, 'Wrong original comparison references')
        require({p: h for p, h in batches[0]['sourceHashes'].items() if p.startswith('extract/')} == item['referencePins'], 'Extra original input in registered batch')
    require(addresses == set(EXPECTED), 'Incomplete ten-function membership')
    historical = {b['report']: {p: h for p, h in b['sourceHashes'].items() if p.startswith('extract/arm9_overlays/')} for b in baseline if b['report'] not in reports and any(p.startswith('extract/arm9_overlays/') for p in b['sourceHashes'])}
    require(contract['historicalOverlayReferences'] == historical, 'Historical overlay consumer set changed')
    require(contract['legacyLedgerSha256'] == canonical(json.loads(blob(LEDGER, SOURCE))), 'Frozen main ledger differs')
    require({p['path'] for p in contract['dependencies']} == set(DEPENDENCIES) and len(contract['dependencies']) == len(DEPENDENCIES), 'Missing/extra/duplicate dependency pin')
    for pin in contract['dependencies']:
        require(digest(blob(pin['path'], SOURCE)) == pin['sha256'] == sha256(ROOT / pin['path']), 'Pinned dependency changed')
    require({p['path'] for p in contract['inventoryDependencies']} == set(INVENTORY_DEPS) and len(contract['inventoryDependencies']) == len(INVENTORY_DEPS), 'Inventory dependency scope changed')
    for pin in contract['inventoryDependencies']:
        require(digest(blob(pin['path'], SOURCE)) == pin['sha256'] == sha256(ROOT / pin['path']), 'Inventory dependency changed')
    inventory = contract['remainingMainConsumerInventory']
    require(sha256(ROOT / inventory['path']) == inventory['sha256'], 'Remaining-main inventory changed')
    audit = read_json(ROOT / inventory['path'])
    require(audit['sourceCommit'] == SOURCE and audit['totalMainReferencingBatches'] == 130 and not audit['unknownMainConsumers'] and audit['registrySha256'] == inventory['registrySha256'] == digest(blob('recovery.json', SOURCE)), 'Incomplete remaining-main inventory')
    validate_inventory(contract, audit, baseline)
    require(contract['negativeProfile'] == {'consumer': 'evidence/matches/cohort175-packet-06.json', 'replaceSingle': '-O2', 'with': '-O0', 'allOtherInputsUnchanged': True, 'oneCompilerInvocation': True}, 'Unprescribed negative control')
    return contract


def project_batches(actual, contract):
    require(len({b['report'] for b in actual}) == len(actual), 'Duplicate registered report')
    expected = {c['report']: c for c in contract['consumers']}
    require(set(expected) <= {b['report'] for b in actual}, 'Missing selected consumer')
    require([b['report'] for b in actual if b['report'] in expected] == list(expected), 'Selected consumer order changed')
    copies, removed = copy.deepcopy(actual), []
    for batch in copies:
        refs = {p: h for p, h in batch['sourceHashes'].items() if p.startswith('extract/arm9_overlays/')}
        if batch['report'] not in expected:
            require(not refs or refs == contract['historicalOverlayReferences'].get(batch['report']), 'Unknown/changed overlay consumer')
            continue
        consumer = expected[batch['report']]
        comparison = copy.deepcopy(batch)
        omissions = []
        for name in (MAIN,):
            if name not in comparison['sourceHashes']:
                comparison['sourceHashes'][name] = consumer['referencePins'][name]
                omissions.append(name)
        require(canonical(comparison) == consumer['batchSha256'], 'Selected projected batch differs beyond qualified prior main omission')
        expected_refs = {p: h for p, h in consumer['referencePins'].items() if p.startswith('extract/arm9_overlays/')}
        require(refs == expected_refs, 'Missing/extra/changed selected overlay evidence')
        if OV in expected_refs:
            del batch['sourceHashes'][OV]
        removed.append(dict(report=batch['report'], removed=[OV] if OV in expected_refs else [], priorMainOmissionsPreserved=omissions))
    return copies, removed


def comparison_views(contract, qualifications, ledger):
    require(canonical(ledger) == contract['legacyLedgerSha256'] and len(ledger['consumers']) == 26, 'Original26 main consumers changed')
    output, proofs, reports = copy.deepcopy(ledger), {}, {}
    require(set(qualifications) == {c['report'] for c in contract['consumers']}, 'Missing/extra fresh qualification')
    for item in contract['consumers']:
        name, row = item['report'], item['row']
        proof = copy.deepcopy(qualifications[name]['qualification'])
        require(proof['report'] == name and proof['reportSha256'] == item['reportSha256'] and proof['producer'] == item['generator'] and proof['producerSha256'] == item['generatorSha256'], 'Qualification report/producer identity differs')
        require(proof['expectedRanges'] == {row['address']: row['bytes']} and len(proof['proofs']) == 1 and proof['proofs'][0]['address'] == row['address'], 'Qualification full extent differs')
        expected_inputs = dict(originalCodeCompilerInput=False, source=row['source'], sha256=row['sourceSha256'], includes=[dict(path=source_path(h['path'])[0], sha256=h['sha256']) for h in row['sourceDependencies']])
        require(qualifications[name]['closedInputs']['comparison'] == expected_inputs, 'Canonical source-only comparison inputs differ')
        proof['proofs'][0]['sourceOnlyCompilerInput'] = copy.deepcopy(qualifications[name]['closedInputs']['comparison'])
        output['consumers'].append(dict(report=name, producer=item['generator'], producerSha256=item['generatorSha256'], processor='arm9', program='', module='main', mode='arm', expectedRanges={row['address']: row['bytes']}, sourceOnlyCompilerInputQualification='live-ten-consumer-qualification'))
        report, aliases = producer_view(json.loads(blob(name, SOURCE)), item)
        proof['transientProducerMetadataAliases'] = aliases
        require('sourceOnlyCompilerInput' not in report['matches'][0], 'Original report already has comparison annotation')
        report['matches'][0]['sourceOnlyCompilerInput'] = copy.deepcopy(proof['proofs'][0]['sourceOnlyCompilerInput'])
        proofs[name], reports[name] = proof, report
    require(output['consumers'][:26] == ledger['consumers'], 'Original main prefix changed')
    return output, proofs, reports


def live_qualify(contract, directory):
    validate_contract(contract)
    contract_hash = canonical(contract)
    directory = Path(directory).resolve()
    require(directory.is_relative_to(ROOT / 'work') and not directory.exists(), 'Qualification needs a new WORK directory')
    raw_registry = blob('recovery.json')
    require(raw_registry == (ROOT / 'recovery.json').read_bytes(), 'Registry is not exact HEAD')
    require(digest(raw_registry) == contract['remainingMainConsumerInventory']['registrySha256'], 'Current main-consumer inventory epoch changed')
    require(blob(LEDGER) == (ROOT / LEDGER).read_bytes(), 'Original main ledger is not exact HEAD')
    registry = json.loads(raw_registry)['batches']
    snapshot = {ROOT / 'recovery.json': digest(raw_registry), ROOT / LEDGER: sha256(ROOT / LEDGER)}
    for pin in contract['dependencies']:
        snapshot[ROOT / pin['path']] = pin['sha256']
    for pin in contract['inventoryDependencies']:
        snapshot[ROOT / pin['path']] = pin['sha256']
    inventory = contract['remainingMainConsumerInventory']
    snapshot[ROOT / inventory['path']] = inventory['sha256']
    rows = {}
    for item in contract['consumers']:
        selected = [b for b in registry if b['report'] == item['report']]
        require(len(selected) == 1 and canonical(selected[0]) == item['batchSha256'], 'Full committed selected batch differs')
        raw = (ROOT / item['report']).read_bytes()
        require(raw == blob(item['report']), 'Report is not exact HEAD')
        report, row = validate_report(raw, item)
        closed = closed_graph(row)
        original = ROOT / row['object']
        require(sha256(original) == row['objectSha256'], 'Pinned original compiler object differs')
        original_contract = object_contract(original, row)
        rows[item['report']] = dict(row=row, closedInputs=closed, originalContract=original_contract)
        for name in [item['report'], item['generator'], row['object'], row.get('compiler') or row['compilerPath'], row['source'], *[p['path'] for p in row['sourceDependencies']]]:
            path = (ROOT / name).resolve()
            snapshot[path] = sha256(path)
    directory.mkdir(parents=True)
    cfg = configuration()
    require(sha256(cfg['rom']) == ROM, 'Owned ROM differs')
    snapshot[cfg['rom'].resolve()] = ROM
    main = derive_main()
    original_overlay = overlay.derive(cfg['rom'].read_bytes(), (ROOT / OV).read_bytes(), read_json(ROOT / 'provenance/seed-manifest.json'))
    for name in (MAIN, OV):
        snapshot[ROOT / name] = sha256(ROOT / name)
    for name, module in list(sys.modules.items()):
        if name.split('.')[0] in {'elftools', 'ndspy'} and getattr(module, '__file__', None):
            path = Path(module.__file__).resolve()
            require(path.is_relative_to(ROOT / 'deps/native'), 'Native reader imported from an unpinned external package')
            snapshot[path] = sha256(path)
    started = time.time_ns()
    for ordinal, item in enumerate(contract['consumers']):
        require(canonical(contract) == contract_hash, 'Contract mutated during live qualification')
        name, row = item['report'], item['row']
        output = directory / str(ordinal)
        view, aliases = producer_view(json.loads((ROOT / name).read_bytes()), item)
        original_reader = main_packets.read_json
        def read_report(path):
            return copy.deepcopy(view) if Path(path).resolve() == ROOT / name else original_reader(path)
        with patch.object(main_packets, 'read_json', read_report):
            proof = qualify_report(name, {row['address']: row['bytes']}, output / 'c99')
        proof['transientProducerMetadataAliases'] = aliases
        fresh = ROOT / proof['proofs'][0]['explicitC99Qualification']['explicitC99Object']
        require(fresh.stat().st_mtime_ns >= started, 'Stale fresh compiler output')
        require(object_contract(fresh, row) == rows[name]['originalContract'], 'Complete fresh allocated ARM object/relocations differ')
        linked = linker.validate(dict(row, object=fresh.relative_to(ROOT).as_posix(), objectSha256=sha256(fresh)), row['nativeSymbolEntries'], output / 'link')
        offset = int(row['address'], 0) - 0x02000000
        require(digest(main[offset:offset + row['bytes']]) == row['targetSha256'] == linked['linkedCallerSha256'] and linked['exactCallerBytes'], 'Fresh genuine full native caller differs')
        require(all(p['initializedCodeBytes'] == p['nativeCalleeBytesUsed'] == p['calleeSourceCredit'] == 0 for p in linked['bindingOnlyProbes']), 'Original executable body entered binding link')
        rows[name].update(qualification=proof, freshObject=fresh.relative_to(ROOT).as_posix(), freshObjectSha256=sha256(fresh), freshGenuineLink=linked)
        print(json.dumps(dict(qualifiedFunctions=ordinal + 1, completeNativeBytes=sum(c['row']['bytes'] for c in contract['consumers'][:ordinal + 1]), sourceCredit=0)), flush=True)
    negative_consumer = next(c for c in contract['consumers'] if c['report'] == contract['negativeProfile']['consumer'])
    require(negative_consumer['report'] == 'evidence/matches/cohort175-packet-06.json' and contract['negativeProfile']['replaceSingle'] == '-O2' and contract['negativeProfile']['with'] == '-O0', 'Unprescribed negative profile')
    first = negative_consumer['row']
    options = first['compilerFlags'].copy()
    require(options.count('-O2') == 1, 'Prescribed negative profile absent')
    options[options.index('-O2')] = '-O0'
    wrong = directory / 'wrong-O0.o'
    command = [str(ROOT / (first.get('compiler') or first['compilerPath'])), *options, '-c', str(ROOT / first['source']), '-o', str(wrong)]
    result = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, timeout=120)
    (directory / 'wrong-profile.log').write_bytes(result.stdout + result.stderr)
    require(result.returncode == 0 and wrong.is_file(), 'Negative profile did not compile')
    try:
        rejected = object_contract(wrong, first) != rows[negative_consumer['report']]['originalContract']
    except ValueError:
        rejected = True
    require(rejected, 'Prescribed wrong profile unexpectedly passed complete object gate')
    for path in directory.rglob('*'):
        if path.is_file():
            snapshot[path] = sha256(path)
    require(all(sha256(p) == h for p, h in snapshot.items()), 'Live qualification input changed')
    require(canonical(contract) == contract_hash, 'Contract mutated during live qualification')
    return dict(passed=True, proposalOnly=True, productionActivated=False, sourceCredit=0, functions=10, bytes=2100, contractCanonicalSha256=contract_hash, startedTimeNs=started, finishedTimeNs=time.time_ns(), originalRegistryGateUnchanged=True, independentMainSha256=digest(main), independentOverlay=original_overlay, qualifications=rows, wrongProfile=dict(command=command, objectSha256=sha256(wrong), rejectedByCompleteObjectGate=True), inputHashes={p.relative_to(ROOT).as_posix(): h for p, h in snapshot.items()}, helperSha256=sha256(__file__))


@contextmanager
def route(contract, directory):
    contract_hash = canonical(contract)
    proof = live_qualify(contract, directory)
    require(proof['contractCanonicalSha256'] == contract_hash, 'Live contract qualification differs')
    require(sha256(__file__) == proof['helperSha256'], 'Qualification helper changed')
    def ensure():
        require(canonical(contract) == contract_hash, 'Contract mutated during comparison epoch')
        require(all(sha256(ROOT / p) == h for p, h in proof['inputHashes'].items()), 'Live qualification scope changed')
    ledger, qualifications, reports = comparison_views(contract, proof['qualifications'], read_json(ROOT / LEDGER))
    original_project, original_read, original_qualify = overlay.project_batches, main_audit.read_json, main_audit.qualify_report
    events = []
    def projected(actual, report, declared):
        ensure()
        copies, removed = project_batches(actual, contract)
        events.append(removed)
        return original_project(copies, report, declared)
    def read(path):
        resolved = Path(path).resolve()
        if resolved == ROOT / LEDGER:
            return copy.deepcopy(ledger)
        item = next((c for c in contract['consumers'] if ROOT / c['report'] == resolved), None)
        return producer_view(original_read(path), item)[0] if item else original_read(path)
    def qualify(name, expected, directory):
        if name not in qualifications:
            return original_qualify(name, expected, directory)
        ensure()
        item = next(c for c in contract['consumers'] if c['report'] == name)
        require(expected == {item['row']['address']: item['row']['bytes']}, 'Changed main qualification request')
        result = copy.deepcopy(qualifications[name])
        result['liveQualificationReuse'] = dict(requestedDirectory=str(directory), actualFreshOutputUnchanged=True)
        return result
    try:
        with ExitStack() as stack:
            stack.enter_context(patch.object(overlay, 'project_batches', projected))
            stack.enter_context(patch.object(main_audit, 'read_json', read))
            stack.enter_context(patch.object(main_audit, 'qualify_report', qualify))
            yield dict(projectionEvents=events, liveQualification=copy.deepcopy(proof), contractCanonicalSha256=contract_hash, transientMainLedgerOriginalConsumers=26, transientMainLedgerAdditionalConsumers=10, canonicalRegistryAndLedgerUnmodified=True)
    finally:
        ensure()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, default=CONTRACT)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    contract_raw_hash = sha256(args.contract)
    contract = load_contract(args.contract)
    proof = live_qualify(contract, args.output)
    require(sha256(args.contract) == contract_raw_hash, 'Contract file changed during qualification')
    proof['contractSha256'] = contract_raw_hash
    (args.output / 'qualification.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
