/* ov000 row 0x02228170: 1064 bytes.
 *
 * What it does: 266 instructions; 29 call(s) to 0x02065d88, 0x02065d88, 0x02228d58, +26 more; loops (back edge at +0x50); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x48 -> +0xa4
 *   branch +0x5c -> +0x78
 *   branch +0x74 -> +0x84
 *   branch +0x80 -> +0x8c
 *   branch +0xbc -> +0xd8
 *   branch +0xf4 -> +0x114
 *   branch +0x120 -> +0x134
 *   branch +0x130 -> +0x240
 *   branch +0x204 -> +0x224
 *   branch +0x254 -> +0x270
 *   branch +0x284 -> +0x2b8
 *   branch +0x298 -> +0x2b8
 *   branch +0x2bc -> +0x2f8
 *   branch +0x2d4 -> +0x2f8
 *   branch +0x308 -> +0x324
 *   branch +0x320 -> +0x330
 *   branch +0x334 -> +0x360
 *   test +0x20 cmp r5, r6
 *   test +0x44 cmpeq r11, r0
 *   test +0x58 cmp r0, #3
 *   test +0x70 cmp r0, #3
 *   test +0x8c cmp r9, #0
 *   test +0xb8 cmp r0, r1
 *   test +0xc4 cmp r9, r4
 *   test +0xf0 cmp r0, r1
 *   test +0xfc cmp r9, r4
 *   test +0x11c cmp r0, #0
 *   test +0x12c cmp r0, #0
 *   test +0x134 cmp r9, #0
 *   test +0x164 cmp r0, #7
 *   test +0x188 cmp r0, r1
 *   test +0x1ac cmp r0, #7
 *   test +0x1d0 cmp r0, r1
 *   test +0x1ec cmp r0, r1
 *   test +0x200 cmp r0, #0
 *   test +0x250 cmp r0, r1
 *   test +0x258 cmp r9, r4
 *   test +0x270 cmp r4, #0
 *   test +0x280 cmp r9, #0
 *   test +0x294 cmp r0, #3
 *   test +0x2b8 cmp r9, #1
 *   test +0x2d0 cmp r0, #3
 *   test +0x304 cmp r0, #3
 *   test +0x31c cmp r0, #3
 *   test +0x330 cmp r9, #2
 *   test +0x378 cmp r0, #7
 *   test +0x39c cmp r0, r1
 *   test +0x3c8 cmp r0, #7
 *   test +0x3ec cmp r0, r1
 *   0 block transfer(s), 23 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228170; the literal pool and
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

extern void native_fn_02065d88(void);
extern void native_fn_02228d58(void);
extern void native_fn_02228c30(void);
extern void native_fn_02044d60(void);
extern void native_fn_020449d4(void);
extern void native_fn_02044dc4(void);
extern void native_fn_02228968(void);
extern void native_fn_02228ac8(void);
extern void native_fn_02228b78(void);
extern void native_fn_02228650(void);


asm u32 native_ov000_02228170 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r10, r0
    mov r0, r1
    ldrsh r6, [r0, #24]
    ldrsh r5, [r10, #24]
    ldrb r0, [r0, #0x1a]
    ldrb r11, [r10, #0x1a]
    cmp r5, r6
    ldr r8, [sp, #0x30]
    mov r4, #0
    ldr r7, [sp, #0x34]
    strb r4, [r8]
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r9, r3
    str r4, [r7]
    cmpeq r11, r0
    bne ov000_02228170_La4
    ldrb r0, [r10, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    beq ov000_02228170_L78
    ldr r0, [sp, #0x4]
    ldrb r0, [r0, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    bne ov000_02228170_L84
ov000_02228170_L78:
    mov r0, #8
    strb r0, [r8]
    b ov000_02228170_L8c
ov000_02228170_L84:
    mov r0, #10
    strb r0, [r8]
ov000_02228170_L8c:
    cmp r9, #0
    addeq sp, sp, #12
    moveq r0, r5
    streq r11, [r7]
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r4, r4, #1
ov000_02228170_La4:
    ldr r1, [sp, #0x4]
    mov r0, r10
    mov r2, r7
    bl native_fn_02228d58
    mvn r1, #0
    cmp r0, r1
    beq ov000_02228170_Ld8
    mov r1, #9
    cmp r9, r4
    addeq sp, sp, #12
    strb r1, [r8]
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r4, r4, #1
ov000_02228170_Ld8:
    ldr r1, [sp, #0x4]
    mov r2, #0
    mov r0, r10
    str r2, [r7]
    bl native_fn_02228c30
    mvn r1, #0
    cmp r0, r1
    beq ov000_02228170_L114
    mov r1, #1
    cmp r9, r4
    strb r1, [r8]
    addeq sp, sp, #12
    streqb r1, [r8]
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r4, r4, #1
ov000_02228170_L114:
    mov r0, r5
    bl native_fn_02044d60
    cmp r0, #0
    bne ov000_02228170_L134
    mov r0, r6
    bl native_fn_02044d60
    cmp r0, #0
    beq ov000_02228170_L240
ov000_02228170_L134:
    cmp r9, #0
    addne sp, sp, #12
    mvnne r0, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r1, #4
    mov r0, r6
    strb r1, [r8]
    bl native_fn_020449d4
    mov r4, r0
    ldr r1, [sp, #0x8]
    mov r0, r6
    bl native_fn_02044dc4
    cmp r0, #7
    ldrh r1, [r4, #4]
    movhs r2, #1
    movlo r2, #0
    mov r1, r1, lsl #24
    mov r0, r5
    mov r1, r1, lsr #28
    bl native_fn_02228968
    mvn r1, #0
    cmp r0, r1
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r5
    bl native_fn_020449d4
    mov r4, r0
    mov r0, r5
    mov r1, r11
    bl native_fn_02044dc4
    cmp r0, #7
    ldrh r1, [r4, #4]
    movhs r2, #1
    movlo r2, #0
    mov r1, r1, lsl #24
    mov r0, r6
    mov r1, r1, lsr #28
    bl native_fn_02228968
    mvn r1, #0
    cmp r0, r1
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r5
    mov r1, r6
    bl native_fn_02228ac8
    mvn r1, #0
    cmp r0, r1
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r5
    bl native_fn_02044d60
    cmp r0, #0
    beq ov000_02228170_L224
    ldr r3, [sp, #0x8]
    mov r0, r5
    mov r1, r11
    mov r2, r6
    bl native_fn_02228b78
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L224:
    ldr r1, [sp, #0x8]
    mov r0, r6
    mov r2, r5
    mov r3, r11
    bl native_fn_02228b78
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L240:
    mov r0, r5
    mov r1, r6
    bl native_fn_02228ac8
    mvn r1, #0
    cmp r0, r1
    beq ov000_02228170_L270
    cmp r9, r4
    moveq r1, #2
    add sp, sp, #12
    streqb r1, [r8]
    movne r0, r1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L270:
    cmp r4, #0
    addgt sp, sp, #12
    movgt r0, r1
    ldmgtia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    cmp r9, #0
    bne ov000_02228170_L2b8
    ldrb r0, [r10, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    bne ov000_02228170_L2b8
    mov r0, #8
    strb r0, [r8]
    ldrb r1, [r10, #0x1a]
    add sp, sp, #12
    mov r0, r5
    str r1, [r7]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L2b8:
    cmp r9, #1
    bne ov000_02228170_L2f8
    ldr r0, [sp, #0x4]
    ldrb r0, [r0, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    bne ov000_02228170_L2f8
    mov r0, #8
    strb r0, [r8]
    ldr r0, [sp, #0x4]
    add sp, sp, #12
    ldrb r1, [r0, #0x1a]
    mov r0, r6
    str r1, [r7]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L2f8:
    ldrb r0, [r10, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    beq ov000_02228170_L324
    ldr r0, [sp, #0x4]
    ldrb r0, [r0, #0x31]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2a]
    cmp r0, #3
    bne ov000_02228170_L330
ov000_02228170_L324:
    add sp, sp, #12
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L330:
    cmp r9, #2
    bhs ov000_02228170_L360
    mov r0, #0
    strb r0, [r8]
    ldr r3, [sp, #0x8]
    mov r0, r5
    mov r1, r6
    mov r2, r11
    str r9, [sp]
    bl native_fn_02228650
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228170_L360:
    mov r0, r6
    bl native_fn_020449d4
    mov r4, r0
    ldr r1, [sp, #0x8]
    mov r0, r6
    bl native_fn_02044dc4
    cmp r0, #7
    ldrh r1, [r4, #4]
    movhs r2, #1
    movlo r2, #0
    mov r1, r1, lsl #24
    mov r0, r5
    mov r1, r1, lsr #28
    bl native_fn_02228968
    mvn r1, #0
    cmp r0, r1
    movne r1, #3
    addne sp, sp, #12
    strneb r1, [r8]
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r5
    bl native_fn_020449d4
    mov r4, r0
    mov r0, r5
    mov r1, r11
    bl native_fn_02044dc4
    cmp r0, #7
    ldrh r1, [r4, #4]
    movhs r2, #1
    movlo r2, #0
    mov r1, r1, lsl #24
    mov r0, r6
    mov r1, r1, lsr #28
    bl native_fn_02228968
    mvn r1, #0
    cmp r0, r1
    movne r1, #3
    addne sp, sp, #12
    strneb r1, [r8]
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r3, [sp, #0x8]
    mov r0, r5
    mov r1, r6
    mov r2, r11
    str r9, [sp]
    bl native_fn_02228650
    mov r1, #0
    strb r1, [r8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
