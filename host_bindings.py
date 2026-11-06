import re


def apply_typed_bindings(units):
    from link_runtime_unit import measured_module, verify_binding
    renamed = {(unit["module"], old): new for unit in units for old, new in unit.get("symbols", {}).items()}
    configurations = {}
    for unit in units:
        bindings = unit.pop("typedNativeBindings", {})
        if not bindings:
            continue
        resolved = {}
        for name, binding in bindings.items():
            if binding.get("kind") != "function":
                continue
            target = verify_binding(name, binding)
            module, mode = binding["module"], binding["mode"]
            if binding.get('alternateEntryEvidence'):
                from native_alternate_entries import verify
                proof = verify(name, binding)
                resolved[name] = {**binding, **proof, 'address': binding['address'], 'linkedNativeSymbol': name}
                continue
            if module not in configurations:
                metadata, native, symbols = measured_module(module)
                configurations[module] = metadata, symbols
            metadata, symbols = configurations[module]
            pattern = r"^(\S+) kind:function\(" + mode + r",size=0x[0-9a-f]+\) addr:0x" + f"{target:08x}" + r"$"
            matches = re.findall(pattern, symbols, re.M)
            if len(matches) != 1:
                raise ValueError("Typed target does not have one qualified configured native entry")
            original = matches[0]
            actual = renamed.get((module, original), original)
            resolved[name] = {**binding, "configuredNativeSymbol": original, "linkedNativeSymbol": actual, "inputModuleSha256": metadata["sha256"], "calleeSourceCredit": 0}
        aliases = unit.setdefault("relocationAliases", {})
        for relocation in unit.pop("typedBindingRelocations", []):
            if relocation["symbol"] not in resolved:
                continue
            if resolved[relocation['symbol']].get('alternateEntryEvidence'):
                continue
            if relocation["type"] not in (1, 2, 10, 15, 28, 29):
                raise ValueError("Unsupported genuine function relocation")
            aliases[str(relocation["offset"])] = resolved[relocation["symbol"]]["linkedNativeSymbol"]
        unit["typedFunctionBindings"] = resolved
    return units
