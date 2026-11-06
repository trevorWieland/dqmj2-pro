import contextlib
import io
import json
import tempfile
import time
import unittest
from pathlib import Path

from build_bytematch import BundleError, build_outcome, run_private
from progress_accounting import accounting


class ReportingBoundaryTests(unittest.TestCase):
    def setUp(self):
        work = Path(__file__).resolve().parents[1] / 'work/reporting-boundary-tests'
        work.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_child_output_only_exposes_script_exit_status(self):
        script = self.root / 'child.py'
        script.write_text('import json\nprint("private original instruction dump")\nprint(json.dumps({"script":"check.py","exitCode":0}))\nprint(json.dumps({"script":"check.py","exitCode":0,"instructions":["private"]}))\n', encoding='utf-8')
        private_log, public_log = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(public_log):
            run_private(self.root, private_log, ['child.py'])
        self.assertEqual(json.loads(public_log.getvalue()), {'script': 'check.py', 'exitCode': 0})
        self.assertIn('private original instruction dump', private_log.getvalue())
        self.assertNotIn('private', public_log.getvalue())

    def test_copied_historical_checks_cannot_authorize_a_build(self):
        path = self.root / 'evidence/verification/checks.json'
        path.parent.mkdir(parents=True)
        path.write_text('{"allChecksPassed":true}', encoding='utf-8')
        with self.assertRaises(BundleError):
            build_outcome(self.root, 0, time.time_ns() + 1000000)

    def test_bss_does_not_inflate_native_initialized_progress(self):
        directory = self.root / 'public'
        directory.mkdir()
        functions = dict(revision='snapshot', romSha256='build', acceptedInitializedBytes=30,
                         initializedDenominatorBytes=100, sourceOnlyRomProven=False,
                         functions=[dict(bytes=2, states=dict(functionMatched=True, moduleLinked=True))])
        data = dict(buildSha256='build', records=[
            dict(kind='data', storedBytes=4, states=dict(dataMatched=True, moduleLinked=True)),
            dict(kind='bss', storedBytes=512, states=dict(dataMatched=True, moduleLinked=True))])
        (directory / 'accepted-functions.json').write_text(json.dumps(functions), encoding='utf-8')
        (directory / 'accepted-data.json').write_text(json.dumps(data), encoding='utf-8')
        result = accounting(self.root)
        self.assertEqual(result['initializedSourcePercent'], 30)
        self.assertEqual(result['acceptedDataInitializedBytes'], 4)
        self.assertEqual(result['separatelyAcceptedAlignmentBytes'], 24)


if __name__ == '__main__':
    unittest.main()
