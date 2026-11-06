from pathlib import Path
import hashlib
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
CONTRACT=dict(alias='func_0201d444',processor='arm9',program='',module='main',mode='arm',address=0x0201D444,bytes=44,
    source='src/runtime/20261030_format/native_main_0201d444.c',sourceSha256='4e853d8baaf06d4795419883b7365a5180be9c2c04f7b338312c961cb93556d3',
    nativeSpanSha256='e2149781be07fcbdd5b4b3221cd615c1913f2a033ccdf51153ad4dea6bda2e58',
    returnType='s32',contextPrototype='extern s32 func_0201d444(u8 *, const u8 *, ...);',
    sourcePrototype='extern int native_fn_0201d444(u8 *, const u8 *, ...);',
    qualification='Existing matched ARM32 variadic declaration view only. Inferred extra argument values/types remain hypotheses until original caller/compiler/link qualification;no host/Android va_list guarantee.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(contract):
    from link_runtime_unit import measured_module
    metadata,binary,config=measured_module('main')
    assert sha((ROOT/contract['source']).read_bytes())==contract['sourceSha256'],'Formatter source pin'
    entry=contract['address']
    offset=entry-int(metadata['base'],0)
    assert sha(binary[offset:offset+contract['bytes']])==contract['nativeSpanSha256'],'Formatter native pin'
    assert re.search(r'\bfunc_0201d444 kind:function\(arm,size=0x2c\) addr:0x0201d444\b',config)
    return dict(contract,nativeModuleSha256=metadata['sha256'])


def catalogue():
    return [validate(CONTRACT)]


def apply(context,spec):
    if spec.get('processor')!='arm9' or spec.get('program','') not in ['',None] or spec.get('mode') not in ['arm','thumb']:
        return context,[]
    pattern=r'^extern\s+u32\s+func_0201d444\s*\(\s*\)\s*;'
    found=list(re.finditer(pattern,context,re.M))
    if not found:
        return context,[]
    assert len(found)==1,'Ambiguous formatter declaration'
    contract=catalogue()[0]
    result=re.sub(pattern,contract['contextPrototype'],context,count=1,flags=re.M)
    return result,[dict(contract,previousPrototype=found[0].group())]
