import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('seven_consumers', HERE / 'qualify_ten_consumers_v2.py')
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


class TenConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((HERE / 'ten-consumer-contract-v2.json').read_bytes())
        cls.original = worker.blob
        names = ['recovery.json', worker.LEDGER, *[c['report'] for c in cls.contract['consumers']]]
        cls.blobs = {name: worker.blob(name, worker.SOURCE) for name in names}
        registry = json.loads(cls.blobs['recovery.json'])['batches']
        selected = {c['report'] for c in cls.contract['consumers']}
        cls.batches = [b for b in registry if b['report'] in selected]
        cls.ledger = json.loads(cls.blobs[worker.LEDGER])

    def setUp(self):
        self.contract = copy.deepcopy(type(self).contract)
        self.actual = copy.deepcopy(self.batches)
        self.first = self.contract['consumers'][0]
        self.raw = self.blobs[self.first['report']]
        self.blob_patch = patch.object(worker, 'blob', side_effect=lambda name, revision='HEAD': self.blobs[name] if name in self.blobs else type(self).original(name, revision))
        self.blob_patch.start()
        self.addCleanup(self.blob_patch.stop)

    def qualifications(self):
        results = {}
        for c in self.contract['consumers']:
            r = c['row']
            inputs = dict(originalCodeCompilerInput=False, source=r['source'], sha256=r['sourceSha256'], includes=[dict(path=p['path'].replace('\\', '/'), sha256=p['sha256']) for p in r['sourceDependencies']])
            results[c['report']] = dict(closedInputs=dict(comparison=inputs), qualification=dict(report=c['report'], reportSha256=c['reportSha256'], producer=c['generator'], producerSha256=c['generatorSha256'], expectedRanges={r['address']: r['bytes']}, proofs=[dict(address=r['address'], sourceOnlyCompilerInput=dict())]))
        return results

    def altered_report(self, mutation, change_contract=False):
        report = json.loads(self.raw)
        mutation(report['matches'][0])
        raw = json.dumps(report).encode()
        c = copy.deepcopy(self.first)
        c['reportSha256'] = worker.digest(raw)
        if change_contract:
            c['row'] = report['matches'][0]
        return raw, c

    def test_all_ten_real_frozen_rows_and_baseline_objects_pass(self):
        for c in self.contract['consumers']:
            report, row = worker.validate_report(self.blobs[c['report']], c)
            result = worker.object_contract(worker.ROOT / row['object'], row)
            self.assertEqual(result['bytes'], row['bytes'])
            self.assertEqual(result['mapping']['mode'], 'arm')
            self.assertEqual('outputSha256' in row, c['report'] in worker.SOURCE1_REPORTS)

    def test_real_closed_headers_pass_without_mutating_raw_metadata(self):
        for c in self.contract['consumers']:
            row = c['row']
            before = copy.deepcopy(row)
            result = worker.closed_graph(row)
            self.assertEqual(row, before)
            self.assertEqual(len(result['graph']), 2)
            self.assertEqual('\\' in result['original']['includes'][0]['path'], c['report'] not in worker.SOURCE1_REPORTS)
            self.assertNotIn('\\', result['comparison']['includes'][0]['path'])

    def test_full_compiler_object_gate_rejects_a_different_actual_object(self):
        other = self.contract['consumers'][1]['row']
        with self.assertRaises(ValueError):
            worker.object_contract(worker.ROOT / other['object'], self.first['row'])

    def test_exact_projection_changes_only_seven_overlay_pins(self):
        before = copy.deepcopy(self.actual)
        result, removed = worker.project_batches(self.actual, self.contract)
        self.assertEqual(self.actual, before)
        self.assertEqual(len(removed), 10)
        self.assertEqual(sum(bool(r['removed']) for r in removed), 7)
        for a, b in zip(before, result):
            restored = copy.deepcopy(b)
            if worker.OV in a['sourceHashes']:
                restored['sourceHashes'][worker.OV] = worker.OV_SHA
            self.assertEqual(a, restored)
            self.assertEqual(b['sourceHashes'][worker.MAIN], worker.MAIN_SHA)

    def test_prior_main_projection_remains_missing_without_reintroduction(self):
        for b in self.actual:
            del b['sourceHashes'][worker.MAIN]
        result, removed = worker.project_batches(self.actual, self.contract)
        self.assertTrue(all(worker.MAIN not in b['sourceHashes'] for b in result))
        self.assertTrue(all(r['priorMainOmissionsPreserved'] == [worker.MAIN] for r in removed))

    def test_missing_extra_duplicate_or_changed_selected_batches_fail(self):
        cases = []
        x = copy.deepcopy(self.actual); x.pop(); cases.append(x)
        x = copy.deepcopy(self.actual); x.append(copy.deepcopy(x[0])); cases.append(x)
        x = copy.deepcopy(self.actual); x[0]['report'] = 'evidence/matches/unknown.json'; cases.append(x)
        x = copy.deepcopy(self.actual); x[0]['entries'] = []; cases.append(x)
        x = copy.deepcopy(self.actual); x.reverse(); cases.append(x)
        for x in cases:
            with self.subTest(case=cases.index(x)), self.assertRaises(ValueError):
                worker.project_batches(x, self.contract)

    def test_missing_extra_wrong_overlay_and_main_hashes_fail(self):
        cases = [lambda x: x.pop(worker.OV), lambda x: x.update({worker.OV: '0' * 64}), lambda x: x.update({worker.MAIN: '0' * 64}), lambda x: x.update({'extract/arm9_overlays/ov001.bin': '0' * 64})]
        for mutate in cases:
            actual = copy.deepcopy(self.actual)
            mutate(actual[3]['sourceHashes'])
            with self.assertRaises(ValueError):
                worker.project_batches(actual, self.contract)

    def test_unknown_reference_consumer_is_not_silently_passed(self):
        self.actual.append(dict(report='unknown.json', sourceHashes={worker.OV: worker.OV_SHA}))
        with self.assertRaises(ValueError):
            worker.project_batches(self.actual, self.contract)

    def test_unrelated_fields_and_historical_references_are_preserved(self):
        name, refs = next(iter(self.contract['historicalOverlayReferences'].items()))
        unrelated = dict(report=name, sourceHashes=refs.copy(), marker=dict(value=[1, 2]))
        self.actual.append(unrelated)
        result, removed = worker.project_batches(self.actual, self.contract)
        self.assertEqual(result[-1], unrelated)

    def test_full_namespace_and_extent_negatives_fail(self):
        for key, value in [('processor', 'arm7'), ('program', 'child'), ('module', 'ov000'), ('mode', 'thumb'), ('address', '0x2076444'), ('bytes', 196), ('compiledBytes', 196)]:
            raw, c = self.altered_report(lambda r: r.update({key: value}), True)
            with self.subTest(key=key), self.assertRaises(ValueError):
                worker.validate_report(raw, c)

    def test_changed_source_header_object_compiler_and_invented_output_fail(self):
        changes = [('source', 'src/other.c'), ('sourceSha256', '0' * 64), ('sourceDependencies', []), ('objectSha256', '0' * 64), ('compilerSha256', '0' * 64), ('compilerFlags', ['-O0']), ('outputSha256', '0' * 64)]
        for key, value in changes:
            raw, c = self.altered_report(lambda r: r.update({key: value}))
            with self.subTest(key=key), self.assertRaises(ValueError):
                worker.validate_report(raw, c)

    def test_missing_extra_report_rows_and_failed_acceptance_fail(self):
        for rows in [[], [self.first['row'], self.first['row']]]:
            r = json.loads(self.raw); r['matches'] = rows
            raw = json.dumps(r).encode(); c = copy.deepcopy(self.first); c['reportSha256'] = worker.digest(raw)
            with self.assertRaises(ValueError):
                worker.validate_report(raw, c)
        with self.assertRaises(ValueError):
            worker.validate_report(self.raw + b' ', self.first)
        for field, value in [('allPassed', False), ('romSha256', '0' * 64)]:
            r = json.loads(self.raw); r[field] = value
            raw = json.dumps(r).encode(); c = copy.deepcopy(self.first); c['reportSha256'] = worker.digest(raw)
            with self.assertRaises(ValueError):
                worker.validate_report(raw, c)

    def test_hidden_flags_and_noncanonical_paths_fail(self):
        for extra in [['-include', 'src/other.h'], ['-DOTHER'], ['@other.rsp'], ['-Ielsewhere'], ['-o', 'output.o']]:
            with self.assertRaises(ValueError):
                worker.validate_flags(self.first['row']['compilerFlags'] + extra)
        for name in ['src/../inputs/a.c', '../src/a.c', 'C:/outside/a.c', '/src/a.c', 'generated/a.c', 'src/a.bin']:
            with self.assertRaises(ValueError):
                worker.source_path(name)

    def test_comparison_views_preserve26_and_all_original_report_fields(self):
        q = self.qualifications(); before = copy.deepcopy(q)
        ledger, proofs, reports = worker.comparison_views(self.contract, q, self.ledger)
        self.assertEqual(q, before)
        self.assertEqual(len(ledger['consumers']), 36)
        self.assertEqual(ledger['consumers'][:26], self.ledger['consumers'])
        for c in self.contract['consumers']:
            r = copy.deepcopy(reports[c['report']]); annotation = r['matches'][0].pop('sourceOnlyCompilerInput')
            for target in c['producerMetadataAliases']:
                r.pop(target)
            self.assertEqual(r, json.loads(self.blobs[c['report']]))
            self.assertTrue(annotation['includes'][0]['path'].startswith('src/'))

    def test_changed_old_ledger_or_fresh_qualification_is_rejected(self):
        bad = copy.deepcopy(self.ledger); bad['consumers'].reverse()
        with self.assertRaises(ValueError):
            worker.comparison_views(self.contract, self.qualifications(), bad)
        for key in ['reportSha256', 'producerSha256', 'expectedRanges']:
            q = self.qualifications(); q[self.first['report']]['qualification'][key] = 'bad'
            with self.subTest(key=key), self.assertRaises(ValueError):
                worker.comparison_views(self.contract, q, self.ledger)

    def test_route_is_live_and_nested_projection_restores_on_exception(self):
        qualifications = self.qualifications()
        proof = dict(passed=True, functions=10, contractCanonicalSha256=worker.canonical(self.contract), qualifications=qualifications, helperSha256=worker.sha256(worker.__file__), inputHashes={})
        base = Mock(side_effect=lambda actual, report, declared: actual)
        with patch.object(worker.overlay, 'project_batches', base), patch.object(worker, 'live_qualify', return_value=proof) as live:
            previous_read, previous_qualify = worker.main_audit.read_json, worker.main_audit.qualify_report
            with self.assertRaisesRegex(RuntimeError, 'fixture'):
                with worker.route(self.contract, HERE / 'unused-test-output') as state:
                    current = worker.overlay.project_batches
                    actual = copy.deepcopy(self.actual)
                    for b in actual:
                        del b['sourceHashes'][worker.MAIN]
                    result = current(actual, {}, {})
                    self.assertNotIn(worker.OV, result[0]['sourceHashes'])
                    self.assertNotIn(worker.MAIN, result[0]['sourceHashes'])
                    ledger = worker.main_audit.read_json(worker.ROOT / worker.LEDGER)
                    self.assertEqual(len(ledger['consumers']), 36)
                    request = {self.first['row']['address']: self.first['row']['bytes']}
                    report = worker.main_audit.qualify_report(self.first['report'], request, HERE)
                    self.assertTrue(report['proofs'][0]['sourceOnlyCompilerInput']['includes'][0]['path'].startswith('src/'))
                    self.assertEqual(len(state['projectionEvents']), 1)
                    raise RuntimeError('fixture')
            self.assertIs(worker.overlay.project_batches, base)
            self.assertIs(worker.main_audit.read_json, previous_read)
            self.assertIs(worker.main_audit.qualify_report, previous_qualify)
            live.assert_called_once()
            base.assert_called_once()

    def test_failing_live_qualification_installs_no_hooks(self):
        original = worker.overlay.project_batches
        with patch.object(worker, 'live_qualify', side_effect=ValueError('failed live')):
            with self.assertRaises(ValueError):
                with worker.route(self.contract, HERE):
                    self.fail('entered failed route')
        self.assertIs(worker.overlay.project_batches, original)

    def test_nested_historical_projector_order_and_success_restoration(self):
        events = []
        proof = dict(passed=True, functions=10, contractCanonicalSha256=worker.canonical(self.contract), qualifications=self.qualifications(), helperSha256=worker.sha256(worker.__file__), inputHashes={})
        def original(actual, report, declared):
            events.append('legacy-after-seven')
            self.assertTrue(all(worker.OV not in b['sourceHashes'] and worker.MAIN not in b['sourceHashes'] for b in actual))
            return actual
        with patch.object(worker.overlay, 'project_batches', original), patch.object(worker, 'live_qualify', return_value=proof):
            with worker.route(self.contract, HERE / 'unused'):
                seven = worker.overlay.project_batches
                def historical(actual, report, declared):
                    events.append('historical-before-seven')
                    copied = copy.deepcopy(actual)
                    for batch in copied:
                        del batch['sourceHashes'][worker.MAIN]
                    return seven(copied, report, declared)
                with patch.object(worker.overlay, 'project_batches', historical):
                    worker.overlay.project_batches(self.actual, {}, {})
                self.assertIs(worker.overlay.project_batches, seven)
            self.assertIs(worker.overlay.project_batches, original)
        self.assertEqual(events, ['historical-before-seven', 'legacy-after-seven'])

    def test_actual_legacy_registry_gate_rejects_before_any_projection(self):
        def committed(name, revision=None):
            return {'batches': self.actual} if name == 'recovery.json' else {}
        with patch.object(worker.overlay, 'committed', side_effect=committed), patch.object(worker.overlay.subprocess, 'check_output', return_value=b'head\n'), patch.object(worker.overlay.subprocess, 'run'), patch.object(worker.overlay, 'project_batches') as projected:
            with self.assertRaisesRegex(ValueError, 'exact committed native registry'):
                worker.overlay.qualify([], HERE / 'unused')
            projected.assert_not_called()

    def test_contract_missing_extra_duplicate_or_reordered_consumers_fail(self):
        cases = []
        c = copy.deepcopy(self.contract); c['consumers'].pop(); cases.append(c)
        c = copy.deepcopy(self.contract); c['consumers'].append(c['consumers'][0]); cases.append(c)
        c = copy.deepcopy(self.contract); c['consumers'][1] = c['consumers'][0]; cases.append(c)
        c = copy.deepcopy(self.contract); c['consumers'].reverse(); cases.append(c)
        for c in cases:
            with self.assertRaises(ValueError):
                worker.validate_contract(c)

    def test_source1_producer_aliases_preserve_raw_and_have_exact_origin(self):
        for c in self.contract['consumers']:
            raw = json.loads(self.blobs[c['report']]); before = copy.deepcopy(raw)
            view, aliases = worker.producer_view(raw, c)
            self.assertEqual(raw, before)
            self.assertEqual(view['matches'], raw['matches'])
            if c['report'] in worker.SOURCE1_REPORTS:
                self.assertEqual(len(aliases), 2)
                self.assertEqual(view['generator'], raw['producer'])
                self.assertEqual(view['generatorSha256'], raw['producerSha256'])
                self.assertIn('outputSha256', view['matches'][0])
                for field in ('generator', 'generatorSha256'):
                    view.pop(field)
                self.assertEqual(view, raw)
            else:
                self.assertEqual(aliases, [])
                self.assertEqual(view, raw)

    def test_missing_wrong_ambiguous_or_conflicting_producer_is_rejected(self):
        c = self.contract['consumers'][0]; raw = json.loads(self.blobs[c['report']])
        mutations = [lambda r: r.pop('producer'), lambda r: r.pop('producerSha256'), lambda r: r.update(producer='wrong.py'), lambda r: r.update(producerSha256='0' * 64), lambda r: r.update(generator=c['generator']), lambda r: r.update(generatorSha256=c['generatorSha256']), lambda r: r.update(producer=['ambiguous'])]
        for mutate in mutations:
            candidate = copy.deepcopy(raw); mutate(candidate)
            with self.assertRaises(ValueError):
                worker.producer_view(candidate, c)
        candidate = copy.deepcopy(raw); candidate['matches'][0]['generator'] = 'invented.py'
        encoded = json.dumps(candidate).encode(); adapted = copy.deepcopy(c); adapted['reportSha256'] = worker.digest(encoded)
        with self.assertRaises(ValueError):
            worker.validate_report(encoded, adapted)

    def test_factory_yields_full_live_proof_and_detects_contract_mutation(self):
        proof = dict(passed=True, functions=10, bytes=2100, contractCanonicalSha256=worker.canonical(self.contract), qualifications=self.qualifications(), helperSha256=worker.sha256(worker.__file__), inputHashes={})
        previous = worker.overlay.project_batches
        with patch.object(worker, 'live_qualify', return_value=proof):
            with self.assertRaisesRegex(ValueError, 'Contract mutated'):
                with worker.route(self.contract, HERE / 'unused') as state:
                    self.assertEqual(state['liveQualification']['functions'], 10)
                    self.assertEqual(state['liveQualification']['bytes'], 2100)
                    self.assertEqual(state['contractCanonicalSha256'], worker.canonical(self.contract))
                    self.contract['functionBytes'] = 0
        self.assertIs(worker.overlay.project_batches, previous)

    def test_invented_output_field_is_rejected_for_exact_original_seven(self):
        for c in self.contract['consumers']:
            if c['report'] in worker.SOURCE1_REPORTS:
                continue
            report = json.loads(self.blobs[c['report']]); report['matches'][0]['outputSha256'] = report['matches'][0]['targetSha256']
            raw = json.dumps(report).encode(); changed = copy.deepcopy(c); changed['reportSha256'] = worker.digest(raw)
            with self.assertRaises(ValueError):
                worker.validate_report(raw, changed)

    def test_inventory_is_recomputed_and_missing_or_unknown_records_fail(self):
        audit = json.loads((worker.ROOT / self.contract['remainingMainConsumerInventory']['path']).read_bytes())
        baseline = json.loads(self.blobs['recovery.json'])['batches']
        worker.validate_inventory(self.contract, audit, baseline)
        missing = copy.deepcopy(audit); missing['rows'].pop()
        with self.assertRaises(ValueError):
            worker.validate_inventory(self.contract, missing, baseline)
        added = copy.deepcopy(baseline); added.append(dict(report='unknown-main.json', sourceHashes={worker.MAIN: worker.MAIN_SHA}))
        with self.assertRaises(ValueError):
            worker.validate_inventory(self.contract, audit, added)


if __name__ == '__main__':
    unittest.main(verbosity=2)
