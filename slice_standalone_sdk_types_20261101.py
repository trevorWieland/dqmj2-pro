import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, write_json, sha256
from slice_standalone_sdk_functions_20261101 import functions, NONCODE
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def declaration_name(text):
    text = re.sub(r'(?m)^\s*#.*$', '', text).strip()
    if not text: return None
    if text.startswith('typedef'):
        pointer = re.search(r'\(\s*\*\s*([A-Za-z_]\w*)\s*\)', text)
        if pointer: return pointer[1]
        tail = text.rsplit('}',1)[-1] if '}' in text else text
        words = re.findall(r'\b[A-Za-z_]\w*\b', tail)
        return words[-1] if words else None
    before = text.rstrip().removesuffix(';').strip()
    if before.endswith(')'):
        depth = 0
        for at in range(len(before)-1,-1,-1):
            if before[at] == ')': depth += 1
            elif before[at] == '(':
                depth -= 1
                if depth == 0:
                    found = re.search(r'([A-Za-z_]\w*)\s*$', before[:at])
                    return found[1] if found else None
    before = before.split('=',1)[0]
    before = before.split('[',1)[0]
    words = re.findall(r'\b[A-Za-z_]\w*\b',before)
    return words[-1] if words else None


def main():
    original = ROOT / 'generated/recovery/20261101-reference-oam-sliced/native_main_0203716c.c'
    text = original.read_text(encoding='utf-8')
    mask = NONCODE.sub(lambda match:' '*len(match.group()),text)
    mask = re.sub(r'(?m)^\s*#.*$',lambda match:' '*len(match.group()),mask)
    definitions = functions(text)
    ranges = {row['start']:row for row in definitions}
    entities, start, index, depth = [], 0, 0, 0
    while index < len(mask):
        if index in ranges:
            row = ranges[index]
            entities.append(dict(start=start,end=row['end'],name=row['name'],kind='function'))
            index,start = row['end'],row['end']
            continue
        char = mask[index]
        if char == '{':depth += 1
        elif char == '}':depth -= 1
        elif char == ';' and depth == 0:
            fragment=text[start:index+1]
            name=declaration_name(fragment)
            entities.append(dict(start=start,end=index+1,name=name,kind='declaration'))
            start=index+1
        index += 1
    assert depth == 0
    by_name = {}
    for row in entities:
        if row['name']:by_name.setdefault(row['name'],[]).append(row)
    selected, pending = set(), ['native_main_0203716c']
    while pending:
        name = pending.pop()
        if name in selected:continue
        selected.add(name)
        assert name in by_name,name
        for row in by_name[name]:
            names=set(re.findall(r'\b[A-Za-z_]\w*\b',mask[row['start']:row['end']]))
            pending.extend((names & set(by_name))-selected)
    pieces=[]
    for row in entities:
        fragment=text[row['start']:row['end']]
        if row['name'] in selected:pieces.append(fragment)
        else:pieces.extend(line for line in fragment.splitlines()if line.lstrip().startswith('#'))
    result='\n'.join(pieces)+'\n'
    result=NONCODE.sub(lambda match:(' ' + '\n'*match.group().count('\n'))if match.group().startswith('/')else match.group(),result)
    result='\n'.join(line.rstrip()for line in result.splitlines()if line.strip())+'\n'
    assert not re.search(r'\b(?:va_list|size_t|J2pUnknownVaList|asm|__asm|__asm__)\b',result)
    source=ROOT/'generated/recovery/20261101-reference-oam-closed/native_main_0203716c.c'
    assert not source.exists()
    source.parent.mkdir(parents=True,exist_ok=True);source.write_text(result,encoding='utf-8')
    compiler.FLAGS+=['-lang','c99','-ipa','file'];compiler.WORK=ROOT/'work/main-reference-oam-closed-20261101/compile'
    rows,unused=compiler.compare(source,'main','4,p','on,noauto',compiler=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    row=rows[0]
    if row.get('compileFailed'):proof=None;exact=False
    else:
        try:proof=validate(row,qualified_bindings(row),ROOT/'work/main-reference-oam-closed-20261101/genuine-link');exact=True
        except ValueError as error:proof=error.args[0];exact=False
    write_json(ROOT/'evidence/attempts/main-reference-oam-type-slice-20261101.json',dict(sourceCredit=0,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
        input=original.relative_to(ROOT).as_posix(),inputSha256=sha256(original),selectedNames=sorted(selected),
        entities=len(entities),keptEntities=sum(row['name']in selected for row in entities),
        compilation=row,genuineLinkComparison=proof,exact=exact,noHeaderOrPlaceholderDependencies=True))
    print(dict(entities=len(entities),selectedNames=len(selected),lines=len(result.splitlines()),exact=exact))
    if row.get('compileFailed'):print(row.get('stdout','')[:1800])


if __name__=='__main__':
    main()
