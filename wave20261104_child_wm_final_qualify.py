HELPER_NAMES = set()


def qualified():
    return []


def helper_target(name, spec):
    raise ValueError('Compiler helper has no qualification in this packet')


def validate_relocations(row):
    if any(r['symbol'].startswith(('_s32', '_ll_', '_u32', '__aeabi')) for r in row['relocations']):
        raise ValueError('Unexpected compiler helper has no qualified original caller contract')
