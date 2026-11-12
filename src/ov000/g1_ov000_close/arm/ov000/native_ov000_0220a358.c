/* ov000 row 0x0220a358: 348 bytes.
 *
 * What it does: 85 instructions; 14 call(s) to 0x020c58c0, 0x02044cdc, 0x021dffb4, +11 more; loops (back edge at +0x2c); returns through pop {r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x154 -> constant 0x02238634 (image word 0x02238634)
 *   pool +0x158 -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0x20 -> +0x148
 *   branch +0x4c -> +0x148
 *   branch +0x98 -> +0xb0
 *   test +0x1c cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0x11c cmp r0, #0
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a358; the literal pool and
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

extern void native_fn_020c58c0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021dffb4(void);
extern void native_fn_02041f34(void);
extern void native_fn_02041f90(void);
extern void native_fn_020c56b4(void);
extern void native_fn_021da5e4(void);
extern void native_fn_020449d4(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_0220a30c(void);
extern void native_fn_0221089c(void);


asm u32 native_ov000_0220a358 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r2, =0x02238634
    mov r1, #708
    mla r4, r0, r1, r2
    ldrb r0, [r4, #0x274]
    mov r5, #0
    cmp r0, #0
    beq ov000_0220a358_L148
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c58c0
    bl native_fn_02044cdc
    add r1, r4, #256
    mov r2, r0
    ldrsh r1, [r1, #106]
    mov r0, r4
    bl native_fn_021dffb4
    cmp r0, #0
    beq ov000_0220a358_L148
    ldr r1, [r4, #0x2a8]
    ldr r2, [r4, #0x2ac]
    ldr r3, [r4, #0x2b0]
    mov r0, r4
    bl native_fn_02041f34
    ldr r1, [r4, #0x2b4]
    mov r0, r4
    mov r2, r5
    bl native_fn_02041f90
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r3, [r0, #0xc]
    add r0, r4, #680
    add r1, r4, #528
    add r2, sp, #0
    bl native_fn_021da5e4
    cmp r0, #0
    beq ov000_0220a358_Lb0
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r4
    bl native_fn_02041f34
ov000_0220a358_Lb0:
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c58c0
    bl native_fn_020449d4
    ldr r12, [r0]
    ldr r0, =0x0000019a
    mov r1, r12, asr #31
    umull r3, r2, r12, r0
    mla r2, r1, r0, r2
    adds r3, r3, #2048
    adc r0, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r0, lsl #20
    str r3, [r4, #0x7c]
    str r3, [r4, #0x80]
    mov r0, r4
    mov r1, #0
    mov r2, #1
    str r3, [r4, #0x84]
    bl native_fn_0220a2a4
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c58c0
    mov r1, r0
    mov r0, r4
    bl native_fn_0220a30c
    ldrb r0, [r4, #0x1e5]
    cmp r0, #0
    moveq r1, #1
    movne r1, #0
    mov r0, r4
    and r1, r1, #255
    bl native_fn_0221089c
    add r0, r4, #112
    add r3, r4, #272
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r5, #1
ov000_0220a358_L148:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
