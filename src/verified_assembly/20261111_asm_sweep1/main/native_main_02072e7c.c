/* main row 0x02072e7c: 36 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x1c -> native_data_021c5a16 (image word 0x021c5a17)
 *   pool +0x20 -> native_data_021c5a18 (image word 0x021c5a18)
 *   memory +0x0c strb r1, [r2, r3]
 *   memory +0x14 strb r1, [r0, r3]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: base/offset registers permuted (`r3`/`ip` vs `r2`/`r3`)
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02072e7c; the literal pool and
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

extern u8 native_data_021c5a18[];


asm u32 native_main_02072e7c (register u32 a0)
{
    ldr r2, =0x021c5a17
    add r3, r0, r0, lsl #3
    ldr r0, =native_data_021c5a18
    strb r1, [r2, r3]
    mov r1, #1
    strb r1, [r0, r3]
    bx lr
}
