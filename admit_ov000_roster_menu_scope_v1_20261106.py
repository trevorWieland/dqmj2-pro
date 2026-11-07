import hashlib
import json
import re
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_ov000_large_actor_readonly_scout import cfg as native_cfg


def main():
    proposal='evidence/lanes/parallel-wave20261106/ov000-roster-menu-scout/proposal.json'
    assert sha256(ROOT/proposal)=='eddaf1d7ab09f9a82b70361ed442869649be6ebb7783f7dcefc3091b6acfc60f'
    j=read_json(ROOT/proposal)
    expected={0x021f8134:400,0x021f85c8:624,0x021f8838:292,0x021f8e6c:260,
        0x021f9178:260,0x021f933c:328,0x021f9a18:316,0x021f9b54:264,
        0x021fa498:536,0x021fa6b0:1116,0x021fedf0:280,0x02202070:324}
    rows=j['entries']
    assert len(rows)==12 and {int(r['identity']['address'],0):r['identity']['bytes']for r in rows}==expected
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
    for pin in j['pins']:
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
        assert sorted(incoming,key=lambda x:(x['sourcePath'],x['record']))==sorted(entry['actualIncomingRecords'],key=lambda x:(x['sourcePath'],x['record']))
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
    folder=ROOT/'evidence/lanes/parallel-wave20261106/ov000-roster-menu-next'
    source='src/runtime/parallel_wave20261106/ov000-roster-menu-next'
    assert not folder.exists()and not(ROOT/source).exists()and not(ROOT/'work/w6rm').exists()
    assert not list(ROOT.glob('wave20261106_ov000_roster_menu_source_*.py'))
    claim=(folder/'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT/claim,dict(owner='workflow_research',status='coordinator-admitted-source-scope-no-credit',sourceCredit=0,
        createdUtc=now(),sourceRevision=revision,exclusiveSourceRoot=source,exclusiveWorkRoot='work/w6rm',
        helperPrefix='wave20261106_ov000_roster_menu_source_',claimedFunctions=claimed,
        reconstructionBasis='measured-game-code-and-pinned-accepted-main-interfaces-no-public-primary-source-claim'))
    write_json(folder/'coordinator-admission.json',dict(passed=True,sourceCredit=0,claim=claim,claimSha256=sha256(ROOT/claim),
        exclusiveSourceRoot=source,functions=12,initializedCandidateBytes=5000,sourceRevision=revision,
        proposal=dict(path=proposal,sha256=sha256(ROOT/proposal)),protectionPins=pins,sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT/'evidence/lanes/parallel-wave20261102/dispatch.json'),
        originalRomOverlay0IndependentlyDecompressed=True,fullNativeCfgLiteralCoverageAndIncomingNamespacesRechecked=True,
        allAcceptedCodeDataLinkageCurrentClaimsAndSpecificationsProtected=True,generatorSha256=sha256(__file__)))
    print(dict(passed=True,functions=12,bytes=5000,sourceCredit=0))


if __name__=='__main__':
    main()
