import argparse
import contextlib
import functools
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
import uuid
from pathlib import Path
from bytematch_project import DENOMINATOR, REPORTS, contained, digest, read, selected_rows, namespace, write
from native_objects import FreshObjects, selected_metadata
from public_manifest import verify
from native_mb_context import register_context


APPROVED_CHECKPOINTS = {
    '1a3602d9eb57e0952f8bf003de2bf2a189294158e77469577ecfda26d10e8c60':
        (172, '14ac8dcd6f8ab0009e5dd54d73cf31c928540776', 11482, 1224354),
    '9325fb758e0e68446c4fe885b4fe5422b0b5c35fac0208a48cf49dfbbf7d6250':
        (173, 'c7ef53f30f326f0d3b38d0eeb61186a1a3f9dd4c', 11546, 1236780),
    '6d613fb925b8acbad647b9c27a1b5825a02016c493d4ae03dcd09b194a17f9d8':
        (174, '96198869f6da84c51da3e506888061aa92f1249f', 11640, 1262114),
    '8d4d8623cd416b87d8700b970de1ad687c826064cd5745e9e1f2883ecea4d18b':
        (175, 'e56b4df0c067ec6fd83cb6d3205c59cb5308fd7c', 11652, 1265646),
}


def approved_checkpoint(manifest, manifest_hash):
    expected = APPROVED_CHECKPOINTS.get(manifest_hash)
    actual = (manifest.get('revision'), manifest.get('acceptedFunctions'), manifest.get('acceptedInitializedBytes'))
    if (expected is None or actual != expected[1:]
            or manifest.get('initializedDenominatorBytes') != DENOMINATOR
            or manifest.get('romSha256') != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'):
        raise ValueError('Native driver requires an approved closed source checkpoint and exact manifest bytes')
    return expected[0]


def runtime(root):
    sys.path.insert(0, str(root))
    project = importlib.import_module('project')
    if project.ROOT.resolve() != root:
        raise ValueError('Native builder imported a different checkout')
    config = project.configuration()
    project.native_dependencies(config)
    return project, config


def failure_status(root, error):
    root = root.resolve()
    frames = []
    for frame, line in traceback.walk_tb(error.__traceback__):
        try:
            path = Path(frame.f_code.co_filename).resolve()
        except (OSError, TypeError, ValueError):
            continue
        if not path.is_relative_to(root):
            continue
        relative = path.relative_to(root)
        owned = len(relative.parts) == 1 or relative.parts[0] == 'public_tools'
        function = frame.f_code.co_name
        if owned and path.is_file() and re.fullmatch(r'[A-Za-z_]\w*\.py', path.name):
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,127}|<(?:module|listcomp|dictcomp|setcomp|genexpr|lambda)>', function):
                function = '<unknown>'
            frames.append(dict(file=path.name, line=line, function=function))
    kind = type(error).__name__
    status = dict(errorType=kind if re.fullmatch(r'[A-Za-z_]\w{0,63}', kind) else 'Exception', frames=frames[-8:])
    if isinstance(error, OSError) and isinstance(error.filename, (str, os.PathLike)):
        try:
            missing = Path(error.filename).resolve()
        except (OSError, TypeError, ValueError):
            return status
        if missing.is_relative_to(root):
            relative = missing.relative_to(root)
            public = len(relative.parts) == 1 or relative.parts[0] in {'public', 'public_tools', 'config', 'evidence', 'ledger', 'provenance'}
            if public and missing.suffix in {'.json', '.yaml', '.yml', '.txt', '.py', '.lcf'} and re.fullmatch(r'[A-Za-z0-9_./-]+', relative.as_posix()):
                status['missingInput'] = relative.as_posix()
    return status


def write_failure_status(root, error):
    destination = (root / 'build/B2JJ-modified/native-failure-status.json').resolve()
    if not root.is_dir() or not destination.is_relative_to(root.resolve()):
        raise ValueError('Native failure status must remain inside the source root')
    write(destination, failure_status(root, error))


@contextlib.contextmanager
def attributes(target, **values):
    previous = {key: getattr(target, key) for key in values}
    try:
        for key, value in values.items():
            setattr(target, key, value)
        yield
    finally:
        for key, value in previous.items():
            setattr(target, key, value)


def original_modules(root, manifest):
    inventory = read(contained(root, 'ledger/modules.json'))
    modules = inventory['modules']
    if inventory['buildSha256'] != manifest['romSha256'] or len(modules) != 20 or sum(m['bytes'] for m in modules) != DENOMINATOR:
        raise ValueError('Focused native build requires all twenty measured modules')
    if len({m['name'] for m in modules}) != 20:
        raise ValueError('Native module namespaces are not unique')
    for module in modules:
        if digest(contained(root, module['binary'])) != module['sha256']:
            raise ValueError('Original module identity differs: ' + module['name'])
    return modules


@contextlib.contextmanager
def auth_extraction(builder, root, units):
    matching = [u for u in units if u.get('function') == 'native_main_0209770c']
    if not matching:
        yield None
        return
    descriptor = contained(root, 'provenance/auth-http-context-function-route-v2-20261106.json')
    declared = read(descriptor)
    qualification = contained(root, 'evidence/verification/auth-context-production-routing-v2-qualification-20261106.json')
    if digest(qualification) != '7429d3fceaf2e63a91f4b4e6f3d384631b5066f805bfb2ad4d24cbcf59c77423':
        raise ValueError('Inherited private AuthStart qualification artifact differs')
    proof = read(qualification)
    if len(matching) != 1 or not proof['passed'] or proof['sourceCredit'] or proof['contextDataCredit'] or not proof['scopeNegativeControlsPassed'] or not proof['originalAllSharedChecksRetained']:
        raise ValueError('Qualified AuthStart extraction scope or controls differ')
    recipe = {name: proof['qualifiedCodeAndDescriptorHashes'][name] for name in (
        'auth_context_function_extract_20261106.py', 'auth_context_route_v2_20261106.py', descriptor.relative_to(root).as_posix())}
    for name, expected in recipe.items():
        if digest(contained(root, name)) != expected:
            raise ValueError('Qualified AuthStart helper or descriptor changed')
    unit = matching[0]
    if (unit['module'], unit['mode'], int(unit['start'], 0), int(unit['end'], 0), unit['source'], unit['sourceSha256']) != (
            'main', 'thumb', 0x0209770c, 0x020977cc, declared['source'], declared['sourceSha256']):
        raise ValueError('Qualified AuthStart source identity differs')
    extractor = importlib.import_module('auth_context_function_extract_20261106')
    if declared['sourceCredit'] or declared['contextDataCredit'] or proof['originalCompilerObjectSha256'] != declared['objectSha256']:
        raise ValueError('Frozen AuthStart qualification provenance differs')
    for name, expected in ((declared['ready'], declared['readySha256']),
                           (declared['contextDataClaim'], declared['contextDataClaimSha256']),
                           ('wave20261106_dwc_auth_next_context_link.py', declared['wholeObjectLinkHelperSha256'])):
        if digest(contained(root, name)) != expected:
            raise ValueError('Frozen AuthStart context input differs')
    original = builder.split_symbol
    def split(elf, name, output, *extra, **options):
        if name != declared['name']:
            return original(elf, name, output, *extra, **options)
        source = Path(elf.stream.name)
        before = digest(source)
        intermediate = output.with_suffix('.context-source.o')
        extractor.extract(elf, name, intermediate)
        with intermediate.open('rb') as stream:
            result = original(type(elf)(stream), name, output, *extra, **options)
        if digest(source) != before:
            raise ValueError('Fresh compiler object changed during qualified AuthStart extraction')
        return result
    with attributes(builder, split_symbol=split):
        yield dict(descriptor=descriptor.relative_to(root).as_posix(), descriptorSha256=digest(descriptor),
                   qualificationSha256=digest(qualification), originalFreshCompilerObjectUnchanged=True,
                   qualificationProvenance='owner-supplied untracked private artifact', qualifiedRecipeHashesVerified=recipe,
                   inheritedHistoricalPins={name: dict(sha256=expected, verified=False, replayed=False,
                       available=(root / name).is_file()) for name, expected in proof['qualifiedCodeAndDescriptorHashes'].items() if name not in recipe},
                   contextDataSourceCredit=0, historicalObjectReplayed=False, qualificationOraclesReplayed=False)


def host_arm9(root, work, config, canonical, fresh):
    builder = importlib.import_module('build_modules')
    gap_alignment = importlib.import_module('data_gap_alignment')
    layout = importlib.import_module('linker_layout_regions')
    if builder.ROOT.resolve() != root or digest(config['dsd']) != builder.DSD_HASH or digest(config['linker']) != builder.LINKER_HASH:
        raise ValueError('Pinned native linker/dsd identity or checkout differs')
    units = [fresh.unit(unit) for unit in canonical['sourceUnits']]
    spec = work / 'arm9-source-units.json'
    write(spec, dict(schemaVersion=1, units=units, nativeSymbols=canonical.get('nativeSymbols', {})))
    output = work / 'host-arm9'
    output.mkdir()
    report = dict(schemaVersion=1, createdUtc=importlib.import_module('project').now(),
                  buildNamespace=fresh.manifest['romSha256'], kind='fresh-source-original-gap-native-link',
                  sourceReconstruction=False, commands=[], modules=[], replacements=[], sourceUnits=[])
    environment = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    with attributes(builder, WORK=output), auth_extraction(builder, root, units) as context, register_context(builder, root, units):
        prepared = builder.prepare_units(spec, report)
        generated = builder.generated_config(prepared)
        def run(command):
            if not builder.run(command, output, environment, report, timeout=600):
                raise ValueError('Native ARM9 tool failed: ' + Path(str(command[0])).name)
        run([config['linker'], '-version'])
        run([config['dsd'], 'delink', '--config-path', generated, '--all-mapping-symbols'])
        run([config['dsd'], 'lcf', '--config-path', generated])
        builder.native_link_symbols(report)
        builder.thumb_gap_alignment(report)
        gap_alignment.apply(report, output)
        run([config['linker'], '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', 'Entry',
             '-sym', 'on', '-map', output / 'arm9.lcf', '@' + str(output / 'objects.txt'), '-o', output / 'linked.elf'])
        run([config['dsd'], 'check', 'modules', '--config-path', generated, '--fail'])
        run([config['dsd'], 'check', 'symbols', '--config-path', generated, '--elf-path', output / 'linked.elf', '--fail'])
        builder.compare_modules(report)
        if not report['modules'] or not all(m.get('exactBytes') for m in report['modules']):
            raise ValueError('Genuinely linked ARM9 module bytes differ')
        report.update(allModuleBytesExact=True, symbolCheckPassed=True,
                      sourceLinkedBytes=sum(u['compiledBytes'] for u in report['sourceUnits']),
                      sourceBssBytes=sum(u.get('allocatedBytes', 0) for u in report['sourceUnits']))
        layout.annotate(report, output)
        report['qualifiedAuthContextRoute'] = context
    return report


def host_arm7(root, work, config, fresh):
    builder = importlib.import_module('link_arm7')
    project = importlib.import_module('project')
    layout = read(contained(root, 'evidence/arm7/runtime-layout.json'))
    canonical = read(contained(root, 'evidence/linking/arm7-latest.json'))
    functions, symbols, unused_bindings, metadata = selected_metadata(root, canonical, processor='arm7')
    functions = [fresh.entry(item) for item in functions]
    for item in metadata:
        fresh.entry(item)
    output = work / 'host-arm7'
    output.mkdir()
    report = dict(schemaVersion=1, createdUtc=project.now(), buildNamespace=fresh.manifest['romSha256'],
                  modules=[], sourceUnits=[], sourceReconstructionComplete=False)
    def failure_report(path, value):
        write(work / 'diagnostics' / Path(path).name, value)
    with attributes(builder, write_json=failure_report):
        for module in layout['modules']:
            result, units = builder.build_module(module, functions, symbols, config, output_root=output)
            report['modules'].append(result)
            report['sourceUnits'].extend(units)
    report.update(allModuleBytesExact=all(m['exactBytes'] for m in report['modules']),
                  symbolCheckPassed=all(m['symbolCheckPassed'] for m in report['modules']),
                  sourceLinkedBytes=sum(u['compiledBytes'] for u in report['sourceUnits']))
    return report


def child(root, work, config, fresh):
    utility = importlib.import_module('link_utility')
    linker = importlib.import_module('link_program')
    project = importlib.import_module('project')
    state = importlib.import_module('utility_state')
    modules, unused_candidates, layout = state.runtime_state()
    if not layout or len(modules) != 6:
        raise ValueError('Embedded native runtime inventory is incomplete')
    canonical = read(contained(root, 'evidence/linking/utility-latest.json'))
    plans = {r['processor']: selected_metadata(root, canonical, layout['program'], r['processor']) for r in layout['processors']}
    for plan in plans.values():
        for item in plan[3]:
            fresh.entry(item)
    tail = read(contained(root, 'evidence/utility/itcm-tail.json'))
    module = next(m for m in modules if m['name'] == tail['module'])
    if module['sha256'] != tail['inputModuleSha256'] or not tail['supportsDeterministicLinkerZeroAlignment']:
        raise ValueError('Embedded alignment proof differs from measured input')
    module['sourceAlignmentFill'] = dict(start=tail['tail']['address'], bytes=tail['tail']['bytes'],
                                       alignment=tail['observedExtentAlignment'], evidence='evidence/utility/itcm-tail.json',
                                       evidenceSha256=digest(root / 'evidence/utility/itcm-tail.json'))
    output = work / 'child'
    output.mkdir()
    report = dict(schemaVersion=1, createdUtc=project.now(), buildNamespace=fresh.manifest['romSha256'],
                  program=layout['program'], modules=[], sourceUnits=[], sourceReconstructionComplete=False)
    imported = 0
    original_linkage = []
    for processor in layout['processors']:
        functions, symbols, bindings, unused_metadata = plans[processor['processor']]
        for item in functions:
            if item.get('kind') != 'linkage':
                continue
            module = next(m for m in modules if m['name'] == item['module'])
            image = contained(root, module['binary']).read_bytes()
            offset = int(item['address'], 0) - int(module['base'], 0)
            size = item.get('bytes', item.get('size'))
            if hashlib.sha256(image[offset:offset + size]).hexdigest() != item['sha256']:
                raise ValueError('Original zero-credit linkage span differs from frozen metadata')
            imported += size
            original_linkage.append(dict(module=item['module'], address=item['address'], bytes=size,
                                         sha256=item['sha256'], sourceCredit=0, input='measured-original-module-gap'))
        functions = [fresh.entry(item) for item in functions if item.get('kind') != 'linkage']
        selected = [m for m in modules if m['processor'] == processor['processor']]
        def failure_report(path, value):
            write(work / 'diagnostics' / Path(path).name, value)
        with attributes(linker, write_json=failure_report):
            results, units = linker.build_cpu(selected, functions, symbols, bindings, config, output, processor['resetEntry'])
        report['modules'].extend(results)
        report['sourceUnits'].extend(units)
    report.update(allModuleBytesExact=all(m['exactBytes'] for m in report['modules']),
                  symbolCheckPassed=all(m['symbolCheckPassed'] for m in report['modules']),
                  sourceLinkedBytes=sum(u['compiledBytes'] for u in report['sourceUnits'] if u.get('kind') != 'linkage'),
                  importedFrozenLinkageBytes=imported, importedLinkageSourceCredit=0,
                  originalGapLinkageBytes=imported, originalGapLinkageRanges=original_linkage)
    return report


def verify_results(root, work, modules, reports, manifest):
    expected = {m['name']: m for m in modules}
    actual, credited = {}, set()
    accepted = {}
    for row in manifest['functions']:
        accepted.setdefault((*namespace(row), row['sourceUnit'], row['sourceSha256']), []).append(row)
    for report in reports:
        if not report.get('allModuleBytesExact') or not report.get('symbolCheckPassed'):
            raise ValueError('Native module bytes and symbol checks must all pass')
        for item in report['modules']:
            if item['module'] in actual or item['module'] not in expected:
                raise ValueError('Duplicate or unexpected native module')
            module = expected[item['module']]
            output = contained(root, item['output'])
            if not output.is_relative_to(work):
                raise ValueError('Native output must be freshly created beneath this work directory')
            if not item.get('exactBytes') or digest(output) != module['sha256'] or item['inputSha256'] != module['sha256']:
                raise ValueError('Native linker output differs from original module')
            actual[item['module']] = item
        for unit in report['sourceUnits']:
            if unit.get('kind', 'function') != 'function':
                continue
            for row in selected_rows(unit, expected[unit['module']], accepted):
                credited.add(row['id'])
    if set(actual) != set(expected) or len(credited) != len(manifest['functions']):
        raise ValueError('Native build omitted original modules or accepted source functions')
    return dict(moduleCount=len(actual), initializedBytes=sum(m['bytes'] for m in modules),
                acceptedFunctionsLinked=len(credited), allModuleBytesExact=True, allSymbolChecksPassed=True)


def rebuild(root, compilation, output, compiler_root=None, license_file=None, compilation_not_before_ns=None):
    root, output = root.resolve(), output.resolve()
    if not output.is_relative_to(root / 'work') or output == root / 'work' or output.exists():
        raise ValueError('Use a new dedicated native build directory beneath work/')
    compilation = contained(root, compilation)
    if compilation_not_before_ns is not None and compilation_not_before_ns <= 0:
        raise ValueError('CI compilation start time must be positive')
    if compilation_not_before_ns is not None and compilation.stat().st_mtime_ns < compilation_not_before_ns:
        raise ValueError('Source compilation report predates this CI build')
    source_verifier = importlib.import_module('public_manifest')
    with attributes(source_verifier, include_names=functools.lru_cache(maxsize=None)(source_verifier.include_names)):
        manifest, unused_units, unused_pins, unused_summary = verify(root, root / 'public/accepted-functions.json')
    approved_checkpoint(manifest, digest(root / 'public/accepted-functions.json'))
    modules = original_modules(root, manifest)
    project, config = runtime(root)
    builder = importlib.import_module('build_modules')
    if digest(config['linker']) != builder.LINKER_HASH or digest(config['dsd']) != builder.DSD_HASH:
        raise ValueError('Pinned native linker or dsd identity differs')
    inputs = project.verify_inputs(config)
    pins = {name: digest(contained(root, name)) for name in (
        'recovery.json', 'source-preferences.json', 'manifest.json', 'ledger/modules.json',
        *('evidence/linking/' + name for name in REPORTS))}
    canonical = read(root / 'evidence/linking/latest.json')
    if not canonical.get('allModuleBytesExact') or not canonical.get('symbolCheckPassed') or canonical['buildNamespace'] != manifest['romSha256']:
        raise ValueError('Frozen source selection lacks its accepted native link proof')
    output.mkdir(parents=True)
    fresh = FreshObjects(root, compilation, output / 'fresh-auxiliary', compiler_root or root / 'tools/mwccarm',
                         license_file or config['license'])
    started = time.time_ns()
    receipt = dict(schemaVersion=1, buildPassed=False, nativeBuildPassed=False,
                   publicGitRevision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                   acceptedManifestSha256=digest(root / 'public/accepted-functions.json'), startedTimeNs=started,
                   publicSourceCompileReport=dict(path=compilation.relative_to(root).as_posix(), sha256=digest(compilation),
                                                 modifiedTimeNs=compilation.stat().st_mtime_ns),
                   compilationNotBeforeTimeNs=compilation_not_before_ns,
                   freshCompilationTimeBound=compilation_not_before_ns is not None,
                   canonicalInputs=pins,
                   behavioralReplayPerformed=False, fullContainerBuildPerformed=False,
                   scope='Fresh compilation and genuine linking of all twenty native modules from the closed accepted snapshot.')
    report_paths = {}
    try:
        logs = output / 'native-tools.log'
        reports = []
        with logs.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            reports.append(host_arm7(root, output, config, fresh))
            reports.append(child(root, output, config, fresh))
            reports.append(host_arm9(root, output, config, canonical, fresh))
            registry = importlib.import_module('recovery_registry')
            for batch in registry.batches():
                if batch.get('kind') == 'container':
                    document = read(contained(root, batch['report']))
                    if not document.get('program'):
                        for entry in document.get('containerMatches', []):
                            fresh.entry({**document, **entry})
        for name, report in zip(('arm7-latest.json', 'utility-latest.json', 'latest.json'), reports):
            path = output / 'evidence/linking' / name
            write(path, report)
            report_paths[path.relative_to(root).as_posix()] = dict(sha256=digest(path), modifiedTimeNs=path.stat().st_mtime_ns)
        receipt.update(verify_results(root, output, modules, reports, manifest))
        receipt['freshCompilation'] = fresh.finish()
        receipt['importedFrozenLinkageBytes'] = sum(r.get('importedFrozenLinkageBytes', 0) for r in reports)
        receipt['importedLinkageSourceCredit'] = 0
        if inputs != project.verify_inputs(config) or any(digest(root / name) != value for name, value in pins.items()):
            raise ValueError('Original inputs, accepted registry, or frozen native receipts changed')
        receipt.update(buildPassed=True, nativeBuildPassed=True, frozenInputsUnchanged=True, reports=report_paths)
    except Exception as error:
        receipt['failure'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        receipt['finishedTimeNs'] = time.time_ns()
        write(output / 'native-build-receipt.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--compile-report', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--compiler-root', type=Path)
    parser.add_argument('--license-file', type=Path)
    parser.add_argument('--compilation-not-before-ns', type=int)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.out_dir or root / 'work/nb' / uuid.uuid4().hex[:10]
    if not output.is_absolute():
        output = root / output
    compilation = args.compile_report if args.compile_report.is_absolute() else root / args.compile_report
    try:
        receipt = rebuild(root, compilation, output, args.compiler_root, args.license_file, args.compilation_not_before_ns)
        print(json.dumps({k: v for k, v in receipt.items() if k != 'freshCompilation'}, indent=2))
    except Exception as error:
        traceback.print_exc()
        write_failure_status(root, error)
        parser.exit(1, 'Native rebuild failed; raw diagnostics remain in the private log.\n')


if __name__ == '__main__':
    main()
