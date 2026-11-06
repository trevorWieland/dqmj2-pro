import copy
from unittest.mock import patch
from project import ROOT, read_json, sha256, write_json
import publish_arm7_host02_bindings_20261030 as publication
import validate_arm7_bulk_20261030_host02 as legacy

ORIGINAL_VALIDATE = legacy.validate_document
SOURCE = 'publish_arm7_host02_bindings_20261030.py'


def validate(report):
    source = {'path': SOURCE, 'sha256': sha256(ROOT / SOURCE)}
    if report['generatorSources'].count(source) != 1:
        raise ValueError('Binding publication source missing or changed')
    expected = publication.qualified_bindings(report)
    if report.get('nativeSymbols') != {x['symbol']: x['address'] for x in expected} or report.get('nativeSymbolEntries') != expected:
        raise ValueError('Published module binding differs from qualified native relocation')
    if report.get('bindingPublication') != {**source, 'freshSourceRebuildRequired': True,
            'unchangedRelocationAddends': True, 'newCodeOrDataCredit': 0}:
        raise ValueError('Binding publication provenance or credit differs')
    projected = {**report, 'generatorSources': [x for x in report['generatorSources'] if x != source]}
    return ORIGINAL_VALIDATE(projected)


def main():
    baseline = read_json(publication.REPORT)
    validate(baseline)
    with patch.object(legacy, 'validate_document', validate):
        legacy.main()
    mutations = [
        ('missing-module-map', lambda r: r.pop('nativeSymbols')),
        ('shifted-module-map', lambda r: r['nativeSymbols'].update(native_host_arm7_data_03806fa9='0x03807028')),
        ('wrong-binding-namespace', lambda r: r['nativeSymbolEntries'][0].update(processor='arm9')),
        ('function-binding-fiction', lambda r: r['nativeSymbolEntries'][0].update(kind='function')),
        ('omitted-publication-source', lambda r: r.update(generatorSources=[x for x in r['generatorSources'] if x['path'] != SOURCE])),
        ('changed-publication-source', lambda r: next(x for x in r['generatorSources'] if x['path'] == SOURCE).update(sha256='0' * 64)),
        ('source-credit-for-binding', lambda r: r['bindingPublication'].update(newCodeOrDataCredit=160)),
        ('changed-unchanged-addend', lambda r: r['matches'][1]['relocations'][0].update(explicitAddend=0))]
    controls = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        try:
            validate(candidate)
        except (ValueError, KeyError, AssertionError) as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise AssertionError('Invalid ARM7 publication accepted: ' + name)
    legacy_path = 'evidence/verification/arm7-bulk-host02-controls-20261030.json'
    result = {'passed': True, 'controls': controls,
              'legacyControlsReplayed': len(read_json(ROOT / legacy_path)['negativeControls']),
              'legacyProof': {'path': legacy_path, 'sha256': sha256(ROOT / legacy_path)},
              'generator': 'verify_arm7_host02_publication_20261030.py',
              'generatorSha256': sha256(__file__), 'sourceByteCredit': 0,
              'canonicalReportSha256': sha256(publication.REPORT)}
    write_json(ROOT / 'evidence/verification/arm7-host02-publication-controls-20261030.json', result)
    print({'passed': True, 'publicationControls': len(controls), 'legacyControls': result['legacyControlsReplayed']})


if __name__ == '__main__':
    main()
