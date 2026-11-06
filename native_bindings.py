import re
from functools import lru_cache
from project import ROOT, read_json


@lru_cache(maxsize=1)
def main_thumb_targets():
    symbols = (ROOT / "config/arm9/symbols.txt").read_text()
    return {int(value, 0) for value in re.findall(r"^\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:(0x[0-9a-f]+)$", symbols, re.M)}


@lru_cache(maxsize=8)
def overlay_thumb_targets(module):
    if not re.fullmatch(r"ov\d{3}", module):
        raise ValueError("Unqualified overlay mode namespace")
    path = ROOT / "config/arm9/overlays" / module / "symbols.txt"
    symbols = path.read_text()
    return {int(value, 0) for value in re.findall(r"^\S+ kind:function\(thumb,size=0x[0-9a-f]+[^\n]*\) addr:(0x[0-9a-f]+)$", symbols, re.M)}


def canonical_target(name, value):
    address = int(value, 0) if isinstance(value, str) else value
    if not name.startswith(("native_fn_", "func_")) or not name.endswith(f"{address & ~1:08x}"):
        return hex(address)
    if address & ~1 in main_thumb_targets():
        return hex(address & ~1)
    overlay = re.match(r"(?:native_fn_|func_)(ov\d{3})_", name)
    if overlay and address & ~1 in overlay_thumb_targets(overlay[1]):
        return hex(address & ~1)
    return hex(address)


def merge_target(bindings, name, value):
    value = canonical_target(name, value)
    if name in bindings and canonical_target(name, bindings[name]) != value:
        raise ValueError("Inconsistent native symbol target: " + name)
    bindings[name] = value


def scoped_bindings(paths):
    reports = {path: read_json(path) for path in paths}
    identities = {}
    for report in reports.values():
        for name, value in report.get("nativeSymbols", {}).items():
            scope = report.get("nativeSymbolModules", {}).get(name)
            identities.setdefault(name, set()).add((scope, canonical_target(name, value)))
    result = {}
    for path, report in reports.items():
        aliases = {}
        for name, value in report.get("nativeSymbols", {}).items():
            if len(identities[name]) < 2:
                continue
            scope = report.get("nativeSymbolModules", {}).get(name, report.get("module", "main"))
            scope = re.sub(r"[^A-Za-z0-9_]", "_", scope)
            aliases[name] = f"__binding_{scope}_{int(value, 0):08x}_{name}"
        result[path] = aliases
    return result
