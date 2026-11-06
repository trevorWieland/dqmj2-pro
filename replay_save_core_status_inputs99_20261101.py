import sys,json,subprocess,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]


def worker(address):
    import save_core_historical_link_20261031 as B
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
    rows=json.loads((ROOT/'evidence/attempts/save-core-owned-frontier98-20261101.json').read_text())['rows'];p=next(r for r in rows if int(r['address'],0)==address);text=(ROOT/p['source']).read_text();folder=ROOT/'nonmatching/save-core/20261101-status-input99';folder.mkdir(parents=True,exist_ok=True)
    if address==0x205F27C:text=text.replace('native_fn_0205f2d8();','native_fn_0205f2d8(s32);',1).replace('native_fn_0205f2d8()','native_fn_0205f2d8(arg0)')
    elif address==0x205F404:text=text.replace('native_fn_0205f45c();','native_fn_0205f45c(s32);',1).replace('native_fn_0205f45c()','native_fn_0205f45c(arg0)')
    elif address in (0x205F45C,0x205F848):text=text.replace('native_fn_0203a090();','native_fn_0203a090(void *);',1).replace('native_fn_0203a090()','native_fn_0203a090(native_data_021b8af0 + (arg0 * 8))')
    else:text=text.replace('native_fn_0203a01c();','native_fn_0203a01c(void *);',1).replace('s8 arg1','u32 arg1')
    for name,proto in [('0205ed58','s8'),('020380e4','void *,u32'),('0203a000','void *,u32')]:text=text.replace('native_fn_'+name+'();','native_fn_'+name+'('+proto+');',1)
    path=folder/(f'native_main_{address:08x}.c');path.write_text(text);B.MODULE='main';B.MODE='arm';B.ENTRY=address;B.LENGTH=p['bytes'];B.NAME=p['name'];B.SOURCE=path.relative_to(ROOT).as_posix();B.WORK=f'work/scsi99/{address:08x}';B.FLAGS=p['flags'];B.COMPILER=p['compilerPath'];B.COMPILER_HASH=p['compilerSha256'];arm=B.measured_module('main')[1];row,body=B.build(arm[address-0x2000000:address-0x2000000+p['bytes']]);d=Cs(CS_ARCH_ARM,CS_MODE_ARM);a=list(d.disasm(arm[address-0x2000000:address-0x2000000+p['bytes']],address));b=list(d.disasm(body,address));diff=[dict(address=hex(x.address),native=x.mnemonic+' '+x.op_str,candidate=y.mnemonic+' '+y.op_str) for x,y in zip(a,b) if x.bytes!=y.bytes];return dict(input=p,build=row,diff=diff)


def main():
    addresses=[0x205F27C,0x205F404,0x205F45C,0x205F848,0x205F7E0]
    if len(sys.argv)>1:
        v=worker(int(sys.argv[1],0));out=ROOT/('evidence/attempts/save-core-status-input99-'+sys.argv[1][2:]+'-20261101.json');out.write_text(json.dumps(v,indent=2)+'\n');print(sys.argv[1],v['build']['exactByteEqual'],v['build']['compiledBytes'],v['diff']);return
    def launch(a):
        p=subprocess.run([sys.executable,__file__,hex(a)],capture_output=True,text=True,timeout=90);assert p.returncode==0,p.stdout+p.stderr;return p.stdout
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for value in pool.map(launch,addresses):print(value)


if __name__=='__main__':main()
