/* ov000 row 0x0220325c: 140 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x80 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x84 -> constant 0x022550ff (image word 0x022550ff)
 *   pool +0x88 -> constant 0x91a2b3c5 (image word 0x91a2b3c5)
 *   test +0x24 cmp r1, r12
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220325c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02061944(void);
extern void native_fn_020633bc(void);


asm u32 native_ov000_0220325c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02061944
    mov r4, r0
    bl native_fn_020633bc
    ldr r2, [r0]
    ldr r0, =0x88888889
    ldr r1, =0x022550ff
    umull r0, r12, r2, r0
    mov r12, r12, lsr #4
    cmp r1, r12
    ldr r3, =0x91a2b3c5
    movlo r12, r1
    umull r0, r14, r12, r3
    mov r2, #3600
    mov lr, lr, lsr #11
    umull r1, r0, r2, r14
    umull r0, r5, r12, r3
    ldr r2, =0x88888889
    sub lr, r12, r1
    umull r0, r3, r14, r2
    umull r0, r12, r14, r2
    mov r3, r3, lsr #5
    mov r2, #60
    umull r0, r1, r2, r3
    mov r5, r5, lsr #11
    add r1, r4, #512
    strh r5, [r1, #180]
    mov r12, r12, lsr #5
    strh r12, [r1, #182]
    sub r3, lr, r0
    strh r3, [r1, #184]
    ldmia sp!, {r3, r4, r5, pc}
}
