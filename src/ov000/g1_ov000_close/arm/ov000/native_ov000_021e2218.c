/* ov000 row 0x021e2218: 696 bytes.
 *
 * What it does: 169 instructions; 27 call(s) to 0x021e4388, 0x021e1c4c, 0x020404f0, +24 more; loops (back edge at +0x5c); returns through pop {r3, r4, r5, r6, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x2a4 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0x2a8 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x2ac -> constant 0x0223244c (image word 0x0223244c)
 *   pool +0x2b0 -> constant 0x02232458 (image word 0x02232458)
 *   pool +0x2b4 -> native_data_0222ebec (image word 0x0222ebec)
 *   branch +0x30 -> +0xa0
 *   branch +0x9c -> +0x28c
 *   branch +0xb4 -> +0x18c
 *   branch +0x130 -> +0x178
 *   branch +0x148 -> +0x164
 *   branch +0x160 -> +0x178
 *   branch +0x188 -> +0x28c
 *   branch +0x1a4 -> +0x1e0
 *   branch +0x1dc -> +0x28c
 *   branch +0x1f4 -> +0x210
 *   branch +0x20c -> +0x28c
 *   branch +0x224 -> +0x260
 *   branch +0x25c -> +0x28c
 *   branch +0x274 -> +0x28c
 *   branch +0x290 -> +0x298
 *   test +0x2c cmp r0, #0
 *   test +0xb0 cmp r0, #0
 *   test +0x12c cmp r0, #0
 *   test +0x144 cmp r0, #0
 *   test +0x1a0 cmp r0, #0
 *   test +0x1f0 cmp r0, #0
 *   test +0x220 cmp r0, #0
 *   test +0x270 tst r0, #7
 *   test +0x28c cmp r6, #0
 *   16 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2218; the literal pool and
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

extern void native_fn_021e4388(void);
extern void native_fn_021e1c4c(void);
extern void native_fn_020404f0(void);
extern void native_fn_021e74e8(void);
extern void native_fn_021e7510(void);
extern void native_fn_021e48dc(void);
extern void native_fn_021e339c(void);
extern u8 native_data_0222ebec[];
extern void native_fn_021d8c80(void);
extern void native_fn_021e489c(void);
extern void native_fn_021e48bc(void);
extern void native_fn_021d8eb4(void);
extern void native_fn_021d8b24(void);
extern void native_fn_021d8a08(void);
extern void native_fn_02213b68(void);
extern void native_fn_021e07f0(void);
extern void native_fn_021e8a14(void);
extern void native_fn_021e45b8(void);
extern void native_fn_021e55d8(void);


asm u32 native_ov000_021e2218 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #140
    ldr r5, =0x02232344
    ldr r3, =0x022322d4
    add r2, sp, #88
    mov r0, r5
    mov r1, #1
    str r3, [sp, #0xc]
    ldr r4, [r3, #0x8c]
    mov r6, #0
    bl native_fn_021e4388
    cmp r0, #0
    beq ov000_021e2218_La0
    mov r0, r6
    str r0, [sp]
    ldrsh r1, [sp, #134]
    mov r0, #2
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #136]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #123]
    ldrsb r2, [sp, #127]
    ldrb r3, [sp, #0x81]
    bl native_fn_021e1c4c
    add r0, sp, #88
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #100
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #11
    bl native_fn_020404f0
    ldrb r0, [sp, #0x83]
    bl native_fn_021e74e8
    add r0, sp, #88
    bl native_fn_021e7510
    mov r6, #1
    b ov000_021e2218_L28c
ov000_021e2218_La0:
    ldr r0, [sp, #0xc]
    add r2, sp, #88
    mov r1, #2
    bl native_fn_021e48dc
    cmp r0, #0
    beq ov000_021e2218_L18c
    mov r0, r6
    str r0, [sp]
    ldrsh r1, [sp, #134]
    mov r0, #5
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #136]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #123]
    ldrsb r2, [sp, #127]
    ldrb r3, [sp, #0x81]
    bl native_fn_021e1c4c
    ldr r12, [sp, #0xc]
    add r0, sp, #88
    add r3, r12, #376
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #100
    add r3, r12, #388
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    bl native_fn_021e339c
    ldr r1, =native_data_0222ebec
    mov r0, #1
    strb r0, [r1]
    bl native_fn_021d8c80
    ldrsb r0, [sp, #118]
    add r1, sp, #76
    add r2, sp, #64
    bl native_fn_021e489c
    cmp r0, #0
    beq ov000_021e2218_L178
    ldrsb r0, [sp, #118]
    add r1, sp, #52
    add r2, sp, #40
    bl native_fn_021e48bc
    cmp r0, #0
    beq ov000_021e2218_L164
    add r0, sp, #52
    add r1, sp, #76
    mov r2, r6
    mov r3, #1
    bl native_fn_021d8eb4
    b ov000_021e2218_L178
ov000_021e2218_L164:
    add r0, sp, #76
    add r1, sp, #64
    bl native_fn_021d8b24
    mov r0, #1
    bl native_fn_021d8a08
ov000_021e2218_L178:
    ldr r0, [sp, #0xc]
    mov r1, #0
    strb r1, [r0, #0x1e3]
    mov r6, #1
    b ov000_021e2218_L28c
ov000_021e2218_L18c:
    add r2, sp, #28
    add r3, sp, #16
    mov r0, r5
    mov r1, r4
    bl native_fn_02213b68
    cmp r0, #0
    beq ov000_021e2218_L1e0
    mov r0, #2
    bl native_fn_021e07f0
    add r0, sp, #28
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #16
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #10
    bl native_fn_020404f0
    mov r6, #1
    b ov000_021e2218_L28c
ov000_021e2218_L1e0:
    add r2, sp, #12
    mov r0, r5
    mov r1, r4
    bl native_fn_021e8a14
    cmp r0, #0
    beq ov000_021e2218_L210
    mov r0, #2
    bl native_fn_021e07f0
    mov r0, #12
    bl native_fn_020404f0
    mov r6, #1
    b ov000_021e2218_L28c
ov000_021e2218_L210:
    add r2, sp, #88
    mov r0, r5
    mov r1, r4
    bl native_fn_021e45b8
    cmp r0, #0
    beq ov000_021e2218_L260
    mov r0, #2
    bl native_fn_021e07f0
    add r0, sp, #88
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #100
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #20
    bl native_fn_020404f0
    mov r6, #1
    b ov000_021e2218_L28c
ov000_021e2218_L260:
    mov r1, #1
    ldr r0, =0x022322d4
    mov r2, r1
    bl native_fn_021e55d8
    tst r0, #7
    beq ov000_021e2218_L28c
    mov r0, #2
    bl native_fn_021e07f0
    mov r0, #32
    bl native_fn_020404f0
    mov r6, #1
ov000_021e2218_L28c:
    cmp r6, #0
    beq ov000_021e2218_L298
    bl native_fn_021e339c
ov000_021e2218_L298:
    mov r0, r6
    add sp, sp, #140
    ldmia sp!, {r3, r4, r5, r6, pc}
}
