import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
import unicorn
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov005_controller905_machine_20261102 as M
import ov005_controller905_model_20261102 as G

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-controller903/explicit-descriptor-input'
SECOND = ROOT / 'nonmatching/overlay-lane/20261102-controller861/021d8900/contiguous-two-word-callback-payload'
WORK = ROOT / 'work/ol906-proof'


def build(source, name, origin):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov005', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('906 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'} | dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3,13,5) or unicorn.__version__ != '2.1.4':
        raise ValueError('906 pinned runtime differs')
    for row in read_json(ROOT / 'evidence/verification/ov005-controller906-inputs-20261102.json')['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('906 input differs', row['path']))
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov005')
    hypotheses = []
    images = {}
    for name, source, origin in [('ghidra',SOURCE,0x02650000),('m2c',SECOND,0x02652000)]:
        proof, image = build(source / 'source.c', name, origin)
        if proof['canonicalComparison'].get('exactCallerBytes'):
            raise ValueError('906 unexpected exact source; review separately')
        images[origin] = image
        hypotheses.append(dict(name=name,origin=origin,proof=proof))
    template = (SOURCE / 'source.c').read_text()
    controls = []
    for index,(name,text) in enumerate([('wrong-return',template.replace('return iVar11;', 'return iVar11 ^ 1;')),('wrong-payload',template.replace('payload[1] = param_2;', 'payload[1] = param_2 ^ 1U;'))]):
        if text == template:
            raise ValueError('906 control mutation site absent')
        directory = ROOT / 'nonmatching/overlay-lane/20261102-controller906' / name
        directory.mkdir(parents=True,exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('906 frozen control differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        origin = 0x02654000 + index * 0x2000
        proof,image = build(source,name,origin)
        images[origin] = image
        controls.append(dict(name=name,origin=origin,proof=proof,actualTopReturns=0,rejected=0,positive=0))
    totals = dict(pairs=0,actualTopReturns=0,actualNativeDescriptorReturns=0,suppliedServiceCalls=0)
    variants = []
    traces = []
    pcs = set()
    for hypothesis in hypotheses:
        counts = dict(pairs=0,actualTopReturns=0,actualNativeDescriptorReturns=0,suppliedServiceCalls=0)
        for profile in G.profiles():
            results = []
            entries = [('native',M.ENTRY),('candidate',hypothesis['origin'])]
            if hypothesis['name'] == 'ghidra':
                entries += [(row['name'],row['origin']) for row in controls]
            failures = []
            for kind,entry in entries:
                vm = M.Machine(main,overlay,images,profile)
                result = vm.run(entry)
                result['kind'] = kind
                results.append(result)
                failures.append(G.model(vm,result))
            original,candidate = results[:2]
            if failures[0] or failures[1]:
                write_json(ROOT/'evidence/attempts/ov005-controller906-model-rejected-20261102.json',dict(variant=hypothesis['name'],profile=profile,failures=failures,results=list(map(compact,results))))
                raise ValueError(('906 model rejected',hypothesis['name'],profile['ordinal'],failures[:2]))
            differences = [name for name in ['objectHex','writes'] if original[name] != candidate[name]]
            if G.logical_calls(original) != G.logical_calls(candidate):
                differences.append('consumed call contracts')
            if differences or original['registers'][0] != candidate['registers'][0]:
                raise ValueError(('906 own effects differ',profile['ordinal'],differences))
            firstStack = min(original['privateStackStart'],candidate['privateStackStart'])
            if not M.SP - 0x1000 <= firstStack <= M.SP:
                raise ValueError('906 private stack bound')
            memories = []
            for result in [original,candidate]:
                memory = bytearray(result['memory'])
                memory[firstStack - 0x02000000:M.SP - 0x02000000] = bytes(M.SP - firstStack)
                memories.append(memory)
            if memories[0] != memories[1]:
                raise ValueError('906 full observable RAM differs')
            counts['pairs'] += 1
            counts['actualTopReturns'] += 2
            counts['actualNativeDescriptorReturns'] += sum(len(row['nativeHelperPhysicalReturns']) for row in results[:2])
            counts['suppliedServiceCalls'] += sum(len(row['calls']) for row in results[:2])
            pcs.update(original['ownPcs'])
            if hypothesis['name'] == 'ghidra':
                for index,control in enumerate(controls):
                    control['actualTopReturns'] += 1
                    control['rejected' if failures[index+2] else 'positive'] += 1
            traces.append(dict(variant=hypothesis['name'],profile=profile,results=list(map(compact,results)),modelFailures=failures,observedPrivateStackStart=firstStack,observableRamSha256=hashlib.sha256(memories[0]).hexdigest(),scratchDifferences=[i for i in [1,2,3,12]if original['registers'][i] != candidate['registers'][i]],cpsrDiffers=original['cpsr']!=candidate['cpsr']))
        variants.append(dict(**hypothesis,totals=counts))
        for key,value in counts.items():
            totals[key] += value
    if any(not row['rejected'] for row in controls):
        raise ValueError('906 controls did not reject')
    raw = json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact = ROOT/'evidence/generated/ov005-controller906-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report = dict(schemaVersion=1,allPassed=True,sourceCredit=0,canonicalMatchedBytes=0,canonicalMatchedFunctions=0,romSha256=configuration()['romSha256'],module='ov005',processor='arm9',program='',mode='arm',address=hex(M.ENTRY),nativeBytes=1500,moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],hypotheses=variants,totals=totals,negativeEvidence=controls,nativeOwnInstructionAddresses=sorted(pcs),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Only event6 of the complete nonmatching1500-byte controller is behavior-qualified. Both complete C bodies compile and genuinely link at private origins without overwriting adjacent native code; canonical failures remain1476/1500 and1444/1500. Other events/scene reachability remain unsupported.','Original196-byte descriptor search executes with both required words: controller pointer and request pointer. The independent model checks all16 entry slots, exact and high-bit generic selection rules, callback return gates and resulting selected/key writes. Synthetic rows and initialized request/object are prerequisites.','Descriptor select method and event callback are explicitly supplied service boundaries with deterministic legal caller-saved GPR/NZCV clobbers; callbacks can mutate the first of two initialized payload words. The second payload word carries the full request address. No original source formal-arity or complete payload extent is inferred beyond actual initialized/read words.','Each frontend performs270 separately executed original/C pairs; originals are rerun for the second frontend. Reported1080 positive top returns and descriptor returns are actual distinct executions, not duplicated accounting. Whole-C negative returns are counted separately.','Full8MiB RAM outside measured private-stack union, ordered observable writes, consumed call words, native proper return opcodes/SP/callee-saved state and raw return word are checked; raw unused argument/scratch/CPSR differences remain in the trace.','No module/source/whole-ROM byte credit, game-state meaning, ordinary scene validity, application edits, device execution or other-event pointer/shift domains are established.'])
    write_json(ROOT/'evidence/application/ov005-controller906-behavior-20261102.json',report)
    print(dict(totals=totals,variants=[dict(name=r['name'],totals=r['totals'])for r in variants],controls=[{k:r[k]for k in ['name','actualTopReturns','rejected','positive']}for r in controls],sourceCredit=0),flush=True)

if __name__ == '__main__':
    execute()
