import hashlib
import json
import re
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from admit_ov006_aes_resumption_v1_20261106 import spans


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/crypto-utility-resumption-proposal.json'
    assert sha256(ROOT / proposal_name) == 'ba4bd1095436fbe214c691f01ea18fcb5f167566969a3d819967af75c960887e'
    proposal = read_json(ROOT / proposal_name)
    rows = proposal['optionalMd5Helpers']['entries']
    expected = {0x021f1e40: 44, 0x021f1e6c: 42, 0x021f1e98: 22, 0x021f1eb0: 22}
    assert len(rows) == 4 and {int(row['address'], 0): row['bytes'] for row in rows} == expected
    revision = '9e6aea5ee032dd24a884041a098b669534d88629'
    raw = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in raw.splitlines()]
    selected = {row['id']: row for row in ledger}
    intervals = list(spans([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(raw).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        intervals.extend(spans(read_json(path)))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw_data = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw_data).hexdigest()))
        intervals.extend(spans(json.loads(raw_data)[key]))
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256']
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert hashlib.sha256(image).hexdigest() == 'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'
    symbols_name = 'config/arm9/overlays/ov006/symbols.txt'
    assert sha256(ROOT / symbols_name) == 'f94081b2c914fe6f120e555b5b3ef7a1b048d20b1a90684e8425f81c90cebcc0'
    symbols = (ROOT / symbols_name).read_text(encoding='utf-8').splitlines()
    primary_name = 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-md5/md5c.c'
    assert sha256(ROOT / primary_name) == '84c3be9838f414cb4c080e6a99d247f084167c21d7680fe47d90f9027254eb5a'
    text = (ROOT / primary_name).read_text(encoding='utf-8-sig')
    assert all(re.search(r'static void ' + name + r'\s*\(', text) for name in ['Encode', 'Decode', 'MD5_memcpy', 'MD5_memset'])
    functions = []
    for row in rows:
        start, size = int(row['address'], 0), row['bytes']
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        current = selected[row['id']]
        assert current['bytes'] == size and current['mode'] == 'thumb'
        assert not current['states']['functionMatched'] and not current['sourceUnit']
        assert not any(max(start, a) < min(start + size, b) for a, b in intervals)
        canonical = f'func_ov006_{start:08x} kind:function(thumb,size=0x{size:x}) addr:0x{start:08x}'
        assert canonical in symbols
        for line in symbols:
            match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
            assert not match or not start < int(match[1], 0) < start + size
        assert hashlib.sha256(image[start - base:start - base + size]).hexdigest() == row['targetSha256']
        functions.append(dict(row, moduleSha256=hashlib.sha256(image).hexdigest(), canonicalInventoryRecord=canonical))
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/ov006-md5-helper-next'
    source_root = 'src/ov006/parallel_wave20261106/md5-helper-next'
    assert not folder.exists() and not (ROOT / source_root).exists()
    claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / claim_name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6mh', helperPrefix='wave20261106_ov006_md5_helper_next_', claimedFunctions=functions,
        noHistoricalClaimOwnershipInvented=True, completesImportedHelpersForMd5Packet=True,
        importedMd5CallersAndPaddingAdditionalCredit=0))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=claim_name,
        claimSha256=sha256(ROOT / claim_name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'), functions=4,
        initializedCandidateBytes=130, originalNativeAndStorageAdmissionGuardsRetained=True,
        sourceRevision=revision, proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)),
        freshPreviouslyUnownedStorageAndFunctionScopeAdmitted=True, allCohortSpecificationsExcluded=True,
        protectionPins=pins, completePrimarySource=dict(path=primary_name, sha256=sha256(ROOT / primary_name)),
        noOriginalClaimExpandedOrMutated=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=4, initializedCandidateBytes=130, sourceCredit=0))


if __name__ == '__main__':
    main()
