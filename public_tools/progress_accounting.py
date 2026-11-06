import argparse
import hashlib
import json
from pathlib import Path


def accounting(root):
    function_path = root / 'public/accepted-functions.json'
    data_path = root / 'public/accepted-data.json'
    functions = json.loads(function_path.read_text(encoding='utf-8'))
    data = json.loads(data_path.read_text(encoding='utf-8'))
    if data['buildSha256'] != functions['romSha256']:
        raise ValueError('Function and data snapshots name different builds')
    if any(r['states'].get('functionMatched') is not True or r['states'].get('moduleLinked') is not True for r in functions['functions']):
        raise ValueError('Unaccepted function in the closed source snapshot')
    if any(r['states'].get('dataMatched') is not True or r['states'].get('moduleLinked') is not True for r in data['records']):
        raise ValueError('Unaccepted data in the closed source snapshot')
    code_bytes = sum(r['bytes'] for r in functions['functions'])
    data_bytes = sum(r['storedBytes'] for r in data['records'] if r['kind'] != 'bss')
    total = functions['acceptedInitializedBytes']
    denominator = functions['initializedDenominatorBytes']
    other = total - code_bytes - data_bytes
    if not 0 <= code_bytes + data_bytes <= total <= denominator or other not in {0, 24}:
        raise ValueError('Closed initialized accounting does not reconcile; review qualified alignment separately')
    return dict(schemaVersion=1, sourceSnapshotRevision=functions['revision'],
                functionManifestSha256=hashlib.sha256(function_path.read_bytes()).hexdigest(),
                dataManifestSha256=hashlib.sha256(data_path.read_bytes()).hexdigest(),
                acceptedFunctions=len(functions['functions']), acceptedFunctionBytes=code_bytes,
                acceptedDataInitializedBytes=data_bytes, separatelyAcceptedAlignmentBytes=other,
                acceptedInitializedBytes=total, initializedDenominatorBytes=denominator,
                initializedSourcePercent=total * 100 / denominator,
                scope='Closed accepted native initialized-source coverage; code, data and qualified alignment. BSS and interpreted scripts are excluded.',
                bytematchScope='ByteMatch reports measured function code separately. Its code percentage uses a different denominator.',
                sourceOnlyRomProven=functions['sourceOnlyRomProven'])


def outputs(value):
    percent = f"{value['initializedSourcePercent']:.2f}%"
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="209" height="20" role="img" '
           f'aria-label="Initialized source: {percent}">'
           '<title>Closed accepted native initialized-source coverage</title>'
           '<rect width="147" height="20" fill="#555"/>'
           '<rect x="147" width="62" height="20" fill="#007ec6"/>'
           '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">'
           '<text x="73.5" y="14">Initialized source</text>'
           f'<text x="178" y="14">{percent}</text></g></svg>\n')
    return {'public/native-progress.json': json.dumps(value, indent=2) + '\n', 'public/native-progress.svg': svg}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    value = accounting(root)
    for name, content in outputs(value).items():
        path = root / name
        if args.write:
            path.write_text(content, encoding='utf-8')
        elif not path.is_file() or path.read_text(encoding='utf-8') != content:
            raise ValueError('Progress badge/accounting is stale: ' + name)
    print(json.dumps({key: value[key] for key in ('acceptedInitializedBytes', 'initializedDenominatorBytes', 'initializedSourcePercent')}))


if __name__ == '__main__':
    main()
