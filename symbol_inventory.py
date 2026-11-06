import re
from project import ROOT, configuration, sha256, write_json


def augment(candidates, modules, write=True):
    known = {(row['module'], row['mode'].lower(), int(row['address'], 0) & ~1): row for row in candidates}
    added, census = [], []
    pattern = re.compile(r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)(.*)\) addr:(0x[0-9a-f]+)$', re.M)
    for module in modules:
        if module.get('processor') != 'arm9' or module.get('program') or not module.get('symbolsFile'):
            continue
        path = ROOT / module['symbolsFile']
        text = path.read_text()
        config_hash = sha256(path)
        declared = [line for line in text.splitlines() if ' kind:function(' in line]
        matches = list(pattern.finditer(text))
        if len(declared) != len(matches):
            raise ValueError('Unparsed canonical function declarations: ' + module['name'])
        base = int(module['base'], 0)
        rows = []
        for match in matches:
            name, mode, size_text, attributes, address_text = match.groups()
            size, address = int(size_text, 0), int(address_text, 0)
            if not size or address & 1 or address < base or address + size > base + module['bytes']:
                raise ValueError('Canonical function extent lies outside its measured module')
            if attributes and not attributes.startswith(',dsprot='):
                raise ValueError('Unclassified canonical function attributes')
            key = module['name'], mode, address
            row = {'module': module['name'], 'processor': 'arm9', 'mode': mode, 'address': hex(address), 'size': size,
                   'symbol': name, 'boundaryConfidence': 'heuristic-ds-decomp-protection-metadata' if attributes else 'heuristic-ds-decomp',
                   'discovery': path.relative_to(ROOT).as_posix(), 'symbolConfigSha256': config_hash, 'protectionMetadata': attributes.removeprefix(',dsprot=') or None}
            if key in known:
                previous_size = known[key].get('size')
                if previous_size is not None and previous_size != size:
                    raise ValueError('Canonical and imported function extents disagree')
            else:
                known[key] = row
                added.append(row)
            rows.append(row)
        census.append({'module': module['name'], 'moduleInputSha256': module['sha256'], 'symbols': path.relative_to(ROOT).as_posix(),
                       'symbolConfigSha256': config_hash, 'canonicalFunctions': len(rows), 'protectionAnnotatedFunctions': sum(bool(row['protectionMetadata']) for row in rows),
                       'functions': rows})
    report = {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'source': 'symbol_inventory.py', 'sourceSha256': sha256(ROOT / 'symbol_inventory.py'), 'canonicalModules': census, 'additionalCandidates': added,
              'additionalCandidateCount': len(added), 'acceptedSourceFunctions': 0, 'sourceMatchedBytes': 0,
              'limitations': ['Canonical symbol declarations supply analysis candidates, not verified original boundaries or recovered source',
                              'DSProtect annotations describe the extraction analysis view; runtime transformations and reconstructed protected code need separate evidence']}
    if write:
        write_json(ROOT / 'evidence/regions/canonical-symbol-functions.json', report)
    return candidates + added
