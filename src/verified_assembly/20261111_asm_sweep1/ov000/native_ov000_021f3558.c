/* ov000 row 0x021f3558: 40 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   call +0x08 -> native_fn_021f3544
 *   test +0x0c cmp r4, #0
 *   memory +0x18 ldrh r0, [r0, #4]
 *
 * Why transcribed rather than written as C: bit extraction compiles shorter; the image `lsl #31`/`lsr #31`
 * form is not reproduced
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3558; the literal pool and
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

extern void native_fn_021f3544(void);


asm u32 native_ov000_021f3558 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    bl native_fn_021f3544
    cmp r4, #0
    movne r0, #0
    ldmneia sp!, {r4, pc}
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #0x1f
    mov r0, r0, lsr #0x1f
    ldmia sp!, {r4, pc}
}
