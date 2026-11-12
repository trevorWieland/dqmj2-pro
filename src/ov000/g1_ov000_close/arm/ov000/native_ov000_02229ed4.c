/* ov000 row 0x02229ed4: 100 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x02229f08, 0x02229eec, 0x02229f30, +1 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x34
 *   branch +0x24 -> +0x34
 *   back edge +0x30 -> +0x18
 *   branch +0x3c -> +0x5c
 *   branch +0x4c -> +0x5c
 *   back edge +0x58 -> +0x40
 *   test +0x0c cmp r1, #0
 *   test +0x1c cmp r5, r12
 *   test +0x2c cmp r4, r1
 *   test +0x34 cmp r3, #0
 *   test +0x44 cmp r5, r0
 *   test +0x54 cmp r1, r3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02229ed4; the literal pool and
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



asm u32 native_ov000_02229ed4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov lr, #0
    mov r4, lr
    cmp r1, #0
    ldr r5, [sp, #0x10]
    ble ov000_02229ed4_L34
ov000_02229ed4_L18:
    ldrb r12, [r0, r4, lsl #1]
    cmp r5, r12
    moveq lr, #1
    beq ov000_02229ed4_L34
    add r4, r4, #1
    cmp r4, r1
    blt ov000_02229ed4_L18
ov000_02229ed4_L34:
    cmp r3, #0
    mov r1, #0
    ble ov000_02229ed4_L5c
ov000_02229ed4_L40:
    ldrb r0, [r2, r1, lsl #1]
    cmp r5, r0
    moveq lr, #1
    beq ov000_02229ed4_L5c
    add r1, r1, #1
    cmp r1, r3
    blt ov000_02229ed4_L40
ov000_02229ed4_L5c:
    mov r0, lr
    ldmia sp!, {r3, r4, r5, pc}
}
