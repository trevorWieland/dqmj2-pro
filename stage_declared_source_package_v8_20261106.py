from project import ROOT,sha256
import oracle_source_closure_20261031 as legacy
import oracle_source_closure_v2_20261106 as optimized
import stage_declared_source_package_v7_20261102 as previous
PINS={
    'oracle_source_closure_20261031.py':'0ec035a656951c7a6175c019a7a547d1c3ab96ecc91332e9eab72c152a3fafdb',
    'oracle_source_closure_v2_20261106.py':'f4b070a006e0c2ec6010876a086843bf16be3e52c1915e2cc23eeb971b452eb5',
    'stage_declared_source_package_v7_20261102.py':'55a89a196380c5e82883b9dc2eae57cdbaeda87f163da377eccede1bf1c25355',
    'stage_verified_cohort.py':'fd8965a28d8b04d2d6fe760a363b538790ec010824dcd6f43f66cf840e25e416'
}


def main():
    if {name:sha256(ROOT/name) for name in PINS}!=PINS:raise ValueError('Qualified source staging/collector code identity changed')
    original=legacy.collect;legacy.collect=optimized.collect
    try:previous.main()
    finally:legacy.collect=original


if __name__=='__main__':main()
