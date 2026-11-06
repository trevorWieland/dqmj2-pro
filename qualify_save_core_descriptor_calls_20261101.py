import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import verify_inputs,sha,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM

def main():
    verify_inputs();cache={};rows=[]
    for owner,site in [(0x020506E4,0x0205076C),(0x02050828,0x02050874)]:
        entry=native_entry('main',owner,cache);meta,binary,config=cache['main'];base=int(meta['base'],0);raw=binary[owner-base:site+4-base];ins=[dict(address=hex(i.address),mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(raw,owner)];assert ins[-1]['mnemonic']=='bl' and ins[-1]['operands']=='#0x205f7e0'
        if owner==0x020506E4:
            assert [(i['mnemonic'],i['operands']) for i in ins[-4:]]==[('mov','r0, r6'),('mov','r1, r8'),('mov','r2, r7'),('bl','#0x205f7e0')]
        rows.append(dict(owner=entry,callAddress=hex(site),sliceSha256=sha(raw),instructions=ins,threeWordSetupExplicit=owner==0x020506E4,executionCredit=0))
    out=dict(schemaVersion=1,arm9Sha256=MAIN_SHA,sourceCredit=0,staticEdges=rows,qualifiedObservation='The first caller converts context words +0x10 and +0x14 through original020259B4, keeps their returned words in R8/R7, clamps R8 to0..127, then explicitly supplies R0/R1/R2 at0205076C after a nonzero0205F45C gate. This is static dataflow evidence, without enclosing execution or public parameter meanings.',unresolved='The second edge explicitly sets only R0/R1. Its R2 origin and supported full caller domain remain unqualified. Bounded slot fixtures independently prove that R2 affects object+0xF4; no unconditional caller or scene contract follows.')
    target=ROOT/'evidence/verification/save-core-descriptor-calls133-20261101.json';target.write_text(json.dumps(out,indent=2)+'\n');print(sha(target.read_bytes()))

if __name__=='__main__':main()
