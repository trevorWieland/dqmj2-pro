import json
import re
from pathlib import Path
import utility_code
import utility_runtime
import reuse_utility_c as reuse
from wave20261102_child_third_prepare import ROOT, WORK
from project import sha256


def closure(source):
    pending, paths, links = [source], set(), {}
    while pending:
        path = pending.pop().resolve()
        if path in paths:
            continue
        if not path.is_relative_to(ROOT / 'src'):
            raise ValueError('Origin include escapes accepted source tree')
        text = path.read_text()
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
            raise ValueError('Origin source/header is not bounded comment-free ordinary C')
        if re.search(r'^\s*#\s*include\s*<', text, re.M):
            raise ValueError('Origin has an implicit system include')
        paths.add(path)
        for include in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"', text, re.M):
            target = (path.parent / include).resolve()
            if not target.is_file():
                raise ValueError('Missing origin include')
            links[path, include] = target
            pending.append(target)
        if len(paths) > 80:
            raise ValueError('Origin include closure exceeds bounded adaptation scope')
    return sorted(paths), links


def snapshot(origin, spec, native, directory):
    source = ROOT / origin['source']
    if sha256(source) != origin['sourceSha256']:
        raise ValueError('Origin source changed')
    paths, links = closure(source)
    text = '\n'.join(p.read_text() for p in paths)
    layout, unused = utility_runtime.derive()
    rename = reuse.replacements(origin, spec, native, layout['modules'], text)
    if rename is None:
        raise ValueError('Measured relocations do not admit one consistent symbol adaptation')
    directory.mkdir(parents=True, exist_ok=True)
    destinations = {source.resolve(): directory / (spec['name'] + '.c')}
    for index, path in enumerate(p for p in paths if p != source.resolve()):
        destinations[path] = directory / ('dependency%03d.h' % index)
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, rename)) + r')\b')
    provenance = []
    for path in paths:
        text = pattern.sub(lambda match: rename[match[0]], path.read_text())
        def include(match):
            target = links[path, match[1]]
            return '#include "' + destinations[target].name + '"'
        text = re.sub(r'^\s*#\s*include\s*"([^"<>]+)"', include, text, flags=re.M)
        destination = destinations[path]
        if destination.exists() and destination.read_text() != text:
            raise ValueError('Refusing adapted source overwrite')
        if not destination.exists():
            destination.write_text(text)
        provenance.append(dict(source=path.relative_to(ROOT).as_posix(), sourceSha256=sha256(path),
            adapted=destination.relative_to(ROOT).as_posix(), adaptedSha256=sha256(destination)))
    dependencies = [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p))
                    for original, p in destinations.items() if original != source.resolve()]
    return destinations[source.resolve()], dependencies, provenance


def validate_candidate(origin, spec, native, tag):
    directory = WORK / 'adapted' / ('%08x' % spec['address']) / tag
    source, dependencies, provenance = snapshot(origin, spec, native, directory)
    flags = origin['compilerFlags']
    configured = dict(spec, compilerPath=ROOT / origin['compiler'],
        compilerProc=flags[flags.index('-proc') + 1], interworking='-nointerworking' not in flags)
    row, code = utility_code.compile_compare(source, configured, flags[0][2:],
        flags[flags.index('-inline') + 1], 'speed' in flags)
    row.update(sourceDependencies=dependencies, sourceReuseProvenance=provenance,
        sourceAdaptationMethod='accepted ordinary C translated by measured full-extent relocation fingerprint')
    return row, code
