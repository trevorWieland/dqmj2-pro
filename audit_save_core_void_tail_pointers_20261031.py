import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from capstone.arm import ARM_OP_REG,ARM_OP_MEM,ARM_OP_IMM,ARM_REG_R0,ARM_REG_PC,ARM_CC_AL,ARM_CC_INVALID
from link_runtime_unit import measured_module
from match_mechanics_save_20261029_record33 import MAIN_SHA
SNAPSHOT='evidence/verification/accepted-cohort89-identities-v2-20261031.json'
EXCLUDE={0x02096CF8,0x02096D9C,0x02096D4C,0x02096D6C,0x02096D24,0x02096D04}


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    metadata,binary,config=measured_module('main');assert sha(binary)==MAIN_SHA;base=int(metadata['base'],0)
    functions={int(address,16):dict(alias=alias,mode=mode,bytes=int(size,16)) for alias,mode,size,address in re.findall(r'^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)\) addr:0x([0-9a-f]{8})$',config,re.M)}
    decoders={mode:Cs(CS_ARCH_ARM,CS_MODE_THUMB if mode=='thumb' else CS_MODE_ARM) for mode in ('arm','thumb')}
    for decoder in decoders.values():decoder.detail=True
    def decode(address):
        f=functions[address];return list(decoders[f['mode']].disasm(binary[address-base:address-base+f['bytes']],address))
    def literal(i):
        op=i.operands[1];pc=((i.address+4)&~3) if i.size==2 else i.address+8;address=pc+op.mem.disp
        if not base<=address<=base+len(binary)-4:return None
        return int.from_bytes(binary[address-base:address-base+4],'little')
    def unconditional(i):return i.cc in (ARM_CC_AL,ARM_CC_INVALID)
    def tail(address):
        ins=decode(address)
        if not ins:return None,'Empty native body'
        first=ins[0]
        if first.mnemonic=='b' and unconditional(first) and first.operands[0].type==ARM_OP_IMM:return first.operands[0].imm,'Direct unconditional tail branch preserves incomingR0'
        if len(ins)<2:return None,'Not a simple literal tail'
        second=ins[1]
        if first.mnemonic!='ldr' or not unconditional(first) or len(first.operands)!=2 or first.operands[0].type!=ARM_OP_REG or first.operands[0].reg in (ARM_REG_R0,ARM_REG_PC) or first.operands[1].type!=ARM_OP_MEM or first.operands[1].mem.base!=ARM_REG_PC:return None,'Wrapper changes input or is not simple literal tail'
        if second.mnemonic!='bx' or not unconditional(second) or second.operands[0].type!=ARM_OP_REG or second.operands[0].reg!=first.operands[0].reg:return None,'Not a matching unconditional BX'
        value=literal(first);return (value&~1 if value is not None else None),'Literal scratch-register BX preserves incomingR0'
    def pointer_path(address,depth=0,visited=()):
        if depth>5 or address in visited or address not in functions:return None,'Unknown/recursive callee namespace'
        aliases={ARM_REG_R0:0};steps=[];constants={};f=functions[address]
        for i in decode(address)[:12]:
            steps.append(dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str))
            if not unconditional(i):return None,'Conditional prefix before pointer read'
            ops=i.operands
            if i.mnemonic in ('push','nop') or (i.mnemonic=='mov' and len(ops)==2 and ops[0].type==ARM_OP_REG and ops[1].type==ARM_OP_REG and ops[0].reg==ops[1].reg):continue
            if i.mnemonic in ('ldr','ldrb','ldrh','ldrsb','ldrsh') and len(ops)==2 and ops[1].type==ARM_OP_MEM:
                mem=ops[1].mem
                if mem.base in aliases and not mem.index:
                    return dict(callee=hex(address),mode=f['mode'],readPc=hex(i.address),fixedInputOffset=aliases[mem.base]+mem.disp,readInstruction=i.mnemonic+' '+i.op_str,steps=steps,chain=[hex(address)]),'Unconditional fixed-offset load through incomingR0 alias'
                if mem.base==ARM_REG_PC:
                    value=literal(i)
                    if value is not None:constants[ops[0].reg]=value
                aliases.pop(ops[0].reg,None);continue
            if i.mnemonic=='mov' and len(ops)==2 and ops[0].type==ARM_OP_REG:
                if ops[1].type==ARM_OP_REG and ops[1].reg in aliases:aliases[ops[0].reg]=aliases[ops[1].reg]
                else:aliases.pop(ops[0].reg,None)
                continue
            if i.mnemonic in ('add','sub') and len(ops)==3 and ops[0].type==ARM_OP_REG and ops[1].type==ARM_OP_REG and ops[2].type==ARM_OP_IMM:
                if ops[1].reg in aliases:aliases[ops[0].reg]=aliases[ops[1].reg]+ops[2].imm*(1 if i.mnemonic=='add' else -1)
                else:aliases.pop(ops[0].reg,None)
                continue
            if i.mnemonic in ('b','bl','blx') and ops and ops[0].type==ARM_OP_IMM and ARM_REG_R0 in aliases and aliases[ARM_REG_R0]==0:
                target=ops[0].imm&~1;result,reason=pointer_path(target,depth+1,visited+(address,))
                if result:result=dict(result,steps=steps+result['steps'],chain=[hex(address)]+result['chain']);return result,reason
                return None,reason
            if i.mnemonic=='bx' and ops and ops[0].type==ARM_OP_REG and ops[0].reg in constants and ARM_REG_R0 in aliases and aliases[ARM_REG_R0]==0:
                result,reason=pointer_path(constants[ops[0].reg]&~1,depth+1,visited+(address,))
                if result:result=dict(result,steps=steps+result['steps'],chain=[hex(address)]+result['chain']);return result,reason
                return None,reason
            if i.mnemonic in ('cmp','tst','teq','cmn'):continue
            return None,'Nontrivial or return prefix before qualified pointer load'
        return None,'No qualified dereference in bounded straight prefix'
    snapshot=json.loads((ROOT/SNAPSHOT).read_text());rows=[];skips={};formal_count=0
    for row in snapshot['functions']:
        if row['processor']!='arm9' or row['module']!='main' or row['address'] in EXCLUDE or (row.get('bytes') or 100)>24:continue
        path=ROOT/row['source']
        if not path.is_file() or sha(path.read_bytes())!=row['sourceSha256']:continue
        text=path.read_text();name=row['name'];match=re.search(r'\b'+re.escape(name)+r'\s*\(\s*void\s*\)\s*\{([^{}]*)\}',text,re.S)
        if not match or not re.fullmatch(r'\s*return\s+native_fn_[0-9a-f]{8}\s*\(\s*\)\s*;\s*',match[1]):continue
        formal_count+=1;address=row['address']
        if address not in functions:continue
        target,why=tail(address)
        if target is None:skips[why]=skips.get(why,0)+1;continue
        named=int(re.search(r'native_fn_([0-9a-f]{8})',match[1])[1],16)
        if target!=named:skips['Source/native tail target mismatch']=skips.get('Source/native tail target mismatch',0)+1;continue
        proof,reason=pointer_path(target)
        if proof is None:skips[reason]=skips.get(reason,0)+1;continue
        code=binary[address-base:address-base+functions[address]['bytes']];rows.append(dict(identity=dict(processor='arm9',program='',module='main',mode=row['mode'],address=hex(address),bytes=functions[address]['bytes'],romSha256=snapshot['romSha256']),source=row['source'],sourceSha256=row['sourceSha256'],nativeSha256=sha(code),tailTarget=hex(target),tailReason=why,pointerPath=proof,staticEvidenceOnly=True,sourceCredit=0,proofNeeds=['Fresh isolated native execution must witness this exact dereference with distinct disposable pointers and exclude unsupported conditions/caller states','Actual inbound callers and original ordinary reachability remain unproved','Typed alternative requires compiler+real-link/native-byte gates and caller-dependent controls;old primaries remain frozen'],ownedSourceRange=0x02040000<=address<0x020D0000))
    controls=[]
    for address,positive in [(0x02096D9C,True),(0x020485B4,False),(0x02041800,False)]:
        target,reason=tail(address);proof=None
        if target is not None:proof,reason=pointer_path(target)
        assert bool(proof)==positive,(hex(address),reason,proof)
        controls.append(dict(wrapper=hex(address),positive=positive,qualified=bool(proof),reason=reason,tailTarget=hex(target) if target is not None else None,pointerPath=proof))
    out=dict(schemaVersion=1,sourceCredit=0,readOnly=True,controls=controls,arm9Sha256=MAIN_SHA,snapshot=SNAPSHOT,snapshotSha256=sha((ROOT/SNAPSHOT).read_bytes()),counts=dict(simpleVoidReturnSources=formal_count,pathQualifiedStaticLeads=len(rows),provenNativeOrCDefects=0,newSourceFunctions=0),skips=skips,candidates=rows,limitations=['Narrow selected89 mainARM9 audit only;current source hashes required. Six already qualified140-byte alternatives are excluded. No source/config/ledger is modified.','Only a literal scratch-register BX or unconditional direct tail preserving incomingR0 is admitted. The target path must reach a fixed-offset load through incomingR0 before a conditional/nontrivial/unknown prefix;conditional correlation such as485B4 is not assumed feasible. Raw register reads alone never qualify.','These are static proof leads,not accepted migrations or coverage. Original scene/context/bounds and a bounded native read witness are required before typed-source proposals. Other namespaces,complex wrappers and guarded cases remain outside this audit.'])
    path=ROOT/'evidence/attempts/save-core-void-tail-pointer-audit-20261031.json';path.write_text(json.dumps(out,indent=2)+'\n');print(out['counts']);print('skips',skips);print('candidates',[(x['identity']['address'],x['tailTarget'],x['pointerPath']['readPc']) for x in rows]);print(sha(path.read_bytes()))


if __name__=='__main__':main()

