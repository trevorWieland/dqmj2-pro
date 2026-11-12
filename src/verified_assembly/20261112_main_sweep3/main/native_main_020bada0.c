/* main row 0x020bada0: 44 bytes.
 *
 * What it does: calls 1 helper; 1 indirect call through a register; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r5, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bada0; the literal pool and
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

extern void native_fn_020bac94(void);


asm u32 native_main_020bada0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r2
    bl native_fn_020bac94
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    cmp r5, #0
    movne r0, #1
    moveq r0, #0
    blx r4
    ldmia sp!, {r3, r4, r5, pc}
}
