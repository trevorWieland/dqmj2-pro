import contextlib
import copy
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, sha256
import auth_context_function_extract_20261106 as extractor
import link_runtime_unit as linker
import wave20261106_dwc_auth_next_context_link as whole_linker

CONTRACT = 'provenance/auth-http-context-function-route-v2-20261106.json'


def contract():
    row = read_json(ROOT / CONTRACT)
    assert row['sourceCredit'] == row['contextDataCredit'] == 0
    assert sha256(ROOT / row['ready']) == row['readySha256']
    assert sha256(ROOT / row['source']) == row['sourceSha256']
    assert sha256(ROOT / row['object']) == row['objectSha256']
    assert sha256(ROOT / row['contextDataClaim']) == row['contextDataClaimSha256'] == extractor.CLAIM_SHA
    assert sha256(ROOT / 'wave20261106_dwc_auth_next_context_link.py') == row['wholeObjectLinkHelperSha256']
    assert (row['program'], row['processor'], row['module'], row['mode'], row['address'], row['bytes']) == ('', 'arm9', 'main', 'thumb', '0x209770c', 192)
    return row


def validate_context(entry, bindings, directory, original_validate):
    declared = contract()
    for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'name', 'source', 'sourceSha256']:
        assert entry[key] == declared[key], ('Context route identity changed', key)
    assert sha256(ROOT / entry['object']) == entry['objectSha256']
    root = Path(directory or ROOT / 'work/lowlevel-recovery/auth-context-links' / entry['objectSha256'])
    whole = whole_linker.validate(entry, bindings, root / 'whole-compiler-object')
    assert whole['exactCallerBytes'] and whole['contextExactOriginalBytes'] and whole['unchangedWholeCompilerObject']
    assert whole['contextDataSourceCredit'] == 0 and whole['compilerObjectRewritten'] is False
    original_object = (ROOT / entry['object']).resolve()
    raw_rows = linker.relocation_rows
    original_relocations = raw_rows(original_object, entry['name'])
    assert [(r['offset'], r['type'], r['symbol'], r['explicitAddend']) for r in original_relocations
            if r['symbol'] in ['.data', extractor.DATA_SYMBOL]] == [(156, 2, '.data', 0), (176, 2, extractor.DATA_SYMBOL, 0)]

    def split(elf, name, output, *extra, **options):
        assert name == declared['name'] and not extra and options == {'section_padding': 0}
        return extractor.extract(elf, name, output)

    def canonical_rows(path, name):
        rows = raw_rows(path, name)
        if path.resolve() == original_object:
            for row in rows:
                if row['symbol'] == '.data':
                    row['symbol'] = extractor.DATA_SYMBOL
        return rows

    with patch.object(linker, 'split_symbol', split), patch.object(linker, 'relocation_rows', canonical_rows):
        result = original_validate(entry, bindings, root / 'derived-function')
    result['wholeCompilerContextLink'] = whole
    result['originalRawRelocations'] = original_relocations
    result['contextFunctionExtraction'] = dict(sourceCredit=0, contextDataCredit=0,
        originalWholeCompilerObjectUnchanged=True, instructionAndLiteralBytesUnchanged=True,
        relocationOffsetsTypesAddendsAndEncodedWordsUnchanged=True,
        sectionReferenceCanonicalizedToActualDefinedGlobalObject=True,
        originalSectionSymbol='.data', actualOriginalGlobalObject=extractor.DATA_SYMBOL,
        originalSectionOffset=0, originalContextAddress='0x20deb2c', contextBytes=28,
        originalSymbolNamesPreserved=False, route=CONTRACT, routeSha256=sha256(ROOT / CONTRACT),
        generatorSha256=sha256(ROOT / 'auth_context_route_v2_20261106.py'),
        extractorSha256=sha256(ROOT / 'auth_context_function_extract_20261106.py'))
    return result


@contextlib.contextmanager
def validation_route():
    declared = contract()
    original = linker.validate

    def routed(entry, bindings, directory=None):
        if entry['name'] != declared['name']:
            return original(entry, bindings, directory)
        return validate_context(entry, bindings, directory, original)

    with patch.object(linker, 'validate', routed):
        yield


@contextlib.contextmanager
def module_route(module_builder):
    declared = contract()
    original = module_builder.split_symbol

    def routed(elf, name, output, *extra, **options):
        if name != declared['name']:
            return original(elf, name, output, *extra, **options)
        source = Path(elf.stream.name)
        assert sha256(source) == declared['objectSha256']
        intermediate = output.with_suffix('.context-source.o')
        assert intermediate.resolve() != source.resolve() and output.resolve() != source.resolve()
        extractor.extract(elf, name, intermediate)
        with intermediate.open('rb') as stream:
            return original(type(elf)(stream), name, output, *extra, **options)

    with patch.object(module_builder, 'split_symbol', routed):
        yield
