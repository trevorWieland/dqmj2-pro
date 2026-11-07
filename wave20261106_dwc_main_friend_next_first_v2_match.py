import re
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_main_friend_next_first_v2_compiler import LANE, WORK
from wave20261106_dwc_main_friend_next_first_v2_build import build
from wave20261106_dwc_main_friend_next_first_v2_bindings import negatives
from wave20261106_dwc_main_friend_next_first_v2_controls import strict, layout, wrong_c
from wave20261106_dwc_main_friend_next_first_v2_fixtures import prove


def main():
    inputs = read_json(LANE / 'inputs.json')
    for item in inputs['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('Frozen friend input changed', item['path']))
    if inputs['romSha256'] != configuration()['romSha256']:
        raise ValueError('Friend ROM identity changed')
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    matches, models = [], []
    keys = ['address', 'bytes', 'source', 'sourceSha256', 'sourceDependencies', 'targetSha256',
            'compilerPath', 'compilerSha256', 'compilerFlags', 'relocations', 'nativeSymbolEntries']
    for item in inputs['entries']:
        source = ROOT / item['source']
        for path in [source, *[ROOT / pin['path'] for pin in item['sourceDependencies']]]:
            text = path.read_text()
            if len(text.splitlines()) > 500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b', text):
                raise ValueError(('Ordinary C source policy changed', str(path)))
        row, body = build(source, WORK / 'proof' / source.stem / 'source')
        for key in keys:
            if row[key] != item[key]:
                raise ValueError(('Frozen friend compiler/ABI contract differs', item['address'], key))
        if row['compiledBytes'] != row['bytes'] or not row['realLink']['exactCallerBytes']:
            raise ValueError('Complete genuine friend extent differs')
        start = int(row['address'], 0) - 0x2000000
        native = image[start:start + row['bytes']]
        model = prove(row, native, body)
        models.append(model)
        row.update(program='', sourceLanguage='C', ordinaryCOnly=True, ordinaryCBytes=row['bytes'],
            justifiedAssemblyBytes=0, justifiedAssemblyRanges=[], sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, sourceProvenance=item['sourceProvenance'],
            matchingBytesScope='Complete genuine MW-linked native caller extent including literal pool',
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],
            suppliedCalleeSourceOrExecutionCredit=0, suppliedStorageCredit=0, hardwareOrGameExecutionCredit=0,
            boundaryReturnContract=item['boundaryReturnContract'])
        matches.append(row)
        print('proved friend C', row['address'], row['bytes'], model['cases'], flush=True)
    if len(matches) != 8 or sum(row['bytes'] for row in matches) != 1484:
        raise ValueError('Friend packet membership changed')
    prototypes, types, bindings, altered = strict(matches), layout(matches), negatives(matches), wrong_c(matches)
    closure = code_closure([Path(__file__).name])
    limits = [
        'Eight complete ordinary-C callers genuinely compile/link to1484 original bytes. Coordinator shared acceptance remains pending.',
        'The published friend/main comparison revision is adapted only for directly measured legacy flag20/8/10 call sequences and172-byte profile-match records. Those raw flag labels do not establish broader account/game meanings.',
        'Actual compiler checks cover the92-byte consumed friend prefix,12-byte records,64-byte user data,532-byte buddy status,172-byte match stride and GP response field offsets. The GP get-info declaration is only a consumed prefix; no complete provider record or friend-control allocation size is claimed.',
        'Forty-eight bounded cases compare native and rebuilt caller returns,all GPRs/CPSR,callee-saved state,stack,ordered writes,raw provider tuples,observed reads and independent final memory/call models. Read order is compared native-to-source,not independently modeled. Provider outputs and ARM/Thumb callbacks are fixture contracts; no provider implementation,real network,hardware,game,Windows or Android execution is established.',
        'Opaque providers include even selected sibling functions in this packet: they receive zero supplied-provider execution or source credit in caller fixtures. No imported data,table,global backing or scaffolding byte is credited.',
        'Error handling models cover GP results0..4 only; the published switch has no defined initialization for other result values. Tests assume valid declared pointers,indices and count bounds. Real concurrency,allocation failure,callback lifetime and unified portable imported ABI completeness remain unproved.',
        'Strict prototype diagnostics preserve every complete function body and relocation signature. Eight genuine wrong-C links fail independent models; two wrong layout declarations and32 original-namespace/relocation contracts reject.']
    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=inputs['moduleSha256'],
        program='', processor='arm9', module='main', allPassed=True, matches=matches,
        matchedFunctions=8, matchedBytes=1484, ordinaryCBytes=1484, justifiedAssemblyBytes=0,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),
        boundedCallerModels=models, strictPrototypeControls=prototypes, actualCompilerLayoutControls=types,
        nativeBindingControls=bindings, wrongSourceControls=altered, suppliedCalleeSourceOrExecutionCredit=0,
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure],
        mandatoryInputs=[dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json'))],
        originalObjectScaffolding=False, limits=limits)
    write_json(LANE / 'match.json', report)
    print(dict(functions=8, bytes=1484, nativeAndSourceReturns=report['actualNativeAndSourceCallerReturns']))


if __name__ == '__main__':
    main()
