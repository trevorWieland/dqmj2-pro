import hashlib
from project import ROOT, configuration, read_json, sha256


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def require(value, message):
    if not value:
        raise ValueError(message)


def identity(row):
    return row.get('program', ''), row['processor'], row['module'], row['mode'].lower(), number(row['address'])


def pinned(row):
    path = (ROOT / row['path']).resolve()
    require(path.is_relative_to(ROOT.resolve()), 'Discontiguous evidence leaves repository')
    require(path.is_file() and sha256(path) == row['sha256'], 'Discontiguous evidence hash differs')
    return read_json(path)


def reconcile(candidates, modules, policies=None):
    if policies is None:
        directory = ROOT / 'evidence/regions/discontiguous-boundaries'
        policies = [(p.relative_to(ROOT).as_posix(), read_json(p)) for p in sorted(directory.glob('*.json'))]
    result = [dict(row) for row in candidates]
    for path, policy in policies:
        require(policy['schemaVersion'] == 1 and policy['kind'] == 'reviewed-discontiguous-function', 'Discontiguous schema differs')
        require(policy['romSha256'] == configuration()['romSha256'], 'Discontiguous build namespace differs')
        key = identity(policy)
        require(key == ('', 'arm7', 'arm7-wram', 'arm', 0x037FFF54), 'Unreviewed discontiguous function identity')
        require(policy['coordinatorReviewPassed'] is True, 'Discontiguous coordinator review absent')
        require((policy['bytes'], policy['codeBytes'], policy['literalBytes'], policy['priorInstructionBytes'], policy['newlyConfirmedCodeBytes'], policy['additionalInitializedModuleBytes']) == (352, 344, 8, 280, 64, 0), 'Discontiguous exact code/pool accounting differs')
        module = next((m for m in modules if m['processor'] == key[1] and m['name'] == key[2]), None)
        require(module is not None and module['sha256'] == policy['inputModuleSha256'], 'Discontiguous module namespace differs')
        binary_path = (ROOT / module['binary']).resolve()
        require(binary_path.is_relative_to(ROOT.resolve()) and sha256(binary_path) == policy['inputModuleSha256'], 'Discontiguous measured module differs')
        raw = binary_path.read_bytes()
        start = key[4] - number(module['base'])
        require(0 <= start and start + 352 <= len(raw), 'Discontiguous span outside module')
        require(hashlib.sha256(raw[start:start + 352]).hexdigest() == policy['inputBytesSha256'], 'Discontiguous input span differs')
        inventory = pinned(policy['originalRawInventory'])
        original = next((r for r in inventory['functions'] if r['module'] == key[2] and number(r['address']) == key[4]), None)
        require(original is not None and original['bodyBytes'] == 280 and original['ranges'] == [['0x37fff54', '0x3800000'], ['0x3800040', '0x38000ac']], 'Original discontiguous raw row differs')
        evidence = [pinned(row) for row in policy['reviewEvidence']]
        require(len(evidence) == 5, 'Discontiguous proof closure is incomplete')
        loader, consumers, roles, caller, controls = evidence
        require(loader['configuredFunction'] == original and loader['candidate']['spanSha256'] == policy['inputBytesSha256'], 'Original loader/code ownership review differs')
        require(not consumers['configuredOverlapConflicts'] and not consumers['additionalConfiguredRootsInsideCodeOrPool'], 'Discontiguous entry conflict remains')
        require(len(roles['roles']) == 10 and roles['knownPcRelativeDataReadsAddressingSpecificOpcodeWords'] == [], 'Specific instruction role/data use review differs')
        require(caller['actualNativeAndCompiledReturns'] == 790 and caller['actualSeparatelyObservedNestedReturns'] == 211774 and caller['sourceAcceptanceCredit'] == 0, 'Independent caller proof differs')
        require(len(controls['controls']) == 36 and controls['allPassed'], 'Discontiguous rejection controls failed')
        found = [r for r in result if identity(r) == key]
        require(len(found) == 1 and found[0] == policy['originalCandidate'], 'Prior canonical candidate changed or repeated')
        begin, end = key[4], key[4] + 352
        for row in result:
            if row['module'] != key[2] or row['processor'] != key[1] or identity(row) == key:
                continue
            address = number(row['address'])
            length = row.get('size')
            require(not begin < address < end, 'Additional function root inside reviewed span')
            require(length is None or not address < end or not begin < address + length, 'Discontiguous span overlaps another known function')
        revised = dict(found[0], size=352, instructionBodyBytes=344, bodyRanges=[[hex(begin), hex(begin + 344)]],
                       boundaryVerified=True, boundaryConfidence='compiler-native-cfg-and-loader-reviewed',
                       originalBoundaryEvidence=found[0]['evidence'], boundaryReconciliation=path, discovery=path,
                       generatedLiteralBytes=8, priorInstructionBodyBytes=280, newlyAnalyzedInstructionBytes=64)
        result = [revised if identity(row) == key else row for row in result]
    return result
