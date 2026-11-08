import argparse
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256
from finish_source_package_context import PINS, verify
from finish_source_packet_cohort import Route
from staged_git_checks import names


CONTEXT = 'cohort176_committed_context_v3.py'
REPORT = 'evidence/verification/cohort176-current-scope-context-v1-20261108.json'
ORIGINAL = 'finish_source_package_v25_20261106.py'
SCOPE = 'current-main-matching-inputs'


def require(value, message):
    if not value:
        raise ValueError(message)


class CurrentRoute(Route):
    def __init__(self, module, package, pins):
        super().__init__(module, 176, package)
        self.extra = REPORT
        self.pins = copy.deepcopy(pins)

    def dispatch(self, command, log):
        expected = [sys.executable, str(ROOT / 'verify_committed_source_inputs_context_v9_20261106.py'), '--cohort', '176']
        if command != expected:
            return super().dispatch(command, log)
        require(self.stage_done and not self.audit_done, 'Exactly one staging must precede committed scope audit')
        actual = [sys.executable, '-B', str(ROOT / CONTEXT), '--cohort', '176']
        for role in ('epoch-contract', 'scope-contract', 'scope-proof', 'scope-driver'):
            actual.extend(['--' + role + '-sha256', self.pins[role]['sha256']])
        result = self.previous_run(actual, log)
        self.audit_done = True
        return result

    def write(self, path, value):
        if Path(path) != ROOT / self.closure:
            return super().write(path, value)
        require(self.audit_done and not self.closure_done, 'Fresh committed scope audit required exactly once')
        require((value.get('cohort'), value.get('passed'), value.get('sourceCredit'), value.get('fullCleanReplayProven'))
                == (176, True, 0, False), 'Frozen closure predicates changed')
        require([row['path'] for row in value['reports']] == self.base, 'Frozen source/oracle components changed')
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        require(value['sourceCommit'] == revision, 'Closure source commit differs from actual HEAD')
        for row in value['reports']:
            require(row['sha256'] == sha256(ROOT / row['path']), 'Frozen closure component bytes changed')
            report = read_json(ROOT / row['path'])
            proof = report.get('committedVerification', report)
            require(proof.get('passed') is True and proof.get('commit') == revision, 'Base audit does not bind source commit')
        report = read_json(ROOT / self.extra)
        require(report.get('passed') is True and report.get('commit') == revision and report.get('cohort') == 176
                and report.get('sourceCredit') == 0 and report.get('acceptanceScope') == SCOPE, 'Current scope report failed or changed commit')
        require(all(report.get(name) is True for name in ('allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted',
                'canonicalRegistryEpochAuthenticated', 'historical1375BatchRecordsPreserved')), 'Inherited committed checks incomplete')
        require(report.get('originalFullDriverPassed') is False and report.get('originalHistoricalWorkspacePassed') is False,
                'Original failure status hidden')
        require(report['generator'] == CONTEXT and report['generatorSha256'] == sha256(ROOT / CONTEXT), 'Unreviewed report generator')
        for role, field in [('epoch-contract', 'epochContract'), ('scope-contract', 'scopeContract'),
                            ('scope-proof', 'workspaceScopeProof'), ('scope-driver', 'scopedDriver')]:
            require(report[field] == self.pins[role], 'Context defining input differs')
            require(sha256(ROOT / self.pins[role]['path']) == self.pins[role]['sha256'], 'Context defining input changed')
        context = report['contextQualification']
        native = context['newHostLiveReference']
        require((native['functions'], native['bytes'], native['c99Functions'], native['thumbFunctions']) == (6, 1184, 5, 1)
                and len(native['compilerLinkProofs']) == 6, 'New native reference scope incomplete')
        events = context['comparisonProjectionEvents']
        require(events and all(len(event) == 9 for event in events), 'Exact nine-field comparison projection missing')
        require(context['originalMainLedgerFileConsumers'] == 26 and context['unchangedMainComparisonViewConsumers'] == 36
                and context['originalFullDriverAndWorkspaceUnmodified'] is True, 'Original ledger or failure scope changed')
        result = copy.deepcopy(value)
        result['reports'].append(dict(path=self.extra, sha256=sha256(ROOT / self.extra)))
        result['finisherContext'] = dict(originalFinisher=ORIGINAL, pinnedEntrypoints=PINS,
            stagePackage=self.package, acceptanceScope=SCOPE, historicalOriginalDriverPassed=False,
            historicalOriginalWorkspacePassed=False, underlyingFinisherGuardsUnchanged=True, sourceCredit=0)
        result['scopedStagedGitChecks'] = dict(allIndexVsHeadChangesIncluded=True, windowsArgvBudget=16000, sourceCredit=0)
        written = self.previous_write(path, result)
        self.closure_done = True
        return written


def main():
    import cohort176_scope_acceptance_v1 as acceptance
    import cohort176_committed_context_v3 as context
    parser = argparse.ArgumentParser()
    for name in ('package', 'document', 'label'):
        parser.add_argument('--' + name, required=True)
    for role in ('epoch-contract', 'scope-contract', 'scope-proof', 'scope-driver'):
        parser.add_argument('--' + role + '-sha256', required=True)
    args = parser.parse_args()
    verify()
    require(not names(subprocess, ROOT), 'Empty index required before current-scope transaction')
    require(not (ROOT / REPORT).exists(), 'Current committed scope report already exists; no retry')
    paths = {'epoch-contract': context.EPOCH_CONTRACT, 'scope-contract': context.SCOPE_CONTRACT,
             'scope-proof': context.SCOPE_PROOF, 'scope-driver': acceptance.SCOPED_DRIVER}
    pins = {}
    for role, name in paths.items():
        expected = getattr(args, role.replace('-', '_') + '_sha256')
        raw = acceptance.checked(ROOT, dict(path=name, sha256=expected))
        pins[role] = dict(path=name, bytes=len(raw), sha256=expected)
    proof = json.loads(acceptance.checked(ROOT, pins['scope-proof']))
    acceptance.precommit(ROOT, dict(contract=pins['scope-contract'], preproof=pins['scope-proof']),
                         pins['scope-driver'], proof['qualificationCompletedUtc'])
    spec = importlib.util.spec_from_file_location('frozen_current_scope_finisher', ROOT / ORIGINAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    route = CurrentRoute(module, args.package, pins)
    module.run, module.write_json, module.subprocess = route.dispatch, route.write, route
    previous_argv = sys.argv
    sys.argv = [str(ROOT / ORIGINAL), '--cohort', '176', '--stage', 'stage_declared_source_package_v9_20261106.py',
                '--document', args.document, '--label', args.label]
    try:
        module.main()
        route.complete()
    finally:
        sys.argv = previous_argv
        module.run, module.write_json, module.subprocess = route.previous_run, route.previous_write, route.process
        verify()


if __name__ == '__main__':
    main()
