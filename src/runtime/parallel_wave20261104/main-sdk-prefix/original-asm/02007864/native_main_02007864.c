#include "context_00.h"
asm void native_main_02007864 (void)
{
    ldr r1, = native_data_main_020e3644.field_002c;
    mrs r2, CPSR
    str r2, [r1, #OSiExContext.debug[1]]
    str r0, [r1, #OSiExContext.exinfo]
    ldr r0, [r12, #0]
    str r0, [r1, #4 ]
    ldr r0, [r12, #4]
    str r0, [r1, #8 ]
    ldr r0, [r12, #8]
    str r0, [r1, #12 ]
    ldr r0, [r12, #12]
    str r0, [r1, #16 ]
    ldr r2, [r12, #16]
    bic r2, r2, #1
    add r0, r1, #20
    stmia r0, {r4 - r11}
    str r12, [r1, #OSiExContext.debug[0]]
    ldr r0, [r2, #0]
    str r0, [r1, #OSiExContext.cp15]
    ldr r3, [r2, #4]
    str r3, [r1, #0 ]
    ldr r0, [r2, #8]
    str r0, [r1, #52 ]
    ldr r0, [r2, #12]
    str r0, [r1, #64 ]
    mrs r0, CPSR
    orr r3, r3, #0x80
    bic r3, r3, #0x20
    msr CPSR_cxsf, r3
    str sp, [r1, #56 ]
    str lr, [r1, #60 ]
    mrs r2, SPSR
    str r2, [r1, #OSiExContext.debug[3]]
    msr CPSR_cxsf, r0
    bx lr
}
