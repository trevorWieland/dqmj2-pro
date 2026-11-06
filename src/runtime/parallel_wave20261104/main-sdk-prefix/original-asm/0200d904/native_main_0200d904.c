#include "context_00.h"
asm void native_main_0200d904 (register const CPContext *context)
{
    stmfd sp !, {r4}
    ldr r1, = (0x04000000 + 0x290)
    ldmia r0, {r2 - r4, r12}
    stmia r1, {r2 - r4, r12}
    ldrh r2, [r0, #CPContext.div_mode]
    ldrh r3, [r0, #CPContext.sqrt_mode]
    strh r2, [r1, #0x280 - 0x290 ]
    strh r3, [r1, #0x2b0 - 0x290 ]
    add r0, r0, #CPContext.sqrt
    add r1, r1, #0x2b8 - 0x290
    ldmia r0, {r2 - r3}
    stmia r1, {r2 - r3}
    ldmfd sp !, {r4}
    bx lr
}
