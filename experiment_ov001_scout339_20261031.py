import json
from pathlib import Path
import match_runtime as c
from project import ROOT,sha256,write_json
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import validate
BASE=ROOT/'nonmatching/overlay-lane/20261031-scout339'
OLD=ROOT/'nonmatching/overlay-lane/20261031-scout338/ov001/021f9608-arm'

def run():
    original=(OLD/'source.c').read_text()
    expression='M2C_FIELD(M2C_FIELD(temp_r0, void **, 0x1E8), s8 *, 0xB0)'
    old='M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16) (('+expression+' * 0xA) + 0);'
    compound='M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) += '+expression+' * 0xA;'
    accumulator=original.replace('    void *temp_r0;','    s32 value;\n    void *temp_r0;').replace('M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = 0;','value = 0;\n    M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16)value;').replace(old,'value += '+expression+' * 0xA;\n    M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16)value;')
    variants=dict(original=original,compound=original.replace(old,compound),accumulator=accumulator)
    if len(set(variants.values()))!=3:raise ValueError('Scout339 natural shapes missing')
    results=[]
    flags=list(c.FLAGS)
    try:
        for name,value in variants.items():
            source=BASE/name/'source.c'
            source.parent.mkdir(parents=True,exist_ok=True)
            for p,v in[(source,value),(source.with_name('context.h'),(OLD/'context.h').read_text())]:
                if p.exists()and p.read_bytes()!=v.encode():raise ValueError('Scout339 preserve old source')
                p.write_bytes(v.encode())
            for processor,symbols in[('arm946e','on'),('arm9','on'),('arm946e','off')]:
                c.FLAGS[:]=flags
                c.FLAGS[c.FLAGS.index('-proc')+1]=processor
                c.FLAGS[c.FLAGS.index('-sym')+1]=symbols
                directory=ROOT/'work/ol339'/name/(processor+'-'+symbols)
                c.WORK=directory/'compile'
                try:rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
                except Exception as error:
                    results.append(dict(variant=name,processor=processor,symbols=symbols,compileFailed=str(error),sourceCredit=0))
                    continue
                row=rows[0]
                if 'relocations'not in row:
                    results.append(dict(variant=name,processor=processor,symbols=symbols,compileFailed=row,sourceCredit=0))
                    continue
                row['sourceDependencies']=[dict(path=str(source.with_name('context.h').relative_to(ROOT)),sha256=sha256(source.with_name('context.h')))]
                try:proof=validate(row,qualified_bindings(row),directory/'link')
                except ValueError as error:
                    proof=error.args[0]
                    if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
                results.append(dict(variant=name,processor=processor,symbols=symbols,compilation=row,realLink=proof,exact=proof.get('exactCallerBytes',False),sourceCredit=0))
    finally:c.FLAGS[:]=flags
    write_json(ROOT/'evidence/attempts/ov001-scout339-natural-profiles-20261031.json',dict(results=results,sourceCredit=0,limitations=['Natural ordinary accumulator/compound shapes and bounded target/debug profiles only; no forced registers, padding, assembly or opcode changes','Matching flags are scope-specific demonstrated configurations, not proof of original unit settings','All earlier source/experiments and accepted files remain unchanged'],generatorSha256=sha256(__file__)))
    print(json.dumps([dict(variant=r['variant'],processor=r['processor'],symbols=r['symbols'],exact=r.get('exact'),compiled=r.get('compilation',{}).get('compiledBytes'),matching=r.get('realLink',{}).get('matchingBytes',172 if r.get('exact')else None),failed=r.get('compileFailed'))for r in results]))

if __name__=='__main__':run()
