import itertools
from project import ROOT, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    source = ROOT / 'nonmatching/main-runtime/20261031-near-frontier85/0x2029758/source.c'
    original = source.read_text(encoding='utf-8')
    declarations = ['s32 temp_r8;', 'u32 temp_r0;', 'u32 var_r4;', 'u32 var_r6;']
    assert all(original.count('    ' + item + '\n') == 1 for item in declarations)
    output, exact = [], []
    for alias in [True, False]:
        items = [*declarations, *(['void *context;'] if alias else [])]
        for index, order in enumerate(itertools.permutations(items)):
            body = original
            for item in declarations:
                body = body.replace('    ' + item + '\n', '')
            signature, remainder = body.split(' {\n', 1)
            if alias:
                remainder = remainder.replace('arg0', 'context')
            body = signature + ' {\n' + ''.join('    ' + item + '\n' for item in order)
            body += ('    context = arg0;\n' if alias else '') + remainder
            label = f'{int(alias)}-{index:03}'
            path = ROOT / f'nonmatching/main-runtime/20261031-context-declarations/{label}/source.c'
            path.parent.mkdir(parents=True, exist_ok=True)
            assert not path.exists() or path.read_bytes() == body.encode()
            path.write_bytes(body.encode())
            compiler.WORK = ROOT / f'work/main-context-declarations-20261031/{label}/compile'
            rows, unused = compiler.compare(path, 'main', 2, 'off', True)
            assert len(rows) == 1
            row = rows[0]
            result = dict(label=label, declarations=list(order), contextAlias=alias,
                          sourceSha256=sha256(path), match=row, genuineLinkExact=False)
            if row.get('compiledBytes') == 136 and row.get('matchingBytes') == 136:
                result['proof'] = validate(row, qualified_bindings(row), compiler.WORK.parent / 'link')
                result['genuineLinkExact'] = True
                exact.append(label)
            output.append(result)
            if result['genuineLinkExact']:
                print(dict(exact=label, tested=len(output), declarations=order), flush=True)
                break
        if exact:
            break
    write_json(ROOT / 'evidence/attempts/main-context-declarations-20261031.json',
               dict(results=output, exact=exact, nativeExecutionCount=0, sourceCredit=0,
                    limits=['Only ordinary local declaration ordering/context naming is varied',
                            'Nonmatching compiler scores are not linked-byte matches']))
    print(dict(tested=len(output), genuineExact=exact), flush=True)


if __name__ == '__main__':
    main()
