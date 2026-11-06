import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_historical_link_20261031 as B

def main():
    old=json.loads((ROOT/'evidence/lanes/save-core/near-refresh128-20261101.json').read_text());arm=B.measured_module('main')[1];results=[]
    for address in (0x0209D690,):
        p=next(r for r in old['functions'] if int(r['address'],0)==address);source=(ROOT/p['source']).read_text()
        call='native_fn_020aa3e0(M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), u32 *, 4), sp0, arg1)'
        cut=source.rfind('    if (native_fn_020aa3e0')
        assert cut>=0
        text=source[:cut]+'    return '+call+' == 0U;\n}\n'
        variations=[('boolean_return',text)]
        for name,text in variations:
            path=ROOT/f'nonmatching/save-core/20261101-frontier135/{address:08x}_{name}.c';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);B.MODULE='main';B.MODE=p['mode'];B.ENTRY=address;B.LENGTH=p['bytes'];B.NAME=f'native_main_{address:08x}';B.SOURCE=path.relative_to(ROOT).as_posix();B.WORK=f'work/scf135/{address:08x}_{name}';B.FLAGS=p['flags'];B.COMPILER=p['compilerPath'];B.COMPILER_HASH=p['compilerSha256'];row,body=B.build(arm[address-0x02000000:address-0x02000000+p['bytes']]);results.append(dict(experiment=name,match=row));print(hex(address),name,row.get('exactByteEqual'),row.get('compiledBytes'),row.get('linkMismatch',{}).get('matchingBytes'))
    (ROOT/'evidence/attempts/save-core-frontier135-boolean-20261101.json').write_text(json.dumps(dict(schemaVersion=1,sourceCredit=0,experiments=results),indent=2)+'\n')

if __name__=='__main__':main()
