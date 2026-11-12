/* main row 0x020baf04: 60 bytes.
 *
 * What it does: calls 3 helpers; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x1c cmp r2, r0
 *   test +0x20 cmpeq r3, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020baf04; the literal pool and
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

extern void native_fn_020685b0(void);
extern void native_fn_02097330(void);
extern void native_fn_02096f3c(void);


asm u32 native_main_020baf04 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_020685b0
    blx native_fn_02097330
    mov r3, r0
    mov r2, r1
    mov r0, #0
    cmp r2, r0
    cmpeq r3, r0
    ldmeqia sp!, {r4, pc}
    mov r0, r4
    mov r1, r3
    blx native_fn_02096f3c
    mov r0, r4
    ldmia sp!, {r4, pc}
}
