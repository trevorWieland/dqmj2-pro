import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from project import ROOT,sha256
from slice_reference_sdk_entities_v3_20261102 import functions,NONCODE


def normalized(text):
    return re.sub(r'\s+', '', text.replace(chr(92) + chr(10), ''))


def include_paths(text):
    result = set()
    for encoded in re.findall(r'^#line\s+\d+\s+("(?:\\.|[^"\\])*")', text, re.M):
        name = json.loads(encoded)
        if name.startswith('('):
            continue
        path = Path(name).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(), name
        result.add(path.relative_to(ROOT).as_posix())
    return result


def verify(item, source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    published = item['publishedInput']
    flags = published['flags'][:]
    for index in range(len(flags) - 1):
        if flags[index] == '-i':
            assert not Path(flags[index + 1]).is_absolute()
            flags[index + 1] = str(ROOT / flags[index + 1])
    output = directory / 'fresh-published.i'
    if output.exists():
        output.unlink()
    command = [str(ROOT / item['compilerPath']), *flags, '-E', str(ROOT / published['source']), '-o', str(output)]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120, env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    assert process.returncode == 0, (process.stdout,process.stderr)
    text = output.read_text()
    actual_includes = include_paths(text)
    assert actual_includes == set(published['dependencies']), sorted(actual_includes.symmetric_difference(published['dependencies']))
    text = NONCODE.sub(lambda m:(' '+'\n'*m[0].count('\n')) if m[0].startswith('/') else m[0],text)
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#')) + '\n'
    candidates = [f for f in functions(text) if f['name'] == item['referenceFunction']]
    assert len(candidates) == 1
    function = candidates[0]
    declaration = text[function['start']:function['opening']]
    assert re.search(r'\basm\b', declaration)
    body = text[function['opening']+1:function['end']-1]
    for name,alias in sorted(item['provenance']['measuredAliases'].items(),key=lambda pair:len(pair[0]),reverse=True):
        if re.fullmatch(r'[A-Za-z_]\w*',name):
            body = re.sub(r'\b'+re.escape(name)+r'\b',alias,body)
    authored = source.read_text()
    authored_body = authored[authored.index('{')+1:authored.rfind('}')]
    assert normalized(body) == normalized(authored_body), 'Published assembly statements changed beyond measured aliases/formatting'
    raw = (ROOT / published['source']).read_text()
    assert normalized(item['assemblyJustification']['publishedAsmDeclaration']) in normalized(raw)
    assert sha256(ROOT / published['source']) == item['assemblyJustification']['publishedSourceSha256']
    return dict(freshPublishedPreprocessing=True,actualPublishedIncludeFiles=len(actual_includes),allIncludesDeclaredAndFrozen=True,publishedExplicitAsmDeclaration=True,bodyTokensEqualAfterMeasuredAliasesAndWhitespace=True,normalizedBodySha256=hashlib.sha256(normalized(body).encode()).hexdigest(),restoredPublishedLineContinuations=item['provenance']['restoredPublishedAsmLineContinuations'],sourceStatementsDerivedFromPublishedSdkNotDisassembly=True,instructionOrObjectPatches=False,callerCalleeHardwareExecutionCredit=0)
