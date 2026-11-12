/* ov000 row 0x021d9af4: 64 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x3c -> native_data_0223042c (image word 0x0223042c)
 *   back edge +0x34 -> +0x14
 *   test +0x24 cmp r3, #0
 *   test +0x30 cmp lr, #3
 *   memory +0x1c ldr r3, [r1, #0x7a8]
 *   memory +0x28 strne r2, [r1, #0x7a8]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: `0x17a8` field offset folded into the literal, dropping the
 * image `add #0x1000` (76 vs 64 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d9af4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0223042c[];


asm u32 native_ov000_021d9af4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #0
    ldr ip, =native_data_0223042c
    mov lr, r0
    mov r2, r0
ov000_021d9af4_L14:
    add r1, ip, lr, lsl #2
    add r1, r1, #0x1000
    ldr r3, [r1, #0x7a8]
    add lr, lr, #1
    cmp r3, #0
    strne r2, [r1, #0x7a8]
    addne r0, r0, #1
    cmp lr, #3
    blt ov000_021d9af4_L14
    ldmia sp!, {r3, pc}
}
