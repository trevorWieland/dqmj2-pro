import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, write_json, sha256
from slice_standalone_sdk_functions_20261101 import functions, NONCODE
from slice_standalone_sdk_types_20261101 import declaration_name
from probe_main_reference_oam_family_20261101 import MAPPING
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def function_slice(text,target):
    records=functions(text);mapping={row['name']:row for row in records}
    selected=set();pending=[target]
    while pending:
        name=pending.pop()
        if name in selected:continue
        selected.add(name);row=mapping[name]
        names=set(re.findall(r'\b[A-Za-z_]\w*\b',text[row['opening']:row['end']]))
        pending.extend((names & set(mapping))-selected)
    for row in sorted(records,key=lambda row:row['start'],reverse=True):
        if row['name']in selected:continue
        fragment=text[row['start']:row['end']]
        directives='\n'.join(line for line in fragment.splitlines()if line.lstrip().startswith('#'))
        text=text[:row['start']]+'\n'+directives+'\n'+text[row['end']:]
    return text,sorted(selected)


def type_slice(text,target):
    mask=NONCODE.sub(lambda match:' '*len(match.group()),text)
    mask=re.sub(r'(?m)^\s*#.*$',lambda match:' '*len(match.group()),mask)
    ranges={row['start']:row for row in functions(text)}
    entities=[];start=index=depth=0
    while index<len(mask):
        if index in ranges:
            row=ranges[index];entities.append(dict(start=start,end=row['end'],name=row['name']))
            index=start=row['end'];continue
        char=mask[index]
        if char=='{':depth+=1
        elif char=='}':depth-=1
        elif char==';'and depth==0:
            entities.append(dict(start=start,end=index+1,name=declaration_name(text[start:index+1])))
            start=index+1
        index+=1
    assert depth==0
    mapping={}
    for row in entities:
        if row['name']:mapping.setdefault(row['name'],[]).append(row)
    selected=set();pending=[target]
    while pending:
        name=pending.pop()
        if name in selected:continue
        selected.add(name)
        for row in mapping[name]:
            names=set(re.findall(r'\b[A-Za-z_]\w*\b',mask[row['start']:row['end']]))
            pending.extend((names & set(mapping))-selected)
    pieces=[]
    for row in entities:
        fragment=text[row['start']:row['end']]
        if row['name']in selected:pieces.append(fragment)
    result=NONCODE.sub(lambda match:' 'if match.group().startswith('/')else match.group(),'\n'.join(pieces))
    result=re.sub(r'(?m)^\s*#.*$','',result)
    result='\n'.join(line.rstrip()for line in result.splitlines()if line.strip())+'\n'
    assert '#include'not in result
    assert not re.search(r'\b(?:va_list|size_t|J2pUnknownVaList|asm|__asm|__asm__)\b',result)
    return result,sorted(selected)


def main():
    original=ROOT/'generated/recovery/20261101-reference-oam-standalone/native_main_0203716c.c'
    text=original.read_text(encoding='utf-8')
    aliases={**{name:'native_main_'+f'{address:08x}'for name,address in MAPPING.items()},
        'DC_FlushRange':'native_fn_02007308','GX_LoadOAM':'native_fn_020049fc',
        'GXS_LoadOAM':'native_fn_02004a50','MIi_CpuClear16':'native_fn_02008be0',
        'numRegisterdInstance_':'native_data_020f0f04'}
    for name,alias in aliases.items():text=re.sub(r'\b'+re.escape(name)+r'\b',alias,text)
    before='static u16 native_data_020f0f04 = 0x0;'
    assert text.count(before)==1
    text=text.replace(before,'extern u16 native_data_020f0f04;')
    pattern=r'static OBJLoadFunction \* funcTbl\[\] = \{.*?\};'
    text,count=re.subn(pattern,'extern OBJLoadFunction * native_data_020dd810[5];',text,flags=re.S)
    assert count==1,count
    text=text.replace('return funcTbl[type];','return native_data_020dd810[type];')
    compiler.FLAGS+=['-lang','c99','-ipa','file']
    results=[]
    for address in list(MAPPING.values())[:-1]:
        target='native_main_'+f'{address:08x}'
        sliced,definitions=function_slice(text,target)
        closed,names=type_slice(sliced,target)
        source=ROOT/f'generated/recovery/20261101-oam-standalone-family-v2/{target}.c'
        assert not source.exists();source.parent.mkdir(parents=True,exist_ok=True)
        source.write_text(closed,encoding='utf-8')
        compiler.WORK=ROOT/f'work/oam-standalone-family-v2-20261101/{target}/compile'
        rows,_=compiler.compare(source,'main','4,p','on,noauto',compiler=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
        assert len(rows)==1 and int(rows[0]['address'],0)==address
        row=rows[0];exact=False
        if row.get('compileFailed'):proof=dict(compileFailed=True,diagnostic=row.get('stdout','')[:1800])
        else:
            try:proof=validate(row,qualified_bindings(row),ROOT/f'work/oam-standalone-family-v2-20261101/{target}/link');exact=True
            except ValueError as error:proof=error.args[0]
        results.append(dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
            lines=len(closed.splitlines()),definitions=definitions,names=names,compilation=row,
            genuineLinkComparison=proof,exact=exact,sourceCredit=0))
        print(dict(address=hex(address),lines=len(closed.splitlines()),bytes=row.get('bytes'),exact=exact),flush=True)
    write_json(ROOT/'evidence/attempts/main-oam-standalone-family-v2-20261101.json',dict(sourceCredit=0,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),input=original.relative_to(ROOT).as_posix(),
        inputSha256=sha256(original),aliases=aliases,results=results,noHeaderPlaceholders=True,
        callerInterfaceAndNativeProofsPending=True,manualEntityReviewPending=True))


if __name__=='__main__':
    main()
