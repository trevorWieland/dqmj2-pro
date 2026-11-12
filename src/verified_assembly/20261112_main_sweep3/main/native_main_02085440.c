/* main row 0x02085440: 56 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 0 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x20 tst r1, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02085440; the literal pool and
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

extern void native_fn_0205e7a8(void);


asm u32 native_main_02085440 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r2, r0
    ldr r1, [r2, #0x80]
    mov r0, #0
    mov r1, r1, lsl #0x10
    movs r1, r1, lsr #0x1f
    ldmeqia sp!, {r3, pc}
    ldrh r1, [r2, #0x6e]
    tst r1, #2
    ldmneia sp!, {r3, pc}
    ldrh r1, [r2, #0x88]
    sub r0, r0, #1
    bl native_fn_0205e7a8
    ldmia sp!, {r3, pc}
}
