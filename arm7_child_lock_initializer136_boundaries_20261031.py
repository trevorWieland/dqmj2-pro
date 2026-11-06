import audit_arm7_bulk_20261030 as inventory


def boundaries(entry):
    identity=tuple(entry.get(k) for k in ('program','processor','module','mode','address','bytes'))
    if identity!=('dwc/utility.bin/move/child.srl','arm7','utility-child-arm7-wram','arm','0x37fc0b8',136):raise ValueError('Exact child lock initializer scope differs')
    specs=[s for s in inventory.specs() if s['program']==identity[0]];own=next(s for s in specs if s['address']==0x037fc0b8 and s['mode']=='arm')
    if own['bytes']!=136 or sorted(own['pools'])!=list(range(0x037fc130,0x037fc140,4)) or set(own['pools'].values())!={0x038059b8,0x027ffff0,0x027fffb8,0x027fffbc}:raise ValueError('Current full code/literal layout differs')
    references=[]
    for spec in specs:
        for instruction in spec['instructions']:
            if not instruction.mnemonic.startswith('b') or not instruction.operands or instruction.operands[0].type!=2:continue
            target=instruction.operands[0].imm&~1
            if not 0x037fc0b8<=target<0x037fc140 or 0x037fc0b8<=instruction.address<0x037fc140:continue
            if target!=0x037fc0b8:raise ValueError('External direct branch enters a child initializer interior or pool')
            references.append(dict(module=spec['module'],caller=hex(spec['address']),mode=spec['mode'],site=hex(instruction.address),target=hex(target)))
    if not references:raise ValueError('Expected original direct caller missing')
    return dict(program=identity[0],processor='arm7',module=identity[2],mode='arm',address=identity[4],bytes=136,
        codeStart='0x37fc0b8',codeEnd='0x37fc130',codeBytes=120,literalStart='0x37fc130',literalBytes=16,
        inputModuleSha256=entry['inputModuleSha256'],directOutsideReferences=references,directInteriorReferences=[],indirectReferenceCompleteness=False,
        ordinaryWaitSourceCredit=0,originalObjectExtentOrDataCredit=0,wholeImageCoverage=False)
