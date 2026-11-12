/* ov000 row 0x021ee458: 2224 bytes.
 *
 * What it does: 555 instructions and 79 call(s), then a 5-entry dispatch through an inline branch table at 0x021ee49c (dispatch word at 0x021ee494)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021ee01c(void);
extern void native_fn_021f04c4(void);
extern void native_fn_021f052c(void);
extern void native_fn_020c4c58(void);
extern void native_fn_021ee300(void);
extern void native_fn_02063144(void);
extern void native_fn_021efc14(void);
extern void native_fn_021f04e4(void);
extern void native_fn_021ed63c(void);
extern void native_fn_02065d88(void);
extern void native_fn_02062b0c(void);
extern void native_fn_021ee168(void);
extern void native_fn_0204a448(void);
extern void native_fn_0208485c(void);
extern void native_fn_0204a724(void);
extern void native_fn_0204a1d0(void);
extern void native_fn_021ee42c(void);
extern void native_fn_021ef518(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_021eff48(void);
extern void native_fn_0204a574(void);
extern void native_fn_021ef4d8(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_021ef474(void);
extern void native_fn_02062a88(void);
extern void native_fn_02211064(void);
extern void native_fn_0204a4ac(void);
extern void native_fn_0207b460(void);
extern void native_fn_0207c424(void);
extern void native_fn_0204a154(void);
extern void native_fn_021efaac(void);


asm u32 native_ov000_021ee458 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #100
    add r2, sp, #32
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldrb r1, [r0]
    str r0, [sp, #0x10]
    ldr r0, [pc, #0x884]
    tst r1, #1
    ldr r5, [r0, #0x4]
    beq L_021ee48c
    bl native_fn_021ee01c
L_021ee48c:
    ldrsb r0, [r5, #32]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021eecec
    dcd 0xea000003
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea0000f9
    dcd 0xea000127
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #1
    beq L_021eecec
    add r0, r5, #16
    bl native_fn_021f04c4
    bl native_fn_021f052c
    b L_021eecec
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #7
    beq L_021ee51c
    ldr r0, [pc, #0x81c]
    mvn r1, #0
    ldr r2, [r0, #0x4]
    ldr r0, [r2, #0x10]
    add r0, r2, r0, lsl #2
    ldr r0, [r0, #0x104]
    mov r0, r0, lsl #16
    mov r4, r0, asr #16
    mov r0, r4
    bl native_fn_020c4c58
    bl native_fn_021ee300
    mov r0, r4
    bl native_fn_02063144
    and r0, r0, #255
    bl native_fn_021efc14
L_021ee51c:
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #1
    beq L_021ee538
    add r0, r5, #16
    bl native_fn_021f04e4
    bl native_fn_021f052c
L_021ee538:
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #2
    beq L_021ee82c
    ldrh r0, [r5, #28]
    mov r10, #0
    cmp r0, #0
    ble L_021ee82c
    mvn r0, #15
    mov r8, #8
    add r11, sp, #32
    str r0, [sp, #0x14]
L_021ee568:
    ldr r0, [pc, #0x794]
    ldr r2, [r5, #0x14]
    ldr r1, [r0, #0x4]
    add r2, r2, r10
    ldrb r0, [r1, #0x504]
    cmp r2, r0
    bge L_021ee7bc
    add r0, r1, r2, lsl #2
    ldr r0, [r0, #0x104]
    ldrsb r1, [r5, #32]
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    cmp r1, #1
    mov r0, r9
    bne L_021ee5b0
    bl native_fn_021ed63c
    mov r6, r0
    b L_021ee5b8
L_021ee5b0:
    bl native_fn_02065d88
    ldr r6, [r0, #0x4]
L_021ee5b8:
    ldrsb r0, [r5, #32]
    mov r7, #1
    cmp r0, #1
    bne L_021ee608
    bl native_fn_02062b0c
    mov r4, r0
    mov r0, r9
    bl native_fn_021ed63c
    cmp r4, r0
    blt L_021ee600
    mov r0, r9
    bl native_fn_02063144
    mov r4, r0
    mov r0, r9
    bl native_fn_02065d88
    ldrb r0, [r0, #0x27]
    cmp r4, r0
    blt L_021ee618
L_021ee600:
    mov r7, #3
    b L_021ee618
L_021ee608:
    mov r0, r9
    bl native_fn_021ee168
    cmp r0, #0
    movne r7, #3
L_021ee618:
    mov r0, #0
    strh r0, [sp, #34]
    mov r0, #16
    strh r0, [sp, #32]
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r10, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, r7
    mov r3, r9
    bl native_fn_0204a448
    ldr r0, [sp, #0x14]
    strh r0, [sp, #32]
    ldrsb r0, [r5, #32]
    cmp r0, #1
    mov r0, r9
    bne L_021ee700
    bl native_fn_0208485c
    cmp r0, #0
    bne L_021ee6d0
    mov r0, r9
    bl native_fn_02063144
    mov r4, r0
    mov r0, r9
    bl native_fn_02065d88
    ldrb r0, [r0, #0x27]
    cmp r4, r0
    blt L_021ee6d0
    mov r0, #2
    str r0, [sp]
    mov r0, #20
    stmib sp, {r0, r7}
    mov r0, #1
    str r0, [sp, #0xc]
    add r0, r10, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, #0
    mov r3, #9
    bl native_fn_0204a724
    b L_021ee770
L_021ee6d0:
    mov r0, #5
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r10, #8
    mov r0, r0, lsl #24
    mov r2, r7
    mov r3, r6
    mov r0, r0, asr #24
    mov r1, r11
    bl native_fn_0204a1d0
    b L_021ee770
L_021ee700:
    bl native_fn_021ee168
    cmp r0, #1
    beq L_021ee73c
    mov r0, #5
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r10, #8
    mov r0, r0, lsl #24
    mov r2, r7
    mov r3, r6
    mov r0, r0, asr #24
    mov r1, r11
    bl native_fn_0204a1d0
    b L_021ee770
L_021ee73c:
    mov r0, #2
    str r0, [sp]
    mov r0, #15
    stmib sp, {r0, r7}
    mov r0, #1
    str r0, [sp, #0xc]
    add r0, r10, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, #0
    mov r3, #9
    bl native_fn_0204a724
L_021ee770:
    ldrsb r0, [r5, #32]
    cmp r0, #1
    bne L_021ee7ac
    mov r0, r9
    bl native_fn_021ee42c
    cmp r0, #0
    beq L_021ee7ac
    mov r0, #8
    strh r0, [sp, #32]
    mov r0, r8, lsl #3
    strh r0, [sp, #34]
    mov r0, r10
    mov r1, r11
    bl native_fn_021ef518
    b L_021ee818
L_021ee7ac:
    mov r0, r10
    mov r1, #0
    bl native_fn_021ef518
    b L_021ee818
L_021ee7bc:
    add r0, r10, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    cmp r0, #0
    ldrne r0, [r0]
    cmpne r0, #0
    beq L_021ee7e4
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
L_021ee7e4:
    add r0, r10, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    cmp r0, #0
    ldrne r0, [r0]
    cmpne r0, #0
    beq L_021ee80c
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
L_021ee80c:
    mov r0, r10
    mov r1, #0
    bl native_fn_021ef518
L_021ee818:
    add r8, r8, #2
    add r10, r10, #1
    ldrh r0, [r5, #28]
    cmp r10, r0
    blt L_021ee568
L_021ee82c:
    ldr r0, [pc, #0x4d0]
    ldr r2, [r0, #0x4]
    ldrb r0, [r2, #0x101]
    cmp r0, #0
    beq L_021eecec
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #4
    beq L_021eecec
    ldr r0, [r2, #0x10]
    ldrsb r1, [r5, #32]
    add r0, r2, r0, lsl #2
    ldr r0, [r0, #0x104]
    cmp r1, #1
    bne L_021ee874
    bl native_fn_021ed63c
    mov r1, r0
    b L_021ee87c
L_021ee874:
    bl native_fn_02065d88
    ldr r1, [r0, #0x4]
L_021ee87c:
    ldr r0, [pc, #0x480]
    ldr r0, [r0, #0x4]
    add r0, r0, #1280
    ldrsh r0, [r0, #6]
    bl native_fn_021eff48
    b L_021eecec
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #1
    beq L_021ee8b0
    add r0, r5, #16
    bl native_fn_021f04c4
    bl native_fn_021f052c
L_021ee8b0:
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #2
    beq L_021eecec
    ldr r0, [pc, #0x43c]
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x50c]
    bl native_fn_02063144
    and r0, r0, #255
    bl native_fn_021efc14
    mov r0, #16
    strh r0, [sp, #32]
    mov r0, #0
    str r0, [sp]
    mov r2, #1
    ldr r0, [pc, #0x410]
    str r2, [sp, #0x4]
    ldr r0, [r0, #0x4]
    add r1, sp, #32
    ldr r3, [r0, #0x50c]
    mov r0, #20
    mov r3, r3, lsl #16
    mov r3, r3, asr #16
    bl native_fn_0204a448
    ldr r0, [pc, #0x3ec]
    mvn r1, #23
    ldr r0, [r0, #0x4]
    strh r1, [sp, #32]
    ldr r0, [r0, #0x50c]
    bl native_fn_021ed63c
    mov r3, r0
    mov r0, #5
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #20
    add r1, sp, #32
    mov r2, #1
    bl native_fn_0204a1d0
    b L_021eecec
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #1
    beq L_021ee96c
    add r0, r5, #16
    bl native_fn_021f04e4
    bl native_fn_021f052c
L_021ee96c:
    ldr r0, [sp, #0x10]
    ldrb r0, [r0]
    tst r0, #2
    beq L_021eecec
    ldr r0, [pc, #0x380]
    add r3, sp, #28
    mov r2, #0
    add r1, sp, #24
    ldr r0, [r0, #0x4]
    strh r2, [r3]
    strh r2, [r3, #2]
    strh r2, [r1]
    strh r2, [r1, #2]
    ldr r0, [r0, #0x50c]
    bl native_fn_02063144
    and r0, r0, #255
    bl native_fn_021efc14
    mov r0, #16
    strh r0, [sp, #28]
    mov r0, #0
    str r0, [sp]
    mov r2, #1
    ldr r0, [pc, #0x338]
    str r2, [sp, #0x4]
    ldr r0, [r0, #0x4]
    add r1, sp, #28
    ldr r3, [r0, #0x50c]
    mov r0, #20
    mov r3, r3, lsl #16
    mov r3, r3, asr #16
    bl native_fn_0204a448
    mvn r0, #23
    strh r0, [sp, #28]
    ldr r0, [pc, #0x30c]
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x50c]
    bl native_fn_021ed63c
    mov r3, r0
    mov r0, #5
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #20
    add r1, sp, #28
    mov r2, #1
    bl native_fn_0204a1d0
    mov r0, #16
    strh r0, [sp, #28]
    mov r0, #11
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #21
    add r1, sp, #28
    mov r2, #9
    mov r3, #2
    bl native_fn_0204a574
    bl native_fn_021ef4d8
    mov r0, #32
    strh r0, [sp, #24]
    mov r0, #64
    strh r0, [sp, #26]
    ldrh r0, [r5, #28]
    mov r9, #0
    cmp r0, #0
    ble L_021eecec
    ldr r10, [pc, #0x284]
    add r7, sp, #28
    mov r11, #1
    mvn r6, #15
L_021eea88:
    bl native_fn_02062aa0
    cmp r9, r0
    bge L_021eeab0
    mov r0, r9
    bl native_fn_02062a50
    mov r8, r0
    mov r0, r9
    add r1, sp, #24
    bl native_fn_021ef474
    b L_021eead4
L_021eeab0:
    bl native_fn_02062aa0
    sub r0, r9, r0
    bl native_fn_02062a88
    mov r8, r0
    bl native_fn_02062aa0
    sub r0, r9, r0
    add r0, r0, #3
    add r1, sp, #24
    bl native_fn_021ef474
L_021eead4:
    ldrsh r1, [sp, #26]
    ldr r0, [r10, #0x4]
    add r1, r1, #16
    strh r1, [sp, #26]
    ldr r0, [r0, #0x50c]
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r8
    bl native_fn_02211064
    cmp r0, #0
    movne r0, #1
    moveq r0, #0
    ands r4, r0, #255
    mov r0, #24
    strh r0, [sp, #28]
    movne r0, #1
    moveq r0, #3
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r9, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r8
    mov r2, #0
    mov r3, r7
    bl native_fn_0204a4ac
    cmp r4, #0
    bne L_021eeb8c
    strh r6, [sp, #28]
    mov r0, #2
    str r0, [sp]
    mov r0, #24
    str r0, [sp, #0x4]
    mov r0, #3
    str r0, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    add r0, r9, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r7
    mov r2, #0
    mov r3, #5
    bl native_fn_0204a724
    b L_021eecdc
L_021eeb8c:
    ldrsh r0, [r8, #24]
    ldrb r1, [r8, #0x1a]
    add r2, r8, #122
    add r3, sp, #36
    bl native_fn_0207b460
    add r0, r8, #32
    add r1, sp, #36
    bl native_fn_0207c424
    mov r4, r0
    mov r1, #0
    strh r1, [sp, #28]
    mov r1, #4
    add r0, r9, #8
    stmia sp, {r1, r11}
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r7
    mov r2, r11
    mov r3, r4
    bl native_fn_0204a154
    ldrsh r1, [sp, #28]
    ldr r0, [r10, #0x4]
    mov r3, #2
    add r1, r1, #32
    strh r1, [sp, #28]
    ldr r1, [r0, #0x50c]
    ldrb r0, [r8, #0x31]
    cmp r1, r0
    bne L_021eec40
    ldrsh r1, [sp, #28]
    add r0, r9, #8
    mov r0, r0, lsl #24
    add r1, r1, #8
    strh r1, [sp, #28]
    mov r1, #10
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    mov r1, r7
    mov r2, #9
    bl native_fn_0204a574
    b L_021eecdc
L_021eec40:
    mov r0, #30
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r0, r9, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r7
    mov r2, #5
    bl native_fn_0204a574
    ldrsh r0, [sp, #28]
    add r0, r0, #8
    strh r0, [sp, #28]
    ldrb r0, [r8, #0x31]
    bl native_fn_02065d88
    mov r8, r0
    ldr r0, [r10, #0x4]
    ldr r0, [r0, #0x50c]
    bl native_fn_02065d88
    ldrh r1, [r8, #28]
    ldrh r0, [r0, #28]
    sub r1, r4, r1
    add r3, r1, r0
    cmp r3, r4
    movgt r2, #9
    bgt L_021eecb8
    movlt r2, #7
    movge r2, #1
L_021eecb8:
    mov r0, #4
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r0, r9, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r7
    bl native_fn_0204a154
L_021eecdc:
    add r9, r9, #1
    ldrh r0, [r5, #28]
    cmp r9, r0
    blt L_021eea88
L_021eecec:
    bl native_fn_021efaac
    ldr r0, [sp, #0x10]
    mov r1, #0
    strb r1, [r0]
    add sp, sp, #100
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02236bc4
}
