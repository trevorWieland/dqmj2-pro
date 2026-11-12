/* ov000 row 0x021ff6bc: 2952 bytes.
 *
 * What it does: 729 instructions and 120 call(s), then a 8-entry dispatch through an inline branch table at 0x021ff70c (dispatch word at 0x021ff704)
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

extern void native_fn_02215698(void);
extern void native_fn_0202a634(void);
extern void native_fn_022156c4(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02049f24(void);
extern void native_fn_02008d78(void);
extern void native_fn_02215ce4(void);
extern void native_fn_022004c8(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02217ac8(void);
extern void native_fn_0205dc70(void);
extern void native_fn_0205dc88(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02216664(void);
extern void native_fn_021ff5e4(void);
extern void native_fn_0221570c(void);
extern void native_fn_0221794c(void);
extern void native_fn_0204b5d4(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_0207afec(void);
extern void native_fn_0207b460(void);
extern void native_fn_0207b244(void);
extern void native_fn_02062378(void);
extern void native_fn_0206de44(void);
extern void native_fn_02215d94(void);
extern void native_fn_02210f74(void);
extern void native_fn_02215324(void);
extern void native_fn_0207c0d4(void);
extern void native_fn_0207c11c(void);
extern void native_fn_0205f35c(void);
extern void native_fn_0203d294(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c73c(void);
extern void native_fn_02026144(void);
extern void native_fn_0207d198(void);
extern void native_fn_022014e8(void);
extern void native_fn_02060954(void);
extern void native_fn_02047ff0(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02217c9c(void);
extern void native_fn_022008d8(void);
extern void native_fn_02201428(void);


asm u32 native_ov000_021ff6bc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #220
    bl native_fn_02215698
    ldr r1, [pc, #0xb50]
    mov r5, #0
    ldr r6, [r1, #0x2d8]
    mov r4, r0
    bl native_fn_0202a634
    mov r8, r0
    bl native_fn_022156c4
    str r0, [sp, #0x14]
    mov r7, r5
    bl native_fn_02062aa0
    bl native_fn_02062ad0
    bl native_fn_02049f24
    ldr r2, [pc, #0xb20]
    ldr r0, [r2]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_022001f0
    dcd 0xea000006
    dcd 0xea000035
    dcd 0xea000083
    dcd 0xea000095
    dcd 0xea0000e6
    dcd 0xea0000f9
    dcd 0xea00022a
    dcd 0xea000278
    ldr r0, [pc, #0xaf0]
    mov r1, r5
    mov r2, #768
    bl native_fn_02008d78
    ldr r10, [pc, #0xadc]
    mov r8, r5
    mov r6, r10
    mov r11, r5
L_021ff74c:
    mov r9, r11
    strb r11, [r10, #0x5dc]
    add r5, r6, r8, lsl #7
    and r7, r8, #255
L_021ff75c:
    mov r0, r7
    mov r1, r9
    bl native_fn_02215ce4
    cmp r0, #0
    beq L_021ff78c
    ldrb r0, [r10, #0x5dc]
    and r1, r9, #255
    add r0, r5, r0, lsl #2
    str r1, [r0, #0x2dc]
    ldrb r0, [r10, #0x5dc]
    add r0, r0, #1
    strb r0, [r10, #0x5dc]
L_021ff78c:
    add r9, r9, #1
    cmp r9, #256
    blt L_021ff75c
    add r8, r8, #1
    cmp r8, #6
    add r10, r10, #1
    blt L_021ff74c
    ldr r5, [pc, #0xa78]
    mov r0, #1
    bl native_fn_022004c8
    add r0, r4, #16
    mov r1, #1
    bl native_fn_0204b61c
    ldr r1, [r5]
    ldr r0, [pc, #0xa60]
    ldr r0, [r0, r1, lsl #2]
    bl native_fn_0206dcd0
    ldr r1, [pc, #0xa48]
    mov r2, #1
    mov r0, #0
    str r2, [r1]
    bl native_fn_02217ac8
    mov r7, #1
    b L_022001f0
    ldrh r0, [r8, #2]
    ldr r5, [pc, #0xa30]
    tst r0, #1
    beq L_021ff8f0
    ldrh r0, [r5, #12]
    ldr r3, [r5]
    sub r0, r0, #1
    cmp r3, r0
    beq L_021ff8dc
    ldr r0, [pc, #0xa18]
    ldrb r0, [r0, r3]
    cmp r0, #0
    beq L_021ff898
    cmp r0, #1
    beq L_021ff838
    cmp r0, #2
    moveq r0, #3
    streqb r0, [r2, #0x5e7]
    b L_021ff840
L_021ff838:
    mov r0, #2
    strb r0, [r2, #0x5e7]
L_021ff840:
    ldr r1, [pc, #0x9d8]
    mov r0, #5
    ldrb r2, [r1, #0x5e7]
    mov r1, #6
    add r2, r2, #15
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_0205dc70
    bl native_fn_0205dc88
    cmp r0, #0
    beq L_021ff88c
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b61c
    ldr r0, [pc, #0x9a0]
    mov r1, #1
    str r1, [r0, #0x4]
    mov r1, #6
    str r1, [r0]
L_021ff88c:
    mov r0, #84
    bl native_fn_021e7b9c
    b L_022001f0
L_021ff898:
    mov r1, #2
    str r1, [r2]
    ldr r0, [pc, #0x984]
    mov r1, r7
    ldr r3, [r0, r3, lsl #2]
    add r0, r4, #16
    str r3, [r2, #0x2d8]
    bl native_fn_0204b61c
    mov r0, r5
    bl native_fn_02216664
    ldr r1, [pc, #0x958]
    mov r2, r7
    str r2, [r1, #0xf8]
    mov r0, #82
    str r2, [r1, #0xfc]
    bl native_fn_021e7b9c
    b L_022001f0
L_021ff8dc:
    mov r0, #1
    bl native_fn_021ff5e4
    mov r0, #1
    bl native_fn_0221570c
    b L_022001f0
L_021ff8f0:
    tst r0, #2
    beq L_021ff904
    mov r0, #1
    bl native_fn_021ff5e4
    b L_022001f0
L_021ff904:
    mov r0, r5
    bl native_fn_0221794c
    movs r7, r0
    beq L_022001f0
    ldr r1, [r5]
    ldr r0, [pc, #0x90c]
    ldr r0, [r0, r1, lsl #2]
    bl native_fn_0206dcd0
    b L_022001f0
    mov r0, #3
    ldr r5, [pc, #0x900]
    bl native_fn_022004c8
    ldr r2, [pc, #0x8e4]
    mov r3, #3
    add r0, r4, #16
    mov r1, #1
    str r3, [r2]
    bl native_fn_0204b61c
    add r0, r4, #16
    mov r1, #36
    bl native_fn_0204b5d4
    add r0, r4, #16
    mov r1, #224
    bl native_fn_0204b5b0
    mov r0, #1
    bl native_fn_02217ac8
    mov r7, #1
    b L_022001f0
    ldr r5, [pc, #0x8b8]
    mov r0, r5
    bl native_fn_0221794c
    ldrh r1, [r8, #2]
    mov r7, r0
    tst r1, #1
    beq L_021ffaa0
    ldr r0, [pc, #0x888]
    ldr r2, [pc, #0x888]
    ldr r1, [r0, #0x8]
    ldr r0, [r0, #0xf8]
    and r3, r1, #255
    and r1, r0, #255
    add r0, r2, r3, lsl #7
    ldr r0, [r0, r1, lsl #2]
    mov r0, r0, lsl #16
    mov r9, r0, lsr #16
    mov r0, r9
    bl native_fn_0207afec
    mov r8, r0
    ldrsh r0, [r6, #24]
    ldrb r1, [r6, #0x1a]
    add r3, sp, #156
    add r2, r6, #122
    bl native_fn_0207b460
    ldrsh r1, [r6, #38]
    mov r0, r9
    add r2, sp, #156
    bl native_fn_0207b244
    ldr r1, [r5]
    ldr r0, [pc, #0x83c]
    ldrb r0, [r0, r1]
    cmp r0, #0
    beq L_021ffa58
    mov r6, #4
    add r0, r6, #15
    mov r0, r0, lsl #16
    ldr r3, [pc, #0x810]
    mov r2, r0, lsr #16
    mov r0, #5
    mov r1, #6
    strb r6, [r3, #0x5e7]
    bl native_fn_0205dc70
    bl native_fn_0205dc88
    cmp r0, #0
    beq L_021ffa4c
    add r0, r4, #16
    mov r1, #38
    bl native_fn_0204b5d4
    ldr r0, [pc, #0x7e0]
    mov r1, #3
    str r1, [r0, #0x4]
    mov r1, #6
    str r1, [r0]
L_021ffa4c:
    mov r0, #84
    bl native_fn_021e7b9c
    b L_022001f0
L_021ffa58:
    ldrh r0, [r8, #8]
    ldr r2, [pc, #0x7bc]
    mov r3, #4
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    moveq r1, #1
    movne r1, #0
    strb r1, [r2, #0x5e8]
    add r0, r4, #16
    mov r1, #0
    str r3, [r2]
    bl native_fn_0204b61c
    mov r0, r5
    bl native_fn_02216664
    mov r0, #82
    bl native_fn_021e7b9c
    b L_022001f0
L_021ffaa0:
    tst r1, #2
    beq L_022001f0
    mov r0, #3
    bl native_fn_021ff5e4
    mov r0, #83
    bl native_fn_021e7b9c
    b L_022001f0
    mov r0, #5
    ldr r5, [pc, #0x770]
    bl native_fn_022004c8
    add r0, r4, #16
    mov r1, #1
    bl native_fn_0204b61c
    ldr r0, [pc, #0x744]
    mov r1, #5
    str r1, [r0]
    ldr r0, [r0, #0x5f8]
    bl native_fn_0206dcd0
    bl native_fn_02062378
    cmp r0, #1
    bne L_021ffafc
    mov r0, #1
    bl native_fn_0206de44
L_021ffafc:
    mov r0, #0
    bl native_fn_02217ac8
    mov r7, #1
    b L_022001f0
    ldr r0, [r2, #0x8]
    ldr r1, [r2, #0xf8]
    ldr r3, [pc, #0x708]
    and r5, r0, #255
    ldrb r0, [r2, #0x5e8]
    and r2, r1, #255
    add r1, r3, r5, lsl #7
    ldr r1, [r1, r2, lsl #2]
    cmp r0, #0
    mov r0, r1, lsl #16
    mov r9, r0, lsr #16
    ldr r5, [pc, #0x6f8]
    bne L_021ffb4c
    mov r0, r5
    bl native_fn_0221794c
    mov r7, r0
L_021ffb4c:
    ldr r11, [r5]
    ldr r10, [pc, #0x6d4]
    ldrsh r0, [r6, #24]
    ldr r10, [r10, r11, lsl #2]
    ldrb r1, [r6, #0x1a]
    add r3, sp, #156
    add r2, r6, #122
    str r10, [sp, #0x18]
    bl native_fn_0207b460
    ldrsh r1, [r6, #38]
    add r2, sp, #156
    mov r0, r9
    bl native_fn_0207b244
    ldrh r1, [r8, #2]
    str r0, [sp, #0x10]
    tst r1, #1
    beq L_021fffa0
    ldr r0, [pc, #0x688]
    ldrb r0, [r0, #0x5e8]
    cmp r0, #0
    beq L_021ffcb4
    mov r0, #0
    str r0, [sp, #0xc]
    bl native_fn_02062378
    mov r11, r0
    ldr r0, [pc, #0x668]
    mov r10, #0
    ldrb r0, [r0, #0x5e6]
    cmp r0, #0
    ble L_021ffc5c
L_021ffbc4:
    ldr r0, [pc, #0x654]
    add r0, r0, r10, lsl #2
    ldr r8, [r0, #0x5f8]
    ldrb r0, [r8, #0x33]
    cmp r0, #0
    bne L_021ffc48
    and r0, r10, #255
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r8
    bl native_fn_02210f74
    ldrsh r1, [r8, #36]
    add r2, r8, #122
    add r3, sp, #92
    cmp r1, r0
    movlt r0, #1
    strlt r0, [sp, #0xc]
    ldrsh r0, [r8, #24]
    ldrb r1, [r8, #0x1a]
    bl native_fn_0207b460
    mov r0, r8
    mov r1, r6
    mov r2, r9
    add r3, sp, #156
    bl native_fn_02215324
    mov r1, r0
    add r0, r8, #32
    add r2, sp, #92
    bl native_fn_0207c0d4
    cmp r11, #1
    bne L_021ffc48
    mov r0, #1
    bl native_fn_0206de44
L_021ffc48:
    ldr r0, [pc, #0x5d0]
    add r10, r10, #1
    ldrb r0, [r0, #0x5e6]
    cmp r10, r0
    blt L_021ffbc4
L_021ffc5c:
    ldr r0, [sp, #0xc]
    cmp r0, #0
    beq L_021ffc9c
    ldr r1, [sp, #0x10]
    add r2, sp, #156
    add r0, r6, #32
    rsb r1, r1, #0
    bl native_fn_0207c11c
    mov r7, #1
    ldr r2, [pc, #0x598]
    mov r3, #10
    sub r0, r7, #2
    mov r1, #154
    strb r3, [r2, #0x5e7]
    bl native_fn_0205f35c
    b L_021fff08
L_021ffc9c:
    mov r0, #84
    bl native_fn_021e7b9c
    ldr r0, [pc, #0x574]
    mov r1, #11
    strb r1, [r0, #0x5e7]
    b L_021fff08
L_021ffcb4:
    ldr r1, [r5]
    ldr r0, [pc, #0x570]
    ldrb r0, [r0, r1]
    cmp r0, #0
    beq L_021ffce0
    mov r0, #84
    bl native_fn_021e7b9c
    ldr r0, [pc, #0x548]
    mov r1, #6
    strb r1, [r0, #0x5e7]
    b L_021fff08
L_021ffce0:
    mov r0, r9
    bl native_fn_0207afec
    mov r10, r0
    ldrh r0, [r10, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #2
    bne L_021ffd7c
    ldr r0, [sp, #0x18]
    ldr r1, [sp, #0x18]
    ldr r2, [sp, #0x18]
    ldrsh r0, [r0, #24]
    ldrb r1, [r1, #0x1a]
    add r3, sp, #92
    add r2, r2, #122
    bl native_fn_0207b460
    ldr r0, [pc, #0x4f8]
    mov r1, #7
    strb r1, [r0, #0x5e7]
    ldrsh r0, [r6, #24]
    ldrb r1, [r6, #0x1a]
    add r3, sp, #156
    add r2, r6, #122
    bl native_fn_0207b460
    ldr r0, [sp, #0x18]
    mov r2, r9
    mov r1, r6
    add r3, sp, #156
    bl native_fn_02215324
    mov r1, r0
    ldr r0, [sp, #0x18]
    add r2, sp, #92
    add r0, r0, #32
    bl native_fn_0207c0d4
    mvn r0, #0
    mov r1, #154
    bl native_fn_0205f35c
    mov r7, #1
    b L_021ffed8
L_021ffd7c:
    mov r0, #100
    bl native_fn_0203d294
    ldrsh r1, [r10, #16]
    cmp r0, r1
    bge L_021ffec0
    ldr r0, [pc, #0x488]
    mov r1, #8
    strb r1, [r0, #0x5e7]
    ldr r0, [r5]
    and r0, r0, #255
    bl native_fn_02215d94
    str r0, [sp, #0x8]
    mov r1, r0
    ldr r0, [sp, #0x18]
    add r0, r0, #32
    bl native_fn_0207c2b8
    ldrsh r2, [r10, #18]
    ldr r1, [pc, #0x474]
    ldrsh r8, [r10, #24]
    mul r2, r0, r2
    smull r0, r7, r1, r2
    mov r0, r2, lsr #31
    add r7, r0, r7, asr #5
    mov r0, #10
    ldrsh r11, [r10, #26]
    bl native_fn_0203d294
    add r10, r0, #95
    ldrsh r0, [r6, #24]
    ldrb r1, [r6, #0x1a]
    add r2, r6, #122
    add r3, sp, #28
    bl native_fn_0207b460
    add r0, r6, #32
    add r1, sp, #28
    bl native_fn_0207c73c
    cmp r0, r8
    movle r2, #1
    ble L_021ffe58
    cmp r0, r11
    blt L_021ffe34
    mul r1, r7, r10
    ldr r3, [pc, #0x414]
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #5
    b L_021ffe58
L_021ffe34:
    sub r0, r0, r8
    mul r0, r7, r0
    sub r1, r11, r8
    bl native_fn_02026144
    mul r1, r10, r0
    ldr r3, [pc, #0x3ec]
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #5
L_021ffe58:
    add r0, sp, #28
    mov r1, r9
    bl native_fn_0207d198
    mov r8, r0
    ldr r0, [sp, #0x18]
    ldr r1, [sp, #0x8]
    add r0, r0, #32
    bl native_fn_0207c2b8
    cmp r8, r0
    movlt r1, r8
    movge r1, r0
    cmp r1, #1
    movlt r8, #1
    blt L_021ffe98
    cmp r8, r0
    movge r8, r0
L_021ffe98:
    ldr r0, [sp, #0x18]
    mov r7, #1
    strh r8, [r0, #36]
    ldr r2, [sp, #0x18]
    mov r3, #0
    sub r0, r7, #2
    mov r1, #154
    strb r3, [r2, #0x33]
    bl native_fn_0205f35c
    b L_021ffed8
L_021ffec0:
    ldr r1, [pc, #0x358]
    mov r2, #9
    mov r0, #84
    strb r2, [r1, #0x5e7]
    bl native_fn_021e7b9c
    mov r7, #1
L_021ffed8:
    cmp r7, #0
    beq L_021fff08
    ldr r1, [sp, #0x10]
    add r2, sp, #156
    add r0, r6, #32
    rsb r1, r1, #0
    bl native_fn_0207c11c
    bl native_fn_02062378
    cmp r0, #1
    bne L_021fff08
    mov r0, #1
    bl native_fn_0206de44
L_021fff08:
    ldr r1, [pc, #0x310]
    mov r0, #5
    ldrb r2, [r1, #0x5e7]
    mov r1, #6
    add r2, r2, #15
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_0205dc70
    bl native_fn_0205dc88
    cmp r0, #0
    beq L_021fff58
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b61c
    ldr r0, [pc, #0x2d8]
    mov r1, #5
    str r1, [r0, #0x4]
    mov r1, #6
    str r1, [r0]
    b L_021fffc0
L_021fff58:
    ldrsh r1, [r6, #38]
    ldr r0, [sp, #0x10]
    cmp r0, r1
    ble L_021fff74
    mov r0, #5
    bl native_fn_021ff5e4
    b L_021fffc0
L_021fff74:
    ldr r0, [pc, #0x2a4]
    ldr r0, [r0, #0x8]
    and r0, r0, #255
    bl native_fn_022014e8
    cmp r0, #0
    bne L_021fffc0
    mov r0, r6
    bl native_fn_0206dcd0
    mov r0, #5
    bl native_fn_021ff5e4
    b L_021fffc0
L_021fffa0:
    tst r1, #2
    beq L_021fffc0
    mov r0, r6
    bl native_fn_0206dcd0
    mov r0, #5
    bl native_fn_021ff5e4
    mov r0, #83
    bl native_fn_021e7b9c
L_021fffc0:
    cmp r7, #0
    beq L_022001f0
    ldr r0, [sp, #0x18]
    bl native_fn_0206dcd0
    b L_022001f0
    ldrb r0, [r2, #0x5e7]
    ldr r6, [r2, #0x1e8]
    ldr r3, [pc, #0x248]
    add r0, r0, #15
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #5
    mov r1, #6
    ldr r7, [r3, r6, lsl #2]
    bl native_fn_0205dc70
    mov r6, r5
    bl native_fn_0205dc88
    cmp r0, #0
    bne L_0220006c
    ldr r0, [pc, #0x20c]
    ldr r0, [r0, #0x8]
    and r0, r0, #255
    bl native_fn_022014e8
    cmp r0, #0
    ldreq r0, [pc, #0x1f8]
    ldreq r0, [r0, #0x4]
    cmpeq r0, #5
    bne L_0220003c
    mov r0, #5
    bl native_fn_021ff5e4
    mov r6, #1
L_0220003c:
    cmp r6, #0
    ldreq r0, [pc, #0x1d8]
    ldreq r1, [r0, #0x4]
    streq r1, [r0]
    add r0, r4, #16
    mov r1, #36
    bl native_fn_0204b5d4
    ldr r0, [pc, #0x1c0]
    mov r1, #9
    str r1, [r0, #0x4]
    mov r7, #1
    b L_022001f0
L_0220006c:
    mov r0, #7
    bl native_fn_022004c8
    ldr r0, [pc, #0x1a4]
    mov r1, #7
    str r1, [r0]
    ldrb r0, [r0, #0x5e7]
    cmp r0, #10
    addls pc, pc, r0, lsl #2
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000d8
    b L_022000bc
    b L_022000bc
    b L_022000bc
    b L_022000bc
L_022000bc:
    ldrsh r0, [r7, #24]
    mov r1, r5
    bl native_fn_02060954
    mov r0, r7
    mov r1, #16
    mov r2, #2
    bl native_fn_02047ff0
L_022000d8:
    mov r3, #1
    str r3, [sp]
    sub r1, r3, #2
    ldr r0, [pc, #0x134]
    str r1, [sp, #0x4]
    ldrb r2, [r0, #0x5e7]
    mov r0, #5
    mov r1, #6
    add r2, r2, #15
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_02217bdc
    mov r7, #1
    b L_022001f0
    ldrh r1, [r8, #2]
    ldr r0, [pc, #0x124]
    mov r8, r5
    tst r1, r0
    beq L_022001f0
    mov r0, #1
    bl native_fn_02217c9c
    ldr r0, [pc, #0xec]
    ldr r1, [r0, #0x4]
    cmp r1, #5
    bne L_022001c4
    ldr r1, [r0, #0x8]
    ldr r0, [r0, #0xf8]
    and r3, r1, #255
    ldr r2, [pc, #0xd4]
    and r1, r0, #255
    add r0, r2, r3, lsl #7
    ldr r1, [r0, r1, lsl #2]
    ldrsh r0, [r6, #24]
    mov r7, r1, lsl #16
    ldrb r1, [r6, #0x1a]
    add r3, sp, #156
    add r2, r6, #122
    mov r7, r7, lsr #16
    bl native_fn_0207b460
    ldrsh r1, [r6, #38]
    add r2, sp, #156
    mov r0, r7
    bl native_fn_0207b244
    ldrsh r1, [r6, #38]
    cmp r0, r1
    ble L_022001a0
    mov r0, #5
    bl native_fn_021ff5e4
    mov r8, #1
    b L_022001c4
L_022001a0:
    ldr r0, [pc, #0x78]
    ldr r0, [r0, #0x8]
    and r0, r0, #255
    bl native_fn_022014e8
    cmp r0, #0
    bne L_022001c4
    mov r0, #5
    bl native_fn_021ff5e4
    mov r8, #1
L_022001c4:
    cmp r8, #0
    ldreq r0, [pc, #0x50]
    ldreq r1, [r0, #0x4]
    streq r1, [r0]
    add r0, r4, #16
    mov r1, #36
    bl native_fn_0204b5d4
    ldr r0, [pc, #0x38]
    mov r1, #9
    str r1, [r0, #0x4]
    mov r7, #1
L_022001f0:
    cmp r7, #0
    beq L_02200204
    ldr r0, [pc, #0x20]
    ldr r0, [r0]
    bl native_fn_022008d8
L_02200204:
    cmp r5, #0
    beq L_02200214
    mov r0, r5
    bl native_fn_02201428
L_02200214:
    ldr r0, [sp, #0x14]
    add sp, sp, #220
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02237778
    dcd 0x02237a54
    dcd 0x02237780
    dcd 0x02237d70
    dcd 0x02237d63
    dcd 0x02237870
    dcd 0x02237960
    dcd 0x51eb851f
    dcd 0x00000ff7
}
