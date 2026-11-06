import collections
import hashlib
import re
from project import ROOT,configuration,native_dependencies,sha256,write_json,now
native_dependencies(configuration())
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_INS_B,ARM_INS_BL,ARM_INS_BLX,ARM_INS_BX,ARM_INS_POP,ARM_INS_PUSH,ARM_INS_SVC,ARM_OP_IMM,ARM_OP_MEM,ARM_CC_AL,ARM_CC_INVALID
from capstone.arm import ARM_REG_PC,ARM_REG_LR,ARM_REG_SP
from link_runtime_unit import measured_module

BASE=0x02000000
OUTPUT=ROOT/'evidence/attempts/main-native-register-abi-20261031.json'


def graph(data,address,size,decoder):
    nodes={};pending=[address];unresolved=set();stack_reads=False;homes=False
    while pending:
        pc=pending.pop()
        if pc in nodes:continue
        if not address<=pc<address+size or pc&3:unresolved.add('branch outside declared body');continue
        items=list(decoder.disasm(data[pc-BASE:pc-BASE+4],pc,count=1))
        if len(items)!=1:unresolved.add('undecodable reachable instruction');continue
        ins=items[0]
        try:read,written=ins.regs_access()
        except Exception:unresolved.add('register effects unavailable');continue
        bits=lambda regs:sum(1<<int(decoder.reg_name(r)[1:]) for r in set(regs) if decoder.reg_name(r) in {'r0','r1','r2','r3'})
        used=0 if ins.id==ARM_INS_PUSH else bits(read);defined=bits(written);conditional=ins.cc not in [ARM_CC_AL,ARM_CC_INVALID]
        if ins.id==ARM_INS_PUSH:
            names={decoder.reg_name(r) for r in read};homes|=any(r in names for r in ['r0','r1','r2'])
        for operand in ins.operands:
            if operand.type==ARM_OP_MEM and operand.mem.base==ARM_REG_SP and ins.mnemonic.startswith(('ldr','ldm')):stack_reads=True
        successors=[];callee=None;call=False;tail=False
        if ins.id in [ARM_INS_BL,ARM_INS_BLX]:
            call=True
            if ins.operands and ins.operands[0].type==ARM_OP_IMM:callee=ins.operands[0].imm
            else:unresolved.add('indirect call ABI')
            successors.append(pc+4)
        elif ins.id==ARM_INS_B:
            target=ins.operands[0].imm
            if address<=target<address+size:successors.append(target)
            else:callee=target;tail=True
            if conditional:successors.append(pc+4)
        elif ins.id==ARM_INS_BX:
            if not ins.operands or ins.operands[0].reg!=ARM_REG_LR:unresolved.add('indirect branch ABI')
            if conditional:successors.append(pc+4)
        elif ARM_REG_PC in written:
            returning=ins.id==ARM_INS_POP or any(op.type==ARM_OP_MEM and op.mem.base==ARM_REG_SP for op in ins.operands) or any(op.type!=ARM_OP_MEM and getattr(op,'reg',None)==ARM_REG_LR for op in ins.operands)
            if not returning:unresolved.add('computed PC control flow')
            if conditional:successors.append(pc+4)
        elif ins.id==ARM_INS_SVC:
            unresolved.add('software interrupt ABI')
        else:successors.append(pc+4)
        successors=[x for x in successors if x!=address+size]
        if not successors and not tail and ins.id not in [ARM_INS_BX,ARM_INS_SVC] and ARM_REG_PC not in written:unresolved.add('unqualified fallthrough end')
        nodes[pc]={'read':used,'written':defined,'conditional':conditional,'successors':successors,'callee':callee,'call':call,'tail':tail}
        pending.extend(x for x in successors if x not in nodes)
    return nodes,sorted(unresolved),stack_reads,homes


def incoming(nodes,address,callee_masks):
    states={address:15};pending=collections.deque([address]);used=0
    while pending:
        pc=pending.popleft()
        if pc not in nodes:continue
        node=nodes[pc];live=states[pc];used|=node['read']&live
        if node['callee'] is not None:used|=callee_masks.get(node['callee'],0)&live
        if not node['conditional']:
            live&=~node['written']
            if node['call']:live=0
        for nxt in node['successors']:
            before=states.get(nxt,0);after=before|live
            if nxt not in states or after!=before:states[nxt]=after;pending.append(nxt)
    return used


def main():
    metadata,data,config=measured_module('main');decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    functions={int(address,0):(name,int(size,0)) for name,size,address in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',(ROOT/'config/arm9/symbols.txt').read_text(),re.M)}
    graphs={};masks={address:0 for address in functions}
    for address,(name,size) in functions.items():graphs[address]=graph(data,address,size,decoder)
    rounds=0
    while True:
        rounds+=1;next_masks={a:masks[a]|incoming(g[0],a,masks) for a,g in graphs.items()}
        if next_masks==masks:break
        masks=next_masks;assert rounds<=4*len(functions)+1
    rows=[]
    for address,(name,size) in functions.items():
        nodes,unresolved,stack_reads,homes=graphs[address];mask=masks[address];arity=mask.bit_length();unknown=sorted({n['callee'] for n in nodes.values() if n['callee'] is not None and n['callee'] not in graphs})
        eligible=bool(mask) and not unresolved and not stack_reads and not homes and not unknown
        rows.append({'processor':'arm9','program':'','module':'main','mode':'arm','address':hex(address),'symbol':name,'nativeBytes':size,'nativeBodySha256':hashlib.sha256(data[address-BASE:address-BASE+size]).hexdigest(),'reachableInstructions':len(nodes),'incomingRegisterMask':mask,'incomingRegisterWords':[f'r{x}' for x in range(4) if mask&(1<<x)],'minimumArgumentWords':arity,'draftContextEligible':eligible,'ownUnresolved':unresolved,'unknownDirectTargets':[hex(x) for x in unknown],'stackReadsUnqualified':stack_reads,'argumentHomesUnqualified':homes,'alias':f'func_{address:08x}','contextPrototype':f"extern u32 func_{address:08x}({', '.join(['u32']*arity) if arity else 'void'});",'sourceCredit':0})
    by_address={int(r['address'],0):r for r in rows};checks=[]
    for address,expected in [(0x02008BE0,3),(0x02036830,2),(0x0203694C,2),(0x02036994,2),(0x0203CB8C,3),(0x020343FC,3),(0x020236E8,4)]:
        row=by_address[address];assert row['minimumArgumentWords']==expected,(hex(address),row)
        checks.append({'address':hex(address),'expectedRegisterWords':expected,'measured':row['minimumArgumentWords']})
    report={'createdUtc':now(),'romSha256':configuration()['romSha256'],'nativeModulePath':'extract/arm9/arm9.bin','nativeModuleSha256':sha256(ROOT/'extract/arm9/arm9.bin'),'generatorSha256':sha256(ROOT/'infer_native_argument_words_20261031.py'),'sourceCredit':0,'fixedPointRounds':rounds,'functions':len(rows),'eligibleDraftContexts':sum(x['draftContextEligible'] for x in rows),'calibration':checks,'results':rows,'limitations':['Read-before-def register flow provides experimental raw-word hypotheses, not historical signatures or complete native ABI proofs','Only host main ARM entries are analyzed; all boundaries remain subject to the measured inventory confidence','Stack argument counts, multiword/flags returns and nonstandard conventions are unqualified','Pushes used for register saving/local allocation do not count as semantic argument reads; argument-home and stack-read functions are excluded from fixed contexts','Unknown indirect/computed/software-interrupt paths exclude fixed contexts; direct-callee effects are a monotone register-use fixed point','Every caller still requires independent compilation, genuine linking, defined source and actual native-return gates']}
    write_json(OUTPUT,report);print({k:report[k] for k in ['functions','eligibleDraftContexts','fixedPointRounds','sourceCredit']})


if __name__=='__main__':main()
