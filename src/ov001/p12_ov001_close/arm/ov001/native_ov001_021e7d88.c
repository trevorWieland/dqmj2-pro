/* ov001 row 0x021e7d88: 116 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x021e7da4, 0x021e7dd8; loops (back edge at +0x44); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (26 instructions, 2 calls, 0 branches, 2 back edges, 3 literal slots).
 *
 *   pool +0x68 -> constant 0x02238d1c (image word 0x02238d1c)
 *   pool +0x6c -> constant 0x02238d2e (image word 0x02238d2e)
 *   pool +0x70 -> constant 0x02238d40 (image word 0x02238d40)
 *   back edge +0x44 -> +0x1c
 *   back edge +0x60 -> +0x50
 *   test +0x38 cmp r2, #3
 *   test +0x5c cmp lr, #6
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e7d88; the literal pool and
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



asm u32 native_ov001_021e7d88 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r2, #0
    ldr r3, =0x02238d1c
    ldr r12, =0x02238d2e
    mov r1, #6
    mvn r0, #0
    mov lr, r2
ov001_021e7d88_L1c:
    strh r1, [r3]
    strh r1, [r12]
    strb r0, [r3, #0x3]
    strb r0, [r12, #0x3]
    add r2, r2, #1
    strb lr, [r3, #0x4]
    strb lr, [r12, #0x4]
    cmp r2, #3
    add r3, r3, #6
    add r12, r12, #6
    blt ov001_021e7d88_L1c
    ldr r1, =0x02238d40
    mvn r2, #0
ov001_021e7d88_L50:
    add r0, r1, lr, lsl #2
    add lr, lr, #1
    strb r2, [r0, #0x1]
    cmp lr, #6
    blt ov001_021e7d88_L50
    ldmia sp!, {r3, pc}
}
