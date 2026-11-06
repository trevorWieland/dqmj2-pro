import struct

from ov001_ability28_fixture_20261031 import RULES, ACTOR, RECORD

MASK, RNG = 0xFFFFFFFF, 0x020F6044


def recipes():
    rows = []
    identifiers = [row[0] for row in RULES]
    for traits in ([], [40], [41], [40, 41]):
        for current in (0, 250, 750, 751):
            for initial in (0, 1, MASK, 0x12345678, 0x80000000, 0xAE51203D):
                rows.append(dict(skills=identifiers + traits, current=current, maximum=1000, initial=initial))
    for identifier, unused, unused2, unused3 in RULES:
        for traits, current in (([40], 0), ([41], 751)):
            rows.append(dict(skills=[identifier] + traits, current=current, maximum=1000, initial=0xFFFFFFFF))
    for skills in ([], [42] * 64, [42, 40] * 32, [42, 0] + identifiers + [40, 41]):
        for current, maximum in ((-32768, -32768), (32767, 32767), (-1, 0)):
            rows.append(dict(skills=skills, current=current, maximum=maximum, initial=0x80000000))
    for index, row in enumerate(rows):
        row.update(flags=(0, MASK, 0x55555555, 0xAAAAAAAA)[index % 4], seed=0x130000 + index)
    return rows


def vectors():
    output = []
    for recipe in recipes():
        actor, saved = bytearray(0x440), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, RECORD)
        struct.pack_into('<h', actor, 0x1F0, recipe['current'])
        struct.pack_into('<h', actor, 0x21C, recipe['maximum'])
        struct.pack_into('<I', actor, 0x33C, recipe['flags'])
        saved[0x46:0x86] = bytes((recipe['skills'] + [0] * 64)[:64])
        saved[0x86] = 40
        skills = list(saved[0x46:0x86])
        if 0 in skills:
            skills = skills[:skills.index(0)]
        state, draws, protocols, flags, result = recipe['initial'], [], [], recipe['flags'], 0
        decisions = []

        def call(address, arguments, returned):
            item = dict(address=address, arguments=arguments, returnWord=returned & MASK)
            protocols.append(item)
            return item

        def lookup(identifier):
            count = skills.count(identifier)
            call(0x0207B674, [identifier, RECORD + 0x46], count)
            return count

        def draw(limit):
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & MASK
            value = (state >> 16) % limit
            draws.append((limit, value))
            return value

        for identifier, limit, threshold, mask in RULES:
            if lookup(identifier) == 0:
                decisions.append(dict(identifier=identifier, lookupCount=0, gateEntered=False))
                continue
            marker = call(0x02210AD0, [ACTOR, limit, threshold], 0)
            before = len(draws)
            initial_draw = draw(limit)
            success = initial_draw < threshold
            reroll_trait = lookup(41 if success else 40)
            if not success and not reroll_trait:
                call(0x0207D988, [0], 0)
            if reroll_trait:
                maximum, current = min(recipe['maximum'], 9999), recipe['current']
                call(0x021DBD24, [ACTOR], current)
                call(0x021DBCBC, [ACTOR], maximum)
                for skill in range(128, 138):
                    if lookup(skill):
                        raise ValueError('Native30 maximum-scalar extras require separate modeling')
                if (maximum * 3 <= current * 4 if success else maximum >= current * 4):
                    success = draw(limit) < threshold
            marker['returnWord'] = int(success)
            if success:
                flags |= mask
                result = 1
            decisions.append(dict(identifier=identifier, gateEntered=True, initialDraw=initial_draw,
                rngDraws=len(draws) - before, success=success, flagsAfter=flags))
        output.append(dict(**recipe, physicalR0=result, finalState=state, finalFlags=flags, decisions=decisions,
            draws=draws, protocols=protocols, arguments=[ACTOR],
            memory=[(ACTOR, bytes(actor)), (RECORD, bytes(saved)), (RNG, struct.pack('<I', recipe['initial']))],
            patches=[(RNG, struct.pack('<I', state)), (ACTOR + 0x33C, struct.pack('<I', flags))]))
    return output
