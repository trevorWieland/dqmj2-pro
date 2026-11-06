import itertools
import random
from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    path = ROOT / 'nonmatching/main-runtime/20261031-slot-register/cached-u8/native_main_02015c70.c'
    report = read_json(ROOT / 'evidence/attempts/main-slot-register-consolidated-20261031.json')
    frozen = next(row for row in report['matches'] if row['source'] == path.relative_to(ROOT).as_posix())
    assert sha256(path) == frozen['sourceSha256']
    base = path.read_text(encoding='utf-8')
    block = base[base.index('    s32 temp_r2;'):base.index('\n\n    var_r4')]
    declarations = block.splitlines()
    order = [4, 2, 5, 0, 1, 6, 3]
    logical = tuple(declarations[index] for index in order)
    available = list(itertools.permutations(declarations))
    random.Random(0x15C70656).shuffle(available)
    orders = [logical, tuple(reversed(logical))]
    orders.extend(item for item in available if item not in orders)
    rows = []
    for index, ordered in enumerate(orders[:96]):
        body = base.replace(block, '\n'.join(ordered))
        source = ROOT / f'nonmatching/main-runtime/20261031-slot-declarations/{index:03}/source.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists() and source.read_bytes() != body.encode():
            raise ValueError('Earlier declaration-order source differs')
        source.write_bytes(body.encode())
        compiler.WORK = ROOT / f'work/main-slot-declarations-20261031/{index:03}/compile'
        result, unused = compiler.compare(source, 'main', 2, 'off', True)
        rows.extend(result)
    best = max(rows, key=lambda row: row.get('matchingBytes', 0))
    try:
        proof = validate(best, qualified_bindings(best), ROOT / 'work/main-slot-declarations-20261031/best-link')
    except ValueError as error:
        link = dict(exact=False, error=str(error))
    else:
        link = dict(exact=True, proof=proof)
    output = dict(input=path.relative_to(ROOT).as_posix(), inputSha256=sha256(path),
                  matches=rows, genuineLink=link, bestSource=best['source'],
                  matchingBytes=best['matchingBytes'], sourceCredit=0, registered=False)
    write_json(ROOT / 'evidence/attempts/main-slot-declarations-20261031.json', output)
    print(dict(attempts=len(rows), matchingBytes=best['matchingBytes'], genuineLinkExact=link['exact']))


if __name__ == '__main__':
    main()
