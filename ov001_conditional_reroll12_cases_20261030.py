import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, ATTACKER_RECORD

MASK = 0xFFFFFFFF
SKILLS = ([], [40], [41], [40, 41], [40, 0, 41], [41] * 64)


def recipes():
    rows = [dict(skills=skills, current=current, maximum=maximum, limit=limit, threshold=threshold, initial=initial)
            for skills, current, maximum, (limit, threshold), initial
            in product(SKILLS, (-32768, -1, 0, 1, 249, 250, 750, 751, 32767), (-32768, -1, 0, 1, 1000, 9999, 32767),
                       ((10, 2), (100, 5)), (0, MASK))]
    rows += [dict(skills=skills, current=current, maximum=maximum, limit=limit, threshold=threshold, initial=initial)
             for skills, (current, maximum), limit, threshold, initial in product(SKILLS, ((1, 1000), (900, 1000)),
                 (-2147483648, -1, 0, 1, 10, 100, 2147483647), (-2147483648, -1, 0, 1, 2, 10, 100, 2147483647), (0, MASK))]
    return rows


def vectors():
    output = []
    for index, recipe in enumerate(recipes()):
        actor, saved = bytearray(1088), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
        struct.pack_into('<h', actor, 0x1F0, recipe['current'])
        struct.pack_into('<h', actor, 0x21C, recipe['maximum'])
        saved[0x46:0x86], saved[0x86] = bytes((recipe['skills'] + [0] * 64)[:64]), 40
        skills = recipe['skills'][:64]
        if 0 in skills:
            skills = skills[:skills.index(0)]
        state, draws, protocols = recipe['initial'], [], []

        def draw():
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & MASK
            value = (state >> 16) % recipe['limit'] if recipe['limit'] > 0 else 0
            draws.append((recipe['limit'], value))
            return value

        first = draw()
        success = first < recipe['threshold']
        skill = 41 if success else 40
        count = skills.count(skill)
        protocols.append(dict(address=0x0207B674, arguments=[skill, ATTACKER_RECORD + 0x46], returnWord=count))
        maximum, current = min(recipe['maximum'], 9999), recipe['current']
        if count:
            protocols += [dict(address=0x021DBD24, arguments=[ATTACKER], returnWord=current & MASK),
                          dict(address=0x021DBCBC, arguments=[ATTACKER], returnWord=maximum & MASK)]
            protocols += [dict(address=0x0207B674, arguments=[skill, ATTACKER_RECORD + 0x46], returnWord=0)
                          for skill in range(128, 138)]
            reroll = maximum * 3 <= current * 4 if success else maximum >= current * 4
            if reroll:
                success = draw() < recipe['threshold']
        output.append(dict(**recipe, physicalR0=int(success), initialDraw=first, seed=2140000 + index, draws=draws, protocols=protocols,
            arguments=[ATTACKER, recipe['limit'], recipe['threshold']],
            memory=[(ATTACKER, bytes(actor)), (ATTACKER_RECORD, bytes(saved)), (0x020F6044, struct.pack('<I', recipe['initial']))],
            patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
