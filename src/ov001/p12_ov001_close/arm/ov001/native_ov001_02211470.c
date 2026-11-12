/* ov001 row 0x02211470: 80 bytes.
 *
 * What it does: 18 instructions; 1 call(s) to 0x02211488; loops (back edge at +0x3c); returns through bx lr; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (18 instructions, 1 call, 1 branch, 1 back edge, 2 literal slots).
 *
 *   pool +0x48 -> constant 0x0223e124 (image word 0x0223e124)
 *   pool +0x4c -> constant 0x0223e130 (image word 0x0223e130)
 *   branch +0x20 -> +0x34
 *   back edge +0x3c -> +0x18
 *   test +0x1c cmp r1, r0
 *   test +0x24 cmp r12, r3
 *   test +0x38 cmp r12, #8
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211470; the literal pool and
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



asm u32 native_ov001_02211470 (register u32 a0)
{
    ldr r2, [r0, #0x2c]
    ldr r1, =0x0223e124
    mov r12, #0
    ldrb r3, [r1, r2]
    ldr r1, =0x0223e130
    add r2, r1, r2, lsl #5
ov001_02211470_L18:
    ldr r1, [r2, r12, lsl #2]
    cmp r1, r0
    bne ov001_02211470_L34
    cmp r12, r3
    moveq r0, #1
    movne r0, #0
    bx lr
ov001_02211470_L34:
    add r12, r12, #1
    cmp r12, #8
    blt ov001_02211470_L18
    mov r0, #0
    bx lr
}
