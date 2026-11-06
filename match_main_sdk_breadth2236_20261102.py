import shutil
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder

WORK = ROOT / 'work/main-sdk-breadth2236-matching-20261102'
REPORT = ROOT / 'evidence/matches/main-sdk-breadth2236-20261102.json'
CAMPAIGN = ROOT / 'evidence/attempts/main-sdk-remaining-breadth-20261102.json'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, _ = measured_module('main')
    assert metadata['sha256'] == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK = WORK
    rows = []
    for candidate in read_json(CAMPAIGN)['results']:
        if not candidate['genuineExact']: continue
        original = ROOT / candidate['source']
        assert sha256(original) == candidate['sourceSha256']
        source = ROOT / 'src/runtime/20261102_sdk_breadth2236' / original.name
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists(): assert source.read_bytes() == original.read_bytes()
        else: shutil.copyfile(original, source)
        text = source.read_text(encoding='utf-8')
        assert len(text.splitlines()) <= 500
        assert not any(t in text for t in ['/*', '//', 'asm ', '__asm', 'va_list', 'J2pUnknown'])
        row, proof, body = builder.build(source, source.stem, True)
        assert len(body) == candidate['identity']['bytes']
        row.update(sourceLanguage='C', exactBytes=len(body), sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, genuineLinkComparison=freeze_link(proof),
            ordinaryLogicSource=True, nativeBehavioralReturns=0,
            evidenceClass='Complete ordinary C compiler and genuine linked-byte comparison; semantics unqualified')
        rows.append(row)
    assert len(rows) == 12 and sum(r['bytes'] for r in rows) == 2236
    write_json(REPORT, dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=rows, matchedFunctions=len(rows), matchedBytes=sum(r['bytes'] for r in rows),
        actualNativeFunctionReturns=0, inferredGameplaySemantics=False,
        sourceOrigin=dict(referenceCampaign=CAMPAIGN.relative_to(ROOT).as_posix(), referenceCampaignSha256=sha256(CAMPAIGN),
            publicReferenceRevision='d636fb5d2b212e8736f09859fff447be2bd0ac85', gameSdkRevisionEstablished=False,
            typedAddressQualifiedFunctionsAndData=True, explicit32BitWordTypes=True,
            generatedDisassemblyOrEncodedExecutableInput=False),
        reproductionCommand='python match_main_sdk_breadth2236_20261102.py',
        limitations=[
            'Byte matching covers complete compiled caller spans and declared relocations; it supplies no native execution or gameplay-semantic evidence',
            'Original callees, hardware state and data bindings retain zero additional source credit',
            'Compiler and flags are recorded per unit; prior checksum configurations are not generalized',
            'Interface/boundary audit, module acceptance and whole-ROM regression remain separate gates',
            'No complete Windows/Android game, rendered scene, source-only ROM or ordinary caller reachability claim']))
    print(dict(genuineOrdinaryCFunctions=len(rows), genuineInitializedBytes=sum(r['bytes'] for r in rows),
        actualNativeFunctionReturns=0, moduleAcceptancePending=True))


if __name__ == '__main__':
    main()
