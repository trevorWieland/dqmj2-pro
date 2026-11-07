import sys
import re
from project import ROOT,configuration,native_dependencies
from wave20261106_ov006_resource_slot_source_second_bindings import inputs
from wave20261106_child_arm9_boundary_family_readonly_v4 import derive,qualify_return_tokens


def check():
    value,images,inventories,records=inputs();sys.path.insert(0,str(native_dependencies(configuration())))
    from ndspy.rom import NintendoDSRom
    from ndspy.code import loadOverlayTable
    game=NintendoDSRom((ROOT/'inputs/game.nds').read_bytes());overlays=loadOverlayTable(game.arm9OverlayTable,lambda i,f:game.files[f]);known={(int(a,0),mode)for text in inventories.values()for mode,a in re.findall(r'kind:function\((arm|thumb)[^\n]*?\) addr:(0x[0-9a-f]+)',text)};proof=[]
    for entry in value['entries']:
        module=entry['module'];a=int(entry['address'],0);base=int(value['images'][module]['base'],0)
        if bytes(overlays[int(module[2:])].data)!=images[module]:raise ValueError('Fresh raw measured-ROM complete overlay differs')
        flow=derive(images[module],base,a,a+entry['bytes'],'arm',known)
        if not flow['complete']or not flow['allExtentBytesClassified']or flow['bytes']!=entry['bytes']:raise ValueError('Complete original native CFG/literal/entry-LR flow changed')
        for incoming in entry['originalIncomingRecords']:
            if incoming['record']not in records[incoming['callerModule']].splitlines()or incoming['qualifier']!='overlay(%d)'%int(module[2:]):raise ValueError('Original incoming overlay namespace/record changed')
        proof.append(dict(module=module,originalIncomingRecords=entry['originalIncomingRecords'],completeNativeFlow=flow))
    return dict(passed=True,rawMeasuredRomWholeOverlayImagesVerified=True,entries=proof,returnTokenControls=qualify_return_tokens(),callerOrHelperOrStorageCredit=0,transitiveApplicationReachabilityProven=False)
