/* ov005 row 0x021df4c4: 36 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x20 -> constant 0x88888889 (image word 0x88888889)
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov005.bin at 0x021df4c4; the literal pool and
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

extern void native_fn_020633bc(void);
extern void native_fn_021db5d0(void);


asm u32 native_ov005_021df4c4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_020633bc
    ldr r2, [r0]
    ldr r0, =0x88888889
    umull r1, r0, r2, r0
    mov r0, r0, lsr #4
    bl native_fn_021db5d0
    ldmia sp!, {r3, pc}
}
