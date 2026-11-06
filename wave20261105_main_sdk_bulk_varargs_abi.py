import re
from pathlib import Path
from project import ROOT, read_json, sha256
import wave20261104_main_sdk_prefix_match as F

ARM_SHA = '034877f8a69a5f78b6d3fdc9014e6f752461f85e51da6f74a2347dfff6c3e051'
TYPES_SHA = '8df8bb5a2b299c7731a6e1d1aef7b4eb2bf77699a2e93d27da35cfa78597341a'


def verify_abi(inputs):
    arm, types = (ROOT / inputs['publishedArmABI'][key]['path'] for key in ['arm', 'types'])
    assert sha256(arm) == inputs['publishedArmABI']['arm']['sha256'] == ARM_SHA
    assert sha256(types) == inputs['publishedArmABI']['types']['sha256'] == TYPES_SHA
    assert '#define _MSL_VA_LIST_TYPE char *' in types.read_text()
    defines = '\n'.join(line.strip() for line in arm.read_text().splitlines() if line.strip().startswith('#define'))
    macro_header = '#ifndef _MSL_STDARG_ARM_H\n#define _MSL_STDARG_ARM_H\n#define __std(x) x\n' + defines + '\n#endif\n'
    return macro_header


def checked_source(item, macro_header):
    source = ROOT / item['source']
    pins = [dict(path=item['source'], sha256=item['sourceSha256']), *item['sourceDependencies']]
    combined = ''
    for pin in pins:
        path = ROOT / pin['path']
        text = path.read_text()
        if sha256(path) != pin['sha256'] or len(text.splitlines()) > 500 or '/*' in text or '//' in text:
            raise ValueError('Frozen readable formatter source/header changed')
        if re.search(r'\b(?:asm|__asm|__asm__|J2pUnknownVaList)\b', text):
            raise ValueError('Formatter source contains assembly or a provisional type')
        if path.suffix == '.h' and '#include' in text:
            raise ValueError('Undeclared transitive formatter source header')
        if path.name == 'msl_arm_varargs.h' and text != macro_header:
            raise ValueError('Source ARM va_start/va_arg macros differ from their pinned published definitions')
        combined += text + '\n'
    if re.search(r'\bva_list\b', combined) and not re.search(r'typedef\s+char\s*\*\s*va_list\s*;', combined):
        raise ValueError('Source variadic representation is not the published ARM MSL char pointer')
    if re.search(r'\bsize_t\b', combined) and not re.search(r'typedef\s+unsigned\s+(?:int|long)\s+size_t\s*;', combined):
        raise ValueError('Formatter length type is not a native32 unsigned C integer')
    assert sha256(ROOT / item['compilerPath']) == item['compilerSha256']
    assert '-lang' in item['flags'] and item['flags'][item['flags'].index('-lang') + 1] == 'c99'
    assert not any(flag.startswith('-D') or flag == '-i' for flag in item['flags'])
    return source
