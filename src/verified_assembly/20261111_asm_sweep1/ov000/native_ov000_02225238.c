/* ov000 row 0x02225238: 56 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x30 -> native_data_022468b8 (image word 0x022468b8)
 *   pool +0x34 -> native_data_02246aa8 (image word 0x02246aa8)
 *   test +0x10 cmp r2, #0
 *   test +0x24 cmp r1, #0
 *   memory +0x08 ldr r2, [r1, #4]
 *   memory +0x18 strgt r0, [r1, #4]
 *   memory +0x1c ldrb r1, [r3, #0x192]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: block pointer rotation after the two literal loads (24-byte
 * diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225238; the literal pool and
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

extern u8 native_data_022468b8[];
extern u8 native_data_02246aa8[];


asm u32 native_ov000_02225238 (register u32 a0)
{
    ldr r1, =native_data_022468b8
    ldr r3, =native_data_02246aa8
    ldr r2, [r1, #4]
    mov r0, #1
    cmp r2, #0
    subgt r0, r2, #1
    strgt r0, [r1, #4]
    ldrb r1, [r3, #0x192]
    movgt r0, #0
    cmp r1, #0
    movne r0, #0
    bx lr
}
