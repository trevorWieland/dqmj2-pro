/* ov001 row 0x02203418: 68 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x40 -> constant 0x88888889 (image word 0x88888889)
 *   branch +0x24 -> +0x38
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r4, #0
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203418; the literal pool and
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

extern void native_fn_02203408(void);
extern void native_fn_021e2bac(void);
extern void native_fn_021e2c10(void);


asm u32 native_ov001_02203418 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_02203408
    mov r4, r0
    bl native_fn_021e2bac
    ldr r1, =0x88888889
    umull r1, r2, r0, r1
    sub r4, r4, r2, lsr #4
    bl native_fn_021e2c10
    cmp r0, #0
    beq ov001_02203418_L38
    cmp r4, #0
    movle r0, #1
    movgt r0, #0
    ldmia sp!, {r4, pc}
ov001_02203418_L38:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
