/* ov001 row 0x021e76b4: 68 bytes.
 *
 * What it does: 13 instructions; no calls; no back edge; returns through bx lr; 4 literal slot(s) in the extent
 *
 * Decoded shape: straight-line scalar (13 instructions, 0 calls, 0 branches, 0 back edges, 4 literal slots).
 *
 *   pool +0x34 -> constant 0x02238d40 (image word 0x02238d40)
 *   pool +0x38 -> constant 0x02238d41 (image word 0x02238d41)
 *   pool +0x3c -> constant 0x02238d1c (image word 0x02238d1c)
 *   pool +0x40 -> constant 0x02238d2e (image word 0x02238d2e)
 *   test +0x14 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e76b4; the literal pool and
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



asm u32 native_ov001_021e76b4 (register u32 a0)
{
    ldr r1, =0x02238d40
    mov r2, r0, lsl #2
    ldrsb r0, [r1, r2]
    ldr r1, =0x02238d41
    ldrsb r2, [r1, r2]
    cmp r0, #0
    mov r0, #6
    muleq r1, r2, r0
    ldreq r0, =0x02238d1c
    mulne r1, r2, r0
    ldrne r0, =0x02238d2e
    ldrh r0, [r0, r1]
    bx lr
}
