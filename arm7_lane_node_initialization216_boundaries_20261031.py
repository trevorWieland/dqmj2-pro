import audit_arm7_bulk_20261030 as inventory
from project import ROOT,sha256


def boundaries(entry):
    identity=(entry.get('program'),entry.get('processor'),entry.get('module'),entry.get('mode'),entry.get('address'),entry.get('bytes'))
    if identity!=('','arm7','arm7-main','arm','0x27e8c78',216):raise ValueError('Exact node initializer identity differs')
    specs=[s for s in inventory.specs() if not s['program']];own=next(s for s in specs if s['address']==0x027e8c78 and s['mode']=='arm')
    if own['bytes']!=216 or own['pools']!={0x027e8d4c:0x0380fff4} or any(i.mnemonic=='bl' and i.operands[0].imm not in (0x027e8c5c,0x037f886c) for i in own['instructions']):raise ValueError('Own code/pool or callee targets differ')
    refs=[];interiors=[]
    for spec in specs:
        for instruction in spec['instructions']:
            if not instruction.mnemonic.startswith('b') or not instruction.operands or instruction.operands[0].type!=2:continue
            target=instruction.operands[0].imm&~1
            if not 0x027e8c78<=target<0x027e8d50 or 0x027e8c78<=instruction.address<0x027e8d50:continue
            record=dict(module=spec['module'],function=hex(spec['address']),mode=spec['mode'],site=hex(instruction.address),target=hex(target),instruction=instruction.mnemonic)
            refs.append(record)
            if target!=0x027e8c78:interiors.append(record)
    if interiors or not refs:raise ValueError('Unexpected direct interior reference or no measured caller')
    caller=next(s for s in specs if s['address']==0x027e89ec and s['mode']=='arm');calls=[i for i in caller['instructions'] if i.mnemonic=='bl' and i.operands[0].imm==0x027e8c78]
    if len(calls)!=1:raise ValueError('Unique qualified constructor call differs')
    index=caller['instructions'].index(calls[0]);argument=caller['instructions'][index-1]
    if argument.mnemonic!='add' or argument.op_str!='r0, r4, #0x20':raise ValueError('Constructor descriptor-word argument producer differs')
    return dict(identity={key:entry[key] for key in ('program','processor','module','mode','address','bytes')},inputModuleSha256=entry['inputModuleSha256'],codeStart='0x27e8c78',codeEnd='0x27e8d4c',
        literalStart='0x27e8d4c',literalBytes=4,literalValue='0x380fff4',ordinaryCodeBytes=212,directOutsideReferences=refs,directInteriorReferences=[],
        constructorArgumentProducer=dict(entry='0x27e89ec',site=hex(argument.address),callSite=hex(calls[0].address),argument='incoming descriptor address plus0x20',wordsRead=3,actualEnclosingConstructorReturnClaim=False),
        acceptedInitializerDependency=dict(address='0x27e8c5c',bytes=28,source='src/arm7/translated03/native_arm7_main_027e8c5c.c',sha256=sha256(ROOT/'src/arm7/translated03/native_arm7_main_027e8c5c.c'),contract='u32(void*,s16); caller constants2..12 fit signed16'),
        opaqueOrIndirectReferenceCompleteness=False,completeImageOrProgramCoverage=False,sourceCredit=0)
