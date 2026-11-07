import os
import shutil
import subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256
from link_runtime_unit import validate, relocation_rows
from recover_linked_runtime import qualified_bindings
from wave20261106_dwc_main_friend_next_second_compiler import WORK, COMPILER, compare
from wave20261106_dwc_main_friend_next_second_fixtures import run
import wave20261106_dwc_main_friend_next_second_models as F


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
    0x209bc9c: ('DWCi_GetMathRand32(0x4000)', 'DWCi_GetMathRand32(0x4001)', 1),
    0x209be4c: ('ownCloseFlag=FALSE', 'ownCloseFlag=TRUE', 1),
    0x209be5c: ('return;', 'native_fn_0209a9f8(DWC_ERROR_FATAL,0); return;', 0),
    0x209c24c: ('connection, message, len, reliable', 'connection, message, reliable, len', 1),
    0x209c4c8: ('DWC_ERROR_FATAL', 'DWC_ERROR_NETWORK', 0),
    0x209dd80: ('stGameMatchKeys[index].isStr = 0;', 'stGameMatchKeys[index].isStr = 1;', 3),
    0x209eca4: ('htons(port)', 'port', 2)}



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


LAYOUT = [('sizeof(MainGlobalConsumedPrefix)',8),('O(MainGlobalConsumedPrefix,lastSocketError)',4),
    ('O(MainCoreConsumedPrefix,gt2Socket)',0),('O(MainCoreConsumedPrefix,gt2SendBufSize)',20),
    ('O(MainCoreConsumedPrefix,gt2RecvBufSize)',24),('O(MainCoreConsumedPrefix,ownCloseFlag)',44),
    ('sizeof(struct sockaddr_in)',8),('O(struct sockaddr_in,sin_len)',0),('O(struct sockaddr_in,sin_family)',1),
    ('O(struct sockaddr_in,sin_port)',2),('O(struct sockaddr_in,sin_addr)',4),
    ('sizeof(DWCGameMatchKeyData)',12),('O(DWCGameMatchKeyData,isStr)',1),('O(DWCGameMatchKeyData,pad)',2),
    ('O(DWCGameMatchKeyData,keyStr)',4),('O(DWCGameMatchKeyData,value)',8)]


def layout(rows):
    exemplar=next(row for row in rows if row['address']=='0x209eca4')
    positive=WORK/'controls/layout/positive';positive.mkdir(parents=True,exist_ok=True)
    for header in(ROOT/exemplar['source']).parent.glob('*.h'):shutil.copyfile(header,positive/header.name)
    source=positive/'layout.c';source.write_text('#include "context.h"\n#define O(T,F) ((u32)&((T*)0)->F)\nconst u32 layout_values[]={'+','.join(expression for expression,expected in LAYOUT)+'};\n')
    flags=exemplar['compilerFlags'];obj=positive/'layout.o'
    process=subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True)
    if process.returncode:raise ValueError(('Actual second layout compile failed',process.stdout,process.stderr))
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='layout_values');offset=symbol['st_value'];actual=elf.get_section(symbol['st_shndx']).data()[offset:offset+symbol['st_size']]
    expected=b''.join(value.to_bytes(4,'little')for expression,value in LAYOUT)
    if actual!=expected:raise ValueError(('Actual second consumed layout differs',actual.hex(),expected.hex()))
    changed=[]
    for label,before,after,condition in [('foreign-sockaddr16','struct in_addr sin_addr;','struct in_addr sin_addr;u32 unconsumed[2];','sizeof(struct sockaddr_in)==8'),('wrong-key-stride16','u16 pad;char*keyStr;','u32 pad;char*keyStr;','sizeof(DWCGameMatchKeyData)==12')]:
        directory=WORK/'controls/layout'/label;directory.mkdir(parents=True,exist_ok=True)
        for header in positive.glob('*.h'):shutil.copyfile(header,directory/header.name)
        header=directory/'context.h';text=header.read_text()
        if before not in text:raise ValueError('Wrong second layout text absent')
        header.write_text(text.replace(before,after,1));check=directory/'check.c';check.write_text('#include "context.h"\ntypedef char required_native_layout[('+condition+')?1:-1];\n')
        process=subprocess.run([str(COMPILER),*flags,'-c',str(check),'-o',str(directory/'check.o')],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True)
        if not process.returncode:raise ValueError('Wrong native layout escaped strict check')
        changed.append(dict(label=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    return dict(actualCompilerValues=[dict(expression=e,expected=v)for e,v in LAYOUT],wrongLayouts=changed,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),sourceStorageOrInitializedDataCredit=0,onlyConsumedPrefixesAndFieldsQualified=True)
