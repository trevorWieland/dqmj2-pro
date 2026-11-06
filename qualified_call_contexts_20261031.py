import re
from project import ROOT, configuration, sha256, write_json

CONTRACTS = [
    ('02048404', 'u8', 'u32, const char *, u32, u32',
     'src/runtime/20261029_cache_sdk/lookup_8f132205fc42.c',
     'Four explicit words; native bounded lookup return is zero-extended byte'),
    ('0204854c', 'void *', 'u32, u32',
     'src/runtime/20261029_cache_sdk/acquire_22c90cbd192f.c',
     'Second argument is a scalar record index; Candidate pointer is erased only to an opaque pointer ABI view'),
    ('02049f4c', 'u32', 'void **',
     'src/runtime/main-null01/native_main_02049f4c.c',
     'Native callee reads the pointer-holder word through R0; new menu proof verifies explicit forwarding'),
    ('02061dcc', 'u32', 's32',
     'src/runtime/runtime07/native_main_02061dcc.c',
     'Preserve raw return word and signed input; no universal pointer-pointee or ownership claim'),
]


def catalogue():
    rows = []
    for address, returns, parameters, source, limit in CONTRACTS:
        rows.append({'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': '0x' + address,
                     'alias': 'func_' + address, 'returnType': returns, 'parameterTypes': parameters,
                     'source': source, 'sourceSha256': sha256(ROOT / source), 'qualification': limit,
                     'contextPrototype': 'extern ' + returns + ' func_' + address + '(' + parameters + ');',
                     'sourceCredit': 0, 'callerNativeValidationRequired': True})
    return rows


def apply(context, module, rows, processor="arm9", program=None):
    if processor != "arm9" or program is not None or not (module in {"main", "itcm", "dtcm"} or re.fullmatch(r"ov\d{3}", module)):
        raise ValueError("Host ARM9 context contract cannot cross processor/program namespaces")
    changed = []
    for row in rows:
        assert row['processor'] == 'arm9' and row['module'] == 'main'
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        pattern = r'^extern\s+[^;\n]*\b' + re.escape(row['alias']) + r'\s*\([^;\n]*\);'
        context, count = re.subn(pattern, lambda match: row['contextPrototype'], context, flags=re.M)
        if count:
            changed.append({'address': row['address'], 'prototype': row['contextPrototype'], 'sourceSha256': row['sourceSha256']})
    return context, changed


def main():
    report = {'romSha256': configuration()['romSha256'], 'sourceCredit': 0,
              'contracts': catalogue(), 'generatorSha256': sha256(ROOT / 'qualified_call_contexts_20261031.py'),
              'limitations': ['For new host ARM9 m2c contexts only; original contexts and accepted source are immutable',
                              'These are constrained parameter/return ABI views, not complete object-layout or call-domain proofs',
                              'Every new caller still requires compilation, genuine linking, bounds/ABI review and native validation']}
    write_json(ROOT / 'evidence/verification/qualified-call-contexts-20261031.json', report)
    print({'qualifiedContextContracts': len(report['contracts']), 'sourceCredit': 0})


if __name__ == '__main__':
    main()
