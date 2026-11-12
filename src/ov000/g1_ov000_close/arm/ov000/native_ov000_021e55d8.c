/* ov000 row 0x021e55d8: 364 bytes.
 *
 * What it does: 89 instructions; 1 call(s) to 0x021e561c; loops (back edge at +0x154); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x164 -> constant 0x02232868 (image word 0x02232868)
 *   pool +0x168 -> constant 0x0223255c (image word 0x0223255c)
 *   branch +0x4c -> +0x148
 *   branch +0x5c -> +0x148
 *   branch +0xf0 -> +0x108
 *   branch +0x104 -> +0x118
 *   branch +0x124 -> +0x148
 *   branch +0x144 -> +0x158
 *   back edge +0x154 -> +0x44
 *   test +0x48 cmp r4, #0
 *   test +0x54 cmp r4, r1
 *   test +0x58 cmpne r2, #0
 *   test +0xec cmp r7, #0
 *   test +0xf4 cmp r5, #0
 *   test +0x108 cmp r5, #0
 *   test +0x11c cmp r7, #0
 *   test +0x120 cmpeq r5, #0
 *   test +0x128 cmp r2, #0
 *   test +0x14c cmp r3, #32
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e55d8; the literal pool and
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



asm u32 native_ov000_021e55d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r9, [r0, #0xb8]
    ldr r4, [r0, #0x70]
    ldr r8, [r0, #0xbc]
    rsb r4, r4, r9, lsl #1
    mov r3, #0
    ldr r7, [r0, #0x74]
    str r4, [sp, #0x4]
    rsb r4, r7, r8, lsl #1
    ldr r6, [r0, #0xc0]
    ldr r5, [r0, #0x78]
    ldr r12, =0x02232868
    ldr r8, =0x0223255c
    str r3, [sp, #0x8]
    str r4, [sp]
    rsb r11, r5, r6, lsl #1
ov000_021e55d8_L44:
    ldrh r4, [r12]
    cmp r4, #0
    beq ov000_021e55d8_L148
    ldrb r4, [r12, #0x2]
    cmp r4, r1
    cmpne r2, #0
    bne ov000_021e55d8_L148
    ldr r4, [r12, #0x8]
    ldr r6, [r0, #0x74]
    ldr r5, [r12, #0x4]
    sub r6, r6, r4
    smull r9, r7, r6, r6
    ldr r10, [r0, #0x70]
    ldr r6, [r12, #0xc]
    sub r10, r10, r5
    smlal r9, r7, r10, r10
    ldr r10, [r0, #0x78]
    ldr lr, [r12, #0x10]
    sub r10, r10, r6
    smlal r9, r7, r10, r10
    mov r10, r9, lsr #12
    orr r10, r10, r7, lsl #20
    mov r9, r7, asr #12
    subs r7, r10, lr
    sbcs r7, r9, lr, asr #31
    ldr r9, [sp]
    movlt r7, #1
    sub r4, r9, r4
    smull r10, r9, r4, r4
    ldr r4, [sp, #0x4]
    movge r7, #0
    sub r4, r4, r5
    smlal r10, r9, r4, r4
    sub r4, r11, r6
    smlal r10, r9, r4, r4
    mov r4, r10, lsr #12
    orr r4, r4, r9, lsl #20
    mov r5, r9, asr #12
    subs r4, r4, lr
    sbcs r4, r5, lr, asr #31
    movlt r5, #1
    movge r5, #0
    cmp r7, #0
    beq ov000_021e55d8_L108
    cmp r5, #0
    movne r4, #4
    strneh r4, [r8, #2]
    moveq r4, #1
    b ov000_021e55d8_L118
ov000_021e55d8_L108:
    cmp r5, #0
    movne r4, #2
    strneh r4, [r8, #2]
    moveq r4, #0
ov000_021e55d8_L118:
    streqh r4, [r8, #2]
    cmp r7, #0
    cmpeq r5, #0
    beq ov000_021e55d8_L148
    cmp r2, #0
    ldrneh r1, [r12]
    ldrne r0, =0x0223255c
    strneh r1, [r0, #4]
    ldr r0, =0x0223255c
    ldrh r0, [r0, #2]
    str r0, [sp, #0x8]
    b ov000_021e55d8_L158
ov000_021e55d8_L148:
    add r3, r3, #1
    cmp r3, #32
    add r12, r12, #20
    blt ov000_021e55d8_L44
ov000_021e55d8_L158:
    ldr r0, [sp, #0x8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
