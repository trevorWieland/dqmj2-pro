import json
import re
from pathlib import Path
from project import ROOT,sha256,write_json
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


def declaration_aliases(text,name):
    clean=re.sub(r'(?m)^\s*#.*$','',text).strip()
    tag=re.match(r'(?:struct|union|enum)\s+([A-Za-z_]\w*)\s*\{',clean)
    if tag:return[tag.group(1)]
    if not clean.startswith('typedef'):return [name]if name else[]
    tail=clean.rsplit('}',1)[-1]if '}'in clean else clean.removeprefix('typedef')
    pointer=re.findall(r'\(\s*\*\s*([A-Za-z_]\w*)\s*\)',tail)
    if pointer:return pointer
    aliases=[]
    for part in tail.rstrip(';').split(','):
        part=part.split('[',1)[0];words=re.findall(r'\b[A-Za-z_]\w*\b',part)
        if words:aliases.append(words[-1])
    return aliases

def slice_closed(text,seeds):
    records=functions(text);mapping={r['name']:r for r in records};selected=set();pending=list(seeds)
    while pending:
        name=pending.pop()
        if name in selected:continue
        if name not in mapping:raise ValueError('Function definition missing:'+name)
        selected.add(name);row=mapping[name];names=set(re.findall(r'\b[A-Za-z_]\w*\b',text[row['opening']:row['end']]))
        pending.extend((names&set(mapping))-selected)
    for row in sorted([r for r in records if r['name']not in selected],key=lambda r:r['start'],reverse=True):
        fragment=text[row['start']:row['end']];directives='\n'.join(l for l in fragment.splitlines()if l.lstrip().startswith('#'))
        text=text[:row['start']]+'\n'+directives+'\n'+text[row['end']:]
    mask=NONCODE.sub(lambda match:' '*len(match.group()),text);mask=re.sub(r'(?m)^\s*#.*$',lambda match:' '*len(match.group()),mask)
    definitions=functions(text);ranges={r['start']:r for r in definitions};entities=[];start=index=depth=0
    while index<len(mask):
        if index in ranges:
            row=ranges[index];entities.append(dict(start=start,end=row['end'],name=row['name'],kind='function'));index=start=row['end'];continue
        char=mask[index]
        if char=='{':depth+=1
        elif char=='}':depth-=1
        elif char==';'and depth==0:
            entities.append(dict(start=start,end=index+1,name=declaration_name(text[start:index+1]),kind='declaration'));start=index+1
        index+=1
    if depth:raise ValueError('Unbalanced closed declaration parse')
    by_name={}
    for row in entities:
        for alias in declaration_aliases(text[row['start']:row['end']],row['name']):by_name.setdefault(alias,[]).append(row)
    names=set();pending=list(seeds)
    while pending:
        name=pending.pop()
        if name in names:continue
        names.add(name)
        if name not in by_name:raise ValueError('Selected lexical entity missing:'+name)
        for row in by_name[name]:
            used=set(re.findall(r'\b[A-Za-z_]\w*\b',mask[row['start']:row['end']]))
            pending.extend((used&set(by_name))-names)
    pieces=[]
    for row in entities:
        if set(declaration_aliases(text[row['start']:row['end']],row['name']))&names:pieces.append(text[row['start']:row['end']])
    result='\n'.join(pieces)+'\n';result=NONCODE.sub(lambda match:(' '+'\n'*match.group().count('\n'))if match.group().startswith('/')else match.group(),result)
    result='\n'.join(l.rstrip()for l in result.splitlines()if l.strip()and not l.lstrip().startswith('#'))+'\n'
    return result,dict(selectedFunctions=sorted(selected),selectedEntities=sorted(names),allEntityCount=len(entities),selectedEntityCount=sum(bool(set(declaration_aliases(text[r['start']:r['end']],r['name']))&names)for r in entities),forbiddenTokens=sorted(set(re.findall(r'\b(?:va_list|size_t|J2pUnknownVaList|asm|__asm|__asm__)\b',result))))
