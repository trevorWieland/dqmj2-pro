import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT


def main():
    commands = ['probe_windows_target_layout_20261101.py', 'probe_arm7_target_layout_20261101.py',
        'compile_windows_source_census111_targetabi_v2_20261101.py',
        'reconcile_windows_targetabi_census111_v4_20261101.py']
    for command in commands:
        run = subprocess.run([sys.executable, str(ROOT / command)], cwd=ROOT)
        if run.returncode:
            raise SystemExit(run.returncode)


if __name__ == '__main__':
    main()
