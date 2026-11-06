from project import ROOT,sha256
import oracle_source_closure_20261031 as legacy
import oracle_source_closure_v3_20261106 as optimized
import stage_declared_source_package_v7_20261102 as previous
PINS={
    'oracle_source_closure_20261031.py':'0ec035a656951c7a6175c019a7a547d1c3ab96ecc91332e9eab72c152a3fafdb',
    'oracle_source_closure_v2_20261106.py':'f4b070a006e0c2ec6010876a086843bf16be3e52c1915e2cc23eeb971b452eb5',
    'oracle_source_closure_v3_20261106.py':'f338d521c95d210eb87b5aa2ec7795c96e911ef12f8676be7e31b86d3c068d55',
    'collector_path_lookup_epoch_20261106.py':'33bdd30e2a341c099ef2237182b9131be0b7c16510c8c2b2e72d3633457973d4',
    'stage_declared_source_package_v7_20261102.py':'55a89a196380c5e82883b9dc2eae57cdbaeda87f163da377eccede1bf1c25355',
    'stage_verified_cohort.py':'fd8965a28d8b04d2d6fe760a363b538790ec010824dcd6f43f66cf840e25e416'
}


def main():
    if {name:sha256(ROOT/name) for name in PINS}!=PINS:raise ValueError('Qualified source staging/collector/lookup code identity changed')
    original=legacy.collect;legacy.collect=optimized.collect
    try:return previous.main()
    finally:legacy.collect=original


if __name__=='__main__':raise SystemExit(main())
