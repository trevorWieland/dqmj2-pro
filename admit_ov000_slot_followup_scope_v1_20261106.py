import hashlib
import json
import re
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_ov000_controller_followup_readonly_scout import cfg_v2 as native_cfg


def main():
    proposal='evidence/lanes/parallel-wave20261106/ov000-controller-followup-scout/proposal-v2.json'
    assert sha256(ROOT/proposal)=='670aaf6b302ceea937142bff8dbb66aec1ffca6ed93a58fbaffc8dde5b8ab2a1'
    j=read_json(ROOT/proposal)
    expected={0x021ef008:168,0x021ef77c:140,0x021efaac:292,0x021efec4:132,
        0x021f29ac:116,0x021f30e4:176,0x02206868:164,0x02207acc:176,
        0x0220820c:232,0x02208854:196,0x022162e4:108,0x02217dbc:144,
        0x02217f14:100,0x0221d05c:180,0x022202f4:300,0x0222390c:116}
    rows=j['entries']
    assert len(rows)==16 and {int(r['identity']['address'],0):r['identity']['bytes']for r in rows}==expected
    revision='0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
    raw=subprocess.check_output(['git','show',revision+':ledger/functions.jsonl'],cwd=ROOT)
    ledger=[json.loads(line)for line in raw.splitlines()]
    selected={r['id']:r for r in ledger}
    protected=[];pins=[]
    def protect(document):
        protected.extend((a,b)for program,cpu,module,a,b in intervals(document)if(program,cpu,module)==('', 'arm9','ov000'))
    protect([r for r in ledger if r['states']['functionMatched']or r.get('sourceUnit')])
    for name,key in [('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        data=subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT)
        protect(json.loads(data)[key]);pins.append(dict(gitObject=revision+':'+name,sha256=hashlib.sha256(data).hexdigest()))
    paths=sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)));protect(read_json(path))
    for pin in j['actualInputPins']:
        assert sha256(ROOT/pin['path'])==pin['sha256']
    config=configuration();native_dependencies(config)
    assert sha256(config['rom'])==config['romSha256']
    import ndspy.rom
    rom=ndspy.rom.NintendoDSRom(config['rom'].read_bytes())
    overlay=rom.loadArm9Overlays([0])[0]
    metadata=next(r for r in read_json(ROOT/'provenance/seed-manifest.json')['modules']if r['name']=='ov000')
    image=bytes(overlay.data);base=overlay.ramAddress
    assert base==int(metadata['base'],0)and image==(ROOT/metadata['binary']).read_bytes()
    assert hashlib.sha256(image).hexdigest()==metadata['sha256']
    symbol_lines=(ROOT/'config/arm9/overlays/ov000/symbols.txt').read_text(encoding='utf-8').splitlines()
    relocation_lines=(ROOT/'config/arm9/overlays/ov000/relocs.txt').read_text(encoding='utf-8').splitlines()
    claimed=[]
    for entry in rows:
        row=entry['identity'];start,size=int(row['address'],0),row['bytes'];old=selected[row['id']]
        assert (row.get('program')or'',row['processor'],row['module'],row['mode'])==('', 'arm9','ov000','arm')
        assert not old['states']['functionMatched']and not old['sourceUnit']and old['bytes']==size
        assert not any(max(start,a)<min(start+size,b)for a,b in protected)
        assert entry['canonicalInventoryRecord']in symbol_lines
        for line in symbol_lines:
            m=re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)',line)
            assert not m or not start<int(m[1],0)<start+size
        outgoing=[line for line in relocation_lines if(m:=re.match(r'from:(0x[0-9a-fA-F]+)',line))and start<=int(m[1],0)<start+size]
        incoming=[]
        for path in sorted((ROOT/'config/arm9').rglob('relocs.txt')):
            relative=path.relative_to(ROOT).as_posix()
            caller='main' if path.parent==ROOT/'config/arm9' else path.parent.name
            for line in path.read_text(encoding='utf-8').splitlines():
                m=re.search(r' to:(0x[0-9a-fA-F]+) module:(.+)$',line)
                if m and (int(m[1],0)&~1)==start and 'overlay(0)'in m[2]:
                    incoming.append(dict(callerProgram='',callerProcessor='arm9',callerModule=caller,
                        record=line,targetNamespaceQualifier=m[2],ambiguous=m[2]!='overlay(0)',sourcePath=relative))
        assert outgoing==entry['originalRelocationRecords']
        fields=['callerProgram','callerProcessor','callerModule','record','targetNamespaceQualifier','ambiguous','sourcePath']
        projection=lambda values:sorted([tuple(v[k]for k in fields)for v in values])
        assert projection(incoming)==projection(entry['actualIncomingRecords'])
        assert all(not v['ambiguous'] and not v['interiorTarget'] and v['targetOverlayCandidates']==[0]for v in entry['actualIncomingRecords'])
        assert hashlib.sha256(image[start-base:start-base+size]).hexdigest()==entry['nativeSha256']==row['inputBytesSha256']
        flow=native_cfg(image,base,start,size)
        assert flow==entry['cfg']and not flow['issues']and flow['exits']
        coverage=set()
        for instruction in flow['instructions']:
            a=int(instruction['address'],0);assert image[a-base:a-base+4].hex()==instruction['bytes'];coverage.update(range(a,a+4))
        for literal in flow['literals']:
            a=int(literal['address'],0);assert literal['insideConfiguredExtent'];assert image[a-base:a-base+4].hex()==literal['bytes'];coverage.update(range(a,a+4))
        assert coverage==set(range(start,start+size))
        claimed.append(dict(id=row['id'],program='',processor='arm9',module='ov000',mode='arm',address=hex(start),bytes=size,
            targetSha256=entry['nativeSha256'],canonicalInventoryRecord=entry['canonicalInventoryRecord'],
            originalRelocationRecords=outgoing,originalIncomingRecords=incoming,sourceMeaning='measured-native-game-reconstruction-names-remain-hypotheses'))
    assert all(not p.get('path')or sha256(ROOT/p['path'])==p['sha256']for p in pins)
    folder=ROOT/'evidence/lanes/parallel-wave20261106/ov000-slot-controller-followup'
    source='src/runtime/parallel_wave20261106/ov000-slot-controller-followup'
    assert not folder.exists()and not(ROOT/source).exists()and not(ROOT/'work/w6ocf').exists()
    assert not list(ROOT.glob('wave20261106_ov000_slot_controller_followup_*.py'))
    claim=(folder/'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT/claim,dict(owner='ds_tooling_research',status='coordinator-admitted-source-scope-no-credit',sourceCredit=0,
        createdUtc=now(),sourceRevision=revision,exclusiveSourceRoot=source,exclusiveWorkRoot='work/w6ocf',
        helperPrefix='wave20261106_ov000_slot_controller_followup_',claimedFunctions=claimed,
        reconstructionBasis='measured-game-code-and-pinned-accepted-main-interfaces-no-public-primary-source-claim'))
    write_json(folder/'coordinator-admission.json',dict(passed=True,sourceCredit=0,claim=claim,claimSha256=sha256(ROOT/claim),
        exclusiveSourceRoot=source,functions=16,initializedCandidateBytes=2740,sourceRevision=revision,
        proposal=dict(path=proposal,sha256=sha256(ROOT/proposal)),protectionPins=pins,sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT/'evidence/lanes/parallel-wave20261102/dispatch.json'),
        originalRomOverlay0IndependentlyDecompressed=True,fullNativeCfgLiteralCoverageAndIncomingNamespacesRechecked=True,
        allAcceptedCodeDataLinkageCurrentClaimsAndSpecificationsProtected=True,generatorSha256=sha256(__file__)))
    print(dict(passed=True,functions=16,bytes=2740,sourceCredit=0))


if __name__=='__main__':
    main()
