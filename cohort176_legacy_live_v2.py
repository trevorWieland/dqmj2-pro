import copy
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch
from cohort176_epoch_v1 import require


def ten_live(epoch, contract, directory):
    require(epoch.committed_revision is not None, 'Fresh ten qualification requires committed epoch')
    import qualify_ten_consumers_v2 as legacy
    from qualify_ten_consumers_v2 import ROOT, canonical, blob, digest, LEDGER, sha256, SOURCE, source_path, read_json, validate_report, closed_graph, object_contract, configuration, ROM, derive_main, overlay, OV, MAIN, main_packets, qualify_report, linker
    epoch.ensure()
    require(legacy.load_contract() == contract, 'Original ten contract validators differ')
    legacy.validate_contract(contract)
    contract_hash = canonical(contract)
    directory = Path(directory).resolve()
    require(directory.is_relative_to(ROOT / 'work') and not directory.exists(), 'Qualification needs a new WORK directory')
    raw_registry = blob('recovery.json')
    require(raw_registry == (ROOT / 'recovery.json').read_bytes(), 'Registry is not exact HEAD')
    epoch.check_canonical(json.loads(raw_registry)['batches'])
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
        view, aliases = legacy.producer_view(json.loads((ROOT / name).read_bytes()), item)
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
    epoch.ensure()
    return dict(epochAdapterSha256=sha256(Path(__file__)), passed=True, proposalOnly=True, productionActivated=False, sourceCredit=0, functions=10, bytes=2100, contractCanonicalSha256=contract_hash, startedTimeNs=started, finishedTimeNs=time.time_ns(), exactDescendantRegistryGate=True, independentMainSha256=digest(main), independentOverlay=original_overlay, qualifications=rows, wrongProfile=dict(command=command, objectSha256=sha256(wrong), rejectedByCompleteObjectGate=True), inputHashes={p.relative_to(ROOT).as_posix(): h for p, h in snapshot.items()}, helperSha256=sha256(legacy.__file__))


def child_live(epoch, contract, directory):
    require(epoch.committed_revision is not None, 'Fresh child qualification requires committed epoch')
    import qualify_child_snd_reference_v1_20261107 as legacy
    from qualify_child_snd_reference_v1_20261107 import ROOT, sha, read, local, ROM_SHA, REPORT, REPORT_SHA, validate, compiler_inputs, REFS, object_contract, child_link, resumed_positive, derive_originals, ensure, canonical, committed
    epoch.ensure()
    contract_path, resume_positive = legacy.CONTRACT, None
    import link_runtime_unit as linker
    from project import configuration
    require(sha(legacy.__file__) == contract['helperSha256'], 'Wrong helper')
    require(read(contract_path) == contract and Path(contract_path).resolve().is_relative_to(ROOT), 'Wrong contract file')
    raw_registry, raw_report = committed('recovery.json'), committed(REPORT)
    epoch.check_canonical(json.loads(raw_registry)['batches'])
    require(hashlib.sha256(raw_report).hexdigest() == REPORT_SHA, 'Wrong committed report scope')
    registry, report = json.loads(raw_registry)['batches'], json.loads(raw_report)
    row = validate(contract, registry, report)
    inputs = compiler_inputs(row)
    names = ['recovery.json', REPORT, row['source'], row['object'], row['compiler'], contract['producer'], *REFS, *[h['path'] for h in row['sourceDependencies']], *contract['dependencies']]
    snapshot = {name: sha(local(name)) for name in names}
    require(snapshot[row['object']] == row['objectSha256'] and snapshot[row['compiler']] == row['compilerSha256'], 'Wrong original object or compiler')
    for name, expected in contract['dependencies'].items():
        require(snapshot[name] == expected, 'Pinned qualification dependency changed')
    snapshot[Path(legacy.__file__).relative_to(ROOT).as_posix()] = sha(legacy.__file__)
    snapshot[Path(contract_path).resolve().relative_to(ROOT).as_posix()] = sha(contract_path)
    cfg = configuration()
    originals, image = derive_originals(cfg['rom'])
    snapshot[cfg['rom'].resolve().relative_to(ROOT).as_posix()] = ROM_SHA
    for name, module in list(sys.modules.items()):
        if name.split('.')[0] in {'elftools', 'ndspy', 'capstone'} and getattr(module, '__file__', None):
            path = Path(module.__file__).resolve()
            require(path.is_relative_to(ROOT / 'deps/native'), 'External native reader fallback')
            snapshot[path.relative_to(ROOT).as_posix()] = sha(path)
    output = Path(directory).resolve()
    require(output.is_relative_to(ROOT / 'work') and not output.exists(), 'Fresh WORK output required')
    output.mkdir(parents=True)
    reference = object_contract(local(row['object']), row)
    started = time.time_ns()
    def compile_one(flags, path):
        command = [str(local(row['compiler'])), *flags, '-c', str(local(row['source'])), '-o', str(path)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=120, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        path.with_suffix('.log').write_bytes(result.stdout + result.stderr)
        require(result.returncode == 0 and path.is_file() and path.stat().st_mtime_ns >= started, 'Fresh compiler failed or stale object')
        return dict(command=command, object=path.relative_to(ROOT).as_posix(), objectSha256=sha(path), exitCode=result.returncode)
    positive = resumed_positive(resume_positive, row) if resume_positive else compile_one(row['compilerFlags'], output / 'explicit-c99.o')
    actual = object_contract(local(positive['object']), row)
    require(actual == reference, 'Complete fresh allocated symbol or relocation contract differs')
    if resume_positive:
        snapshot[Path(resume_positive).resolve().relative_to(ROOT).as_posix()] = sha(resume_positive)
        snapshot[positive['object']] = positive['objectSha256']
        first_freeze = local(read(resume_positive)['freeze']['path'])
        snapshot[first_freeze.relative_to(ROOT).as_posix()] = sha(first_freeze)
        snapshot.update({pin['path']: pin['sha256'] for pin in read(first_freeze)['pins']})
    link = child_link(dict(row, object=positive['object'], objectSha256=positive['objectSha256']), output / 'link')
    target = image[0x6eb8:0x6eb8 + 196]
    require(link['exactCallerBytes'] and link['linkedCallerSha256'] == hashlib.sha256(target).hexdigest() == row['targetSha256'], 'Genuine fresh child native bytes differ')
    negative_flags = row['compilerFlags'].copy()
    require(negative_flags.count('-O4,p') == 1 and negative_flags.index('-O4,p') > negative_flags.index('-O2'), 'Prescribed final optimization goal absent')
    negative_flags[negative_flags.index('-O4,p')] = '-O0'
    negative = compile_one(negative_flags, output / 'wrong-final-O0.o')
    from elftools.elf.elffile import ELFFile
    with (output / 'wrong-final-O0.o').open('rb') as stream:
        elf = ELFFile(stream)
        negative_geometry = dict(allocated=[dict(name=s.name, type=s['sh_type'], bytes=s['sh_size'], flags=s['sh_flags']) for s in elf.iter_sections() if s['sh_flags'] & 2 and s['sh_size']], functions=[dict(name=s.name, bytes=s['st_size'], value=s['st_value']) for s in elf.get_section_by_name('.symtab').iter_symbols() if s['st_info']['type'] == 'STT_FUNC' and s['st_info']['bind'] == 'STB_GLOBAL' and s['st_shndx'] != 'SHN_UNDEF'])
    try:
        wrong_contract = object_contract(output / 'wrong-final-O0.o', row)
    except ValueError as error:
        wrong_contract = dict(rejectedCompleteGeometry=type(error).__name__, reason=str(error))
    require(wrong_contract != reference, 'Prescribed wrong effective profile passed complete object gate')
    proof = dict(passed=True, sourceCredit=0, functions=1, bytes=196, report=REPORT, reportSha256=REPORT_SHA,
        contractCanonicalSha256=canonical(contract), helperSha256=sha(legacy.__file__), sourceOnlyCompilerInput=inputs,
        originals=originals, originalObjectContract=reference, freshObjectContract=actual, positiveCompilation=positive,
        freshGenuineLink=link, negativeCompilation=negative, negativeObjectContract=wrong_contract,
        negativeObservedGeometry=negative_geometry,
        positiveCompilerInvocationsThisInvocation=0 if resume_positive else 1, negativeCompilerInvocations=1, mwLinkerInvocations=1,
        prescribedFinalO4pToO0Rejected=True, startedTimeNs=started, finishedTimeNs=time.time_ns(),
        exactDescendantRegistryGate=True, canonicalRegistryReportsSourcesObjectsAndProfilesUnmodified=True,
        noOriginalCalleeCredit=True, nativeOrCandidateBehaviorExecuted=False)
    for path in output.rglob('*'):
        if path.is_file():
            snapshot[path.relative_to(ROOT).as_posix()] = sha(path)
    epoch.ensure()
    proof['epochAdapterSha256'] = sha(Path(__file__))
    proof['inputHashes'] = snapshot
    ensure(proof, contract)
    (output / 'qualification.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    return proof


@contextmanager
def installed(epoch, ten_module, child_module):
    original_ten, original_child = ten_module.live_qualify, child_module.qualify
    def ten(contract, directory):
        return ten_live(epoch, contract, directory)
    def child(contract, directory, contract_path=None, resume_positive=None):
        require(contract_path is None and resume_positive is None, 'Old resumption is forbidden in a new epoch')
        return child_live(epoch, contract, directory)
    ten_module.live_qualify, child_module.qualify = ten, child
    try:
        yield
    finally:
        unchanged = ten_module.live_qualify is ten and child_module.qualify is child
        ten_module.live_qualify, child_module.qualify = original_ten, original_child
        require(unchanged, 'Legacy live qualifier binding changed unexpectedly')
        epoch.ensure()
