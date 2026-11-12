/* ov006 row 0x021e8a54: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x88 -> constant 0xaaaaaaab (image word 0xaaaaaaab)
 *   test +0x68 cmp r4, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e8a54; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e8814(void);


asm u32 native_ov006_021e8a54 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r4, =0x2aaaaaab
    mov lr, r1
    smull r3, r1, r4, r0
    sub r5, r4, #-2147483648
    umull r3, r6, r14, r5
    smull r3, r12, r4, r0
    add r1, r1, r0, lsr #31
    mov r5, #6
    smull r1, r3, r5, r1
    mov r6, r6, lsr #2
    umull r4, r3, r5, r6
    mov r3, r2
    subs r6, lr, r4
    ldr r2, =0xaaaaaaab
    movne r5, #1
    umull r2, r4, r14, r2
    moveq r5, #0
    add r12, r12, r0, lsr #31
    subs r6, r12, #1
    add r2, r5, r4, lsr #2
    submi r6, r2, #1
    sub r1, r0, r1
    mov r2, #6
    mla r4, r6, r2, r1
    sub r1, lr, #1
    cmp r4, r1
    movge r4, r1
    mov r1, r4
    mov r2, lr
    bl native_fn_021e8814
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
