import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys
from project import ROOT, read_json, sha256


ORIGINAL = 'run_source_cohort_v5_20261106.py'
ORIGINAL_SHA256 = '080352fe3e679b3ddf0c36e8e4c2de6da7a93092faa21cb841d30a2963b24821'
TEMPLATE = 'evidence/verification/cohort67-validation-driver.json'
TEMPLATE_SHA256 = '2b39b5ce1f8453f9638819a0336016ff64e511b0b25e770cde244d446f5b3487'
TARGET = ['link_utility.py', '--clean']
WRAPPER = ['link_utility_child_snd_alias_v1_20261106.py', '--clean']
DELEGATES = [dict(path=WRAPPER[0], sha256='f0709383fd7b83d7665bdb8341ca37d50d136f28b9bf7661403c4a6db444ca16'),
    dict(path='utility_child_snd_alias_v1_20261106.py', sha256='9b915a150ae51f3b84b05ed5ee378119d10a41a22c0ce810793c372b2180832a'),
    dict(path='provenance/utility-child-snd-alias-v1-20261106-contract.json', sha256='fa4b1c02d4f16b8988fa658bb4a2bb9269f593d59371aa3fb409b87e824be84c')]
sys.dont_write_bytecode = True
if sha256(ROOT / TEMPLATE) != TEMPLATE_SHA256:
    raise ValueError('Exact original sixteen-stage template changed')
BASELINE = [copy.deepcopy(item['command']) for item in read_json(ROOT / TEMPLATE)['steps']]


def verify():
    for item in [dict(path=ORIGINAL, sha256=ORIGINAL_SHA256), dict(path=TEMPLATE, sha256=TEMPLATE_SHA256), *DELEGATES]:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Pinned cohort174 runner delegation changed: ' + item['path'])


def rewrite_steps(value):
    commands = [item['command'] for item in value['steps']]
    if len(commands) != 15 or commands != BASELINE or commands.count(TARGET) != 1:
        raise ValueError('Only the exact original fifteen template commands and one utility clean step are supported')
    result = copy.deepcopy(value)
    for item in result['steps']:
        if item['command'] == TARGET:
            item['command'] = list(WRAPPER)
    return result


def expected_commands():
    result = [['verify_source_selection_v2_20261106.py'], *copy.deepcopy(BASELINE)]
    for index, command in enumerate(result):
        if command == ['integrate.py', '--clean']:
            result[index] = ['integrate_context_v4_20261106.py', '--clean']
        elif command == ['validate_evidence.py']:
            result[index] = ['validate_evidence_ash_cache_20261031.py']
        elif command == TARGET:
            result[index] = list(WRAPPER)
    if len(result) != 16 or result.count(WRAPPER) != 1:
        raise ValueError('Exact sixteen-stage command contract differs')
    return result


class Dispatch:
    def __init__(self, previous):
        self.previous = previous
        self.commands = expected_commands()
        self.next = 0
        self.wrapper_count = 0

    def __getattr__(self, name):
        return getattr(self.previous, name)

    def run(self, command, *args, **kwargs):
        if self.next >= 16:
            raise ValueError('Duplicate or additional cohort174 stage dispatch')
        expected = self.commands[self.next]
        executable = [sys.executable, str(ROOT / expected[0]), *expected[1:]]
        if command != executable or kwargs.get('cwd') != ROOT:
            raise ValueError('Cohort174 stage command/order/arguments differ from the exact delegated V5 sequence')
        if expected == WRAPPER:
            stream = kwargs.get('stdout')
            if stream is None:
                raise ValueError('Actual wrapper command must be recorded in its original stage log')
            stream.write(json.dumps(dict(actualDelegatedCommand=command, originalCommand=TARGET, sourceCredit=0)) + '\n')
            stream.flush()
            self.wrapper_count += 1
        self.next += 1
        return self.previous.run(command, *args, **kwargs)

    def complete(self):
        if self.next != 16 or self.wrapper_count != 1:
            raise ValueError('Missing original stage or exact-once utility wrapper dispatch')


def load_original():
    verify()
    spec = importlib.util.spec_from_file_location('cohort174_original_v5', ROOT / ORIGINAL)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    return original


def delegate(original):
    previous_read, previous_write, previous_process = original.read_json, original.write_json, original.subprocess
    dispatch = Dispatch(previous_process)
    output = ROOT / 'evidence/verification/cohort174-validation-driver.json'
    def read(path):
        value = previous_read(path)
        return rewrite_steps(value) if Path(path) == ROOT / TEMPLATE else value
    def write(path, value):
        if Path(path) != output:
            return previous_write(path, value)
        if value.get('cohort') != 174:
            raise ValueError('Version6 utility alias delegation is restricted to cohort174')
        if value.get('state') == 'build-and-regression-checks-passed':
            dispatch.complete()
        result = copy.deepcopy(value)
        result['utilityAliasLinkDelegation'] = dict(originalRunner=ORIGINAL, originalRunnerSha256=ORIGINAL_SHA256,
            template=TEMPLATE, templateSha256=TEMPLATE_SHA256, delegateInputs=DELEGATES,
            originalCommand=TARGET, actualCommand=WRAPPER, expectedStages=16,
            stagesDispatched=dispatch.next, wrapperDispatches=dispatch.wrapper_count,
            remainingV5GuardsAndPredicatesUnchanged=True, sourceListFileUnchanged=True, sourceCredit=0)
        return previous_write(path, result)
    original.read_json, original.write_json, original.subprocess = read, write, dispatch
    return previous_read, previous_write, previous_process, dispatch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True, choices=[174])
    parser.parse_args()
    original = load_original()
    previous_read, previous_write, previous_process, dispatch = delegate(original)
    try:
        original.main()
        dispatch.complete()
    finally:
        original.read_json, original.write_json, original.subprocess = previous_read, previous_write, previous_process
        verify()


if __name__ == '__main__':
    main()
