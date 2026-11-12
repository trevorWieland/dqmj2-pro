/* main row 0x02038224: 36 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 0 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x08 cmp r2, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02038224; the literal pool and
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

extern void native_fn_02037f60(void);


asm u32 native_main_02038224 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, [r0]
    cmp r2, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r0, [r0]
    ldrb r0, [r0, #0x3c]
    bl native_fn_02037f60
    ldmia sp!, {r3, pc}
}
