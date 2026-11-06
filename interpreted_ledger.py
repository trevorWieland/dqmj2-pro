import json
from project import ROOT, configuration, read_json, sha256, write_text


REPORT = ROOT / 'evidence/encounter/scripts-inventory-20261029.json'


def measure(write=True):
    unavailable = {'inventoryAvailable': False, 'ordinarySourceCredit': 0,
                   'overallGameCompletionPercentage': None,
                   'nativeInitializedModuleCoverageIncludesScripts': False}
    if not REPORT.is_file():
        return unavailable
    inventory = read_json(REPORT)
    if inventory['romSha256'] != configuration()['romSha256']:
        raise ValueError('Interpreted inventory belongs to a different measured ROM')
    dependencies = inventory['dependencies'] + [{'path': inventory['generator'], 'sha256': inventory['generatorSha256']}]
    identities = dependencies + [row['cfg'] for row in inventory['images']]
    if any(not (ROOT / row['path']).is_file() or sha256(ROOT / row['path']) != row['sha256'] for row in identities):
        return {**unavailable, 'inventoryEvidenceStale': True}
    totals = inventory['totals']
    if inventory['containerValidationFailures']:
        raise ValueError('Interpreted container/hash inventory has unresolved failures')
    if len(inventory['images']) != totals['uniqueDecodedScriptImages']:
        raise ValueError('Interpreted image identities disagree with the measured totals')
    if len({image['codeSha256'] for image in inventory['images']}) != totals['uniqueCodeHashes']:
        raise ValueError('Interpreted content aliases were counted as unique programs')
    import interpreted_sources
    source_units, unavailable_sources = interpreted_sources.measure(inventory)
    empty_definition = 'c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d/before_primary_flag_reset'
    empty_units = [unit for unit in source_units if unit['sourceDefinitionId'] == empty_definition]
    copy_units = [unit for unit in source_units if unit.get('copyOnly')]
    other_units = [unit for unit in source_units if unit['sourceDefinitionId'] != empty_definition and not unit.get('copyOnly')]
    rows = []
    for image in inventory['images']:
        if image['ordinaryScriptSourceUnitsRecovered'] or image['ordinaryScriptSourceBytesRecovered']:
            raise ValueError('Interpreted source credit requires a separately accepted source build')
        owned = [unit for unit in source_units if unit['codeSha256'] == image['codeSha256']]
        source_bytes = sum(unit['sourceByteCredit'] for unit in owned)
        rows.append({'id': inventory['romSha256'] + '/scr/' + image['codeSha256'],
                     'buildSha256': inventory['romSha256'], 'executionKind': 'interpreted-SCR-on-ARM9',
                     'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
                     'decodedBytes': image['decodedBytes'], 'codeContainerBytes': image['codeBytes'],
                     'entryTableSha256': image['entryTableSha256'], 'members': image['members'],
                     'cfg': image['cfg'], 'opaqueSysNodes': image['opaqueSysNodeCount'],
                     'unresolvedCfgFailures': image['unresolvedCfgFailureCount'],
                     'uncoveredContainerBytes': image['uncoveredContainerBytes'],
                     'completeControlFlowCoverageCertified': image['completeControlFlowCoverageCertified'],
                     'states': {'inventoried': True, 'partialCfgAnalyzed': True, 'draftedOrdinarySource': bool(owned),
                                'sourceCompiled': bool(owned), 'sourceMatched': False,
                                'partialSourceMatched': bool(owned), 'wholeRomMatchedFromSource': False},
                     'sourceUnits': owned, 'ordinarySourceByteCredit': source_bytes,
                     'ordinarySourceUnitCredit': len(owned), 'completeImageCredit': 0})
    if sum(row['codeContainerBytes'] for row in rows) != totals['uniqueCodeContainerBytes']:
        raise ValueError('Unique interpreted code-container byte totals differ')
    if write:
        write_text(ROOT / 'ledger/interpreted-programs.jsonl', ''.join(json.dumps(row, separators=(',', ':')) + '\n' for row in rows))
    return {'inventoryAvailable': True, 'evidence': REPORT.relative_to(ROOT).as_posix(),
            'evidenceSha256': sha256(REPORT), 'scriptArchives': totals['primaryScriptArchives'],
            'memberTableIdentities': totals['allMemberTableIdentities'], 'uniqueImages': len(rows),
            'uniqueCodeContainerBytes': totals['uniqueCodeContainerBytes'],
            'opaqueSysNodes': totals['opaqueSysNodesPerUniqueImage'],
            'unresolvedCfgFailures': totals['unresolvedCfgFailures'],
            'uncoveredContainerBytes': totals['uncoveredContainerBytesPerUniqueImage'],
            'ordinarySourceUnitsRecovered': len(source_units),
            'authoredSourceDefinitionsRecovered': len({unit['sourceDefinitionId'] for unit in source_units}),
            'emptyRoutineInstances': len(empty_units),
            'emptyRoutineSourceBytes': sum(unit['sourceByteCredit'] for unit in empty_units),
            'nonemptyRoutineInstances': len(source_units) - len(empty_units),
            'nonemptyRoutineSourceBytes': sum(unit['sourceByteCredit'] for unit in source_units) - sum(unit['sourceByteCredit'] for unit in empty_units),
            'copyOnlyRoutineInstances': len(copy_units),
            'copyOnlyRoutineSourceBytes': sum(unit['sourceByteCredit'] for unit in copy_units),
            'nonemptyNoncopyRoutineInstances': len(other_units),
            'nonemptyNoncopyRoutineSourceBytes': sum(unit['sourceByteCredit'] for unit in other_units),
            'ordinarySourceBytesRecovered': sum(unit['sourceByteCredit'] for unit in source_units),
            'ordinarySourceCredit': sum(unit['sourceByteCredit'] for unit in source_units),
            'imagesWithPartialSource': sum(bool(row['sourceUnits']) for row in rows),
            'completeImagesRecovered': 0, 'sourceEvidenceUnavailable': unavailable_sources,
            'overallGameCompletionPercentage': None,
            'nativeInitializedModuleCoverageIncludesScripts': False,
            'limitations': ['Code-container bytes include interpreted records/data and are not an executable-only denominator',
                            'SYS effects/variable layouts and one code-end jump remain unresolved',
                            'Generated partial CFGs, duplicate members and native VM matches provide no ordinary script-source credit']}
