import gzip
import hashlib
import json
import match_runtime
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module
import match_ov001_action822_20261102 as B
import ov001_action822_machine_20261102 as M
import ov001_action822_model_20261102 as G
from ov001_action822_profiles_20261102 import profiles

PARENT = 0x021F90B4
CALL_PC = 0x021F9154


class Machine(M.Machine):
    def __init__(self, main, overlay, images, profile):
        super().__init__(main, overlay, images, profile)
        self.ranges[PARENT] = 404
        context = bytearray(self.beforeContext)
        context[0x1B] = 1
        self.beforeContext = bytes(context)
        self.u.mem_write(M.CONTEXT, bytes(context))
        self.targetEntries = []

    def code(self, u, pc, width, unused):
        if pc == M.ENTRY:
            lr = u.reg_read(M.UC_ARM_REG_LR)
            if lr != CALL_PC + 4:
                raise ValueError('823 unexpected direct caller')
            self.pending.append((pc, lr))
            self.targetEntries.append(dict(entry=hex(pc), callerPc=hex(lr - 4), rawWords=[u.reg_read(reg) for reg in M.REGS[:4]]))
        super().code(u, pc, width, unused)


def compact(result):
    return {key: value for key, value in result.items() if key not in ['memory', 'context', 'actors']} | dict(contextHex=result['context'].hex(), actorStateSha256={hex(key): hashlib.sha256(value).hexdigest() for key, value in result['actors'].items()}, completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    mainInfo, main, unused = measured_module('main')
    overlayInfo, overlay, unused = measured_module('ov001')
    B.WORK = ROOT / 'work/ol823-proof'
    match, body = B.build(B.SOURCE / 'dispatch.c', 'source')
    totals = dict(pairs=0, actualParentTopReturns=0, actualChildReturns=0, actualOtherNativeReturnInstructions=0, suppliedCalls=0)
    traces = []
    pcs = set()
    for profile in profiles()[::4]:
        results = []
        for code in [None, body]:
            vm = Machine(main, overlay, {} if code is None else {M.ENTRY: code}, profile)
            result = vm.run(PARENT)
            failures = G.model(vm, result)
            if failures or len(vm.targetEntries) != 1:
                raise ValueError(('823 parent/child model failed', profile['ordinal'], failures, vm.targetEntries))
            child = [row for row in result['nativeCompletions'] if int(row['address'], 0) == M.ENTRY]
            if len(child) != 1 or child[0]['rawR0'] != 0:
                raise ValueError('823 actual child zero return missing')
            result['actualTargetEntries'] = vm.targetEntries
            results.append(result)
        original, source = results
        for key in ['registers', 'cpsr', 'calls', 'rawCalls', 'nativeEntries', 'nativeCompletions', 'writes', 'context', 'actors', 'memory', 'actualTargetEntries']:
            if original[key] != source[key]:
                raise ValueError(('823 native/source parent difference', profile['ordinal'], key))
        totals['pairs'] += 1
        totals['actualParentTopReturns'] += 2
        totals['actualChildReturns'] += 2
        totals['actualOtherNativeReturnInstructions'] += original['actualNativeReturnInstructions'] + source['actualNativeReturnInstructions'] - 2
        totals['suppliedCalls'] += len(original['calls']) + len(source['calls'])
        pcs.update(original['ownPcs'])
        traces.append(dict(profile=profile, original=compact(original), source=compact(source), completeParentAndChildReturned=True, allRawRegistersCpsrRamIncludingStackAndCallWritesEqual=True))
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov001-action823-parent-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, canonicalMatchingCredit=0, romSha256=sha256(ROOT / 'inputs/game.nds'), processor='arm9', program='', module='ov001', moduleSha256=overlayInfo['sha256'], mainSha256=mainInfo['sha256'], parent=dict(address=hex(PARENT), bytes=404, selectedSource='src/runtime/ov001-drafts01/native_ov001_021f90b4.c', selectedSourceSha256='c6aad420a945447a08f82dc4ea18b7a0cc677f82ffda79960ea579789cb75882', nativeSpanSha256=hashlib.sha256(overlay[PARENT - 0x021D7240:PARENT - 0x021D7240 + 404]).hexdigest(), actualBranchPc=hex(CALL_PC)), child=dict(address=hex(M.ENTRY), bytes=1540, compiledSource=match), totals=totals, allPassed=True, observedChildInstructionBytes=len(pcs) * 4, trace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), generatorSha256=sha256(__file__), limits=['Actual original parent jump-table case1 dispatches to the original or canonically linked child and returns after its zero result. Parent is existing accepted source and gains no credit here.', 'Initial context0223989C+0x1B=1 is supplied, not reached through an ordinary scene initializer. The child phase, actors, synthetic MoveTbl and lower services retain all action822 qualifications.', 'Other parent cases, nonzero child return iterations and full scene/battle reachability remain unsupported. Child returns are separated from parent top returns and other native helper returns.', 'No frozen822 source, producer, reports or pin files are edited; its two returning whole-C controls remain the source acceptance controls.'])
    write_json(ROOT / 'evidence/application/ov001-action823-parent-20261102.json', report)
    print(totals, flush=True)


if __name__ == '__main__':
    execute()
