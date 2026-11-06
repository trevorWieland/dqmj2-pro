from project import ROOT,read_json
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from wave20261105_dwc_http_next_fifth_bindings import inputs

def verify(rows):
 value,image,inventory,records,imports=inputs();base=0x21d1914
 assert imports['dataViews'][hex(base)]==dict(type='netcheck-storage24',minimumBytes=24,storage='bss',expectedHex='')
 for address in [base,base+4,base+24]:assert 'data_%08x kind:bss addr:0x%08x'%(address,address)in inventory.splitlines()
 witnesses=[];decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
 for address,offset,mnemonic,operands,role in [(0x2098fbc,0x44,'ldr','r0, [r2, #0x14]','Read Http pointer at storage+20'),(0x2098fbc,0x62,'str','r0, [r1, #4]','Clear hotspot word at storage+4'),(0x2099058,0x0a,'ldr','r0, [r1, #0x14]','Read Http pointer at storage+20'),(0x20990f0,0x0a,'ldr','r0, [r0, #0x14]','Read Http pointer at storage+20')]:
  row=next(row for row in rows if int(row['address'],0)==address);raw=image[address+offset-0x2000000:address+offset-0x2000000+2];decoded=list(decoder.disasm(raw,address+offset));assert len(decoded)==1 and(decoded[0].mnemonic,decoded[0].op_str)==(mnemonic,operands)
  assert any(int(rel['target'],0)==base for rel in row['relocations']);witnesses.append(dict(caller=row['address'],offset=offset,nativeBytes=raw.hex(),instruction=mnemonic+' '+operands,role=role))
 return dict(allPassed=True,storageBase=hex(base),storageEndExclusive=hex(base+24),nextCanonicalBssSymbol=hex(base+24),measuredFields=[dict(offset=0,bytes=4,view='Netcheck pointer word'),dict(offset=4,bytes=4,view='hotspot raw boolean word'),dict(offset=20,bytes=4,view='Http pointer word')],opaqueRanges=[dict(offset=8,bytes=12)],witnesses=witnesses,initializedDataOrBssSourceCredit=0)
