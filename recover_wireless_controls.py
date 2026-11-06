import json
from pathlib import Path
import match_arm7
import utility_code
import utility_runtime
import wireless_oracle
from match_utility_primitives import native_bindings

ROOT = Path(__file__).resolve().parent
UNITS = [('arm7', 'arm7-main', 0x027E9CC0, 'wireless23', 2),
         ('utility', 'utility-child-arm7-main', 0x027F15BC, 'wireless14', 1)]


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
            raise ValueError('Frozen wireless control C source changed')
        compiler = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        if target == 'arm7':
            entry, compiled = match_arm7.compare(source, spec, compiler, utility_code.COMPILER_HASH, level, 'off')
        else:
            entry, compiled = utility_code.compile_compare(source, dict(spec, compilerPath=compiler), level, 'off')
        if compiled is None:
            raise ValueError('Wireless control C stopped matching all native bytes and relocations')
        entry['oracle'] = wireless_oracle.verify(compiled, spec)
        entry['sourceModel'] = {'kind': 'shift-and-register-store', 'stateFieldOffset': 0x354, 'shift': 1,
                                'registerAddress': '0x0480803c', 'width': 2} if target == 'arm7' else {
                                'kind': 'clear-state-register', 'stateFieldOffset': 0x4a4, 'registerAddress': '0x04808080',
                                'width': 2, 'sharedPointerCachedBeforeRegisterWrite': True}
        report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'runtimeMappingCanonical': True,
                  'matches': [entry], 'nativeSymbols': {rel['symbol']: rel['target'] for rel in entry['relocations']},
                  'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
                  'limitations': ['Ordinary C preserves the measured halfword field/register operation and ordering; application field meanings remain unknown',
                                  'MMIO is an isolated Unicorn byte window, not physical hardware; volatile C preserves the native register access',
                                  'Source-only replay checks frozen C, pinned compiler, qualified runtime module hash and bounded independent effects']}
        if target == 'utility':
            report.update(program=utility_runtime.PROGRAM, nativeSymbolBindings=native_bindings([entry]))
        else:
            report['processor'] = 'arm7'
        path.write_text(json.dumps(report, indent=2) + '\n')
        print({'target': target, 'module': module, 'address': hex(address), 'bytes': entry['bytes'], 'cases': entry['oracle']['vectors']})


if __name__ == '__main__':
    main()
