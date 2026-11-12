/* main row 0x02045738: 56 bytes.
 *
 * What it does: calls 2 helpers; 3 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x14 -> +0x20
 *   branch +0x1c -> +0x24
 *   back edge +0x30 -> +0x0c
 *   test +0x0c cmp r5, #0
 *   test +0x2c cmp r4, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02045738; the literal pool and
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

extern void native_fn_02045654(void);
extern void native_fn_02045680(void);


asm u32 native_main_02045738 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #0
main_02045738_Lc:
    cmp r5, #0
    mov r0, r4
    bne main_02045738_L20
    bl native_fn_02045654
    b main_02045738_L24
main_02045738_L20:
    bl native_fn_02045680
main_02045738_L24:
    add r0, r4, #1
    and r4, r0, #0xff
    cmp r4, #4
    blo main_02045738_Lc
    ldmia sp!, {r3, r4, r5, pc}
}
