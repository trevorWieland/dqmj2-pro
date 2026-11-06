import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,sha256

CASES=[(0x0204d884,112,0x0204d8b0,0x0204d8b8,0x0204d8f0,'strb'),(0x0204d8f4,124,0x0204d8f8,0x0204d900,0x0204d96c,'ldrb'),(0x0204dae0,264,0x0204dae4,0x0204daec,0x0204dbe4,'ldrb'),(0x0204dbe8,228,0x0204dbec,0x0204dbf4,0x0204dcc8,'ldrb')]


def qualify(expected=0x02102d78,width=1):
    binary=ROOT/'extract/arm9/arm9.bin';raw=binary.read_bytes();decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);records=[]
    if width!=1:raise ValueError('Measured flag accesses are byte instructions')
    for address,size,load,access,pool,mnemonic in CASES:
        word=struct.unpack_from('<I',raw,load-0x02000000)[0]
        if word&0xffff0000!=0xe59f0000 or load+8+(word&0xfff)!=pool:raise ValueError('Original ARM literal load or exact pool differs')
        value=struct.unpack_from('<I',raw,pool-0x02000000)[0]
        instruction=next(decoder.disasm(raw[access-0x02000000:access-0x02000000+4],access),None)
        if value!=expected or instruction is None or instruction.mnemonic!=mnemonic:raise ValueError('Original native data target or access width differs')
        records.append(dict(program='',processor='arm9',module='main',mode='arm',caller=hex(address),bytes=size,callerSha256=match_runtime.sha(raw[address-0x02000000:address-0x02000000+size]),literalLoad=hex(load),literalPool=hex(pool),observedAddress=hex(value),access=hex(access),mnemonic=mnemonic,accessWidth=1,originalStorageCredit=0))
    return dict(status='passed',originalBinarySha256=sha256(binary),cases=records,sourceOrStorageCredit=0,actualNativeInstructionsExecuted=0)


def execute():
    result=qualify();negatives=[]
    for label,arguments in [('wrong-data-address',dict(expected=0x02102d7c)),('wrong-memory-width',dict(width=2))]:
        try:qualify(**arguments)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original-data witness accepted')
    return dict(result,negativeControls=negatives)
