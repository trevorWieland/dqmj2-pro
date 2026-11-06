#include "context_00.h"
asm void native_main_02006d98 (register OSContext * context)
{
    stmfd sp !, { lr, r0 }
    add r0, r0, #72
    ldr r1, = native_fn_0200d904
    blx r1
    ldmfd sp !, { lr, r0 }
    mrs r1, cpsr
    bic r1, r1, #0x1f
    orr r1, r1, #0x13 | 0x80 | 0x40
    msr cpsr_c, r1
    ldr r1, [r0], #4 - 0
    msr spsr_fsxc, r1
    ldr sp, [r0, #68 - 4 ]
    ldr lr, [r0, #64 - 4 ]
    ldmia r0, { r0 - r14 }^
    nop
    subs pc, lr, #4
}
