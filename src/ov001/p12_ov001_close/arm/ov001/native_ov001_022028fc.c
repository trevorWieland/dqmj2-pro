/* ov001 row 0x022028fc: 80 bytes.
 *
 * What it does: 20 instructions; 2 call(s) to 0x0220290c, 0x022028fc; loops (back edge at +0x1c); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 2 calls (20 instructions, 2 calls, 4 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x0c -> +0x18
 *   branch +0x14 -> +0x20
 *   back edge +0x1c -> +0x10
 *   branch +0x24 -> +0x48
 *   branch +0x30 -> +0x48
 *   back edge +0x40 -> +0x00
 *   test +0x18 cmp r12, r3
 *   test +0x20 cmp r2, #0
 *   test +0x2c cmp r2, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022028fc; the literal pool and
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



asm u32 native_ov001_022028fc (register u32 a0)
{
ov001_022028fc_L0:
    stmdb sp!, {r3, lr}
    mov r12, r2
    mov r2, #0
    b ov001_022028fc_L18
ov001_022028fc_L10:
    mov r2, #1
    b ov001_022028fc_L20
ov001_022028fc_L18:
    cmp r12, r3
    blt ov001_022028fc_L10
ov001_022028fc_L20:
    cmp r2, #0
    bne ov001_022028fc_L48
    ldrsb r2, [sp, #8]
    cmp r2, #0
    beq ov001_022028fc_L48
    mov r2, #0
    and r3, r12, #255
    str r2, [sp]
    bl ov001_022028fc_L0
    mov r12, r0
ov001_022028fc_L48:
    mov r0, r12
    ldmia sp!, {r3, pc}
}
