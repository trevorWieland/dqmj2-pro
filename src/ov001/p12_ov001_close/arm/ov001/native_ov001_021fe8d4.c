/* ov001 row 0x021fe8d4: 96 bytes.
 *
 * What it does: 23 instructions; 2 call(s) to 0x02202320, 0x02045dc4; loops (back edge at +0x50); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (23 instructions, 2 calls, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x5c -> constant 0x02239dea (image word 0x02239dea)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe8d4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02202320(void);
extern void native_fn_02045dc4(void);


asm u32 native_ov001_021fe8d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    mov r5, r0
    ldr r1, [r5]
    ldrsb r0, [r5, #5]
    ldr r4, [r1, #0x4]
    bl native_fn_02202320
    ldrb r3, [r4, #0x5e]
    mov r1, #12
    mul r2, r0, r1
    str r3, [sp]
    ldrb r1, [r4, #0x5f]
    ldr r0, =0x02239dea
    str r1, [sp, #0x4]
    ldr r1, [r5]
    ldrb r0, [r0, r2]
    ldr r1, [r1, #0x4]
    ldrb r2, [r4, #0x5c]
    ldrb r1, [r1, #0x30]
    ldrb r3, [r4, #0x5d]
    bl native_fn_02045dc4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
