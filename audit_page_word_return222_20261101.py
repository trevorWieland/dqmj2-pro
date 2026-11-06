from pathlib import Path
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'deps/native')]
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from capstone.arm import ARM_REG_R0


def number(operand):return int(operand.removeprefix('#'),0)


def main():
    rows=[]
    receipts=[]
    modules=json.loads((ROOT/'provenance/seed-manifest.json').read_text())['modules']
    for module in modules:
        blob=(ROOT/module['binary']).read_bytes()
        assert hashlib.sha256(blob).hexdigest()==module['sha256']
        symbols=ROOT/module['symbolsFile']
        text=symbols.read_text()
        base=int(module['base'],0)
        receipts.append(dict(module=module['name'],moduleSha256=module['sha256'],symbolsFile=module['symbolsFile'],symbolsSha256=hashlib.sha256(symbols.read_bytes()).hexdigest()))
        for name,mode,length,address in re.findall(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',text,re.M):
            at,size=int(address,0),int(length,0)
            cs=Cs(CS_ARCH_ARM,CS_MODE_ARM if mode=='arm' else CS_MODE_THUMB)
            cs.skipdata=True
            cs.detail=True
            instructions=list(cs.disasm(blob[at-base:at-base+size],at))
            lookup={i.address:i for i in instructions}
            for inst in instructions:
                if inst.mnemonic not in ['bl','blx'] or inst.op_str.lower()!='#0x206e6c0':continue
                path=[]
                point=inst.address+inst.size
                result='Unqualified'
                for _ in range(8):
                    current=lookup.get(point)
                    if current is None:break
                    path.append(dict(address=hex(point),mnemonic=current.mnemonic,operands=current.op_str))
                    if current.mnemonic=='b':
                        point=number(current.op_str)
                        continue
                    if current.mnemonic=='bl':
                        if current.op_str=='#0x2062328':result='62328 overwrites R0 before any read'
                        break
                    try:reads,writes=current.regs_access()
                    except Exception:break
                    if ARM_REG_R0 in reads:
                        result='R0 read before overwrite'
                        break
                    if ARM_REG_R0 in writes:
                        result='R0 overwritten before read'
                        break
                    point+=current.size
                rows.append(dict(processor='arm9',program='',module=module['name'],name=name,address=hex(at),mode=mode,bytes=size,callAddress=hex(inst.address),target='0x0206e6c0',followingExecutedPath=path,rawR0UseClassification=result,reachabilityQualified=False))
    arm=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    span=arm[0x62328:0x62328+48]
    assert int.from_bytes(span[4:8],'little')==0xE59F0020
    assert len(rows)==7 and all('before' in row['rawR0UseClassification'] for row in rows)
    result=dict(schemaVersion=1,sourceCredit=0,callSites=rows,moduleReceipts=receipts,nextCallee62328=dict(address='0x02062328',bytes=48,firstR0Definition='0x0206232c LDR R0 fromliteral replaces incoming before R0 read',spanSha256=hashlib.sha256(span).hexdigest()),limitations=[
        'Configured ARM/Thumb disassembly direct immediate BL/BLX targets only;literal/code boundary artifacts,indirect calls,unlisted executable regions andordinary scene reachability remain unproved.',
        'Following unconditional branches and explicit overwrite sites qualify the observed seven direct sites,not original C return intent. Matching raw-u32 andvoid hypotheses remainavailable;preferred raw-u32 retains observed final writer-index1 production andcompatible existing return declarations.'])
    path=ROOT/'evidence/lanes/save-core/page-word-return-consumers222-20261101.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(len(rows),hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':main()
