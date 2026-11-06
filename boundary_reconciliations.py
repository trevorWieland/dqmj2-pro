import hashlib
from project import ROOT, configuration, read_json, sha256


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def identity(row):
    return row['module'], row['mode'].lower(), number(row['address']) & ~1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reconcile(candidates, modules, policies=None):
    if policies is None:
        directory = ROOT / 'evidence/regions/boundary-reconciliations'
        policies = [(path.relative_to(ROOT).as_posix(), read_json(path)) for path in sorted(directory.glob('*.json'))]
    result = [dict(row) for row in candidates]
    module_index = {(row['processor'], row['name']): row for row in modules}
    for path, policy in policies:
        require(policy['schemaVersion'] == 1 and policy['romSha256'] == configuration()['romSha256'], 'Boundary review namespace differs')
        module = module_index.get((policy['processor'], policy['module']))
        require(module is not None and module['sha256'] == policy['inputModuleSha256'], 'Boundary review module identity differs')
        binary = ROOT / module['binary']
        require(binary.resolve().is_relative_to(ROOT.resolve()), 'Boundary module path leaves repository')
        require(sha256(binary) == policy['inputModuleSha256'], 'Boundary review input module differs')
        begin, size = number(policy['address']), number(policy['bytes'])
        base = number(module['base'])
        data = binary.read_bytes()
        require(size > 0 and base <= begin and begin + size <= base + len(data), 'Boundary review span is outside module')
        require(hashlib.sha256(data[begin - base:begin - base + size]).hexdigest() == policy['inputBytesSha256'], 'Boundary review input bytes differ')
        historical = ROOT / policy['historicalReview']['path']
        require(historical.resolve().is_relative_to(ROOT.resolve()), 'Boundary review evidence leaves repository')
        require(sha256(historical) == policy['historicalReview']['sha256'], 'Historical boundary review differs')
        review = read_json(historical)
        require(review['romSha256'] == policy['romSha256'] and review['inputModuleSha256'] == policy['inputModuleSha256'], 'Historical review input identity differs')
        require(number(review['address']) == begin and review['combinedBytes'] == size and review['combinedSha256'] == policy['inputBytesSha256'], 'Historical review span differs')
        prior = policy['priorEntries']
        require(len(prior) > 1, 'Boundary merge has no absorbed entry')
        spans = sorted((number(row['address']), number(row['bytes'])) for row in prior)
        cursor = begin
        for address, length in spans:
            require(address == cursor and length > 0, 'Prior boundary extents are not contiguous')
            cursor += length
        require(cursor == begin + size, 'Boundary merge invents or loses input bytes')
        keys = {(policy['module'], policy['mode'].lower(), address) for address, length in spans}
        require(len(keys) == len(prior), 'Boundary merge repeats a prior entry')
        for address, length in spans:
            found = [row for row in result if identity(row) == (policy['module'], policy['mode'].lower(), address)]
            require(len(found) == 1 and found[0].get('size') == length, 'Prior inventory boundary differs')
        for row in result:
            if row['module'] == policy['module'] and row['mode'].lower() == policy['mode'].lower() and identity(row) not in keys:
                address, length = number(row['address']), row.get('size')
                require(length is None or not (address < begin + size and begin < address + length), 'Boundary merge overlaps another candidate')
        updated = []
        for row in result:
            if identity(row) not in keys:
                updated.append(row)
            elif number(row['address']) == begin:
                merged = dict(row, size=size, boundaryConfidence='compiler-and-native-cfg-reviewed',
                              discovery=path, boundaryReconciliation=path)
                updated.append(merged)
        require(len(updated) == len(result) - len(prior) + 1, 'Boundary merge changed an unrelated candidate')
        result = updated
    return result
