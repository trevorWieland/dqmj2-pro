import copy
import sys
import unittest
import io
import tempfile
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import host_arm9_overlay_reference_v1_20261106 as proposal
import host_arm9_overlay_reference_policy_v1_20261106 as policy
from qualify_arm9_reference_consumer_v2_20261105 import compiler_inputs as legacy_main_inputs


class RouteControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = policy.load_contract()
        cls.first = cls.contracts['consumers'][0]
        cls.report = proposal.read_json(proposal.ROOT / cls.first['report'])

    def test_all_frozen_namespaces_and_closed_sources(self):
        count = 0
        for consumer in self.contracts['consumers']:
            report = proposal.read_json(proposal.ROOT / consumer['report'])
            rows = proposal.validate_report(report, consumer)
            for row in rows.values():
                value = proposal.compiler_inputs(row)
                self.assertFalse(value['originalCodeCompilerInput'])
                self.assertEqual(value['namespace'], list(proposal.identity(row)))
                with self.assertRaises(AssertionError):
                    legacy_main_inputs(row)
                count += 1
        self.assertEqual(count, 39)

    def test_each_actual_row_rejects_wrong_namespace_extent_source_and_compiler(self):
        changes = [('program', 'wrong-child'), ('processor', 'arm7'), ('module', 'main'), ('mode', 'thumb'),
            ('bytes', 4), ('sourceSha256', '0' * 64), ('targetSha256', '0' * 64),
            ('objectSha256', '0' * 64), ('compilerFlags', ['-O2', '@unapproved.rsp'])]
        for consumer in self.contracts['consumers']:
            report = proposal.read_json(proposal.ROOT / consumer['report'])
            for index in range(len(report['matches'])):
                for key, value in changes:
                    wrong = copy.deepcopy(report)
                    wrong['matches'][index][key] = value
                    with self.subTest(report=consumer['report'], index=index, field=key):
                        with self.assertRaises(ValueError):
                            proposal.validate_report(wrong, consumer)

    def test_missing_duplicate_extra_and_failed_report(self):
        for label in ['missing', 'duplicate', 'extra-namespace', 'failed', 'rom']:
            wrong = copy.deepcopy(self.report)
            if label == 'missing':
                wrong['matches'].pop()
            elif label in ['duplicate', 'extra-namespace']:
                extra = copy.deepcopy(wrong['matches'][0])
                if label == 'extra-namespace':
                    extra['module'] = 'ov003'
                wrong['matches'].append(extra)
            elif label == 'failed':
                wrong['allPassed'] = False
            else:
                wrong['romSha256'] = '0' * 64
            with self.subTest(label=label), self.assertRaises(ValueError):
                proposal.validate_report(wrong, self.first)

    def test_full_namespace_distinguishes_equal_addresses(self):
        one = dict(self.report['matches'][0])
        two = dict(one, module='ov006')
        self.assertEqual(len(proposal.identities([one, two])), 2)
        with self.assertRaises(ValueError):
            proposal.identities([one, one])

    def test_actual_two_overlay_packet_keeps_both_distinct_rows(self):
        consumer = next(item for item in self.contracts['consumers'] if 'overlay-strict-reuse' in item['report'])
        report = proposal.read_json(proposal.ROOT / consumer['report'])
        selected = proposal.validate_report(report, consumer)
        self.assertEqual({key[2] for key in selected}, {'ov003', 'ov006'})
        self.assertEqual(len({key[4] for key in selected}), 2)

    def test_closed_text_rejects_hidden_includes_binary_and_ambiguous_preprocessing(self):
        source = 'src/f/c.c'
        for text in ['#include <x.h>', '#include HEADER', '#include_next "c.h"', '#embed "x.bin"',
            '#define INCLUDE "x.h"', 'asm("mov r0,r0");', '.incbin "x.bin"',
            '#include ' + chr(92) + chr(10) + '"c.h"', '??=include "c.h"', '%:include "c.h"', '#include "../../x.h"']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                proposal.validate_texts({source: text, 'src/f/c.h': 'typedef int X;'}, source)
        with self.assertRaises(ValueError):
            proposal.validate_texts({source: 'int f(void);', 'src/f/c.h': 'typedef int X;'}, source)
        with self.assertRaises(ValueError):
            proposal.validate_texts({source: '#include "c.h"', 'src/f/c.h': '#include "c.h"'}, source)

    def test_hidden_compiler_inputs_and_languages_rejected(self):
        flags = self.report['matches'][0]['compilerFlags']
        for extra in ['@unapproved.rsp', '-includeX.h', '-prefixX.h', '-Iother', '-iother', '-DREALCODE=x',
            'extract/original.bin', 'inputs/game.nds', 'asm/original.s', 'unapproved.o', '-c', '-o']:
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                proposal.validate_flags(flags + [extra])
        wrong = list(flags)
        wrong[wrong.index('c99')] = 'c++'
        with self.assertRaises(ValueError):
            proposal.validate_flags(wrong)

    def batches(self):
        result = []
        for consumer in self.contracts['consumers']:
            pins = {item['path']: item['sha256'] for item in consumer['comparisonInputs']}
            for row in consumer['rows']:
                pins[row['source']] = row['sourceSha256']
                pins.update({header['path']: header['sha256'] for header in row['sourceDependencies']})
            result.append(dict(report=consumer['report'], sourceHashes=pins))
        result.append(dict(report='untouched-legacy', sourceHashes={'extract/arm9_overlays/ov000.bin': 'legacy', 'src/legacy.c': 'source'}))
        return result

    def test_projection_exact_roles_all_sources_and_unrelated_legacy_preserved(self):
        original = self.batches()
        baseline = copy.deepcopy(original)
        projected, removed = proposal._comparison_projection(original, self.contracts)
        self.assertEqual(original, baseline)
        self.assertEqual(len(removed), 29)
        self.assertEqual(projected[-1], original[-1])
        self.assertEqual(sum(len(batch['sourceHashes']) for batch in projected[:-1]), 78)

    def test_projection_rejects_unknown_changed_missing_and_duplicate_inputs(self):
        for label in ['unknown', 'changed', 'missing', 'duplicate']:
            wrong = self.batches()
            if label == 'duplicate':
                wrong.append(copy.deepcopy(wrong[0]))
            elif label == 'unknown':
                wrong[0]['sourceHashes']['extract/arm9_overlays/ov005.bin'] = 'unapproved'
            else:
                key = self.first['comparisonInputs'][0]['path']
                if label == 'changed':
                    wrong[0]['sourceHashes'][key] = 'wrong'
                else:
                    del wrong[0]['sourceHashes'][key]
            with self.subTest(label=label), self.assertRaises(ValueError):
                proposal._comparison_projection(wrong, self.contracts)

    def test_projection_after_registry_identity_and_before_legacy_projector(self):
        actual = self.batches()
        snapshot = copy.deepcopy(actual)
        def legacy_projector(batches):
            self.assertEqual(batches[-1], snapshot[-1])
            self.assertTrue(all(not any(name.startswith('extract/') for name in batch['sourceHashes']) for batch in batches[:-1]))
            return batches
        module = SimpleNamespace(project_batches=legacy_projector)
        def original_qualifier(batches):
            proposal.require(batches == snapshot, 'Original committed-registry identity changed')
            return module.project_batches(batches)
        previous = module.project_batches
        def proposed_projector(batches):
            projected, removed = proposal._comparison_projection(batches, self.contracts)
            return previous(projected)
        with patch.object(module, 'project_batches', proposed_projector):
            original_qualifier(actual)
            with self.assertRaises(ValueError):
                original_qualifier(proposal._comparison_projection(actual, self.contracts)[0])
        self.assertEqual(module.project_batches, previous)
        self.assertEqual(actual, snapshot)


class MutableRoleControls(unittest.TestCase):
    def setUp(self):
        base = HERE / 'work/goal-resume-20261106/overlay-reference-production-tests'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(base.resolve()))
        self.root_patch = patch.object(policy, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.root_patch.stop)
        self.baseline = dict(schemaVersion=1, sourceCredit=0, consumers=[dict(report='original-' + str(index)) for index in range(26)])
        self.put('recovery.json', {'current': 174})
        self.put('manifest.json', {'generated': 174})
        self.put('source-preferences.json', {'fixed': True})
        self.put('provenance/arm9-reference-only-consumers-20261101.json', self.baseline)
        self.put(policy.CONTRACT, {})
        self.put(policy.LEDGER, {})
        self.put('evidence/verification/host-arm9-overlay-reference-v1/tool.txt', 'historical-tool')
        pins = [dict(path=name, sha256='0' * 64, policy=role) for name, role in policy.MUTABLE.items()]
        pins += [dict(path='source-preferences.json', sha256=policy.sha256(self.root / 'source-preferences.json')),
            dict(path='work/historical-tool.py', archivePath='evidence/verification/host-arm9-overlay-reference-v1/tool.txt',
                sha256=policy.sha256(self.root / 'evidence/verification/host-arm9-overlay-reference-v1/tool.txt'))]
        self.contract = dict(scopePins=pins, productionFiles=[], historicalMainLedger=dict(
            path='provenance/arm9-reference-only-consumers-20261101.json', document=copy.deepcopy(self.baseline)))

    def put(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        proposal.write_json(path, value)

    def test_exact_three_mutable_roles_and_manifest_live_duration(self):
        snapshot = policy.scope_snapshot(self.contract, self.root / 'proof')
        policy.ensure_scope(snapshot)
        self.put('manifest.json', {'generated': 175})
        with self.assertRaises(ValueError):
            policy.ensure_scope(snapshot)
        wrong = copy.deepcopy(self.contract)
        wrong['scopePins'][3]['policy'] = 'generated-manifest-live-stable'
        with self.assertRaises(ValueError):
            policy.scope_roles(wrong)

    def test_source_preferences_remain_immutable(self):
        self.put('source-preferences.json', {'fixed': False})
        with self.assertRaises(ValueError):
            policy.scope_snapshot(self.contract, self.root / 'proof')

    def test_committed_recovery_and_inert_archive_use_exact_head_checks(self):
        checked = []
        def committed(name, revision):
            checked.append((name, revision))
            return policy.sha256(self.root / name)
        with patch.object(policy.subprocess, 'check_output', return_value='fixture-head\n'), patch.object(policy, 'committed_file', side_effect=committed):
            policy.scope_snapshot(self.contract, self.root / 'proof', committed=True)
        self.assertEqual(checked, [('recovery.json', 'fixture-head'), ('evidence/verification/host-arm9-overlay-reference-v1/tool.txt', 'fixture-head')])
        self.assertFalse((self.root / 'work/historical-tool.py').exists())
        with patch.object(policy.subprocess, 'check_output', return_value='fixture-head\n'), patch.object(policy, 'committed_file', side_effect=ValueError('Not exact HEAD')):
            with self.assertRaises(ValueError):
                policy.scope_snapshot(self.contract, self.root / 'proof', committed=True)

    def test_original26_records_cannot_change_move_or_disappear(self):
        for label in ['change', 'move', 'missing']:
            ledger = copy.deepcopy(self.baseline)
            if label == 'change':
                ledger['consumers'][0]['report'] = 'changed'
            elif label == 'move':
                ledger['consumers'][0], ledger['consumers'][1] = ledger['consumers'][1], ledger['consumers'][0]
            else:
                ledger['consumers'].pop()
            self.put(self.contract['historicalMainLedger']['path'], ledger)
            with self.subTest(label=label), self.assertRaises(ValueError):
                policy.validate_main_ledger(self.contract, self.root / 'proof')

    def append_fixture(self):
        producer = 'qualified_main.py'
        receipt_name = 'evidence/verification/cohort174-arm9-reference-packets-v2-20261105.json'
        for name in [producer, 'src/main.c', 'work/original.o', 'tools/compiler.exe', 'qualify_arm9_reference_packets_v2_20261105.py']:
            self.put(name, 'inert-unit-fixture')
        digest = lambda name: policy.sha256(self.root / name)
        row = dict(source='src/main.c', sourceSha256=digest('src/main.c'), object='work/original.o', objectSha256=digest('work/original.o'),
            compiler='tools/compiler.exe', compilerSha256=digest('tools/compiler.exe'), sourceDependencies=[])
        report_name = 'evidence/matches/qualified-main.json'
        self.put(report_name, dict(matches=[row]))
        consumer = dict(report=report_name, producer=producer, producerSha256=digest(producer), program='', processor='arm9', module='main', mode='arm',
            expectedRanges={'0x2000000': 4}, sourceOnlyCompilerInputQualification=receipt_name)
        self.put(receipt_name, dict(passed=True, registered=True, generatorSha256=digest('qualify_arm9_reference_packets_v2_20261105.py'),
            qualification=[dict(report=report_name, reportSha256=digest(report_name), expectedRanges=consumer['expectedRanges'], producer=producer, producerSha256=digest(producer))]))
        self.put(self.contract['historicalMainLedger']['path'], dict(self.baseline, consumers=[*self.baseline['consumers'], consumer]))
        return consumer, receipt_name

    def test_main_append_reruns_the_unchanged_qualifier(self):
        consumer, receipt_name = self.append_fixture()
        with patch.object(policy, 'qualify_main', return_value=dict(producerSha256=consumer['producerSha256'], freshSourceOnlyCompilerBoundaryProven=True)) as qualified:
            proof = policy.validate_main_ledger(self.contract, self.root / 'proof')
        self.assertEqual(len(proof['proofs']), 1)
        qualified.assert_called_once_with(consumer['report'], consumer['expectedRanges'], self.root / 'proof/0')
        self.assertIn(receipt_name, proof['files'])
        self.assertIn('src/main.c', proof['files'])

    def test_append_overlay_or_boolean_receipt_cannot_authorize(self):
        consumer, receipt_name = self.append_fixture()
        ledger = proposal.read_json(self.root / self.contract['historicalMainLedger']['path'])
        ledger['consumers'][-1]['module'] = 'ov000'
        self.put(self.contract['historicalMainLedger']['path'], ledger)
        with patch.object(policy, 'qualify_main') as qualified, self.assertRaises(ValueError):
            policy.validate_main_ledger(self.contract, self.root / 'proof')
        qualified.assert_not_called()
        consumer, receipt_name = self.append_fixture()
        self.put(receipt_name, dict(passed=True, registered=True, generatorSha256=policy.sha256(self.root / 'qualify_arm9_reference_packets_v2_20261105.py'), qualification=[]))
        with patch.object(policy, 'qualify_main') as qualified, self.assertRaises(ValueError):
            policy.validate_main_ledger(self.contract, self.root / 'proof')
        qualified.assert_not_called()


class ActualNestedFactoryControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = policy.load_contract()

    def nested(self, failure=None):
        import host_arm9_overlay_reference_context_v1_20261106 as context
        import game_overlay_reference_route_v1_20261106 as game
        import itcm_reset_source_audit_route_v1_20261106 as itcm
        overlay, audit = game.overlay, itcm.audit
        actual = RouteControls.batches(self)
        actual += [dict(report=game.REPORT, sourceHashes={overlay.REFERENCE: overlay.REFERENCE_SHA, 'src/game.c': 'game'}),
            dict(report=itcm.REPORT, sourceHashes={itcm.IMAGE: 'main-original', itcm.ITCM: 'itcm-original', 'src/itcm.c': 'itcm'})]
        if failure == 'unknown-reference':
            actual[0]['sourceHashes']['extract/arm9_overlays/ov005.bin'] = 'unqualified'
        snapshot, events = copy.deepcopy(actual), []
        old_overlay, old_audit = overlay.project_batches, audit.qualify_overlay
        def terminal(batches, report, declared):
            events.append('terminal')
            self.assertEqual(batches[14], snapshot[14])
            for batch in [*batches[:14], *batches[15:]]:
                self.assertFalse(any(name.startswith('extract/') for name in batch['sourceHashes']))
            if failure == 'legacy-exception':
                raise RuntimeError('Deliberate final legacy projector failure')
            return batches, dict(legacy=True)
        def registry_gate(batches, directory):
            self.assertEqual(batches, snapshot)
            events.append('registry-gate')
            return overlay.project_batches(batches, {}, {})
        def live(contract, directory, committed):
            self.assertTrue(committed)
            events.append('live39-qualification')
            return dict(liveScope={'fixture': True})
        def projection(batches, contract):
            events.append('new-projection')
            return proposal._comparison_projection(batches, contract)
        try:
            with (patch.object(overlay, 'project_batches', terminal), patch.object(audit, 'qualify_overlay', registry_gate),
                    patch.object(context, 'load_contract', return_value=self.contracts), patch.object(context, 'verify_committed_promotion'),
                    patch.object(context, 'qualify', side_effect=live) as qualified, patch.object(context, 'ensure_scope'),
                    patch.object(context, '_comparison_projection', side_effect=projection), patch.object(game, 'qualify', return_value={'fixture': True}),
                    patch.object(game, 'contract'), patch.object(itcm, 'qualify', return_value=dict(originalDerivedNativeInputs={itcm.IMAGE: 'main-original', itcm.ITCM: 'itcm-original'}))):
                try:
                    with context.validation_route() as proof, game.route(), itcm.route():
                        audit.qualify_overlay(actual, HERE / 'work/unused-fixture-output')
                finally:
                    self.assertIs(overlay.project_batches, terminal)
                    self.assertIs(audit.qualify_overlay, registry_gate)
                    self.assertEqual(actual, snapshot)
                    qualified.assert_called_once()
        finally:
            self.assertIs(overlay.project_batches, old_overlay)
            self.assertIs(audit.qualify_overlay, old_audit)
        self.assertLess(events.index('live39-qualification'), events.index('registry-gate'))
        self.assertLess(events.index('registry-gate'), events.index('new-projection'))
        return events

    def test_real_nested_context_factories_order_and_restore(self):
        self.assertIn('terminal', self.nested())

    def test_unknown_reference_fails_inside_real_nested_factories(self):
        with self.assertRaises(ValueError):
            self.nested('unknown-reference')

    def test_legacy_exception_restores_all_real_nested_factories(self):
        with self.assertRaises(RuntimeError):
            self.nested('legacy-exception')

    def test_no_receipt_boolean_route_argument(self):
        import host_arm9_overlay_reference_context_v1_20261106 as context
        with self.assertRaises(TypeError):
            with context.validation_route({'passed': True}):
                self.fail('A receipt Boolean authorized a projection')


def main():
    controls = '--write-controls' in sys.argv
    if controls:
        sys.argv.remove('--write-controls')
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    transcript = io.StringIO()
    result = unittest.TextTestRunner(stream=transcript, verbosity=2).run(suite)
    print(transcript.getvalue(), end='')
    if not result.wasSuccessful():
        raise SystemExit(1)
    if controls:
        contract = policy.load_contract()
        directory = HERE / 'work/integration/host-arm9-overlay-reference-v1' / ('controls-' + uuid.uuid4().hex[:12])
        fresh = proposal.qualify(contract, directory, committed=False)
        names = [*contract['productionFiles'], policy.CONTRACT, policy.LEDGER, *[pin['archivePath'] for pin in contract['historicalPrototypeArchives']]]
        document = dict(passed=True, sourceCredit=0, globalCommittedGatesRun=False, testsPassed=result.testsRun,
            contract=dict(path=policy.CONTRACT, sha256=policy.CONTRACT_SHA), freshNativeOverlayFunctions=fresh['functions'],
            focusedFreshQualification=fresh, fixtureTestsAreSeparateFromCommittedGlobalAudits=True,
            actualNestedLegacyFactoriesExercisedWithIsolatedFixtures=True, testTranscript=transcript.getvalue(),
            files=[dict(path=name, sha256=policy.sha256(HERE / name)) for name in names])
        proposal.write_json(HERE / policy.CONTROLS, document)
        print(dict(controls=policy.CONTROLS, testsPassed=result.testsRun, freshOverlayFunctions=fresh['functions'], activated=False))


if __name__ == '__main__':
    main()


