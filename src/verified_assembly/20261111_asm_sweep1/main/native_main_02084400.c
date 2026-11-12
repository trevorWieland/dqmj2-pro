/* main row 0x02084400: 52 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x2c -> native_data_021c9600 (image word 0x021c9600)
 *   pool +0x30 -> native_data_021c961c (image word 0x021c961c)
 *   memory +0x0c ldr lr, [r2, #0x2c]
 *   memory +0x10 ldr ip, [r2, #0x30]
 *   memory +0x14 str lr, [r2, #0x1c]
 *   memory +0x18 str ip, [r2, #0x20]
 *   memory +0x1c str r0, [r2, #0x2c]
 *   memory +0x24 str r1, [r2, #0x30]
 *   4 store instruction(s)
 *
 * Why transcribed rather than written as C: pair rotation: eight bytes long
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02084400; the literal pool and
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

extern u8 native_data_021c9600[];
extern u8 native_data_021c961c[];


asm u32 native_main_02084400 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, =native_data_021c9600
    ldr r3, =native_data_021c961c
    ldr lr, [r2, #0x2c]
    ldr ip, [r2, #0x30]
    str lr, [r2, #0x1c]
    str ip, [r2, #0x20]
    str r0, [r2, #0x2c]
    mov r0, r3
    str r1, [r2, #0x30]
    ldmia sp!, {r3, pc}
}
