/* main row 0x02063ad0: 56 bytes.
 *
 * What it does: calls 2 helpers; 1 load, 0 stores; 1 local pool word (0x021c0c7c); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x021c0c7c (image word 0x021c0c7c)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02063ad0; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);


asm u32 native_main_02063ad0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r2, #0x24
    mul r4, r0, r2
    ldr r5, =0x021c0c7c
    mov r6, r1
    add r0, r5, r4
    mov r1, #0
    bl native_fn_02008d78
    mov r0, r6
    add r1, r5, r4
    mov r2, #0x24
    bl native_fn_02008e0c
    ldmia sp!, {r4, r5, r6, pc}
}
