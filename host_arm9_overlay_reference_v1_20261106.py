import argparse
import copy
import hashlib
import json
import re
import struct
import sys
import time
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
HERE = ROOT
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from project import configuration, read_json, sha256, write_json
from closed_c_compiler_inputs_20261105 import compiler_inputs as closed_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99, signature
from qualify_arm9_overlay_reference_inputs_20261105 import arm_mapping
from qualify_arm9_thumb_reference_inputs_20261105 import derive as derive_main
import link_runtime_unit as linker
from host_arm9_overlay_reference_policy_v1_20261106 import load_contract, scope_snapshot, ensure_scope, CONTRACT


FIELDS = ('name', 'program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256',
    'sourceDependencies', 'object', 'objectSha256', 'compiler', 'compilerPath', 'compilerSha256', 'compilerFlags',
    'nativeSymbolEntries', 'targetSha256', 'outputSha256', 'ordinaryCBytes', 'sourceLanguage', 'justifiedAssemblyBytes')


def require(value, message):
    if not value:
        raise ValueError(message)


def identity(row):
    return (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0))


def identities(rows):
    result = {identity(row): row for row in rows}
    require(len(result) == len(rows), 'Duplicate complete program/CPU/module/mode/address identity')
    return result


def contract_row(row):
    return {name: row.get(name) for name in FIELDS}


def validate_report(report, contract):
    require(report.get('allPassed') is True and report['romSha256'] == contract['romSha256'], 'Failed report or changed ROM identity')
    require(report['generator'] == contract['generator'] and report['generatorSha256'] == contract['generatorSha256'], 'Producer identity differs')
    actual, expected = identities(report['matches']), identities(contract['rows'])
    require(actual.keys() == expected.keys(), 'Exact frozen namespace identity set differs')
    for key, row in actual.items():
        require(key[:4] in [('', 'arm9', name, 'arm') for name in ('ov000', 'ov003', 'ov006')], 'Unqualified overlay caller namespace')
        require(contract_row(row) == expected[key], 'Frozen source/object/compiler/native contract differs')
        require(row['sourceLanguage'] == 'C' and row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0, 'Complete ordinary C extent required')
        require(row['exactAfterDeclaredRelocation'] and row['realLink']['exactCallerBytes'], 'Full genuine link/match absent')
        require(row['targetSha256'] == row['outputSha256'] == row['realLink']['linkedCallerSha256'], 'Complete linked native hash differs')
    return actual


def validate_texts(documents, source):
    require(source in documents, 'Closed root C text missing')
    edges = {}
    for name, text in documents.items():
        path = PurePosixPath(name)
        require(name == path.as_posix() and name.startswith('src/') and '..' not in path.parts and not any(x in name for x in ('\\', ':', '\n', '\r', '\0')), 'Noncanonical SRC compiler input path')
        require(path.suffix == ('.c' if name == source else '.h'), 'Only one C source and quoted SRC headers are qualified')
        require(not any(token in text for token in ('\\', '??', '%:', '\0')), 'Ambiguous preprocessing or binary text')
        require(not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin', text), 'Executable assembly input is not C-only')
        edges[name] = []
        for line in text.splitlines():
            if '#' not in line:
                continue
            found = re.fullmatch(r'\s*#\s*include\s*"([^"<>]+)"\s*', line)
            require(found is not None, 'Only explicit complete quoted includes are qualified in these frozen rows')
            target = (path.parent / found[1]).as_posix()
            require(target in documents and target != source, 'Compiler include is outside the closed source/header graph')
            edges[name].append(target)
    reached, active = set(), set()
    def visit(name):
        require(name not in active, 'Cyclic quoted include graph')
        if name in reached:
            return
        active.add(name)
        for child in edges[name]:
            visit(child)
        active.remove(name)
        reached.add(name)
    visit(source)
    require(reached == documents.keys(), 'Declared header was not reached by an actual quoted include')
    return edges


def validate_flags(flags):
    require(flags.count('-lang') == 1 and flags[flags.index('-lang') + 1] == 'c99', 'Exactly one explicit production C99 language flag required')
    require(flags.count('-proc') == 1 and flags[flags.index('-proc') + 1] == 'arm946e' and '-thumb' not in flags, 'Actual measured ARM9 ARM profile required')
    for flag in flags:
        lower = str(flag).lower()
        require(not lower.startswith(('@', '-include', '-prefix', '-i', '-d', '-u')) or lower.startswith(('-inline', '-interworking', '-ipa')), 'Implicit compiler input, macro override or response file')
        require(not any(x in lower for x in ('extract/', 'inputs/', 'asm/', '\\', '.bin', '.nds', '.o', '.s', '.inc')), 'Original/binary/assembly compiler input flag')
        require(flag not in ('-c', '-o'), 'Caller cannot replace compiler input/output arguments')


def compiler_inputs(row):
    validate_flags(row['compilerFlags'])
    pins = {row['source']: row['sourceSha256']}
    require(isinstance(row['sourceDependencies'], list), 'Explicit complete source/header pins required')
    for header in row['sourceDependencies']:
        require(header['path'] not in pins, 'Duplicate source/header pin')
        pins[header['path']] = header['sha256']
    documents = {}
    for name, digest in pins.items():
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT / 'src') and sha256(path) == digest, 'Current production C/header bytes differ')
        documents[name] = path.read_text(encoding='utf-8')
    graph = validate_texts(documents, row['source'])
    return dict(closed_inputs(row), namespace=list(identity(row)), reachableQuotedIncludeGraph=graph,
        allActualCompilerInputsAreClosedCAndHeaders=True, actualMode='arm', productionCompilerFlags=row['compilerFlags'])


def derive_references(contracts):
    cfg = configuration()
    require(sha256(cfg['rom']) == contracts['romSha256'], 'Owned original ROM hash differs')
    rom = cfg['rom'].read_bytes()
    main = derive_main()
    values = {'extract/arm9/arm9.bin': main}
    table, table_size = struct.unpack_from('<II', rom, 0x50)
    fat, fat_size = struct.unpack_from('<II', rom, 0x48)
    require(table_size % 32 == 0 and table + table_size <= len(rom) and fat + fat_size <= len(rom), 'Original overlay/FAT bounds differ')
    records = [struct.unpack_from('<8I', rom, at) for at in range(table, table + table_size, 32)]
    require(len({row[0] for row in records}) == len(records), 'Duplicate original overlay namespace')
    seed = read_json(ROOT / 'provenance/seed-manifest.json')
    from ndspy.codeCompression import decompress
    proofs = []
    for name in ('ov000', 'ov003', 'ov006'):
        module = next(row for row in seed['modules'] if row['name'] == name)
        entry = next(row for row in records if row[0] == int(name[2:]))
        require(entry[6] * 8 + 8 <= fat_size, 'Overlay file ID escapes FAT')
        begin, end = struct.unpack_from('<II', rom, fat + entry[6] * 8)
        require(0 <= begin < end <= len(rom), 'Overlay original file span invalid')
        data = decompress(rom[begin:end]) if entry[7] >> 24 & 1 else rom[begin:end]
        require(len(data) == entry[2] == module['bytes'] and int(module['base'], 0) == entry[1], 'Original overlay load address/initialized extent differs')
        require(hashlib.sha256(data).hexdigest() == module['sha256'] == sha256(ROOT / module['binary']), 'Original overlay derived/extracted hash differs')
        values[module['binary']] = data
        proofs.append(dict(path=module['binary'], sha256=module['sha256'], module=name, tableEntry=list(entry), originalFatRange=[begin, end], initializedBytes=len(data)))
    for pin in contracts['references']:
        require(pin['path'] in values and hashlib.sha256(values[pin['path']]).hexdigest() == pin['sha256'], 'Frozen original comparison role/hash differs')
    return dict(romSha256=contracts['romSha256'], sourceCredit=0, mainSha256=hashlib.sha256(main).hexdigest(),
        overlayDerivations=proofs, originalsAreNeverCompilerInputs=True), values


def _comparison_projection(actual, contracts):
    selected = {item['report']: item for item in contracts['consumers']}
    require(len(selected) == len(contracts['consumers']), 'Duplicate exact overlay report contract')
    require(all(sum(batch['report'] == name for batch in actual) == 1 for name in selected), 'Missing or duplicate selected overlay batch')
    projected = copy.deepcopy(actual)
    removed = []
    for batch in projected:
        if batch['report'] not in selected:
            continue
        contract = selected[batch['report']]
        for row in contract['rows']:
            require(batch['sourceHashes'].get(row['source']) == row['sourceSha256'], 'Selected batch lacks its exact frozen C source pin')
            for header in row['sourceDependencies']:
                require(batch['sourceHashes'].get(header['path']) == header['sha256'], 'Selected batch lacks its exact frozen quoted-header pin')
        references = {pin['path']: pin['sha256'] for pin in contract['comparisonInputs']}
        require({name: digest for name, digest in batch['sourceHashes'].items() if name.startswith('extract/')} == references, 'Unknown/missing/changed original comparison input in selected overlay batch')
        for name, digest in references.items():
            del batch['sourceHashes'][name]
            removed.append(dict(report=batch['report'], path=name, sha256=digest, role='Independently derived original comparison evidence; zero compiler/source credit'))
    for before, after in zip(actual, projected):
        if before['report'] not in selected:
            require(before == after, 'Unrelated legacy batch changed')
        else:
            require({name: digest for name, digest in before['sourceHashes'].items() if not name.startswith('extract/')} == after['sourceHashes'], 'Authored or other frozen source pin removed')
    return projected, removed


def wrong_profile_control(row, directory):
    adjusted = copy.deepcopy(row)
    flags = adjusted['compilerFlags']
    index = flags.index('-lang')
    adjusted['compilerFlags'] = flags[:index] + flags[index + 2:]
    require(adjusted['compilerFlags'].count('-O2') == 1, 'Negative profile control lacks its exact O2 input')
    adjusted['compilerFlags'][adjusted['compilerFlags'].index('-O2')] = '-O0'
    started = time.time_ns()
    try:
        fresh_c99(adjusted, directory)
    except AssertionError:
        output = directory / 'explicit-c99.o'
        require(output.is_file() and output.stat().st_mtime_ns >= started, 'Wrong-profile control did not actually compile fresh C99')
        original, wrong = signature(ROOT / row['object'], row['name']), signature(output, row['name'])
        require(original != wrong, 'Wrong-profile fresh C99 did not test the complete byte/relocation gate')
        return dict(rejected=True, actualFreshWrongProfileC99Compiled=True, instructionObjectAndRelocationPatching=False,
            object=output.relative_to(ROOT).as_posix(), objectSha256=sha256(output), originalSignature=original,
            wrongProfileSignature=wrong, wrongFlags=adjusted['compilerFlags'], sourceCredit=0)
    raise ValueError('Wrong-profile source object was accepted as identical')


def qualify(contracts, directory, committed=False):
    directory = Path(directory).resolve()
    require(directory.is_relative_to(ROOT / 'work'), 'Live qualification output must remain under repository work')
    snapshot = scope_snapshot(contracts, directory / 'main-append', committed=committed)
    derivations, images = derive_references(contracts)
    qualified, ordinal = [], 0
    for consumer in contracts['consumers']:
        require(sha256(ROOT / consumer['report']) == consumer['reportSha256'], 'Frozen canonical report changed')
        report = read_json(ROOT / consumer['report'])
        actual = validate_report(report, consumer)
        proofs = []
        for row in actual.values():
            inputs = compiler_inputs(row)
            adjusted = copy.deepcopy(row)
            index = adjusted['compilerFlags'].index('-lang')
            adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
            unit_directory = directory / f'{ordinal:02d}'
            fresh = fresh_c99(adjusted, unit_directory / 'c')
            before, after = arm_mapping(ROOT / row['object'], row['name']), arm_mapping(ROOT / fresh['explicitC99Object'], row['name'])
            require(before == after and before['functionBytes'] == row['bytes'], 'Fresh actual ARM mapping/full extent differs')
            linked_row = dict(row, object=fresh['explicitC99Object'], objectSha256=fresh['explicitC99ObjectSha256'])
            linked = linker.validate(linked_row, row['nativeSymbolEntries'], unit_directory / 'l')
            require(linked['exactCallerBytes'] and linked['linkedCallerSha256'] == row['targetSha256'], 'Fresh C99 genuine native link differs')
            require(all(probe['initializedCodeBytes'] == probe['nativeCalleeBytesUsed'] == probe['calleeSourceCredit'] == 0 for probe in linked['bindingOnlyProbes']), 'Executable original callee implementation entered the fresh link')
            module = next(item for item in contracts['modules'] if item['name'] == row['module'])
            offset = int(row['address'], 0) - int(module['base'], 0)
            require(hashlib.sha256(images[module['binary']][offset:offset + row['bytes']]).hexdigest() == row['targetSha256'], 'Wrong original overlay caller bytes')
            proofs.append(dict(identity=list(identity(row)), bytes=row['bytes'], sourceOnlyCompilerInput=inputs,
                actualArmMapping=after, explicitC99=fresh, freshGenuineLink=linked, sourceCredit=0))
            ordinal += 1
        qualified.append(dict(report=consumer['report'], reportSha256=consumer['reportSha256'], proofs=proofs))
        print(dict(qualifiedReports=len(qualified), freshIdenticalC99Functions=ordinal), flush=True)
    require(ordinal == 39, 'Exact frozen overlay function set changed')
    negative = wrong_profile_control(read_json(ROOT / contracts['consumers'][0]['report'])['matches'][0], directory / 'negative-profile')
    ensure_scope(snapshot)
    result = dict(passed=True, qualificationOnly=True, registered=False, sourceCredit=0, functions=ordinal,
        bytes=sum(row['bytes'] for consumer in contracts['consumers'] for row in consumer['rows']),
        contractsSha256=sha256(ROOT / CONTRACT), derivedOriginalReferences=derivations, consumers=qualified,
        allFullProgramCpuModuleModeAddressIdentitiesRetained=True, allLiveScopePinsUnchanged=True,
        allC99FunctionBytesRelocationsMappingsAndFreshNativeLinksEqual=True, globalChecksRun=False,
        legacyMainAssertionsUnchangedAndOriginal26LedgerRecordsPreserved=True, actualCompiledWrongProfileControl=negative,
        generatorSha256=sha256(Path(__file__)))
    result['liveScope'] = snapshot
    result['committedMode'] = committed
    write_json(directory / 'qualification.json', result)
    return result


