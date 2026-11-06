import hashlib
import json
import struct
import subprocess
from project import ROOT, configuration, read_json, write_json, sha256, now
from admit_arm7_wm_residual_resumption_v1_20261106 import independently_close


def spans(node, parent=None):
    parent = parent or {}
    if isinstance(node, list):
        for item in node:
            yield from spans(item, parent)
    elif isinstance(node, dict):
        context = {key: node.get(key, parent.get(key)) for key in ['program', 'processor', 'module']}
        cpu = context['processor'] or ('arm7' if 'arm7' in (context['module'] or '') else 'arm9')
        if (context['program'] or '', cpu, context['module']) == ('', 'arm7', 'arm7-wram'):
            size = node.get('storedBytes', node.get('bytes', node.get('size')))
            if node.get('address') and size:
                start = int(node['address'], 0) if isinstance(node['address'], str) else node['address']
                if isinstance(size, str):
                    size = len(bytes.fromhex(size)) if 'instruction' in node else int(size, 0)
                assert type(size) is int and size > 0
                yield start, start + size
        for item in node.values():
            yield from spans(item, context)


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/arm7-sdk-next-proposal/proposal.json'
    assert sha256(ROOT / proposal_name) == '09650eda436cf0e8522d53ce2e0c893283f535117dff8a7951e37005a36bc7e4'
    proposal = read_json(ROOT / proposal_name)
    expected = {0x038048e0: 320, 0x03804a20: 352, 0x03804b80: 68, 0x03804bc4: 60,
                0x03804fbc: 420, 0x0380516c: 288, 0x038052fc: 48, 0x0380532c: 164}
    rows = [row for row in proposal['candidates'] if int(row['address'], 0) in expected]
    assert len(rows) == 8 and {int(row['address'], 0): row['bytes'] for row in rows} == expected
    revision = '142f10ae8d094bf5ae27dc09a017b6ba3a19adeb'
    content = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in content.splitlines()]
    protected = list(spans([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(content).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        protected.extend(spans(read_json(path)))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw).hexdigest()))
        protected.extend(spans(json.loads(raw)[key]))
    for pin in proposal['primaryC']['completeUnmodifiedFiles']:
        data = (ROOT / pin['path']).read_bytes()
        assert sha256(ROOT / pin['path']) == pin['sha256'] and len(data) == pin['bytes']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == pin['gitBlobSha1']
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']; rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]
    assert struct.unpack_from('<3I', raw, 160024) == (0x037f8000, 63096, 15980)
    image, base = raw[540:63636], 0x037f8000
    assert image == (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    assert hashlib.sha256(image).hexdigest() == 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
    import link_arm7_bulk_20261030 as original
    modules, functions = original.namespace(''); reviews, claimed = [], []
    for row in rows:
        start, size = int(row['address'], 0), row['bytes']
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm7', 'arm7-wram', 'arm')
        assert row['eligibleForIndependentBoundaryAdmission'] and not row['foreignInteriorEntries']
        assert not any(max(start, a) < min(start + size, b) for a, b in protected)
        assert start in functions and functions[start]['module'] == 'arm7-wram' and functions[start]['mode'] == 'arm'
        assert not any(start < address < start + size for address, item in functions.items() if item['module'] == 'arm7-wram')
        adapted = dict(row, historicalClaimedBytes=size, entryReachableBytes=row['entryReachableInstructionBytes'],
            literalReadBytes=row['actualLiteralReadBytes'], computedEvidenceSha256=row['nativeSpanSha256'],
            currentHistoricalNativeSpanSha256=row['nativeSpanSha256'])
        review = independently_close(adapted, image, base); reviews.append(review)
        claimed.append(dict(program='', processor='arm7', module='arm7-wram', mode='arm', architecture='ARMv4T',
            address=hex(start), bytes=size, targetSha256=review['nativeSpanSha256'], physicalFlow=row['flow'],
            base=base, binary='extract/arm7/runtime/arm7-wram.bin', inputModuleSha256=hashlib.sha256(image).hexdigest()))
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/arm7-pm-next'; source_root = 'src/arm7/parallel_wave20261106/pm-next'
    assert not folder.exists() and not (ROOT / source_root).exists() and not (ROOT / 'work/w6pm').exists()
    assert not list(ROOT.glob('wave20261106_arm7_pm_next_*.py'))
    name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / name, dict(owner='repo_audit', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6pm', helperPrefix='wave20261106_arm7_pm_next_', claimedFunctions=claimed,
        perFunctionSourceNamesRemainHypotheses=True, micAndBlockedSwitchCandidatesNotAdmitted=True))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=name,
        claimSha256=sha256(ROOT / name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        functions=8, initializedCandidateBytes=1720, sourceRevision=revision,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), protectionPins=pins,
        independentOriginalEntryCfgAndEveryLiteralOriginWidthValue=reviews,
        noHistoricalOwnershipProjectionOrDataStorageCredit=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=8, initializedCandidateBytes=1720, sourceCredit=0))


if __name__ == '__main__':
    main()
