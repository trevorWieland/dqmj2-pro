/* main row 0x020cde3c: 60 bytes.
 *
 * What it does: calls 1 helper; 2 loads, 1 store; 1 local pool word (0x021d697c); 1 branch, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x38 -> constant 0x021d697c (image word 0x021d697c)
 *   back edge +0x30 -> +0x10
 *   test +0x2c cmp lr, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020cde3c; the literal pool and
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

extern void native_fn_020cf27c(void);


asm u32 native_main_020cde3c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_020cf27c
    ldr r12, =0x021d697c
    mov lr, #0
main_020cde3c_L10:
    add r3, r12, lr, lsl #2
    add r1, lr, #1
    mov r1, r1, lsl #0x18
    add r2, r0, lr, lsl #2
    ldr r3, [r3, #0x18]
    mov lr, r1, asr #0x18
    str r3, [r2, #0x18]
    cmp lr, #3
    blt main_020cde3c_L10
    ldmia sp!, {r3, pc}
}
