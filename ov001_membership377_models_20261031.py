import ov001_recruit373_models_20261031 as OLD
from ov001_recruit373_models_20261031 import BASE,RECORDS,PARAMS,ACTOR_BASES,read


def recipes():
    source=OLD.standalone_recipes()[1]
    cases=[]
    for uid in[0,101,103,200,999,0xFFFFFFFF]:
        for active,reserve in[([],[]),([101],[]),([],[101]),([103],[105]),([101,103],[200]),([999],[]),([0],[0]),([101],[101])]:
            cases.append(dict(source,seed=377000+len(cases),actorUid=uid,active=active,reserve=reserve,nullActor=False))
    for active in[[],[999],[0]]:cases.append(dict(source,seed=377000+len(cases),actorUid=0,active=active,reserve=[],nullActor=True))
    return cases


def setup(obj,recipe):
    OLD.setup(obj,recipe)
    obj.word(PARAMS,recipe['actorUid'])
    return 0 if recipe.get('nullActor')else ACTOR_BASES[0]


def expected(before,actor):
    records={read(before,RECORDS-BASE+132*i+20,4)for i in range(100)}-{0}
    groups={read(before,0x021BD540-BASE+4*i,4)for i in range(6)}&records
    if not groups:return 1
    if not actor:raise ValueError('Membership377 null actor with resolved group remains unsupported')
    pointer=read(before,actor-BASE+0x1E8,4)
    ident=read(before,pointer-BASE,4)
    return int(ident not in groups)
