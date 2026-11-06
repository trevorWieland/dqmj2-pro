#include "context_00.h"
asm void native_main_0200d8c4 (register CPContext *context)
{
    ldr r1, = (0x04000000 + 0x290)
    stmfd sp !, {r4}
    ldmia r1, {r2 - r4, r12}
    stmia r0 !, {r2 - r4, r12}
    ldrh r12, [r1, #0x280 - 0x290 ]
    add r1, r1, #0x2b8 - 0x290
    ldmia r1, {r2 - r3}
    stmia r0 !, {r2 - r3}
    and r12, r12, #0x0003
    ldrh r2, [r1, #0x2b0 - 0x2b8 ]
    strh r12, [r0]
    and r2, r2, #0x0001
    strh r2, [r0, #2]
    ldmfd sp !, {r4}
    bx lr
}
