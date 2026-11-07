import re
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_main_friend_next_second_compiler import LANE, WORK
from wave20261106_dwc_main_friend_next_second_build import build
from wave20261106_dwc_main_friend_next_second_bindings import negatives
from wave20261106_dwc_main_friend_next_second_controls import strict, layout, wrong_c
from wave20261106_dwc_main_friend_next_second_fixtures import prove


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
    if len(matches) != 7 or sum(row['bytes'] for row in matches) != 558:
        raise ValueError('Friend packet membership changed')
    prototypes, types, bindings, altered = strict(matches), layout(matches), negatives(matches), wrong_c(matches)
    closure = code_closure([Path(__file__).name])
    limits = [
        'Seven complete ordinary-C callers genuinely compile/link to558 original bytes. The2-byte published empty return is a whole configured function; adjacent2-byte alignment is uncredited.',
        'Measured original types qualify only the consumed main-core prefix,main global pointer/error words,12-byte game-key records and all initialized8 sockaddr bytes. Original object allocation/capacity or storage authorship is not established.',
        'Thirty-one bounded cases compare native/rebuilt all GPRs/CPSR,callee-saved/stack,raw provider tuples,ordered writes/reads and independent final-memory/call/return models. Providers and selected siblings are opaque fixture contracts with zero implementation/execution credit.',
        'Startup callback pointers preserve exact canonical main/Thumb entry+lowbit values. Game-key field references retain one genuine source symbol plus original0/1/2/4/8 relocation addends; no interior aliases or object patches are created.',
        'The main-global8-byte struct view and older4-byte pointer-only declaration remain separate frozen DS views. Their common first-word evidence does not prove whole-program portable type compatibility; the mandatory interface receipt preserves that debt.',
        'Tests cover declared valid pointers,small key indices,allocation success/failure,close/error forwarding,QR/NAT/unknown packet routing and network-port boundaries. Real network/hardware/services,callback lifetimes,concurrency,arbitrary invalid inputs and Windows/Android behavior remain unproved.',
        'All new rows pass unchanged closed_c_compiler_inputs and strict prototype diagnostics with identical function bytes/relocations. Seven meaningful wrong-C links fail independent models;16 compiler layout checks,two wrong-layout guards and original-namespace/addend/pointer controls remain strict.']

    report = dict(schemaVersion=1, romSha256=inputs['romSha256'], moduleSha256=inputs['moduleSha256'],
        program='', processor='arm9', module='main', allPassed=True, matches=matches,
        matchedFunctions=7, matchedBytes=558, ordinaryCBytes=558, justifiedAssemblyBytes=0,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),
        boundedCallerModels=models, strictPrototypeControls=prototypes, actualCompilerLayoutControls=types,
        nativeBindingControls=bindings, wrongSourceControls=altered, suppliedCalleeSourceOrExecutionCredit=0,
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in closure],
        mandatoryInputs=[dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json'))],
        originalObjectScaffolding=False, limits=limits)
    write_json(LANE / 'match.json', report)
    print(dict(functions=7, bytes=558, nativeAndSourceReturns=report['actualNativeAndSourceCallerReturns']))


if __name__ == '__main__':
    main()
