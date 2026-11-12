/* ov001 row 0x021dca04: 80 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x021dca3c, 0x021dca14; loops (back edge at +0x40); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (19 instructions, 2 calls, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x4c -> constant 0x00007fff (image word 0x00007fff)
 *   branch +0x28 -> +0x38
 *   back edge +0x40 -> +0x10
 *   test +0x20 cmp r1, lr
 *   test +0x3c cmp r12, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dca04; the literal pool and
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



asm u32 native_ov001_021dca04 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov lr, #0
    ldr r2, =0x00007fff
    mov r12, lr
ov001_021dca04_L10:
    add r1, r0, r12, lsl #1
    add r1, r1, #768
    ldrsh r3, [r1, #78]
    sub r1, r2, r3
    cmp r1, lr
    movlt lr, r2
    blt ov001_021dca04_L38
    add r1, lr, r3
    mov r1, r1, lsl #16
    mov lr, r1, asr #16
ov001_021dca04_L38:
    add r12, r12, #1
    cmp r12, #3
    blt ov001_021dca04_L10
    mov r0, lr
    ldmia sp!, {r3, pc}
}
