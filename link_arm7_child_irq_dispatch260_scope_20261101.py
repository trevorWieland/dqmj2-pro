from contextlib import contextmanager
from pathlib import Path
import json
import link_arm7_bulk_20261030 as linker
import prove_arm7_child_callback16_dispatch_abi_20261101 as scope
import validate_arm7_child_callback16_dispatch_abi_20261101 as witness
from project import ROOT, write_json

PROGRAM = 'dwc/utility.bin/move/child.srl'
MODULE = 'utility-child-arm7-wram'
MODULE_SHA = '13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6'
BASE_LINKER_SHA = 'f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROVER_SHA = '818ab2524a9fff3e188216819ed5be6dc939e4ea15cf51830cd38bcb33896b5d'
VALIDATOR_SHA = '43ebf7dea8b69f7916d87ff1404274942859938b2423ae662063b76f90d336a8'
REPORT_SHA = '8edfa7692a966ee44ee3fa5eef284ad2b25977e23b7292c5861b5e93bac5b5c5'
SPECS = {58702612: {'bytes': 16, 'codeBytes': 12, 'targetSha256': 'b419445e053479e7268155ad46073cfba0fe145b56a2e06f33fc8bd81c23b6bc'}, 58702628: {'bytes': 16, 'codeBytes': 12, 'targetSha256': 'fce4b2aa80c01757144a03c2ab0f7a25b00c2d158c15eab8cd30bf89fb1da4ed'}, 58702644: {'bytes': 16, 'codeBytes': 12, 'targetSha256': '39656bab1138a9fb784c2d878f2db6c2550142b0c43ca7754d9b2806fc02267c'}, 58702660: {'bytes': 16, 'codeBytes': 12, 'targetSha256': '487d3580a49534865c231ecaca318b235191843009c6aec52cf7b09700cf10c3'}, 58702676: {'bytes': 16, 'codeBytes': 12, 'targetSha256': '98514ea806e39063deec7feee937c8d08df15e9f447b43cb0167931d7776b58e'}, 58702692: {'bytes': 16, 'codeBytes': 12, 'targetSha256': '186ecdda2b349a016c2fbe471e1f314c63061c8a55c9b5dc6ec59d4cce811df8'}, 58702708: {'bytes': 16, 'codeBytes': 12, 'targetSha256': '674b00d8869590e251a486e98a707759052a4961db99f1eca0c833aef1b55d48'}, 58702724: {'bytes': 148, 'codeBytes': 128, 'targetSha256': '71597cff1a7664c58ec713c434e5fe0584631e8de70880a36b20ee3a90de31cf'}}
BASE_NAMESPACE = linker.namespace
REFERENCE = {'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm',
    'path':scope.REPORT.relative_to(ROOT).as_posix(),'sha256':REPORT_SHA,
    'range':['0x037fbb14','0x037fbc18'],'bytes':260,'instructionBytes':212,'poolBytes':48,
    'sourceOrAssemblyOrDenominatorCredit':0}


def checked(path, expected):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or linker.digest(path.read_bytes()) != expected:
        raise ValueError('Current qualified IRQ scope input/witness differs: '+str(path))
    return path


def inventory():
    checked(scope.__file__,PROVER_SHA)
    checked(witness.__file__,VALIDATOR_SHA)
    checked(linker.__file__,BASE_LINKER_SHA)
    current=json.loads(checked(scope.REPORT,REPORT_SHA).read_text())
    witness.validate(current)
    bounds=current['boundary']
    measured={int(item['address'],0):{key:item[key] for key in ('bytes','codeBytes')}|{'targetSha256':item['sha256']} for item in bounds['entries']}
    if measured!=SPECS or bounds['inputModuleSha256']!=MODULE_SHA or bounds['instructionBytes']!=212 or bounds['poolBytes']!=48:
        raise ValueError('Exact eight original ARM entry boundaries/pools/mappings differ')
    if current['sourceCredit'] or current['dataOrDenominatorCredit'] or current['assemblyExceptionJustified'] or bounds['scopeAdopted']:
        raise ValueError('Native scope evidence acquired source/assembly/adoption credit')
    modules,functions=BASE_NAMESPACE(PROGRAM)
    if modules[MODULE]['sha256']!=MODULE_SHA or any(address in functions for address in SPECS):
        raise ValueError('Proposed scope conflicts with original strict namespace')
    return bounds


def prepare():
    scope.main()
    return inventory()


def guard(entry):
    if any(entry.get(key)!=value for key,value in {'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm'}.items()):
        raise ValueError('IRQ source extension is child ARM7 WRAM ARM only')
    address=int(entry['address'],0) if isinstance(entry.get('address'),str) else entry.get('address')
    if address not in SPECS or any(entry.get(key)!=value for key,value in SPECS[address].items()):
        raise ValueError('Only a complete exact one-of-eight original entry is qualified')
    if entry.get('inputModuleSha256')!=MODULE_SHA or entry.get('qualifiedCanonicalScope')!=REFERENCE:
        raise ValueError('Qualified original module or complete scope reference differs')
    if address!=0x037FBB84:
        refs=[item for item in entry.get('relocations',[]) if item['symbol']=='native_utility_child_arm7_arm_037fbb84']
        if len(refs)!=1 or any(refs[0].get(key)!=value for key,value in {'offset':12,'type':2,'explicitAddend':0}.items()):
            raise ValueError('Exact unchanged original dispatcher tail-pointer relocation required')
    return inventory()


def namespace(program):
    modules,functions=BASE_NAMESPACE(program)
    modules,functions=dict(modules),dict(functions)
    if program!=PROGRAM:
        return modules,functions
    inventory()
    for address,item in SPECS.items():
        functions[address]={'processor':'arm7','program':PROGRAM,'module':MODULE,'mode':'arm','kind':'function',
            'address':hex(address),'bytes':item['bytes'],'instructionBytes':item['codeBytes'],
            'boundarySource':'hash-qualified-original-IRQ-stub-dispatcher-scope-20261101',
            'canonicalScopeEvidence':dict(REFERENCE),'sourceCredit':0,'initializedDenominatorDelta':0}
    return modules,functions


@contextmanager
def installed(entry):
    guard(entry)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Another namespace adapter is installed')
    linker.namespace=namespace
    try:
        yield
    finally:
        linker.namespace=BASE_NAMESPACE


def validate(entry,directory):
    with installed(entry):
        proof=linker.validate(entry,directory)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Original namespace was not restored')
    proof['qualifiedCanonicalScope']=dict(REFERENCE,adapter=Path(__file__).name,
        adapterSha256=linker.digest(Path(__file__).read_bytes()),scopeProverSha256=PROVER_SHA,scopeValidatorSha256=VALIDATOR_SHA,
        completeFreshNativeWitnessRequired=True,originalUnknownFunctionAndDataGuardsPreserved=True,
        namespaceRestored=True,sharedInventoryAndConfigurationChanged=False)
    write_json(Path(directory)/'qualified-proof.json',proof)
    return proof
