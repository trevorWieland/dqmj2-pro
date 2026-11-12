"""Test how mwccarm pools two loads of the same constant, ARM and Thumb.

The duplicate-pool class needs a spelling that keeps two same-valued pool slots
distinct.  This probes the candidates against the pinned compiler (2.0/sp1p5,
the identity every transcribed lane uses):

* the same numeric literal twice;
* two different spellings of the same numeric literal;
* two distinct extern alias symbols whose names both end in the value;
* one extern alias plus one numeric literal.

Every variant is a tiny inline-asm function with two ``ldr rX, =expr`` loads.
The object's ``.text`` is read back, so the number of pool words and the
relocation table are measured, not assumed.  A textual variant still folds into
one slot; two distinct symbols do not.  That is the spelling the transcriber's
``constant_aliases=True`` mode uses.

    python ops/probe_pool_aliases.py
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402

CC = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
FLAGS = {
    'arm': ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
            '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off',
            '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc',
            '-nolink', '-msgstyle', 'gcc', '-opt', 'speed'],
    'thumb': ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
              '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off',
              '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc',
              '-nolink', '-msgstyle', 'gcc', '-opt', 'speed', '-thumb'],
}
TYPES = ('typedef unsigned char u8;\ntypedef unsigned int u32;\n'
         'typedef unsigned short u16;\n')
BODY = '    ldr r0, =%s\n    ldr r1, =%s\n    bx lr\n'
VARIANTS = {
    # name: (first expression, second expression, extra declarations, pool words, relocations)
    'same-literal': ('0x0000011d', '0x0000011d', '', 1, 0),
    'text-variant': ('0x0000011d', '0x11d', '', 1, 0),
    'paren': ('0x0000011d', '(0x0000011d)', '', 1, 0),
    'extern-pair': ('native_const_0000011d', 'native_const2_0000011d',
                    'extern u8 native_const_0000011d[];\n'
                    'extern u8 native_const2_0000011d[];\n', 2, 2),
    'extern-plus-literal': ('native_const_0000011d', '0x0000011d',
                            'extern u8 native_const_0000011d[];\n', 2, 1),
}


def compile_variant(mode, name, first, second, extra, work):
    source = Path(work) / ('probe_%s_%s.c' % (mode, name))
    obj = Path(work) / ('probe_%s_%s.o' % (mode, name))
    source.write_text(TYPES + extra + '\nasm u32 probe (void)\n{\n'
                      + BODY % (first, second) + '}\n', encoding='ascii')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(CC), *FLAGS[mode], '-c', str(source), '-o', str(obj)],
                            cwd=str(work), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit('%s/%s compile failed: %s' % (mode, name, result.stdout[-500:]))
    text, defined, relocations = form_search.read_object(obj)
    # Code bytes: ARM = two 4-byte loads + 4-byte ``bx lr`` = 12; Thumb = two
    # 2-byte loads + 2-byte ``bx lr`` + the 2-byte return padding = 8.  Every
    # remaining byte is a 4-byte pool word.
    body_bytes = 12 if mode == 'arm' else 8
    return {'poolWords': (len(text) - body_bytes) // 4,
            'relocations': relocations, 'defined': defined}


def main():
    failures = 0
    with tempfile.TemporaryDirectory(prefix='pool-aliases-') as work:
        for mode in ('arm', 'thumb'):
            print('===', mode)
            for name, (first, second, extra, want_words, want_relocs) in VARIANTS.items():
                result = compile_variant(mode, name, first, second, extra, work)
                ok = (result['poolWords'] == want_words
                      and len(result['relocations']) == want_relocs)
                failures += 0 if ok else 1
                print('  %-20s pool words %d (want %d), relocations %d (want %d) %s' % (
                    name, result['poolWords'], want_words, len(result['relocations']),
                    want_relocs, 'ok' if ok else 'FAIL'))
                if name == 'extern-pair':
                    symbols = [item[2] for item in result['relocations']]
                    values = [form_search.symbol_address(symbol) for symbol in symbols]
                    if sorted(set(values)) != [0x11d]:
                        failures += 1
                        print('    alias values %s != [0x11d]' % values)
                    if len(set(symbols)) != 2:
                        failures += 1
                        print('    alias symbols are not distinct: %s' % symbols)
    print('\n%d failure(s)' % failures)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
