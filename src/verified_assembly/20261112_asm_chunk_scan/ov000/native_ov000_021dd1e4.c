/* ov000 row 0x021dd1e4: 192 bytes.
 *
 * What it does: Copies a 3-register block to an optional destination under a condition in 2 predicated moves.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0xbc -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x28 -> +0xb4
 *   branch +0x88 -> +0xa4
 *   branch +0xa0 -> +0xb4
 *   back edge +0xb0 -> +0x3c
 *   test +0x20 cmp r1, #0
 *   test +0x8c cmp r11, #0
 *   test +0xa8 cmp r6, r1
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dd1e4; the literal pool and
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



asm u32 native_ov000_021dd1e4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r4, =0x0223142c
    mov r3, #0
    str r3, [sp]
    ldr r3, [r4, #0x79c]
    mov r11, r2
    ldr r2, [r3, #0x18c]
    ldr r6, [sp]
    cmp r1, #0
    add r7, r3, r2
    ble ov000_021dd1e4_Lb4
    ldr r9, [r0]
    ldmib r0, {r8, r10}
    mov r2, #0
    mov r0, #2048
ov000_021dd1e4_L3c:
    ldmia r7, {r3, r4}
    sub r5, r8, r4
    smull r4, r14, r5, r5
    sub r3, r9, r3
    smlal r4, r14, r3, r3
    ldr r3, [r7, #0x8]
    ldr r5, [r7, #0x14]
    sub r3, r10, r3
    smlal r4, r14, r3, r3
    smull r12, r3, r5, r5
    adds r5, r12, r0
    mov r4, r4, lsr #12
    adc r3, r3, r2
    mov r5, r5, lsr #12
    orr r5, r5, r3, lsl #20
    orr r4, r4, lr, lsl #20
    subs r3, r4, r5
    mov r3, r5, asr #31
    rscs r3, r3, lr, asr #12
    bge ov000_021dd1e4_La4
    cmp r11, #0
    ldmneia r7, {r0, r1, r2}
    stmneia r11, {r0, r1, r2}
    mov r0, #1
    str r0, [sp]
    b ov000_021dd1e4_Lb4
ov000_021dd1e4_La4:
    add r6, r6, #1
    cmp r6, r1
    add r7, r7, #24
    blt ov000_021dd1e4_L3c
ov000_021dd1e4_Lb4:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
