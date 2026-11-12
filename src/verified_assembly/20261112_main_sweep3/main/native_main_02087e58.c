/* main row 0x02087e58: 44 bytes.
 *
 * What it does: 1 indirect call through a register; 4 loads, 2 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02087e58; the literal pool and
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



asm u32 native_main_02087e58 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldrb lr, [sp, #0x10]
    ldrb r12, [sp, #0x14]
    str lr, [sp]
    str r12, [sp, #4]
    ldr r12, [r0, #0x14]
    ldr r12, [r12, #8]
    blx r12
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
