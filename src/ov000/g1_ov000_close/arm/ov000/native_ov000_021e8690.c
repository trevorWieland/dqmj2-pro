/* ov000 row 0x021e8690: 324 bytes.
 *
 * What it does: 81 instructions; 10 call(s) to 0x02042b3c, 0x021e0e04, 0x02042cb8, +7 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x28
 *   branch +0x2c -> +0xd8
 *   branch +0x40 -> +0xd8
 *   branch +0xb4 -> +0xc8
 *   branch +0xcc -> +0xd8
 *   branch +0xdc -> +0xfc
 *   branch +0x108 -> +0x138
 *   branch +0x128 -> +0x138
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r4, #0
 *   test +0x3c cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xc8 cmp r4, #0
 *   test +0xd8 cmp r4, #0
 *   test +0x104 cmp r1, #0
 *   test +0x124 cmp r2, r0
 *   4 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8690; the literal pool and
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

extern void native_fn_02042b3c(void);
extern void native_fn_021e0e04(void);
extern void native_fn_02042cb8(void);
extern void native_fn_021e07b8(void);
extern void native_fn_021dc374(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021e85f8(void);
extern void native_fn_021e7d18(void);


asm u32 native_ov000_021e8690 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #24
    add r1, sp, #12
    mov r5, r0
    bl native_fn_02042b3c
    movs r4, r0
    beq ov000_021e8690_L28
    bl native_fn_021e0e04
    cmp r0, #0
    moveq r4, #0
ov000_021e8690_L28:
    cmp r4, #0
    beq ov000_021e8690_Ld8
    ldr r0, [r5, #0x164]
    bl native_fn_02042cb8
    ldrb r0, [r5, #0x277]
    cmp r0, #0
    bne ov000_021e8690_Ld8
    mov r0, #0
    bl native_fn_021e07b8
    ldr r3, [r0, #0x4]
    ldr r1, [sp, #0x10]
    ldr lr, [sp, #0xc]
    sub r6, r3, r1
    smull r1, r3, r6, r6
    ldr r6, [r0]
    ldr r12, [r0, #0x8]
    sub r6, r6, lr
    ldr r0, [sp, #0x14]
    smlal r1, r3, r6, r6
    sub r0, r12, r0
    smlal r1, r3, r0, r0
    mov r0, r1, lsr #12
    ldr r2, [r5, #0x29c]
    orr r0, r0, r3, lsl #20
    mov r1, r2, asr #31
    subs r0, r0, r2
    rscs r0, r1, r3, asr #12
    movlt r4, #0
    add r0, sp, #12
    add r2, sp, #0
    add r1, r5, #528
    mov r3, #2
    bl native_fn_021dc374
    cmp r0, #0
    moveq r4, #0
    beq ov000_021e8690_Lc8
    add r0, sp, #0
    add r1, sp, #12
    mov r2, #12
    bl native_fn_02008e0c
ov000_021e8690_Lc8:
    cmp r4, #0
    bne ov000_021e8690_Ld8
    mov r0, r5
    bl native_fn_021e85f8
ov000_021e8690_Ld8:
    cmp r4, #0
    beq ov000_021e8690_Lfc
    add r12, sp, #12
    add r3, r5, #112
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r5, #272
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021e8690_Lfc:
    add r0, r5, #512
    ldrsb r1, [r0, #117]
    cmp r1, #0
    blt ov000_021e8690_L138
    ldr r2, [r5, #0x60]
    ldr r0, [r2, #0x8]
    ldr r2, [r2]
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #12
    sub r0, r0, #1
    cmp r2, r0
    blt ov000_021e8690_L138
    mov r0, r5
    mov r2, #0
    bl native_fn_021e7d18
ov000_021e8690_L138:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, pc}
}
