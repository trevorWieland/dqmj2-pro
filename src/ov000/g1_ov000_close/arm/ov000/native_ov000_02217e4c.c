/* ov000 row 0x02217e4c: 200 bytes.
 *
 * What it does: 50 instructions; 8 call(s) to 0x02049ad0, 0x022174a8, 0x02217418, +5 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x20 cmp r4, r7
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217e4c; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_022174a8(void);
extern void native_fn_02217418(void);
extern void native_fn_0206006c(void);


asm u32 native_ov000_02217e4c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r5, [r0]
    ldr r4, [r0, #0x4]
    mov r7, r1
    mov r0, r2
    sub r4, r5, r4
    mov r6, r3
    bl native_fn_02049ad0
    cmp r4, r7
    movne r2, #1
    ldr r1, [sp, #0x18]
    moveq r2, #0
    strb r2, [r0, #0x5]
    ldr r2, [r0]
    add r1, r1, #7
    mov r1, r1, asr #3
    add r1, r1, #4
    mov r7, r1, lsl #24
    ldrsb r0, [r0, #5]
    ldr r4, [r2, #0x4]
    mov r5, r7, asr #24
    bl native_fn_022174a8
    bl native_fn_02217418
    ldrsb r1, [r4, #31]
    mov r3, r5
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    bl native_fn_0206006c
    mov r0, r6
    bl native_fn_02049ad0
    mov r1, #14
    strb r1, [r0, #0x5]
    mov r0, r1
    bl native_fn_022174a8
    bl native_fn_02217418
    ldrsb r1, [sp, #28]
    ldrsb r2, [r4, #31]
    sub r1, r1, r7, asr #24
    str r2, [sp]
    mov r1, r1, lsl #24
    mov r3, r1, asr #24
    ldrb r1, [r4, #0x1c]
    ldrsb r2, [r4, #29]
    add r1, r1, r7, asr #24
    mov r1, r1, lsl #24
    mov r1, r1, asr #24
    bl native_fn_0206006c
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
