import hashlib
import json
import re
import struct
import subprocess
import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_IMM,ARM_OP_MEM,ARM_REG_PC,ARM_CC_AL,ARM_CC_INVALID,ARM_INS_BL,ARM_INS_BLX,ARM_INS_B,ARM_INS_BX
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_nns_primary_readonly_scout import intervals
from qualify_arm7_pm_mic_boundaries_v1_20261106 import bounded_switch
from ndspy.codeCompression import decompress

REVISION='966db0d2ea81f07a861df51addef602de548765e'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov001-command-controller-next-proposal'
SELECTED={0x021fe4ac:160,0x021fe618:160,0x0220aba0:184,0x0220ac9c:212,0x0220ad70:400,0x0220afe4:268,0x0220b0f0:300,0x0220b2fc:72,0x0220b3e4:152}


def blob(name):return subprocess.check_output(['git','show',REVISION+':'+name],cwd=ROOT)


def paths():return sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json')))


def bounded_return_switch(image,base,at):
    compare,dispatch,default=struct.unpack_from('<III',image,at-base-4)
    assert compare&0xfff0f000==0xe3500000 and dispatch&0xfffffff0==0x908ff100 and default==0xe12fff1e
    register=dispatch&15;assert register<15 and(compare>>16)&15==register
    rotate=((compare>>8)&15)*2;immediate=compare&255;upper=((immediate>>rotate)|(immediate<<(32-rotate)))&0xffffffff if rotate else immediate
    assert upper==3;addresses=[at+8+4*i for i in range(upper+1)];words=[struct.unpack_from('<I',image,a-base)[0]for a in addresses];assert all(w>>24==0xea for w in words)
    return dict(dispatch=hex(at),compareAddress=hex(at-4),compareWord=hex(compare),dispatchWord=hex(dispatch),defaultWord=hex(default),defaultReturnsViaBxLr=True,upper=upper,indexRegister=register,tableAddresses=[hex(a)for a in addresses],tableWords=[hex(w)for w in words])


def cfg_v3(image, base, address, size):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    pending, seen, literals, edges, exits, issues, memory, aliases, blocks = [address], {}, set(), [], [], [], [], {}, {address}
    switches=[]
    while pending:
        pc = pending.pop()
        if pc in seen:
            continue
        if not address <= pc < address + size or pc & 3:
            issues.append(dict(kind='CFG-address-outside-configured-extent', address=hex(pc)))
            continue
        data = image[pc - base:pc - base + 4]
        decoded = list(decoder.disasm(data, pc, count=1))
        if len(decoded) != 1 or decoded[0].size != 4:
            issues.append(dict(kind='undecodable-reachable-word', address=hex(pc)))
            continue
        instruction = decoded[0]
        seen[pc] = dict(address=hex(pc), bytes=data.hex(), mnemonic=instruction.mnemonic, operands=instruction.op_str)
        fall, conditional = pc + 4, instruction.cc not in [ARM_CC_AL, ARM_CC_INVALID]
        mnemonic = instruction.mnemonic
        if pc < address + 20 and mnemonic in ['mov', 'movs'] and len(instruction.operands) == 2 and instruction.reg_name(instruction.operands[1].reg) == 'r0':
            aliases[instruction.reg_name(instruction.operands[0].reg)] = 'original-r0'
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM:
                mem = operand.mem
                register = instruction.reg_name(mem.base)
                if mem.base == ARM_REG_PC and not mem.index:
                    literals.add(pc + 8 + mem.disp)
                memory.append(dict(origin=hex(pc), mnemonic=mnemonic, baseRegister=register,
                    indexRegister=instruction.reg_name(mem.index) if mem.index else None, displacement=mem.disp,
                    width=1 if mnemonic.startswith(('ldrb', 'ldrsb', 'strb')) else 2 if mnemonic.startswith(('ldrh', 'ldrsh', 'strh')) else 4,
                    heuristicEarlyR0CopyNotPreservationProof=aliases.get(register), nativeWord=data.hex()))
        if instruction.id in [ARM_INS_BL, ARM_INS_BLX]:
            if instruction.operands and instruction.operands[0].type == ARM_OP_IMM:
                edges.append(dict(origin=hex(pc), kind='call', target=hex(instruction.operands[0].imm)))
            else:
                issues.append(dict(kind='indirect-call-needs-typed-interface', origin=hex(pc), operands=instruction.op_str))
            pending.append(fall)
            continue
        if instruction.id == ARM_INS_BX:
            if instruction.op_str == 'lr':
                exits.append(dict(origin=hex(pc), kind='return', conditional=conditional))
            else:
                issues.append(dict(kind='indirect-branch-needs-entry-proof', origin=hex(pc), operands=instruction.op_str))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if instruction.id == ARM_INS_B and instruction.operands and instruction.operands[0].type == ARM_OP_IMM:
            target = instruction.operands[0].imm
            edges.append(dict(origin=hex(pc), kind='conditional-branch' if conditional else 'branch', target=hex(target)))
            blocks.add(target)
            if address <= target < address + size:
                pending.append(target)
            else:
                exits.append(dict(origin=hex(pc), kind='external-tail', target=hex(target)))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if 'pc' in instruction.op_str and (mnemonic.startswith(('pop', 'ldm')) or mnemonic.startswith('mov') and instruction.op_str.startswith('pc,')):
            exits.append(dict(origin=hex(pc), kind='return-or-pc-write', conditional=conditional))
            if conditional:
                pending.append(fall);blocks.add(fall)
            continue
        if instruction.op_str.startswith('pc,'):
            try:switch=bounded_return_switch(image,base,pc)
            except AssertionError:issues.append(dict(kind='computed-PC-needs-table-proof',origin=hex(pc),operands=instruction.op_str));continue
            switches.append(switch);pending.extend([pc+4]+[int(at,0)for at in switch['tableAddresses']]);continue
        pending.append(fall)
    if any(at in seen for at in literals):
        issues.append(dict(kind='reachable-instruction-also-loaded-as-literal'))
    return dict(switches=switches,reachableWords=len(seen), blockEntryCount=len(blocks), edges=edges, exits=exits, issues=issues,
        literals=[dict(address=hex(at), insideConfiguredExtent=address <= at <= address + size - 4, bytes=image[at - base:at - base + 4].hex()) for at in sorted(literals)],
        memory=memory, instructions=[seen[at] for at in sorted(seen)])


def main():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261106/ov001-command-controller-next-proposal'or LANE.exists():raise ValueError('Fresh exact read-only ov001 proposal scope required')
    ledgerRaw=blob('ledger/functions.jsonl');ledger=[json.loads(line)for line in ledgerRaw.splitlines()];manifestRaw=blob('manifest.json');module=next(m for m in json.loads(manifestRaw)['modules']if m['name']=='ov001'and m['processor']=='arm9'and not m.get('program'));image=(ROOT/module['binary']).read_bytes();base=int(module['base'],0);assert C.sha(image)==module['sha256'];cfg=configuration();assert sha256(cfg['rom'])==cfg['romSha256'];rom=cfg['rom'].read_bytes();ovt,size=struct.unpack_from('<2I',rom,0x50);entries=[struct.unpack_from('<8I',rom,at)for at in range(ovt,ovt+size,32)];record=next(e for e in entries if e[0]==1);assert record[1]==base and record[2]==len(image)and record[3]==module['expectedBssBytes'];fat=struct.unpack_from('<I',rom,0x48)[0];begin,end=struct.unpack_from('<2I',rom,fat+8*record[6]);encoded=rom[begin:end];decoded=decompress(encoded)if record[7]>>24&1 else encoded;assert decoded==image
    before=paths();protect=[];pins=[]
    def add(document,origin):
        protect.extend((a,b,origin)for program,cpu,name,a,b in intervals(document)if(program,cpu,name)==('','arm9','ov001'))
    add([r for r in ledger if r['states']['functionMatched']or r.get('sourceUnit')],REVISION+':ledger/functions.jsonl')
    for name,key in [('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        raw=blob(name);add(json.loads(raw)[key],REVISION+':'+name);pins.append(dict(gitObject=REVISION+':'+name,sha256=C.sha(raw)))
    for path in before:
        raw=path.read_bytes();pins.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=C.sha(raw)));add(json.loads(raw),path.relative_to(ROOT).as_posix())
    symbols='config/arm9/overlays/ov001/symbols.txt';relocs='config/arm9/overlays/ov001/relocs.txt';pins.extend(dict(path=n,sha256=sha256(ROOT/n))for n in[module['binary'],symbols,relocs]);inventory=(ROOT/symbols).read_text().splitlines();relocationLines=(ROOT/relocs).read_text().splitlines();candidates=[];controls=[]
    for a,n in sorted(SELECTED.items()):
        r=next(r for r in ledger if(r.get('program')or'',r['processor'],r['module'],r['mode'],int(r['address'],0))==('','arm9','ov001','arm',a));assert r['bytes']==n and not r['states']['functionMatched']and not r.get('sourceUnit');body=image[a-base:a-base+n];assert C.sha(body)==r['inputBytesSha256'];conflicts=[(x,y,origin)for x,y,origin in protect if max(x,a)<min(y,a+n)];assert not conflicts
        otherExtents=[x['id']for x in ledger if x['id']!=r['id']and(x.get('program')or'',x['processor'],x['module'])==('','arm9','ov001')and x.get('bytes')and max(a,int(x['address'],0))<min(a+n,int(x['address'],0)+x['bytes'])];assert not otherExtents
        canonical=next((line for line in inventory if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),line)),None);assert canonical
        foreign=[x['address']for x in ledger if(x.get('program')or'',x['processor'],x['module'])==('','arm9','ov001')and a<int(x['address'],0)<a+n];assert not foreign;flow=cfg_v3(image,base,a,n);assert not flow['issues']
        assert all(not any(e['target']==sw['dispatch']for e in flow['edges'])for sw in flow['switches'])
        code={int(x['address'],0)+i for x in flow['instructions']for i in range(4)};literal={int(x['address'],0)+i for x in flow['literals']for i in range(4)};assert not code&literal and code|literal==set(range(a,a+n))and all(x['insideConfiguredExtent']for x in flow['literals']);assert all(m['width']==4 and m['mnemonic'].startswith('ldr')for m in flow['memory']if m['baseRegister']=='pc');out=[line for line in relocationLines if(m:=re.match(r'from:(0x[0-9a-f]+)',line))and a<=int(m[1],0)<a+n];assert not any('module:('in line for line in out)
        for switch in flow['switches']:
            at=int(switch['dispatch'],0)-base
            for label,pos,mask in [('conditional-cmp',at-4,0x10000000),('missing-cmp-flags',at-4,1<<20),('other-index',at,1),('wrong-shift',at,1<<7),('wrong-condition',at,0x10000000),('default-call',at+4,1<<24),('case-call',at+8,1<<24),('oversized-index',at-4,None)]:
                changed=bytearray(image);word=struct.unpack_from('<I',changed,pos)[0];struct.pack_into('<I',changed,pos,(word^mask)if mask is not None else((word&~4095)|0x401))
                try:bounded_return_switch(changed,base,int(switch['dispatch'],0))
                except AssertionError:controls.append(dict(address=hex(a),case=label,rejected=True))
                else:raise ValueError(('Malformed original controller switch admitted',label))
        candidates.append(dict(program='',processor='arm9',module='ov001',mode='arm',architecture='ARMv5TE',address=hex(a),bytes=n,endExclusive=hex(a+n),base=base,binary=module['binary'],inputModuleSha256=module['sha256'],targetSha256=C.sha(body),canonicalInventoryRecord=canonical,foreignInteriorEntries=[],protectionIntersections=[],originalRelocationRecords=out,cfg=flow,instructionBytes=len(code),literalBytes=len(literal),sourceCredit=0,semanticMeaning='Unproven game/controller role; field names remain neutral.'))
    helperPins=[];helperEvidence=[]
    for address in[0x02049ad0,0x02049be4]:
        helper=next(r for r in ledger if r['module']=='main'and int(r['address'],0)==address);assert helper['states']['functionMatched'];source=helper['sourceUnit'];assert sha256(ROOT/source)==helper['sourceSha256'];helperPins.append(dict(path=source,sha256=sha256(ROOT/source)))
        for pin in helper['sourceDependencies']:assert sha256(ROOT/pin['path'])==pin['sha256'];helperPins.append(pin)
        helperEvidence.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=helper['bytes'],source=source,sourceSha256=helper['sourceSha256'],acceptedEvidence=helper['evidence'],bodyCredit=0))
    pins+=helperPins;assert paths()==before and all(not p.get('path')or sha256(ROOT/p['path'])==p['sha256']for p in pins)
    report=dict(status='read-only-ov001-controller-proposal-awaits-independent-admission',sourceCredit=0,sourceOwnershipGranted=False,sourceRevision=REVISION,sourceClosure='evidence/verification/cohort171-expanded-source-closure-20261101.json',functions=9,bytes=sum(SELECTED.values()),instructionBytes=sum(r['instructionBytes']for r in candidates),literalBytes=sum(r['literalBytes']for r in candidates),namespace=dict(program='',processor='arm9',module='ov001',mode='arm'),candidates=candidates,originalRawRomOverlay=dict(romSha256=cfg['romSha256'],overlayTableOffset=ovt,record=list(record),fatFileId=record[6],fileStart=begin,fileEnd=end,encodedSha256=C.sha(encoded),decompressedSha256=C.sha(decoded),initializedBytes=len(image),bssBytes=record[3]),actualAcceptedHelperEvidence=helperEvidence,measuredInterfaceFacts=['Accepted main02049ad0 computes global-base+12*index; this proves record stride12,not allocation semantics.','Accepted main02049be4 writes a partial8-byte EntryView footprint and uses an11-argument boundary containing explicit u8/s8 words. A partial8-byte view is not a claim that the indexed record is only8 bytes.','Original ov001 callers reuse those exact main-qualified ARM entries;0220aba0 also follows entry[0] then link+4, reads/writes 32-bit resource fields and byte/signed-byte arguments. Shared ov001 state223df3c uses a signed-byte field0 and32-bit field4;223df44 is byte-indexed. Types/semantics beyond actual accesses remain unknown.','0220ad70/0220afe4/0220b0f0/0220b2fc reuse the local0220aba0/0220ac58 family and shared state. All function/data references retain original main versus overlay(1) qualifiers; no same-address/plural-overlay inference.'],actualSwitchMutationControls=controls,protectionInputPins=pins,gitPins=[dict(gitObject=REVISION+':ledger/functions.jsonl',sha256=C.sha(ledgerRaw)),dict(gitObject=REVISION+':manifest.json',sha256=C.sha(manifestRaw))],limits=['No compiler invocation,reconstruction source,claim,canonical alias,registry/preferences/dispatch,index,old source/helper/Ready or shared outputs changed. All nine spans are currently unclaimed/unaccepted and have no code/data/linkage/current/historical reservation/spec intersections. Root must independently refresh physical scope and raw boundaries before admission.','No complete primary game C is claimed. Native CFG,all code/literal bytes,record widths and existing accepted helper interfaces ground ordinary measured-C reconstruction. SDK/game semantic names and original caller compiler revision remain hypotheses until complete genuine link/ABI/model/wrong-C/source-only copied-root proof.','Imports and all overlay/global BSS/table storage remain zero credit. The sole4-case computed-PC controller uses an actual immediate CMP/ADDLS/BX-LR-default/four-AL-B-case table with eight malformed raw-word guard/condition/shift/call controls. Remaining ambiguities are preserved; physical game/device/rendering execution is not established.'])
    LANE.mkdir();write_json(LANE/'proposal.json',report);print(dict(functions=9,bytes=report['bytes'],instructionBytes=report['instructionBytes'],literalBytes=report['literalBytes'],switchControls=len(controls),sha256=sha256(LANE/'proposal.json')),flush=True)


if __name__=='__main__':main()
