/* ov000 row 0x0222456c: 80 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x4c -> native_data_0222fdf0 (image word 0x0222fdf0)
 *   back edge +0x1c -> +0x0c
 *   back edge +0x44 -> +0x2c
 *   test +0x14 cmp r3, #6
 *   test +0x38 cmp r3, #3
 *   memory +0x10 strh r2, [ip, #0x18]
 *   memory +0x30 ldrsh r1, [r1, r2]
 *   memory +0x3c strh r1, [r0, #0x18]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: two record-pointer walks allocate one extra register (92 vs 80
 * B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222456c; the literal pool and
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

extern u8 native_data_0222fdf0[];


asm u32 native_ov000_0222456c (register u32 a0)
{
    mov ip, r0
    mov r3, #0
    mvn r2, #0
ov000_0222456c_Lc:
    add r3, r3, #1
    strh r2, [ip, #0x18]
    cmp r3, #6
    add ip, ip, #0x34
    blt ov000_0222456c_Lc
    ldr r2, =native_data_0222fdf0
    mov r3, #0
    add r2, r2, r1, lsl #3
ov000_0222456c_L2c:
    mov r1, r3, lsl #1
    ldrsh r1, [r1, r2]
    add r3, r3, #1
    cmp r3, #3
    strh r1, [r0, #0x18]
    add r0, r0, #0x34
    blt ov000_0222456c_L2c
    bx lr
}
