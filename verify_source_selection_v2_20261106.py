import contextlib
from unittest.mock import patch
from project import ROOT,configuration,sha256
import verify_source_selection as original
import source_selection as selection
import ledger_state
import source_dependencies
from probe_source_selection_snapshot_20261106 import Tracker
from guard_source_selection_snapshot_20261106 import GuardedSnapshot


PINS={
    'verify_source_selection.py':'c60cf9becbcd75742ee906a8e445398b4498c7382a1d1bcd540dac6b3e30fad4',
    'source_selection.py':'09f1bf791bf05ccb528462fd6764d93e772cf829f582dd6265798082035dbd4d',
    'ledger_state.py':'35b0b76b478d2860c9135fe6968549cc590b582bff2eedf0db2e2b2c4ae6de4a',
    'recovery_registry.py':'920470a8ce920654343c389bc1ff3a9c3959cca8e6536791655d9fc2c520c01d',
    'source_dependencies.py':'97efee44d3bbb96ac70cfee5034d2d08c269688b96f511d29fb17ce70154db75',
    'project.py':'2b305d7f6cb69bd8ffb68498bfb1749f9b7c9b7002601bf49b5c3ce825f1676a',
    'project.json':'b81583c95a586d37beb2ec4436e23403af90e4499be59dc61e1e10420207adab',
    'guard_source_selection_snapshot_20261106.py':'7e5bad332866d7583ac2a16f66ba6bacdffcf1c599fa8255ca9be47089f923a4',
    'probe_source_selection_snapshot_20261106.py':'7ac4db2838b2c026be5684be275515584f61ceddb45c60396d9d24aec949e597'
}


class InputTracker(Tracker):
    def private(self,path):return False


def verify_pins():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Qualified source-selection implementation changed: '+name)


def main():
    verify_pins();tracker=InputTracker();snapshot=GuardedSnapshot(configuration()['romSha256'],tracker)
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(selection,'preferences',snapshot.preferences))
        stack.enter_context(patch.object(original,'batches',snapshot.batches))
        stack.enter_context(patch.object(ledger_state,'read_json',tracker.read))
        stack.enter_context(patch.object(ledger_state,'sha256',tracker.hash))
        stack.enter_context(patch.object(source_dependencies,'sha256',tracker.hash))
        result=original.main();snapshot.verify();verify_pins()
    return result


if __name__=='__main__':raise SystemExit(main())
