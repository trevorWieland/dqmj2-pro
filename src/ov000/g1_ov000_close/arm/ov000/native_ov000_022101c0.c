/* ov000 row 0x022101c0: 388 bytes.
 *
 * What it does: 97 instructions; 13 call(s) to 0x02042b3c, 0x021e0e04, 0x02042cb8, +10 more; loops (back edge at +0x10); returns through pop {r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x28
 *   branch +0x2c -> +0x16c
 *   branch +0x40 -> +0x6c
 *   branch +0x48 -> +0x6c
 *   branch +0x70 -> +0x144
 *   branch +0xbc -> +0xe0
 *   branch +0xdc -> +0x124
 *   branch +0xe8 -> +0x104
 *   branch +0x100 -> +0x16c
 *   branch +0x120 -> +0x16c
 *   branch +0x130 -> +0x16c
 *   branch +0x140 -> +0x16c
 *   branch +0x15c -> +0x16c
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r4, #0
 *   test +0x3c cmp r1, #0
 *   test +0x44 tst r0, #8
 *   test +0x6c cmp r4, #0
 *   test +0xd0 cmp r0, #4
 *   test +0xd8 cmpeq r0, #9
 *   test +0xe4 cmp r0, #3
 *   test +0xfc cmp r0, #9
 *   test +0x12c cmp r0, #0
 *   test +0x158 cmp r0, #0
 *   4 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022101c0; the literal pool and
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
extern void native_fn_020c56b4(void);
extern void native_fn_0220ff24(void);
extern void native_fn_02210008(void);
extern void native_fn_02209c68(void);
extern void native_fn_0221008c(void);
extern void native_fn_021e0008(void);


asm u32 native_ov000_022101c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    add r1, sp, #0
    mov r5, r0
    bl native_fn_02042b3c
    movs r4, r0
    beq ov000_022101c0_L28
    bl native_fn_021e0e04
    cmp r0, #0
    moveq r4, #0
ov000_022101c0_L28:
    cmp r4, #0
    beq ov000_022101c0_L16c
    ldr r0, [r5, #0x164]
    bl native_fn_02042cb8
    ldrb r1, [r5, #0x2c1]
    cmp r1, #0
    bne ov000_022101c0_L6c
    tst r0, #8
    beq ov000_022101c0_L6c
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r2, [r0, #0xc]
    add r1, sp, #0
    mov r0, r5
    bl native_fn_0220ff24
    mov r4, r0
ov000_022101c0_L6c:
    cmp r4, #0
    beq ov000_022101c0_L144
    ldrb r0, [r5, #0x2c2]
    bic r0, r0, #240
    orr r0, r0, #16
    strb r0, [r5, #0x2c2]
    ldr r2, [r5, #0x2a8]
    ldr r1, [sp]
    ldr r0, [r5, #0x2b8]
    sub r1, r2, r1
    smull r3, r2, r1, r1
    ldr lr, [r5, #0x2b0]
    ldr r12, [sp, #0x8]
    mov r1, r0, asr #31
    sub r12, lr, r12
    smlal r3, r2, r12, r12
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    blt ov000_022101c0_Le0
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0xa]
    cmp r0, #4
    ldreqb r0, [r5, #0x278]
    cmpeq r0, #9
    bne ov000_022101c0_L124
ov000_022101c0_Le0:
    ldrb r0, [r5, #0x278]
    cmp r0, #3
    bne ov000_022101c0_L104
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #9
    beq ov000_022101c0_L16c
ov000_022101c0_L104:
    add r12, sp, #0
    add r3, r5, #112
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r5, #272
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    b ov000_022101c0_L16c
ov000_022101c0_L124:
    mov r0, r5
    bl native_fn_02210008
    cmp r0, #0
    beq ov000_022101c0_L16c
    mov r0, r5
    mov r1, #7
    bl native_fn_02209c68
    b ov000_022101c0_L16c
ov000_022101c0_L144:
    ldrb r1, [r5, #0x2c2]
    mov r0, r5
    bic r1, r1, #240
    strb r1, [r5, #0x2c2]
    bl native_fn_0221008c
    cmp r0, #0
    beq ov000_022101c0_L16c
    mov r0, r5
    mov r1, #8
    bl native_fn_02209c68
ov000_022101c0_L16c:
    mov r0, r5
    mov r1, r5
    bl native_fn_021e0008
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
