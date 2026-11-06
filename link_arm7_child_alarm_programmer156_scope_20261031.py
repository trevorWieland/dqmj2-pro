from contextlib import contextmanager
from pathlib import Path
import json
import link_arm7_bulk_20261030 as linker
import prove_arm7_child_alarm_callback16_scope_20261031 as scope
import validate_arm7_child_alarm_callback16_scope_20261031 as witness
from project import ROOT, write_json

PROGRAM = 'dwc/utility.bin/move/child.srl'
MODULE = 'utility-child-arm7-wram'
CALLER = 0x037FDD30
CALLBACK = 0x037FD900
CALLER_SHA = 'bcc8a75cf7faca954dd694050d4573f52d5116ce83cbc43d08ea78da44481cb4'
MODULE_SHA = '13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6'
CALLBACK_SHA = '785ae0872480afca27d740a8210a281fc5ac2d64ff610e3ae61c04cec102b2ab'
PROJECTION = 'nonmatching/arm7-bulk/20261031/lane-child-alarm-programmer156-qualified-final/callback-boundary.json'
PROJECTION_SHA = '1d62fc7af7d749b36979c0a129199136e744db225903a046e9f8f84657b879dd'
PROVER_SHA = '6815caa9775db5d64202552a45a16232dded40ad50b4bd9aa2c13c50d378c2cc'
WITNESS_SHA = '7bf4648b38bf99da672269e9e5175e5ea4c29cf73a86dfb422923923b61a5e9e'
BASE_NAMESPACE = linker.namespace
REFERENCE = {'path': PROJECTION, 'sha256': PROJECTION_SHA, 'processor': 'arm7', 'program': PROGRAM,
    'module': MODULE, 'mode': 'arm', 'address': hex(CALLBACK), 'bytes': 16, 'codeSha256': CALLBACK_SHA,
    'initializedDenominatorDelta': 0, 'callbackSourceCredit': 0}


def checked(path, expected):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or scope.digest(path.read_bytes()) != expected:
        raise ValueError('Qualified callback boundary/source/input changed: ' + str(path))
    return path


def projection(report):
    return {key: report[key] for key in ('romSha256', 'boundary', 'native', 'baseLinkerSha256',
        'newAcceptedFunctionOrByteCredit', 'newExecutableInventoryProposalBytes', 'initializedDenominatorDelta', 'scopeAdopted')}


def inventory():
    checked(scope.__file__, PROVER_SHA)
    checked(witness.__file__, WITNESS_SHA)
    checked(linker.__file__, scope.BASE_LINKER_SHA)
    frozen = json.loads(checked(ROOT / PROJECTION, PROJECTION_SHA).read_text())
    current = json.loads(scope.REPORT.read_text())
    witness.validate(current)
    if projection(current) != frozen or scope.inventory() != frozen['boundary']:
        raise ValueError('Fresh original callback entry/frame/mode/producer witness differs')
    boundary = frozen['boundary']
    expected = {'processor': 'arm7', 'program': PROGRAM, 'module': MODULE, 'mode': 'arm', 'address': hex(CALLBACK)}
    if boundary['identity'] != expected or boundary['bytes'] != 16 or boundary['instructionBytes'] != 16 or boundary['codeSha256'] != CALLBACK_SHA:
        raise ValueError('Callback extension is not the single complete qualified ARM entry')
    if boundary['inputModuleSha256'] != MODULE_SHA or boundary['literalBytes'] or boundary['alignmentBytes'] or boundary['ordinarySourceCredit'] or frozen['initializedDenominatorDelta']:
        raise ValueError('Callback source/pool/denominator or original module differs')
    modules, functions = BASE_NAMESPACE(PROGRAM)
    if MODULE not in modules or any(address in functions for address in range(CALLBACK, CALLBACK + 16, 4)):
        raise ValueError('Callback supplement conflicts with untouched legacy namespace')
    return boundary


def prepare():
    scope.main()
    return inventory()


def guard(entry):
    if any(entry.get(key) != value for key, value in {'processor': 'arm7', 'program': PROGRAM, 'module': MODULE, 'mode': 'arm'}.items()):
        raise ValueError('Callback qualification is child ARM7 WRAM ARM only')
    address = int(entry['address'], 0) if isinstance(entry.get('address'), str) else entry.get('address')
    if address != CALLER or entry.get('bytes') != 156 or entry.get('codeBytes') != 140:
        raise ValueError('Qualified source caller must be the complete programmer156 entry')
    if entry.get('targetSha256') != CALLER_SHA or entry.get('inputModuleSha256') != MODULE_SHA:
        raise ValueError('Qualified programmer/current original input bytes differ')
    if entry.get('qualifiedCanonicalScope') != REFERENCE:
        raise ValueError('Exact single-callback identity/extent/mode/hash reference required')
    references = [row for row in entry.get('relocations', []) if row['symbol'] == 'native_utility_child_arm7_arm_037fd900']
    if len(references) != 1 or any(references[0].get(key) != value for key, value in {'offset': 0x90, 'type': 2, 'explicitAddend': 0}.items()):
        raise ValueError('Only the measured unchanged original ARM callback pointer relocation is qualified')
    return inventory()


def namespace(program):
    modules, functions = BASE_NAMESPACE(program)
    modules, functions = dict(modules), dict(functions)
    if program != PROGRAM:
        return modules, functions
    inventory()
    functions[CALLBACK] = {'processor': 'arm7', 'program': PROGRAM, 'module': MODULE, 'mode': 'arm',
        'kind': 'function', 'address': hex(CALLBACK), 'bytes': 16, 'instructionBytes': 16,
        'boundarySource': 'hash-qualified-original-callback16-entry-20261031', 'canonicalScopeEvidence': REFERENCE,
        'sourceCredit': 0, 'initializedDenominatorDelta': 0}
    return modules, functions


@contextmanager
def installed(entry):
    guard(entry)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Another namespace adapter is already installed')
    linker.namespace = namespace
    try:
        yield
    finally:
        linker.namespace = BASE_NAMESPACE


def validate(entry, directory):
    with installed(entry):
        proof = linker.validate(entry, directory)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Original namespace was not restored')
    proof['qualifiedCanonicalScope'] = dict(REFERENCE, adapter=Path(__file__).name,
        adapterSha256=scope.digest(Path(__file__).read_bytes()), scopeProverSha256=PROVER_SHA, scopeValidatorSha256=WITNESS_SHA,
        currentFullBoundaryWitnessIndependentlyValidated=True, checkoutDebugObjectMetadataExcludedOnlyFromFrozenProjection=True,
        originalUnknownSymbolGuardsPreserved=True, namespaceRestored=True, callbackSourceCredit=0,
        additionalInitializedDenominatorBytes=0, sharedInventoryAndConfigUnchanged=True)
    write_json(Path(directory) / 'qualified-proof.json', proof)
    return proof
