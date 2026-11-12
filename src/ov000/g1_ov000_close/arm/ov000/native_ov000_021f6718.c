/* ov000 row 0x021f6718: 1132 bytes.
 *
 * What it does: 280 instructions; 40 call(s) to 0x02061944, 0x02061c1c, 0x021f6ca0, +37 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x460 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   pool +0x464 -> native_data_0222b964 (image word 0x0222b964)
 *   pool +0x468 -> native_data_0222f308 (image word 0x0222f308)
 *   branch +0x11c -> +0x150
 *   branch +0x158 -> +0x19c
 *   branch +0x1ac -> +0x43c
 *   branch +0x20c -> +0x21c
 *   branch +0x2b0 -> +0x3d8
 *   branch +0x370 -> +0x39c
 *   branch +0x3d4 -> +0x414
 *   back edge +0x438 -> +0x1f8
 *   test +0xa0 cmp r0, #28
 *   test +0x118 cmp r0, #28
 *   test +0x154 cmp r0, #0
 *   test +0x1a8 cmp r0, #0
 *   test +0x208 cmp r0, #28
 *   test +0x2ac cmp r0, #1
 *   test +0x36c cmp r3, #100
 *   test +0x378 cmp r3, r11
 *   test +0x434 cmp r0, r1, asr #24
 *   0 block transfer(s), 58 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f6718; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_02061c1c(void);
extern void native_fn_021f6ca0(void);
extern void native_fn_02045ed0(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02067dd4(void);
extern void native_fn_02067d54(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02067e14(void);
extern void native_fn_01ffb50c(void);
extern void native_fn_021f6ce0(void);
extern u8 native_data_0222b964[];
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021f70a4(void);
extern void native_fn_02061dcc(void);
extern void native_fn_020602ec(void);
extern void native_fn_020630b0(void);
extern u8 native_data_0222f308[];
extern void native_fn_0204ab98(void);
extern void native_fn_0204a9d4(void);
extern void native_fn_0206e284(void);
extern void native_fn_0206e644(void);
extern void native_fn_02062554(void);


asm u32 native_ov000_021f6718 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #56
    bl native_fn_02061944
    mov r1, #2
    mov r4, r0
    mov r0, #3
    str r1, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    mov r5, #1
    mov r2, r0
    mov r1, #8
    mov r3, #16
    str r5, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r0, =0x02236ee4
    mov r1, #0
    str r1, [r0, #0x8]
    bl native_fn_021f6ca0
    mov r0, r5
    bl native_fn_02045ed0
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #6
    mov r1, #3
    mov r2, r0
    mov r3, #15
    bl native_fn_02061c1c
    add r1, sp, #52
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    strh r0, [sp, #52]
    add r0, r4, #512
    ldrsb r0, [r0, #105]
    add r1, sp, #52
    mov r2, #16
    cmp r0, #28
    movlt r0, r5
    movge r0, #2
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #6
    mov r3, #18
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #52]
    mov r5, #8
    add r0, r1, r0
    strh r0, [sp, #52]
    bl native_fn_02062aa0
    str r0, [sp, #0xc]
    bl native_fn_02067dd4
    bl native_fn_02067d54
    add r0, r0, #4
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #16
    mov r1, #18
    bl native_fn_0205dc70
    mov r1, #0
    bl native_fn_02048034
    add r0, r4, #512
    ldrsb r0, [r0, #105]
    cmp r0, #28
    blt ov000_021f6718_L150
    bl native_fn_02062ad0
    str r0, [sp, #0xc]
    bl native_fn_02067e14
    bl native_fn_02067d54
    add r0, r0, #4
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #16
    mov r1, #18
    bl native_fn_0205dc70
    mov r1, #0
    bl native_fn_02048034
ov000_021f6718_L150:
    ldr r0, [sp, #0xc]
    cmp r0, #0
    ble ov000_021f6718_L19c
    mov r0, #2
    str r0, [sp]
    mov r6, #0
    str r6, [sp, #0x4]
    mov r0, #13
    mov r1, #17
    mov r2, #6
    mov r3, #14
    str r6, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #13
    mov r1, #16
    mov r2, #18
    mov r3, #3
    str r6, [sp]
    bl native_fn_01ffb50c
ov000_021f6718_L19c:
    bl native_fn_021f6ce0
    ldr r0, [sp, #0xc]
    mov r10, #0
    cmp r0, #0
    ble ov000_021f6718_L43c
    ldr r0, =native_data_0222b964
    add r4, r4, #512
    ldrh r3, [r0, #2]
    ldrh r2, [r0, #4]
    ldrh r1, [r0, #6]
    ldrh r0, [r0, #8]
    strh r3, [sp, #36]
    strh r2, [sp, #38]
    strh r0, [sp, #34]
    ldrh r0, [sp, #36]
    strh r1, [sp, #32]
    str r0, [sp, #0x10]
    ldrh r0, [sp, #38]
    str r0, [sp, #0x14]
    ldrh r0, [sp, #32]
    str r0, [sp, #0x18]
    ldrh r0, [sp, #34]
    str r0, [sp, #0x1c]
ov000_021f6718_L1f8:
    mov r0, r10
    bl native_fn_02062a50
    mov r7, r0
    ldrsb r0, [r4, #105]
    cmp r0, #28
    blt ov000_021f6718_L21c
    mov r0, r10
    bl native_fn_02062a88
    mov r7, r0
ov000_021f6718_L21c:
    ldrsh r0, [r7, #24]
    bl native_fn_02044cdc
    mov r6, r0
    bl native_fn_021f70a4
    mov r1, #2
    add r0, r5, r0
    and r8, r0, #255
    str r1, [sp]
    mov r1, #0
    add r0, r10, #7
    str r1, [sp, #0x4]
    mov r0, r0, lsl #24
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    mov r1, #7
    mov r2, r8
    mov r3, #19
    bl native_fn_02061c1c
    add r0, r8, #2
    and r2, r0, #255
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r9, r10, #10
    str r0, [sp, #0x8]
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    mov r1, #7
    mov r3, #17
    bl native_fn_02061c1c
    ldrsb r0, [r4, #105]
    sub r0, r0, #27
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    bhi ov000_021f6718_L3d8
    add r8, r10, #7
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02061dcc
    mov r1, #0
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    ldrsh r1, [r7, #24]
    ldr r0, [r0]
    mov r2, r7
    mov r3, #0
    bl native_fn_020602ec
    mov r0, r8, lsl #24
    mov r8, r0, asr #24
    ldrb r0, [r7, #0x1c]
    bl native_fn_020630b0
    ldr r1, [sp, #0x10]
    mov r11, r0
    strh r1, [sp, #48]
    ldr r1, [sp, #0x14]
    mov r0, r8
    strh r1, [sp, #50]
    mov r1, #1
    str r1, [sp]
    str r1, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    add r1, sp, #48
    mov r2, #5
    mov r3, #1
    bl native_fn_0204aaf0
    ldrsh r2, [sp, #48]
    ldr r3, =native_data_0222f308
    mov r0, r8
    add r2, r2, #16
    strh r2, [sp, #48]
    mov r2, #0
    str r2, [sp]
    add r1, sp, #48
    mov r2, #1
    bl native_fn_0204ab98
    ldrsh r0, [sp, #48]
    add r0, r0, #8
    strh r0, [sp, #48]
    ldrb r3, [r7, #0x30]
    cmp r3, #100
    beq ov000_021f6718_L39c
    mov r1, #2
    cmp r3, r11
    movlt r2, #1
    str r1, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    movge r2, #5
    mov r0, r8
    add r1, sp, #48
    bl native_fn_0204a9d4
ov000_021f6718_L39c:
    ldr r1, [sp, #0x18]
    mov r0, r9, lsl #24
    strh r1, [sp, #44]
    ldr r1, [sp, #0x1c]
    mov r0, r0, asr #24
    strh r1, [sp, #46]
    ldrb r3, [r7, #0x32]
    add r1, sp, #44
    mov r2, #0
    str r3, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_0204aaf0
    b ov000_021f6718_L414
ov000_021f6718_L3d8:
    mov r2, #0
    add r1, sp, #40
    strh r2, [r1]
    strh r2, [r1, #2]
    mov r1, #16
    strh r1, [sp, #40]
    ldrb r3, [r7, #0x32]
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    str r3, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    add r1, sp, #40
    str r3, [sp, #0x8]
    bl native_fn_0204aaf0
ov000_021f6718_L414:
    add r0, r6, #1
    add r0, r0, r0, lsl #2
    add r0, r5, r0
    and r5, r0, #255
    add r0, r10, #1
    mov r1, r0, lsl #24
    ldr r0, [sp, #0xc]
    mov r10, r1, asr #24
    cmp r0, r1, asr #24
    bgt ov000_021f6718_L1f8
ov000_021f6718_L43c:
    bl native_fn_0206e284
    mov r0, #2
    bl native_fn_0206e644
    bl native_fn_02062554
    ldr r0, =0x02236ee4
    mov r1, #1
    str r1, [r0, #0xc]
    add sp, sp, #56
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
