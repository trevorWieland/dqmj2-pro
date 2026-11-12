/* main row 0x02081cac: 48 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 1 store; 2 local pool words (0x020de5a4, 0x04000050); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x28 -> native_data_020de5a4 (image word 0x020de5a4)
 *   pool +0x2c -> constant 0x04000050 (image word 0x04000050)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02081cac; the literal pool and
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

extern u8 native_data_020de5a4[];
extern void native_fn_020042c4(void);


asm u32 native_main_02081cac (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =native_data_020de5a4
    ldr r0, =0x04000050
    ldrsb r3, [r1]
    mov r1, #8
    mov r2, #1
    rsb r12, r3, #0x10
    str r12, [sp]
    bl native_fn_020042c4
    ldmia sp!, {r3, pc}
}
