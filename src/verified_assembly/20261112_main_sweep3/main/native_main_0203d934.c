/* main row 0x0203d934: 56 bytes.
 *
 * What it does: calls 4 helpers; 2 loads, 1 store; 1 local pool word (0x020f6054); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x020f6054 (image word 0x020f6054)
 *   test +0x14 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203d934; the literal pool and
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

extern void native_fn_02040808(void);
extern void native_fn_021dff98(void);
extern void native_fn_0203d784(void);
extern void native_fn_02040468(void);


asm u32 native_main_0203d934 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02040808
    bl native_fn_021dff98
    bl native_fn_0203d784
    bl native_fn_02040468
    cmp r0, #0
    ldrne r0, =0x020f6054
    movne r1, #0x26
    ldreq r0, =0x020f6054
    moveq r1, #1
    strb r1, [r0, #0xa]
    mov r0, #0
    ldmia sp!, {r3, pc}
}
