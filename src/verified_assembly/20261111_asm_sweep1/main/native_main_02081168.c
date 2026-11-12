/* main row 0x02081168: 52 bytes.
 *
 * Decoded shape: guarded entry: bxne at +0x0c returns before the body.
 *
 *   pool +0x2c -> native_data_021c6dfc (image word 0x021c6dfc)
 *   pool +0x30 -> native_data_020de580 (image word 0x020de580)
 *   test +0x08 cmp r1, #0
 *   memory +0x04 ldr r1, [r2, #0xc]
 *   memory +0x14 strb r1, [r2, #1]
 *   memory +0x1c strb r0, [r2, #5]
 *   memory +0x24 strb r0, [r1]
 *   3 store instruction(s)
 *
 * Why transcribed rather than written as C: final byte store allocated to `r3` where the image uses `r0`
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02081168; the literal pool and
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

extern u8 native_data_020de580[];
extern u8 native_data_021c6dfc[];


asm u32 native_main_02081168 (register u32 a0)
{
    ldr r2, =native_data_021c6dfc
    ldr r1, [r2, #0xc]
    cmp r1, #0
    bxne lr
    mov r1, #6
    strb r1, [r2, #1]
    ldr r1, =native_data_020de580
    strb r0, [r2, #5]
    mov r0, #1
    strb r0, [r1]
    bx lr
}
