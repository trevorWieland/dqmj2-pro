/* main row 0x02038174: 32 bytes.
 *
 * What it does: Guarded field call: returns when [r0] is null, otherwise reloads [r0] and calls 0x02009160 with the byte at +0x3c of the object.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x08 cmp r2, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02038174; the literal pool and
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

extern void native_fn_02009160(void);


asm u32 native_main_02038174 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, [r0]
    cmp r2, #0
    ldmeqia sp!, {r3, pc}
    ldr r0, [r0]
    ldrb r0, [r0, #0x3c]
    bl native_fn_02009160
    ldmia sp!, {r3, pc}
}
