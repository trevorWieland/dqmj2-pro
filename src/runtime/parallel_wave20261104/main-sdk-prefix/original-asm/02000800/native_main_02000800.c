#include "context_00.h"
__declspec(weak) asm void native_main_02000800(void)
{
    mov r12, #0x04000000
    str r12, [r12, #0x208 ]
@wait_vcount_0:
    ldrh r0, [r12, #0x006 ]
    cmp r0, #0
    bne @wait_vcount_0
    bl native_fn_02000a78
    mov r0, #0x13
    msr cpsr_c, r0
    ldr r0, = native_data_main_027e0000
    add r0, r0, #0x3FC0
    mov sp, r0
    mov r0, #0x12
    msr cpsr_c, r0
    ldr r0, = native_data_main_027e0000
    add r0, r0, #0x3FC0
    sub r0, r0, #0x40
    sub sp, r0, #4
    tst sp, #4
    subeq sp, sp, #4
    ldr r1, = native_data_main_00001000
    sub r1, r0, r1
    mov r0, #0x1f
    msr cpsr_csfx, r0
    sub sp, r1, #4
    mov r0, #0
    ldr r1, = native_data_main_027e0000
    mov r2, #0x4000
    bl native_fn_0200093c
    mov r0, #0
    ldr r1, = 0x05000000
    mov r2, #(0x05000400-0x05000000)
    bl native_fn_0200093c
    mov r0, #0x0200
    ldr r1, = 0x07000000
    mov r2, #(0x07000400-0x07000000)
    bl native_fn_0200093c
    ldr r1, = native_data_main_02000b68.field_0000
    ldr r0, [r1, #20]
    bl native_fn_02000950
    bl native_fn_020009fc
    ldr r0, = native_data_main_02000b68.field_0000
    ldr r1, [r0, #12]
    ldr r2, [r0, #16]
    mov r3, r1
    mov r0, #0
@1:
    cmp r1, r2
    strcc r0, [r1], #4
    bcc @1
    bic r1, r3, #32 - 1
@cacheflush:
    mcr p15, 0, r0, c7, c10, 4
    mcr p15, 0, r1, c7, c5, 1
    mcr p15, 0, r1, c7, c14, 1
    add r1, r1, #32
    cmp r1, r2
    blt @cacheflush
    ldr r1, = (0x02000000 + 0x007fff9c)
    str r0, [r1, #0]
    ldr r1, = native_data_main_027e0000
    add r1, r1, #0x3FC0
    add r1, r1, #0x3c
    ldr r0, = native_fn_01ff8000
    str r0, [r1, #0]
    bl native_fn_02026a90
    bl native_fn_02000b60
    bl native_fn_02026a94
    ldr r1, = native_fn_02000c34
    ldr lr, = 0xffff0000
    tst sp, #4
    subne sp, sp, #4
    bx r1
}
