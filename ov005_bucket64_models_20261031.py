from functools import cache

RNG_STATE, PROGRESS, OUTPUT = 0x020F6044, 0x021C0DC8, 0x021B9E94
TABLES = [(10, 0, 0, 0), (5, 10, 0, 0), (2, 7, 10, 0), (0, 3, 7, 10)]


def next_state(value):
    return (value * 0x41C64E6D + 0x3039) & 0xFFFFFFFF


@cache
def recipes():
    seeds = {}
    seed = 0
    while len(seeds) < 100:
        first = next_state(seed)
        second = next_state(first)
        seeds.setdefault(((first >> 16) % 10, (second >> 16) % 10), seed)
        seed += 1
        if seed > 100000:
            raise ValueError('Bucket64 deterministic seed search bound exceeded')
    profiles = [(0, 0), (10, 28), (11, 28), (12, 28), (13, 28), (255, 28), (13, 29), (255, 255)]
    return [dict(seed=0x164000 + profile * 100 + index, rngWord=word, progress0=values[0], progress20=values[1], draws=list(draws))
        for profile, values in enumerate(profiles) for index, (draws, word) in enumerate(sorted(seeds.items()))]


def model(recipe):
    table = int(recipe['progress0'] >= 11) + int(recipe['progress0'] >= 13)
    if recipe['progress20'] >= 29:
        table = 3
    first = next_state(recipe['rngWord'])
    second = next_state(first)
    draws = ((first >> 16) % 10, (second >> 16) % 10)
    if list(draws) != recipe['draws']:
        raise ValueError('Bucket64 explicit independent seed pair differs')
    bucket = next((index for index, upper in enumerate(TABLES[table]) if draws[0] < upper), 0)
    base = (23, 23, 24, 25)[bucket]
    extra = int(bucket in (1, 2) and draws[1] < 5 or bucket == 3 and draws[1] < 3)
    return dict(table=table, bucket=bucket, output=base + extra, rngAfter=second, draws=list(draws))
