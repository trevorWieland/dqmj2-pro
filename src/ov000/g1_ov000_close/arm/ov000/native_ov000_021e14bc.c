/* ov000 row 0x021e14bc: 292 bytes.
 *
 * What it does: 71 instructions; 1 call(s) to 0x0200235c; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x11c -> constant 0x0000028f (image word 0x0000028f)
 *   pool +0x120 -> constant 0x00000a3e (image word 0x00000a3e)
 *   branch +0x94 -> +0xd0
 *   branch +0xcc -> +0x104
 *   test +0x14 cmp r0, #5
 *   test +0x8c cmp r5, #1
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e14bc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0200235c(void);


asm u32 native_ov000_021e14bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    ldrb r0, [r7, #0x1e0]
    mov r6, r1
    ldr r2, [r7, #0x1f8]
    cmp r0, #5
    ldr r0, [r6, #0x4]
    ldr r1, [r7, #0x1ec]
    mov r4, #1
    moveq r5, #0
    sub r0, r0, r2
    sub r1, r1, r2
    movne r5, r4
    bl native_fn_0200235c
    ldr r12, [r7, #0x1f4]
    ldr r2, [r7, #0x1e8]
    mov r1, #0
    sub r2, r2, r12
    smull r3, r2, r0, r2
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r12, r3
    str r2, [r6]
    ldr r12, [r7, #0x1fc]
    ldr r2, [r7, #0x1f0]
    sub r2, r2, r12
    smull r3, r2, r0, r2
    adds r3, r3, #2048
    adc r0, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r0, lsl #20
    add r0, r12, r2
    str r0, [r6, #0x8]
    cmp r5, #1
    ldr r2, [r6, #0x4]
    bne ov000_021e14bc_Ld0
    ldr r0, [r7, #0x1f8]
    ldr r12, [r6]
    sub r3, r2, r0
    smull r0, r2, r3, r3
    ldr r3, [r7, #0x1f4]
    ldr r5, [r6, #0x8]
    sub r6, r12, r3
    smlal r0, r2, r6, r6
    ldr r3, [r7, #0x1fc]
    sub r3, r5, r3
    smlal r0, r2, r3, r3
    mov r3, r0, lsr #12
    ldr r0, =0x0000028f
    b ov000_021e14bc_L104
ov000_021e14bc_Ld0:
    ldr r0, [r7, #0x1ec]
    ldr r12, [r6]
    sub r3, r2, r0
    smull r0, r2, r3, r3
    ldr r3, [r7, #0x1e8]
    ldr r5, [r6, #0x8]
    sub r6, r12, r3
    smlal r0, r2, r6, r6
    ldr r3, [r7, #0x1f0]
    sub r3, r5, r3
    smlal r0, r2, r3, r3
    mov r3, r0, lsr #12
    ldr r0, =0x00000a3e
ov000_021e14bc_L104:
    orr r3, r3, r2, lsl #20
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    movlt r4, r1
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
