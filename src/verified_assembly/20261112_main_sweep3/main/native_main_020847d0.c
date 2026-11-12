/* main row 0x020847d0: 56 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 2 stores; 1 local pool word (0x021c968c); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x021c968c (image word 0x021c968c)
 *   test +0x0c cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020847d0; the literal pool and
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


asm u32 native_main_020847d0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =0x021c968c
    ldr r1, [r1]
    cmp r1, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_0202a498
    ldr r0, =0x021c968c
    mov r1, #0
    str r1, [r0]
    str r1, [r0, #4]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
