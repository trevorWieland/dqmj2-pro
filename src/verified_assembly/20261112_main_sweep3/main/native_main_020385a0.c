/* main row 0x020385a0: 40 bytes.
 *
 * What it does: calls 1 helper; 2 loads, 1 store; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x10 cmpne r4, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020385a0; the literal pool and
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

extern void native_fn_02009128(void);


asm u32 native_main_020385a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    movs r5, r0
    ldrneb r0, [r5, #0x2e]
    mov r4, r1
    cmpne r4, r0
    ldmeqia sp!, {r3, r4, r5, pc}
    ldrb r0, [r5, #0x3c]
    bl native_fn_02009128
    strb r4, [r5, #0x2e]
    ldmia sp!, {r3, r4, r5, pc}
}
