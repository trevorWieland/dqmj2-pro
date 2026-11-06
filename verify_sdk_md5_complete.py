import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link
from mechanics_save_sdk_md5_complete_oracle import validate


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    rom_sha = sha((ROOT / 'inputs/game.nds').read_bytes())
    if rom_sha != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0' or sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('Complete MD5 pinned host inputs differ')
    path = ROOT / 'evidence/matches/mechanics-save-sdk-memory-original-asm.json'
    document = json.loads(path.read_text(encoding='utf-8'))
    if document['romSha256'] != rom_sha or document['ordinaryCBytes'] != 0 or document['justifiedAssemblyBytes'] != 452:
        raise AssertionError('Complete MD5 SDK source provenance/classification differs')
    matches = {}
    wanted = {0x02008d78, 0x02008e0c}
    for entry in document['matches']:
        if int(entry['address'], 0) not in wanted or entry['sourceLanguage'] != 'assembly' or entry.get('program') or entry['module'] != 'main':
            raise AssertionError('Complete MD5 source helper namespace differs')
        row = dict(entry)
        row.update(freeze_link(validate_link(row, document['nativeSymbolEntries'])))
        code = (ROOT / row['isolatedCallerBinary']).read_bytes()
        if sha(code) != row['isolatedCallerBinarySha256']:
            raise AssertionError('Complete MD5 actual MW snapshot differs')
        matches[row['name']] = row, code
    oracle = validate(arm, save, matches, ROOT)
    oracle['reusedAcceptedSources'].extend(row for row, code in matches.values())
    report = {'schemaVersion': 1, 'romSha256': rom_sha, 'saveSha256': sha(save), 'arm9Sha256': sha(arm), 'matches': [], 'newFunctionCredit': 0, 'newByteCredit': 0, 'sourceFunctions': 6, 'ordinaryCFunctions': 4, 'verifiedOriginalAssemblyFunctions': 2, 'ordinaryCBytes': 1396, 'justifiedAssemblyBytes': 452, 'oracle': oracle, 'oracleSource': 'mechanics_save_sdk_md5_complete_oracle.py', 'oracleSourceSha256': sha((ROOT / 'mechanics_save_sdk_md5_complete_oracle.py').read_bytes()), 'runner': Path(__file__).name, 'runnerSha256': sha(Path(__file__).read_bytes()), 'originalSdkAssemblyProvenance': document['originalSdkAssemblyProvenance'], 'limitations': ['This separate refreshed protocol adds no functions or source-byte credit and preserves earlier native-boundary evidence.', 'Every executed instruction is inside one of six recovered bodies: four ordinary C MD5 routines and two independently verified original SDK assembly memory helpers.', 'The padding byte and448 constant/index data bytes remain hashed original data without data-source credit.', 'No physical memory/cache timing, authentication or semantic save-byte claim follows from deterministic MD5/transfer calculations.']}
    report['inputsUnchanged'] = sha((ROOT / 'inputs/game.nds').read_bytes()) == rom_sha and sha((ROOT / 'inputs/save.sav').read_bytes()) == sha(save)
    if not report['inputsUnchanged']:
        raise AssertionError('Complete MD5 inputs changed')
    (ROOT / 'evidence/matches/mechanics-save-sdk-md5-complete-protocol.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'sourceFunctions': 6, 'ordinaryCFunctions': 4, 'originalSdkAssemblyFunctions': 2, 'oracleCases': oracle['cases'], 'oracleCalls': oracle['nativeAndRecompiledCalls'], 'retainedNativeBodies': len(oracle['retainedNativeEntries']), 'outsideSourceInstructions': oracle['executionOutsideSixRecoveredSourceBodies']}, indent=2))


if __name__ == '__main__':
    main()
