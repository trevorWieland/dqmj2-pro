import hashlib
import json
import struct
import subprocess
from project import ROOT, configuration, read_json, write_json, sha256, now
from qualify_arm7_pm_mic_boundaries_v1_20261106 import close, bounded_switch


def spans(node, parent=None):
    parent = parent or {}
    if isinstance(node, list):
        for item in node:
            yield from spans(item, parent)
    elif isinstance(node, dict):
        context = {key: node.get(key, parent.get(key)) for key in ['program', 'processor', 'module']}
        cpu = context['processor'] or ('arm7' if 'arm7' in (context['module'] or '') else 'arm9')
        if (context['program'] or '', cpu, context['module']) == ('', 'arm7', 'arm7-main'):
            size = node.get('storedBytes', node.get('bytes', node.get('size')))
            if node.get('address') and size:
                start = int(node['address'], 0) if isinstance(node['address'], str) else node['address']
                if isinstance(size, str):
                    size = len(bytes.fromhex(size)) if 'instruction' in node else int(size, 0)
                assert type(size) is int and size > 0
                yield start, start + size
        for item in node.values():
            yield from spans(item, context)


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/arm7-wl-rxman-next-proposal/proposal.json'
    assert sha256(ROOT / proposal_name) == '431d414c7d406cd508bd7a936ed47011dd5b534645390a841fb8ebeb0a3a27ac'
    proposal = read_json(ROOT / proposal_name)
    expected = {0x027f3f40:1716}
    evidence=proposal['nativeBoundary']
    assert evidence['extentDerivedIndependentlyBeforeSourceComparison']and not evidence['currentPhysicalConflicts']
    flow_name='evidence/lanes/parallel-wave20261106/arm7-wl-rxman-next-proposal/coordinator-native-flow.json'
    if(ROOT/flow_name).exists():assert read_json(ROOT/flow_name)==evidence['flow']
    else:write_json(ROOT/flow_name,evidence['flow'])
    flow_pin=dict(path=flow_name,sha256=sha256(ROOT/flow_name))
    rows=[dict(proposal['identity'],boundaryProof=dict(status='passed'),foreignInteriorEntries=[],protectionIntersections=[],flow=flow_pin,instructionBytes=1704,literalBytes=12,targetSha256=evidence['targetSha256'])]
    assert len(rows)==1 and {int(r['address'],0):r['bytes'] for r in rows} == expected
    revision = '0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
    content = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in content.splitlines()]
    protected = list(spans([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(content).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        protected.extend(spans(read_json(path)))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw).hexdigest()))
        protected.extend(spans(json.loads(raw)[key]))
    for pin in [proposal['primarySource']]:
        data = (ROOT / pin['path']).read_bytes()
        assert sha256(ROOT / pin['path']) == pin['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == pin['gitBlob']
    for pin in proposal['actualInputPins']:
        assert sha256(ROOT/pin['path'])==pin['sha256']
    function=proposal['publishedFunction']
    assert hashlib.sha256(function['publishedText'].encode()).hexdigest()==function['bodySha256']
    witness=proposal['sourceCompilerContext'];ready=witness['sameTUFrozenReady']
    assert sha256(ROOT/ready['path'])==ready['sha256'] and sha256(ROOT/witness['compiler'])==witness['compilerSha256']
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']; rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]
    assert struct.unpack_from('<3I', raw, 160024) == (0x037f8000, 63096, 15980)
    assert struct.unpack_from('<3I', raw, 160036) == (0x027e0000, 96388, 6504)
    image, base = raw[63636:160024], 0x027e0000
    assert image == (ROOT / 'extract/arm7/runtime/arm7-main.bin').read_bytes()
    assert hashlib.sha256(image).hexdigest() == 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'
    import link_arm7_bulk_20261030 as original
    modules, functions = original.namespace(''); reviews, claimed = [], []
    for row in rows:
        start, size = int(row['address'], 0), row['bytes']
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm7', 'arm7-main', 'arm')
        assert row['boundaryProof']['status']=='passed' and not row['foreignInteriorEntries']
        assert not row['protectionIntersections']
        assert not any(max(start, a) < min(start + size, b) for a, b in protected)
        assert start in functions and functions[start]['module'] == 'arm7-main' and functions[start]['mode'] == 'arm'
        assert not any(start < address < start + size for address, item in functions.items() if item['module'] == 'arm7-main')
        flow_pin = row['flow']
        assert sha256(ROOT / flow_pin['path']) == flow_pin['sha256']
        adapted = dict(row, entryReachableInstructionBytes=row['instructionBytes'],
            actualLiteralReadBytes=row['literalBytes'], nativeSpanSha256=row['targetSha256'])
        review = close(adapted,image,base)
        assert review['instructionBytes']==1704 and review['literalBytes']==12 and review['completePerOriginLiteralLoads']==len(evidence['flow']['literalReads'])
        assert len(review['originalSwitches'])==2 and all(x['upper']==12 for x in review['originalSwitches'])
        switches=[]
        for original_switch in review['originalSwitches']:
            dispatch=int(original_switch['dispatch'],0);at=dispatch-base
            for label,position,mask in [('conditional-cmp',at-4,0x10000000),('missing-cmp-flags',at-4,1<<20),('other-index',at,1),('wrong-shift',at,1<<7),('wrong-condition',at,0x10000000),('default-call',at+4,1<<24),('case-call',at+8,1<<24),('oversized-index',at-4,None)]:
                changed=bytearray(image);word=struct.unpack_from('<I',changed,position)[0]
                struct.pack_into('<I',changed,position,(word^mask)if mask is not None else((word&~4095)|0x401))
                try:bounded_switch(changed,base,dispatch)
                except AssertionError:switches.append(dict(dispatch=hex(dispatch),case=label,rejected=True))
                else:raise AssertionError(label)
        assert len(switches)==16
        review['independentActualSwitchNegativeControls']=switches
        review['nativeSpanSha256']=row['targetSha256'];reviews.append(review)
        claimed.append(dict(program='', processor='arm7', module='arm7-main', mode='arm', architecture='ARMv4T',
            address=hex(start), bytes=size, targetSha256=review['nativeSpanSha256'], physicalFlow=flow_pin,
            base=base, binary='extract/arm7/runtime/arm7-main.bin', inputModuleSha256=hashlib.sha256(image).hexdigest()))
    from elftools.elf.elffile import ELFFile
    from elftools.elf.relocation import RelocationSection
    primary=proposal['actualPrimaryElf'];assert not primary['objectUsedAsImplementationInput']
    assert sha256(ROOT/primary['object']['path'])==primary['object']['sha256']
    with(ROOT/primary['object']['path']).open('rb')as stream:
        elf=ELFFile(stream);symbols=elf.get_section_by_name('.symtab');symbol=symbols.get_symbol_by_name(primary['function'])[0]
        assert symbol['st_info']['type']=='STT_FUNC'and symbol['st_size']==1716
        section=symbol['st_shndx'];offset=symbol['st_value']-elf.get_section(section)['sh_addr'];body=bytearray(elf.get_section(section).data()[offset:offset+1716])
        target=bytearray(image[0x027f3f40-base:0x027f3f40-base+1716]);relocations=[]
        for sec in elf.iter_sections():
            if not isinstance(sec,RelocationSection)or sec['sh_info']!=section:continue
            for relocation in sec.iter_relocations():
                position=relocation['r_offset']-offset
                if not 0<=position<1716:continue
                assert relocation['r_info_type']==1 and relocation['r_addend']==-8 and position%4==0
                word=struct.unpack_from('<I',target,position)[0];assert word>>24==0xeb
                displacement=word&0xffffff;displacement-=0x1000000 if displacement&0x800000 else 0
                destination=0x027f3f40+position+8+4*displacement
                record=next(r for r in primary['actualElfRelocations']if r['offset']==position)
                assert destination==int(record['nativeTarget'],0)and destination in functions and functions[destination]['mode']=='arm'
                assert functions[destination]['module']==record['targetModule']
                relocations.append(position);body[position:position+4]=bytes(4);target[position:position+4]=bytes(4)
        assert len(relocations)==len(set(relocations))==61 and body==target
        assert len(body)-4*len(relocations)==1472
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/arm7-wl-rxman-next'; source_root = 'src/arm7/parallel_wave20261106/wl-rxman-next'
    assert not folder.exists() and not (ROOT / source_root).exists() and not (ROOT / 'work/w6rxm').exists()
    assert not list(ROOT.glob('wave20261106_arm7_wl_rxman_source_*.py'))
    name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6rxm', helperPrefix='wave20261106_arm7_wl_rxman_source_', claimedFunctions=claimed,
        perFunctionSourceNamesRemainHypotheses=True, completePrimaryImplementationCAndGitBlobsVerified=True))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=name,
        claimSha256=sha256(ROOT / name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        functions=1, initializedCandidateBytes=1716, sourceRevision=revision,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), protectionPins=pins,
        independentOriginalEntryCfgAndEveryLiteralOriginWidthValue=reviews,
        noHistoricalOwnershipProjectionOrDataStorageCredit=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=1, initializedCandidateBytes=1716, sourceCredit=0))


if __name__ == '__main__':
    main()
