#include "context_00.h"
asm void native_main_02006ce0 (register OSContext * context, register u32 newpc, register u32 newsp)
{
    add newpc, newpc, #4
    str newpc, [context, #64 ]
    str newsp, [context, #68 ]
    sub newsp, newsp, #0x40
    tst newsp, #4
    subne newsp, newsp, #4
    str newsp, [context, #56 ]
    ands r1, newpc, #1
    movne r1, #0x1f | 0x20
    moveq r1, #0x1f | 0x0
    str r1, [context, #0 ]
    mov r1, #0
    str r1, [context, #4 ]
    str r1, [context, #8 ]
    str r1, [context, #12 ]
    str r1, [context, #16 ]
    str r1, [context, #20 ]
    str r1, [context, #24 ]
    str r1, [context, #28 ]
    str r1, [context, #32 ]
    str r1, [context, #36 ]
    str r1, [context, #40 ]
    str r1, [context, #44 ]
    str r1, [context, #48 ]
    str r1, [context, #52 ]
    str r1, [context, #60 ]
    bx lr
}
