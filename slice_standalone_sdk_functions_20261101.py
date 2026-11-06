import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

NONCODE = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)


def functions(text):
    mask = NONCODE.sub(lambda match: ' ' * len(match.group()), text)
    mask = re.sub(r'(?m)^\s*#.*$', lambda match: ' ' * len(match.group()), mask)
    depth, start, opening, name = 0, 0, 0, None
    result = []
    for index, char in enumerate(mask):
        if char == '{':
            if depth == 0:
                header = mask[start:index].rstrip()
                name = None
                if header.endswith(')') and '=' not in header:
                    balance = 0
                    for at in range(len(header)-1, -1, -1):
                        if header[at] == ')': balance += 1
                        elif header[at] == '(':
                            balance -= 1
                            if balance == 0:
                                found = re.search(r'([A-Za-z_]\w*)\s*$', header[:at])
                                name = found[1] if found else None
                                break
                opening = index
            depth += 1
        elif char == '}':
            depth -= 1
            assert depth >= 0
            if depth == 0 and name:
                result.append(dict(name=name,start=start,end=index+1,opening=opening))
                start, name = index+1, None
        elif char == ';' and depth == 0:
            start = index+1
    assert depth == 0
    assert len({item['name'] for item in result}) == len(result)
    return result


def main():
    original = ROOT / 'generated/recovery/20261101-reference-oam-standalone/native_main_0203716c.c'
    text = original.read_text(encoding='utf-8')
    records = functions(text)
    mapping = {row['name']: row for row in records}
    selected, pending = set(), ['native_main_0203716c']
    while pending:
        name = pending.pop()
        if name in selected: continue
        selected.add(name)
        row = mapping[name]
        names = set(re.findall(r'\b[A-Za-z_]\w*\b', text[row['opening']:row['end']]))
        pending.extend((names & set(mapping)) - selected)
    removed = [row for row in records if row['name'] not in selected]
    for row in sorted(removed,key=lambda row:row['start'],reverse=True):
        fragment = text[row['start']:row['end']]
        directives = '\n'.join(line for line in fragment.splitlines() if line.lstrip().startswith('#'))
        text = text[:row['start']] + '\n' + directives + '\n' + text[row['end']:]
    assert not re.search(r'\b(?:va_list|size_t|J2pUnknownVaList)\b', text) and '#include' not in text
    source = ROOT / 'generated/recovery/20261101-reference-oam-sliced/native_main_0203716c.c'
    assert not source.exists()
    source.parent.mkdir(parents=True,exist_ok=True)
    source.write_text(text,encoding='utf-8')
    compiler.FLAGS += ['-lang','c99','-ipa','file']
    compiler.WORK = ROOT / 'work/main-reference-oam-sliced-20261101/compile'
    rows,unused = compiler.compare(source,'main','4,p','on,noauto',compiler=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    row = rows[0]
    if row.get('compileFailed'):proof=None;exact=False
    else:
        try:proof=validate(row,qualified_bindings(row),ROOT/'work/main-reference-oam-sliced-20261101/genuine-link');exact=True
        except ValueError as error:proof=error.args[0];exact=False
    write_json(ROOT/'evidence/attempts/main-reference-oam-function-slice-20261101.json',dict(sourceCredit=0,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),
        input=original.relative_to(ROOT).as_posix(),inputSha256=sha256(original),
        source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
        keptDefinitions=sorted(selected),removedDefinitions=[row['name']for row in removed],
        compilation=row,genuineLinkComparison=proof,exact=exact,sourceAndTypeReviewPending=True))
    print(dict(definitions=len(records),kept=len(selected),removed=len(removed),lines=len(text.splitlines()),exact=exact))
    if row.get('compileFailed'):print(row.get('stdout','')[:1800])


if __name__ == '__main__':
    main()
