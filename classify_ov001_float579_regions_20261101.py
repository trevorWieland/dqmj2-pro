import re
from project import ROOT,configuration,write_json
from link_runtime_unit import measured_module
import match_runtime as c


def execute():
    module,body,symbols=measured_module('ov001');records=[]
    for address,size,count in[(0x022122AC,240,2),(0x0221239C,424,3),(0x022125D0,432,3)]:
        if re.search(r'kind:function\(arm,size='+hex(size)+r'\) addr:0x'+f'{address:08x}',symbols)is None:raise ValueError('579 region boundary differs')
        codeEnd=address+size-count*4;span=body[address-0x021D7240:address-0x021D7240+size];literals=[]
        for literal in range(codeEnd,address+size,4):
            readers=[]
            for pc in range(address,codeEnd,4):
                word=int.from_bytes(span[pc-address:pc-address+4],'little')
                if word&0x0F7F0000!=0x051F0000:continue
                target=pc+8+((word&4095)if word&(1<<23)else-(word&4095))
                if target==literal:readers.append(dict(pc=hex(pc),word=f'{word:08x}',condition=word>>28,unconditional=(word>>28)==14))
            if not readers or not any(r['unconditional']for r in readers):raise ValueError('579 literal lacks an unconditional code reader')
            value=int.from_bytes(span[literal-address:literal-address+4],'little')
            if value not in[0x66666667,0x40240000,0x0222E100]:raise ValueError('579 unexpected literal')
            literals.append(dict(address=hex(literal),bytes=4,value=hex(value),readers=readers))
        records.append(dict(processor='arm9',program='',module='ov001',mode='arm',address=hex(address),bytes=size,nativeSpanSha256=c.sha(span),codeBytes=codeEnd-address,literalBytes=count*4,literals=literals,unclassifiedBytes=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],moduleSha256=module['sha256'],functions=records,totalFunctionBytes=sum(r['bytes']for r in records),codeBytes=sum(r['codeBytes']for r in records),literalBytes=sum(r['literalBytes']for r in records),sourceCreditFromClassification=0,limits=['Classification supplements complete C compile/link/execution checks; it contributes no independent source credit.','Width-table pointer is data at a qualified module address; the table extent/meaning and table-source credit remain unresolved.']);write_json(ROOT/'evidence/verification/ov001-float579-regions-20261101.json',report);print(dict(functionBytes=report['totalFunctionBytes'],codeBytes=report['codeBytes'],literalBytes=report['literalBytes'],unclassifiedBytes=0))


if __name__=='__main__':execute()
