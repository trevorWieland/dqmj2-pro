import argparse
import copy
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'project.py').is_file())
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
REPORT = 'evidence/matches/cohort174-parallel-wave20261105-s-child-snd-resume-0.json'
REPORT_SHA = '7c8c51c65a143d975e1ff858f2495ace06aec9ed7c234829cc01fdca7fdfef37'
REGISTRY_SHA = 'f792a31d3bbe574aeced9f6146576999e4d0e28bc5517111ada5b5b8dda82629'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
PROGRAM = 'dwc/utility.bin/move/child.srl'
MODULE = 'utility-child-arm9-main'
REFS = {'extract/files/dwc/utility.bin': 'db8ee36170897f60791f713b7669c50a125e62c6ad775fda98466c85fe48e81e',
    'extract/utility/runtime/utility-child-arm9-main.bin': 'af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0'}
CONTRACT = Path(__file__).with_name('child-snd-reference-contract-v1.json')


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def local(name):
    path = (ROOT / name).resolve()
    require(path.is_relative_to(ROOT) and path.is_file(), 'Missing or escaping qualified input')
    return path


def validate(contract, registry, report):
    require(contract['qualificationOnly'] is True and contract['sourceCredit'] == 0, 'Wrong credit scope')
    require(contract['report'] == REPORT and contract['reportSha256'] == REPORT_SHA and contract['registrySha256'] == REGISTRY_SHA, 'Wrong immutable epoch')
    require(contract['referencePins'] == REFS and report['romSha256'] == ROM_SHA and report['allPassed'] is True, 'Wrong originals or failed report')
    selected = [b for b in registry if b['report'] == REPORT]
    require(len(selected) == 1 and selected[0] == contract['batch'], 'Missing duplicate or changed canonical batch')
    require({p: h for p, h in selected[0]['sourceHashes'].items() if p.startswith('extract/')} == REFS, 'Extra or changed native reference')
    require(report['matches'] == [contract['row']], 'Changed source object profile bindings or extent')
    row = report['matches'][0]
    require((row['program'], row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes'], row['compiledBytes']) == (PROGRAM, 'arm9', MODULE, 'arm', 0x02006eb8, 196, 196), 'Wrong complete physical namespace')
    require(row['targetSha256'] == '8272fbae28d4aa957c44508293701607b6c7a8ee985f9d9f255cf879e70356b8', 'Wrong native body')
    require(len(row['nativeSymbolEntries']) == 8 and row['nativeSymbolEntries'] == contract['bindings'], 'Changed binding set')
    for binding in row['nativeSymbolEntries'].values():
        require((binding['program'], binding['processor'], binding['module'], binding['mode'], binding['kind']) == (PROGRAM, 'arm9', MODULE, 'arm', 'function'), 'Wrong binding namespace')
    flags = row['compilerFlags']
    require(flags.count('-lang') == 1 and flags[flags.index('-lang') + 1] == 'c99' and flags.count('-O4,p') == 1, 'Wrong production frontend or final goal')
    require(report['generator'] == contract['producer'] and report['generatorSha256'] == contract['producerSha256'], 'Wrong original producer')
    return row


def compiler_inputs(row):
    documents = {}
    pins = [(row['source'], row['sourceSha256']), *[(p['path'], p['sha256']) for p in row['sourceDependencies']]]
    for name, expected in pins:
        path = local(name)
        require(path.is_relative_to(ROOT / 'src') and path.suffix in {'.c', '.h'} and sha(path) == expected, 'Wrong C header input')
        require(path not in documents, 'Duplicate source input')
        text = path.read_text(encoding='utf-8')
        require(not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin|\\\r?\n|\?\?|%:', text), 'Executable or ambiguous preprocessing input')
        documents[path] = text
    reached, active = set(), set()
    def visit(path):
        require(path not in active, 'Cyclic include graph')
        if path in reached:
            return
        active.add(path)
        for line in documents[path].splitlines():
            if re.match(r'^\s*#', line):
                match = re.fullmatch(r'\s*#\s*include\s+"([^"<>]+)"\s*', line)
                require(match is not None, 'Unclosed compiler include')
                child = (path.parent / match[1]).resolve()
                require(child in documents, 'Unpinned include')
                visit(child)
        active.remove(path)
        reached.add(path)
    visit(local(row['source']))
    require(reached == set(documents), 'Unreachable header')
    for flag in row['compilerFlags']:
        low = flag.lower()
        require(not low.startswith(('@', '-include', '-prefix', '-i', '-d', '-u')) or low.startswith(('-inline', '-interworking', '-ipa')), 'Hidden compiler input')
        require(not any(x in low for x in ['extract/', 'inputs/', 'asm/', '.bin', '.nds', '.o', '.inc', '\\']), 'File bearing compiler flag')
    return dict(originalCodeCompilerInput=False, source=row['source'], sha256=row['sourceSha256'], includes=copy.deepcopy(row['sourceDependencies']))


def object_contract(path, row):
    from elftools.elf.elffile import ELFFile
    import link_runtime_unit as linker
    with Path(path).open('rb') as stream:
        elf = ELFFile(stream)
        require(elf.elfclass == 32 and elf.little_endian and elf['e_machine'] == 'EM_ARM' and elf['e_type'] == 'ET_REL', 'Wrong fresh ELF')
        allocated = [(i, s) for i, s in enumerate(elf.iter_sections()) if s['sh_flags'] & 2 and s['sh_size']]
        require(len(allocated) == 1 and allocated[0][1].name == '.text' and allocated[0][1]['sh_size'] == 196, 'Extra or wrong complete object extent')
        index, section = allocated[0]
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        function = [s for s in symbols if s.name == row['name']]
        require(len(function) == 1 and function[0]['st_info']['type'] == 'STT_FUNC' and function[0]['st_shndx'] == index and function[0]['st_value'] == 0 and function[0]['st_size'] == 196, 'Wrong source symbol geometry')
        result = dict(flags=elf['e_flags'], sectionFlags=section['sh_flags'], alignment=section['sh_addralign'], bytes=196, bodySha256=hashlib.sha256(section.data()).hexdigest(), symbols=sorted((s.name, s['st_value'], s['st_size'], s['st_info']['type'], s['st_info']['bind']) for s in symbols if s['st_shndx'] == index))
    result['rawRelocations'] = linker.relocation_rows(path, row['name'])
    return result


def committed(name):
    raw = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)
    require(raw == local(name).read_bytes(), 'Canonical committed input changed')
    return raw


def derive_originals(rom_path):
    import utility_runtime
    from ndspy.rom import NintendoDSRom
    raw = Path(rom_path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == ROM_SHA, 'Wrong owned ROM')
    nds = NintendoDSRom(raw)
    file_id = nds.filenames.idOf('dwc/utility.bin')
    fat, fat_bytes = struct.unpack_from('<II', raw, 0x48)
    require(file_id is not None and (file_id + 1) * 8 <= fat_bytes, 'Wrong utility FAT identity')
    begin, end = struct.unpack_from('<II', raw, fat + 8 * file_id)
    archive = raw[begin:end]
    require(archive == nds.files[file_id] == local('extract/files/dwc/utility.bin').read_bytes() and hashlib.sha256(archive).hexdigest() == REFS['extract/files/dwc/utility.bin'], 'ROM FAT archive differs')
    report, products = utility_runtime.derive()
    module = next(m for m in report['modules'] if m['id'] == MODULE)
    image = products[ROOT / module['binary']]
    require((module['program'], module['processor'], module['name'], int(module['base'], 0)) == (PROGRAM, 'arm9', MODULE, 0x02000000), 'Wrong child loader namespace')
    require(module['sha256'] == hashlib.sha256(image).hexdigest() == REFS[module['binary']] and image == local(module['binary']).read_bytes(), 'Child loader image differs')
    return dict(archiveFat=dict(id=file_id, begin=begin, end=end, sha256=REFS['extract/files/dwc/utility.bin']), child=report['child'], processor=report['processors'][0], module=module), image


def ensure(proof, contract):
    require(canonical(contract) == proof['contractCanonicalSha256'], 'Contract changed during qualification epoch')
    require(all(sha(local(p)) == h for p, h in proof['inputHashes'].items()), 'Qualified inputs or fresh proof changed')


def child_link(row, directory):
    from elftools.elf.elffile import ELFFile
    import wave20261102_child_link as legacy
    from wave20261106_child_snd_resume_bindings import qualify as binding_qualification
    canonical_entries, bindings, witnesses = binding_qualification(row)
    require(bindings == row['nativeSymbolEntries'] and len(witnesses) == 8, 'Exact original child BL binding witnesses differ')
    with patch.object(legacy, 'canonical', return_value=canonical_entries):
        proof = legacy.validate(row, directory)
    require(len(proof['bindings']) == 8, 'Child linker binding count differs')
    for binding in proof['bindings']:
        require((binding['program'], binding['processor'], binding['module'], binding['mode'], binding['kind']) == (PROGRAM, 'arm9', MODULE, 'arm', 'function'), 'Child linker changed binding namespace')
        require(binding['initializedCodeBytes'] == binding['nativeCalleeBytesUsed'] == binding['calleeSourceCredit'] == 0, 'Executable binding scaffold credit')
        with local(binding['anchorObject']).open('rb') as stream:
            elf = ELFFile(stream)
            symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == binding['name'])
            require(symbol['st_size'] == 0 and elf.get_section(symbol['st_shndx'])['sh_type'] == 'SHT_NOBITS', 'Binding object acquired initialized code')
    proof['originalNativeBLAndEntryWitnesses'] = witnesses
    return proof


def resumed_positive(path, row):
    require(sha(path) == 'edf7bc28cfce25478e0cbba0137f69b1f34770618b59c17d39ad4e85ac40b78b', 'Only the exact coordinator-admitted first attempt may resume')
    receipt = read(path)
    freeze = local(receipt['freeze']['path'])
    require(sha(freeze) == receipt['freeze']['sha256'] == '1c91ddff2b09f5aadd5ed21847271915eabf253864fd8c6524bc428e9b8034a4', 'First-attempt precompile freeze differs')
    for pin in read(freeze)['pins']:
        require(sha(local(pin['path'])) == pin['sha256'], 'First-attempt input changed')
    object_path = local(receipt['positiveObject']['path'])
    require(sha(object_path) == receipt['positiveObject']['sha256'] == '943ed2746727fe401033c13c2363a5194fc1140e5c625400cc0e33e4af0bed3c', 'First fresh object changed')
    require(object_path.stat().st_mtime_ns == receipt['positiveObject']['modifiedTimeNs'] > freeze.stat().st_mtime_ns == receipt['freeze']['modifiedTimeNs'], 'First-attempt fresh-start time binding differs')
    command = [str(local(row['compiler'])), *row['compilerFlags'], '-c', str(local(row['source'])), '-o', str(object_path)]
    require(command == receipt['positiveArgv'] and canonical(object_contract(object_path, row)) == canonical(receipt['completeFreshObjectContract']), 'First fresh source profile or object differs')
    return dict(command=command, object=object_path.relative_to(ROOT).as_posix(), objectSha256=sha(object_path), exitCode=0,
        reusedOnlyExactAdmittedFreshFirstAttempt=True, freshPositiveCompiledByFirstAttemptNotThisInvocation=True,
        resumptionReceipt=dict(path=Path(path).resolve().relative_to(ROOT).as_posix(), sha256=sha(path)))


def qualify(contract, directory, contract_path=CONTRACT, resume_positive=None):
    import link_runtime_unit as linker
    from project import configuration
    require(sha(__file__) == contract['helperSha256'], 'Wrong helper')
    require(read(contract_path) == contract and Path(contract_path).resolve().is_relative_to(ROOT), 'Wrong contract file')
    raw_registry, raw_report = committed('recovery.json'), committed(REPORT)
    require(hashlib.sha256(raw_registry).hexdigest() == REGISTRY_SHA and hashlib.sha256(raw_report).hexdigest() == REPORT_SHA, 'Wrong committed scope')
    registry, report = json.loads(raw_registry)['batches'], json.loads(raw_report)
    row = validate(contract, registry, report)
    inputs = compiler_inputs(row)
    names = ['recovery.json', REPORT, row['source'], row['object'], row['compiler'], contract['producer'], *REFS, *[h['path'] for h in row['sourceDependencies']], *contract['dependencies']]
    snapshot = {name: sha(local(name)) for name in names}
    require(snapshot[row['object']] == row['objectSha256'] and snapshot[row['compiler']] == row['compilerSha256'], 'Wrong original object or compiler')
    for name, expected in contract['dependencies'].items():
        require(snapshot[name] == expected, 'Pinned qualification dependency changed')
    snapshot[Path(__file__).relative_to(ROOT).as_posix()] = sha(__file__)
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
        contractCanonicalSha256=canonical(contract), helperSha256=sha(__file__), sourceOnlyCompilerInput=inputs,
        originals=originals, originalObjectContract=reference, freshObjectContract=actual, positiveCompilation=positive,
        freshGenuineLink=link, negativeCompilation=negative, negativeObjectContract=wrong_contract,
        negativeObservedGeometry=negative_geometry,
        positiveCompilerInvocationsThisInvocation=0 if resume_positive else 1, negativeCompilerInvocations=1, mwLinkerInvocations=1,
        prescribedFinalO4pToO0Rejected=True, startedTimeNs=started, finishedTimeNs=time.time_ns(),
        originalRegistryGateUnchanged=True, canonicalRegistryReportsSourcesObjectsAndProfilesUnmodified=True,
        noOriginalCalleeCredit=True, nativeOrCandidateBehaviorExecuted=False)
    for path in output.rglob('*'):
        if path.is_file():
            snapshot[path.relative_to(ROOT).as_posix()] = sha(path)
    proof['inputHashes'] = snapshot
    ensure(proof, contract)
    (output / 'qualification.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    return proof


def project_batches(actual, contract):
    selected = [b for b in actual if b['report'] == REPORT]
    require(len(selected) == 1 and selected[0] == contract['batch'], 'Child shadow source batch differs')
    copies = copy.deepcopy(actual)
    row = next(b for b in copies if b['report'] == REPORT)
    for name, expected in REFS.items():
        require(row['sourceHashes'].pop(name) == expected, 'Child comparison hash differs')
    require(all(a == b for a, b in zip(actual, copies) if a['report'] != REPORT), 'Other comparison batch changed')
    return copies, dict(report=REPORT, removed=copy.deepcopy(REFS), sourceCredit=0)


@contextmanager
def route(contract, directory):
    import qualify_arm9_overlay_reference_inputs_20261105 as overlay
    proof = qualify(contract, directory)
    previous = overlay.project_batches
    events = []
    def projected(actual, report, declared):
        ensure(proof, contract)
        copies, prior = previous(actual, report, declared)
        result, event = project_batches(copies, contract)
        events.append(event)
        return result, prior
    try:
        with patch.object(overlay, 'project_batches', projected):
            yield dict(liveQualification=proof, childProjectionEvents=events,
                projectionAfterExistingCanonicalRegistryGate=True, exactTenAndOldNamespaceChecksUnmodified=True)
    finally:
        ensure(proof, contract)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, default=CONTRACT)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--resume-positive', type=Path)
    args = parser.parse_args()
    raw = args.contract.read_bytes()
    result = qualify(json.loads(raw), args.output, args.contract, args.resume_positive)
    require(args.contract.read_bytes() == raw, 'Contract file changed')
    print(json.dumps(dict(passed=result['passed'], functions=1, bytes=196, sourceCredit=0)))


if __name__ == '__main__':
    main()
