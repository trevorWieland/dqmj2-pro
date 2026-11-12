/* ov000 row 0x021e2744: 404 bytes.
 *
 * What it does: 99 instructions; 12 call(s) to 0x021e48dc, 0x021e1c4c, 0x021e3140, +9 more; loops (back edge at +0x60); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x18c -> constant 0x022322c4 (image word 0x022322c4)
 *   pool +0x190 -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x20 -> +0xcc
 *   branch +0x40 -> +0xb4
 *   branch +0x9c -> +0xa8
 *   branch +0xb0 -> +0xc4
 *   branch +0xc8 -> +0x174
 *   branch +0xd0 -> +0x174
 *   branch +0xec -> +0x160
 *   branch +0x148 -> +0x154
 *   branch +0x15c -> +0x170
 *   test +0x1c tst r0, #64
 *   test +0x3c cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xcc tst r0, #128
 *   test +0xe8 cmp r0, #0
 *   test +0x144 cmp r0, #0
 *   8 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2744; the literal pool and
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

extern void native_fn_021e48dc(void);
extern void native_fn_021e1c4c(void);
extern void native_fn_021e3140(void);
extern void native_fn_021e489c(void);
extern void native_fn_021d8a08(void);
extern void native_fn_021e0d78(void);


asm u32 native_ov000_021e2744 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #64
    ldr r0, =0x022322c4
    mov r1, #0
    ldr r0, [r0, #0x4]
    ldr r4, =0x022322d4
    ldrh r0, [r0]
    tst r0, #64
    beq ov000_021e2744_Lcc
    mov r3, #5
    add r2, sp, #12
    mov r0, r4
    mov r1, #1
    strb r3, [r4, #0x1e0]
    bl native_fn_021e48dc
    cmp r0, #0
    beq ov000_021e2744_Lb4
    mov r2, #0
    str r2, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    ldrsb r1, [sp, #48]
    ldrb r3, [sp, #0x35]
    mov r0, #2
    bl native_fn_021e1c4c
    add r0, sp, #12
    add r3, r4, #376
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    add r3, r4, #388
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    bl native_fn_021e3140
    mov r1, #0
    ldrsb r0, [sp, #42]
    mov r2, r1
    bl native_fn_021e489c
    cmp r0, #0
    beq ov000_021e2744_La8
    mov r0, #0
    bl native_fn_021d8a08
ov000_021e2744_La8:
    mov r0, #1
    strb r0, [r4, #0x1e3]
    b ov000_021e2744_Lc4
ov000_021e2744_Lb4:
    mov r0, #10
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
ov000_021e2744_Lc4:
    mov r1, #1
    b ov000_021e2744_L174
ov000_021e2744_Lcc:
    tst r0, #128
    beq ov000_021e2744_L174
    mov r3, #6
    add r2, sp, #12
    mov r0, r4
    strb r3, [r4, #0x1e0]
    bl native_fn_021e48dc
    cmp r0, #0
    beq ov000_021e2744_L160
    mov r2, #0
    str r2, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    ldrsb r1, [sp, #48]
    ldrb r3, [sp, #0x35]
    mov r0, #2
    bl native_fn_021e1c4c
    add r0, sp, #12
    add r3, r4, #376
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    add r3, r4, #388
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    bl native_fn_021e3140
    mov r1, #0
    ldrsb r0, [sp, #42]
    mov r2, r1
    bl native_fn_021e489c
    cmp r0, #0
    beq ov000_021e2744_L154
    mov r0, #0
    bl native_fn_021d8a08
ov000_021e2744_L154:
    mov r0, #1
    strb r0, [r4, #0x1e3]
    b ov000_021e2744_L170
ov000_021e2744_L160:
    mov r0, #13
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
ov000_021e2744_L170:
    mov r1, #1
ov000_021e2744_L174:
    ldr r2, =0x022322d4
    mov r0, #0
    str r0, [r2, #0x274]
    strb r1, [r2, #0x27e]
    add sp, sp, #64
    ldmia sp!, {r4, pc}
}
