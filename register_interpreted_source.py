import argparse
from pathlib import Path
import interpreted_sources
from project import ROOT, configuration, now, read_json, sha256, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report')
    parser.add_argument('reproduce', nargs='+')
    args = parser.parse_args()
    path = interpreted_sources.local(args.report)
    report = read_json(path)
    relative = path.relative_to(ROOT).as_posix()
    if report.get('evidenceClass') == 'ordinary-C-complete-shared-module-primary-configuration-SCR-source-match':
        from interpreted_runtime_configuration_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-native-record-capacity-decision-SCR-source-match':
        from interpreted_record_capacity_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-primary-conditional-byte-mode-SCR-source-match':
        from interpreted_byte_modes_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-native-byte-row-configuration-SCR-source-match':
        from interpreted_byte_rows_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-registered-dynamic-primary-float-return-SCR-source-match':
        from interpreted_registered_flags_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-module-global-float-initializer-SCR-source-match':
        from interpreted_registered_initializer_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-numeric-primary-context-word-SCR-source-match':
        from interpreted_context_words_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-runtime-primary-flag-loop-SCR-source-match':
        from interpreted_runtime_loop_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-formal-primary24-set-clear-SCR-source-match':
        from interpreted_primary_pair_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-bounded-random-early-return-SCR-source-match':
        from interpreted_bounded_selection_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-reset-caller-with-source-linked-SCR-callees':
        from interpreted_reset_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-world-state-progression-reset-SCR-match':
        from interpreted_world_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-entry129-typed-script-call-SCR-match':
        from interpreted_entry_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-nested-primary24-SCR-match':
        from interpreted_primary_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif report.get('evidenceClass') == 'ordinary-C-complete-nested-numeric-state-transition-SCR-match':
        from interpreted_numeric_sources import candidates
        additions = candidates(report, relative, args.reproduce)
    elif 'modules' in report:
        if report['evidenceClass'] == 'ordinary-C-fixed-slot-input-capture-SCR-source-matches':
            from interpreted_capture_sources import candidates
        elif report['evidenceClass'] == 'reused-empty-C-family-source-rebuild-and-native-execution':
            from interpreted_empty_sources import candidates
        elif report['evidenceClass'] == 'ordinary-C-runtime-Boolean-SCR-decision-source-match':
            from interpreted_decision_sources import candidates
        else:
            from interpreted_linked_sources import candidates
        additions = candidates(report, path.relative_to(ROOT).as_posix(), args.reproduce)
    else:
        hashes = {row['path']: row['sha256'] for row in report['sourceClosure']
                  if Path(row['path']).suffix.lower() in ('.c', '.h', '.inc', '.py')}
        if sha256(ROOT / report['generator']) != report['generatorSha256']:
            raise ValueError('Interpreted source replay generator changed')
        hashes[report['generator']] = report['generatorSha256']
        region = report['matchedRange']
        batch = {'report': path.relative_to(ROOT).as_posix(), 'reproduce': args.reproduce,
                 'identity': {'scriptSha256': report['inputScriptSha256'], 'codeSha256': report['inputCodeSha256'],
                              'entryTableSha256': report['entryTableSha256']},
                 'range': {'entrySlots': report['boundaries']['entrySlots'], **region}, 'sourceHashes': hashes}
        additions = [batch]
    target = interpreted_sources.REGISTRY
    registry = read_json(target) if target.is_file() else {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'batches': []}
    previous = [row for row in registry['batches'] if row['report'] == relative]
    if previous and previous != additions:
        raise ValueError('Accepted interpreted source changed; an explicit migration is required')
    registry['batches'] = [row for row in registry['batches'] if row['report'] != relative] + additions
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    units, unavailable = interpreted_sources.measure(inventory, registry)
    if unavailable:
        raise ValueError('Interpreted source has not been freshly rebuilt: ' + repr(unavailable))
    write_json(target, registry)
    print({'sourceUnits': len(units), 'sourceBytes': sum(unit['sourceByteCredit'] for unit in units),
           'completeImages': 0, 'nativeSourceByteCredit': 0})


if __name__ == '__main__':
    main()
