import json
from pathlib import Path
import match_arm7
import utility_code
import utility_runtime
import wireless_oracle
from match_utility_primitives import native_bindings

ROOT = Path(__file__).resolve().parent
UNITS = [('arm7', 'arm7-main', 0x027EBFEC, 'wireless22', 2),
         ('utility', 'utility-child-arm7-main', 0x027E9DF4, 'wireless13', 1)]


def main():
    for target, module, address, batch, level in UNITS:
        path = ROOT / f'evidence/matches/{target}-{batch}.json'
        previous = json.loads(path.read_text()) if path.exists() else None
        if previous:
            old = previous['matches'][0]
            spec = match_arm7.accepted_spec(old) if target == 'arm7' else utility_code.accepted_spec(old)
        else:
            candidates = match_arm7.candidates(192) if target == 'arm7' else utility_code.candidates()
            spec = next(spec for spec in candidates if spec['module'] == module and spec['address'] == address)
        name = f'native_{module.replace("-", "_")}_{address:08x}'
        source = ROOT / f'src/{"arm7" if target == "arm7" else "utility"}/{batch}/{name}.c'
        if previous and utility_runtime.sha(source.read_bytes()) != old['sourceSha256']:
            raise ValueError('Frozen wireless leaf C source changed')
        compiler = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        if target == 'arm7':
            entry, compiled = match_arm7.compare(source, spec, compiler, utility_code.COMPILER_HASH, level, 'off')
        else:
            entry, compiled = utility_code.compile_compare(source, dict(spec, compilerPath=compiler), level, 'off')
        if compiled is None:
            raise ValueError('Frozen wireless leaf stopped matching all native bytes and relocation entries')
        entry['oracle'] = wireless_oracle.verify(compiled, spec)
        entry['sourceModel'] = {'kind': 'fixed-stride-record-accessor', 'recordBytes': 28, 'fieldOffset': 0,
                                'historicalRecordCountKnown': False} if target == 'arm7' else {
                                'kind': 'halfword-mask-query', 'sourceFieldOffset': 0x32c, 'definedShiftSelectors': [0, 31]}
        report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'runtimeMappingCanonical': True,
                  'matches': [entry], 'nativeSymbols': {rel['symbol']: rel['target'] for rel in entry['relocations']},
                  'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
                  'limitations': ['Ordinary C models measured record stride or bit query; application names, record count and historical source types are unproven',
                                  'Only complete CPU/module-qualified native spans and real compiler relocation objects are accepted',
                                  'The independent RAM fixture is bounded to32 records or shift selectors0..31 and does not execute native helper bodies']}
        if target == 'utility':
            report.update(program=utility_runtime.PROGRAM, nativeSymbolBindings=native_bindings([entry]))
        else:
            report['processor'] = 'arm7'
        path.write_text(json.dumps(report, indent=2) + '\n')
        print({'target': target, 'module': module, 'address': hex(address), 'bytes': entry['bytes'], 'cases': entry['oracle']['vectors']})


if __name__ == '__main__':
    main()
