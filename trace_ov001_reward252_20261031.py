import bisect
import hashlib
import json
import platform
import struct
import sys
from pathlib import Path
import match_runtime
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module
sys.path.insert(0, str(ROOT / 'evidence/application'))
from preparation_machine_20261029 import Machine, inputs, REGS, STOP, STACK
from ndspy.rom import NintendoDSRom
from ov001_award_cases_20261029 import assets, setup, expected, CONTEXT, ROSTER, ACTIVE, RESERVE
from ov001_award_fixture_20261029 import functions, check_rows
from unicorn import __version__ as unicorn_version, Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_CPU_ARM_946
UI = {35680680, 35680720, 35680372, 35680760, 33728052, 33833852, 33833884}
RESOURCE = 33728536
WATCH = {33966456, 33966588, 35495792, 35495580, 35494404, 35502288, 35546536, 35540656, 35730992, 35592772, 35539408, 35539036, 35540020, 35539764, 35539652, 35539708, 33804948}

class TraceMachine(Machine):

    def __init__(self, arm, save, blobs, overlay):
        self.events = []
        self.reads = []
        self.frames = []
        self.returned = []
        self.pc_counts = {}
        self.stages = []
        self.providers_seen = []
        self.instructions = 0
        self.all_writes = []
        self.pc_digest = hashlib.sha256()
        self.division_total = 0
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(33554432, 8388608)
        self.u.mem_map(67108864, 4096)
        self.u.mem_write(33554432, arm)
        for start, end, destination in [(144, 14952, 35378460), (14952, 15004, 35364532), (15004, 23872, 35369592), (23872, 28880, 35364584)]:
            self.u.mem_write(destination, save[start:end])
        for address, name, skip in [(38797312, 'EnmyKindTbl.bin', 8), (38862848, 'SkillTbl.bin', 0), (38928384, 'FeatTbl.bin', 0), (38993920, 'ItemTbl.bin', 8)]:
            self.u.mem_write(address, blobs[name][skip:])
        for address, value in [(34564592, 38797312), (35415868, 38862848), (35415872, (len(blobs['SkillTbl.bin']) - 8) // 60), (35415888, 38928384), (35415892, 38928392), (35400372, 38993920)]:
            self.word(address, value)
        self.trace, self.writes, self.divisions, self.pending = ([], [], [], {})
        self.providers = {}
        self.calls = 0
        self.u.hook_add(UC_HOOK_CODE, self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)
        self.u.hook_add(UC_HOOK_MEM_READ, self.divide)
        self.u.mem_write(35484224, overlay)
        self.starts, self.ranges = functions()
        self.blobs = None
        self.stage = None
        self.u.hook_add(UC_HOOK_CODE, self.trace_code)
        self.u.hook_add(UC_HOOK_MEM_READ, self.trace_read)

    def write(self, uc, access, address, size, value, data):
        if not (33554432 <= address and address + size <= 41943040 or (67109504 <= address and address + size <= 67109568)):
            raise ValueError(('Reward252 native write outside private RAM/divider', hex(address)))
        self.all_writes.append((self.stage, address, size, value))

    def finish_frames(self, pc):
        while self.frames and pc == self.frames[-1]['returnAddress']:
            frame = self.frames.pop()
            if self.u.reg_read(UC_ARM_REG_SP) != frame['sp'] or [self.u.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Reward252 actual native frame differs')
            event = dict(stage=self.stage, address=hex(frame['address']), result=self.u.reg_read(REGS[0]))
            if frame['address'] == 35502288 and event['result'] != frame['expectedEligibility']:
                raise ValueError('Reward252 independent native eligibility predicate differs')
            if frame['address'] == 35495580:
                event['actor1ffAfter'] = self.u.mem_read(frame['actor'] + 511, 1)[0]
            self.returned.append(event)

    def trace_code(self, uc, pc, width, data):
        self.finish_frames(pc)
        self.instructions += 1
        self.pc_digest.update(struct.pack('<I', pc))
        if self.instructions > 1000000:
            raise ValueError('Reward252 total instruction bound exceeded')
        mode = 'thumb' if uc.reg_read(UC_ARM_REG_CPSR) & 32 else 'arm'
        if pc in UI or pc == RESOURCE:
            if mode != 'arm':
                raise ValueError('Reward252 provider target mode differs')
            args = [uc.reg_read(r) for r in REGS[:4]]
            if pc == RESOURCE:
                name, destination, length, offset = args
                if bytes(uc.mem_read(name, 15)) != b'LevelUpTbl.bin\x00' or destination != 35364508 or length != 4 or offset % 4 or (offset + 4 > len(self.blobs['LevelUpTbl.bin'])):
                    raise ValueError('Reward252 bounded original threshold IO differs')
                uc.mem_write(destination, self.blobs['LevelUpTbl.bin'][offset:offset + 4])
                result = 1
                event = dict(stage=self.stage, address=hex(pc), scope='original-ROM-file-IO-substitution', offset=offset, length=length, fileSha256=hashlib.sha256(self.blobs['LevelUpTbl.bin']).hexdigest())
            else:
                result = 39845888 if pc == 33728052 else 0
                event = dict(stage=self.stage, address=hex(pc), scope='input-reference-provider' if pc == 33728052 else 'battle-frame-update-provider' if pc in [33833852, 33833884] else 'UI-provider', arguments=args)
            self.providers_seen.append(event)
            for k in [1, 2, 3, 12]:
                uc.reg_write(REGS[k], 3774873600 + k * 257)
            uc.reg_write(REGS[0], result)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        index = bisect.bisect_right(self.starts, pc) - 1
        if index < 0 or not self.ranges[index][0] <= pc < self.ranges[index][1]:
            raise ValueError(('Reward252 escaped measured function inventory', hex(pc)))
        entry = self.ranges[index]
        if entry[3] != mode:
            raise ValueError(('Reward252 native target mode differs', hex(pc), entry))
        self.pc_counts[entry] = self.pc_counts.get(entry, 0) + 1
        if pc in WATCH:
            args = [uc.reg_read(r) for r in REGS[:4]]
            event = dict(stage=self.stage, address=hex(pc), arguments=args, mode=mode)
            if pc == 35502288:
                actor = args[0]
                descriptor = self.read_word(actor + 488)
                event.update(ready31c=uc.mem_read(actor + 796, 1)[0], raw1ff=uc.mem_read(actor + 511, 1)[0], descriptor=hex(descriptor), rawDescriptorAC=uc.mem_read(descriptor + 172, 1)[0])
            self.events.append(event)
            self.frames.append(dict(address=pc, returnAddress=uc.reg_read(UC_ARM_REG_LR) & ~1, sp=uc.reg_read(UC_ARM_REG_SP), preserved=[uc.reg_read(r) for r in REGS[4:12]], actor=args[0], expectedEligibility=int(bool(event.get('ready31c')) and (not event.get('raw1ff')) and (not event.get('rawDescriptorAC')))))

    def trace_read(self, uc, access, address, size, value, data):
        for index in range(8):
            target = ROSTER + index * 132 + 51
            if address <= target < address + size:
                self.reads.append(dict(stage=self.stage, pc=hex(uc.reg_read(UC_ARM_REG_PC)), recordIndex=index, field='record33', value=uc.mem_read(target, 1)[0]))

    def invoke(self, stage, address, args=()):
        self.stage = stage
        try:
            result = self.call(address, args, limit=800000)
        except Exception as error:
            write_json(ROOT / 'evidence/attempts/ov001-reward252-machine-failed-20261031.json', dict(stage=stage, error=str(error), pc=hex(self.u.reg_read(UC_ARM_REG_PC)), registers=[hex(self.u.reg_read(r)) for r in REGS], events=self.events, frames=self.frames, provided=self.providers_seen))
            raise
        self.finish_frames(STOP)
        self.division_total += len(self.divisions)
        if self.frames:
            raise ValueError(('Reward252 unreturned measured entries', self.frames))
        self.stages.append(dict(stage=stage, address=hex(address), actualReturn=True, result=result))
        return result

def case(main, save, base_assets, overlay, blobs, raw, pool, post_raw=None):
    vector = dict(seed=2433024 + raw * 10 + pool, pool=pool, species=1, level=1, plus=0, variant=0, skills=1, skillPoints=0, invalid=0, ioSuccess=True, priorProgress=0, ordinal=0)
    machine = TraceMachine(main, save, base_assets, overlay)
    machine.blobs = blobs
    if int.from_bytes(blobs['ActTbl.bin'][:4], 'little') != 5522241:
        raise ValueError('Reward252 original ActTbl header differs')
    rows = setup(machine.u, blobs, vector)
    machine.u.mem_write(39059456, blobs['ActTbl.bin'])
    machine.word(35415876, 39059456)
    machine.word(35415880, 39059464)
    for row in rows:
        machine.u.mem_write(ROSTER + row['index'] * 132 + 51, bytes([raw]))
        record = bytearray(row['record'])
        record[51] = raw
        row['record'] = bytes(record)
    machine.invoke('native-runtime-clear', 33966456)
    view_base = 35393268 + 32
    mappings = []
    for index in range(6):
        view = view_base + (index if index < 3 else index + 3) * 528
        record = ROSTER + index * 132
        if machine.invoke('native-record-constructor', 33966588, [view, record, 0]) != 1:
            raise ValueError('Reward252 original record constructor rejected synthetic row')
        if machine.u.mem_read(view + 303, 1)[0] != raw:
            raise ValueError('Reward252 native record33/view12F mapping differs')
        machine.u.mem_write(view + 514, b'\x01')
        mappings.append(dict(index=index, record=hex(record), view=hex(view), rawRecord33=raw, nativeView12f=machine.u.mem_read(view + 303, 1)[0], supplied202=1, nativeClearedDescriptorAC=machine.u.mem_read(view + 176, 1)[0]))
    for team in [0, 2]:
        if machine.invoke('native-formation-constructor', 35495792, [team]) != 3:
            raise ValueError('Reward252 ordinary formation count differs')
    for row in rows[:6]:
        row['actor'] = bytes(machine.u.mem_read(row['actorAddress'], 1088))
        if row['actor'][511] != raw or row['actor'][796] != 1:
            raise ValueError('Reward252 native record33/ready formation provenance differs')
    if post_raw is not None:
        for row in rows:
            machine.u.mem_write(ROSTER + row['index'] * 132 + 51, bytes([post_raw]))
            record = bytearray(row['record'])
            record[51] = post_raw
            row['record'] = bytes(record)
    machine.u.mem_write(35884956 + 9, b'\x7f' * 4)
    machine.u.mem_write(CONTEXT + 4, b'\r')
    machine.u.mem_write(CONTEXT + 22, b'\x01')
    machine.u.mem_write(CONTEXT + 37, b'\x00')
    anticipated = {address: expected(address, rows, blobs, vector) for address in [35539408, 35539764, 35540020]}
    machine.invoke('ordinary-reward-dispatch', 35546536)
    for address, (result, outcomes) in anticipated.items():
        check_rows(machine.u, address, rows, outcomes)
        returned = [e['result'] for e in machine.returned if e['stage'] == 'ordinary-reward-dispatch' and e['address'] == hex(address)]
        if returned != [result]:
            raise ValueError('Reward252 independent award return/count model differs')
    if machine.u.mem_read(CONTEXT + 4, 1)[0] != (14 if anticipated[35539408][0] else 15):
        raise ValueError('Reward252 independent native parent transition differs')
    guard = [e for e in machine.returned if e['stage'] == 'ordinary-reward-dispatch' and e['address'] == '0x2213630']
    if len(guard) != 1 or guard[0]['result'] != 0:
        raise ValueError('Reward252 native empty-pending guard differs')
    entries = [e['address'] for e in machine.events if e['stage'] == 'ordinary-reward-dispatch']
    if not all((hex(a) in entries for a in [35546536, 35540656, 35539408, 35540020, 35539764])):
        raise ValueError('Reward252 ordinary reward call chain missing')
    if raw and '0x21e485c' in entries:
        raise ValueError('Reward252 blocked records reached native growth')
    final = [dict(index=r['index'], record33=machine.u.mem_read(ROSTER + r['index'] * 132 + 51, 1)[0], recordExperience=machine.read_word(ROSTER + r['index'] * 132 + 52), actorExperience=machine.read_word(r['actorAddress'] + 512) if r['actorAddress'] else None, actor1ff=machine.u.mem_read(r['actorAddress'] + 511, 1)[0] if r['actorAddress'] else None) for r in rows]
    return dict(rawRecord33AtConstruction=raw, rawRecord33AtReward=raw if post_raw is None else post_raw, pool=pool, actualTopCalls=machine.stages, nativeEvents=machine.events, nativeWatchedReturns=machine.returned, record33Reads=machine.reads, providedBoundaries=machine.providers_seen, nativeMappings=mappings, finalRows=final, finalParentState=machine.u.mem_read(CONTEXT + 4, 1)[0], nativeInstructions=machine.instructions, nativeFunctions=[dict(address=hex(a), bytes=b - a, module=m, mode=mode, instructions=n) for (a, b, m, mode), n in sorted(machine.pc_counts.items())], writesSha256=hashlib.sha256(json.dumps(machine.all_writes).encode()).hexdigest(), ramSha256=hashlib.sha256(bytes(machine.u.mem_read(33554432, 8388608))).hexdigest(), hardwareDivisionSubstitutions=machine.division_total, instructionTraceSha256=machine.pc_digest.hexdigest())

def run():
    if platform.python_version() != '3.13.5' or unicorn_version != '2.1.4':
        raise ValueError('Reward252 pinned execution runtime differs')
    metadata, overlay, symbols = measured_module('ov001')
    main, save, base_assets = inputs()
    blobs = assets()
    blobs['ActTbl.bin'] = bytes(NintendoDSRom((ROOT / 'inputs/game.nds').read_bytes()).getFileByName('ActTbl.bin'))
    results = []
    for raw, pool, post_raw in [(r, p, None) for r in [0, 1, 2, 255] for p in [0, 1000]] + [(0, 1000, 255), (255, 1000, 0)]:
        try:
            result = case(main, save, base_assets, overlay, blobs, raw, pool, post_raw)
        except Exception as error:
            write_json(ROOT / 'evidence/attempts/ov001-reward252-failed-20261031.json', dict(raw=raw, pool=pool, postRaw=post_raw, failure=str(error), completedCases=results, sourceCredit=0))
            raise
        results.append(result)
        print(json.dumps(dict(raw=raw, pool=pool, postRaw=post_raw, actualTopCalls=len(result['actualTopCalls']), instructions=result['nativeInstructions'], state=result['finalParentState'])), flush=True)
    for result in results:
        for function in result['nativeFunctions']:
            address = int(function['address'], 0)
            body = main if function['module'] == 'main' else overlay
            base = 33554432 if function['module'] == 'main' else 35484224
            function['spanSha256'] = hashlib.sha256(body[address - base:address - base + function['bytes']]).hexdigest()
    sources = ['trace_ov001_reward252_20261031.py', 'ov001_award_cases_20261029.py', 'ov001_award_fixture_20261029.py', 'evidence/application/preparation_machine_20261029.py']
    stale = [r for r in results if r['rawRecord33AtConstruction'] != r['rawRecord33AtReward']]
    if [(r['finalRows'][0]['actorExperience'], r['finalRows'][6]['recordExperience']) for r in stale] != [(1000, 0), (0, 42)]:
        raise ValueError('Reward252 copied-versus-current raw-field counterexamples differ')
    report = dict(schemaVersion=1, cpuModel='UC_CPU_ARM_946', pythonVersion=platform.python_version(), unicornVersion=unicorn_version, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=metadata['sha256'], generatorSha256=sha256(Path(__file__)), sourceCredit=0, results=results, actualTopReturns=sum((len(r['actualTopCalls']) for r in results)), watchedActualReturnsIncludingTop=sum((len(r['nativeWatchedReturns']) for r in results)), actualGrowthReturns=sum((e['address'] == '0x21e485c' for r in results for e in r['nativeWatchedReturns'])), actualRngReturns=sum((e['address'] == '0x203d294' for r in results for e in r['nativeWatchedReturns'])), providedCalls=sum((len(r['providedBoundaries']) for r in results)), dependencies=[dict(path=p, sha256=sha256(ROOT / p)) for p in sources], inputSaveSha256=hashlib.sha256(save).hexdigest(), initializedMainSha256=hashlib.sha256(main).hexdigest(), assetHashes={name: hashlib.sha256(body).hexdigest() for name, body in sorted((base_assets | blobs).items())}, suppliedInitialization=['Synthetic saved record rows,formation membership,resource pointer maps and reward pools', 'Runtime-view byte202=1 selects the bounded native cached-stat branch; its ordinary lifecycle is not proven', 'Reward context selector1/state13 and UI-reference sentinels7F are supplied entry conditions, not an observed future scene'], nativeInitialization=['Original64978 runtime clear', 'Original649FC record constructor copies record33 to view12F', 'Original9F70 formation invokes original9E9C block copy, deriving actor1FF from view12F and then sets actor31C=1', 'DescriptorAC comes from viewB0 cleared by native64978 and retained by constructors'], limitations=['No source or function coverage credit; no application adapter/UI changes', 'Reward UI calls,input-reference and whole battle-frame update4437C/4439C boundaries plus bounded original LevelUpTbl4-byte IO are explicit providers; all watched reward/growth/eligibility bodies execute original code', 'Actual native caller/state chain starts from supplied state13 and empty pending-UI references; complete battle lifecycle/scene reachability is unproved', 'Runtime record constructor and formation execute actual code under synthetic records and cached-stat branch, not a saved future battle state', 'Controlled post-formation backing-record changes prove a stale-copy distinction only; no real game writer/lifecycle or automatic refresh policy is asserted'])
    if hashlib.sha256((ROOT / 'inputs/save.sav').read_bytes()).hexdigest() != report['inputSaveSha256']:
        raise ValueError('Reward252 original save changed')
    if sha256(ROOT / 'inputs/game.nds') != configuration()['romSha256']:
        raise ValueError('Reward252 original ROM changed')
    report['deterministicContentSha256'] = hashlib.sha256(json.dumps(report, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    write_json(ROOT / 'evidence/application/ov001-reward252-native-state-trace-20261031.json', report)
if __name__ == '__main__':
    run()
