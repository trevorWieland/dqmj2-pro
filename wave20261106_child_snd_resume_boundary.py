import hashlib
import struct
import sys
import utility_runtime
from project import ROOT,read_json,configuration,native_dependencies
from wave20261106_child_arm9_boundary_family_readonly_v4 import derive,qualify_return_tokens


def check():
    layout,files=utility_runtime.derive();module=next(m for m in layout['modules']if m['id']=='utility-child-arm9-main');image=files[ROOT/module['binary']];base=int(module['base'],0);inventory=read_json(ROOT/'evidence/utility/ghidra-arm9.json');known={(int(f['address'],0),f['mode'])for f in inventory['functions']if f['module']==module['id']};proof=[]
    for address,size in[(0x2006eb8,196),(0x2006f7c,136)]:
        if(address,'arm')not in known:raise ValueError('Original ARM entry absent')
        limit=min(a for a,m in known if a>address);record=derive(image,base,address,limit,'arm',known)
        if not record['complete']or not record['allExtentBytesClassified']or record['bytes']!=size or record['gaps']or record['derivationUsedAcceptedSourceSize']:raise ValueError('Independent complete native CFG/literal/return envelope changed')
        proof.append(record)
    call=next((c for c in proof[1]['calls']if int(c['origin'],0)==0x2006ff8),None)
    if call is None or(int(call['target'],0),call['targetMode'])!=(0x2006eb8,'arm'):raise ValueError('Actual complete native ARM incoming caller/BL changed')
    sys.path.insert(0,str(native_dependencies(configuration())));from ndspy.rom import NintendoDSRom
    game=NintendoDSRom((ROOT/'inputs/game.nds').read_bytes());payload=game.files[game.filenames.idOf('dwc/utility.bin')]
    if payload!=(ROOT/'extract/files/dwc/utility.bin').read_bytes():raise ValueError('Raw measured-ROM utility payload disagrees with runtime derivation')
    return dict(passed=True,originalProgram='dwc/utility.bin/move/child.srl',processor='arm9',module=module['id'],mode='arm',rawMeasuredRomUtilityPayloadVerified=True,nativeOnlyBoundaries=proof,returnTokenControls=qualify_return_tokens(),sourceCredit=0,callerOrImportedCalleeCredit=0,transitiveApplicationReachabilityProven=False,limits='Original Ghidra entry plus independently complete native caller and real ARM BL establishes private reconstruction entry evidence; application reachability is unproven.')
