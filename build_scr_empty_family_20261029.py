import argparse
import hashlib
import json
import sys
from pathlib import Path

import scr_c_compiler_20261029_v3 as compiler


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--targets', required=True)
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    source, targets = Path(options.source).resolve(), Path(options.targets).resolve()
    declarations = json.loads(targets.read_text())
    outputs = []
    closure = None
    identities = set()
    for target in declarations:
        identity = (target['scriptSha256'], target['startPc'])
        if identity in identities:
            raise ValueError('Duplicate qualified target')
        identities.add(identity)
        body, report = compiler.compile_source(source, target['startPc'], 0)
        assert len(body) == 16 and not report['variableAllocations'] and not report['namedApiCalls']
        candidate = {key: report[key] for key in ('sourceSha256', 'includeSha256', 'compilerSha256', 'parserDependency')}
        if closure is None:
            closure = candidate
        else:
            assert candidate == closure
        outputs.append({'scriptSha256': target['scriptSha256'], 'startPc': target['startPc'],
                        'bodyHex': body.hex(), 'bytes': 16, 'sha256': digest(body),
                        'sourceFunction': report['function'], 'sourceDefinitionFamily': 'empty-void-SCR-entry'})
    result = {'schemaVersion': 1, 'sourceClosure': closure, 'targetsSha256': digest(targets.read_bytes()),
              'generatorSha256': digest(Path(__file__).read_bytes()), 'pythonVersion': sys.version,
              'compiledInstances': outputs, 'newAuthoredImplementationFamilies': 0,
              'originalBytecodeCompilerInput': False}
    output = Path(options.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'instances': len(outputs), 'qualifiedBytes': len(outputs) * 16, 'newImplementationFamilies': 0}))


if __name__ == '__main__':
    main()
