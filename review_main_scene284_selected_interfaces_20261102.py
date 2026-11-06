import re
from project import ROOT, read_json, write_json, sha256
from slice_reference_sdk_entities_v3_20261102 import functions


def main():
    source = ROOT / 'nonmatching/main/20261102-scene284-store-paths-v2/native_main_0203db28.c'
    text = source.read_text(encoding='utf-8')
    snapshot = ROOT / 'evidence/verification/accepted-cohort144-identities-v2-20261101.json'
    selected = read_json(snapshot)['functions']
    rows = []
    for symbol in re.findall(r'extern \w+ (native_fn_\w+)\([^;]*\);', text):
        module = 'ov000' if 'ov000' in symbol else 'main'
        address = int(symbol[-8:], 16)
        matches = [r for r in selected if r['module'] == module and r['address'] == address]
        headers = []
        for match in matches:
            path = ROOT / match['source']
            assert sha256(path) == match['sourceSha256']
            body = path.read_text(encoding='utf-8')
            headers.extend(body[f['start']:f['opening']].strip() for f in functions(body)
                if f['name'].endswith(f'{address:08x}'))
        declaration = re.search(r'extern \w+ ' + symbol + r'\([^;]*\);', text).group(0)
        rows.append(dict(symbol=symbol, localDeclaration=declaration, selected=headers,
            selectedSources=[r['source'] for r in matches]))
    write_json(ROOT / 'evidence/abi/main-scene284-selected-interface-review-20261102.json',
        dict(sourceCredit=0, sourceSha256=sha256(source), snapshotSha256=sha256(snapshot), rows=rows,
            interfaceClosureComplete=False))
    print('\n'.join(str(r) for r in rows))


if __name__ == '__main__':
    main()
