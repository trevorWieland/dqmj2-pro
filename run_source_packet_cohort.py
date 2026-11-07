import argparse
import copy
import importlib.util
from pathlib import Path
from project import ROOT, sha256

DELEGATE = 'run_source_cohort_v6_20261106.py'
DELEGATE_SHA256 = '0957115a217a4988c279da1ec54f2229eb88d3e24e0663ca2c500c8c14a365bc'

def load_delegate():
    if sha256(ROOT/DELEGATE) != DELEGATE_SHA256:
        raise ValueError('Frozen sixteen-stage delegation changed')
    spec = importlib.util.spec_from_file_location('frozen_source_stage_delegation',ROOT/DELEGATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.verify()
    return module

def delegate(original, frozen, cohort):
    previous_read, previous_write, previous_process = original.read_json, original.write_json, original.subprocess
    dispatch = frozen.Dispatch(previous_process)
    target = ROOT/f'evidence/verification/cohort{cohort}-validation-driver.json'
    def read(path):
        value = previous_read(path)
        return frozen.rewrite_steps(value) if Path(path) == ROOT/frozen.TEMPLATE else value
    def write(path,value):
        if Path(path) != target or value.get('cohort') != cohort:
            raise ValueError('Source stage driver cannot overwrite another cohort artifact')
        if value.get('state') == 'build-and-regression-checks-passed':
            dispatch.complete()
        result = copy.deepcopy(value)
        result['utilityAliasLinkDelegation'] = dict(cohort=cohort,delegate=DELEGATE,
            delegateSha256=DELEGATE_SHA256,originalRunner=frozen.ORIGINAL,
            originalRunnerSha256=frozen.ORIGINAL_SHA256,template=frozen.TEMPLATE,
            templateSha256=frozen.TEMPLATE_SHA256,delegateInputs=frozen.DELEGATES,
            originalCommand=frozen.TARGET,actualCommand=frozen.WRAPPER,expectedStages=16,
            stagesDispatched=dispatch.next,wrapperDispatches=dispatch.wrapper_count,
            originalStageGuardsAndPredicatesUnchanged=True,sourceCredit=0)
        return previous_write(path,result)
    original.read_json, original.write_json, original.subprocess = read, write, dispatch
    return previous_read,previous_write,previous_process,dispatch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort',type=int,required=True)
    cohort = parser.parse_args().cohort
    if cohort < 175:
        raise ValueError('Historical cohorts retain their original frozen runners')
    frozen = load_delegate()
    original = frozen.load_original()
    previous_read,previous_write,previous_process,dispatch = delegate(original,frozen,cohort)
    try:
        original.main()
        dispatch.complete()
    finally:
        original.read_json,original.write_json,original.subprocess = previous_read,previous_write,previous_process
        frozen.verify()
        if sha256(ROOT/DELEGATE) != DELEGATE_SHA256:
            raise ValueError('Frozen source delegation changed during execution')

if __name__ == '__main__':
    main()
