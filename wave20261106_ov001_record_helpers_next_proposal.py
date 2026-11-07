import hashlib
import json
import re
import struct
import subprocess
import match_runtime as C
from ndspy.codeCompression import decompress
from project import ROOT, read_json, write_json, sha256, configuration
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_ov000_controller_followup_readonly_scout import cfg_v2

REVISION = '966db0d2ea81f07a861df51addef602de548765e'
LANE = ROOT / 'evidence/lanes/parallel-wave20261106/ov001-record-helpers-next-proposal'
SELECTED = {
    0x021dbd3c:80,0x021dbd8c:112,0x021e2b1c:108,0x021f07dc:60,
    0x02218430:104,0x02218524:140,0x022189cc:136,
    0x02218c34:196,0x02218cf8:196,0x02223f20:40,
}


def blob(name):
    return subprocess.check_output(['git', 'show', REVISION + ':' + name], cwd=ROOT)


def discovered_paths():
    return sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
                  set((ROOT / 'evidence/lanes').rglob('data-claim.json')) |
                  set(ROOT.glob('cohort*-*specification.json')))


def namespace(row):
    return row.get('program') or '', row['processor'], row['module']


def main():
    expected = ROOT / 'evidence/lanes/parallel-wave20261106/ov001-record-helpers-next-proposal'
    if LANE.resolve() != expected.resolve() or LANE.exists():
        raise ValueError('Fresh exact read-only proposal scope required')
    ledger_raw = blob('ledger/functions.jsonl')
    ledger = [json.loads(line) for line in ledger_raw.splitlines()]
    manifest_raw = blob('manifest.json')
    module = next(m for m in json.loads(manifest_raw)['modules']
                  if (m.get('program') or '', m['processor'], m['name']) == ('', 'arm9', 'ov001'))
    image = (ROOT / module['binary']).read_bytes()
    base = int(module['base'], 0)
    assert C.sha(image) == module['sha256']
    cfg = configuration()
    assert sha256(cfg['rom']) == cfg['romSha256']
    rom = cfg['rom'].read_bytes()
    ovt, table_bytes = struct.unpack_from('<2I', rom, 0x50)
    entries = [struct.unpack_from('<8I', rom, at) for at in range(ovt, ovt + table_bytes, 32)]
    overlay = next(e for e in entries if e[0] == 1)
    assert overlay[1] == base and overlay[2] == len(image)
    assert overlay[3] == module['expectedBssBytes']
    fat = struct.unpack_from('<I', rom, 0x48)[0]
    file_begin, file_end = struct.unpack_from('<2I', rom, fat + 8 * overlay[6])
    encoded = rom[file_begin:file_end]
    decoded = decompress(encoded) if overlay[7] >> 24 & 1 else encoded
    assert decoded == image
    epoch = discovered_paths()
    pins, protect, git_pins = {}, [], []

    def pin(path):
        path = path.relative_to(ROOT).as_posix() if hasattr(path, 'relative_to') else path
        value = sha256(ROOT / path)
        if path in pins and pins[path] != value:
            raise ValueError('Observed input epoch change: ' + path)
        pins[path] = value

    def add(document, origin):
        protect.extend((a, b, origin) for program, cpu, name, a, b in intervals(document)
                       if (program, cpu, name) == ('', 'arm9', 'ov001'))

    add([r for r in ledger if r['states']['functionMatched'] or r.get('sourceUnit')],
        REVISION + ':ledger/functions.jsonl')
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = blob(name)
        add(json.loads(raw)[key], REVISION + ':' + name)
        git_pins.append(dict(gitObject=REVISION + ':' + name, sha256=C.sha(raw)))
    for path in epoch:
        raw = path.read_bytes()
        pins[path.relative_to(ROOT).as_posix()] = C.sha(raw)
        add(json.loads(raw), path.relative_to(ROOT).as_posix())
    symbols = 'config/arm9/overlays/ov001/symbols.txt'
    relocs = 'config/arm9/overlays/ov001/relocs.txt'
    for name in [module['binary'], symbols, relocs, __file__]:
        pin(ROOT / name if not hasattr(name, 'relative_to') else name)
    inventory = (ROOT / symbols).read_text().splitlines()
    relocation_paths = sorted((ROOT / 'config/arm9').rglob('relocs.txt'))
    all_records, symbolic_records = [], []
    for path in relocation_paths:
        pin(path)
        name = path.relative_to(ROOT).as_posix()
        match = re.search(r'/overlays/(ov\d+)/', name)
        source_module = match[1] if match else 'main' if path.parent.name == 'arm9' else path.parent.name
        for line in path.read_text().splitlines():
            record = re.fullmatch(r'from:(0x[0-9a-f]+) kind:(\S+) to:(0x[0-9a-f]+)(?: add:([+-]?0x[0-9a-f]+))? module:(\S+)', line)
            if re.fullmatch(r'from:0x[0-9a-f]+ kind:link_time_const\([^)]*\)', line):
                symbolic_records.append(dict(sourcePath=name, originalRecord=line))
                continue
            assert record or not line.startswith('from:'), ('Unparsed original relocation', name, line)
            if record:
                addend = int(record[4], 0) if record[4] else 0
                all_records.append((int(record[1], 0), int(record[3], 0), record[2], record[5],
                                    name, source_module, line, addend, (int(record[3], 0) + addend) & 0xffffffff))
    candidates = []
    for address, size in sorted(SELECTED.items()):
        row = next(r for r in ledger if namespace(r) == ('', 'arm9', 'ov001')
                   and r['mode'] == 'arm' and int(r['address'], 0) == address)
        assert row['bytes'] == size and not row['states']['functionMatched'] and not row.get('sourceUnit')
        body = image[address - base:address - base + size]
        assert C.sha(body) == row['inputBytesSha256']
        assert not [(a, b, origin) for a, b, origin in protect
                    if max(address, a) < min(address + size, b)]
        other_extents = [r['id'] for r in ledger if r['id'] != row['id']
                         and namespace(r) == ('', 'arm9', 'ov001') and r.get('bytes')
                         and max(address, int(r['address'], 0)) <
                         min(address + size, int(r['address'], 0) + r['bytes'])]
        assert not other_extents
        foreign = [r['address'] for r in ledger if namespace(r) == ('', 'arm9', 'ov001')
                   and address < int(r['address'], 0) < address + size]
        assert not foreign
        canonical = next((s for s in inventory if re.fullmatch(
            r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x' % (size, address), s)), None)
        assert canonical
        flow = cfg_v2(image, base, address, size)
        assert not flow['issues']
        code = {int(r['address'], 0) + i for r in flow['instructions'] for i in range(4)}
        literal = {int(r['address'], 0) + i for r in flow['literals'] for i in range(4)}
        assert not code & literal and code | literal == set(range(address, address + size))
        assert all(r['insideConfiguredExtent'] for r in flow['literals'])
        assert all(m['width'] == 4 and m['mnemonic'].startswith('ldr')
                   for m in flow['memory'] if m['baseRegister'] == 'pc')
        outgoing = [r[6] for r in all_records if r[4] == relocs and address <= r[0] < address + size]
        assert not any('module:(' in r for r in outgoing)
        incoming = [dict(sourceProgram='', sourceProcessor='arm9', sourceModule=r[5],
                         sourceMode='arm' if r[2].startswith('arm') else
                         'thumb' if r[2].startswith('thumb') else None,
                         targetNamespaceRecord=r[3], sourcePath=r[4], originalRecord=r[6],
                         targetBase=hex(r[1]), addend=r[7], effectiveTarget=hex(r[8]),
                         targetIsEntry=r[8] == address,
                         ambiguousOverlaySet=r[3].startswith('('))
                    for r in all_records if address <= r[8] < address + size
                    and (r[3] == 'overlay(1)' or r[3].startswith('(') and 'overlay(1)' in r[3])
                    and not (r[5] == 'ov001' and address <= r[0] < address + size)]
        assert not [r for r in incoming if not r['targetIsEntry']
                    and 'kind:arm_call ' in r['originalRecord']]
        historical = []
        for prefix in ['src', 'nonmatching']:
            process = subprocess.run(['rg', '--files', prefix, '-g', '*%08x*' % address],
                                     cwd=ROOT, capture_output=True, text=True)
            assert process.returncode in [0, 1]
            for name in process.stdout.splitlines():
                path = ROOT / name
                if path.is_file() and path.suffix.lower() in ['.c', '.cpp', '.h', '.s', '.json']:
                    pin(path)
                    historical.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        candidates.append(dict(program='', processor='arm9', module='ov001', mode='arm',
                               architecture='ARMv5TE', address=hex(address), bytes=size,
                               endExclusive=hex(address + size), binary=module['binary'],
                               base=base, inputModuleSha256=module['sha256'], targetSha256=C.sha(body),
                               canonicalInventoryRecord=canonical, originalRelocationRecords=outgoing,
                               originalIncomingRelocations=incoming, cfg=flow, instructionBytes=len(code),
                               literalBytes=len(literal), foreignInteriorEntries=[],
                               protectionIntersections=[], historicalArtifactPins=historical,
                               historicalLedgerStates=row['states'], sourceCredit=0,
                               semanticMeaning='Unproven game role; neutral record/field names required.'))
    helpers = []
    for helper_module, address in [('main', 0x0207afec), ('main', 0x0207b004),
                                   ('ov001', 0x021db438), ('ov001', 0x021db8d0)]:
        row = next(r for r in ledger if namespace(r) == ('', 'arm9', helper_module)
                   and r['mode'] == 'arm' and int(r['address'], 0) == address)
        assert row['states']['functionMatched'] and sha256(ROOT / row['sourceUnit']) == row['sourceSha256']
        pin(ROOT / row['sourceUnit'])
        for dependency in row.get('sourceDependencies', []):
            assert sha256(ROOT / dependency['path']) == dependency['sha256']
            pin(ROOT / dependency['path'])
        helpers.append(dict(program='', processor='arm9', module=helper_module, mode='arm',
                            address=hex(address), bytes=row['bytes'], source=row['sourceUnit'],
                            sourceSha256=row['sourceSha256'], acceptedEvidence=row['evidence'], bodyCredit=0))
    assert discovered_paths() == epoch
    assert sorted((ROOT / 'config/arm9').rglob('relocs.txt')) == relocation_paths
    assert all(sha256(ROOT / name) == value for name, value in pins.items())
    report = dict(
        status='read-only-ov001-record-helper-proposal-awaits-independent-admission',
        sourceCredit=0, sourceOwnershipGranted=False, compilerInvoked=False,
        sourceRevision=REVISION,
        sourceClosure='evidence/verification/cohort171-expanded-source-closure-20261101.json',
        functions=len(candidates), bytes=sum(SELECTED.values()),
        instructionBytes=sum(r['instructionBytes'] for r in candidates),
        literalBytes=sum(r['literalBytes'] for r in candidates),
        namespace=dict(program='', processor='arm9', module='ov001', mode='arm'),
        originalRawRomOverlay=dict(romSha256=cfg['romSha256'], overlayTableOffset=ovt,
                                   record=list(overlay), fatFileId=overlay[6], fileStart=file_begin,
                                   fileEnd=file_end, encodedSha256=C.sha(encoded),
                                   decompressedSha256=C.sha(decoded), initializedBytes=len(image),
                                   bssBytes=overlay[3]),
        candidates=candidates, actualAcceptedHelperEvidence=helpers,
        pendingCallerWitnesses=[dict(path=name,sha256=sha256(ROOT/name),sharedAcceptedCredit=0)for name in[
            'evidence/lanes/parallel-wave20261106/ov001-large-controller-next/first/ready.json',
            'evidence/lanes/parallel-wave20261106/ov001-large-controller-next/second/ready.json']],
        nonNumericOriginalRelocationRecords=symbolic_records,
        measuredInterfaceFacts=[
            'Accepted main0207afec returns *(u32*)(021c6744+4)+index*40. Storage ownership and game semantics remain uncredited.',
            'Accepted main0207b004 returns whether the 32-bit word at that same record+0 intersects its second-argument mask. It is a flag predicate, not a count helper.',
            'Accepted ov001021db438 selects four independent overlay(1) BSS banks and up to three slots at stride0x440. Exact main/ov001 namespaces remain separate.',
            'Accepted ov001021db8d0 checks a nullable record pointer, byte+0x31c, byte+0x1ff, then pointer+0x1e8 and child byte+0xac; broader status meanings remain unknown.',
            'These ten helpers are original direct ARM callees of the admitted record/status/controller family. Native whole spans and their actual primitive/field/call widths ground a measured-C proposal; no original implementation C or semantic SDK name is claimed.',
        ],
        priorAttemptInventory=dict(
            search='rg --files src/nonmatching -g *<8hex>* for each selected identity; files actually read/pinned below.',
            candidatesWithFilenameHistory=[r['address'] for r in candidates if r['historicalArtifactPins']],
            observedDraftsAreUnaccepted=True,
            limits='Filename absence does not prove untouched; ledger drafted=false is preserved alongside two actually present older decompiler drafts. No prior profile/compile result is inferred.'),
        protectionInputPins=[dict(path=name, sha256=value) for name, value in sorted(pins.items())],
        gitPins=git_pins + [dict(gitObject=REVISION + ':ledger/functions.jsonl', sha256=C.sha(ledger_raw)),
                            dict(gitObject=REVISION + ':manifest.json', sha256=C.sha(manifest_raw))],
        limits=[
            'Read-only proposal only: no reconstruction source, compiler, claim, registry, dispatch, preference, index, original helper, Ready or shared output changes.',
            'All current/historical claims, actual root cohort specifications, accepted/source code, data/linkage physical spans and every other configured native extent were excluded without relying on mode differences.',
            'Original incoming/outgoing relocation records retain their actual source module and target qualifier; ambiguous incoming overlay sets remain explicit and are not resolved by numeric address.',
            'MW2.0/base O2/off/speed/C99 is the whole-byte-measured nearby-controller baseline; these helpers require fresh full native/link/ABI/model/wrong-C/copied-root proof. Provider prototypes and imported bodies remain zero credit.',
            'Root must independently refresh ownership, raw boundaries and every protection before source admission. Game meanings, original version and physical game execution remain unproven.',
        ])
    LANE.mkdir()
    write_json(LANE / 'proposal.json', report)
    print(dict(functions=report['functions'], bytes=report['bytes'],
               instructionBytes=report['instructionBytes'], literalBytes=report['literalBytes'],
               priorDrafts=report['priorAttemptInventory']['candidatesWithFilenameHistory'],
               sha256=sha256(LANE / 'proposal.json')), flush=True)


if __name__ == '__main__':
    main()
