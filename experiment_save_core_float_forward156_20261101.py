import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native'),str(ROOT/'evidence/application')]
from link_runtime_unit import measured_module


def sha(data):return hashlib.sha256(data).hexdigest()


def main():
    origin=ROOT/'nonmatching/save-core/20261101-float-pairs154/native_main_02067e54.c'
    text=origin.read_text().replace('extern u32 native_fn_020259b4();','extern u32 native_fn_020259b4(u32);')
    old='    native_fn_02024e0c(temp_r5, native_fn_02025ab8(var_r6, native_fn_02025a28(var_r4_2 + spC)));\n    return native_fn_020259b4();'
    new='    return native_fn_020259b4(native_fn_02024e0c(temp_r5, native_fn_02025ab8(var_r6, native_fn_02025a28(var_r4_2 + spC))));'
    assert old in text
    text=text.replace(old,new)
    variants=[('explicit_input',text,['Native68484 returnR0 is forwarded to259B4 at68488 without intervening setup'])]
    text=text.replace('*(native_data_021c3c4c + (temp_r9 * 2))','*(s16 *)(native_data_021c3c4c + (temp_r9 * 2))')
    assert text!=variants[-1][1]
    variants.append(('signed_table',text,['Native68394 LDRSH consumes signed16 throughbyte stride2,oldbyte-array draft readsu8']))
    text=text.replace('extern u8 native_data_021c37f0;','extern u8 native_data_021c37f0[];').replace('&native_data_021c37f0','native_data_021c37f0')
    assert text!=variants[-1][1]
    variants.append(('buffer_role',text,['Native7B460 output/globalbyte scan given incomplete-arrayaddress role,no aggregateextentdeclared']))
    profile=json.loads(gzip.decompress((ROOT/'evidence/vectors/save-core-float-pairs154-provenance-20261101.json.gz').read_bytes()))[0]['compileAttempts'][1]
    arm=measured_module('main')[1]
    rows=[]
    for label,text,notes in variants:
        p=ROOT/'nonmatching/save-core/20261101-float-forward156'/(label+'.c')
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text)
        spec=importlib.util.spec_from_file_location('float_forward156_'+label,ROOT/'evidence/application/save_core_historical_link_20261031.py')
        b=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(b)
        b.ENTRY,b.LENGTH,b.MODE=0x02067E54,1624,'arm'
        b.NAME,b.SOURCE='native_main_02067e54',p.relative_to(ROOT).as_posix()
        b.WORK='work/save-core/float-forward156/'+label
        b.COMPILER,b.COMPILER_HASH=profile['compilerPath'],profile['compilerSha256']
        b.FLAGS=profile['flags']
        try:
            row,body=b.build(arm[0x67E54:0x684AC])
            out=dict(compiled=True,realLinkCompared=True,candidate=row,sourceCreditAdded=0)
        except Exception as error:out=dict(compiled=False,error=str(error),sourceCreditAdded=0)
        rows.append(dict(label=label,source=p.relative_to(ROOT).as_posix(),sourceSha256=sha(p.read_bytes()),notes=notes,**out))
    payload=json.dumps(rows,indent=2).encode()
    side=ROOT/'evidence/vectors/save-core-float-forward156-20261101.json.gz'
    packed=gzip.compress(payload,mtime=0)
    side.write_bytes(packed)
    report=dict(schema=1,sourceCreditAdded=0,origin=origin.relative_to(ROOT).as_posix(),originSha256=sha(origin.read_bytes()),
        variants=len(rows),compiling=sum(x['compiled'] for x in rows),
        sidecar=dict(path=side.relative_to(ROOT).as_posix(),sha256=sha(packed),uncompressedSha256=sha(payload)),
        rows=[dict(label=x['label'],source=x['source'],compiled=x['compiled'],
            compiledBytes=x.get('candidate',{}).get('compiledBytes'),sameOffsetBytes=x.get('candidate',{}).get('sameOffsetBytes'),notes=x['notes']) for x in rows])
    (ROOT/'evidence/lanes/save-core/float-forward156-20261101.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['rows'])


if __name__=='__main__':
    main()
