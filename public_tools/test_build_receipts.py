import copy
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from build_receipts import DENOMINATOR, REPORTS, digest, receipt_check, validate_build_receipt


class BuildReceiptTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / 'work/build-receipt-tests'
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.revision = 'a' * 40
        self.clock = time.time_ns()
        self.started = self.clock - 20_000_000_000
        self.native_started = self.clock - 10_000_000_000
        manifest = self.root / 'public/accepted-functions.json'
        self.write(manifest, dict(revision='closed-172', acceptedFunctions=11482))
        self.manifest_hash = digest(manifest)
        self.compilation = self.root / 'build/public-source-compile/report.json'
        self.write(self.compilation, dict(status='source-compilation-passed', fullManifestCompiled=True,
                   manifestSha256=self.manifest_hash, results=[]), self.clock - 15_000_000_000)
        self.native_parent = self.root / 'work/native-unique'
        self.native_path = self.native_parent / 'native-build-receipt.json'
        self.outer_path = self.root / 'build/B2JJ-modified/build-receipt.json'
        reports = {}
        for name in REPORTS:
            path = self.native_parent / 'evidence/linking' / name
            self.write(path, dict(genuinelyLinked=True, report=name), self.clock - 8_000_000_000)
            pin = self.pin(path)
            reports[pin.pop('path')] = pin
            frozen = self.root / 'evidence/linking' / name
            self.write(frozen, dict(historicalOnly=True, report=name), self.clock - 30_000_000_000)
        compile_pin = self.pin(self.compilation)
        self.native = dict(schemaVersion=1, buildPassed=True, nativeBuildPassed=True,
            publicGitRevision=self.revision, acceptedManifestSha256=self.manifest_hash,
            startedTimeNs=self.native_started, finishedTimeNs=self.clock - 5_000_000_000,
            moduleCount=20, initializedBytes=DENOMINATOR, acceptedFunctionsLinked=11482,
            allModuleBytesExact=True, allSymbolChecksPassed=True, frozenInputsUnchanged=True,
            behavioralReplayPerformed=False, fullContainerBuildPerformed=False,
            freshCompilationTimeBound=True, compilationNotBeforeTimeNs=self.started,
            publicSourceCompileReport=compile_pin, reports=reports, importedLinkageSourceCredit=0)
        self.outer = dict(schemaVersion=1, buildPassed=True, buildScope='native-modules',
            publicGitRevision=self.revision, acceptedManifestSha256=self.manifest_hash,
            startedTimeNs=self.started, nativeStartedTimeNs=self.native_started,
            publicSourceCompileReport=copy.deepcopy(compile_pin), reports=copy.deepcopy(reports))
        self.persist()

    def write(self, path, value, modified=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + '\n', encoding='utf-8')
        if modified is not None:
            os.utime(path, ns=(modified, modified))

    def pin(self, path):
        return dict(path=path.relative_to(self.root).as_posix(), sha256=digest(path),
                    modifiedTimeNs=path.stat().st_mtime_ns)

    def persist(self, native_modified=None):
        self.write(self.native_path, self.native, native_modified or self.clock - 4_000_000_000)
        self.outer['nativeBuildReceipt'] = self.pin(self.native_path)
        self.write(self.outer_path, self.outer)

    def validate(self, **options):
        with patch('build_receipts.subprocess.check_output', return_value=self.revision + '\n'), patch.dict(os.environ, {'GITHUB_SHA': self.revision}):
            return validate_build_receipt(self.root, self.root, self.outer_path, self.manifest_hash, **options)

    def rebind_function_count(self, count, linked):
        manifest = self.root / 'public/accepted-functions.json'
        self.write(manifest, dict(revision='closed-next', acceptedFunctions=count))
        self.manifest_hash = digest(manifest)
        compiled = json.loads(self.compilation.read_text())
        compiled['manifestSha256'] = self.manifest_hash
        self.write(self.compilation, compiled, self.clock - 15_000_000_000)
        for record in (self.native, self.outer):
            record['acceptedManifestSha256'] = self.manifest_hash
            record['publicSourceCompileReport'] = self.pin(self.compilation)
        self.native['acceptedFunctionsLinked'] = linked
        self.persist()

    def test_current_closed_manifest_function_count_is_required(self):
        self.rebind_function_count(11546, 11546)
        self.assertEqual(self.validate()['nativeReceipt']['acceptedFunctionsLinked'], 11546)

    def test_previous_checkpoint_count_cannot_satisfy_new_manifest(self):
        self.rebind_function_count(11546, 11482)
        with self.assertRaisesRegex(ValueError, 'complete closed module/function scope'):
            self.validate()

    def test_missing_closed_count_is_rejected(self):
        self.rebind_function_count(None, 11482)
        with self.assertRaisesRegex(ValueError, 'lacks its closed function count'):
            self.validate()

    def test_changed_manifest_bytes_cannot_reuse_a_native_receipt(self):
        self.write(self.root / 'public/accepted-functions.json', dict(acceptedFunctions=11546))
        with self.assertRaisesRegex(ValueError, 'manifest changed'):
            self.validate()

    def test_native_reports_route_only_to_new_verified_paths(self):
        result = self.validate()
        self.assertEqual(result['buildScope'], 'native-modules')
        self.assertEqual(result['compilation'], self.compilation)
        self.assertEqual(set(result['reports']), set(REPORTS))
        for path in result['reports'].values():
            self.assertEqual(path.parent, self.native_parent / 'evidence/linking')
            self.assertTrue(json.loads(path.read_text())['genuinelyLinked'])

    def test_receipt_check_remains_a_revision_reexport(self):
        with patch('build_receipts.subprocess.check_output', return_value=self.revision + '\n'), patch.dict(os.environ, {'GITHUB_SHA': self.revision}):
            self.assertEqual(receipt_check(self.root, self.root, self.outer_path, self.manifest_hash), self.revision)

    def test_stale_compilation_cannot_be_reauthorized_by_new_pins(self):
        old = self.started - 1_000_000_000
        os.utime(self.compilation, ns=(old, old))
        self.outer['publicSourceCompileReport'] = self.pin(self.compilation)
        self.native['publicSourceCompileReport'] = self.pin(self.compilation)
        self.persist()
        with self.assertRaisesRegex(ValueError, 'Source compilation report is stale'):
            self.validate()

    def test_failed_or_partial_compilation_cannot_publish(self):
        for changes in (dict(status='source-compilation-failed'), dict(fullManifestCompiled=False), dict(manifestSha256='b' * 64)):
            with self.subTest(changes=changes):
                value = dict(status='source-compilation-passed', fullManifestCompiled=True, manifestSha256=self.manifest_hash)
                value.update(changes)
                self.write(self.compilation, value, self.clock - 15_000_000_000)
                self.outer['publicSourceCompileReport'] = self.pin(self.compilation)
                self.native['publicSourceCompileReport'] = self.pin(self.compilation)
                self.persist()
                with self.assertRaisesRegex(ValueError, 'Complete source compilation'):
                    self.validate()

    def test_stale_native_receipt_cannot_be_reauthorized_by_new_pin(self):
        self.persist(native_modified=self.native_started - 1_000_000_000)
        with self.assertRaisesRegex(ValueError, 'Native build receipt is stale'):
            self.validate()

    def test_native_receipt_tampering_is_rejected(self):
        self.native_path.write_text('{}\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Native build receipt is stale or differs'):
            self.validate()

    def test_stale_link_reports_are_rejected_even_with_matching_receipts(self):
        key = next(iter(self.native['reports']))
        path = self.root / key
        old = self.native_started - 1_000_000_000
        os.utime(path, ns=(old, old))
        pin = self.pin(path)
        pin.pop('path')
        self.native['reports'][key] = pin
        self.outer['reports'] = copy.deepcopy(self.native['reports'])
        self.persist()
        with self.assertRaisesRegex(ValueError, 'Native link report is stale'):
            self.validate()

    def test_frozen_canonical_report_substitution_is_rejected(self):
        reports = {}
        for name in REPORTS:
            path = self.root / 'evidence/linking' / name
            self.write(path, dict(pretendingFresh=True), self.clock - 7_000_000_000)
            pin = self.pin(path)
            reports[pin.pop('path')] = pin
        self.native['reports'] = reports
        self.outer['reports'] = copy.deepcopy(reports)
        self.persist()
        with self.assertRaisesRegex(ValueError, 'Native link report paths'):
            self.validate()

    def test_parent_report_inventory_cannot_differ_from_native_receipt(self):
        self.outer['reports'].pop(next(iter(self.outer['reports'])))
        self.persist()
        with self.assertRaisesRegex(ValueError, 'inventories differ'):
            self.validate()

    def test_complete_module_scope_and_explicit_native_only_scope_are_required(self):
        original = copy.deepcopy(self.native)
        for changes in (dict(buildPassed=False), dict(nativeBuildPassed=False),
                        dict(moduleCount=19), dict(initializedBytes=1), dict(acceptedFunctionsLinked=11481),
                        dict(allModuleBytesExact=False), dict(allSymbolChecksPassed=False),
                        dict(frozenInputsUnchanged=False), dict(behavioralReplayPerformed=True),
                        dict(fullContainerBuildPerformed=True), dict(importedLinkageSourceCredit=1)):
            with self.subTest(changes=changes):
                self.native = dict(original, **changes)
                self.persist()
                with self.assertRaises(ValueError):
                    self.validate()

    def test_native_compilation_must_bind_the_parent_start_and_compile_pin(self):
        self.native['compilationNotBeforeTimeNs'] = self.started - 1
        self.persist()
        with self.assertRaisesRegex(ValueError, 'not bound'):
            self.validate()
        self.native['compilationNotBeforeTimeNs'] = self.started
        self.native['publicSourceCompileReport'] = dict(self.native['publicSourceCompileReport'], sha256='b' * 64)
        self.persist()
        with self.assertRaisesRegex(ValueError, 'another source compilation report'):
            self.validate()

    def test_prior_ci_native_build_cannot_be_rewrapped_in_a_new_parent_receipt(self):
        self.native['startedTimeNs'] = self.started - 1_000_000_000
        self.outer['nativeStartedTimeNs'] = self.native['startedTimeNs']
        self.persist()
        with self.assertRaisesRegex(ValueError, 'predates this CI build'):
            self.validate()

    def test_other_commit_and_ci_revision_are_rejected(self):
        self.native['publicGitRevision'] = 'b' * 40
        self.persist()
        with self.assertRaisesRegex(ValueError, 'another revision'):
            self.validate()
        with patch('build_receipts.subprocess.check_output', return_value=self.revision + '\n'), patch.dict(os.environ, {'GITHUB_SHA': 'c' * 40}):
            with self.assertRaisesRegex(ValueError, 'CI revision'):
                validate_build_receipt(self.root, self.root, self.outer_path, self.manifest_hash)

    def test_requested_compile_report_cannot_switch_to_another_file(self):
        other = self.root / 'build/other/report.json'
        self.write(other, json.loads(self.compilation.read_text()), self.clock - 15_000_000_000)
        with self.assertRaisesRegex(ValueError, 'Requested source compilation report differs'):
            self.validate(compilation=other)

    def test_legacy_full_replay_keeps_canonical_report_paths(self):
        reports = {}
        for name in REPORTS:
            path = self.root / 'evidence/linking' / name
            self.write(path, dict(legacyFullReplay=True), self.clock - 8_000_000_000)
            pin = self.pin(path)
            reports[pin.pop('path')] = pin
        self.outer['buildScope'] = 'full-replay'
        self.outer['reports'] = reports
        self.outer['replayStartedTimeNs'] = self.native_started
        self.write(self.outer_path, self.outer)
        result = self.validate()
        self.assertEqual(result['buildScope'], 'full-replay')
        self.assertTrue(all(p.parent == self.root / 'evidence/linking' for p in result['reports'].values()))


if __name__ == '__main__':
    unittest.main()
