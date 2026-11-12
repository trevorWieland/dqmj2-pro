/* ov000 row 0x021e0e2c: 300 bytes.
 *
 * What it does: 71 instructions; 9 call(s) to 0x021e4bcc, 0x021e1c4c, 0x021e55d8, +6 more; loops (back edge at +0x98); returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x11c -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x120 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0x124 -> constant 0x0223244c (image word 0x0223244c)
 *   pool +0x128 -> constant 0x02232458 (image word 0x02232458)
 *   branch +0x20 -> +0x7c
 *   branch +0x90 -> +0xa8
 *   branch +0xc0 -> +0x110
 *   branch +0xd0 -> +0x110
 *   test +0x1c cmp r0, #0
 *   test +0x8c tst r0, #3
 *   test +0xbc cmp r0, #0
 *   test +0xcc cmp r0, #5
 *   8 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0e2c; the literal pool and
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

extern void native_fn_021e4bcc(void);
extern void native_fn_021e1c4c(void);
extern void native_fn_021e55d8(void);
extern void native_fn_020404f0(void);
extern void native_fn_02213b68(void);
extern void native_fn_02213f4c(void);
extern void native_fn_02213f8c(void);
extern void native_fn_021e07f0(void);


asm u32 native_ov000_021e0e2c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #88
    ldr r0, =0x022322d4
    add r1, sp, #36
    ldr r4, [r0, #0x8c]
    ldr r5, =0x02232344
    bl native_fn_021e4bcc
    cmp r0, #0
    beq ov000_021e0e2c_L7c
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #82]
    mov r0, #7
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #84]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #71]
    ldrsb r2, [sp, #75]
    ldrb r3, [sp, #0x4d]
    bl native_fn_021e1c4c
    add r0, sp, #36
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #48
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add sp, sp, #88
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov000_021e0e2c_L7c:
    ldr r0, =0x022322d4
    mov r1, #0
    mov r2, #1
    bl native_fn_021e55d8
    tst r0, #3
    beq ov000_021e0e2c_La8
    mov r0, #32
    bl native_fn_020404f0
    add sp, sp, #88
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov000_021e0e2c_La8:
    add r2, sp, #24
    add r3, sp, #12
    mov r0, r5
    mov r1, r4
    bl native_fn_02213b68
    cmp r0, #0
    beq ov000_021e0e2c_L110
    bl native_fn_02213f4c
    bl native_fn_02213f8c
    cmp r0, #5
    bne ov000_021e0e2c_L110
    mov r0, #2
    bl native_fn_021e07f0
    add r0, sp, #24
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #12
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #10
    bl native_fn_020404f0
    add sp, sp, #88
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov000_021e0e2c_L110:
    mov r0, #0
    add sp, sp, #88
    ldmia sp!, {r3, r4, r5, pc}
}
