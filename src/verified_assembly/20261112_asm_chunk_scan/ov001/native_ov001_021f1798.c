/* ov001 row 0x021f1798: 108 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x68 -> constant 0x88888889 (image word 0x88888889)
 *   test +0x08 cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1798; the literal pool and
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

extern void native_fn_021e2c10(void);
extern void native_fn_021f19f0(void);
extern void native_fn_02203408(void);
extern void native_fn_021e2bac(void);
extern void native_fn_02048094(void);
extern void native_fn_0204a04c(void);


asm u32 native_ov001_021f1798 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_021e2c10
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r0, #1
    bl native_fn_021f19f0
    mov r5, r0
    ldr r0, [r5]
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    bl native_fn_02203408
    mov r4, r0
    bl native_fn_021e2bac
    ldr r1, =0x88888889
    umull r1, r2, r0, r1
    subs r0, r4, r2, lsr #4
    movmi r0, #0
    mov r1, #32
    bl native_fn_02048094
    ldr r0, [r5]
    mov r1, #1
    ldr r0, [r0, #0x4]
    mov r2, r1
    mov r3, #11
    bl native_fn_0204a04c
    ldmia sp!, {r3, r4, r5, pc}
}
