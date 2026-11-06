import re
from project import ROOT, read_json, write_json, configuration, sha256
from audit_zero_argument_calls_20261031 import signature
import match_runtime as compiler
from link_runtime_unit import validate


def main():
    inputs = read_json(ROOT / 'evidence/verification/forwarded-interfaces-source-inputs-20261031.json')
    assert sha256(ROOT / inputs['audit']) == inputs['auditSha256']
    audit = read_json(ROOT / inputs['audit'])
    compiler.WORK = ROOT / 'work/forwarded-interfaces-20261031/compile'
    results = []
    for candidate in audit['candidates']:
        caller, callee = candidate['caller'], candidate['selectedCallee']
        if caller['module'] != 'main' or caller['mode'] != 'arm' or caller['bytes'] != 12:
            continue
        if not (caller['address'] < 0x02040000 or caller['address'] >= 0x020D0000):
            continue
        text = (ROOT / caller['source']).read_text(encoding='utf-8-sig')
        assert sha256(ROOT / caller['source']) == caller['sourceSha256']
        assert sha256(ROOT / callee['source']) == callee['sourceSha256']
        parsed = signature(text, caller['name'])
        if parsed is None or parsed[0] not in ['', 'void']:
            continue
        symbol = candidate['symbol']
        if not re.fullmatch(r'\s*return\s+' + re.escape(symbol) + r'\s*\(\s*\)\s*;\s*', parsed[1]):
            continue
        declaration = candidate['calleeParameters']
        parts = [part.strip() for part in declaration.split(',')]
        if not all(re.fullmatch(r'(?:u32|s32|int|void)\s*(?:\*\s*)?[A-Za-z_]\w*', part) for part in parts):
            continue
        names = [re.findall(r'[A-Za-z_]\w*', part)[-1] for part in parts]
        callee_text = (ROOT / callee['source']).read_text(encoding='utf-8-sig')
        result_type = re.search(r'^\s*(u32|s32|int)\s+' + re.escape(callee['name']) + r'\s*\(', callee_text, re.M)
        if result_type is None:
            continue
        source = ROOT / f'src/runtime/20261031_forwarded_interfaces/{caller["name"]}.c'
        content = 'typedef unsigned int u32;\ntypedef signed int s32;\n'
        content += f'extern {result_type.group(1)} {symbol}({declaration});\n'
        content += f'u32 {caller["name"]}({declaration}) {{\n    return {symbol}(' + ', '.join(names) + ');\n}\n'
        source.parent.mkdir(parents=True, exist_ok=True)
        payload = content.encode()
        if source.exists():
            assert source.read_bytes() == payload
        else:
            source.write_bytes(payload)
        previous = inputs['compilerInputs'][str(caller['address'])]
        assert sha256(ROOT / previous['compilerPath']) == previous['compilerSha256']
        flags = previous['compilerFlags']
        rows, _ = compiler.compare(source, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
            'speed' in flags, compiler=ROOT / previous['compilerPath'])
        assert len(rows) == 1
        row = rows[0]
        if row.get('exactAfterDeclaredRelocation'):
            binding = dict(processor='arm9', module=callee['module'], mode=callee['mode'], kind='function', address=hex(callee['address']))
            proof = validate(row, {symbol: binding}, directory=ROOT / f'work/forwarded-interfaces-20261031/linked/{caller["name"]}')
            assert proof['exactCallerBytes']
            row.update(realMainLink=proof, exactAfterRealMwLink=True)
        results.append(dict(previous=caller, callee=callee, parameterView=declaration, compiled=row,
            nativeArgumentForwardingProven=False, sourceCredit=0, registered=False))
    write_json(ROOT / 'evidence/attempts/forwarded-interfaces-20261031.json', dict(
        generator='draft_forwarded_interfaces_20261031.py', generatorSha256=sha256(__file__),
        candidates=results, sourceCredit=0, registered=False,
        limitations=['Source-interface hypotheses; byte/link equality does not replace fresh argument-forwarding and return validation']))
    print(dict(candidates=len(results), exact=sum(row['compiled'].get('exactAfterRealMwLink', False) for row in results), sourceCredit=0))


if __name__ == '__main__':
    main()
