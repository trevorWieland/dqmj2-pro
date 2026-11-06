import json
import audit_arm7_bulk_20261030 as inventory
import arm7_runtime
import utility_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_CALL,CS_GRP_JUMP
from capstone.arm import ARM_REG_PC
from project import ROOT,sha256
CODE={0x027e9528:72}


def boundaries(entry):
    program=entry['program'];address=int(entry['address'],0);code=CODE[address];size=entry['bytes']
    path=ROOT/('evidence/utility/ghidra-arm7.json' if program else 'evidence/arm7/ghidra-runtime-inventory.json')
    rows=json.loads(path.read_text())['functions']
    own=[r for r in rows if r['module']==entry['module'] and int(r['address'],0)==address]
    if len(own)!=1 or own[0]['mode']!='arm' or [[int(v,0) for v in pair] for pair in own[0]['ranges']]!=[[address,address+code]]:
        raise ValueError('Original halfword root/instruction range differs')
    if any(address<int(r['address'],0)<address+size for r in rows):raise ValueError('Another original entry overlaps complete halfword body/pool')
    if program:layout=utility_runtime.derive()[0]
    else:layout=arm7_runtime.derive((ROOT/'extract/arm7/arm7.bin').read_bytes())
    modules={r['id']:r for r in layout['modules'] if r.get('processor')=='arm7'};binaries={name:(ROOT/r['binary']).read_bytes() for name,r in modules.items()}
    for name,data in binaries.items():
        if __import__('hashlib').sha256(data).hexdigest()!=modules[name]['sha256']:raise ValueError('Current original halfword program module differs')
    base=int(modules[entry['module']]['base'],0);native=binaries[entry['module']][address-base:address-base+size]
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;instructions=list(decoder.disasm(native[:code],address))
    if len(instructions)*4!=code or any(i.group(CS_GRP_CALL) for i in instructions):raise ValueError('Halfword leaf instruction/call scope differs')
    literals=[]
    for i in instructions:
        for operand in i.operands:
            if operand.type==3 and operand.mem.base==ARM_REG_PC:
                target=i.address+8+operand.mem.disp
                if not address+code<=target<=address+size-4 or target%4:raise ValueError('Unreconciled halfword literal')
                literals.append(dict(pc=hex(i.address),storage=hex(target),value=hex(int.from_bytes(native[target-address:target-address+4],'little'))))
    if {int(r['storage'],0) for r in literals}!=set(range(address+code,address+size,4)):raise ValueError('Unattributed pool/alignment bytes')
    references=[];interiors=[]
    for row in rows:
        if row['module'] not in modules or row['mode'] not in ('arm','thumb'):continue
        module=modules[row['module']];other_base=int(module['base'],0);raw=binaries[row['module']]
        decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB if row['mode']=='thumb' else CS_MODE_ARM);decoder.detail=True
        for first,last in row['ranges']:
            first,last=int(first,0),int(last,0)
            for i in decoder.disasm(raw[first-other_base:last-other_base],first):
                if not (i.group(CS_GRP_CALL) or i.group(CS_GRP_JUMP)) or not i.operands or i.operands[0].type!=2:continue
                target=i.operands[0].imm&~1
                if address<=target<address+size and not address<=i.address<address+code:
                    item=dict(module=row['module'],sourceRoot=row['address'],mode=row['mode'],pc=hex(i.address),target=hex(target));references.append(item)
                    if target!=address:interiors.append(item)
    if interiors:raise ValueError('Outside direct flow enters halfword interior/pool: '+str(interiors))
    for name,raw in binaries.items():
        for offset in range(0,len(raw)-3,4):
            value=int.from_bytes(raw[offset:offset+4],'little')&~1
            if address<value<address+size:raise ValueError('Unreconciled aligned original word targets halfword body/pool')
    return dict(program=program,processor='arm7',module=entry['module'],address=entry['address'],mode='arm',completeBytes=size,instructionBytes=code,literalBytes=size-code,
        inventorySha256=sha256(path),originalModuleSha256=entry['inputModuleSha256'],literalReferences=literals,outsideDirectRootReferences=references,
        outsideInteriorOrPoolReferences=[],initializedDenominatorBytesAdded=0,sourceCredit=0,
        limits=['Current configured direct-flow and aligned initialized-word audit, without a full opaque/computed-pointer producer claim'])
