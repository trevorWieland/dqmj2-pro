/* main row 0x020482b4: 84 bytes.
 *
 * What it does: Cluster sibling of 0x020481b8, body-identical except the trailing pool word (0x021d4bb4): the same clamped halfword copy.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x50 -> constant 0x020fb4e8 (image word 0x020fb4e8)
 *   back edge +0x48 -> +0x34
 *   test +0x08 cmp r3, #0x200
 *   test +0x10 cmp r2, #1
 *   test +0x1c cmp lr, #0
 *   test +0x44 cmp r12, lr
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020482b4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the fields, the table and the callee contract are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_020482b4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    add r3, r1, r2
    cmp r3, #0x200
    rsbhi r2, r1, #0x200
    cmp r2, #1
    ldmltia sp!, {r3, pc}
    mov lr, r2, asr #1
    cmp lr, #0
    mov r12, #0
    ldmleia sp!, {r3, pc}
    mov r2, r1, lsr #1
    ldr r1, =0x020fb4e8
    add r1, r1, r2, lsl #1
main_020482b4_L34:
    ldrh r3, [r0], #2
    mov r2, r12, lsl #1
    add r12, r12, #1
    strh r3, [r2, r1]
    cmp r12, lr
    blt main_020482b4_L34
    ldmia sp!, {r3, pc}
}
