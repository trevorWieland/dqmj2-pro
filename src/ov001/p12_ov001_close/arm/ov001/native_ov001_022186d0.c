/* ov001 row 0x022186d0: 108 bytes.
 *
 * What it does: 27 instructions; 3 call(s) to 0x02218734, 0x022186ec, 0x02218714; loops (back edge at +0x38); returns through bx lr
 *
 * Decoded shape: loop with 3 calls (27 instructions, 3 calls, 2 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x0c -> +0x40
 *   branch +0x18 -> +0x64
 *   back edge +0x38 -> +0x1c
 *   branch +0x3c -> +0x64
 *   back edge +0x60 -> +0x44
 *   test +0x08 cmp r2, #1
 *   test +0x14 cmp r12, #0
 *   test +0x24 cmp r1, r2
 *   test +0x34 cmp r3, r12
 *   test +0x48 cmp r1, r0
 *   test +0x58 cmp r3, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022186d0; the literal pool and
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



asm u32 native_ov001_022186d0 (register u32 a0)
{
    ldrb r2, [r0, #0x322]
    mov r3, #0
    cmp r2, #1
    beq ov001_022186d0_L40
    ldrb r12, [r0, #0x323]
    cmp r12, #0
    ble ov001_022186d0_L64
ov001_022186d0_L1c:
    add r2, r0, r3
    ldrb r2, [r2, #0x35e]
    cmp r1, r2
    moveq r0, #1
    bxeq lr
    add r3, r3, #1
    cmp r3, r12
    blt ov001_022186d0_L1c
    b ov001_022186d0_L64
ov001_022186d0_L40:
    ldr r2, [r0, #0x1e8]
ov001_022186d0_L44:
    ldrb r0, [r2, #0x8]
    cmp r1, r0
    moveq r0, #1
    bxeq lr
    add r3, r3, #1
    cmp r3, #6
    add r2, r2, #1
    blt ov001_022186d0_L44
ov001_022186d0_L64:
    mov r0, #0
    bx lr
}
