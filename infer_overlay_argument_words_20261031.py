import hashlib
import re
import infer_native_argument_words_20261031 as flow
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM


def main():
    reference=read_json(ROOT/'evidence/attempts/main-native-register-abi-20261031.json');assert reference['romSha256']==configuration()['romSha256']
    main_rows={int(row['address'],0):row for row in reference['results']};main_masks={address:row['incomingRegisterMask'] for address,row in main_rows.items()}
    main_closed={address for address,row in main_rows.items() if not row['ownUnresolved'] and not row['unknownDirectTargets'] and not row['stackReadsUnqualified'] and not row['argumentHomesUnqualified']}
    summaries=[]
    for module in ['ov000','ov001','ov002','ov003','ov004','ov005','ov006','ov007']:
        path=ROOT/f'config/arm9/overlays/{module}/symbols.txt'
        if not path.is_file():continue
        metadata,data,config=measured_module(module);flow.BASE=0x021D7240
        functions={int(address,0):(name,int(size,0)) for name,size,address in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',path.read_text(),re.M)}
        decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
        graphs={address:flow.graph(data,address,size,decoder) for address,(name,size) in functions.items()};masks={address:0 for address in functions}
        hazards={address:bool(graph[1] or graph[2] or graph[3] or any(node['callee'] is not None and node['callee'] not in functions and node['callee'] not in main_closed for node in graph[0].values())) for address,graph in graphs.items()}
        rounds=0
        while True:
            rounds+=1;callee_masks=main_masks|masks;new_masks={address:masks[address]|flow.incoming(graph[0],address,callee_masks) for address,graph in graphs.items()}
            new_hazards={address:hazards[address] or any(hazards.get(node['callee'],False) for node in graph[0].values()) for address,graph in graphs.items()}
            if new_masks==masks and new_hazards==hazards:break
            masks,hazards=new_masks,new_hazards;assert rounds<=5*len(functions)+1
        rows=[]
        for address,(name,size) in functions.items():
            graph,unresolved,stack,homes=graphs[address];words=masks[address].bit_length()
            rows.append(dict(processor='arm9',program='',module=module,mode='arm',address=hex(address),symbol=name,nativeBytes=size,nativeBodySha256=hashlib.sha256(data[address-flow.BASE:address-flow.BASE+size]).hexdigest(),incomingRegisterMask=masks[address],minimumArgumentWords=words,draftContextEligible=bool(words) and not hazards[address],transitiveUnqualified=hazards[address],ownUnresolved=unresolved,stackReadsUnqualified=stack,argumentHomesUnqualified=homes,alias=f'func_{address:08x}',contextPrototype=f"extern u32 func_{address:08x}({', '.join(['u32']*words) if words else 'void'});",sourceCredit=0))
        output=ROOT/f'evidence/attempts/{module}-native-register-abi-20261031.json'
        write_json(output,dict(romSha256=configuration()['romSha256'],processor='arm9',module=module,loadAddress=hex(flow.BASE),moduleSha256=hashlib.sha256(data).hexdigest(),generatorSha256=sha256(__file__),flowEngineSha256=sha256(ROOT/'infer_native_argument_words_20261031.py'),mainReferenceSha256=sha256(ROOT/'evidence/attempts/main-native-register-abi-20261031.json'),fixedPointRounds=rounds,sourceCredit=0,results=rows,limitations=['Raw read-before-definition register minima only; no historical or complete ABI claim','Only ARM entries; heuristic boundaries, stack arguments, pointer types, return values and Thumb paths remain unqualified','Main direct-callee masks are reused; transitive unresolved/stack/home paths exclude fixed contexts','Opaque raw word declarations must preserve any independently qualified concrete return/parameter types','Each caller still requires native boundary/return/effect evidence and genuine compilation/linking']))
        summaries.append(dict(module=module,functions=len(rows),eligible=sum(row['draftContextEligible'] for row in rows),report=output.relative_to(ROOT).as_posix()))
        print(summaries[-1],flush=True)
    write_json(ROOT/'evidence/attempts/overlay-native-register-abi-summary-20261031.json',dict(romSha256=configuration()['romSha256'],sourceCredit=0,modules=summaries))


if __name__=='__main__':main()
