import argparse
import json
import subprocess
import sys
from pathlib import Path
from project import ROOT, now, read_json, sha256, write_json


def validation_timeout(command):
    limits = {'integrate.py': 960, 'validate_evidence.py': 1800,
              'match_scr_world32_20261030_batch09.py': 1800,
              'match_scr_context_words_20261030_batch13.py': 1800,
              'match_scr_byte_modes_20261030_batch14.py': 1800,
              'match_scr_world32_source_closure_20261030_batch16.py': 1800}
    return limits.get(command[0], 600)


def oracle_commands(accepted_oracles, interpreted_batches):
    commands = []
    pending = [batch['reproduce'] for batch in interpreted_batches]
    for oracle in accepted_oracles:
        if oracle['reproduce'][0] == 'verify_interpreted_inventory.py':
            commands.extend(pending)
            pending = []
        commands.append(oracle['reproduce'])
    if pending:
        raise ValueError('Interpreted source replay requires its inventory-validation stage')
    return commands


def interpreted_pins_current(batches):
    return all((ROOT / path).is_file() and sha256(ROOT / path) == expected
               for batch in batches for path, expected in batch['sourceHashes'].items())


def replay_entrypoints(commands, root=ROOT):
    root = root.resolve()
    missing = []
    checked = set()
    for command in commands:
        path = (root / command[0]).resolve()
        if not path.is_relative_to(root) or path.suffix != '.py':
            raise ValueError('Unsafe replay entrypoint: ' + command[0])
        name = path.relative_to(root).as_posix()
        checked.add(name)
        if not path.is_file():
            missing.append(name)
    return {'checkedEntrypoints': len(checked), 'missingEntrypoints': sorted(set(missing)), 'passed': not missing}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--tools", action="store_true")
    args = parser.parse_args()
    report = {"schemaVersion": 1, "createdUtc": now(), "steps": [], "sourceReconstructionComplete": False}
    from recovery_registry import batches, oracles, verify_sources, ROOT as source_root
    from recovery_order import order_batches
    try:
        from bootstrap_runtime_inputs_parallel_wave20261102 import materialize
        report['runtimeInputBootstrap'] = materialize(source_root)
        verify_sources()
    except Exception as error:
        report.update(allChecksPassed=False, buildAndOracleChecksPassed=False, state='failed-source-input-preflight',
            failure=f'{type(error).__name__}: {error}')
        write_json(ROOT / 'evidence/verification/checks.json', report)
        raise
    registry_hash = sha256(ROOT / "recovery.json")
    preference_path = ROOT / 'source-preferences.json'
    preference_hash = sha256(preference_path) if preference_path.is_file() else None
    report['sourcePreferenceSha256'] = preference_hash
    accepted_batches, accepted_oracles = batches(), oracles()
    interpreted_registry = ROOT / 'interpreted-recovery.json'
    interpreted_hash = sha256(interpreted_registry) if interpreted_registry.is_file() else None
    interpreted_batches = read_json(interpreted_registry)['batches'] if interpreted_hash else []
    if not interpreted_pins_current(interpreted_batches):
        raise ValueError('Accepted interpreted source/compiler changed before replay')
    report.update(interpretedRegistrySha256=interpreted_hash, interpretedSourceBatches=interpreted_batches)
    report.update(recoveryRegistrySha256=registry_hash, sourceBatches=accepted_batches, oracleScope=accepted_oracles)
    ordered = order_batches(accepted_batches, details=True)
    write_json(ROOT / "evidence/verification/recovery-order.json", ordered)
    commands = [["utility_runtime.py"], ["utility_runtime.py", "--verify"], ["arm7_runtime.py"], ["arm7_runtime.py", "--verify"]]
    commands += [batch["reproduce"] for batch in ordered["batches"]]
    commands += oracle_commands(accepted_oracles, interpreted_batches)
    commands = [list(command) for command in dict.fromkeys(tuple(command) for command in commands)]
    commands += [["evidence/save/native_getters.py", "--rom", str(ROOT / "inputs/game.nds"), "--save", str(ROOT / "inputs/save.sav"), "--deps", str(ROOT / "deps/native"), "--output", str(ROOT / "evidence/save/native-getter-results.json")], ["evidence/save/static_paths.py"]]
    if args.tools:
        commands.append(["install_tools.py", "--verify"])
        commands.append(["validate_compiler_archive.py"])
        commands.append(["validation_tools.py"])
    build = ["integrate.py"]
    if args.clean:
        build.append("--clean")
    auxiliary = ["link_utility.py", "--clean"] if args.clean else ["link_utility.py"]
    commands += [["link_arm7.py"], auxiliary, build, ["verify_linker_layout.py"], ["rom_layout.py", "--compare", str(ROOT / "build/link-work/roundtrip.nds")], ["pack_exact.py", "--prepare", "--linked-rom", str(ROOT / "build/link-work/roundtrip.nds")], ["validate_packaging.py"], ["make_manifest.py"], ["audit_boundaries.py"], ["make_manifest.py"], ["validate_evidence.py"], ["verify_workspace.py"]]
    if preference_hash:
        commands.insert(commands.index(['audit_boundaries.py']), ['verify_linked_preferences.py'])
    report['entrypointPreflight'] = replay_entrypoints(commands)
    if not report['entrypointPreflight']['passed']:
        report.update(allChecksPassed=False, buildAndOracleChecksPassed=False, state='failed-entrypoint-preflight')
        write_json(ROOT / 'evidence/verification/checks.json', report)
        raise ValueError('Replay scripts are missing: ' + ', '.join(report['entrypointPreflight']['missingEntrypoints']))
    logs = ROOT / "logs/checks"
    logs.mkdir(parents=True, exist_ok=True)
    failed = False
    for index, command in enumerate(commands):
        argv = [sys.executable, str(ROOT / command[0]), *command[1:]]
        output = logs / f"{index:02d}-{Path(command[0]).stem}.txt"
        timeout = validation_timeout(command)
        try:
            result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, errors="replace", timeout=timeout)
            text = result.stdout + result.stderr
            row = {"command": argv, "exitCode": result.returncode, "log": output.relative_to(ROOT).as_posix()}
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            text = f"{type(error).__name__}: {error}"
            row = {"command": argv, "exitCode": -1, "log": output.relative_to(ROOT).as_posix(), "failure": text}
        row['deadlineSeconds'] = timeout
        output.write_text(text, encoding="utf-8")
        report["steps"].append(row)
        print(json.dumps({"script": command[0], "exitCode": row["exitCode"]}), flush=True)
        changed_scope = [name for name, expected in [('recovery.json', registry_hash),
            ('source-preferences.json', preference_hash), ('interpreted-recovery.json', interpreted_hash)]
            if (sha256(ROOT / name) if (ROOT / name).is_file() else None) != expected]
        if changed_scope:
            report['scopeChangedDuringReplay'] = changed_scope
            failed = True
            break
        if row["exitCode"]:
            failed = True
            if command[0] != "verify_workspace.py":
                break
    report["recoveryRegistryUnchanged"] = (ROOT / "recovery.json").is_file() and sha256(ROOT / "recovery.json") == registry_hash
    try:
        verify_sources()
        report["sourceHashesCurrent"] = True
    except (OSError, ValueError) as error:
        report.update(sourceHashesCurrent=False, sourceHashFailure=f"{type(error).__name__}: {error}")
    report['interpretedRegistryUnchanged'] = interpreted_hash == (sha256(interpreted_registry) if interpreted_registry.is_file() else None)
    report['interpretedSourceHashesCurrent'] = interpreted_pins_current(interpreted_batches)
    report['sourcePreferencesUnchanged'] = preference_hash == (sha256(preference_path) if preference_path.is_file() else None)
    scope_current = (not report.get('scopeChangedDuringReplay') and report['recoveryRegistryUnchanged'] and report['sourceHashesCurrent'] and
                     report['interpretedRegistryUnchanged'] and report['interpretedSourceHashesCurrent'] and
                     report['sourcePreferencesUnchanged'])
    report["allChecksPassed"] = not failed and scope_current
    report["buildAndOracleChecksPassed"] = scope_current and all(step["exitCode"] == 0 for step in report["steps"] if not step["command"][1].endswith("verify_workspace.py")) and len(report["steps"]) == len(commands)
    write_json(ROOT / "evidence/verification/checks.json", report)
    stamp = report["createdUtc"].replace(":", "").replace(".", "").replace("+", "_")
    write_json(ROOT / f"evidence/verification/checks-{stamp}.json", report)
    from verify_workspace import index_evidence
    index_evidence()
    return 0 if report["allChecksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
