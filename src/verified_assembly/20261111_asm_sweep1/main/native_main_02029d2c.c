/* main row 0x02029d2c: 48 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x28 -> native_data_020edd0c (image word 0x020edd0c)
 *   pool +0x2c -> native_data_04000350 (image word 0x04000350)
 *   memory +0x08 ldr ip, [r1, #0x14]
 *   memory +0x18 str r3, [r1, #0x14]
 *   memory +0x20 str r3, [r2]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: the two pool bases land in `r2`/`r1` swapped
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02029d2c; the literal pool and
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

extern u8 native_data_020edd0c[];
extern u8 native_data_04000350[];


asm u32 native_main_02029d2c (register u32 a0)
{
    ldr r1, =native_data_020edd0c
    ldr r2, =native_data_04000350
    ldr ip, [r1, #0x14]
    bic r3, ip, #0x8000
    orr r3, r3, r0, lsl #15
    and ip, ip, #0x8000
    str r3, [r1, #0x14]
    mov r0, ip, lsr #0xf
    str r3, [r2]
    bx lr
}
