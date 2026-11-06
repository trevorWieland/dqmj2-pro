from contextlib import contextmanager
from pathlib import Path
import json
import link_arm7_bulk_20261030 as linker
import prove_arm7_tick_callback104_scope_20261031 as scope
import validate_arm7_tick_callback104_scope_20261031 as witness
from project import ROOT, write_json

PROGRAM = ''
MODULE = 'arm7-wram'
CALLER = 0x037FD1B4
CALLER_SHA = '2b06d1da94b40e70c3afc49e55ad01c660c35994f4b96ac26c6ff1ad121fa0f8'
MODULE_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
BASE_LINKER_SHA = 'f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROJECTION = 'nonmatching/arm7-bulk/20261101/lane-host-tick-callback104-final/original-native-boundary.json'
PROJECTION_SHA = 'a1ce753413588102e4ee6ff2faaf28430a4b366b41fdfaebfc3ed3e030907c4c'
PROVER_SHA = '84ce7c62e4a0cae8a59ba759a4a1e2def64744209209730a78f6b66026f3d99c'
WITNESS_SHA = 'e89c33624cab249b41c55a30c34e3ab3b518a59d29857f255e74f2cfb4e8da3b'
BASE_NAMESPACE = linker.namespace
REFERENCE = {'path': PROJECTION, 'sha256': PROJECTION_SHA, 'processor': 'arm7', 'program': PROGRAM,
    'module': MODULE, 'mode': 'arm', 'address': hex(CALLER), 'bytes': 104, 'fullSha256': CALLER_SHA,
    'instructionBytes':88,'literalBytes':16,'initializedDenominatorDelta':0,'sourceCreditFromOriginalWitness':0}


def checked(path, expected):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or scope.digest(path.read_bytes()) != expected:
        raise ValueError('Qualified callback boundary/source/input changed: ' + str(path))
    return path


def projection(report):
    return {key:value for key,value in report.items()if key!='unacceptedC'}


def inventory():
    checked(scope.__file__, PROVER_SHA)
    checked(witness.__file__, WITNESS_SHA)
    checked(linker.__file__, BASE_LINKER_SHA)
    frozen = json.loads(checked(ROOT / PROJECTION, PROJECTION_SHA).read_text())
    current = json.loads(witness.REPORT.read_text())
    if linker.namespace is namespace and witness._FRESH is None:
        raise ValueError('A full fresh original witness must precede namespace installation')
    witness.validate(current)
    if projection(current) != frozen:
        raise ValueError('Fresh complete original callback boundary/producer/return witness differs')
    if linker.namespace is BASE_NAMESPACE:
        if scope.boundary()!=frozen['scope']:
            raise ValueError('Current original callback scan differs')
    elif linker.namespace is not namespace:
        raise ValueError('Unrecognized installed namespace adapter')
    boundary=frozen['scope']
    expected={'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm','address':hex(CALLER),'bytes':104,
        'fullSha256':CALLER_SHA,'moduleSha256':MODULE_SHA,'codeRange':[hex(CALLER),hex(CALLER+88)],
        'literalRange':[hex(CALLER+88),hex(CALLER+104)],'outsideInteriorReferences':[]}
    if any(boundary.get(key)!=value for key,value in expected.items()):
        raise ValueError('Single host callback identity/code/pool/module/entry differs')
    if frozen['sourceCredit'] or frozen['originalAssemblyProvenanceCredit'] or frozen['denominatorIncrease']:
        raise ValueError('Original witness acquired source/assembly/denominator credit')
    modules,functions=BASE_NAMESPACE(PROGRAM)
    if MODULE not in modules or any(address in functions for address in range(CALLER,CALLER+104,4)):
        raise ValueError('Host callback supplement conflicts with untouched legacy namespace')
    return boundary


def prepare():
    witness.main()
    return inventory()


def guard(entry):
    if any(entry.get(key)!=value for key,value in {'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm'}.items()):
        raise ValueError('Host callback104 qualification is host ARM7 WRAM ARM only')
    address=int(entry['address'],0)if isinstance(entry.get('address'),str)else entry.get('address')
    if address!=CALLER or entry.get('bytes')!=104 or entry.get('codeBytes')!=88:
        raise ValueError('Qualified source must be the single complete host callback104')
    if entry.get('targetSha256')!=CALLER_SHA or entry.get('inputModuleSha256')!=MODULE_SHA or entry.get('qualifiedCanonicalScope')!=REFERENCE:
        raise ValueError('Exact host callback scope/full-byte/current-module reference required')
    actual=[(row['offset'],row['type'],row['symbol'],row.get('explicitAddend'))for row in entry.get('relocations',[])]
    expected=[(88,2,'native_host_arm7_timer_state_03807898',0),(96,2,'native_host_arm7_arm_037fb858',0),(100,2,'native_host_arm7_arm_037fd1b4',0)]
    if actual!=expected:
        raise ValueError('Only three measured unchanged ABS32 state/writer/self relocations qualified')
    return inventory()


def namespace(program):
    modules,functions=BASE_NAMESPACE(program)
    modules,functions=dict(modules),dict(functions)
    if program!=PROGRAM:
        return modules,functions
    inventory()
    functions[CALLER]={'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm','kind':'function',
        'address':hex(CALLER),'bytes':104,'instructionBytes':88,'boundarySource':'hash-qualified-complete-host-tick-callback104',
        'canonicalScopeEvidence':REFERENCE,'sourceCredit':0,'initializedDenominatorDelta':0}
    return modules,functions


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
        originalUnknownSymbolGuardsPreserved=True, namespaceRestored=True, sourceCreditFromBoundary=0,
        additionalInitializedDenominatorBytes=0, sharedInventoryAndConfigUnchanged=True)
    write_json(Path(directory) / 'qualified-proof.json', proof)
    return proof
