import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link
from evidence.save.sdk_memory_asm_provenance import body, canonical

ASSEMBLER = 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
ASSEMBLER_HASH = 'e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c'
FLAGS = ['-proc', 'arm5TE', '-c']
SPECS = {'saved_sdk_fill': (0x02008d78, 148, 'MI_CpuFill8'), 'saved_sdk_copy': (0x02008e0c, 304, 'MI_CpuCopy8')}
PROVENANCE = 'evidence/save/sdk-memory-original-assembly-provenance.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compile_sources(arm):
    provenance = json.loads((ROOT / PROVENANCE).read_text(encoding='utf-8'))
    if sha((ROOT / provenance['canonicalizer']).read_bytes()) != provenance['canonicalizerSha256']:
        raise AssertionError('SDK original-assembly canonicalizer identity differs')
    if len(provenance['sourceReferences']) != 2 or not provenance['independentReferenceInstructionStreamsEqual']:
        raise AssertionError('Independent original SDK assembly source evidence is incomplete')
    if sha((ROOT / ASSEMBLER).read_bytes()) != ASSEMBLER_HASH:
        raise AssertionError('Pinned original SDK mnemonic assembler differs')
    directory = ROOT / 'work/mechanics-save/sdk-memory-original-asm'
    directory.mkdir(parents=True, exist_ok=True)
    matches = {}
    bindings = {name: {'address': hex(address), 'mode': 'arm', 'module': 'main', 'processor': 'arm9', 'kind': 'function'} for name, (address, size, original) in SPECS.items()}
    for name, (address, size, original) in SPECS.items():
        source = ROOT / f'src/mechanics_save/{name}_original.s'
        text = source.read_text()
        instructions = canonical(body(text, name))
        if any(instructions != reference['selectedDefaultDefinitions'][original] for reference in provenance['sourceReferences']):
            raise AssertionError(('Readable mnemonic source differs from independently pinned SDK definitions', name))
        if any(token in text for token in ('.byte', '.word', '.long', '.short', 'dcd', 'dcw', 'incbin')):
            raise AssertionError('SDK source contains raw executable data')
        output = directory / (name + '.o')
        process = subprocess.run([str(ROOT / ASSEMBLER), *FLAGS, str(source), '-o', str(output)], cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
        if process.returncode:
            raise AssertionError(('SDK mnemonic assembly failed', process.stdout, process.stderr))
        data = output.read_bytes()
        stable = directory / (sha(data) + '.o')
        stable.write_bytes(data)
        with io.BytesIO(data) as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == name)
            payload = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
            relocs = [section for section in elf.iter_sections() if section['sh_type'] in ('SHT_REL', 'SHT_RELA') and section['sh_info'] == symbol['st_shndx'] and section.num_relocations()]
            if relocs or symbol['st_size'] != size or payload != arm[address - 0x02000000:address - 0x02000000 + size]:
                raise AssertionError(('Complete SDK mnemonic source bytes/boundary/relocations differ', name, len(payload)))
            row = {'name': name, 'sdkOriginalSymbol': original, 'module': 'main', 'processor': 'arm9', 'mode': 'arm', 'address': hex(address), 'bytes': size, 'size': size, 'compiledBytes': size, 'matchingBytes': size, 'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha(source.read_bytes()), 'object': stable.relative_to(ROOT).as_posix(), 'objectSha256': sha(data), 'sourceLanguage': 'assembly', 'ordinaryCBytes': 0, 'justifiedAssemblyBytes': size, 'justifiedAssemblyRanges': [{'module': 'main', 'processor': 'arm9', 'mode': 'arm', 'start': hex(address), 'end': hex(address + size), 'bytes': size}], 'assemblyJustification': {'kind': 'verified-original-sdk-inline-assembly', 'originalSymbol': original, 'provenance': PROVENANCE, 'provenanceSha256': sha((ROOT / PROVENANCE).read_bytes()), 'completeInstructionStream': instructions, 'rawExecutableBytesStoredAsSource': False}, 'compiler': ASSEMBLER, 'compilerSha256': ASSEMBLER_HASH, 'assemblerSha256': ASSEMBLER_HASH, 'flags': FLAGS, 'compilerFlags': FLAGS, 'nativeAlias': f'func_{address:08x}', 'targetSha256': sha(payload), 'outputSha256': sha(payload), 'sectionIndex': symbol['st_shndx'], 'sectionOffset': symbol['st_value'], 'relocations': [], 'exactAfterDeclaredRelocation': True, 'exactBytes': True, 'linked': False}
        proof = validate_link(row, bindings)
        row.update(freeze_link(proof))
        row['exactAfterRealMwLink'] = True
        matches[name] = row, payload
    return matches, bindings, provenance


def main():
    rom = (ROOT / 'inputs/game.nds').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(rom) != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0' or sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('SDK assembly pinned input namespace differs')
    matches, bindings, provenance = compile_sources(arm)
    from mechanics_save_sdk_memory_oracle import validate
    oracle = validate(arm, save, matches, ROOT)
    report = {'schemaVersion': 1, 'romSha256': sha(rom), 'saveSha256': sha(save), 'arm9Sha256': sha(arm), 'matches': [row for row, code in matches.values()], 'nativeSymbolEntries': bindings, 'nativeSymbols': {name: value['address'] for name, value in bindings.items()}, 'nativeSymbolModules': {name: 'main' for name in bindings}, 'sourceLanguage': 'assembly', 'ordinaryCBytes': 0, 'justifiedAssemblyBytes': sum(row['bytes'] for row, code in matches.values()), 'originalSdkAssemblyProvenance': provenance, 'oracle': oracle, 'oracleSource': 'mechanics_save_sdk_memory_oracle.py', 'oracleSourceSha256': sha((ROOT / 'mechanics_save_sdk_memory_oracle.py').read_bytes()), 'wholeLinkedRebuild': False, 'inputsUnchanged': sha((ROOT / 'inputs/game.nds').read_bytes()) == sha(rom) and sha((ROOT / 'inputs/save.sav').read_bytes()) == sha(save), 'limitations': ['Exactly two complete original SDK inline-assembly implementations are reconstructed as readable mnemonics under the explicit verified-original-assembly allowance; all452 bytes are separately classified as justified assembly with zero ordinary C bytes.', 'Public SDK and decomp library source references are pinned and agree on every instruction; a separately authenticated Nintendo source-release archive is not available.', 'No failed ordinary C candidate is accepted and no further game/library function receives an inferred assembly allowance.', 'The bounded aligned/unaligned/tail/overlap/zero-length/fault oracle characterizes target access mechanics, without asserting physical VRAM/cache timing or portable overlapping-copy semantics.']}
    (ROOT / 'evidence/matches/mechanics-save-sdk-memory-original-asm.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'matchedFunctions': len(matches), 'justifiedAssemblyBytes': report['justifiedAssemblyBytes'], 'ordinaryCBytes': 0, 'oracleCases': oracle['cases'], 'oracleCalls': oracle['nativeAndReassembledCalls']}, indent=2))


if __name__ == '__main__':
    main()
