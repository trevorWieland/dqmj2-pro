/* main row 0x0206df1c: 36 bytes.
 *
 * What it does: calls 2 helpers; 2 loads, 0 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x10 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0206df1c; the literal pool and
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

extern void native_fn_02061dcc(void);
extern void native_fn_02049ffc(void);


asm u32 native_main_0206df1c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #3
    bl native_fn_02061dcc
    ldr r0, [r0]
    cmp r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r0, [r0, #4]
    bl native_fn_02049ffc
    ldmia sp!, {r3, pc}
}
