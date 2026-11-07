import hashlib
import json
import re
import subprocess

import match_runtime
from project import ROOT, configuration, now, read_json, sha256, write_json
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_child_arm9_boundary_family_readonly_v4 import derive
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection


def main():
    name = 'evidence/lanes/parallel-wave20261106/overlay-strict-reuse-scout/proposal.json'
    assert sha256(ROOT / name) == 'a19cf85e39921027ba84e5dd574bd908d83494493ad125a6f1459eca6c2f4197'
    proposal = read_json(ROOT / name)
    for pin in proposal['pins']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    revision = '0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
    baseline = [json.loads(line) for line in subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT).splitlines()]
    current = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines()]
    protected = list(intervals([r for r in current if r['states']['functionMatched'] or r.get('sourceUnit')]))
    pins = []
    for path in sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) | set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json'))):
        protected.extend(intervals(read_json(path))); pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    for path, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        protected.extend(intervals(read_json(ROOT / path)[key])); pins.append(dict(path=path, sha256=sha256(ROOT / path)))
    config = configuration(); assert sha256(config['rom']) == config['romSha256']
    from ndspy.rom import NintendoDSRom
    rom = NintendoDSRom(config['rom'].read_bytes()); overlays = rom.loadArm9Overlays([3, 6])
    claimed = []; reviews = []
    for entry in proposal['entries']:
        identity = entry['identity']; module = identity['module']; number = int(module[2:]); start = int(identity['address'], 0); size = identity['bytes']
        assert (module, start, size) in [('ov003', 0x021dea38, 192), ('ov006', 0x021dd434, 140)]
        assert not any((p, c, m) == ('', 'arm9', module) and max(a, start) < min(b, start + size) for p, c, m, a, b in protected)
        original = next(r for r in current if (r.get('program') or '', r['processor'], r['module'], int(r['address'], 0)) == ('', 'arm9', module, start))
        assert not original['states']['functionMatched'] and not original.get('sourceUnit') and original['bytes'] == size
        overlay = overlays[number]; image = bytes(overlay.data); base = overlay.ramAddress
        assert base == identity['base'] and image == (ROOT / identity['binary']).read_bytes()
        assert hashlib.sha256(image).hexdigest() == identity['inputModuleSha256']
        body = image[start - base:start - base + size]; assert hashlib.sha256(body).hexdigest() == identity['targetSha256']
        symbols = (ROOT / f'config/arm9/overlays/{module}/symbols.txt').read_text(encoding='utf-8').splitlines()
        assert entry['canonicalInventoryRecord'] in symbols
        starts = {int(m[1], 0) for line in symbols if (m := re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)', line))}
        assert not any(start < address < start + size for address in starts)
        flow = derive(image, base, start, min(a for a in starts if a > start), 'arm', {(a, 'arm') for a in starts})
        assert flow == entry['nativeOnlyCfgLiteralReturnProof'] and flow['complete'] and flow['bytes'] == size
        assert all(e['originalEntryLRProven'] and e['stackDelta'] == 0 for e in flow['exits'])
        outgoing = [line for line in (ROOT / f'config/arm9/overlays/{module}/relocs.txt').read_text(encoding='utf-8').splitlines() if (m := re.match(r'from:(0x[0-9a-fA-F]+)', line)) and start <= int(m[1], 0) < start + size]
        assert outgoing == [r['record'] for r in entry['originalOutgoingRecords']]
        incoming = []
        for path in sorted((ROOT / 'config/arm9').rglob('relocs.txt')):
            for line in path.read_text(encoding='utf-8').splitlines():
                m = re.search(r' to:(0x[0-9a-fA-F]+) module:(.+)$', line)
                if m and (int(m[1], 0) & ~1) == start and f'overlay({number})' in m[2]:
                    assert m[2] == f'overlay({number})'
                    incoming.append((path.relative_to(ROOT).as_posix(), line))
        assert incoming == [(r['sourcePath'], r['record']) for r in entry['allConfiguredIncomingReferences']]
        origin = entry['acceptedOrdinaryCOrigin']
        accepted = next(r for r in baseline if (r.get('program') or '', r['processor'], r['module'], int(r['address'], 0)) == ('', 'arm9', origin['module'], int(origin['address'], 0)))
        assert accepted['states']['functionMatched'] and accepted['bytes'] == size and accepted['sourceSha256'] == origin['sourceSha256']
        assert sha256(ROOT / origin['source']) == origin['sourceSha256'] and sha256(ROOT / origin['object']) == origin['objectSha256']
        with (ROOT / origin['object']).open('rb') as stream:
            elf = ELFFile(stream); table = elf.get_section_by_name('.symtab'); symbol = table.get_symbol_by_name(origin['functionSymbol'])[0]
            assert symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == size
            section_id = symbol['st_shndx']; section = elf.get_section(section_id); offset = symbol['st_value'] - section['sh_addr']
            assert section['sh_flags'] & 4
            mappings = sorted((s['st_value'], s.name[1]) for s in table.iter_symbols() if s['st_shndx'] == section_id and s.name.startswith(('$a', '$t', '$d')) and s['st_value'] <= symbol['st_value'])
            assert mappings[-1][1] == 'a'
            compiled = bytearray(section.data()[offset:offset + size]); native = bytearray(body); relocations = []
            for sec in elf.iter_sections():
                if not isinstance(sec, RelocationSection) or sec['sh_info'] != section_id: continue
                for relocation in sec.iter_relocations():
                    relative = relocation['r_offset'] - offset
                    if 0 <= relative < size:
                        assert relocation['r_info_type'] in (1, 2) and relative % 4 == 0 and relative + 4 <= size
                        relocations.append(dict(offset=relative, type=relocation['r_info_type']))
                        compiled[relative:relative + 4] = bytes(4); native[relative:relative + 4] = bytes(4)
            assert relocations == entry['actualUnchangedObjectDeclaredRelocations'] and compiled == native
        claimed.append(dict(identity, id=original['id'], originalRelocationRecords=outgoing, originalIncomingRecords=entry['allConfiguredIncomingReferences']))
        reviews.append(dict(identity=identity, independentlyDerivedNativeFlow=flow, actualAcceptedSourceOrigin=origin, allNonrelocationBytesEqual=True, relocationWordsMasked=len(relocations)))
    assert len(claimed) == 2 and sum(r['bytes'] for r in claimed) == 332
    assert all(sha256(ROOT / p['path']) == p['sha256'] for p in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/overlay-strict-reuse-next'
    assert not folder.exists() and not (ROOT / proposal['proposedSourceRoot']).exists() and not (ROOT / proposal['proposedWorkRoot']).exists()
    assert not list(ROOT.glob(proposal['proposedHelperPrefix'] + '*.py'))
    claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / claim_name, dict(owner='workflow_research', status='coordinator-admitted-source-scope-no-credit', sourceCredit=0, createdUtc=now(),
        exclusiveSourceRoot=proposal['proposedSourceRoot'], exclusiveWorkRoot=proposal['proposedWorkRoot'], helperPrefix=proposal['proposedHelperPrefix'], claimedFunctions=claimed,
        experimentBudget='Actual accepted profiles only. Preserve explicit modulo32 shifts, s16 widths and measured data imports. Proper call prototypes, genuine links, models, negatives and copied-root proof before Ready; no helper or storage credit.'))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, functions=2, initializedCandidateBytes=332, claim=claim_name, claimSha256=sha256(ROOT / claim_name),
        exclusiveSourceRoot=proposal['proposedSourceRoot'], sharedDispatchUnchanged=True, actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        proposal=dict(path=name, sha256=sha256(ROOT / name)), protectionPins=pins, independentReviews=reviews, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=2, bytes=332, sourceCredit=0))


if __name__ == '__main__': main()
