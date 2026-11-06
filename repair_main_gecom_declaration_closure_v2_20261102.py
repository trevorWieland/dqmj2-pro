import re
from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from link_runtime_unit import relocation_rows


def main():
    output = ROOT / 'evidence/attempts/main-gecom-declaration-closure-v2-20261102.json'
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
        raw_path = ROOT / 'work/main-sdk-visibility-v4-20261102/preprocess/deps-reference-NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85-libraries-g3d-src-gecom-base4p/expanded.i'
        expanded = raw_path.read_text(encoding='utf-8')
        assert re.search(r'typedef struct NNSG3dGeBuffer_\s*\{\s*u32 idx;\s*u32 data\[192\s*\];\s*\} NNSG3dGeBuffer;', expanded)
        assert re.search(r'static NNSG3dGeBuffer \* NNS_G3dGeBuffer = \(\(void \*\)0\)\s*;', expanded)
        if 'typedef struct NNSG3dGeBuffer_' in text:
            declaration = declaration.split('\n', 1)[1]
            text = text.replace('} NNSG3dGeBuffer;', '} NNSG3dGeBuffer;\n' + declaration, 1)
        else:
            text = text.replace('typedef unsigned long u32;\n', 'typedef unsigned long u32;\n' + declaration, 1)
        folder = ROOT / f'nonmatching/main/20261102-gecom-declaration-closure-v2/{address[2:]}'
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
            sourceCredit=0, declarationsDerivedFromOriginalPreprocessedSource=True, originalExpandedSourceSha256=sha256(raw_path))
        if run.returncode == 0:
            result.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
                relocations=relocation_rows(obj, seed['referenceFunction']), compiler=seed['compiler'], compilerFlags=flags,
                referenceFunction=seed['referenceFunction'])
        results.append(result)
    write_json(output, dict(sourceCredit=0, results=results, genuineLinkAndNativeProofPending=True))
    print(dict(profiles=len(results), compiling=sum(r['exitCode'] == 0 for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
