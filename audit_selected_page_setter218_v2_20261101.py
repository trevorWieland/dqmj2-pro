from pathlib import Path
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parent
UP=ROOT.parents[1]/'dqmj2pro-decomp'
sys.dont_write_bytecode=True
sys.path[:0]=[str(UP),str(UP/'deps/native')]
from ledger_state import collect_matches


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def address(value):
    if isinstance(value,int):return value
    if isinstance(value,str):
        if value.startswith('0x'):return int(value,0)
        if re.fullmatch(r'(?:native_fn_|func_)020624b0',value.lower()):return 0x020624B0
    return None


def main():
    receipts={name:sha(UP/name) for name in ['recovery.json','source-preferences.json']}
    selected,rejected=collect_matches('674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6')
    rows=[]
    for (module,mode,at),row in selected.items():
        if Path(row['source']).suffix not in ['.c','.cpp']:continue
        if module!='main' and not re.fullmatch(r'ov[0-9]+',module):continue
        bindings=[r for r in row.get('relocations',[]) if address(r.get('target'))==0x020624B0 and r.get('targetModule') in [None,'main']]
        path=UP/row['source']
        text=path.read_text()
        for dependency in row.get('sourceDependencies',[]):
            item=UP/dependency['path']
            if item.suffix=='.inc':text+='\n'+item.read_text()
        lexical=sorted(set(re.findall(r'\b(native_fn_020624b0|func_020624b0|native_main_020624b0)\b',text,re.I)))
        if not bindings and not lexical:continue
        if at==0x020624B0 and module=='main':continue
        symbols=sorted(set(r['symbol'] for r in bindings if 'symbol' in r))
        symbols=sorted(set(symbols+lexical))
        declarations=[]
        for symbol in symbols:
            declarations.extend(match[0] for match in re.findall(r'(^[^\n;]*\b'+re.escape(symbol)+r'\s*\(([^;]*?)\);)',text,re.M))
        rows.append(dict(processor=row.get('processor'),module=module,mode=mode,address=hex(at),bytes=row.get('size'),source=row['source'],sourceSha256=row['sourceSha256'],report=row['report'],boundSymbols=symbols,declarations=declarations,sourceDependencies=row.get('sourceDependencies',[]),relocations=bindings))
    assert all(sha(UP/name)==digest for name,digest in receipts.items())
    output=dict(schemaVersion=1,evidenceClass='Read-only current selected624B0 relocation-user inventory',selectedRows=len(selected),sourceCreditAdded=0,rootReceipts=receipts,selectedDefinition=selected[('main','arm',0x020624B0)],callerRows=rows,limitations=['Selected ARM9 main/overlay C source lexical aliases and direct object references624B0 are inventoried;other indirect or renamed users remain separate. Relocations are references,not automatically ordinary reachable call sites. Caller compatibility/native word-preparation require individual review;no source mutation or coverage change.'])
    path=ROOT/'evidence/lanes/save-core/page-setter-caller-inventory218-v2-20261101.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(len(rows),'reference users')
    for row in rows:print(row['module'],row['address'],row['bytes'],row['source'],row['declarations'])


if __name__=='__main__':main()
