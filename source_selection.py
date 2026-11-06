from project import ROOT, read_json, sha256

POLICY = ROOT / 'source-preferences.json'
FIELDS = ('source', 'sourceSha256', 'report')


def local(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError('Source preference escapes the private repository')
    return path


def preferences(namespace, path=POLICY):
    if not path.is_file():
        return {}
    document = read_json(path)
    if document['schemaVersion'] != 1 or document['romSha256'] != namespace:
        raise ValueError('Source preference build namespace differs')
    result = {}
    for row in document['preferences']:
        address = int(row['address'], 0)
        key = row['module'], row['mode'], address
        if row['processor'] != 'arm9' or row['mode'] not in ('arm', 'thumb') or address % (4 if row['mode'] == 'arm' else 2):
            raise ValueError('Source preference processor/mode/alignment differs')
        if key in result:
            raise ValueError('Duplicate source preference identity')
        evidence = local(row['evidence'])
        if sha256(evidence) != row['evidenceSha256']:
            raise ValueError('Source preference migration evidence changed')
        audit = read_json(evidence)
        identity = {name: row[name] for name in ('processor', 'module', 'mode', 'address', 'bytes', 'targetSha256')}
        if audit['romSha256'] != namespace or audit['identity'] != identity or audit['preferred'] != {name: row[name] for name in FIELDS}:
            raise ValueError('Source preference migration identity differs')
        if not audit['originalSourceUnchanged'] or not audit['nativeBytesUnchanged'] or audit['newFunctionCredit'] or audit['newByteCredit']:
            raise ValueError('Source preference migration scope differs')
        for version in (audit['previous'], audit['preferred']):
            if sha256(local(version['source'])) != version['sourceSha256']:
                raise ValueError('Source preference frozen source changed')
            local(version['report'])
        if audit['previous']['source'] == audit['preferred']['source']:
            raise ValueError('Source preference does not retain a separate historical implementation')
        result[key] = row
    return result


def preferred(unit, policy):
    return unit is not None and all(unit.get(field) == policy[field] for field in FIELDS)


def choose(previous, candidate, policy=None):
    candidate.setdefault('alternativeImplementations', [])
    if previous is None:
        return candidate
    if previous['size'] != candidate['size']:
        raise ValueError('Accepted source variants disagree on function extent')
    if policy and preferred(previous, policy):
        selected, alternative = previous, candidate
    else:
        selected, alternative = candidate, previous
    selected['alternativeImplementations'] = previous.get('alternativeImplementations', []) + [
        {key: alternative[key] for key in (*FIELDS, 'object', 'objectSha256')}]
    return selected


def enforce(matches, rejected, policies):
    for key, policy in policies.items():
        unit = matches.get(key)
        if not preferred(unit, policy):
            matches.pop(key, None)
            rejected.append({'report': policy['report'], 'reason': 'Preferred source/object is not freshly available',
                             'source': policy['source'], 'historicalVariantFallbackAllowed': False})
            continue
        if unit.get('processor', 'arm9') != policy['processor'] or unit['size'] != policy['bytes'] or unit.get('targetSha256') != policy['targetSha256']:
            raise ValueError('Preferred source native span differs')
        unit['sourceSelection'] = {'policy': 'explicit-hash-qualified-primary', 'evidence': policy['evidence'],
                                   'evidenceSha256': policy['evidenceSha256'], 'newByteCredit': 0}
