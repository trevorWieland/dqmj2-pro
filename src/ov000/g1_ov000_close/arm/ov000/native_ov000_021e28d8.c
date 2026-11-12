/* ov000 row 0x021e28d8: 720 bytes.
 *
 * What it does: 178 instructions; 20 call(s) to 0x021e4a48, 0x021e1c4c, 0x021e3140, +17 more; loops (back edge at +0x70); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x2c8 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x2cc -> constant 0x022322c4 (image word 0x022322c4)
 *   branch +0x18 -> +0x164
 *   branch +0x2c -> +0x38
 *   branch +0x34 -> +0xc4
 *   branch +0x50 -> +0x9c
 *   branch +0x98 -> +0xbc
 *   branch +0xc0 -> +0x2b0
 *   branch +0xd0 -> +0x2b0
 *   branch +0xd8 -> +0x2b0
 *   branch +0xf0 -> +0x13c
 *   branch +0x138 -> +0x15c
 *   branch +0x160 -> +0x2b0
 *   branch +0x168 -> +0x2b0
 *   branch +0x184 -> +0x2b0
 *   branch +0x18c -> +0x198
 *   branch +0x194 -> +0x224
 *   branch +0x1b0 -> +0x1fc
 *   branch +0x1f8 -> +0x21c
 *   branch +0x220 -> +0x2b0
 *   branch +0x228 -> +0x2b0
 *   branch +0x240 -> +0x28c
 *   branch +0x288 -> +0x2ac
 *   test +0x14 cmp r0, #7
 *   test +0x28 tst r0, #16
 *   test +0x30 tst r0, #64
 *   test +0x4c cmp r0, #0
 *   test +0xc4 tst r0, #32
 *   test +0xd4 tst r0, #128
 *   test +0xec cmp r0, #0
 *   test +0x164 cmp r0, #8
 *   test +0x178 tst r0, #16
 *   test +0x188 tst r0, #64
 *   test +0x190 tst r0, #32
 *   test +0x1ac cmp r0, #0
 *   test +0x224 tst r0, #128
 *   test +0x23c cmp r0, #0
 *   16 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e28d8; the literal pool and
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

extern void native_fn_021e4a48(void);
extern void native_fn_021e1c4c(void);
extern void native_fn_021e3140(void);
extern void native_fn_021e0d78(void);
extern void native_fn_021d84e8(void);


asm u32 native_ov000_021e28d8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #64
    ldr r4, =0x022322d4
    mov r3, #0
    ldrb r0, [r4, #0x1e0]
    cmp r0, #7
    bne ov000_021e28d8_L164
    ldr r0, =0x022322c4
    ldr r0, [r0, #0x4]
    ldrh r0, [r0]
    tst r0, #16
    bne ov000_021e28d8_L38
    tst r0, #64
    beq ov000_021e28d8_Lc4
ov000_021e28d8_L38:
    mov r1, #0
    add r2, sp, #12
    mov r0, r4
    mov r3, r1
    bl native_fn_021e4a48
    cmp r0, #0
    beq ov000_021e28d8_L9c
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
    b ov000_021e28d8_Lbc
ov000_021e28d8_L9c:
    mov r0, #31
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
    ldr r0, [r4, #0x8c]
    mov r1, #0
    sub r0, r0, #245760
    bl native_fn_021d84e8
ov000_021e28d8_Lbc:
    mov r3, #1
    b ov000_021e28d8_L2b0
ov000_021e28d8_Lc4:
    tst r0, #32
    movne r0, #8
    strneb r0, [r4, #0x1e0]
    bne ov000_021e28d8_L2b0
    tst r0, #128
    beq ov000_021e28d8_L2b0
    add r2, sp, #12
    mov r0, r4
    mov r1, #1
    bl native_fn_021e4a48
    cmp r0, #0
    beq ov000_021e28d8_L13c
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
    b ov000_021e28d8_L15c
ov000_021e28d8_L13c:
    mov r0, #34
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
    ldr r0, [r4, #0x8c]
    mov r1, #0
    sub r0, r0, #245760
    bl native_fn_021d84e8
ov000_021e28d8_L15c:
    mov r3, #1
    b ov000_021e28d8_L2b0
ov000_021e28d8_L164:
    cmp r0, #8
    bne ov000_021e28d8_L2b0
    ldr r0, =0x022322c4
    ldr r0, [r0, #0x4]
    ldrh r0, [r0]
    tst r0, #16
    movne r0, #7
    strneb r0, [r4, #0x1e0]
    bne ov000_021e28d8_L2b0
    tst r0, #64
    bne ov000_021e28d8_L198
    tst r0, #32
    beq ov000_021e28d8_L224
ov000_021e28d8_L198:
    add r2, sp, #12
    mov r0, r4
    mov r1, #1
    mov r3, #0
    bl native_fn_021e4a48
    cmp r0, #0
    beq ov000_021e28d8_L1fc
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
    b ov000_021e28d8_L21c
ov000_021e28d8_L1fc:
    mov r0, #34
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
    ldr r0, [r4, #0x8c]
    mov r1, #0
    add r0, r0, #245760
    bl native_fn_021d84e8
ov000_021e28d8_L21c:
    mov r3, #1
    b ov000_021e28d8_L2b0
ov000_021e28d8_L224:
    tst r0, #128
    beq ov000_021e28d8_L2b0
    add r2, sp, #12
    mov r0, r4
    mov r1, r3
    bl native_fn_021e4a48
    cmp r0, #0
    beq ov000_021e28d8_L28c
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
    b ov000_021e28d8_L2ac
ov000_021e28d8_L28c:
    mov r0, #31
    mov r1, #0
    mov r2, #1
    bl native_fn_021e0d78
    ldr r0, [r4, #0x8c]
    mov r1, #0
    add r0, r0, #245760
    bl native_fn_021d84e8
ov000_021e28d8_L2ac:
    mov r3, #1
ov000_021e28d8_L2b0:
    ldr r1, =0x022322d4
    mov r0, #0
    str r0, [r1, #0x274]
    strb r3, [r1, #0x27e]
    add sp, sp, #64
    ldmia sp!, {r4, pc}
}
