import re
from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import relocation_rows


def main():
    output = ROOT / 'evidence/attempts/main-gecom-declaration-closure-20261102.json'
    assert not output.exists()
    earlier = read_json(ROOT / 'evidence/attempts/main-sdk-uncovered1112-closure-20261102.json')['results']
    raw = read_json(ROOT / 'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json')['candidates']
    results = []
    for item in earlier:
        if item['referenceFunction'] == 'NNS_G2dArrangeOBJ1D': continue
        address = item['identity']['address']
        seed = next(r for r in raw if r['identity']['address'] == address and r['profile'] == item['profile'])
        original = ROOT / item['source']
        assert sha256(original) == item['sourceSha256']
        text = original.read_text(encoding='utf-8')
        declaration = 'typedef struct NNSG3dGeBuffer_ { u32 idx; u32 data[192]; } NNSG3dGeBuffer;\nstatic NNSG3dGeBuffer * NNS_G3dGeBuffer = ((void *)0);\n'
        text = text.replace('typedef unsigned long u32;\n', 'typedef unsigned long u32;\n' + declaration, 1)
        folder = ROOT / f'nonmatching/main/20261102-gecom-declaration-closure/{address[2:]}'
        folder.mkdir(parents=True, exist_ok=True)
        source = folder / 'source.c'
        source.write_text(text, encoding='utf-8')
        flags, i = [], 0
        while i < len(seed['compilerFlags']):
            flag = seed['compilerFlags'][i]
            if flag == '-i': i += 2; continue
            if flag.startswith('-D'): i += 1; continue
            flags.append(flag); i += 1
        import os, subprocess
        obj = ROOT / f'work/main-gecom-declaration-closure/{address[2:]}.o'
        obj.parent.mkdir(parents=True, exist_ok=True)
        run = subprocess.run([str(ROOT / seed['compiler']), *flags, '-c', str(source), '-o', str(obj)],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        result = dict(identity=item['identity'], source=source.relative_to(ROOT).as_posix(),
            sourceSha256=sha256(source), exitCode=run.returncode, stdout=run.stdout, stderr=run.stderr,
            sourceCredit=0, declarationsDerivedFromOriginalPreprocessedSource=True)
        if run.returncode == 0:
            result.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
                relocations=relocation_rows(obj, seed['referenceFunction']), compiler=seed['compiler'], compilerFlags=flags,
                referenceFunction=seed['referenceFunction'])
        results.append(result)
    write_json(output, dict(sourceCredit=0, results=results, genuineLinkAndNativeProofPending=True))
    print(dict(profiles=len(results), compiling=sum(r['exitCode'] == 0 for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
