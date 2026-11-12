/* main row 0x020ba3bc: 36 bytes.
 *
 * What it does: calls 1 helper; 2 loads, 1 store; 2 local pool words (0x020b9d68, 0x020e2c64); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x1c -> native_fn_020b9d68 (image word 0x020b9d68)
 *   pool +0x20 -> native_data_020e2c64 (image word 0x020e2c64)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020ba3bc; the literal pool and
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

extern void native_fn_0209b5f4(void);
extern void native_fn_020b9d68(void);
extern u8 native_data_020e2c64[];


asm u32 native_main_020ba3bc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    blx native_fn_0209b5f4
    ldr r2, =native_fn_020b9d68
    ldr r1, =native_data_020e2c64
    mov r0, #0xd
    str r2, [r1]
    ldmia sp!, {r3, pc}
}
