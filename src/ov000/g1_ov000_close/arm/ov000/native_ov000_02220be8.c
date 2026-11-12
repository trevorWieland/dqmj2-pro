/* ov000 row 0x02220be8: 748 bytes.
 *
 * What it does: 183 instructions; 19 call(s) to 0x0221c658, 0x02220c84, 0x02220680, +16 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2dc -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0x2e0 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x2e4 -> constant 0x020dbf18 (image word 0x020dbf18)
 *   pool +0x2e8 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x3c -> +0x48
 *   branch +0x44 -> +0x58
 *   branch +0x4c -> +0x148
 *   branch +0x54 -> +0x148
 *   branch +0x68 -> +0xa4
 *   branch +0x74 -> +0x9c
 *   branch +0x98 -> +0xb8
 *   branch +0xa0 -> +0xb8
 *   back edge +0x158 -> +0x38
 *   branch +0x1c0 -> +0x228
 *   branch +0x280 -> +0x294
 *   branch +0x290 -> +0x2b0
 *   branch +0x2ac -> +0x2b4
 *   test +0x38 cmp r10, #0
 *   test +0x40 cmp r6, #0
 *   test +0x48 cmp r10, #1
 *   test +0x50 cmp r7, #0
 *   test +0x64 cmp r1, #0
 *   test +0x70 cmp r1, #10
 *   test +0x88 cmp r1, #2
 *   test +0x90 cmpeq r0, #2
 *   test +0xac cmp r0, #0
 *   test +0x154 cmp r10, #2
 *   test +0x160 cmp r0, #0
 *   test +0x170 tst r0, #4
 *   test +0x1b4 cmp r1, r0
 *   test +0x27c cmp r0, #0
 *   test +0x28c cmp r0, #3
 *   test +0x2a0 cmp r1, r0
 *   1 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220be8; the literal pool and
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

extern void native_fn_0221c658(void);
extern void native_fn_02220680(void);
extern void native_fn_020449d4(void);
extern void native_fn_0221f5fc(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02087554(void);
extern void native_fn_02087a48(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_020877bc(void);
extern void native_fn_02062b0c(void);


asm u32 native_ov000_02220be8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    str r1, [sp, #0xc]
    str r0, [sp, #0x8]
    bl native_fn_0221c658
    mov r10, #0
    str r0, [sp, #0x10]
    ldr r0, [sp, #0xc]
    ldr r5, =0x022463f6
    ldr r11, =0x022463b0
    mov r4, r10
    and r6, r0, #1
    and r7, r0, #2
    mov r8, r10
ov000_02220be8_L38:
    cmp r10, #0
    bne ov000_02220be8_L48
    cmp r6, #0
    bne ov000_02220be8_L58
ov000_02220be8_L48:
    cmp r10, #1
    bne ov000_02220be8_L148
    cmp r7, #0
    beq ov000_02220be8_L148
ov000_02220be8_L58:
    ldr r3, [r11, #0x1c]
    add r0, r3, r4
    ldrsh r1, [r0, #24]
    cmp r1, #0
    beq ov000_02220be8_La4
    ldrb r1, [r0, #0x30]
    cmp r1, #10
    blo ov000_02220be8_L9c
    rsb r2, r10, #1
    mov r1, #132
    mla r1, r2, r1, r3
    ldrb r1, [r1, #0x1b]
    cmp r1, #2
    ldreqb r0, [r0, #0x1b]
    cmpeq r0, #2
    movne r9, #5
    bne ov000_02220be8_Lb8
ov000_02220be8_L9c:
    mov r9, #3
    b ov000_02220be8_Lb8
ov000_02220be8_La4:
    mov r0, r10
    bl native_fn_02220680
    cmp r0, #0
    movne r9, #1
    moveq r9, #3
ov000_02220be8_Lb8:
    ldr r0, [r11, #0x1c]
    add r0, r0, r4
    ldrsh r0, [r0, #24]
    bl native_fn_020449d4
    mov r1, #0
    stmia sp, {r1, r9}
    ldrh r1, [r0, #4]
    add r0, r10, #10
    mov r0, r0, lsl #24
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    and r2, r1, #255
    mov r0, r0, asr #24
    mov r1, r5
    mov r3, #24
    bl native_fn_0221f5fc
    add r0, r10, #10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r9, r0
    mov r0, r10, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_02087554
    strh r0, [sp, #20]
    strh r8, [sp, #22]
    mov r0, #1
    str r0, [sp]
    add r0, sp, #20
    str r0, [sp, #0x4]
    ldr r0, [r9]
    mov r1, r8
    ldr r0, [r0, #0x4]
    mov r2, #8
    mov r3, r8
    bl native_fn_02087a48
ov000_02220be8_L148:
    add r4, r4, #132
    add r5, r5, #20
    add r10, r10, #1
    cmp r10, #2
    blt ov000_02220be8_L38
    ldr r0, [sp, #0x8]
    cmp r0, #0
    addeq sp, sp, #60
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0xc]
    tst r0, #4
    addeq sp, sp, #60
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #12
    bl native_fn_02049ad0
    mov r5, r0
    ldr r0, [r5]
    ldr r4, [r0, #0x4]
    mov r0, r4
    bl native_fn_02049ffc
    mov r0, r5
    bl native_fn_02049f4c
    ldr r1, =0x020dbf18
    ldr r0, =0x022463b0
    ldrh r2, [r1, #66]
    ldr r1, [r0, #0x20]
    mvn r0, #0
    cmp r1, r0
    strh r2, [sp, #28]
    mov r1, #0
    bne ov000_02220be8_L228
    mov r0, #9
    mov r2, #4
    bl native_fn_0205dc70
    mov r3, #58
    mov r1, r0
    strh r3, [sp, #30]
    add r2, sp, #32
    str r2, [sp]
    mov r5, #255
    ldr r0, =0x021c9698
    mov r2, #15
    mov r3, #8
    str r5, [sp, #0x4]
    bl native_fn_02046af4
    mov r0, #1
    mov r1, #0
    str r0, [sp]
    add r5, sp, #28
    mov r0, r4
    mov r3, r1
    mov r2, #8
    str r5, [sp, #0x4]
    bl native_fn_02087a48
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02220be8_L228:
    mov r0, #58
    strh r0, [sp, #30]
    strh r1, [sp, #32]
    mov r0, #1
    str r0, [sp]
    add r5, sp, #28
    mov r0, r4
    mov r3, r1
    mov r2, #8
    str r5, [sp, #0x4]
    bl native_fn_02087a48
    ldr r0, =0x022463b0
    mov r1, r5
    ldr r0, [r0, #0x20]
    mov r2, #14
    mov r3, #6
    bl native_fn_020877bc
    ldr r0, =0x022463b0
    mov r1, #0
    ldrb r0, [r0, #0x2]
    strh r1, [sp, #40]
    cmp r0, #0
    bne ov000_02220be8_L294
    ldr r0, [sp, #0x10]
    ldrsb r0, [r0, #16]
    cmp r0, #3
    bne ov000_02220be8_L2b0
ov000_02220be8_L294:
    bl native_fn_02062b0c
    ldr r1, =0x022463b0
    ldr r1, [r1, #0x20]
    cmp r1, r0
    movle r0, #5
    movgt r0, #3
    b ov000_02220be8_L2b4
ov000_02220be8_L2b0:
    mov r0, #1
ov000_02220be8_L2b4:
    mov r1, #0
    str r0, [sp]
    add r5, sp, #28
    mov r0, r4
    mov r3, r1
    mov r2, #24
    str r5, [sp, #0x4]
    bl native_fn_02087a48
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
