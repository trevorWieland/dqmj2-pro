import copy
import stat
import time
from pathlib import Path
from unittest.mock import patch
from project import ROOT,sha256,read_json
import source_selection as P
import recovery_registry as R
from probe_source_selection_snapshot_20261106 import Tracker,EpochChanged,ORIGINAL_PREF


class GuardedSnapshot:
    def __init__(self,namespace,tracker=None,policy=None,registry=None):
        self.namespace=namespace;self.tracker=tracker or Tracker();self.policy=policy or P.POLICY;self.registry=registry or R.REGISTRY;self.policySha=self.tracker.hash(self.policy);self.registrySha=self.tracker.hash(self.registry);self.localFacts={};self.defaultHits=0;self.registryHits=0;self.customCalls=0;self.observedChange=False;self.started=time.perf_counter();local=P.local
        def track(value):
            resolved=local(value);self.localFacts[value]=str(resolved);return resolved
        self.registryRows=self.tracker.read(self.registry)['batches']
        with patch.object(P,'local',track),patch.object(P,'sha256',self.tracker.hash),patch.object(P,'read_json',self.tracker.read):self.policies=ORIGINAL_PREF(namespace,self.policy)
        self.facts={p:self.tracker.fact(p) for p in self.tracker.hashes};self.buildSeconds=time.perf_counter()-self.started
    def fail(self,reason):self.observedChange=True;self.tracker.observedChange=True;raise EpochChanged(reason)
    def quick(self):
        try:
            if sha256(self.registry)!=self.registrySha or sha256(self.policy)!=self.policySha:self.fail('Run-local registry/default policy content changed')
            for p,fact in self.facts.items():
                if self.tracker.fact(p)!=fact:self.fail('Run-local policy dependency type/identity/metadata changed')
        except OSError:self.fail('Run-local policy dependency missing or unreadable')
    def preferences(self,namespace,path=None):
        actual=self.policy if path is None else path
        if namespace!=self.namespace or actual!=self.policy:self.customCalls+=1;return ORIGINAL_PREF(namespace,actual)
        self.quick();self.defaultHits+=1;return copy.deepcopy(self.policies)
    def batches(self):self.quick();self.registryHits+=1;return copy.deepcopy(self.registryRows)
    def verify(self):
        if self.observedChange:self.fail('Run-local epoch change was observed even if restored')
        self.quick()
        for value,resolved in self.localFacts.items():
            if str(P.local(value))!=resolved:self.fail('Run-local policy source/report/evidence path target changed')
        self.tracker.verify()
