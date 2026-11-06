import sys
from project import ROOT, read_json
import stage_declared_source_package_v9_20261106 as staging


if __name__ == '__main__':
    package = 'cohort172-parallel-wave20261105-q-package.json'
    assert read_json(ROOT / package)['cohort'] == 172
    sys.argv = [sys.argv[0], package]
    staging.main()
