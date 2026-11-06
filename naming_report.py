"""Read-only naming leads from a committed source snapshot; never a quality score."""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import posixpath
import re
import subprocess
from pathlib import PurePosixPath

from project import ROOT,write_json


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def blobs(revision,names):
    names=sorted(set(names))
    if not names:return {}
    raw=subprocess.check_output(
        ['git','cat-file','--batch'],cwd=ROOT,input=''.join(f'{revision}:{name}\n'for name in names).encode())
    result={};offset=0
    for name in names:
        end=raw.index(b'\n',offset);header=raw[offset:end].decode();offset=end+1
        assert not header.endswith(' missing'),name
        oid,kind,size=header.split();assert kind=='blob';size=int(size)
        result[name]=raw[offset:offset+size];offset+=size+1
    assert offset==len(raw)
    return result


def blank_noncode(text):
    pattern=r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern,lambda m:''.join('\n'if c=='\n'else' 'for c in m[0]),text,flags=re.S)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--revision',required=True);parser.add_argument('--module')
    parser.add_argument('--output');parser.add_argument('--json',action='store_true')
    args=parser.parse_args();revision=git('rev-parse',args.revision+'^{commit}').decode().strip()
    legacy=subprocess.run(['git','cat-file','-e',revision+':ledger/functions.jsonl'],cwd=ROOT,capture_output=True)
    if legacy.returncode==0:
        ledger_bytes=git('show',revision+':ledger/functions.jsonl')
        ledger=[json.loads(line)for line in ledger_bytes.splitlines()]
    else:
        ledger_bytes=git('show',revision+':public/accepted-functions.json')
        ledger=json.loads(ledger_bytes)['functions']
    selected=[r for r in ledger if r['states']['functionMatched']]
    sources=defaultdict(set);module_functions=Counter();address_symbols=Counter()
    for row in selected:
        module='/'.join([row.get('program')or'host',row['processor'],row['module']])
        if args.module and args.module not in (module,row['module']):continue
        module_functions[module]+=1
        if re.fullmatch(r'(?:func|native|fn)_[A-Za-z0-9_]*[0-9a-fA-F]{8}',row['symbol']):address_symbols[module]+=1
        name=(row.get('sourceUnit')or'').replace('\\','/')
        if name.endswith(('.c','.cpp','.h','.hpp'))and name.startswith(('src/','include/','lib/')):sources[name].add(module)
    tree=set(git('ls-tree','-r','--name-only',revision,'src','include','lib').decode().splitlines())
    pending=set(sources);contents={};hashes={};includes=defaultdict(set)
    while pending:
        values=blobs(revision,pending);pending=set()
        for name,raw in values.items():
            hashes[name]=hashlib.sha256(raw).hexdigest();text=raw.decode('utf-8-sig',errors='replace');contents[name]=text
            for inc in re.findall(r'^\s*#\s*include\s*"([^"\n]+)"',text,re.M):
                options=[posixpath.normpath(str(PurePosixPath(name).parent/inc)),inc,'include/'+inc]
                target=next((p for p in options if p in tree and p.endswith(('.h','.hpp','.inc'))),None)
                if target:
                    includes[name].add(target)
                    sources[target].update(sources[name])
                    if target not in contents:pending.add(target)
    changed=True
    while changed:
        changed=False
        for parent,children in includes.items():
            for child in children:
                old=len(sources[child]);sources[child].update(sources[parent])
                changed=changed or len(sources[child])!=old
    findings=[];totals=Counter();by_module=defaultdict(Counter)
    identifier=re.compile(r'\b[A-Za-z_]\w*\b')
    for name,text in sorted(contents.items()):
        code=blank_noncode(text);seen=set();items=[]
        for match in identifier.finditer(code):
            value=match[0];kind=None
            if re.fullmatch(r'(?:arg|param|var|v|a)_?\d+',value)or re.fullmatch(r'var_r\d+',value):kind='placeholder_parameter_or_local'
            elif re.match(r'(?i)^(?:unk(?:nown)?(?:_|\d)|field_(?:0x)?[0-9a-f]+$)',value):kind='unknown_or_offset_identifier'
            if kind and(kind,value)not in seen:
                seen.add((kind,value));items.append(dict(kind=kind,line=code.count('\n',0,match.start())+1,identifier=value))
        for pattern,kind in [(r'\bcase\s+(-?(?:0x[0-9a-fA-F]+|\d+))\s*:','numeric_case_lead'),(r'(?:==|!=)\s*((?:0x[0-9a-fA-F]+|[2-9]\d*|1\d+))\b','numeric_comparison_lead')]:
            for match in re.finditer(pattern,code):items.append(dict(kind=kind,line=code.count('\n',0,match.start())+1,value=match[1]))
        count=Counter(item['kind']for item in items);totals.update(count)
        for module in sources[name]:by_module[module].update(count)
        if items:findings.append(dict(path=name,sha256=hashes[name],modules=sorted(sources[name]),counts=dict(count),items=items))
    result=dict(schemaVersion=1,sourceCredit=0,revision=revision,ledgerSha256=hashlib.sha256(ledger_bytes).hexdigest(),
        sourceSnapshotOnly=True,selectedSourceFunctions=sum(module_functions.values()),authoredSourceAndHeaderFiles=len(contents),
        counts=dict(totals),modules=[dict(namespace=m,sourceFunctions=n,canonicalAddressSymbols=address_symbols[m],namingLeads=dict(by_module[m]))for m,n in sorted(module_functions.items())],files=findings,
        sourceHashes=hashes,limitations=['Counts are investigation leads, not errors or a percentage of semantic understanding.',
            'Canonical address identifiers can remain stable even when a descriptive alias is documented.',
            'Only selected committed source and resolvable authored quoted headers are scanned; external SDK references are excluded.',
            'Numeric cases/comparisons can be appropriate; inspect usage before introducing constants or enums.',
            'Shared-header counts can appear in multiple module rows; global counts deduplicate files.',
            'No source, symbols, registries, compiler inputs or accepted matches are changed.'])
    if args.output:
        target=(ROOT/args.output).resolve();assert target.is_relative_to(ROOT/'work');write_json(target,result)
    if args.json:print(json.dumps(result))
    else:print(json.dumps({k:result[k]for k in ['revision','sourceCredit','selectedSourceFunctions','authoredSourceAndHeaderFiles','counts']}))


if __name__=='__main__':main()
