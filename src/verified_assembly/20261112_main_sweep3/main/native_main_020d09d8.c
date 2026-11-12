/* main row 0x020d09d8: 60 bytes.
 *
 * What it does: calls 2 helpers; 3 loads, 1 store; 1 local pool word (0x021d6b5c); 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x38 -> constant 0x021d6b5c (image word 0x021d6b5c)
 *   branch +0x14 -> +0x2c
 *   test +0x10 cmp r1, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d09d8; the literal pool and
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

extern void native_fn_0202a498(void);
extern void native_fn_020d0bfc(void);


asm u32 native_main_020d09d8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x021d6b5c
    mov r4, r0
    ldr r1, [r1, #4]
    cmp r1, #0
    beq main_020d09d8_L2c
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x021d6b5c
    mov r1, #0
    str r1, [r0, #4]
main_020d09d8_L2c:
    mov r0, r4
    bl native_fn_020d0bfc
    ldmia sp!, {r4, pc}
}
