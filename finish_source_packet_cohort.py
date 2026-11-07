import argparse
import copy
import importlib.util
import sys
from pathlib import Path
from project import ROOT,read_json,sha256
from finish_source_package_context import PINS,verify
from staged_git_checks import names,check

ORIGINAL = 'finish_source_package_v25_20261106.py'

class Route:
    def __init__(self,module,cohort,package):
        if cohort < 175:
            raise ValueError('Historical cohorts retain their frozen finishers')
        package_path = (ROOT/package).resolve()
        if not package_path.is_relative_to(ROOT) or not package_path.is_file():
            raise ValueError('Source package must be an existing repository-local file')
        if read_json(package_path)['cohort'] != cohort:
            raise ValueError('Source package belongs to another cohort')
        self.cohort,self.package = cohort,package
        self.previous_run,self.previous_write,self.process = module.run,module.write_json,module.subprocess
        self.base = [f'evidence/verification/cohort{cohort}-committed-source-inputs-v14-20261105.json',
            f'evidence/verification/cohort{cohort}-captured-oracle-closure-verification-20261031.json']
        self.extra = f'evidence/verification/cohort{cohort}-overlay-reference-context-v10-20261106.json'
        self.closure = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
        self.stage_done = self.audit_done = self.closure_done = self.extra_staged = False

    def __getattr__(self,name):
        return getattr(self.process,name)

    def dispatch(self,command,log):
        stage = [sys.executable,str(ROOT/'stage_declared_source_package_v9_20261106.py')]
        audit = [sys.executable,str(ROOT/'verify_committed_source_inputs_context_v9_20261106.py'),'--cohort',str(self.cohort)]
        if command == stage:
            if self.stage_done:
                raise ValueError('Duplicate source-package staging')
            result = self.previous_run([*stage,self.package],log)
            self.stage_done = True
            return result
        if command == audit:
            if not self.stage_done or self.audit_done:
                raise ValueError('Committed source audit must follow exactly one staging operation')
            actual = [sys.executable,str(ROOT/'verify_committed_source_inputs_context_v10_20261106.py'),'--cohort',str(self.cohort)]
            result = self.previous_run(actual,log)
            self.audit_done = True
            return result
        return self.previous_run(command,log)

    def write(self,path,value):
        if Path(path) != ROOT/self.closure:
            if Path(path).parent == ROOT/'evidence/verification' and Path(path).name.endswith('-expanded-source-closure-20261101.json'):
                raise ValueError('Cannot overwrite another cohort expanded closure')
            return self.previous_write(path,value)
        if not self.audit_done or self.closure_done:
            raise ValueError('Fresh committed context audit required exactly once')
        if (value.get('cohort'),value.get('passed'),value.get('sourceCredit'),value.get('fullCleanReplayProven')) != (self.cohort,True,0,False):
            raise ValueError('Original closure scope/success predicates changed')
        if [row['path'] for row in value['reports']] != self.base:
            raise ValueError('Original source/oracle closure components changed')
        if any(row['sha256'] != sha256(ROOT/row['path']) for row in value['reports']):
            raise ValueError('Original closure component bytes changed')
        proof = read_json(ROOT/self.extra)
        if proof.get('sourceCredit') != 0 or not all(proof.get(name) is True for name in
                ('passed','allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted','sourceRegistryAndFrozen174MembershipUnchanged')):
            raise ValueError('Qualified overlay context did not finish its inherited checks')
        result = copy.deepcopy(value)
        result['reports'].append(dict(path=self.extra,sha256=sha256(ROOT/self.extra)))
        result['finisherContext'] = dict(originalFinisher=ORIGINAL,pinnedEntrypoints=PINS,
            stagePackage=self.package,underlyingFinisherGuardsUnchanged=True,sourceCredit=0)
        result['scopedStagedGitChecks'] = dict(allIndexVsHeadChangesIncluded=True,windowsArgvBudget=16000,sourceCredit=0)
        written = self.previous_write(path,result)
        self.closure_done = True
        return written

    def run(self,command,*args,**kwargs):
        expected = ['git','add','--',*self.base,self.closure]
        if command == expected:
            if not self.closure_done or self.extra_staged:
                raise ValueError('Explicit namespace closure component must be staged exactly once')
            result = self.process.run(['git','add','--',*self.base,self.extra,self.closure],*args,**kwargs)
            self.extra_staged = True
            return result
        if command == ['git','diff','--cached','--name-only']:
            paths = names(self.process,ROOT)
            return self.process.CompletedProcess(command,0,''.join(name+'\n' for name in paths),'')
        if command == ['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check']:
            return check(self.process,ROOT,command,names(self.process,ROOT))
        return self.process.run(command,*args,**kwargs)

    def complete(self):
        if not all((self.stage_done,self.audit_done,self.closure_done,self.extra_staged)):
            raise ValueError('Source package finisher did not complete every required operation')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort',type=int,required=True)
    parser.add_argument('--package',required=True)
    parser.add_argument('--document',required=True)
    parser.add_argument('--label',required=True)
    args = parser.parse_args()
    verify()
    spec = importlib.util.spec_from_file_location('frozen_source_package_finisher',ROOT/ORIGINAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    route = Route(module,args.cohort,args.package)
    module.run,module.write_json,module.subprocess = route.dispatch,route.write,route
    previous_argv = sys.argv
    sys.argv = [str(ROOT/ORIGINAL),'--cohort',str(args.cohort),'--stage','stage_declared_source_package_v9_20261106.py',
        '--document',args.document,'--label',args.label]
    try:
        module.main()
        route.complete()
    finally:
        sys.argv = previous_argv
        module.run,module.write_json,module.subprocess = route.previous_run,route.previous_write,route.process
        verify()

if __name__ == '__main__':
    main()
