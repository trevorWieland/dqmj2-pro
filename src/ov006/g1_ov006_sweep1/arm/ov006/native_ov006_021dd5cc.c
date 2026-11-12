/* ov006 row 0x021dd5cc: 1092 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x42c -> constant 0x02044a14 (image word 0x02044a14)
 *   pool +0x430 -> constant 0x02044a58 (image word 0x02044a58)
 *   pool +0x434 -> constant 0x02044a9c (image word 0x02044a9c)
 *   pool +0x438 -> constant 0x02044ae0 (image word 0x02044ae0)
 *   pool +0x43c -> constant 0x02044b24 (image word 0x02044b24)
 *   pool +0x440 -> constant 0x02044b68 (image word 0x02044b68)
 *   branch +0x2f0 -> +0x308
 *   branch +0x39c -> +0x3ec
 *   back edge +0x3e8 -> +0x3ac
 *   branch +0x3fc -> +0x408
 *   test +0x2d8 cmp r10, #75
 *   test +0x2f4 cmp r10, #50
 *   test +0x34c cmp r0, #0
 *   test +0x358 cmp r0, #0
 *   test +0x364 cmp r0, #0
 *   test +0x370 cmp r0, #0
 *   test +0x37c cmp r0, #0
 *   test +0x394 cmp r7, #0
 *   test +0x3e4 cmp r10, r7
 *   test +0x3f4 cmp r0, #8
 *   0 block transfer(s), 53 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dd5cc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020642f8(void);
extern void native_fn_021d83c8(void);
extern void native_fn_0206271c(void);
extern void native_fn_021da654(void);
extern void native_fn_02062a10(void);
extern void native_fn_021dd4c0(void);
extern void native_fn_02044e34(void);
extern void native_fn_02044e44(void);
extern void native_fn_021dd4f0(void);
extern void native_fn_02044e70(void);
extern void native_fn_02044e80(void);
extern void native_fn_02044eac(void);
extern void native_fn_02044ebc(void);
extern void native_fn_02044ee8(void);
extern void native_fn_02044ef8(void);
extern void native_fn_02044f24(void);
extern void native_fn_02044f34(void);
extern void native_fn_02044f60(void);
extern void native_fn_02044f70(void);
extern void native_fn_021dd4d8(void);
extern void native_fn_021dd3c0(void);
extern void native_fn_021dd420(void);
extern void native_fn_021dd3a8(void);
extern void native_fn_021dd434(void);
extern void native_fn_02008d78(void);
extern void native_fn_021dd57c(void);
extern void native_fn_02062e44(void);
extern void native_fn_0203d294(void);
extern void native_fn_02063038(void);
extern void native_fn_021ddf58(void);
extern void native_fn_021d83e4(void);


asm u32 native_ov006_021dd5cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #44
    str r0, [sp, #0xc]
    bl native_fn_020642f8
    mov r5, r0
    mov r7, #0
    bl native_fn_021d83c8
    ldrb r8, [r5, #0x6]
    ldrsh r9, [r5, #2]
    ldrb r10, [r5, #0x5]
    mov r1, r8
    mov r0, r9
    bl native_fn_0206271c
    mov r6, r0
    bl native_fn_021da654
    mov r0, r6
    bl native_fn_02062a10
    mov r4, r0
    mov r0, #1
    bl native_fn_021dd4c0
    mov r11, r0
    mov r0, r9
    mov r1, r8
    strb r10, [r4, #0x30]
    bl native_fn_02044e34
    mov r2, r7
    str r0, [sp, #0x10]
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044e44
    ldr r1, [sp, #0x10]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044a14
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #32]
    mov r0, r9
    mov r1, r8
    bl native_fn_02044e70
    mov r2, r7
    str r0, [sp, #0x14]
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044e80
    ldr r1, [sp, #0x14]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044a58
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #34]
    mov r0, r9
    mov r1, r8
    bl native_fn_02044eac
    mov r2, r7
    str r0, [sp, #0x18]
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044ebc
    ldr r1, [sp, #0x18]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044a9c
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #40]
    mov r0, r9
    mov r1, r8
    bl native_fn_02044ee8
    mov r2, r7
    str r0, [sp, #0x1c]
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044ef8
    ldr r1, [sp, #0x1c]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044ae0
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #42]
    mov r0, r9
    mov r1, r8
    bl native_fn_02044f24
    mov r2, r7
    str r0, [sp, #0x20]
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044f34
    ldr r1, [sp, #0x20]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044b24
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #44]
    mov r0, r9
    mov r1, r8
    bl native_fn_02044f60
    str r0, [sp, #0x24]
    mov r2, r7
    str r2, [sp]
    mov r0, r9
    mov r1, r8
    mov r3, r2
    str r2, [sp, #0x4]
    bl native_fn_02044f70
    ldr r1, [sp, #0x24]
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r1, r1, asr #16
    str r1, [sp]
    mov r0, r0, asr #16
    str r0, [sp, #0x4]
    ldr r1, =0x02044b68
    mov r0, r11
    str r1, [sp, #0x8]
    mov r1, r9
    mov r2, r8
    mov r3, r10
    bl native_fn_021dd4f0
    strh r0, [r4, #46]
    mov r0, r11
    mov r1, #1
    bl native_fn_021dd4d8
    ldrsh r0, [r4, #32]
    cmp r10, #75
    strh r0, [r4, #36]
    ldrsh r0, [r4, #34]
    strh r0, [r4, #38]
    movhi r0, #10
    strhib r0, [r4, #0x1c]
    bhi ov006_021dd5cc_L308
    cmp r10, #50
    movhi r0, #4
    strhib r0, [r4, #0x1c]
    movls r0, r7
    strlsb r0, [r4, #0x1c]
ov006_021dd5cc_L308:
    mov r0, r9
    mov r1, r8
    mov r2, #1
    bl native_fn_021dd3c0
    mov r8, r0
    mov r1, r10
    bl native_fn_021dd420
    str r0, [r4, #0x34]
    mov r0, r8
    add r1, r10, #1
    bl native_fn_021dd420
    str r0, [r4, #0x38]
    mov r0, r8
    mov r1, #1
    bl native_fn_021dd3a8
    ldrb r0, [r5, #0x7]
    mov r2, #1
    cmp r0, #0
    ldrb r0, [r5, #0x8]
    addne r7, r7, #1
    cmp r0, #0
    ldrb r0, [r5, #0x9]
    addne r7, r7, #1
    cmp r0, #0
    ldrb r0, [r5, #0xa]
    addne r7, r7, #1
    cmp r0, #0
    ldrb r0, [r5, #0xb]
    addne r7, r7, #1
    cmp r0, #0
    addne r7, r7, #1
    mov r0, r10
    mov r1, r7
    bl native_fn_021dd434
    strh r0, [r4, #60]
    cmp r7, #0
    mov r10, #0
    ble ov006_021dd5cc_L3ec
    add r9, sp, #40
    mov r8, r10
    mov r4, #2
ov006_021dd5cc_L3ac:
    mov r0, r9
    mov r1, r8
    mov r2, r4
    bl native_fn_02008d78
    mov r0, r5
    mov r1, r10
    bl native_fn_021dd57c
    strb r0, [sp, #0x28]
    mov r0, r6
    mov r1, r10, lsl #24
    mov r1, r1, asr #24
    mov r2, r9
    bl native_fn_02062e44
    add r10, r10, #1
    cmp r10, r7
    blt ov006_021dd5cc_L3ac
ov006_021dd5cc_L3ec:
    mov r0, #17
    bl native_fn_0203d294
    cmp r0, #8
    movlt r1, #0
    blt ov006_021dd5cc_L408
    movgt r1, #1
    movle r1, #2
ov006_021dd5cc_L408:
    mov r0, r6
    and r1, r1, #255
    bl native_fn_02063038
    ldr r0, [sp, #0xc]
    mov r1, r6
    bl native_fn_021ddf58
    bl native_fn_021d83e4
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
