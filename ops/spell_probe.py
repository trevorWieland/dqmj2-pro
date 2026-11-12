"""Probe which spellings mwccarm's assembler accepts for one instruction form."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
         '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI',
         'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink',
         '-msgstyle', 'gcc', '-c']
TEMPLATE = '''typedef unsigned int u32;
extern unsigned char native_data_02000000[];
asm void probe (register u32 a0)
{
%s
}
'''


def try_body(body):
    work = ROOT / 'work/asm-chunk-scan/spell'
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'probe.c'
    source.write_text(TEMPLATE % body, encoding='ascii')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(COMPILER), *FLAGS, str(source), '-o', str(work / 'probe.o')],
                            cwd=str(work), capture_output=True, text=True, env=env)
    return result.returncode, (result.stdout or result.stderr).strip().splitlines()[:1]


def main():
    bodies = [
        '    pophs {r4, r5, r6, r7, r8, r9, r10, pc}',
        '    pople {r4, r5, pc}',
        '    popne {r3, pc}',
        '    pushhs {r4, lr}',
        '    mov r2, r8',
        '    ldr r8, [r5, #0x18]',
        '    add r8, sp, #0',
        '    mov r9, r0',
        '    mov r10, r0',
        '    mov r11, r0',
        '    ldrsb r1, [r5, #32]',
        '    ldrsh r1, [r5, #32]',
        '    ldrh r1, [r5, #32]',
        '    ldrb r1, [r5, #32]',
        '    strh r1, [r5, #32]',
        '    strb r1, [r5, #32]',
        '    ldrneb r0, [r8, #0x160]',
        '    ldrbne r0, [r8, #0x160]',
        '    ldrneh r0, [r8, #0x160]',
        '    ldrhne r0, [r8, #0x160]',
        '    ldrsbne r0, [r8, #0x160]',
        '    ldrnesb r0, [r8, #0x160]',
        '    lsrs r0, r0, #28',
        '    movs r0, r0, lsr #28',
        '    subs r0, r0, #1',
        '    adds r0, r0, #1',
        '    mov r0, r0, lsl #28',
        '    ldmia r7, {r0, r1}',
        '    stmia r7, {r0, r1}',
        '    ldr r0, [r1, #-4]',
        '    ldr r0, [r1], #4',
        '    mla r0, r1, r2, r3',
        '    smull r0, r1, r2, r3',
        '    umull r0, r1, r2, r3',
        '    ldr r0, =native_data_02000000',
        '    movne r0, #0',
        '    bne 1f',
        '1:',
        '    bx lr',
        '    nop',
        '    swp r0, r1, [r2]',
        '    and r1, r1, r0, lsl r2',
        '    ldmneia r4, {r0, r1, r2}',
        '    stmneia r3, {r0, r1, r2}',
        '    rsb r0, r1, #0',
        '    mvn r0, r1',
        '    clz r0, r1',
        '    smlal r0, r1, r2, r3',
    ]
    for body in bodies:
        code, message = try_body(body)
        print('%-4s %-46s %s' % ('ok' if code == 0 else 'FAIL', body.strip(), message))
    return 0


if __name__ == '__main__':
    sys.exit(main())
