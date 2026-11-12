/* ov000 row 0x022208d0: 556 bytes.
 *
 * What it does: 134 instructions; 7 call(s) to 0x0205dc70, 0x02046af4, 0x0205dc70, +4 more; loops (back edge at +0x50); returns through pop {r4, r5, r6, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x218 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x21c -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0x220 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x224 -> constant 0x0224640a (image word 0x0224640a)
 *   pool +0x228 -> constant 0x022463dc (image word 0x022463dc)
 *   branch +0x1c -> +0x11c
 *   branch +0x38 -> +0xe8
 *   branch +0x48 -> +0x7c
 *   branch +0x78 -> +0xa8
 *   branch +0xe4 -> +0x19c
 *   branch +0xfc -> +0x19c
 *   branch +0x118 -> +0x19c
 *   branch +0x120 -> +0x180
 *   branch +0x128 -> +0x180
 *   branch +0x138 -> +0x154
 *   branch +0x150 -> +0x19c
 *   branch +0x168 -> +0x19c
 *   branch +0x17c -> +0x19c
 *   branch +0x1cc -> +0x200
 *   back edge +0x1fc -> +0x1d8
 *   test +0x14 cmp r3, #1
 *   test +0x34 cmp r2, #0
 *   test +0x3c cmp r3, #0
 *   test +0xf4 cmp r2, #0
 *   test +0x108 cmp r1, r0
 *   test +0x11c cmp r5, #0
 *   test +0x124 cmp r3, #2
 *   test +0x134 cmp r0, #0
 *   test +0x15c cmp r0, #0
 *   test +0x170 cmp r0, #0
 *   test +0x188 cmp r0, #0
 *   test +0x19c cmp r5, #0
 *   test +0x1b8 cmp r0, #0
 *   test +0x1c0 cmpne r0, #0
 *   test +0x1e0 cmp r0, #0
 *   test +0x1f8 cmp r3, #3
 *   0 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022208d0; the literal pool and
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

extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_02221118(void);
extern void native_fn_0221cab0(void);


asm u32 native_ov000_022208d0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r6, r0
    ldr r3, [r6]
    mov r5, r1
    cmp r3, #1
    mov r4, #0
    bgt ov000_022208d0_L11c
    ldr r1, =0x022463b0
    mov r0, #132
    ldr r12, [r1, #0x1c]
    mla r2, r3, r0, r12
    ldrsh r2, [r2, #24]
    cmp r2, #0
    beq ov000_022208d0_Le8
    cmp r3, #0
    mov r1, r4
    mov r0, #9
    bne ov000_022208d0_L7c
    mov r2, #2
    bl native_fn_0205dc70
    ldr r2, =0x022463f6
    mov r1, r0
    str r2, [sp]
    mov r12, #255
    ldr r0, =0x021c9698
    mov r2, #24
    mov r3, r4
    str r12, [sp, #0x4]
    bl native_fn_02046af4
    b ov000_022208d0_La8
ov000_022208d0_L7c:
    mov r2, #3
    bl native_fn_0205dc70
    ldr r2, =0x0224640a
    mov r1, r0
    str r2, [sp]
    mov r12, #255
    ldr r0, =0x021c9698
    mov r2, #24
    mov r3, r4
    str r12, [sp, #0x4]
    bl native_fn_02046af4
ov000_022208d0_La8:
    ldr r1, =0x022463b0
    ldr r3, [r6]
    ldr r2, [r1, #0x1c]
    mov r0, #132
    mla r2, r3, r0, r2
    mov r12, #0
    strh r12, [r2, #24]
    ldr r2, [r1, #0x1c]
    ldr r3, [r6]
    mla r2, r3, r0, r2
    str r12, [r2, #0x14]
    ldr r2, [r6]
    ldr r1, [r1, #0x1c]
    mla r0, r2, r0, r1
    strb r2, [r0, #0x1b]
    b ov000_022208d0_L19c
ov000_022208d0_Le8:
    rsb r3, r3, #1
    mla r2, r3, r0, r12
    ldrsh r2, [r2, #24]
    cmp r2, #0
    strne r3, [r6]
    bne ov000_022208d0_L19c
    ldr r1, [r1, #0x20]
    sub r0, r0, #133
    cmp r1, r0
    movne r0, #2
    strne r0, [r6]
    moveq r4, #1
    b ov000_022208d0_L19c
ov000_022208d0_L11c:
    cmp r5, #0
    beq ov000_022208d0_L180
    cmp r3, #2
    bne ov000_022208d0_L180
    ldr r1, =0x022463b0
    ldrb r0, [r1, #0x2]
    cmp r0, #0
    beq ov000_022208d0_L154
    sub r0, r4, #1
    str r0, [r1, #0x20]
    mov r0, r5
    strb r4, [r1, #0x2]
    bl native_fn_02221118
    b ov000_022208d0_L19c
ov000_022208d0_L154:
    ldr r1, [r1, #0x1c]
    ldrsh r0, [r1, #156]
    cmp r0, #0
    movne r0, #1
    strne r0, [r6]
    bne ov000_022208d0_L19c
    ldrsh r0, [r1, #24]
    cmp r0, #0
    strne r4, [r6]
    moveq r4, #1
    b ov000_022208d0_L19c
ov000_022208d0_L180:
    ldr r0, =0x022463b0
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    moveq r0, #1
    streq r0, [r6]
    addne r0, r5, #1
    strne r0, [r6]
ov000_022208d0_L19c:
    cmp r5, #0
    movne r1, #6
    moveq r1, #5
    ldr r0, =0x022463b0
    and r2, r1, #255
    ldr r1, [r0, #0x1c]
    ldrsh r0, [r1, #24]
    cmp r0, #0
    ldrnesh r0, [r1, #156]
    cmpne r0, #0
    subeq r0, r2, #3
    andeq r2, r0, #255
    beq ov000_022208d0_L200
    ldr r1, =0x022463dc
    mov r3, #0
ov000_022208d0_L1d8:
    mov r0, r3, lsl #1
    ldrsh r0, [r1, r0]
    cmp r0, #0
    subeq r0, r2, #1
    andeq r2, r0, #255
    add r0, r3, #1
    mov r0, r0, lsl #24
    mov r3, r0, asr #24
    cmp r3, #3
    blt ov000_022208d0_L1d8
ov000_022208d0_L200:
    strh r2, [r6, #12]
    strh r2, [r6, #14]
    bl native_fn_0221cab0
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
