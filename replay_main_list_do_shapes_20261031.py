import re
from project import ROOT, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def bodies():
    base = ROOT / 'nonmatching/main-runtime/20261031-near-frontier85'
    body = (base / '0x202eb4c/source.c').read_text(encoding='utf-8')
    body = body.replace('loop_5:', '        do {')
    body = re.sub(r'        if \(var_r2 == NULL\) \{\s*return 0U;\s*\}\s*goto loop_5;',
                  '        } while (var_r2 != NULL);', body)
    yield 'remove-do', body
    body = (base / '0x202b884/source.c').read_text(encoding='utf-8')
    body = body.replace('extern u32 native_fn_0202bb88();', 'extern u8 *native_fn_0202bb88(u8 *context, u8 *previous);')
    body = body.replace('loop_1:', '        do {')
    body = re.sub(r'        if \(var_r4 == NULL\) \{\s*return 0U;\s*\}\s*goto loop_1;',
                  '        } while (var_r4 != NULL);', body)
    yield 'search-do', body
    body = (base / '0x202e9ac/source.c').read_text(encoding='utf-8')
    body = body.replace('u32 native_main_0202e9ac(', 'void native_main_0202e9ac(')
    body = re.sub(r'return [^;]+;', 'return;', body)
    body = body.replace('loop_10:', '        do {')
    body = re.sub(r'        if \(var_r2 == NULL\) \{\s*M2C_FIELD\(var_ip, void \*\*, 0x10\) = arg1;\s*return;\s*\}\s*goto loop_10;',
                  '        } while (var_r2 != NULL);', body)
    yield 'insert-do', body


def main():
    results = []
    for name, body in bodies():
        path = ROOT / f'nonmatching/main-runtime/20261031-list-do-shapes/{name}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != body.encode():
            raise ValueError('Frozen trial differs')
        path.write_bytes(body.encode())
        compiler.WORK = ROOT / f'work/main-list-do-shapes-20261031/{name}/compile'
        rows, unused = compiler.compare(path, 'main', 2, 'off', True)
        assert len(rows) == 1
        row = rows[0]
        result = dict(variant=name, sourceSha256=sha256(path), match=row, genuineLinkExact=False)
        try:
            proof = validate(row, qualified_bindings(row), compiler.WORK.parent / 'link')
        except (ValueError, KeyError) as error:
            result['linkFailure'] = str(error)
        else:
            result.update(genuineLinkExact=True, proof=proof)
        results.append(result)
        print(dict(variant=name, bytes=row.get('bytes'), compiled=row.get('compiledBytes'),
                   matching=row.get('matchingBytes'), exact=result['genuineLinkExact']), flush=True)
    write_json(ROOT / 'evidence/attempts/main-list-do-shapes-20261031.json',
               dict(results=results, sourceCredit=0, nativeExecutionCount=0))


if __name__ == '__main__':
    main()
