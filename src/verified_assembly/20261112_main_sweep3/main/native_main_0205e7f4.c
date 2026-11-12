/* main row 0x0205e7f4: 32 bytes.
 *
 * What it does: calls 2 helpers; 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x10 -> +0x18
 *   test +0x08 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205e7f4; the literal pool and
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

extern void native_fn_0205f27c(void);
extern void native_fn_0205f838(void);


asm u32 native_main_0205e7f4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_0205f27c
    cmp r0, #0
    movne r4, #1
    bne main_0205e7f4_L18
    bl native_fn_0205f838
main_0205e7f4_L18:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
