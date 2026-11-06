import gzip
import hashlib
import json
import struct
import ov001_default770_machine_20261101 as D
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module
from ndspy.rom import NintendoDSRom
F = D.F

def case(main, save, base, overlay, blobs, equip, raw, skill, points, seed, post=None, supplied202=False):
    vector = dict(seed=770, pool=1000, species=1, level=1, plus=0, variant=0, skills=1, skillPoints=0, invalid=0, ioSuccess=True, priorProgress=0, ordinal=0)
    m = D.Machine(main, save, base, overlay, int(supplied202))
    m.blobs = blobs
    rows = F.setup(m.u, blobs, vector)
    m.u.mem_write(39059456, blobs['ActTbl.bin'])
    m.word(35415876, 39059456)
    m.word(35415880, 39059464)
    m.u.mem_write(39124992, equip[8:])
    m.word(35417076, 39124992)
    for row in rows:
        address = F.ROSTER + row['index'] * 132
        m.u.mem_write(address + 32, struct.pack('<8h', 100, 90, 80, 70, 60, 50, 40, 30))
        m.u.mem_write(address + 51, bytes([raw]))
        m.u.mem_write(address + 122, bytes([skill, points]))
        row['record'] = bytes(m.u.mem_read(address, 132))
    m.invoke('supplied-seed-native-setter', 33805036, [seed])
    m.invoke('native-runtime-clear', 33966456)
    mappings = []
    for index, view in enumerate(D.VIEWS):
        record = F.ROSTER + index * 132
        if m.invoke('native-record-constructor-' + str(index), 33966588, [view, record, 0]) != 1:
            raise ValueError('770 native constructor rejected supported synthetic record')
        if m.u.mem_read(view + 514, 1)[0] != 0 or m.u.mem_read(view + 303, 1)[0] != raw:
            raise ValueError('770 native view field provenance differs')
        if supplied202:
            m.u.mem_write(view + 514, b'\x01')
        mappings.append(dict(index=index, record=hex(record), view=hex(view), view202=int(supplied202), nativeView12f=raw, actualFeatureBytes=list(m.u.mem_read(view + 74, 8))))
    for team in [0, 2]:
        if m.invoke('native-default-modifier-formation-' + str(team), 35495792, [team]) != 3:
            raise ValueError('770 native formation count differs')
    for row in rows[:6]:
        row['actor'] = bytes(m.u.mem_read(row['actorAddress'], 1088))
        if row['actor'][511] != raw or row['actor'][796] != 1:
            raise ValueError('770 actual formation actor provenance differs')
    if len(m.flag202Writes) != 6 or any((v['stage'] != 'native-runtime-clear' or v['byteValue'] != 0 for v in m.flag202Writes)):
        raise ValueError('770 default-path provenance has an unexpected modifier flag writer')
    afterFormation = m.read_word(34562116)
    formationProviders = len(m.providers_seen)
    if formationProviders:
        raise ValueError('770 construction/formation unexpectedly supplied a service')
    if post is not None:
        for row in rows:
            address = F.ROSTER + row['index'] * 132
            m.u.mem_write(address + 51, bytes([post]))
            row['record'] = bytes(m.u.mem_read(address, 132))
    m.u.mem_write(35884956 + 9, b'\x7f' * 4)
    m.u.mem_write(F.CONTEXT + 4, b'\r')
    m.u.mem_write(F.CONTEXT + 22, b'\x01')
    m.u.mem_write(F.CONTEXT + 37, b'\x00')
    anticipated = {a: F.expected(a, rows, blobs, vector) for a in [35539408, 35539764, 35540020]}
    m.invoke('ordinary-reward-dispatch', 35546536)
    for address, (result, outcomes) in anticipated.items():
        F.check_rows(m.u, address, rows, outcomes)
        actual = [e['result'] for e in m.returned if e['stage'] == 'ordinary-reward-dispatch' and e['address'] == hex(address)]
        if actual != [result]:
            raise ValueError(('770 independent reward count/record model differs', hex(address), actual, result))
    phase = m.u.mem_read(F.CONTEXT + 4, 1)[0]
    if phase != (14 if anticipated[35539408][0] else 15):
        raise ValueError('770 native parent phase differs')
    if m.read_word(34562116) != afterFormation:
        raise ValueError('770 reward phase consumed unexpected RNG')
    entries = [e['address'] for e in m.events if e['stage'] == 'ordinary-reward-dispatch']
    if raw and '0x21e485c' in entries:
        raise ValueError('770 construction-blocked actor reached growth')
    watchedTop = sum((1 for e in m.returned if any((s['stage'] == e['stage'] and s['address'] == e['address'] for s in m.stages))))
    finalRows = [dict(index=r['index'], record33=m.u.mem_read(F.ROSTER + r['index'] * 132 + 51, 1)[0], recordExperience=m.read_word(F.ROSTER + r['index'] * 132 + 52), actor1ff=m.u.mem_read(r['actorAddress'] + 511, 1)[0] if r['actorAddress'] else None, actorExperience=m.read_word(r['actorAddress'] + 512) if r['actorAddress'] else None) for r in rows]
    return dict(counterfactualSupplied202=bool(supplied202), host202Stores=6 if supplied202 else 0, initialRaw33=raw, rewardRaw33=raw if post is None else post, skillId=skill, allocatedPoints=points, suppliedSeed=seed, seedAfterFormation=afterFormation, seedAfterReward=m.read_word(34562116), actualTopReturns=len(m.stages), watchedReturnsIncludingTops=len(m.returned), watchedTopReturns=watchedTop, watchedChildReturns=len(m.returned) - watchedTop, actualNativeRngReturns=len(m.rngResults), formationProviders=formationProviders, providedRewardCalls=len(m.providers_seen), hardwareDivisionSubstitutions=m.division_total, actualStageReturns=m.stages, nativeMappings=mappings, native202Writes=m.flag202Writes, statModels=m.statResults, rngReturns=m.rngResults, nativeEvents=m.events, nativeWatchedReturns=m.returned, providedBoundaries=m.providers_seen, record33Reads=m.reads, finalRows=finalRows, finalPhase=phase, nativeInstructions=m.instructions, nativeFunctions=[dict(address=hex(a), bytes=b - a, module=module, mode=mode, instructions=n) for (a, b, module, mode), n in sorted(m.pc_counts.items())], instructionTraceSha256=m.pc_digest.hexdigest(), writesSha256=hashlib.sha256(json.dumps(m.all_writes, separators=(',', ':')).encode()).hexdigest(), ramSha256=hashlib.sha256(bytes(m.u.mem_read(33554432, 8388608))).hexdigest())

def main():
    arm, save, base = F.inputs()
    rom = NintendoDSRom((ROOT / 'inputs/game.nds').read_bytes())
    blobs = F.assets()
    blobs['ActTbl.bin'] = bytes(rom.getFileByName('ActTbl.bin'))
    equip = bytes(rom.getFileByName('EquipTbl.bin'))
    _, overlay, _ = measured_module('ov001')
    vectors = [(raw, skill, points, seed, None) for raw in [0, 255] for skill, points in [(1, 0), (47, 100)] for seed in [0, 4294967295]] + [(0, 47, 100, 305419896, 255), (255, 47, 100, 305419896, 0), (0, 47, 100, 0, None, True), (255, 47, 100, 0, None, True)]
    rows = []
    for values in vectors:
        row = case(arm, save, base, overlay, blobs, equip, *values)
        rows.append(row)
        print(values, row['actualTopReturns'], row['watchedReturnsIncludingTops'], row['actualNativeRngReturns'], row['finalPhase'], flush=True)
    for raw33 in [0, 255]:
        pair = [r for r in rows if r['initialRaw33'] == raw33 and r['rewardRaw33'] == raw33 and (r['skillId'] == 47) and (r['suppliedSeed'] == 0)]
        if len(pair) != 2 or sorted((r['actualNativeRngReturns'] for r in pair)) != [0, 36]:
            raise ValueError('770 explicit modifier-flag counterfactual differs')
    raw = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/application/ov001-default770-full-traces-20261101.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, scope='original-native construction, default-modifier formation and bounded reward dispatch with supplied records/seed/parent phase', buildSha256=sha256(ROOT / 'inputs/game.nds'), module='ov001', processor='arm9', program='', mode='arm', moduleSha256=hashlib.sha256(overlay).hexdigest(), generatorSha256=sha256(ROOT / 'probe_ov001_default770_20261101.py'), machineSha256=sha256(ROOT / 'ov001_default770_machine_20261101.py'), cases=len(rows), actualTopReturns=sum((r['actualTopReturns'] for r in rows)), watchedReturnsIncludingTops=sum((r['watchedReturnsIncludingTops'] for r in rows)), watchedTopReturns=sum((r['watchedTopReturns'] for r in rows)), watchedChildReturns=sum((r['watchedChildReturns'] for r in rows)), actualNativeRngReturns=sum((r['actualNativeRngReturns'] for r in rows)), formationProviders=sum((r['formationProviders'] for r in rows)), providedRewardCalls=sum((r['providedRewardCalls'] for r in rows)), hardwareDivisionSubstitutions=sum((r['hardwareDivisionSubstitutions'] for r in rows)), fullTraces=dict(path=str(path.relative_to(ROOT)).replace('\\', '/'), sha256=sha256(path), uncompressedSha256=hashlib.sha256(raw).hexdigest()), caseSummaries=[{k: r[k] for k in ['counterfactualSupplied202', 'host202Stores', 'initialRaw33', 'rewardRaw33', 'skillId', 'allocatedPoints', 'suppliedSeed', 'seedAfterFormation', 'actualNativeRngReturns', 'finalPhase', 'finalRows']} for r in rows], inputHashes=dict(originalSave=hashlib.sha256(save).hexdigest(), main=hashlib.sha256(arm).hexdigest(), assets={name: hashlib.sha256(blob).hexdigest() for name, blob in sorted(blobs.items())}, EquipTbl=hashlib.sha256(equip).hexdigest()), roles=dict(active=[0, 1, 2], reserve=[3, 4, 5], stored=[6, 7]), supportedFields=dict(record33='u8 saved-record+0x33, supplied', view12f='u8 runtime-view+0x12F, native copied', view202='u8 runtime-view+0x202, native clear0; explicit supplied1 counterfactual only', actor1ff='u8 actor+0x1FF, native copied', actor31c='u8 actor+0x31C, native formation ready', phase='u8 context+0x04, supplied0x0D', selector='u8 context+0x16, supplied1', seed='u32 main0x020F6044, supplied through original0x0203D2EC'), limits=['Synthetic species1 level1 records, explicit base stats, skill allocation and seed; no live scene or current RNG value inferred.', 'Native construction and formation have zero providers; reward UI, input/frame and bounded original-file threshold IO are supplied.', 'Actual RNG returns are a subset of watchedChildReturns and are not added again.', 'Record33/actor1FF/feature IDs retain raw meanings; post-construction edits distinguish actor cache from stored-record reads.', 'The actual clear to view202=0 is proven for this constructor/formation path only; later writers and scene lifecycle remain unresolved.', 'No decompiled source, source-byte credit, emulator/device execution, application changes or persistence claim.'], allPassed=True)
    chosen = {33804948, 33805036, 33966456, 33966588, 35494404, 35495580, 35495792, 35502288, 35539036, 35539408, 35539764, 35540020, 35540656, 35546536}
    modules = {'main': measured_module('main'), 'ov001': measured_module('ov001')}
    report['nativeRegions'] = []
    for start, end, module, mode in F.functions()[1]:
        if start not in chosen:
            continue
        info, blob, _ = modules[module]
        baseAddress = info['address'] if 'address' in info else info['base'] if 'base' in info else info['loadAddress']
        if isinstance(baseAddress, str):
            baseAddress = int(baseAddress, 0)
        report['nativeRegions'].append(dict(buildSha256=report['buildSha256'], processor='arm9', program='', module=module, moduleSha256=hashlib.sha256(blob).hexdigest(), mode=mode, address=hex(start), bytes=end - start, nativeSpanSha256=hashlib.sha256(blob[start - baseAddress:end - baseAddress]).hexdigest()))
    report['addresses'] = {'savedRecords': hex(F.ROSTER), 'activeActors': hex(F.ACTIVE), 'reserveActors': hex(F.RESERVE), 'rewardContext': hex(F.CONTEXT), 'runtimeViews': [hex(v) for v in D.VIEWS]}
    report['runtime'] = dict(python=F.platform.python_version(), unicorn=F.unicorn_version, cpu='ARM946', nativeInstructionBoundPerCase=1000000, nativeInstructionBoundPerTop=800000)
    report['nativeCounterfactualControls'] = 2
    report['returningWrongCompiledControls'] = 0
    report['sourceCandidateExecuted'] = False
    write_json(ROOT / 'evidence/application/ov001-default770-native-context-20261101.json', report)
    print('ALL', report['actualTopReturns'], report['watchedReturnsIncludingTops'], report['actualNativeRngReturns'])
if __name__ == '__main__':
    main()
