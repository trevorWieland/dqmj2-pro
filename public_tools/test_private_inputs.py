import hashlib
import io
import json
import tarfile
import tempfile
import time
import unittest
from pathlib import Path

from build_bytematch import BundleError, build_outcome, install_bundle


class PrivateInputTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / "work/private-input-tests"
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "checkout"
        self.bundle = Path(self.temporary.name) / "bundle"
        (self.root / "public").mkdir(parents=True)
        self.bundle.mkdir()
        self.revision = "a" * 40
        self.accepted = self.root / "public/accepted-functions.json"
        self.accepted.write_text(json.dumps(dict(revision=self.revision)), encoding="utf-8")

    def pack(self, files, revision=None, split=False):
        payload = io.BytesIO()
        with tarfile.open(fileobj=payload, mode="w:gz") as archive:
            for name, body in files:
                info = tarfile.TarInfo(name)
                if body is None:
                    info.type = tarfile.SYMTYPE
                    info.linkname = "../../src/game.c"
                    archive.addfile(info)
                else:
                    info.size = len(body)
                    archive.addfile(info, io.BytesIO(body))
        raw = payload.getvalue()
        chunks = [raw[:len(raw) // 2], raw[len(raw) // 2:]] if split else [raw]
        parts = []
        for index, chunk in enumerate(chunks):
            name = f"inputs.tar.gz.part{index}"
            (self.bundle / name).write_bytes(chunk)
            parts.append(dict(name=name, sha256=hashlib.sha256(chunk).hexdigest()))
        (self.bundle / "manifest.json").write_text(json.dumps(dict(schemaVersion=1,
            snapshotRevision=revision or self.revision, archiveParts=parts)), encoding="utf-8")

    def test_split_archive_installs_and_identical_inputs_are_reused(self):
        self.pack([("inputs/game.nds", b"owned-input"), ("recovery.json", b"{}")], split=True)
        result = install_bundle(self.root, self.bundle)
        self.assertEqual(result["installedFiles"], 2)
        self.assertEqual((self.root / "inputs/game.nds").read_bytes(), b"owned-input")
        result = install_bundle(self.root, self.bundle)
        self.assertEqual(result["installedFiles"], 0)
        self.assertEqual(result["identicalExistingFiles"], 2)

    def test_traversal_is_rejected_before_installing_any_files(self):
        self.pack([("inputs/game.nds", b"owned"), ("../outside", b"bad")])
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)
        self.assertFalse((self.root / "inputs/game.nds").exists())

    def test_public_source_cannot_be_supplied_or_overwritten(self):
        (self.root / "src").mkdir()
        source = self.root / "src/game.c"
        source.write_bytes(b"original public source")
        for name in ("src/game.c", "docs/guide.md", "config/arm9/config.yaml", "public_tools/check.py", "configure.py"):
            with self.subTest(name=name):
                self.pack([(name, b"replacement")])
                with self.assertRaises(BundleError):
                    install_bundle(self.root, self.bundle)
        self.assertEqual(source.read_bytes(), b"original public source")

    def test_conflicting_existing_input_is_preserved(self):
        (self.root / "inputs").mkdir()
        target = self.root / "inputs/game.nds"
        target.write_bytes(b"existing owner input")
        self.pack([("inputs/game.nds", b"different input")])
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)
        self.assertEqual(target.read_bytes(), b"existing owner input")

    def test_missing_private_source_descriptor_can_be_supplied(self):
        self.pack([('src/runtime/layout.json', b'{"private":true}')])
        install_bundle(self.root, self.bundle)
        self.assertTrue((self.root / 'src/runtime/layout.json').is_file())

    def test_existing_public_source_descriptor_cannot_be_overwritten(self):
        target = self.root / 'src/runtime/layout.json'
        target.parent.mkdir(parents=True)
        target.write_bytes(b'{}')
        self.pack([('src/runtime/layout.json', b'{"replacement":true}')])
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)

    def test_part_hash_mismatch_is_rejected(self):
        self.pack([("inputs/game.nds", b"owned")])
        (self.bundle / "inputs.tar.gz.part0").write_bytes(b"changed")
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)
        self.assertFalse((self.root / "inputs").exists())

    def test_wrong_snapshot_is_rejected(self):
        self.pack([("inputs/game.nds", b"owned")], revision="b" * 40)
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)
        self.assertFalse((self.root / "inputs").exists())

    def test_symbolic_link_member_is_rejected(self):
        self.pack([("inputs/game.nds", None)])
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)

    def test_windows_alias_paths_are_rejected(self):
        for name in ("inputs/../src/game.c", "inputs\\game.nds", "inputs/game.nds:stream", "tools/NUL", "inputs/game.nds."):
            with self.subTest(name=name):
                self.pack([(name, b"bad")])
                with self.assertRaises(BundleError):
                    install_bundle(self.root, self.bundle)

    def test_declared_missing_inputs_are_rejected(self):
        self.pack([("inputs/game.nds", b"owned")])
        path = self.bundle / "manifest.json"
        value = json.loads(path.read_text())
        value["missingRequiredInputs"] = ["evidence/frozen-input.json"]
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaises(BundleError):
            install_bundle(self.root, self.bundle)


class BuildOutcomeTests(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1] / "work/private-input-tests"
        workspace.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / "evidence/verification"
        self.output.mkdir(parents=True)
        self.start = time.time_ns() - 1_000_000_000
        self.checks = dict(allChecksPassed=False, buildAndOracleChecksPassed=True,
            steps=[dict(command=["python", "build.py"], exitCode=0),
                   dict(command=["python", "verify_workspace.py"], exitCode=1)])
        self.audit = dict(sourcePolicy=dict(passed=True), gitRemotes=["origin"],
            isolation=dict(observedChanges=[], unavailableSnapshots=[dict(category="baseline", path="old-private-path")]))

    def outcome(self, exit_code=1):
        (self.output / "checks.json").write_text(json.dumps(self.checks), encoding="utf-8")
        (self.output / "workspace.json").write_text(json.dumps(self.audit), encoding="utf-8")
        return build_outcome(self.root, exit_code, self.start)

    def test_public_policy_override_preserves_legacy_failure_and_reasons(self):
        result = self.outcome()
        self.assertTrue(result["publicReportingOverride"])
        self.assertFalse(result["legacyAllChecksPassed"])
        self.assertEqual(result["gitRemotes"], ["origin"])
        self.assertEqual(result["unavailableSnapshots"], self.audit["isolation"]["unavailableSnapshots"])

    def test_observed_changes_prevent_override(self):
        self.audit["isolation"]["observedChanges"] = [dict(category="application", path="changed.c")]
        with self.assertRaises(BundleError):
            self.outcome()

    def test_source_policy_failure_prevents_override(self):
        self.audit["sourcePolicy"]["passed"] = False
        with self.assertRaises(BundleError):
            self.outcome()

    def test_build_oracle_failure_prevents_override(self):
        self.checks["buildAndOracleChecksPassed"] = False
        with self.assertRaises(BundleError):
            self.outcome()

    def test_other_failed_step_prevents_override(self):
        self.checks["steps"][0]["exitCode"] = 1
        with self.assertRaises(BundleError):
            self.outcome()

    def test_unknown_workspace_failure_prevents_override(self):
        self.audit["gitRemotes"] = []
        self.audit["isolation"]["unavailableSnapshots"] = []
        with self.assertRaises(BundleError):
            self.outcome()

    def test_fully_passing_build_needs_no_override(self):
        self.checks["allChecksPassed"] = True
        self.assertFalse(self.outcome(exit_code=0)["publicReportingOverride"])


if __name__ == "__main__":
    unittest.main()
