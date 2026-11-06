typedef unsigned int u32;
extern u32 func_ov004_021d7f54(u32 key_reference, u32 target_reference, u32 size_reference);
extern u32 func_ov004_021d8014(u32 key_reference, u32 target_reference, u32 size_reference);

asm u32 native_ov004_021d80ec(void) {
    stmdb sp!, {r0, r1, r2, r3}
    str r10, [r12, #16]
    mov r10, r12
    str lr, [r10, #0]
    ldmib r10, {r0, r1, r2}
    bl func_ov004_021d7f54
    mov r12, r0
    ldmia sp!, {r0, r1, r2, r3}
    blx r12
    stmdb sp!, {r4}
    mov r4, r0
    ldmib r10, {r0, r1, r2}
    bl func_ov004_021d8014
    str r0, [r10, #4]
    mov r0, r4
    ldmia sp!, {r4}
    ldr lr, [r10, #0]
    str sp, [r10, #0]
    ldr r10, [r10, #16]
    bx lr
}
