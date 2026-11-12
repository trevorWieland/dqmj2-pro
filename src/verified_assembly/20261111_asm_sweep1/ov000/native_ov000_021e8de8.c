/* ov000 row 0x021e8de8: 52 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x30 -> native_data_0223526c (image word 0x0223526c)
 *   call +0x20 -> native_fn_021e8b20
 *   test +0x18 cmp ip, #0
 *   memory +0x10 ldrb ip, [r0, #0x274]
 *
 * Why transcribed rather than written as C: table/stride allocated to `r2`/`r1` instead of `lr`/`ip`
 * (6/9-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8de8; the literal pool and
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
extern void native_fn_021e8b20(void);


asm u32 native_ov000_021e8de8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr lr, =native_data_0223526c
    mov ip, #0x2cc
    mla r0, ip, r0, lr
    ldrb ip, [r0, #0x274]
    mov lr, #0
    cmp ip, #0
    beq ov000_021e8de8_L28
    bl native_fn_021e8b20
    mov lr, #1
ov000_021e8de8_L28:
    mov r0, lr
    ldmia sp!, {r3, pc}
}
