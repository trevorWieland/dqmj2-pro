import re
from project import ROOT, read_json, write_json, sha256
from slice_reference_sdk_entities_v3_20261102 import functions


def main():
    name = 'evidence/matches/main-sdk-breadth3176-20261102.json'
    report = read_json(ROOT / name)
    results = []
    for row in report['matches']:
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        text = source.read_text(encoding='utf-8')
        assert '#include' not in text
        assert not re.search(r'\b(?:asm|__asm|__asm__|va_list|J2pUnknown)\b', text)
        entries = [r for r in functions(text) if r['name'] == row['name']]
        assert len(entries) == 1
        header = text[entries[0]['start']:entries[0]['opening']].strip()
        assert not re.search(re.escape(row['name']) + r'\s*\(\s*\)', header)
        declarations = []
        for relocation in row.get('relocations', []):
            symbol = relocation['symbol']
            if not symbol.startswith('native_fn_'): continue
            pattern = r'(?m)^\s*(?:extern\s+)?(?:static\s+)?(?:inline\s+)?(?:[A-Za-z_]\w*\s+)+\**\s*' + re.escape(symbol) + r'\s*\([^;{}]*\)\s*[;{]'
            matches = re.findall(pattern, text)
            assert matches, (row['name'], symbol)
            assert all(not re.search(re.escape(symbol) + r'\s*\(\s*\)', declaration) for declaration in matches)
            declarations.append(dict(symbol=symbol, declarations=[m.strip() for m in matches]))
        assert row['sourceOnlyCompilerInput'] and not row['originalObjectScaffolding']
        linked = row['genuineLinkComparison']
        proof = ROOT / linked['isolatedCallerLinkValidation']
        assert sha256(proof) == linked['isolatedCallerLinkValidationSha256']
        assert read_json(proof)['exactCallerBytes']
        results.append(dict(address=row['address'], bytes=row['bytes'], source=row['source'],
            sourceSha256=sha256(source), typedEntryDefinition=header,
            fullyDeclaredRelocatedFunctions=declarations, completePinnedSourceAndLinkChecked=True))
    write_json(ROOT / 'evidence/abi/main-sdk-breadth3176-source-interfaces-20261102.json',
        dict(passed=True, sourceCredit=0, matchingReport=name, matchingReportSha256=sha256(ROOT / name),
            ordinaryCFunctions=len(results), initializedBytes=sum(r['bytes'] for r in results), results=results,
            sourceMeaningAndOrdinaryReachabilityProven=False, actualNativeFunctionReturns=0,
            limits='Lexical source-interface and complete linked-byte audit; no gameplay or native behavioral qualification'))
    print(dict(ordinaryCInterfaceAudits=len(results), matchingInitializedBytes=sum(r['bytes'] for r in results),
        emptyRelocatedPrototypes=0, sourceCredit=0))


if __name__ == '__main__':
    main()
