import json
from pathlib import Path
import match_runtime
import arm7_child_irq_dispatch_scope_engine_20261101 as engine
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC, ARM_REG_R0
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR
from project import ROOT, write_json

REPORT = ROOT / 'evidence/attempts/arm7-child-callback16-dispatch-abi-20261101.json'
GAP_SHA = '37c741e4eb2415cf55bece2eef91e25a4327010b50452012bef43d34fea40030'
ROM = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def boundary():
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    if engine.digest(raw) != engine.WRAM_SHA or engine.digest(raw[0x3B14:0x3C18]) != GAP_SHA:
        raise ValueError('Complete proposed original stub/dispatcher scope changed')
    inventory_path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(inventory_path.read_text())['functions']
    spans = [(a, 16, 12) for a in range(0x037FBB14, 0x037FBB84, 16)] + [(0x037FBB84, 148, 128)]
    if any(int(item['address'], 0) == address for item in inventory if item['module'] == 'utility-child-arm7-wram' for address, size, code in spans):
        raise ValueError('Proposed gap scope already exists in frozen inventory')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    records = []
    for address, size, code_size in spans:
        data = raw[address-engine.BASE:address-engine.BASE+size]
        instructions = list(decoder.disasm(data[:code_size], address))
        if len(instructions) * 4 != code_size:
            raise ValueError('Unknown proposed ARM instruction')
        literals = []
        for instruction in instructions:
            for operand in instruction.operands:
                if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                    target = instruction.address + 8 + operand.mem.disp
                    if not address+code_size <= target <= address+size-4 or target % 4:
                        raise ValueError('Proposed scope has an unresolved pool reference')
                    literals.append({'pc': hex(instruction.address), 'storage': hex(target),
                        'word': hex(int.from_bytes(raw[target-engine.BASE:target-engine.BASE+4], 'little'))})
        if {int(item['storage'], 0) for item in literals} != set(range(address+code_size,address+size,4)):
            raise ValueError('Unreferenced padding/data inside proposed function extent')
        if address != 0x037FBB84 and (instructions[0].mnemonic != 'mov' or instructions[0].operands[0].reg != ARM_REG_R0
            or int.from_bytes(data[12:16], 'little') != 0x037FBB84):
            raise ValueError('Stub does not select a dispatcher index and tail-branch through its private literal')
        records.append({'address': hex(address), 'mode': 'arm', 'bytes': size, 'codeBytes': code_size,
            'poolBytes': size-code_size, 'sha256': engine.digest(data), 'literals': literals,
            'instructions': [{'pc': hex(item.address), 'mnemonic': item.mnemonic, 'operands': item.op_str} for item in instructions]})
    vector = [int.from_bytes(raw[0xD830+i*4:0xD834+i*4], 'little') for i in range(25)]
    indexes = [int.from_bytes(raw[0xD81C+i*2:0xD81E+i*2], 'little') for i in range(9)]
    if vector[4] != 0x037FBB24 or indexes != [8,9,10,11,3,4,5,6,0]:
        raise ValueError('Original timer-vector/IRQ index mapping changed')
    roots = {address for address,size,code in spans}
    incoming, interior = [], []
    layout = engine.measured_layout()
    modules = {item['id']:item for item in layout['modules'] if item.get('processor')=='arm7'}
    for function in inventory:
        if function['module'] not in modules or function['mode'] not in ('arm','thumb'):
            continue
        item = modules[function['module']]
        image = (ROOT/item['binary']).read_bytes()
        base = int(item['base'],0)
        from capstone import CS_MODE_THUMB
        scan = Cs(CS_ARCH_ARM,CS_MODE_ARM if function['mode']=='arm' else CS_MODE_THUMB)
        scan.detail = True
        for first,last in function['ranges']:
            first,last=int(first,0),int(last,0)
            if any(first<address+size and address<last for address,size,code in spans):
                raise ValueError('Proposed scope overlaps an existing canonical code range')
            for instruction in scan.disasm(image[first-base:last-base],first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type!=2:
                    continue
                target=instruction.operands[0].imm&~1
                if 0x037FBB14<=target<0x037FBC18:
                    ref={'kind':'canonical-direct-flow','module':function['module'],'pc':hex(instruction.address),'target':hex(target)}
                    incoming.append(ref)
                    if target not in roots:
                        interior.append(ref)
    for name,item in modules.items():
        image=(ROOT/item['binary']).read_bytes()
        base=int(item['base'],0)
        for offset in range(0,len(image)-3,4):
            target=int.from_bytes(image[offset:offset+4],'little')
            if 0x037FBB14<=(target&~1)<0x037FBC18:
                ref={'kind':'aligned-initialized-word','module':name,'storage':hex(base+offset),'target':hex(target)}
                incoming.append(ref)
                if (target&~1)not in roots:
                    interior.append(ref)
    if interior:
        raise ValueError('Outside initialized/canonical reference enters a proposed interior or pool: '+str(interior))
    r0_flow = []
    consumed, overwritten = False, False
    for instruction in decoder.disasm(raw[0x3BD0:0x3BD8],0x037FBBD0):
        reads,writes = instruction.regs_access()
        consumed |= ARM_REG_R0 in reads and not overwritten
        overwritten |= ARM_REG_R0 in writes
        r0_flow.append({'pc':hex(instruction.address),'reads':[instruction.reg_name(x) for x in reads],
            'writes':[instruction.reg_name(x) for x in writes]})
    if consumed or not overwritten:
        raise ValueError('Known dispatcher continuation does not discard callback R0 as measured')
    return {'program': 'dwc/utility.bin/move/child.srl', 'module': 'utility-child-arm7-wram', 'processor': 'arm7',
        'inputModuleSha256': engine.WRAM_SHA, 'inventorySha256': engine.digest(inventory_path.read_bytes()),
        'range': ['0x037fbb14', '0x037fbc18'], 'bytes': 260, 'sha256': GAP_SHA,
        'outsideReferences':incoming,'outsideInteriorOrPoolReferences':interior,
        'instructionBytes': 212, 'poolBytes': 48, 'paddingBytes': 0, 'entries': records,
        'originalVectorBase': '0x03805830', 'originalVectorWords': vector, 'originalTimer1VectorSlot': 4,
        'originalIndexTableAddress': '0x0380581c', 'originalIndexTableU16': indexes,
        'postCallbackR0Flow':r0_flow,'callbackR0ConsumedBeforeOverwrite':consumed,
        'callback16SeparatePriorScopeBytes': 16, 'dataSourceOrExtentCredit': 0,
        'scopeAdopted': False, 'sharedInventoryOrConfigurationChanged': False,
        'limitations': ['Exact local code/pool/stub mappings only; full-module opaque indirect references remain unresolved',
            'This proposal does not amend canonical inventory or convert the initialized region into source credit']}


def cases():
    return [{'counter': counter, 'sample': sample, 'flags': flags, 'master': master}
        for counter,sample in ((0,0),(0x1234,0x5678),(0xFFFFFFFFFFFF,0xFFFF))
        for flags in (0,0x80000000,0xFFFFFFFF) for master in (0,1,0xFFFF)]


def execute(case, seed, synthetic_direct):
    machine = engine.setup({}, seed)
    cpu = machine['cpu']
    record = engine.DATA + 0x1000
    now = ((case['counter'] << 16) | case['sample']) & 0xFFFFFFFFFFFFFFFF
    values = [(0x03805B60,8,case['counter']),(0x04000100,2,case['sample']),(0x04000214,4,0),
        (0x04000208,2,case['master']),(0x04000210,4,0xA5A50000),(0x0380FFF8,4,case['flags']),
        (record+12,8,(now+0x1000)&0xFFFFFFFFFFFFFFFF)]
    for address,width,value in values:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    producer = machine['invoke'](0x037FDD30,[record])
    if not producer['actualReturn'] or bytes(cpu.mem_read(0x03805988,12)) != (0x037FD900).to_bytes(4,'little') + (1).to_bytes(4,'little') + bytes(4):
        raise ValueError('Actual original producer did not install callback16/enable/zero argument in slot5')
    if synthetic_direct:
        cpu.mem_write(0x03805988,(0x037FD910).to_bytes(4,'little'))
    events = []
    sites = {0x037FBBCC,0x037FD900,0x037FD908,0x037FD910,0x037FBBD0,0x037FBBD4,0x037FBBD8}
    def observe(machine,pc,width,unused):
        if pc in sites:
            events.append({'pc':hex(pc),'r0':machine.reg_read(UC_ARM_REG_R0),'sp':machine.reg_read(UC_ARM_REG_SP),
                'lr':hex(machine.reg_read(UC_ARM_REG_LR)),'cpsr':machine.reg_read(UC_ARM_REG_CPSR)})
    cpu.hook_add(UC_HOOK_CODE,observe)
    entry = int.from_bytes(cpu.mem_read(0x03805830+4*4,4),'little')
    result = machine['invoke'](entry,[])
    if not result['actualReturn']:
        raise ValueError('Actual original producer/table-selected timer dispatch did not return: '+str(result))
    sites = {item['pc']:item for item in events}
    low = now & 0xFFFFFFFF
    expected_before_load = low if synthetic_direct else 0
    if sites['0x37fbbd4']['r0'] != expected_before_load or sites['0x37fbbd8']['r0'] != case['flags'] | 16:
        raise ValueError('Native dispatcher did not overwrite the prior callback R0 without consuming it')
    if not synthetic_direct and (sites['0x37fd908']['r0'] != low or sites['0x37fd900']['r0'] != 0):
        raise ValueError('Actual callback16 preserve/restore observation differs')
    if any(item['sp'] % 8 for item in events):
        raise ValueError('Supported ordinary caller stack was not eight-byte aligned')
    return {'syntheticDirectHandlerPointer':synthetic_direct,'actualNativeProducer':producer,
        'dispatch':result,'events':events,'sampledLowWord':low,'sourceOrReturnMeaningCredit':0}


def proof():
    if engine.digest((ROOT/'inputs/game.nds').read_bytes()) != ROM:
        raise ValueError('Measured ROM changed')
    bounds = boundary()
    records = []
    for seed,case in enumerate(cases()):
        wrapped,direct = execute(case,seed,False),execute(case,seed,True)
        a,b = wrapped['dispatch'],direct['dispatch']
        left = {key:value for key,value in a['completeMemorySha256'].items() if int(key,0) != engine.STACK}
        right = {key:value for key,value in b['completeMemorySha256'].items() if int(key,0) != engine.STACK}
        if left != right or a['registers'] != b['registers'] or a['cpsr'] != b['cpsr']:
            raise ValueError('Measured ordinary caller externally depends on thunk R0 preservation in selected context')
        records.append({'case':case,'originalThunk':wrapped,'syntheticOriginalHandlerPointer':direct,
            'finalRegistersFlagsAndAllNonStackMemoryEqual':True,'deadStackMemoryComparedAsEqual':False})
    exhausted = engine.setup({},0)['invoke'](0x037FBB24,[],1)
    if exhausted['actualReturn'] or not exhausted['postFaultOrBoundaryStateExcluded']:
        raise ValueError('Exhausted dispatcher prefix acquired return/post-boundary credit')
    executions = [item[key] for item in records for key in ('originalThunk','syntheticOriginalHandlerPointer')]
    producer_returns = sum(item['actualNativeProducer']['actualReturn'] for item in executions)
    stub_returns = sum(item['dispatch']['actualReturn'] for item in executions)
    callback_returns = sum(frame['entry']=='0x37fd900' for item in executions for frame in item['dispatch']['nestedReturns'])
    handler_returns = sum(frame['entry']=='0x37fd910' for item in executions for frame in item['dispatch']['nestedReturns'])
    return {'romSha256':ROM,'boundary':bounds,'nativeRecords':records,'actualOriginalProducerReturns':producer_returns,
        'actualTableSelectedTimerStubReturns':stub_returns,'actualOriginalCallback16ReturnsSeparate':callback_returns,
        'actualOriginalHandlerReturnsSeparate':handler_returns,'assemblyExceptionJustified':False,
        'originalAssemblyAuthorshipProven':False,'physicalIrqExceptionEntryValidated':False,
        'callbackR0ConsumedAfterReturn':bounds['callbackR0ConsumedBeforeOverwrite'],'sourceCredit':0,'dataOrDenominatorCredit':0,
        'providerReplacements':[],'nativeInstructionPatches':False,
        'unsupportedControls':[exhausted],'unsupportedReturnCredit':0,
        'limitations':['Original normal function calls in synthetic SVC-mode contexts, no master IRQ exception/BIOS execution',
            'Direct-handler alternative changes only a disposable callback pointer after its real producer and is explicitly synthetic',
            'The wrapper writes an extra8-byte dead stack frame; dead stack bytes are not declared equivalent',
            'No ordinary-C source match, original assembly provenance, whole-game reachability or global preservation requirement follows']}


def main():
    report = {'schemaVersion':1,'generator':Path(__file__).name,'generatorSha256':engine.digest(Path(__file__).read_bytes()),**proof()}
    write_json(REPORT,report)
    print(json.dumps({'report':REPORT.relative_to(ROOT).as_posix(),'sha256':engine.digest(REPORT.read_bytes()),
        'actualTimerStubReturns':report['actualTableSelectedTimerStubReturns'],'assemblyExceptionJustified':False,'sourceCredit':0}))


if __name__ == '__main__':
    main()
