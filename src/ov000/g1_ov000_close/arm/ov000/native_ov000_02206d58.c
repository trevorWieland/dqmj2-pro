/* ov000 row 0x02206d58: 96 bytes.
 *
 * What it does: 22 instructions; 2 call(s) to 0x02049af0, 0x02049ae4; loops (back edge at +0x24); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x58 -> native_data_0222f60c (image word 0x0222f60c)
 *   pool +0x5c -> constant 0x02238248 (image word 0x02238248)
 *   test +0x38 cmp r2, #0
 *   1 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206d58; the literal pool and
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

extern u8 native_data_0222f60c[];
extern void native_fn_02049af0(void);
extern void native_fn_02049ae4(void);


asm u32 native_ov000_02206d58 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    ldr r12, =native_data_0222f60c
    ldr lr, [sp, #0x1c]
    ldr r4, [r12]
    mov r12, #1
    str r3, [sp]
    mov r3, r4, asr #5
    stmib sp, {r12, lr}
    bl native_fn_02049af0
    ldr r2, [sp, #0x18]
    ldr r1, =native_data_0222f60c
    mov r0, r0, lsl #5
    str r0, [r1]
    cmp r2, #0
    ldrne r0, =0x02238248
    movne r1, #5
    strne r1, [r0, #0x1c]
    bl native_fn_02049ae4
    ldr r0, [r0, #0x4]
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
