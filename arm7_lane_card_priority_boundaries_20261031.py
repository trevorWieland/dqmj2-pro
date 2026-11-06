import match_arm7


def boundaries(entry,layout):
    address=int(entry['address'],0)
    if entry.get('program','') or entry.get('processor')!='arm7' or entry.get('module')!='arm7-wram' or address!=0x038026e0:
        raise ValueError('Qualified canonical CARD priority entry differs')
    spec=match_arm7.accepted_spec(entry,True)
    if spec['bytes']!=64 or spec['mode']!='arm' or entry['bytes']!=64 or entry['codeBytes']!=60:
        raise ValueError('Complete original CARD priority span differs')
    if {i.address for i in spec['instructions']}!=set(range(address,address+60,4)):
        raise ValueError('CARD priority instruction/pool qualification differs')
    return dict(canonicalOriginalScope=True,completeAddress=entry['address'],completeBytes=64,
        instructionBytes=60,literalBytes=4,originalModuleSha256=entry['inputModuleSha256'],additionalInitializedDenominatorBytes=0,
        limitations='Original canonical entry and complete instruction/pool extents, without a whole-program indirect caller claim')
