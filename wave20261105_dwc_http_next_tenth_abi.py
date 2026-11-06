import struct
from project import ROOT
from wave20261105_dwc_http_next_tenth_bindings import inputs

def verify(rows):
 value,image,inventory,records,imports=inputs();expected={'0x21d19ac':('error-storage8',8),'0x21d19b4':('allocator-storage8',8)}
 for address,(kind,size)in expected.items():
  assert imports['dataViews'][address]==dict(type=kind,minimumBytes=size,storage='bss',expectedHex='');assert 'data_%08x kind:bss addr:0x%08x'%(int(address,0),int(address,0))in inventory.splitlines()
 function=next(row for row in rows if row['address']=='0x209a944');start=int(function['address'],0)-0x2000000;offsets=struct.unpack('<22h',image[start+0x22:start+0x22+44]);mapped=[image[start+0x24+offset]for offset in offsets];assert mapped==[0,7,6,6,6,6,3,4,6,7,1,1,1,1,5,6,2,6,2,6,2,2]
 clear=next(row for row in rows if row['address']=='0x209a9d0');start=int(clear['address'],0)-0x2000000;assert image[start+4:start+6]==bytes.fromhex('0929')
 return dict(allPassed=True,original22CaseJumpTargetsAndStoredTypes=mapped,rawAdditionalErrorCodes=[dict(code=20,type=2),dict(code=21,type=2)],unknownCodeMeaningsUninferred=True,fatalClearGuard=9,errorStorage=dict(base='0x21d19ac',bytes=8,lastOffset=0,codeOffset=4),allocatorStorage=dict(base='0x21d19b4',bytes=8,freeOffset=0,allocOffset=4),allocationHeaderBytes=32,publishedAllocatorHeaderHelpersRemainImported=True,storageAndCalleeSourceCredit=0)
