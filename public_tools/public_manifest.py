import hashlib
import json
import re
from pathlib import Path, PurePosixPath


class ManifestError(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def relative_file(root, name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise ManifestError("Expected a canonical repository-relative path")
    parts = PurePosixPath(name)
    if parts.is_absolute() or ".." in parts.parts or ":" in name or parts.parts[0] not in {"src", "include"}:
        raise ManifestError("Path leaves the public source root: " + name)
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ManifestError("Public source file is missing or escapes the root: " + name)
    return path


def hash_value(value, label):
    if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
        raise ManifestError("Expected a SHA-256 for " + label)
    return value


def compiler_flags(root, values):
    if not isinstance(values, list) or not values or any(not isinstance(v, str) for v in values):
        raise ManifestError("compilerFlags must be a nonempty string array")
    pairs = {
        "-Cpp_exceptions": {"off", "on"}, "-RTTI": {"off", "on"},
        "-char": {"signed", "unsigned"}, "-enum": {"int"}, "-fp": {"soft"},
        "-inline": {"off", "on", "noauto", "auto", "all", "on,noauto"},
        "-ipa": {"file", "off"}, "-lang": {"c", "c89", "c99", "c++"},
        "-msgstyle": {"gcc"}, "-opt": {"space", "speed", "all", "off"},
        "-proc": {"arm4t", "arm5TE", "arm7tdmi", "arm946e"},
        "-str": {"noreuse", "reuse"}, "-sym": {"on", "off"},
        "-w": {"off", "all", "error"},
    }
    singles = {"-gccext,on", "-gccinc", "-interworking", "-nolink", "-thumb", "-c"}
    result, directories, index = [], [], 0
    while index < len(values):
        flag = values[index]
        if flag == "-i":
            if index + 1 == len(values):
                raise ManifestError("Missing include directory")
            name = values[index + 1]
            if not name or "\\" in name or ":" in name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or PurePosixPath(name).parts[0] not in {"src", "include"}:
                raise ManifestError("Include directory must be repository relative")
            directory = (root / name).resolve()
            if not directory.is_relative_to(root) or not directory.is_dir():
                raise ManifestError("Include directory is unavailable: " + name)
            directories.append(directory)
            result.extend([flag, str(directory)])
            index += 2
        elif flag in pairs:
            if index + 1 == len(values) or values[index + 1] not in pairs[flag]:
                raise ManifestError("Unsupported compiler option value: " + flag)
            result.extend(values[index:index + 2])
            index += 2
        elif flag in singles or re.fullmatch(r"-O[0-4](?:,[ps])?", flag):
            result.append(flag)
            index += 1
        else:
            raise ManifestError("Unsupported or file-bearing compiler option: " + flag)
    return result, directories


def include_names(path):
    text = path.read_text(encoding="utf-8-sig").replace("\\\r\n", "").replace("\\\n", "")
    tokens = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*.*?\*/|//[^\n]*'
    text = re.sub(tokens, lambda m: m[0] if m[0][0] in "\"'" else re.sub(r"[^\n]", " ", m[0]), text, flags=re.S)
    if re.search(r"(?im)^\s*(?:\.incbin|INCBIN)\b", text):
        raise ManifestError("A binary include is outside ROM-free source compilation: " + str(path))
    if re.search(r'(?im)^\s*#\s*include\s+[^"<\s]', text):
        raise ManifestError("Macro-expanded includes need an explicit materialized source closure: " + str(path))
    pattern = r'(?im)^\s*(?:#\s*include|\.include)\s*(["<])([^">]+)[">]'
    return [(m[1], m[2]) for m in re.finditer(pattern, text)]


def verify(root, manifest_path):
    root = Path(root).resolve()
    path = Path(manifest_path).resolve()
    if not path.is_relative_to(root):
        raise ManifestError("The public manifest must be inside --root")
    manifest = read_json(path)
    if manifest.get("schemaVersion") != 1 or not isinstance(manifest.get("revision"), str) or not manifest["revision"]:
        raise ManifestError("Expected public accepted-source manifest schemaVersion 1 and revision")
    rom_hash = hash_value(manifest.get("romSha256"), "romSha256")
    denominator = manifest.get("initializedDenominatorBytes")
    if type(denominator) is not int or denominator <= 0:
        raise ManifestError("Expected a positive declared initialized-byte denominator")
    rows = manifest.get("functions")
    if not isinstance(rows, list) or not rows:
        raise ManifestError("Expected nonempty accepted function rows")
    pins, identities, units = {}, set(), {}
    def pin(name, expected):
        expected = hash_value(expected, name)
        file = relative_file(root, name)
        if file.suffix.lower() not in {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".s", ".asm", ".inc", ".inl"}:
            raise ManifestError("Non-source dependency in ROM-free manifest: " + name)
        if name in pins and pins[name] != expected:
            raise ManifestError("Conflicting public hashes: " + name)
        if name not in pins and digest(file) != expected:
            raise ManifestError("Public source hash mismatch: " + name)
        pins[name] = expected
        return file
    for extra in manifest.get("files", []):
        pin(extra["path"], extra["sha256"])
    for row in rows:
        if not isinstance(row, dict):
            raise ManifestError("Function rows must be objects")
        state = row.get("states", {})
        if state.get("functionMatched") is not True or state.get("moduleLinked") is not True:
            raise ManifestError("Manifest contains an unaccepted or unlinked function")
        if row.get("processor") not in {"arm7", "arm9"} or row.get("mode") not in {"arm", "thumb"}:
            raise ManifestError("Unknown CPU or instruction mode")
        if not isinstance(row.get("module"), str) or not row["module"]:
            raise ManifestError("Missing physical module namespace")
        address = int(row["address"], 0)
        identity = (row.get("program") or "", row["processor"], row["module"], row["mode"], address)
        if identity in identities or not isinstance(row.get("id"), str):
            raise ManifestError("Duplicate or incomplete accepted function identity")
        identities.add(identity)
        if row.get("buildSha256", rom_hash) != rom_hash or type(row.get("bytes")) is not int or row["bytes"] <= 0:
            raise ManifestError("Function build identity or declared extent differs")
        source = pin(row["sourceUnit"], row["sourceSha256"])
        if source.suffix.lower() not in {".c", ".cc", ".cpp", ".cxx", ".s", ".asm"}:
            raise ManifestError("Function source has an unsupported extension")
        for dependency in row.get("sourceDependencies", []):
            pin(dependency["path"], dependency["sha256"])
        compiler = hash_value(row.get("compilerSha256"), "compilerSha256")
        flags, directories = compiler_flags(root, row.get("compilerFlags"))
        key = (row["sourceUnit"], compiler, tuple(row["compilerFlags"]))
        unit = units.setdefault(key, dict(source=source, compilerSha256=compiler, flags=flags, includeDirectories=directories, rows=[]))
        unit["rows"].append(row)
    closure = set()
    for unit in units.values():
        pending, seen = [unit["source"]], set()
        while pending:
            source = pending.pop()
            if source in seen:
                continue
            seen.add(source)
            for delimiter, name in include_names(source):
                candidates = ([source.parent] if delimiter == '"' else []) + unit["includeDirectories"]
                found = None
                for directory in candidates:
                    candidate = (directory / name).resolve()
                    if not candidate.is_relative_to(root):
                        raise ManifestError("Include escapes the public root: " + name)
                    if candidate.is_file():
                        found = candidate
                        break
                if found is None:
                    raise ManifestError("Unclosed include in " + source.relative_to(root).as_posix() + ": " + name)
                relative = found.relative_to(root).as_posix()
                if relative not in pins:
                    raise ManifestError("Included source lacks a declared hash: " + relative)
                pending.append(found)
        closure.update(p.relative_to(root).as_posix() for p in seen)
    summary = dict(schemaVersion=1, status="source-integrity-passed", revision=manifest["revision"], romSha256=rom_hash,
                   manifestSha256=digest(path), acceptedFunctionsDeclared=len(rows), uniqueCompilationUnits=len(units),
                   verifiedSourceFiles=len(pins), reachedIncludeClosureFiles=len(closure),
                   acceptedInitializedBytesDeclared=manifest.get("acceptedInitializedBytes"),
                   initializedDenominatorBytesDeclared=denominator, originalInputsRead=False, compilerInvoked=False,
                   nativeMatchingVerified=False, moduleLinkingVerified=False, wholeRomVerified=False)
    if any(digest(root / name) != expected for name, expected in pins.items()):
        raise ManifestError("Source changed during integrity verification")
    return manifest, list(units.values()), pins, summary


def write_report(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
