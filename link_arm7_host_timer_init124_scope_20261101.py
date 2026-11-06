from contextlib import contextmanager
from pathlib import Path
import json
import link_arm7_bulk_20261030 as linker
import link_arm7_host_tick_callback104_scope_20261101 as callback
from project import ROOT,write_json

CALLER=0x037FD128
CALLER_SHA='6d8fc269956183459d40eee073ed4a4652c1004cc0511d10c19ad476a1bf7263'
BASE_NAMESPACE=callback.BASE_NAMESPACE
REFERENCE=dict(callback.REFERENCE,callerAddress=hex(CALLER),callerBytes=124,callerCodeBytes=112,callerSha256=CALLER_SHA,
    qualifiedExtraPointerCount=1,scope='single-configured-host-timer-initializer-callback-pointer')


def prepare():
    return callback.prepare()


def guard(entry):
    if any(entry.get(key)!=value for key,value in {'processor':'arm7','program':'','module':'arm7-wram','mode':'arm'}.items()):
        raise ValueError('Initializer qualification is host ARM7 WRAM ARM only')
    address=int(entry['address'],0)if isinstance(entry.get('address'),str)else entry.get('address')
    if address!=CALLER or entry.get('bytes')!=124 or entry.get('codeBytes')!=112:
        raise ValueError('Only the complete configured host initializer124 is qualified')
    if entry.get('inputModuleSha256')!=callback.MODULE_SHA or entry.get('targetSha256')!=CALLER_SHA or entry.get('qualifiedCanonicalScope')!=REFERENCE:
        raise ValueError('Initializer/callback full-byte/module/scope identity differs')
    callback.inventory()
    raw=callback.scope.MODULE.read_bytes()
    if callback.scope.digest(raw[CALLER-0x037F8000:CALLER-0x037F8000+124])!=CALLER_SHA:
        raise ValueError('Full configured initializer bytes differ')
    inventory=json.loads(callback.scope.INVENTORY.read_text())['functions']
    rows=[row for row in inventory if row['module']=='arm7-wram'and int(row['address'],0)==CALLER]
    if len(rows)!=1 or rows[0]['mode']!='arm' or rows[0]['ranges']!=[[hex(CALLER),hex(CALLER+112)]]:
        raise ValueError('Configured complete initializer code boundary differs')
    actual=[(row['offset'],row['type'],row['symbol'],row.get('explicitAddend'))for row in entry.get('relocations',[])]
    expected=[(32,1,'native_host_arm7_arm_037fd10c',-8),(80,1,'native_host_arm7_arm_037fb7bc',-8),
        (88,1,'native_host_arm7_arm_037fb8f0',-8),(112,2,'native_host_arm7_timer_state_03807898',0),
        (120,2,'native_host_arm7_arm_037fd1b4',0)]
    if actual!=expected:
        raise ValueError('Only unchanged three calls/state/one reviewed callback ABS32 references qualified')
    return callback.inventory()


@contextmanager
def installed(entry):
    guard(entry)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Another namespace adapter is already installed')
    linker.namespace=callback.namespace
    try:
        yield
    finally:
        linker.namespace=BASE_NAMESPACE


def validate(entry,directory):
    with installed(entry):
        proof=linker.validate(entry,directory)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Original namespace was not restored')
    proof['qualifiedCanonicalScope']=dict(REFERENCE,adapter=Path(__file__).name,adapterSha256=callback.scope.digest(Path(__file__).read_bytes()),
        callbackAdapter=Path(callback.__file__).name,callbackAdapterSha256=callback.scope.digest(Path(callback.__file__).read_bytes()),
        freshFullOriginalInitializerCallbackWitnessRequired=True,originalUnknownSymbolGuardsPreserved=True,namespaceRestored=True,
        additionalInitializedDenominatorBytes=0,extraCallbackSourceCredit=0,originalDataSourceCredit=0)
    write_json(Path(directory)/'qualified-proof.json',proof)
    return proof
