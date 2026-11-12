/* ov001 row 0x0220294c: 92 bytes.
 *
 * What it does: 23 instructions; 1 call(s) to 0x0220294c; loops (back edge at +0x1c); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 1 call (23 instructions, 1 call, 5 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x0c -> +0x18
 *   branch +0x14 -> +0x20
 *   back edge +0x1c -> +0x10
 *   branch +0x24 -> +0x54
 *   branch +0x30 -> +0x54
 *   back edge +0x4c -> +0x00
 *   test +0x18 cmp lr, #0
 *   test +0x20 cmp r2, #0
 *   test +0x2c cmp r2, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220294c; the literal pool and
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



asm u32 native_ov001_0220294c (register u32 a0)
{
ov001_0220294c_L0:
    stmdb sp!, {r3, lr}
    mov lr, r2
    mov r2, #0
    b ov001_0220294c_L18
ov001_0220294c_L10:
    mov r2, #1
    b ov001_0220294c_L20
ov001_0220294c_L18:
    cmp lr, #0
    bge ov001_0220294c_L10
ov001_0220294c_L20:
    cmp r2, #0
    bne ov001_0220294c_L54
    ldrsb r2, [sp, #8]
    cmp r2, #0
    beq ov001_0220294c_L54
    sub r2, r3, #1
    mov r2, r2, lsl #24
    mov r12, #0
    mov r2, r2, asr #24
    and r3, lr, #255
    str r12, [sp]
    bl ov001_0220294c_L0
    mov lr, r0
ov001_0220294c_L54:
    mov r0, lr
    ldmia sp!, {r3, pc}
}
