#include "context_00.h"
asm void native_main_020077dc (void)
{
    ldr r12, = native_data_main_020e3644.field_0000
    ldr r12, [r12]
    cmp r12, #0
    movne lr, pc
    bxne r12
    ldr r12, = (0x01ff8000 + 0x8000)
    stmfd r12 !, {r0 - r3, sp, lr}
    and r0, sp, #1
    mov sp, r12
    mrs r1, CPSR
    and r1, r1, #0x1f
    teq r1, #0x17
    bne @10
    bl native_fn_02007850
    b usr_return
@10:
    teq r1, #0x1b
    bne usr_return
    bl native_fn_02007850
usr_return:
    ldr r12, = native_data_main_020e3644.field_0000
    ldr r12, [r12]
    cmp r12, #0
@1:
    beq @1
@2:
    mov r0, r0
    b @2
    ldmfd sp !, {r0 - r3, r12, lr}
    mov sp, r12
    bx lr
}
