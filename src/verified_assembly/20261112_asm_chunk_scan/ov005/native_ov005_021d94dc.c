/* ov005 row 0x021d94dc: 964 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3bc -> constant 0x00007fff (image word 0x00007fff)
 *   pool +0x3c0 -> constant 0x00001004 (image word 0x00001004)
 *   branch +0x60 -> +0xbc
 *   branch +0xb8 -> +0xec
 *   branch +0xf4 -> +0x108
 *   branch +0x104 -> +0x38c
 *   branch +0x114 -> +0x38c
 *   branch +0x118 -> +0x38c
 *   branch +0x11c -> +0x378
 *   branch +0x120 -> +0x12c
 *   branch +0x124 -> +0x170
 *   branch +0x128 -> +0x344
 *   branch +0x134 -> +0x38c
 *   branch +0x164 -> +0x170
 *   branch +0x16c -> +0x38c
 *   branch +0x178 -> +0x1fc
 *   branch +0x198 -> +0x1a8
 *   branch +0x20c -> +0x38c
 *   branch +0x21c -> +0x288
 *   branch +0x238 -> +0x288
 *   branch +0x294 -> +0x328
 *   branch +0x2b4 -> +0x2f8
 *   branch +0x2c0 -> +0x2c8
 *   back edge +0x2d4 -> +0x2c4
 *   back edge +0x318 -> +0x2ac
 *   branch +0x324 -> +0x38c
 *   branch +0x340 -> +0x38c
 *   branch +0x374 -> +0x38c
 *   branch +0x390 -> +0x3b0
 *   test +0x2c cmp r0, #0
 *   test +0x34 cmp r0, #6
 *   test +0x90 cmp r1, r3, lsr #17
 *   test +0x9c cmpeq r7, r1
 *   test +0xa4 cmp r2, #0
 *   test +0xf0 cmp r0, r1
 *   test +0xfc cmp r0, #4
 *   test +0x10c cmp r0, #4
 *   test +0x130 cmp r0, #2
 *   test +0x14c cmp r1, r0
 *   test +0x158 cmpls r1, r0
 *   test +0x168 cmp r11, #0
 *   test +0x174 cmp r0, #2
 *   test +0x18c cmp r1, r0
 *   test +0x200 cmp r0, #3
 *   test +0x208 cmpeq r0, #3
 *   test +0x218 cmp r7, r0
 *   test +0x234 tst r0, r1, lsl r10
 *   test +0x250 cmp r2, r0
 *   test +0x290 cmp r1, r0
 *   test +0x2b0 cmp r7, #32
 *   test +0x2d0 cmp r6, r1
 *   test +0x300 cmp r6, r1
 *   test +0x314 tst r1, r2, lsl r7
 *   test +0x334 cmp r0, r1
 *   test +0x348 cmp r0, #3
 *   test +0x354 cmpeq r6, r0
 *   test +0x35c cmpeq r1, r0
 *   test +0x36c cmp r0, #4
 *   test +0x380 cmp r11, #0
 *   test +0x38c cmp r4, #0
 *   test +0x398 cmp r0, #0
 *   28 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov005.bin at 0x021d94dc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02008e0c(void);
extern void native_fn_02026350(void);
extern void native_fn_02008c14(void);


asm u32 native_ov005_021d94dc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r9, r0
    ldr r0, [r9, #0x20]
    mov r4, #0
    ldr r0, [r0, #0xc]
    mov r8, r1
    ldr r5, [r0, #0x24]
    mov r11, r4
    ldr r0, [r5, #0x14]
    mov r10, #0
    cmp r0, #0
    ldrh r0, [r8, #4]
    cmp r0, #6
    addlo sp, sp, #12
    movlo r0, r10
    ldmloia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [r8]
    add r1, sp, #4
    mov r2, #6
    bl native_fn_02008e0c
    ldrh r0, [sp, #4]
    mov r1, r0, lsl #31
    movs r1, r1, lsr #31
    beq ov005_021d94dc_Lbc
    ldr r0, [r8]
    add r1, sp, #0
    mov r2, #4
    bl native_fn_02008e0c
    ldrh r2, [sp, #2]
    ldrh r0, [sp]
    ldr r1, =0x00007fff
    mov r6, r2, lsl #31
    mov r3, r0, lsl #16
    mov r2, r2, lsl #16
    mov r7, r2, lsr #17
    cmp r1, r3, lsr #17
    mov r0, r6, lsr #31
    mov r2, r10
    cmpeq r7, r1
    moveq r2, #1
    cmp r2, #0
    movne r1, #4
    moveq r1, #3
    mov r6, r3, lsr #17
    str r1, [r5, #0x18]
    b ov005_021d94dc_Lec
ov005_021d94dc_Lbc:
    mov r0, r0, lsl #24
    mov r0, r0, lsr #27
    str r0, [r5, #0x18]
    ldrh r1, [sp, #4]
    ldrh r6, [sp, #6]
    ldrh r7, [sp, #8]
    mov r2, r1, lsl #30
    mov r0, r1, lsl #29
    mov r1, r1, lsl #16
    mov r11, r2, lsr #31
    mov r0, r0, lsr #31
    mov r10, r1, lsr #24
ov005_021d94dc_Lec:
    ldr r1, [r5, #0x14]
    cmp r0, r1
    beq ov005_021d94dc_L108
    ldr r0, [r5, #0x10]
    cmp r0, #4
    moveq r4, #1
    b ov005_021d94dc_L38c
ov005_021d94dc_L108:
    ldr r0, [r5, #0x18]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov005_021d94dc_L38c
    b ov005_021d94dc_L38c
    b ov005_021d94dc_L378
    b ov005_021d94dc_L12c
    b ov005_021d94dc_L170
    b ov005_021d94dc_L344
ov005_021d94dc_L12c:
    ldr r0, [r5, #0x10]
    cmp r0, #2
    bne ov005_021d94dc_L38c
    str r6, [r9, #0x8]
    strh r10, [r9, #28]
    str r7, [r9, #0x14]
    ldr r1, [r9, #0x4]
    ldr r0, [r9, #0x8]
    cmp r1, r0
    ldrls r1, [r9, #0x14]
    ldrls r0, [r9, #0x18]
    cmpls r1, r0
    movhi r0, #1
    strhi r0, [r5, #0x10]
    bhi ov005_021d94dc_L170
    cmp r11, #0
    beq ov005_021d94dc_L38c
ov005_021d94dc_L170:
    ldr r0, [r5, #0x10]
    cmp r0, #2
    bne ov005_021d94dc_L1fc
    mov r0, #3
    str r0, [r5, #0x10]
    ldrh r1, [r8, #4]
    ldr r0, [r5, #0x8]
    cmp r1, r0
    strne r0, [r5, #0x1c]
    ldrne r0, [r5, #0x4]
    bne ov005_021d94dc_L1a8
    ldr r0, [r5, #0x4]
    str r0, [r5, #0x1c]
    ldr r0, [r5, #0x8]
ov005_021d94dc_L1a8:
    str r0, [r5, #0x20]
    ldr r1, [r5, #0x1c]
    mov r0, #0
    sub r1, r1, #4
    str r1, [r5, #0x1c]
    ldr r1, [r5, #0x20]
    sub r1, r1, #4
    str r1, [r5, #0x20]
    str r0, [r5, #0x24]
    str r0, [r5, #0x28]
    str r0, [r5, #0x2c]
    ldr r0, [r9, #0x14]
    ldr r1, [r5, #0x20]
    add r0, r0, r1
    sub r0, r0, #1
    bl native_fn_02026350
    str r0, [r5, #0x30]
    ldr r2, =0x00001004
    add r1, r5, #52
    mov r0, #0
    bl native_fn_02008c14
ov005_021d94dc_L1fc:
    ldr r0, [r5, #0x18]
    cmp r0, #3
    ldreq r0, [r5, #0x10]
    cmpeq r0, #3
    bne ov005_021d94dc_L38c
    ldr r0, =0x00007fff
    str r6, [r5, #0x28]
    cmp r7, r0
    beq ov005_021d94dc_L288
    mov r6, r7, lsr #5
    add r0, r5, r6, lsl #2
    ldr r0, [r0, #0x34]
    and r10, r7, #31
    mov r1, #1
    tst r0, r1, lsl r10
    bne ov005_021d94dc_L288
    ldr r2, [r5, #0x20]
    ldr r0, [r9, #0x14]
    mul r7, r2, r7
    ldr r1, [r9, #0x10]
    sub r0, r0, r7
    cmp r2, r0
    ldr r3, [r8]
    movhi r2, r0
    add r0, r3, #4
    add r1, r1, r7
    bl native_fn_02008e0c
    add r2, r5, #52
    ldr r1, [r2, r6, lsl #2]
    mov r0, #1
    orr r0, r1, r0, lsl r10
    str r0, [r2, r6, lsl #2]
    ldr r0, [r5, #0x2c]
    add r0, r0, #1
    str r0, [r5, #0x2c]
ov005_021d94dc_L288:
    ldr r1, [r5, #0x2c]
    ldr r0, [r5, #0x30]
    cmp r1, r0
    bhs ov005_021d94dc_L328
    ldr r1, [r5, #0x24]
    mov r3, #0
    mov r0, r1, lsr #5
    and r7, r1, #31
    mov r2, #1
ov005_021d94dc_L2ac:
    add r7, r7, #1
    cmp r7, #32
    blo ov005_021d94dc_L2f8
    add r0, r0, #1
    mvn r1, #0
    b ov005_021d94dc_L2c8
ov005_021d94dc_L2c4:
    add r0, r0, #1
ov005_021d94dc_L2c8:
    add r6, r5, r0, lsl #2
    ldr r6, [r6, #0x34]
    cmp r6, r1
    beq ov005_021d94dc_L2c4
    add r1, r5, r0, lsl #2
    ldr r1, [r1, #0x34]
    mvn r1, r1
    mvn r6, r1
    sub r1, r1, #1
    and r1, r6, r1
    clz r1, r1
    rsb r7, r1, #32
ov005_021d94dc_L2f8:
    ldr r1, [r5, #0x30]
    add r6, r7, r0, lsl #5
    cmp r6, r1
    movhs r0, r3
    add r1, r5, r0, lsl #2
    ldr r1, [r1, #0x34]
    movhs r7, r3
    tst r1, r2, lsl r7
    bne ov005_021d94dc_L2ac
    add r0, r7, r0, lsl #5
    str r0, [r5, #0x24]
    b ov005_021d94dc_L38c
ov005_021d94dc_L328:
    ldr r1, =0x00007fff
    str r1, [r5, #0x24]
    ldr r0, [r5, #0x28]
    cmp r0, r1
    moveq r0, #4
    streq r0, [r5, #0x10]
    b ov005_021d94dc_L38c
ov005_021d94dc_L344:
    ldr r0, [r5, #0x10]
    cmp r0, #3
    ldreq r0, =0x00007fff
    streq r6, [r5, #0x28]
    cmpeq r6, r0
    ldreq r1, [r5, #0x24]
    cmpeq r1, r0
    moveq r0, #4
    streq r0, [r5, #0x10]
    ldr r0, [r5, #0x10]
    cmp r0, #4
    moveq r4, #1
    b ov005_021d94dc_L38c
ov005_021d94dc_L378:
    mov r0, #1
    str r0, [r5, #0x10]
    cmp r11, #0
    movne r0, #0
    strne r0, [r5, #0xc]
ov005_021d94dc_L38c:
    cmp r4, #0
    beq ov005_021d94dc_L3b0
    ldr r0, [r5, #0x14]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    str r0, [r5, #0x14]
    mov r0, #1
    str r0, [r5, #0x10]
ov005_021d94dc_L3b0:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
