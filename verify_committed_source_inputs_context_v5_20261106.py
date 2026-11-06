import subprocess
from project import ROOT
import verify_committed_source_inputs_context_v4_20261106 as original
from itcm_reset_source_audit_route_v1_20261106 import route


def main():
    for name in ['verify_committed_source_inputs_context_v5_20261106.py',
                 'itcm_reset_source_audit_route_v1_20261106.py', 'qualify_itcm_reset_reference_v1_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    with route():
        original.main()


if __name__ == '__main__':
    main()
