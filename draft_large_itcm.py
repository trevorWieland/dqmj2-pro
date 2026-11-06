import json
import os
import re
import subprocess
from pathlib import Path
import call_prototypes
import draft_itcm
import early_guards
import match_lowlevel as matcher
from typed_global_fields import recover_global_records

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/lowlevel-recovery/itcm-large-drafts'
POINTERS = {'func_01ffb334': 'u8 *', 'func_01ffb340': 'u8 *', 'func_01ffb500': 's16 *',
            'func_ov000_02223c60': 'u32 *', 'func_ov000_02223c54': 'u8 *', 'func_02049ad0': 'u8 *',
            'func_020894d4': 's32 *'}
TARGETS = ['func_01ffbbcc', 'func_01ffc890', 'func_01ff97e0', 'func_01ffcd84']


def split_source(source, name, directory):
    directory.mkdir(parents=True, exist_ok=True)
    entry = re.search(r'^(?:u32|void) ' + re.escape(name) + r'\(', source, re.M)
    if entry is None:
        raise ValueError('Large ordinary C entry definition is missing')
    header, body = source[:entry.start()], source[entry.start():]
    if len(header.splitlines()) > 500:
        raise ValueError('Large context header needs a logical type split')
    files = {'context.h': header}
    lines = body.splitlines(keepends=True)
    if len(lines) <= 450:
        files[name + '.c'] = '#include "context.h"\n' + body
    else:
        switch = next((index for index, line in enumerate(lines) if line.startswith('    switch (')), None)
        opening = body.index('{', sum(map(len, lines[:switch]))) if switch is not None else None
        closing = early_guards.closing(early_guards.masked(body), opening, '{', '}') if opening is not None else None
        ending = body[:closing].count('\n') if closing is not None else None
        if switch is None or ending is None or ending <= switch:
            raise ValueError('Large state machine has no top-level switch boundary')
        prefix, suffix = lines[:switch + 1], lines[ending:]
        cases = lines[switch + 1:ending]
        chunks = []
        while len(cases) > 400:
            cuts = [index for index, line in enumerate(cases[:401]) if index > 0 and re.match(r'    (?:case\b|default:)', line)]
            if not cuts:
                raise ValueError('One state case needs a separate normal C helper before exceeding the file limit')
            cut = cuts[-1]
            chunks.append(cases[:cut])
            cases = cases[cut:]
        chunks.append(cases)
        includes = []
        for index, chunk in enumerate(chunks):
            filename = f'states-{index:02}.inc'
            files[filename] = ''.join(chunk)
            includes.append('#include "' + filename + '"\n')
        files[name + '.c'] = '#include "context.h"\n' + ''.join(prefix + includes + suffix)
    for filename, text in files.items():
        if len(text.splitlines()) > 500:
            raise ValueError('Authored source file exceeds the physical line limit')
        (directory / filename).write_text(text)
    return directory / (name + '.c'), [{'path': (directory / filename).relative_to(ROOT).as_posix(),
                                       'sha256': matcher.sha(text.encode()), 'lines': len(text.splitlines())} for filename, text in files.items()]


def stack_records(text, target):
    if target == 'func_01ffbbcc':
        text = text.replace('    s32 sp14;\n    u16 sp12;\n    u16 sp10;\n    u16 spE;\n    u16 spC;',
                            '    struct { struct {u16 x,y;} second,first;u16 text[32]; } frame;')
        text = text.replace('&sp14', 'frame.text').replace('&sp10', '&frame.first').replace('&spC', '&frame.second')
        for old, new in [('sp12', 'frame.first.y'), ('sp10', 'frame.first.x'), ('spE', 'frame.second.y'), ('spC', 'frame.second.x')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
    if target == 'func_01ffc890':
        text = text.replace('    u32 sp10;\n    u32 spC;\n    u32 sp8;', '    struct {u32 first,second,third;} counters;')
        text = text.replace('&sp8', '&counters')
        for old, new in [('sp10', 'counters.third'), ('spC', 'counters.second'), ('sp8', 'counters.first')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
    return text


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    draft_itcm.RESOLVE_WORD_TYPES = True
    draft_itcm.ARGUMENTS = {}
    draft_itcm.inputs()
    context = (draft_itcm.WORK / 'context.c').read_text()
    for name, result in POINTERS.items():
        context = context.replace('extern u32 ' + name + '(', 'extern ' + result + name + '(')
    journals = []
    for target in TARGETS:
        for returns in ('u32', 'void'):
            directory = WORK / 'native-context' / target / returns
            directory.mkdir(parents=True, exist_ok=True)
            typed = context.replace('extern u32 ' + target + '(', 'extern ' + returns + ' ' + target + '(')
            context_path = directory / 'decompiler-context.h'
            context_path.write_text(typed)
            command = [matcher.sys.executable, str(draft_itcm.M2C), '--target', 'arm-mwcc-c', '--comment-style', 'none',
                       '--no-cache', '--valid-syntax', '--globals', 'none', '--context', str(context_path), '-f', target, str(draft_itcm.WORK / 'itcm.s')]
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=90,
                                     env=dict(os.environ, PYTHONPATH=str(ROOT / 'tools/m2c-python')))
            record = {'target': target, 'returnHypothesis': returns, 'command': command, 'exitCode': process.returncode,
                      'stdout': process.stdout, 'stderr': process.stderr, 'attempts': []}
            journals.append(record)
            if process.returncode:
                continue
            text = draft_itcm.source_text(process.stdout, target, limit=None)
            for name, result in POINTERS.items():
                native = 'native_fn_' + name.removeprefix('func_')
                text = text.replace('extern u32 ' + native + '(', 'extern ' + result + native + '(')
            if 'NULL' in text:
                text = '#define NULL ((void *)0)\n' + text
            text = stack_records(text, target)
            prototype_changes = []
            name = 'native_itcm_' + target.removeprefix('func_')
            for typed_globals in (False, True):
                variant = recover_global_records(text)[0] if typed_globals else text
                source, dependencies = split_source(variant, name, directory / ('typed' if typed_globals else 'plain'))
                record.setdefault('sourcePacks', []).append({'source': source.relative_to(ROOT).as_posix(), 'dependencies': dependencies,
                                                            'typedGlobals': typed_globals, 'prototypeChanges': prototype_changes})
                for level, speed in ((2, False), (2, True), (3, True), (1, False)):
                    try:
                        entries, found = matcher.compare(source, 'itcm', level, 'off', speed)
                    except matcher.UnresolvedNativeSymbol as error:
                        record['attempts'].append(error.details)
                        continue
                    record['attempts'].extend(entries)
                    for entry in entries:
                        if not entry.get('compileFailed'):
                            print({'target': target, 'returns': returns, 'typed': typed_globals, 'level': level, 'speed': speed,
                                   'bytes': entry.get('compiledBytes'), 'matching': entry.get('matchingBytes'), 'exact': entry.get('exactAfterDeclaredRelocation')}, flush=True)
                    if found:
                        record['pendingExactMatch'] = next(iter(found.values()))[0]
                        record['pendingSourceDependencies'] = dependencies
                        break
    output = ROOT / 'evidence/attempts/itcm-large-native-context.json'
    output.write_text(json.dumps({'pointerReturnHypotheses': POINTERS, 'results': journals, 'sourceReconstructionComplete': False}, indent=2) + '\n')
    print({'decompiledContexts': len(journals), 'comparedBodies': sum(not entry.get('compileFailed') for item in journals for entry in item['attempts']),
           'pendingMatches': sum('pendingExactMatch' in item for item in journals)})


if __name__ == '__main__':
    main()
