/* ov000 row 0x021dd2a4: 412 bytes.
 *
 * What it does: Copies a 3-register block to an optional destination under a condition in 2 predicated moves.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x198 -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0xd4 -> +0xe8
 *   test +0x15c cmp r4, #0
 *   18 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dd2a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02002618(void);


asm u32 native_ov000_021dd2a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #24
    mov r5, r2
    ldr r6, [r0]
    ldr r4, [r5]
    mov r2, #0
    sub r4, r6, r4
    str r4, [sp, #0xc]
    ldr r7, [r0, #0x4]
    ldr r6, [r5, #0x4]
    mov r4, r3
    sub r3, r7, r6
    str r3, [sp, #0x10]
    ldr r6, [r0, #0x8]
    ldr r3, [r5, #0x8]
    add r0, sp, #12
    sub r3, r6, r3
    str r3, [sp, #0x14]
    ldr r6, [r1]
    ldr r3, [r5]
    sub r3, r6, r3
    str r3, [sp]
    ldr r6, [r1, #0x4]
    ldr r3, [r5, #0x4]
    sub r3, r6, r3
    str r3, [sp, #0x4]
    ldr r6, [r1, #0x8]
    ldr r3, [r5, #0x8]
    mov r1, r0
    sub r3, r6, r3
    str r3, [sp, #0x8]
    str r2, [sp, #0x10]
    str r2, [sp, #0x4]
    bl native_fn_02002618
    add r0, sp, #0
    mov r1, r0
    bl native_fn_02002618
    ldr r1, [sp, #0x8]
    ldr r0, [sp]
    rsb r12, r1, #0
    ldr r2, [sp, #0x10]
    ldr r1, [sp, #0x4]
    ldr r3, [sp, #0xc]
    smull r7, r6, r2, r1
    smlal r7, r6, r3, r12
    ldr r1, [sp, #0x14]
    str r12, [sp]
    smlal r7, r6, r1, r0
    adds r2, r7, #2048
    adc r1, r6, #0
    mov r2, r2, lsr #12
    str r0, [sp, #0x8]
    orrs r2, r2, r1, lsl #20
    bpl ov000_021dd2a4_Le8
    rsb r1, r12, #0
    rsb r0, r0, #0
    str r1, [sp]
    str r0, [sp, #0x8]
ov000_021dd2a4_Le8:
    ldr r0, [sp]
    ldr r1, =0x0000019a
    ldr r3, [sp, #0x4]
    umull r12, r6, r0, r1
    mov r0, r0, asr #31
    adds r7, r12, #2048
    mla r6, r0, r1, r6
    umull r12, r14, r3, r1
    mov r0, r3, asr #31
    adc r3, r6, #0
    mla r14, r0, r1, r14
    adds r6, r12, #2048
    mov r0, r7, lsr #12
    orr r0, r0, r3, lsl #20
    ldr r2, [sp, #0x8]
    adc lr, lr, #0
    umull r12, r3, r2, r1
    mov r2, r2, asr #31
    mov r6, r6, lsr #12
    orr r6, r6, lr, lsl #20
    mla r3, r2, r1, r3
    adds r12, r12, #2048
    adc r1, r3, #0
    mov r2, r12, lsr #12
    orr r2, r2, r1, lsl #20
    str r0, [sp]
    str r6, [sp, #0x4]
    str r2, [sp, #0x8]
    ldr r1, [r5]
    cmp r4, #0
    add r0, r0, r1
    str r0, [sp, #0xc]
    ldr r0, [r5, #0x4]
    add r0, r6, r0
    str r0, [sp, #0x10]
    ldr r0, [r5, #0x8]
    add r0, r2, r0
    str r0, [sp, #0x14]
    addne r0, sp, #12
    ldmneia r0, {r0, r1, r2}
    stmneia r4, {r0, r1, r2}
    mov r0, #1
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
