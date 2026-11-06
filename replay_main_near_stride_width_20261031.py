from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    inputs = read_json(ROOT / 'evidence/verification/main-near-frontier85-inputs-20261031.json')
    selected = {row['address']: row for row in inputs['candidates']}
    fixes = {
        '0x202e380': ('arg0 + 4', 'arg0 + 1'),
        '0x203c5b8': ('M2C_FIELD(var_r4, s32 **, 0) + 4', 'M2C_FIELD(var_r4, s32 **, 0) + 1'),
        '0x2037b94': ('arg0 + 4', 'arg0 + 1'),
        '0x2005bd8': ('return *var_r2;', 'return *(u32 *)var_r2;'),
    }
    results = []
    for address, (old, new) in fixes.items():
        original = ROOT / selected[address]['source']
        assert sha256(original) == selected[address]['sourceSha256']
        body = original.read_text(encoding='utf-8')
        assert old in body
        body = body.replace(old, new)
        path = ROOT / f'nonmatching/main-runtime/20261031-near-frontier85-fixed/{address}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != body.encode():
            raise ValueError('Earlier corrected source differs')
        path.write_bytes(body.encode())
        compiler.WORK = ROOT / f'work/main-near-frontier85-fixed-20261031/{address}/compile'
        rows, unused = compiler.compare(path, 'main', 2, 'off', True)
        assert len(rows) == 1
        proof = validate(rows[0], qualified_bindings(rows[0]), compiler.WORK.parent / 'link')
        results.append(dict(match=rows[0], proof=proof))
    write_json(ROOT / 'evidence/attempts/main-near-frontier85-stride-and-width-20261031.json',
               dict(results=results, sourceCredit=0, registered=False, nativeExecutionCount=0))
    print(dict(genuineLinks=len(results), initializedBytes=sum(r['match']['bytes'] for r in results)))


if __name__ == '__main__':
    main()
