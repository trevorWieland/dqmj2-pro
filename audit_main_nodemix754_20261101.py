import re
import struct
import match_runtime as c
from project import ROOT,write_json
from link_runtime_unit import measured_module
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM

def execute():
    main,binary,unused=measured_module('main');cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);start,end=0x02030F58,0x020316A4
    calls=[dict(pc=hex(i.address),mnemonic=i.mnemonic,target=i.op_str)for i in cs.disasm(binary[start-0x02000000:end-0x02000000],start)if i.mnemonic in['bl','blx','bx']]
    hits=[];offset=0
    while True:
        offset=binary.find(struct.pack('<I',start),offset)
        if offset<0:break
        hits.append(0x02000000+offset);offset+=1
    if len(hits)!=1:raise ValueError('754 callback word inventory differs')
    hit=hits[0];table=hit-9*4;symbols=(ROOT/'config/arm9/symbols.txt').read_text();refs=[]
    for line in symbols.splitlines():
        match=re.match(r'\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$',line)
        if not match:continue
        address,size=int(match[2],0),int(match[1],0)
        for insn in cs.disasm(binary[address-0x02000000:address-0x02000000+size],address):
            operand=re.search(r'\[pc(?:, #(-?0x[0-9a-f]+|-?\d+))?\]',insn.op_str)
            if insn.mnemonic!='ldr'or not operand:continue
            pointer=insn.address+8+(int(operand[1],0)if operand[1]else 0)
            if 0x02000000<=pointer<0x02000000+len(binary)-4 and struct.unpack_from('<I',binary,pointer-0x02000000)[0]==table:refs.append(dict(function=hex(address),pc=hex(insn.address),literalAddress=hex(pointer),tableAddress=hex(table)))
    report=dict(schemaVersion=1,romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',module='main',processor='arm9',program='',moduleSha256=main['sha256'],address=hex(start),mode='arm',spanBytes=1884,codeBytes=1868,literalBytes=16,spanSha256=c.sha(binary[start-0x02000000:start-0x02000000+1884]),directCalls=calls,bodyIndirectCallbackCalls=0,defaultCallbackTableLead=dict(address=hex(table),entryIndex=9,entryAddress=hex(hit),entries=[hex(x)for x in struct.unpack_from('<14I',binary,table-0x02000000)],staticLiteralReferences=refs),signature=dict(kept='void(NNSG3dRS*,u32)',requiredEntryRegisterWords=1,secondWord='Public reference callback-table formal retained; native first load overwrites incoming R1 before consumption.'),accessedLayouts=dict(state=dict(c='0x00 pointer32',render='0x04 pointer32',isEvpCached='0xCC two u32 words'),render=dict(model='0x04 pointer32'),model=dict(inverseOffset='0x10 u32 byte offset'),inverse=dict(stride=84,matrix43Bytes=48,normal33Bytes=36),globalCache=dict(referenceBase='0x020EE1F8',evpCache='0x020EF5F8',cacheStride=100,matrix44Bytes=64,normal33Bytes=36)),hardwareTransfer=dict(entry='0x0200434C',tail='0x02005994',readWords=12,meaningfulNormalWords=9,canonicalTrailingWords='Saved incoming R4/R5/R6 at three adjacent physical stack slots; recorded separately from mathematical matrix values.'),limits=['Callback table identity is a static reference lead. Dispatcher/ordinary scene execution is not established by this packet.','Full reference structures and unused fields remain historical type hypotheses. Only accessed offsets/widths and actual helper footprints are measured here.','No data/table/global BSS source credit; table words are original binary evidence only.','Main ARM symbol-inventory literal scan is bounded static evidence; computed/Thumb/other-program references are not excluded.'])
    report['measuredStaticDispatcher']=dict(entry='0x0202F820',bytes=72,tableLoadPc='0x0202F824',indirectCallPc='0x0202F850',preparedR0='render-state pointer retained from dispatcher incomingR0',preparedR1='unsigned command byte masked0xE0',tableIndex='unsigned command byte masked0x1F',nodeMixIndex=9,sourceFormalType='void(NNSG3dRS*,u32)',execution='Not run by this static audit; direct NODEMIX harness is separately native-qualified.')
    write_json(ROOT/'evidence/abi/main-nodemix754-static-callback-layout-20261101.json',report)
    print(dict(callbackTable=hex(table),references=refs),flush=True)

if __name__=='__main__':execute()
