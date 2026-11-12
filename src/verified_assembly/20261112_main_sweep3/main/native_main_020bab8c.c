/* main row 0x020bab8c: 32 bytes.
 *
 * What it does: 1 indirect call through a register; 2 loads, 0 stores; 1 local pool word (0x021d3044); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x1c -> constant 0x021d3044 (image word 0x021d3044)
 *   test +0x0c cmp r3, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bab8c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_020bab8c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r3, =0x021d3044
    ldr r3, [r3, #0x20]
    cmp r3, #0
    ldmeqia sp!, {r3, pc}
    blx r3
    ldmia sp!, {r3, pc}
}
