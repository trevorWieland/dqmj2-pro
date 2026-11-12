/* main row 0x0203c438: 36 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x18 -> native_data_020f5bdc (image word 0x020f5bdc)
 *   pool +0x1c -> native_fn_0203c388 (image word 0x0203c388)
 *   pool +0x20 -> native_data_020f5bdc (image word 0x020f5bdc)
 *   memory +0x08 str r0, [r2]
 *   memory +0x10 str r1, [r2, #4]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: tail call through a literal function pointer: four bytes long
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203c438; the literal pool and
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

extern u8 native_data2_020f5bdc[];
extern u8 native_data_020f5bdc[];
extern void native_fn_0203c388(void);


asm u32 native_main_0203c438 (register u32 a0)
{
    ldr r2, =native_data_020f5bdc
    ldr ip, =native_fn_0203c388
    str r0, [r2]
    ldr r0, =native_data2_020f5bdc
    str r1, [r2, #4]
    bx ip
}
