import subprocess
import sys
from project import ROOT
import prove_arm7_child_divide_scope_20261031
import validate_arm7_child_divide_scope_20261031


def main():
    for producer in ['prove_arm7_child_divide_scope_20261031.py', 'validate_arm7_child_divide_scope_20261031.py']:
        subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
