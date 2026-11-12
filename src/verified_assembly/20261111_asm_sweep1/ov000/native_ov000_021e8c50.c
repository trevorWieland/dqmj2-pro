/* ov000 row 0x021e8c50: 48 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x2c -> native_data_0223526c (image word 0x0223526c)
 *   call +0x20 -> native_fn_02041f34
 *   test +0x14 cmp ip, #0
 *   memory +0x10 ldrb ip, [r0, #0x274]
 *
 * Why transcribed rather than written as C: table/stride allocated to `r2`/`r1` instead of `lr`/`ip`
 * (6/9-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8c50; the literal pool and
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

extern u8 native_data_0223526c[];
extern void native_fn_02041f34(void);


asm u32 native_ov000_021e8c50 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr lr, =native_data_0223526c
    mov ip, #0x2cc
    mla r0, ip, r0, lr
    ldrb ip, [r0, #0x274]
    cmp ip, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_02041f34
    mov r0, #1
    ldmia sp!, {r3, pc}
}
