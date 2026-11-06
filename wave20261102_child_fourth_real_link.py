import json
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path
import utility_code
import utility_runtime
from elf_units import split_symbol
from elftools.elf.elffile import ELFFile
from link_runtime_unit import binding_object, relocation_rows, LINKER, LINKER_HASH
from project import sha256, write_json
from wave20261102_child_fourth_prepare import ROOT
from wave20261102_child_fourth_index import candidates


@lru_cache(maxsize=1)
def canonical():
    return {(s['processor'], s['address']): s for s in candidates()}


def validate(entry, directory):
    directory.mkdir(parents=True, exist_ok=True)
    if sha256(LINKER) != LINKER_HASH:
        raise ValueError('Pinned linker changed')
    spec = utility_code.accepted_spec(entry)
    native = (ROOT / spec['binary']).read_bytes()[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    source, original = ROOT / entry['source'], ROOT / entry['object']
    if sha256(source) != entry['sourceSha256'] or sha256(original) != entry['objectSha256']:
        raise ValueError('Source/object changed')
    caller = directory / 'caller.o'
    with original.open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    relocs = relocation_rows(original, entry['name'])
    if relocs != relocation_rows(caller, entry['name']):
        raise ValueError('Splitting altered relocation encoding/addends')
    candidates = canonical()
    layout, unused = utility_runtime.derive()
    modules = [m for m in layout['modules'] if m['processor'] == entry['processor']]
    memory = ['CALL: ORIGIN = %s > caller.bin' % entry['address']]
    selectors = ['.caller: { caller.o(.text) } > CALL']
    assignments, objects, bindings = [], [caller], []
    unique_rows = {}
    for row in entry['relocations']:
        if row['symbol'] in unique_rows and any(row[k] != unique_rows[row['symbol']][k] for k in ('target', 'targetMode')):
            raise ValueError('Repeated symbol has conflicting target identity')
        unique_rows[row['symbol']] = row
    for index, row in enumerate(unique_rows.values()):
        name, address = row['symbol'], int(row['target'], 0)
        if not re.fullmatch(r'[A-Za-z_]\w*', name):
            raise ValueError('Malformed relocation symbol')
        if row['targetMode'] in ('arm', 'thumb'):
            target = candidates.get((entry['processor'], address & ~1))
            if target is None or target['mode'] != row['targetMode']:
                raise ValueError('Function binding lacks canonical same-program CPU/mode entry')
            probe = directory / ('binding%d.o' % index)
            binding_object(name, target['mode'], flags, probe)
            memory.append('BIND%d: ORIGIN = %#x > binding%d.bin' % (index, address & ~1, index))
            selectors.append('.binding%d: { binding%d.o(.text) } > BIND%d' % (index, index, index))
            objects.append(probe)
            bindings.append(dict(name=name, program=entry['program'], processor=entry['processor'],
                module=target['module'], address=hex(address & ~1), mode=target['mode'], kind='function',
                initializedCodeBytes=0, nativeCalleeBytesUsed=0, calleeSourceCredit=0,
                anchorObject=probe.relative_to(ROOT).as_posix(), anchorObjectSha256=sha256(probe)))
        else:
            assignments.append('%s = %#x;' % (name, address))
            owned = [m for m in modules if int(m['base'], 0) <= address < int(m['bssEnd'], 0)]
            bindings.append(dict(name=name, program=entry['program'], processor=entry['processor'],
                module=owned[0]['id'] if len(owned) == 1 else 'external-measured-native-literal',
                address=hex(address), mode='data', kind='data', originalDataSourceCredit=0))
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memory) + '\n}\nSECTIONS {\n' +
                   '\n'.join(selectors + assignments) + '\n}\n')
    linked = directory / 'linked.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi',
               '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ,
        LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    attempt = dict(command=command, cwd=str(directory), exitCode=process.returncode,
                   stdout=process.stdout, stderr=process.stderr)
    write_json(directory / 'link-attempt.json', attempt)
    if process.returncode:
        raise ValueError(attempt)
    output = (directory / 'caller.bin').read_bytes()
    if output != native:
        raise ValueError(dict(linkedBytes=len(output), nativeBytes=len(native), equal=False))
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(s for s in symbols if s.name == entry['name'])
        if (symbol['st_value'] & ~1, symbol['st_size']) != (spec['address'], spec['bytes']):
            raise ValueError('Linked symbol extent changed')
        for binding in bindings:
            if binding['kind'] == 'function':
                target = int(binding['address'], 0)
                symbol = next(s for s in symbols if s.name == binding['name'])
                if symbol['st_size'] != 0 or symbol['st_value'] & ~1 != target:
                    raise ValueError('Binding acquired code or wrong address')
    for path in directory.glob('binding*.bin'):
        if path.stat().st_size:
            raise ValueError('Binding emitted initialized code')
    result = dict(program=entry['program'], processor=entry['processor'], module=entry['module'],
        name=entry['name'], address=entry['address'], bytes=len(native), exactCallerBytes=True,
        linkerSha256=LINKER_HASH, linkerAttempt=attempt, originalRelocations=relocs,
        splitPreservesRelocationTypesAddendsAndEncodedHBits=True, nativeSpanSha256=entry['targetSha256'],
        linkedCallerSha256=utility_runtime.sha(output), linkedElf=linked.relative_to(ROOT).as_posix(),
        linkedElfSha256=sha256(linked), lcf=lcf.relative_to(ROOT).as_posix(), lcfSha256=sha256(lcf),
        bindings=bindings, wholeModuleLinked=False, calleeCodeOrSourceCredit=0)
    write_json(directory / 'validation.json', result)
    return result
