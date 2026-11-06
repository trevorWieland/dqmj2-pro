from project import ROOT, sha256


def consolidate(units, policies=None):
    policies = policies or {}

    def policy_for(unit):
        return policies.get((unit['module'], unit.get('mode'), int(unit['start'], 0)))

    def preferred(unit, policy):
        return all(unit.get(field) == policy[target] for field, target in
                   [('source', 'source'), ('sourceSha256', 'sourceSha256'), ('sourceReport', 'report')])

    selected = {}
    for unit in units:
        key = (unit["module"], unit.get("section", ".text"), int(unit["start"], 0), int(unit["end"], 0))
        previous = selected.get(key)
        if previous:
            if unit.get("mode") != previous.get("mode") or unit.get("kind") != previous.get("kind"):
                raise ValueError("Overlapping source implementations disagree on region identity")
            if not unit.get("targetSha256") or unit["targetSha256"] != previous.get("targetSha256"):
                raise ValueError("Equivalent source implementations need identical measured target hashes")
            for candidate in (previous, unit):
                if sha256(ROOT / candidate["source"]) != candidate["sourceSha256"] or sha256(ROOT / candidate["object"]) != candidate["sha256"]:
                    raise ValueError("Equivalent source implementation is stale")
            policy = policy_for(unit)
            chosen, other = (previous, unit) if policy and preferred(previous, policy) else (unit, previous)
            alternatives = previous.get("equivalentUnlinkedImplementations", []) + unit.get("equivalentUnlinkedImplementations", [])
            alternate = {key: value for key, value in other.items() if key != "equivalentUnlinkedImplementations"}
            chosen["equivalentUnlinkedImplementations"] = alternatives + [alternate]
            unit = chosen
        selected[key] = unit
    for unit in selected.values():
        policy = policy_for(unit)
        if policy:
            if not preferred(unit, policy):
                raise ValueError('Preferred source implementation absent from module inputs')
            if unit.get('processor', 'arm9') != policy['processor'] or int(unit['end'], 0) - int(unit['start'], 0) != policy['bytes'] or unit.get('targetSha256') != policy['targetSha256']:
                raise ValueError('Preferred module source native span differs')
            if sha256(ROOT / unit['source']) != unit['sourceSha256'] or sha256(ROOT / unit['object']) != unit['sha256']:
                raise ValueError('Preferred module source/object is stale')
    return list(selected.values())
