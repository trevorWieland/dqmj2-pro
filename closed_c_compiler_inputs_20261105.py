import re
from project import ROOT, sha256


def compiler_inputs(row):
    source = (ROOT / row['source']).resolve()
    assert source.is_relative_to(ROOT / 'src') and source.suffix == '.c' and sha256(source) == row['sourceSha256']
    headers = row['sourceDependencies']
    assert isinstance(headers, list)
    if not headers:
        text = source.read_text(encoding='utf-8')
        assert not any(token in text for token in ['#', '\\', '??'])
        assert not any(str(flag).startswith(('-include', '-prefix', '-I', '@')) for flag in row['compilerFlags'])
        assert not any(str(flag).startswith('-i') and not str(flag).startswith(('-inline', '-interworking', '-ipa')) for flag in row['compilerFlags'])
    allowed = {source}
    for pin in headers:
        path = (ROOT / pin['path']).resolve()
        assert path.is_relative_to(ROOT / 'src') and path.suffix == '.h' and sha256(path) == pin['sha256']
        allowed.add(path)
    for path in allowed:
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b|\.incbin', text)
        assert not any(t in text for t in ['??', '%:', '\0'])
        assert not re.search(r'\\\r?\n', text)
        for line in text.splitlines():
            if re.match(r'^\s*#\s*(?:include|include_next|import|embed)\b', line):
                found = re.fullmatch(r'\s*#\s*include\s+"([^"<>]+)"\s*', line)
                assert found and (path.parent / found[1]).resolve() in allowed
        for include in re.findall(r'^\s*#include\s+"([^"]+)"', text, re.M):
            assert (path.parent / include).resolve() in allowed
        assert not re.search(r'^\s*#include\s*<', text, re.M)
    flags = row['compilerFlags']
    assert not any(str(f).startswith(('-include', '-prefix', '-I', '@')) for f in flags)
    assert not any(str(f).startswith('-i') and not str(f).startswith(('-inline', '-interworking', '-ipa')) for f in flags)
    assert not any(str(flag).lower().endswith(('.bin', '.nds', '.o', '.s', '.inc')) or
                   any(part in str(flag).replace('\\', '/') for part in ['extract/', 'inputs/', 'asm/']) for flag in flags)
    assert not any(flag in flags for flag in ['-include', '-prefix', '-i', '-I'])
    return dict(originalCodeCompilerInput=False, source=row['source'], sha256=row['sourceSha256'], includes=headers)
