#include "context_00.h"
asm BOOL native_main_02006d4c (register OSContext * context)
{
    stmfd sp !, { lr, r0 }
    add r0, r0, #72
    ldr r1, = native_fn_0200d8c4
    blx r1
    ldmfd sp !, { lr, r0 }
    add r1, r0, #0
    mrs r2, cpsr
    str r2, [r1], #4 - 0
    mov r0, #0x13 | 0x80 | 0x40 | 0x0
    msr cpsr_c, r0
    str sp, [r1, #68 - 4 ]
    msr cpsr_c, r2
    mov r0, #1
    stmia r1, {r0 - r14}
    add r0, pc, #8
    str r0, [r1, #64 - 4 ]
    mov r0, #0
    bx lr
}
