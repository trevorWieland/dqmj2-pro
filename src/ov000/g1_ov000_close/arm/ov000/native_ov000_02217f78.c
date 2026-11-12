/* ov000 row 0x02217f78: 140 bytes.
 *
 * What it does: 34 instructions; 3 call(s) to 0x02217e4c, 0x0204b5b0, 0x0205fb3c; loops (back edge at +0x3c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x022459c4 (image word 0x022459c4)
 *   test +0x44 cmp r1, r6
 *   test +0x64 cmp r0, r6
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217f78; the literal pool and
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

extern void native_fn_02217e4c(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_0205fb3c(void);


asm u32 native_ov000_02217f78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r6, r0
    add r12, r6, #5
    mov r5, r1
    str r2, [sp]
    mov r4, r3
    add r0, r6, #12
    mov r3, r0, lsl #24
    mov r2, r12, lsl #24
    mov r0, r5
    mov r1, r6
    str r4, [sp, #0x4]
    mov r2, r2, asr #24
    mov r3, r3, asr #24
    bl native_fn_02217e4c
    ldr r1, [r5]
    cmp r1, r6
    movne r0, r4, lsl #3
    moveq r0, r0, lsl #3
    and r4, r0, #255
    ldr r0, =0x022459c4
    mov r1, r4
    bl native_fn_0204b5b0
    ldr r0, [r5]
    cmp r0, r6
    movne r1, #3
    moveq r1, #2
    ldr r0, =0x022459c4
    and r1, r1, #255
    bl native_fn_0205fb3c
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
