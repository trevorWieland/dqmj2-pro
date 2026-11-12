/* main row 0x020c1fdc: 52 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x30 -> native_data_020e2cf4 (image word 0x020e2cf4)
 *   memory +0x04 ldrb r3, [r1]
 *   memory +0x0c ldrb r2, [r1, #1]
 *   memory +0x14 strb r3, [lr, r0, lsl #2]
 *   memory +0x18 strb r2, [ip, #1]
 *   memory +0x1c ldrb r2, [r1, #2]
 *   memory +0x20 ldrb r0, [r1, #3]
 *   memory +0x24 strb r2, [ip, #2]
 *   memory +0x28 strb r0, [ip, #3]
 *   4 store instruction(s)
 *
 * Why transcribed rather than written as C: four-byte stride copy: four bytes long
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020c1fdc; the literal pool and
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

extern u8 native_data_020e2cf4[];


asm u32 native_main_020c1fdc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldrb r3, [r1]
    ldr lr, =native_data_020e2cf4
    ldrb r2, [r1, #1]
    add ip, lr, r0, lsl #2
    strb r3, [lr, r0, lsl #2]
    strb r2, [ip, #1]
    ldrb r2, [r1, #2]
    ldrb r0, [r1, #3]
    strb r2, [ip, #2]
    strb r0, [ip, #3]
    ldmia sp!, {r3, pc}
}
