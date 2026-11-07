import hashlib
import json
import re
import subprocess
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC, ARM_CC_AL, ARM_CC_INVALID, ARM_INS_BL, ARM_INS_BLX, ARM_INS_B, ARM_INS_BX
from project import ROOT, read_json, write_json, sha256
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_ov000_controller_readonly_scout import cfg


REVISION = '0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
LANE = ROOT / 'evidence/lanes/parallel-wave20261106/ov000-controller-followup-scout'
CENSUS = ROOT / 'evidence/lanes/parallel-wave20261106/ov000-controller-scout/medium-candidates.json'
OTHER = ROOT / 'evidence/lanes/parallel-wave20261106/ov000-slot-controller-next/claim.json'


def blob(name):
    return subprocess.check_output(['git', 'show', REVISION + ':' + name], cwd=ROOT)


def pin(path):
    return dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path))


def overlay_set(qualifier):
    match = re.fullmatch(r'overlays?\(([0-9, ]+)\)', qualifier)
    return [int(value) for value in match[1].split(',')] if match else None


def cfg_v2(image, base, address, size):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    pending, seen, literals, edges, exits, issues, memory, aliases, blocks = [address], {}, set(), [], [], [], [], {}, {address}
    while pending:
        pc = pending.pop()
        if pc in seen:
            continue
        if not address <= pc < address + size or pc & 3:
            issues.append(dict(kind='CFG-address-outside-configured-extent', address=hex(pc)))
            continue
        data = image[pc - base:pc - base + 4]
        decoded = list(decoder.disasm(data, pc, count=1))
        if len(decoded) != 1 or decoded[0].size != 4:
            issues.append(dict(kind='undecodable-reachable-word', address=hex(pc)))
            continue
        instruction = decoded[0]
        seen[pc] = dict(address=hex(pc), bytes=data.hex(), mnemonic=instruction.mnemonic, operands=instruction.op_str)
        fall, conditional = pc + 4, instruction.cc not in [ARM_CC_AL, ARM_CC_INVALID]
        mnemonic = instruction.mnemonic
        if pc < address + 20 and mnemonic in ['mov', 'movs'] and len(instruction.operands) == 2 and instruction.reg_name(instruction.operands[1].reg) == 'r0':
            aliases[instruction.reg_name(instruction.operands[0].reg)] = 'original-r0'
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM:
                mem = operand.mem
                register = instruction.reg_name(mem.base)
                if mem.base == ARM_REG_PC and not mem.index:
                    literals.add(pc + 8 + mem.disp)
                memory.append(dict(origin=hex(pc), mnemonic=mnemonic, baseRegister=register,
                    indexRegister=instruction.reg_name(mem.index) if mem.index else None, displacement=mem.disp,
                    width=1 if mnemonic.startswith(('ldrb', 'ldrsb', 'strb')) else 2 if mnemonic.startswith(('ldrh', 'ldrsh', 'strh')) else 4,
                    heuristicEarlyR0CopyNotPreservationProof=aliases.get(register), nativeWord=data.hex()))
        if instruction.id in [ARM_INS_BL, ARM_INS_BLX]:
            if instruction.operands and instruction.operands[0].type == ARM_OP_IMM:
                edges.append(dict(origin=hex(pc), kind='call', target=hex(instruction.operands[0].imm)))
            else:
                issues.append(dict(kind='indirect-call-needs-typed-interface', origin=hex(pc), operands=instruction.op_str))
            pending.append(fall)
            continue
        if instruction.id == ARM_INS_BX:
            if instruction.op_str == 'lr':
                exits.append(dict(origin=hex(pc), kind='return', conditional=conditional))
            else:
                issues.append(dict(kind='indirect-branch-needs-entry-proof', origin=hex(pc), operands=instruction.op_str))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if instruction.id == ARM_INS_B and instruction.operands and instruction.operands[0].type == ARM_OP_IMM:
            target = instruction.operands[0].imm
            edges.append(dict(origin=hex(pc), kind='conditional-branch' if conditional else 'branch', target=hex(target)))
            blocks.add(target)
            if address <= target < address + size:
                pending.append(target)
            else:
                exits.append(dict(origin=hex(pc), kind='external-tail', target=hex(target)))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if 'pc' in instruction.op_str and (mnemonic.startswith(('pop', 'ldm')) or mnemonic.startswith('mov') and instruction.op_str.startswith('pc,')):
            exits.append(dict(origin=hex(pc), kind='return-or-pc-write', conditional=conditional))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if instruction.op_str.startswith('pc,'):
            issues.append(dict(kind='computed-PC-needs-table-proof', origin=hex(pc), operands=instruction.op_str))
            continue
        pending.append(fall)
    if any(at in seen for at in literals):
        issues.append(dict(kind='reachable-instruction-also-loaded-as-literal'))
    return dict(reachableWords=len(seen), blockEntryCount=len(blocks), edges=edges, exits=exits, issues=issues,
        literals=[dict(address=hex(at), insideConfiguredExtent=address <= at <= address + size - 4, bytes=image[at - base:at - base + 4].hex()) for at in sorted(literals)],
        memory=memory, instructions=[seen[at] for at in sorted(seen)])


def main():
    census, other = read_json(CENSUS), read_json(OTHER)
    taken = {row['id'] for row in other['claimedFunctions']}
    all_hits = [row for row in census['candidates'] if row['identity']['id'] not in taken and
        any(re.search(r'to:0x02049(?:ad0|be4)\b', record) for record in row['originalRelocationRecords'])]
    candidates = [row for row in all_hits if int(row['identity']['address'], 0) != 0x21fe4b0]
    raw = blob('ledger/functions.jsonl')
    ledger = [json.loads(line) for line in raw.splitlines()]
    lookup = {row['id']: row for row in ledger}
    protections, inputs, git_pins = [], {}, []
    def protect(document, origin):
        protections.extend((start, end, origin) for program, cpu, module, start, end in intervals(document)
            if (program, cpu, module) == ('', 'arm9', 'ov000'))
    protect([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')], REVISION + ':ledger/functions.jsonl')
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = blob(name)
        protect(json.loads(content)[key], REVISION + ':' + name)
        git_pins.append(dict(gitObject=REVISION + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        data = path.read_bytes()
        inputs[path.relative_to(ROOT).as_posix()] = hashlib.sha256(data).hexdigest()
        protect(json.loads(data), path.relative_to(ROOT).as_posix())
    for path in [CENSUS, OTHER]:
        inputs[path.relative_to(ROOT).as_posix()] = sha256(path)
    modules = json.loads(blob('manifest.json'))['modules']
    module = next(row for row in modules if row['name'] == 'ov000' and row['processor'] == 'arm9' and not row.get('program'))
    base = int(module['base'], 0)
    binary = ROOT / module['binary']
    image = binary.read_bytes()
    if sha256(binary) != census['nativeModuleSha256'] or hashlib.sha256(image).hexdigest() != module['sha256']:
        raise ValueError('Original overlay0 native module epoch differs')
    symbol_path = ROOT / 'config/arm9/overlays/ov000/symbols.txt'
    symbols = symbol_path.read_text(encoding='utf8').splitlines()
    relocation_path = symbol_path.with_name('relocs.txt')
    relocations = relocation_path.read_text(encoding='utf8').splitlines()
    for path in [binary, symbol_path, relocation_path]:
        inputs[path.relative_to(ROOT).as_posix()] = sha256(path)
    incoming_files = sorted((ROOT / 'config/arm9').rglob('relocs.txt'))
    incoming_records = []
    for path in incoming_files:
        relative = path.relative_to(ROOT).as_posix()
        inputs[relative] = sha256(path)
        caller = 'main' if path.parent == ROOT / 'config/arm9' else path.parent.name
        for line in path.read_text(encoding='utf8').splitlines():
            match = re.search(r'from:(0x[0-9a-f]+).* to:(0x[0-9a-f]+) module:(.+)$', line)
            if match:
                incoming_records.append((int(match[1], 0), int(match[2], 0), match[3], caller, relative, line))
    selected, rejected = [], []
    for candidate in candidates:
        identity = candidate['identity']
        row = lookup[identity['id']]
        start, size = int(row['address'], 0), row['bytes']
        hits = sorted({origin for a, b, origin in protections if max(a, start) < min(b, start + size)})
        if hits:
            rejected.append(dict(id=row['id'], address=row['address'], bytes=size, physicalConflicts=hits))
            continue
        if row['states']['functionMatched'] or row.get('sourceUnit') or candidate['canonicalInventoryRecord'] not in symbols:
            raise ValueError('Proposed original unaccepted whole boundary differs')
        if any((match := re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-f]+)', line)) and start < int(match[1], 0) < start + size for line in symbols):
            raise ValueError('Canonical interior entry in proposed function')
        body = image[start - base:start - base + size]
        if len(body) != size or hashlib.sha256(body).hexdigest() != candidate['nativeSha256'] or candidate['nativeSha256'] != row['inputBytesSha256']:
            raise ValueError('Actual complete overlay function hash differs')
        actual = [line for line in relocations if (match := re.match(r'from:(0x[0-9a-f]+)', line)) and start <= int(match[1], 0) < start + size]
        if actual != candidate['originalRelocationRecords']:
            raise ValueError('Original complete outgoing relocation list differs')
        legacy_flow = cfg(image, base, start, size)
        flow = cfg_v2(image, base, start, size)
        if legacy_flow != candidate['cfg'] or flow['issues'] or not flow['exits']:
            raise ValueError('Actual bounded ARM control flow differs')
        covered = set()
        for instruction in flow['instructions']:
            at = int(instruction['address'], 0)
            if image[at - base:at - base + 4].hex() != instruction['bytes']:
                raise ValueError('Actual reachable instruction bytes differ')
            covered.update(range(at, at + 4))
        for literal in flow['literals']:
            at = int(literal['address'], 0)
            if not literal['insideConfiguredExtent'] or image[at - base:at - base + 4].hex() != literal['bytes']:
                raise ValueError('Actual original literal range differs')
            covered.update(range(at, at + 4))
        if covered != set(range(start, start + size)):
            raise ValueError(('Native whole extent has unexplained CFG/literal bytes', row['address'], [hex(at) for at in sorted(set(range(start, start + size)) - covered)]))
        incoming = []
        for origin, target, qualifier, caller, path, record in incoming_records:
            destinations = overlay_set(qualifier)
            if start <= (target & ~1) < start + size and destinations is not None and 0 in destinations:
                incoming.append(dict(callerProgram='', callerProcessor='arm9', callerModule=caller,
                    origin=hex(origin), originalTarget=hex(target), record=record, sourcePath=path,
                    targetNamespaceQualifier=qualifier, targetOverlayCandidates=destinations,
                    ambiguous=destinations != [0], interiorTarget=(target & ~1) != start))
        outgoing = []
        for record in actual:
            match = re.search(r'from:(0x[0-9a-f]+) kind:(\S+) to:(0x[0-9a-f]+) module:(.+)$', record)
            targets = overlay_set(match[4])
            outgoing.append(dict(record=record, origin=match[1], kind=match[2], target=match[3],
                originalNamespace=match[4], overlayCandidates=targets,
                namespaceResolved=match[4] in ['main', 'itcm'] or targets is not None and len(targets) == 1,
                guessedNamesOrAliasesAdded=False))
        selected.append(dict(identity=row, nativeSha256=candidate['nativeSha256'],
            canonicalInventoryRecord=candidate['canonicalInventoryRecord'], originalRelocationRecords=actual,
            outgoingNamespaceInventory=outgoing, actualIncomingRecords=incoming, cfg=flow,
            legacyCfgChangedByConditionCodeFix=flow != legacy_flow,
            wholeInitializedExtentCoveredByOriginalInstructionsAndLiterals=True,
            historicalArtifactPins=candidate['historicalArtifactPins'], semanticNamesInferred=True, sourceCredit=0))
    ready_path = ROOT / 'evidence/lanes/parallel-wave20261106/ov000-slot-controller-next/first/ready.json'
    ready = read_json(ready_path)
    report = read_json(ROOT / ready['packets'][0]['report'])
    exemplar = report['matches'][0]
    context_paths = sorted({ROOT / item['source'] for item in report['matches']} |
        {ROOT / pin['path'] for item in report['matches'] for pin in item['sourceDependencies']})
    for path in context_paths + [ready_path]:
        inputs[path.relative_to(ROOT).as_posix()] = sha256(path)
    changed = [path for path, digest in inputs.items() if sha256(ROOT / path) != digest]
    final_paths = set((ROOT / 'evidence/lanes').rglob('claim.json')) | set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json'))
    if changed or final_paths != set(paths):
        raise ValueError(('Protection/input epoch changed; no ownership proposed', changed))
    output = dict(status='read-only-game-controller-followup-proposal-awaiting-Root-admission',
        sourceRevision=REVISION, ledgerSha256=hashlib.sha256(raw).hexdigest(), sourceCredit=0,
        functions=len(selected), bytes=sum(row['identity']['bytes'] for row in selected), entries=selected,
        rejectedProtectedCandidates=rejected, excludedOtherClaim=pin(OTHER), acceptedCodeDataLinkageAndAllCurrentClaimsSpecsCompared=True,
        deferredOutsideRequestedScope=[dict(address='0x21fe4b0', bytes=336, reason='Corrected CFG reveals8 calls and unrelated controller/provider families; outside requested16/2740 wrapper scope,not a claimed protection conflict')],
        cfgConditionCorrection=dict(legacyHelper=pin(ROOT / 'wave20261106_ov000_controller_readonly_scout.py'),
            oldCensusPreserved=pin(CENSUS), oldPredicateMixedInstructionIDsWithConditionCodes=True,
            actualBInstructionID=ARM_INS_B, unconditionalConditionCodesOnly=[ARM_CC_AL, ARM_CC_INVALID],
            changedEntries=[entry['identity']['address'] for entry in selected if entry['legacyCfgChangedByConditionCodeFix']],
            allNativeInstructionsAndLiteralPayloadsRetained=True, originalCensusAndHelperChanged=False),
        measuredInterfaceBasis=dict(ready=pin(ready_path), compilerFlags=exemplar['compilerFlags'],
            nativeMainLookup=dict(entry='main/arm/02049ad0', prototype='EntryView*(s32)', tableBase='0x02102a18', slotStride=12, consumedEntryPrefixBytes=8),
            nativeMainUpdate=dict(entry='main/arm/02049be4', prototype='int(EntryView*,u32,u32,u32,u8,u8,u8,u8,u32,s8,u32)'),
            fields=['Entry link+0; signed byte fields+4/+5/+6', 'Link first word+0; Resource pointer+4; Resource flags word+24'],
            interpretationLimits='Slot/controller/resource/font-style names are hypotheses except literal offsets,widths,accepted helper bytes and measured call ABI. No public-primary source correspondence is claimed.'),
        proposedSourceRoot='src/runtime/parallel_wave20261106/ov000-slot-controller-followup',
        proposedWorkRoot='work/w6ocf', proposedHelperPrefix='wave20261106_ov000_slot_controller_followup_',
        budget='One measured2.0/base O2/off/speed C99 context; actual widths/branch/namespace evidence before any source change. Park allocation plateaus and unresolved overlay candidates.',
        validationPlan=['Complete source-generated object and genuine MW link for each full canonical extent; original relocation and mode/pointer/data addends preserved.',
            'Only independently verified caller/slot/field models; actual accepted20+172 helper execution may be reused with0extra credit and opaque deeper providers.',
            'Meaningful wrong-C/layout/binding negatives,unchanged closed compiler-input guard and required prototypes,fresh source-only copied-root canonical products.'],
        actualInputPins=[dict(path=path, sha256=digest) for path, digest in sorted(inputs.items())], gitPins=git_pins,
        compilerInvoked=False, reconstructionCSourceOrClaimOrSharedWrites=False,
        coordinatorFreshOriginalRomStorageLinkageAndAllProtectionAdmissionStillRequired=True,
        generatorSha256=sha256(__file__))
    write_json(LANE / 'proposal-v2.json', output)
    print(dict(path=(LANE / 'proposal-v2.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'proposal-v2.json'),
        functions=len(selected), bytes=output['bytes'], excluded=len(rejected),
        unresolvedOutgoing=sum(not item['namespaceResolved'] for row in selected for item in row['outgoingNamespaceInventory']),
        incomingAmbiguous=sum(item['ambiguous'] for row in selected for item in row['actualIncomingRecords'])))


if __name__ == '__main__':
    main()
