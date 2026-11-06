import re
import struct
import wave20261104_main_tail_bindings as B
from project import ROOT,sha256


def verify(row,bindings):
    assert row['module']=='main' and row['processor']=='arm9' and row['mode']=='arm'
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    text=(ROOT/'config/arm9/relocs.txt').read_text()
    origin=int(row['address'],0)
    branches=dict(row,relocations=[r for r in row['relocations'] if r['type']!=2])
    calls=B.verify_original(branches,{n:b for n,b in bindings.items() if b['kind']=='function'})
    loads=[]
    for relocation in row['relocations']:
        if relocation['type']!=2:continue
        symbol=relocation['symbol'];binding=bindings[symbol]
        assert binding['processor']=='arm9' and binding['module']=='main'
        assert binding['kind']=='data' and binding['mode']=='data'
        address=int(binding['address'],0)
        assert address==int(relocation['target'],0)
        site=origin+relocation['offset']
        pattern=r'(?m)^from:0x'+format(site,'08x')+r' kind:load to:0x'+format(address,'08x')+r' module:main\s*$'
        assert re.search(pattern,text),(hex(site),symbol,binding)
        word=struct.unpack_from('<I',image,site-0x02000000)[0]
        assert word==(address+relocation['addend'])&0xffffffff
        loads.append(dict(site=hex(site),symbol=symbol,binding=binding,originalWord=hex(word),originalAddend=relocation['addend']))
    return dict(branches=calls,dataLiteralLoads=loads,originalRelocationMetadataSha256=sha256(ROOT/'config/arm9/relocs.txt'),calleeOrDataSourceCredit=0)
