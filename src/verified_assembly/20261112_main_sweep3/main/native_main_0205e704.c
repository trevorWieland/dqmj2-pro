/* main row 0x0205e704: 56 bytes.
 *
 * What it does: calls 1 helper; 1 branch, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x2c -> +0x10
 *   test +0x1c cmp r0, #0
 *   test +0x28 cmp r4, #0x10
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205e704; the literal pool and
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

extern void native_fn_0205f210(void);


asm u32 native_main_0205e704 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, #0
    mov r6, r0
    mov r4, r5
main_0205e704_L10:
    mov r0, r4
    mov r1, r6
    bl native_fn_0205f210
    cmp r0, #0
    add r4, r4, #1
    addne r5, r5, #1
    cmp r4, #0x10
    blt main_0205e704_L10
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
