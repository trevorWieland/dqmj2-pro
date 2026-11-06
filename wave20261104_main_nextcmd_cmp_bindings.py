from project import ROOT, read_json, sha256
from wave20261104_main_tail_bindings import verify_original as base_verify, native_relocations
from wave20261104_main_nextcmd_cmp_abi import HELPERS, CALLERS, qualify_binding


def verify_original(entry, bindings):
    if entry.get('program') or entry['processor'] != 'arm9' or entry['module'] != 'main' or entry['mode'] != 'arm' or int(entry['address'], 0) not in CALLERS:
        raise ValueError('Comparison caller crossed reserved original main ARM namespace')
    if set(bindings) != {item['symbol'] for item in entry['relocations']}:
        raise ValueError('Comparison imports do not match actual object relocations')
    old = dict(entry, relocations=[row for row in entry['relocations'] if row['symbol'] not in HELPERS])
    proof = base_verify(old, bindings)
    extra = [row for row in entry['relocations'] if row['symbol'] in HELPERS]
    if len(extra) != 3 or {row['symbol'] for row in extra} != set(HELPERS):
        raise ValueError('Comparison caller helper set differs')
    records = native_relocations()
    abi_path = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-next/sixth/helper-abi.json'
    abi = read_json(abi_path)
    if abi['status'] != 'passed' or not abi['completeFixedBodyGprAndCpsrReferenceEquality']:
        raise ValueError('Original comparison full-register ABI qualification missing')
    helpers = {row['helper']: row for row in abi['originalQualifiedBodiesAndCallsites']['helpers']}
    offsets = {'_fleq': 0x94, '_fls': 0xAC, '_feq': 0xC4}
    for row in extra:
        name = row['symbol']
        qualify_binding(name, dict(bindings[name], program=bindings[name].get('program') or ''))
        origin = int(entry['address'], 0) + row['offset']
        record = records.get(origin)
        if row['offset'] != offsets[name] or row['type'] not in (1, 28, 29) or record is None:
            raise ValueError('Comparison branch site/type differs from original complete caller')
        if record['module'] != 'main' or int(record['address'], 0) != HELPERS[name][0] or int(row['target'], 0) != HELPERS[name][0]:
            raise ValueError('Comparison helper differs from its original branch target/module')
        proof['witnesses'].append(dict(symbol=name, origin=hex(origin), module='main', mode='arm', address=record['address'],
            originalRelocationRecord=record['record'], configuredHelperBytes=helpers[name]['bytes'],
            originalHelperSha256=helpers[name]['targetSha256'], sourceOrCalleeCredit=0))
    proof['comparisonHelperAbi'] = dict(path=abi_path.relative_to(ROOT).as_posix(), sha256=sha256(abi_path),
        helperCases=abi['cases'], helperOrProbeSourceCredit=0)
    return proof
