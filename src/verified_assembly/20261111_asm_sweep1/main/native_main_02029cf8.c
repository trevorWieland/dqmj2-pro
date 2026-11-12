/* main row 0x02029cf8: 52 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x2c -> native_data_020edd0c (image word 0x020edd0c)
 *   pool +0x30 -> native_data_04000350 (image word 0x04000350)
 *   memory +0x08 ldr r3, [r1, #0x14]
 *   memory +0x1c str r3, [r1, #0x14]
 *   memory +0x24 str r3, [r2]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: same bitfield-replace family, pool bases swapped
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02029cf8; the literal pool and
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


asm u32 native_main_02029cf8 (register u32 a0)
{
    ldr r1, =native_data_020edd0c
    ldr r2, =native_data_04000350
    ldr r3, [r1, #0x14]
    and ip, r3, #0x3f000000
    bic r3, r3, #0x3f000000
    orr r3, r3, r0, lsl #24
    mov ip, ip, lsr #0x18
    str r3, [r1, #0x14]
    and r0, ip, #0xff
    str r3, [r2]
    bx lr
}
