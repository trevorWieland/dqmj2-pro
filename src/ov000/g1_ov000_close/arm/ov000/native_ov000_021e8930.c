/* ov000 row 0x021e8930: 228 bytes.
 *
 * What it does: 56 instructions; 2 call(s) to 0x021e8a08, 0x021e8948; loops (back edge at +0xd4); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x0223526c (image word 0x0223526c)
 *   branch +0x30 -> +0xc8
 *   branch +0x88 -> +0xc8
 *   branch +0xc4 -> +0xd8
 *   back edge +0xd4 -> +0x18
 *   test +0x1c cmp r3, #0
 *   test +0x24 cmpne r3, #0
 *   test +0x2c cmpne r3, #3
 *   test +0x84 cmp r3, r6
 *   test +0xb8 cmp r3, r5
 *   test +0xcc cmp r9, #8
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8930; the literal pool and
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



asm u32 native_ov000_021e8930 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r2, #0
    ldr r10, =0x0223526c
    str r2, [sp]
    mov r9, r2
    mov r11, #2048
ov000_021e8930_L18:
    ldrb r3, [r10, #0x274]
    cmp r3, #0
    ldrneb r3, [r10, #0x1e2]
    cmpne r3, #0
    ldrneb r3, [r10, #0x2a9]
    cmpne r3, #3
    beq ov000_021e8930_Lc8
    ldr r8, [r10, #0x74]
    ldr r3, [r0, #0x4]
    ldr lr, [r10, #0x29c]
    sub r3, r8, r3
    smull r5, r4, r3, r3
    ldr r7, [r10, #0x70]
    ldr r6, [r0]
    smull r12, r3, r14, r14
    sub r6, r7, r6
    smlal r5, r4, r6, r6
    adds r6, r12, r11
    ldr r12, [r10, #0x78]
    adc r3, r3, r2
    mov r6, r6, lsr #12
    orr r6, r6, r3, lsl #20
    ldr r3, [r0, #0x8]
    sub r3, r12, r3
    smlal r5, r4, r3, r3
    mov r3, r5, lsr #12
    orr r3, r3, r4, lsl #20
    cmp r3, r6
    bge ov000_021e8930_Lc8
    ldr r4, [r1, #0x4]
    ldr r6, [r1]
    sub r8, r8, r4
    smull r5, r4, r8, r8
    sub r6, r7, r6
    smlal r5, r4, r6, r6
    ldr r6, [r1, #0x8]
    sub r6, r12, r6
    smlal r5, r4, r6, r6
    mov r5, r5, lsr #12
    orr r5, r5, r4, lsl #20
    cmp r3, r5
    movle r0, #1
    strle r0, [sp]
    ble ov000_021e8930_Ld8
ov000_021e8930_Lc8:
    add r9, r9, #1
    cmp r9, #8
    add r10, r10, #716
    blt ov000_021e8930_L18
ov000_021e8930_Ld8:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
