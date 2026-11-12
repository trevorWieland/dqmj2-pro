/* ov000 row 0x021e7d64: 424 bytes.
 *
 * What it does: 103 instructions; 12 call(s) to 0x021dffb4, 0x02041f34, 0x02041f90, +9 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x19c -> constant 0x0223526c (image word 0x0223526c)
 *   pool +0x1a0 -> constant 0x0000019a (image word 0x0000019a)
 *   pool +0x1a4 -> native_data_0222edbc (image word 0x0222edbc)
 *   branch +0x30 -> +0x180
 *   branch +0x4c -> +0x180
 *   branch +0x7c -> +0xb0
 *   branch +0x98 -> +0xb0
 *   branch +0xcc -> +0xe8
 *   branch +0xe4 -> +0x124
 *   branch +0xec -> +0x124
 *   back edge +0x18c -> +0x28
 *   test +0x2c cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xc8 cmp r1, #0
 *   test +0xe8 cmp r0, #512
 *   test +0x188 cmp r8, #8
 *   2 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e7d64; the literal pool and
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

extern void native_fn_021dffb4(void);
extern void native_fn_02041f34(void);
extern void native_fn_02041f90(void);
extern void native_fn_021da5e4(void);
extern void native_fn_020430b4(void);
extern void native_fn_02210c34(void);
extern void native_fn_020449d4(void);
extern void native_fn_02041e2c(void);
extern u8 native_data_0222edbc[];
extern void native_fn_02028d50(void);
extern void native_fn_021e7d18(void);


asm u32 native_ov000_021e7d64 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r9, #0
    ldr r10, =0x0223526c
    ldr r4, =0x0000019a
    mov r8, r9
    mov r7, r9
    mov r11, r9
    mov r6, r9
    mov r5, #2048
ov000_021e7d64_L28:
    ldrb r0, [r10, #0x274]
    cmp r0, #0
    beq ov000_021e7d64_L180
    add r1, r10, #256
    ldrsh r1, [r1, #106]
    mov r0, r10
    mov r2, #0
    bl native_fn_021dffb4
    cmp r0, #0
    beq ov000_021e7d64_L180
    ldr r1, [r10, #0x280]
    ldr r2, [r10, #0x284]
    ldr r3, [r10, #0x288]
    mov r0, r10
    bl native_fn_02041f34
    ldr r1, [r10, #0x28c]
    mov r0, r10
    mov r2, #0
    bl native_fn_02041f90
    ldrb r0, [r10, #0x277]
    cmp r0, #0
    bne ov000_021e7d64_Lb0
    add r0, r10, #640
    add r1, r10, #528
    add r2, sp, #0
    mov r3, #2
    bl native_fn_021da5e4
    cmp r0, #0
    beq ov000_021e7d64_Lb0
    mov r0, r10
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    bl native_fn_02041f34
ov000_021e7d64_Lb0:
    add r0, r10, #256
    ldrsh r0, [r0, #106]
    bl native_fn_020430b4
    ldrsh r0, [r0, #2]
    bl native_fn_02210c34
    ldr r1, [r10, #0x290]
    cmp r1, #0
    beq ov000_021e7d64_Le8
    str r1, [r10, #0x7c]
    ldr r0, [r10, #0x294]
    str r0, [r10, #0x80]
    ldr r0, [r10, #0x298]
    str r0, [r10, #0x84]
    b ov000_021e7d64_L124
ov000_021e7d64_Le8:
    cmp r0, #512
    bhs ov000_021e7d64_L124
    bl native_fn_020449d4
    ldr r3, [r0]
    mov r0, r3, asr #31
    umull r2, r1, r3, r4
    mla r1, r3, r11, r1
    mla r1, r0, r4, r1
    adds r2, r2, r5
    adc r0, r1, r6
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    str r1, [r10, #0x7c]
    str r1, [r10, #0x80]
    str r1, [r10, #0x84]
ov000_021e7d64_L124:
    ldr r1, [r10, #0x2a0]
    add r0, r10, #256
    mov r2, #492
    mov r3, r1
    bl native_fn_02041e2c
    add r0, r10, #112
    add r3, r10, #272
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r1, =native_data_0222edbc
    mov r0, r10
    bl native_fn_02028d50
    strb r0, [r10, #0x278]
    mov r0, r10
    mov r1, #0
    mov r2, #1
    bl native_fn_021e7d18
    strb r7, [r10, #0x2a8]
    add r0, r10, #512
    strh r7, [r0, #172]
    ldrb r0, [r10, #0x27a]
    add r9, r9, #1
    strb r0, [r10, #0x1dd]
ov000_021e7d64_L180:
    add r10, r10, #716
    add r8, r8, #1
    cmp r8, #8
    blt ov000_021e7d64_L28
    mov r0, r9
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
