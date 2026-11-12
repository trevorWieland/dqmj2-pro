/* main row 0x020861a0: 48 bytes.
 *
 * What it does: calls 2 helpers; 1 load, 0 stores; 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x10 -> +0x28
 *   test +0x0c cmp r1, #0xc
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020861a0; the literal pool and
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

extern void native_fn_02086b50(void);
extern void native_fn_02086b14(void);


asm u32 native_main_020861a0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldr r1, [r4, #0x14]
    cmp r1, #0xc
    bne main_020861a0_L28
    bl native_fn_02086b50
    mov r1, r0
    mov r0, r4
    and r1, r1, #0xff
    bl native_fn_02086b14
main_020861a0_L28:
    mov r0, #1
    ldmia sp!, {r4, pc}
}
