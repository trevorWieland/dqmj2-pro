import os
import shutil
import subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256
from link_runtime_unit import validate, relocation_rows
from recover_linked_runtime import qualified_bindings
from wave20261106_dwc_main_friend_next_first_v2_compiler import WORK, COMPILER, compare
from wave20261106_dwc_main_friend_next_first_v2_fixtures import run
import wave20261106_dwc_main_friend_next_first_v2_models as F


def body(row):
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name'])
        offset = symbol['st_value'] & ~1
        return elf.get_section(symbol['st_shndx']).data()[offset:offset + symbol['st_size']]


def strict(rows):
    output = []
    for row in rows:
        source = ROOT / row['source']
        fresh, unused = compare(source, WORK / 'controls/required-prototypes' / source.stem, strict=True)
        if len(fresh) != 1 or fresh[0].get('compileFailed'):
            raise ValueError(('Explicit declarations failed strict diagnostic', row['address'], fresh))
        candidate = fresh[0]
        if body(candidate) != body(row) or relocation_rows(ROOT / candidate['object'], candidate['name']) != relocation_rows(ROOT / row['object'], row['name']):
            raise ValueError('Required-prototype diagnostic changed genuine function bytes/relocations')
        output.append(dict(address=row['address'], functionBytesAndRelocationsIdentical=True,
            flags=candidate['compilerFlags'], object=candidate['object'], objectSha256=candidate['objectSha256']))
    return output


MUTANTS = {
    0x209d0d4: ('arg->index', 'arg->profile', 2),
    0x209d168: ('return -1;', 'return 0;', 0),
    0x209d1a8: ('gpProcessCount = 0;', 'gpProcessCount = 1;', 1),
    0x209d238: ('state != DWC_FRIEND_STATE_PERS_LOGIN', 'state == DWC_FRIEND_STATE_PERS_LOGIN', 1),
    0x209d704: ('DWC_ECODE_TYPE_ALLOC', 'DWC_ECODE_TYPE_PARAM', 1),
    0x209d758: ('native_fn_02096e50(&stpFriendCnt->friendList[friendIdx], TRUE)', 'native_fn_02096e50(&stpFriendCnt->friendList[friendIdx], FALSE)', 6),
    0x209d8f0: ('native_fn_02096e08(&stpFriendCnt->friendList[i], TRUE)', 'native_fn_02096e08(&stpFriendCnt->friendList[i], FALSE)', 3),
    0x209da68: ('if (native_fn_02096d04', 'if (!native_fn_02096d04', 3)}


def wrong_c(rows):
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    results = []
    for row in rows:
        address = int(row['address'], 0)
        before, after, seed = MUTANTS[address]
        directory = WORK / 'controls/wrong-c' / f'{address:08x}'
        directory.mkdir(parents=True, exist_ok=True)
        source = ROOT / row['source']
        for header in source.parent.glob('*.h'):
            shutil.copyfile(header, directory / header.name)
        text = source.read_text()
        if before not in text:
            raise ValueError('Intended wrong-C branch text absent')
        altered = directory / source.name
        altered.write_text(text.replace(before, after, 1))
        fresh, unused = compare(altered, directory / 'c')
        if len(fresh) != 1 or fresh[0].get('compileFailed'):
            raise ValueError('Wrong-C control did not genuinely compile')
        candidate = fresh[0]
        candidate['program'] = ''
        bindings = qualified_bindings(candidate)
        for binding in bindings.values():
            binding['program'] = ''
        try:
            validate(candidate, bindings, directory / 'l')
        except ValueError as error:
            if not error.args or not isinstance(error.args[0], dict) or 'matchingBytes' not in error.args[0]:
                raise
            mismatch = error.args[0]
        else:
            raise ValueError('Wrong-C source unexpectedly reproduced the complete native body')
        candidate['nativeSymbolEntries'] = bindings
        vector = F.cases(address)[seed]
        trace = run(image, candidate, (directory / 'l/caller.bin').read_bytes(), vector, seed)
        if not trace['topReturned'] or trace['modelPassed']:
            raise ValueError(('Wrong C did not reach the intended observable model failure', address, vector, trace))
        results.append(dict(address=row['address'], altered=before, replacement=after,
            source=altered.relative_to(ROOT).as_posix(), sourceSha256=sha256(altered),
            genuineCompileAndLinkSucceeded=True, fullNativeMismatch=mismatch,
            intendedBranchVector=vector, independentModelRejected=True,
            actualCalls=trace['calls'], expectedCalls=trace['expectedCalls'], topReturned=True))
    return results


LAYOUT = [('sizeof(DWCFriendPrefix)', 92), ('sizeof(DWCFriendData)', 12), ('sizeof(DWCUserData)', 64),
    ('sizeof(GPBuddyStatus)', 532), ('O(GPBuddyStatus,locationString)', 264), ('O(GPBuddyStatus,quietModeFlags)', 528),
    ('O(DWCFriendPrefix,lastGpProcess)', 12), ('O(DWCFriendPrefix,friendListLen)', 20),
    ('O(DWCFriendPrefix,friendList)', 24), ('O(DWCFriendPrefix,buddyUpdateIdx)', 28),
    ('O(DWCFriendPrefix,friendListChanged)', 29), ('O(DWCFriendPrefix,buddyUpdateState)', 30),
    ('O(DWCFriendPrefix,statusCallback)', 52), ('O(DWCFriendPrefix,buddyCallback)', 68),
    ('sizeof(GPProfileSearchMatch)', 172), ('O(GPProfileSearchMatch,firstname)', 56),
    ('O(GPProfileSearchMatch,lastname)', 87), ('sizeof(GPProfileSearchResponseArg)', 16),
    ('O(GPProfileSearchResponseArg,matches)', 12), ('O(GPGetInfoResponseArg,lastname)', 142)]


def layout(rows):
    exemplar = next(row for row in rows if row['address'] == '0x209da68')
    positive = WORK / 'controls/layout/positive'
    positive.mkdir(parents=True, exist_ok=True)
    for header in (ROOT / exemplar['source']).parent.glob('*.h'):
        shutil.copyfile(header, positive / header.name)
    source = positive / 'layout.c'
    source.write_text('#include "context.h"\n#define O(T,F) ((u32)&((T*)0)->F)\nconst u32 layout_values[]={' + ','.join(expression for expression, expected in LAYOUT) + '};\n')
    obj = positive / 'layout.o'
    flags = exemplar['compilerFlags']
    process = subprocess.run([str(COMPILER), *flags, '-c', str(source), '-o', str(obj)], cwd=ROOT,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True)
    if process.returncode:
        raise ValueError(('Actual compiler layout probe failed', process.stdout, process.stderr))
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == 'layout_values')
        offset = symbol['st_value']
        actual = elf.get_section(symbol['st_shndx']).data()[offset:offset + symbol['st_size']]
    expected = b''.join(value.to_bytes(4, 'little') for expression, value in LAYOUT)
    if actual != expected:
        raise ValueError(('Actual compiler consumed-field layout differs', actual.hex(), expected.hex()))
    altered = []
    for label, file, before, after in [
            ('public-namespace-stride176', 'gp_types.h', 'uniquenick[21],firstname[31]', 'uniquenick[21];int namespaceID;gsi_char firstname[31]'),
            ('truncated-buddy-status528', 'context.h', ',quietModeFlags', '')]:
        directory = WORK / 'controls/layout' / label
        directory.mkdir(parents=True, exist_ok=True)
        for header in positive.glob('*.h'):
            shutil.copyfile(header, directory / header.name)
        header = directory / file
        text = header.read_text()
        if before not in text:
            raise ValueError('Wrong layout source fragment absent')
        header.write_text(text.replace(before, after, 1))
        check = directory / 'check.c'
        condition = 'sizeof(GPProfileSearchMatch)==172' if 'namespace' in label else 'sizeof(GPBuddyStatus)==532'
        check.write_text('#include "context.h"\ntypedef char required_consumed_layout[(' + condition + ')?1:-1];\n')
        process = subprocess.run([str(COMPILER), *flags, '-c', str(check), '-o', str(directory / 'check.o')], cwd=ROOT,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True)
        if not process.returncode:
            raise ValueError('Wrong native stride/frame declaration escaped the compiler guard')
        altered.append(dict(label=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(actualCompilerValues=[dict(expression=expression, expected=value) for expression, value in LAYOUT],
        wrongLayouts=altered, object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
        sourceStorageOrInitializedDataCredit=0, friendControlPrefixOnly=True, gpGetInfoResponsePrefixOnly=True)
