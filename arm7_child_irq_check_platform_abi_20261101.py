from pathlib import Path
import prove_arm7_child_irq_check_word_20261101 as witness
import link_arm7_bulk_20261030 as linker

ROOT = Path(__file__).resolve().parent
LINKER_SHA = 'f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
CALLER = {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram',
    'mode': 'arm', 'address': '0x37fd910', 'bytes': 256, 'codeBytes': 244,
    'inputModuleSha256': '13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6',
    'targetSha256': '0985b86d649c448773c1763fd89f494f02d9e99d2343fdc909eeff92ffd7e7ba'}
BINDING = {'address': '0x0380fff8', 'width': 4, 'region': 'reserved-interrupt-check-word', 'dataSourceCredit': 0}


def validate_binding(entry, binding):
    if any(entry.get(key) != value for key, value in CALLER.items()) or binding != BINDING:
        raise ValueError('Fixed platform ABI is limited to the complete qualified handler and four-byte runtime word')
    if linker.digest(Path(linker.__file__).read_bytes()) != LINKER_SHA:
        raise ValueError('Original strict ARM7 linker changed')
    return dict(BINDING)


def guard(entry, binding):
    validate_binding(entry, binding)
    dependencies = entry['sourceDependencies']
    if len(dependencies) != 1:
        raise ValueError('Exact private handler include closure required')
    header = (ROOT / dependencies[0]['path']).read_text()
    if '#define NATIVE_IRQ_CHECK_WORD (*(volatile u32 *)0x0380FFF8)' not in header:
        raise ValueError('Explicit volatile fixed-platform word view is absent')
    proof = witness.proof()
    if proof['actualOriginalReturns'] != 10 or proof['sourceDataExtentCredit'] or proof['initializedDenominatorDelta']:
        raise ValueError('Current original runtime-word witness does not satisfy the bounded contract')
    return {'generator': Path(__file__).name, 'generatorSha256': linker.digest(Path(__file__).read_bytes()),
        'caller': dict(CALLER), 'binding': dict(BINDING), 'witness': proof,
        'unknownSymbolGuardUnchanged': True, 'namespaceExtended': False,
        'originalModuleBssOrDataExtentCredit': 0, 'arbitraryAbsoluteOrdinaryDataAllowed': False}
