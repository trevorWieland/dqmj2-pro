import argparse
import hashlib
import json
from pathlib import Path

import scr_c_compiler_20261029_v4 as compiler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--layout', required=True)
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    layout = Path(options.layout).resolve()
    units = json.loads(layout.read_text())
    products = []
    for unit in units:
        source = layout.parent / unit['sourceName']
        body, report = compiler.compile_source(source, unit['startPc'], unit['allocation'])
        assert not report['generatedBranches']
        products.append({'scriptSha256': unit['scriptSha256'], 'startPc': unit['startPc'],
            'sourceName': unit['sourceName'], 'bodyHex': body.hex(), 'sha256': hashlib.sha256(body).hexdigest(),
            'bytes': len(body), 'compilerReport': report})
    Path(options.output).write_text(json.dumps({'products': products,
        'generatorSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'layoutSha256': hashlib.sha256(layout.read_bytes()).hexdigest(), 'originalBytecodeCompilerInput': False}, indent=2) + '\n')
    print(json.dumps({'compiledUnits': len(products), 'compiledBytes': sum(p['bytes'] for p in products)}))


if __name__ == '__main__':
    main()
