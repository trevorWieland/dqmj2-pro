import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_historical_link_20261031 as B

def main():
    old=json.loads((ROOT/'evidence/lanes/save-core/near-refresh128-20261101.json').read_text());arm=B.measured_module('main')[1];results=[]
    for address in (0x02087224,):
        p=next(r for r in old['functions'] if int(r['address'],0)==address);source=(ROOT/p['source']).read_text()
        if address==0x02087224:
            typed=source.replace('native_fn_02087334();','native_fn_02087334(arg0);').replace('extern u32 native_fn_02087334(arg0);','extern u32 native_fn_02087334(void *);')
            variations=[('prefix_byte_increment',typed.replace('    temp_r2 = M2C_FIELD(arg0, u8 *, 0x85) + 1;\n    M2C_FIELD(arg0, u8 *, 0x85) = temp_r2;\n    if ((u32) temp_r2 <= 8U)', '    if (++M2C_FIELD(arg0, u8 *, 0x85) <= 8U)'))]
        else:
            variations=[('prefix_byte_decrement',source.replace('        temp_r2 = native_data_021c6e50 - 1;\n        native_data_021c6e50 = temp_r2;\n        native_fn_02081aec(temp_r2);','        native_fn_02081aec(--native_data_021c6e50);').replace('native_fn_02081aec();','native_fn_02081aec(u8);'))]
        for name,text in variations:
            name+='__unsigned_flags';text=text.replace('s32 *, 0x80','u32 *, 0x80').replace('s32 temp_r2_2','u32 temp_r2_2').replace('s32 temp_r2_3','u32 temp_r2_3')
            path=ROOT/f'nonmatching/save-core/20261101-frontier134/{address:08x}_{name}.c';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);B.MODULE='main';B.MODE='arm';B.ENTRY=address;B.LENGTH=p['bytes'];B.NAME=f'native_main_{address:08x}';B.SOURCE=path.relative_to(ROOT).as_posix();B.WORK=f'work/scf134/{address:08x}_{name}';B.FLAGS=p['flags'];B.COMPILER=p['compilerPath'];B.COMPILER_HASH=p['compilerSha256'];row,body=B.build(arm[address-0x02000000:address-0x02000000+p['bytes']]);results.append(dict(experiment=name,match=row));print(hex(address),name,row.get('exactByteEqual'),row.get('compiledBytes'),row.get('linkMismatch',{}).get('matchingBytes'))
    (ROOT/'evidence/attempts/save-core-frontier134-unsigned-20261101.json').write_text(json.dumps(dict(schemaVersion=1,sourceCredit=0,experiments=results),indent=2)+'\n')

if __name__=='__main__':main()
