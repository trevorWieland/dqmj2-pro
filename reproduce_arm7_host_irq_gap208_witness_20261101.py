import json
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256

PINS = {'prove_arm7_host_irq_gap208_scope_20261101.py': '23f81318bf55d50cfe6f14f7c00f94c29f8aaec7b34d765bb85ef8412d09e752', 'arm7_host_irq_gap208_native_20261101.py': '4dfbd205fa06489438a203fa353ceca8c5db920c497a9665e50952af1ae168e5', 'arm7_host_irq_gap208_native_engine_20261101.py': 'b934a379f89aaeceb5689ed1579b08e87cb08ef7356c2c4e8be4888326f2cea7', 'validate_arm7_host_irq_gap208_scope_20261101.py': '1003bca11b1b0c9494d11dcdc12acb5726d04493a69f6dad92bb19232318fd65', 'prove_arm7_host_irq_fixed_words_20261101.py': '1b79a45432218a8d3ebf6519a931e784359bf2191747cf154d43be839297bb9e', 'validate_arm7_host_irq_fixed_words_20261101.py': '937811fd288e594b2f46e4e794f268b0be37ad2a112a28d9182fd57d931ea4a9'}
PRODUCTS = {'evidence/attempts/arm7-host-irq-gap208-scope-20261101.json': 'c20ef9849e78bd244d45c12377e52b0b53463e58d5dd7ca934b8f2da5d05400c', 'evidence/verification/arm7-host-irq-gap208-scope-controls-20261101.json': '446fd4bd490815a821dc778aec6a336976632595333bcf956c9bfdc8afc9f64e', 'evidence/attempts/arm7-host-irq-fixed-words-20261101.json': 'ec649faaeb2ab335b4c1fae92d775a1197b7c0683f4db2b1d1311885e6bf946e', 'evidence/verification/arm7-host-irq-fixed-words-controls-20261101.json': '51960c8598f6fe77b6bed21f8fdeca9741fc781d95278fbd4dbb374fa014edaf'}
SCRIPTS = ('prove_arm7_host_irq_gap208_scope_20261101.py','validate_arm7_host_irq_gap208_scope_20261101.py',
    'prove_arm7_host_irq_fixed_words_20261101.py','validate_arm7_host_irq_fixed_words_20261101.py')


def main():
    for path,expected in PINS.items():
        if sha256(ROOT/path)!=expected:raise ValueError('Frozen read-only IRQ witness code changed: '+path)
    logs=ROOT/'work/arm7-bulk-20261030/lane-host-irq-gap208-native/replay-logs'
    logs.mkdir(parents=True,exist_ok=True)
    for script in SCRIPTS:
        run=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True,timeout=300)
        (logs/(script+'.stdout.txt')).write_text(run.stdout)
        (logs/(script+'.stderr.txt')).write_text(run.stderr)
        if run.returncode:raise ValueError('Frozen IRQ witness child failed: '+script+' '+run.stderr)
    for path,expected in PRODUCTS.items():
        if sha256(ROOT/path)!=expected:raise ValueError('Frozen IRQ witness product changed: '+path)
    print(json.dumps(dict(reports=PRODUCTS,negativeControls=71,sourceCredit=0,initializedDenominatorDelta=0)),flush=True)


if __name__=='__main__':main()
