import os
import re
import subprocess
from project import ROOT, read_json, write_json, sha256
from slice_reference_sdk_entities_v3_20261102 import functions, slice_closed
from link_runtime_unit import relocation_rows


def main():
    output = ROOT / 'evidence/attempts/main-arrange760-recursive-closure-20261102.json'
    assert not output.exists()
    previous = read_json(ROOT / 'evidence/attempts/main-sdk-visibility-v4-breadth-20261102.json')
    raw = next(r for r in previous['preprocessed'] if r['source'].endswith('g2d_CharCanvas.c') and r['profile'] == 'base4p')
    path = ROOT / raw['output']
    assert sha256(path) == raw['outputSha256']
    text = path.read_text(encoding='utf-8')
    seed = 'NNS_G2dArrangeOBJ1D'
    records = functions(text)
    own = next(r for r in records if r['name'] == seed)
    assert not re.search(r'\bstatic\b', text[own['start']:own['opening']])
    for record in sorted(records, key=lambda r: r['start'], reverse=True):
        header = text[record['start']:record['opening']]
        if record['name'] == seed or re.search(r'\binline\b', header): continue
        header = re.sub(r'\bstatic\s+', '', header)
        text = text[:record['start']] + header.rstrip() + ';\n' + text[record['end']:]
    text, selection = slice_closed(text, [seed])
    if selection['forbiddenTokens']:
        write_json(output, dict(sourceCredit=0, admittedAsOrdinaryC=False, forbiddenTokens=selection['forbiddenTokens'], sourceLines=len(text.splitlines()), rawExpandedSourceSha256=sha256(path), reason='Original inline assembly requires separate provenance and cannot pass ordinary C admission'))
        print(dict(sourceCredit=0, refusedOrdinaryC=True, forbiddenTokens=selection['forbiddenTokens']))
        return
    assert len(text.splitlines()) <= 500
    source = ROOT / 'nonmatching/main/20261102-arrange760-recursive-closure/source.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    original = next(r for r in read_json(ROOT / 'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json')['candidates']
        if r['identity']['address'] == '0x2036538' and r['profile'] == 'base4p')
    flags, index = [], 0
    while index < len(original['compilerFlags']):
        flag = original['compilerFlags'][index]
        if flag == '-i': index += 2; continue
        if flag.startswith('-D'): index += 1; continue
        flags.append(flag); index += 1
    obj = ROOT / 'work/main-arrange760-recursive-closure/compiled.o'
    obj.parent.mkdir(parents=True, exist_ok=True)
    run = subprocess.run([str(ROOT / original['compiler']), *flags, '-c', str(source), '-o', str(obj)],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    result = dict(sourceCredit=0, identity=original['identity'], source=source.relative_to(ROOT).as_posix(),
        sourceSha256=sha256(source), rawExpandedSourceSha256=sha256(path), exitCode=run.returncode,
        stdout=run.stdout, stderr=run.stderr, selection=selection, compiler=original['compiler'], compilerFlags=flags,
        recursiveGlobalDefinitionPreserved=True, globalStaticRemovalRegexNotApplied=True)
    if run.returncode == 0:
        result.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj), relocations=relocation_rows(obj, seed))
    write_json(output, result)
    print(dict(compiling=run.returncode == 0, sourceLines=len(text.splitlines()), sourceCredit=0))


if __name__ == '__main__':
    main()
