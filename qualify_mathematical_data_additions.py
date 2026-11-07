import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from project import configuration, read_json, sha256
from qualify_child_message_data_additions_20261106 import selected_data, identity, FIELDS

EXPECTED = {0x020d8d84: 128, 0x020d8e04: 256, 0x020d8f14: 256, 0x020d9068: 68}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate_shape(before, after, expected, functions):
    wanted = {identity(row): row['bytes'] for row in expected}
    admitted = {('', 'arm9', 'main', 'data', address): size for address,size in EXPECTED.items()}
    added = set(after) - set(before)
    require(len(expected) == len(wanted) == 4 and wanted == admitted and added == set(wanted), 'Exact four mathematical data identities required')
    for key,row in before.items():
        require(key in after and all(after[key].get(field) == row.get(field) for field in FIELDS), 'Earlier data source/object changed')
    occupied = [(identity(row)[:3], identity(row)[4], identity(row)[4] + row.get('bytes',row.get('size'))) for row in before.values()]
    for row in functions.values():
        key = identity(dict(row, kind='data'))
        occupied.append((key[:3], key[4], key[4] + row.get('bytes',row.get('size'))))
    for key in sorted(added):
        row = after[key]
        require(identity(row) == key and row['kind'] == row['mode'] == 'data', 'Wrong data namespace or mode')
        require(all(row[field] == wanted[key] for field in ('bytes','size','compiledBytes','initializedBytes')), 'Data extent differs')
        require(row['sourceLanguage'] == 'C' and row['sourceSymbolType'] == 'STT_OBJECT', 'Typed C object required')
        require(row['relocations'] == [] and all(row[field] == 0 for field in ('ordinaryFunctionCredit','executableSectionBytes','allocatedZeroFillBytes','encodedAssetBytes','measuredZeroAlignmentBytes','sectionPaddingBytes')), 'Data cannot contain code, relocations, BSS, assets or padding')
        require(not any(scope == key[:3] and max(begin,key[4]) < min(end,key[4]+wanted[key]) for scope,begin,end in occupied), 'Mathematical data overlaps accepted storage/function')
        occupied.append((key[:3], key[4], key[4]+wanted[key]))
    return added

def qualify(before, after, expected, functions, directory):
    added = validate_shape(before, after, expected, functions)
    directory = Path(directory).resolve()
    require(directory.is_relative_to(ROOT / 'work') and not directory.exists(), 'Fresh work-only output directory required')
    from goal_resume_ctype_ascii_data import guarded_render, TABLES, SOURCE as ASCII_SOURCE
    from goal_resume_ctype_ascii_build import build as ascii_build
    from goal_resume_material_pivot import guarded_render as pivot_render, common, SOURCE as PIVOT_SOURCE
    from goal_resume_material_pivot_data import build as pivot_build
    common_ascii, ascii_outputs, blocked_ascii = guarded_render()
    pivot_code, pivot_payload, blocked_pivot = pivot_render()
    require((ASCII_SOURCE / 'ascii.h').read_text() == common_ascii, 'ASCII common declaration differs')
    require((PIVOT_SOURCE / 'material_pivot.h').read_text() == common(), 'Material/pivot declaration differs')
    definitions = {int(row['address'],0): (ASCII_SOURCE / row['filename'], text, payload, row)
                   for row,text,payload in ascii_outputs}
    definitions[0x020d9068] = (PIVOT_SOURCE / 'data.c', pivot_code, pivot_payload, None)
    image_path = ROOT / 'extract/arm9/arm9.bin'
    image_sha = sha256(image_path)
    image = image_path.read_bytes()
    proofs = []
    for key in sorted(added):
        row = after[key]
        source, code, payload, ascii_row = definitions[key[4]]
        require(source.read_text() == code and sha256(source) == row['sourceSha256'], 'Mathematical source differs')
        require(row['source'] == source.relative_to(ROOT).as_posix(), 'Unadmitted mathematical source path')
        require(hashlib.sha256(payload).hexdigest() == row['targetSha256'] == row['outputSha256'], 'Independent mathematical payload differs')
        require(row['inputModuleSha256'] == image_sha and image[key[4]-0x02000000:key[4]-0x02000000+len(payload)] == payload, 'Original initialized span differs')
        require(sha256(ROOT / row['object']) == row['objectSha256'], 'Frozen worker object differs')
        output = directory / f'{key[4]:08x}'
        actual, fresh = ascii_build(source, ascii_row, output, payload) if ascii_row else pivot_build(source, output, payload)
        require(actual == payload and fresh['compilerSha256'] == row['compilerSha256'] and fresh['compilerFlags'] == row['compilerFlags'], 'Fresh source/recipe mismatch')
        require(fresh['sourceSectionAlignment'] == row['sourceSectionAlignment'], 'Natural typed alignment changed')
        require(fresh['realLink']['exactDataAddress'] and fresh['realLink']['exactDataBytes'] and fresh['realLink']['objectUnmodified'], 'Fresh genuine data placement failed')
        proofs.append(dict(address=hex(key[4]), bytes=len(payload), sourceSha256=sha256(source), fresh=fresh))
    return dict(passed=True, newInitializedDataObjects=4, newInitializedDataBytes=708,
        newTypedConstantDataBytes=708, newEncodedAssetBytes=0, newDataAlignmentBytes=0,
        newSourceFunctions=0, earlierDataPreserved=len(before), proofs=proofs,
        blockedOriginalReadsDuringGeneration=dict(ascii=blocked_ascii, materialPivot=blocked_pivot),
        frozenSDK562QualifierChanged=False, sourceCreditPendingSharedAcceptance=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    before = selected_data()
    after = dict(before)
    for name in ('goal-resume20261107-ctype-ascii-data640.json','goal-resume20261107-material-pivot-data68.json'):
        report = read_json(ROOT / 'evidence/matches' / name)
        for row in report['dataMatches']:
            item = {**report, **row}
            require(identity(item) not in after, 'Proposed data already registered')
            after[identity(item)] = item
    functions = {}
    for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines():
        row = json.loads(line)
        if row['states']['functionMatched']:
            functions[row['id']] = row
    expected = [row for key,row in after.items() if key not in before]
    result = qualify(before, after, expected, functions, ROOT / args.output)
    result.update(status='fresh-mathematical-data-qualification-only-not-registered', sourceCreditAdded=0, registryChanged=False)
    path = ROOT / args.output / 'qualification.json'
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('proofs','blockedOriginalReadsDuringGeneration')}))

if __name__ == '__main__':
    main()
