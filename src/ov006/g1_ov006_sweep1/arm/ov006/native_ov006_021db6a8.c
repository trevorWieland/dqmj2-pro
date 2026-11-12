/* ov006 row 0x021db6a8: 1020 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3ec -> native_data10_0220f3b8 (image word 0x0220f3b8)
 *   pool +0x3f0 -> native_data2_0220cdd8 (image word 0x0220cdd8)
 *   pool +0x3f4 -> native_data_0220cec0 (image word 0x0220cec0)
 *   pool +0x3f8 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x18 -> +0xc0
 *   branch +0x30 -> +0x48
 *   branch +0x54 -> +0x68
 *   branch +0x60 -> +0x80
 *   branch +0x64 -> +0x98
 *   branch +0x7c -> +0xac
 *   branch +0x94 -> +0xac
 *   branch +0xcc -> +0x134
 *   branch +0xdc -> +0x134
 *   branch +0xf4 -> +0x10c
 *   branch +0x140 -> +0x194
 *   branch +0x20c -> +0x224
 *   branch +0x214 -> +0x254
 *   branch +0x21c -> +0x270
 *   branch +0x220 -> +0x28c
 *   branch +0x234 -> +0x2d4
 *   branch +0x244 -> +0x2d4
 *   branch +0x250 -> +0x2d4
 *   branch +0x260 -> +0x2d4
 *   branch +0x26c -> +0x2d4
 *   branch +0x27c -> +0x2d4
 *   branch +0x288 -> +0x2d4
 *   branch +0x29c -> +0x2d4
 *   branch +0x2b8 -> +0x2d4
 *   branch +0x2c8 -> +0x2d4
 *   branch +0x330 -> +0x344
 *   branch +0x340 -> +0x37c
 *   branch +0x348 -> +0x35c
 *   branch +0x358 -> +0x37c
 *   branch +0x364 -> +0x374
 *   branch +0x370 -> +0x37c
 *   back edge +0x384 -> +0x1ac
 *   back edge +0x3cc -> +0x3a0
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x58 cmp r0, #1
 *   test +0x5c cmpne r0, #2
 *   test +0xc8 cmp r0, #1
 *   test +0xd8 cmp r0, #0
 *   test +0xf0 cmp r0, #0
 *   test +0x13c cmp r0, #1
 *   test +0x208 cmp r0, #0
 *   test +0x210 cmp r0, #1
 *   test +0x218 cmp r0, #2
 *   test +0x230 cmp r1, r0
 *   test +0x240 cmp r9, r0
 *   test +0x25c cmp r9, r0
 *   test +0x278 cmp r9, r0
 *   test +0x298 cmp r1, r0
 *   test +0x2b4 cmp r1, r0
 *   test +0x2c4 cmp r9, r0
 *   test +0x32c cmp r0, #0
 *   test +0x344 cmp r9, r0
 *   test +0x35c cmp r0, r9
 *   test +0x380 cmp r10, #10
 *   test +0x3c4 cmp r5, #10
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021db6a8; the literal pool and
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

extern void native_fn_021db5b4(void);
extern void native_fn_021d8328(void);
extern u8 native_data10_0220f3b8[];
extern void native_fn_021d77f8(void);
extern u8 native_data2_0220cdd8[];
extern void native_fn_021d7d28(void);
extern void native_fn_021d79e4(void);
extern void native_fn_020684e0(void);
extern u8 native_data_0220cec0[];
extern void native_fn_021d8414(void);
extern void native_fn_021d7ad0(void);
extern void native_fn_02046af4(void);
extern void native_fn_020679f0(void);
extern void native_fn_021d79d4(void);
extern void native_fn_021e2f38(void);
extern void native_fn_021dc750(void);
extern void native_fn_021d80e8(void);
extern void native_fn_021d7e34(void);
extern void native_fn_020643fc(void);
extern void native_fn_021d7ebc(void);


asm u32 native_ov006_021db6a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    bl native_fn_021db5b4
    mov r8, r0
    ldr r0, [r8]
    cmp r0, #0
    bne ov006_021db6a8_Lc0
    mov r0, #0
    bl native_fn_021d8328
    ldr r0, =native_data10_0220f3b8
    ldrsb r0, [r0]
    cmp r0, #0
    beq ov006_021db6a8_L48
    mov r0, #1
    bl native_fn_021d77f8
    ldr r0, =native_data2_0220cdd8
    mov r1, #1
    bl native_fn_021d7d28
ov006_021db6a8_L48:
    ldr r0, =native_data10_0220f3b8
    ldr r0, [r0, #0xc]
    cmp r0, #0
    beq ov006_021db6a8_L68
    cmp r0, #1
    cmpne r0, #2
    beq ov006_021db6a8_L80
    b ov006_021db6a8_L98
ov006_021db6a8_L68:
    mov r0, #0
    mov r1, #15
    mov r2, #4
    mov r3, #138
    bl native_fn_021d79e4
    b ov006_021db6a8_Lac
ov006_021db6a8_L80:
    mov r0, #0
    mov r1, #15
    mov r2, #4
    mov r3, #140
    bl native_fn_021d79e4
    b ov006_021db6a8_Lac
ov006_021db6a8_L98:
    mov r0, #0
    mov r1, #15
    mov r2, #4
    mov r3, #137
    bl native_fn_021d79e4
ov006_021db6a8_Lac:
    ldr r0, =native_data10_0220f3b8
    mov r1, #0
    strb r1, [r0]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov006_021db6a8_Lc0:
    ldr r0, =native_data10_0220f3b8
    ldr r0, [r0, #0xc]
    cmp r0, #1
    bne ov006_021db6a8_L134
    mov r0, #2
    bl native_fn_020684e0
    cmp r0, #0
    bne ov006_021db6a8_L134
    mov r0, #0
    bl native_fn_021d8328
    ldr r0, =native_data10_0220f3b8
    ldrsb r0, [r0]
    cmp r0, #0
    beq ov006_021db6a8_L10c
    mov r0, #1
    bl native_fn_021d77f8
    ldr r0, =native_data2_0220cdd8
    mov r1, #1
    bl native_fn_021d7d28
ov006_021db6a8_L10c:
    mov r0, #0
    mov r1, #15
    mov r2, #4
    mov r3, #140
    bl native_fn_021d79e4
    ldr r0, =native_data10_0220f3b8
    mov r1, #0
    strb r1, [r0]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov006_021db6a8_L134:
    ldr r0, =native_data10_0220f3b8
    ldrsb r0, [r0]
    cmp r0, #1
    beq ov006_021db6a8_L194
    mov r0, #0
    bl native_fn_021d77f8
    ldr r0, =native_data_0220cec0
    mov r1, #33
    bl native_fn_021d7d28
    mov r0, #0
    mov r1, #15
    mov r2, #2
    mov r3, #16
    bl native_fn_021d79e4
    mov r0, #1
    mov r1, #15
    mov r2, #2
    mov r3, #129
    bl native_fn_021d79e4
    mov r0, #2
    mov r1, #15
    mov r2, r0
    mov r3, #130
    bl native_fn_021d79e4
ov006_021db6a8_L194:
    ldr r4, =native_data10_0220f3b8
    mov r10, #0
    add r5, r8, #20
    add r7, sp, #8
    mov r6, #255
    mov r11, #36
ov006_021db6a8_L1ac:
    ldr r2, [r8, #0x4]
    ldr r0, [r4, #0x4]
    mov r1, r7
    add r0, r2, r0
    add r9, r10, r0
    mov r0, r9
    mov r2, #16
    mov r3, #6
    bl native_fn_021d8414
    add r0, r10, #13
    and r0, r0, #255
    mov r1, r7
    bl native_fn_021d7ad0
    str r7, [sp]
    str r6, [sp, #0x4]
    ldr r1, [r4, #0x4]
    ldr r0, =0x021c9698
    add r3, r10, r1
    mla r1, r3, r11, r5
    mov r2, #31
    mov r3, #0
    bl native_fn_02046af4
    ldr r0, [r4, #0xc]
    cmp r0, #0
    beq ov006_021db6a8_L224
    cmp r0, #1
    beq ov006_021db6a8_L254
    cmp r0, #2
    beq ov006_021db6a8_L270
    b ov006_021db6a8_L28c
ov006_021db6a8_L224:
    bl native_fn_020679f0
    ldr r0, [r0]
    ldr r1, [r4, #0x18]
    cmp r1, r0
    bne ov006_021db6a8_L2d4
    bl native_fn_020679f0
    ldr r0, [r0, #0x4]
    cmp r9, r0
    bne ov006_021db6a8_L2d4
    mov r0, #7
    bl native_fn_021d79d4
    b ov006_021db6a8_L2d4
ov006_021db6a8_L254:
    bl native_fn_020679f0
    ldr r0, [r0, #0x4]
    cmp r9, r0
    bne ov006_021db6a8_L2d4
    mov r0, #7
    bl native_fn_021d79d4
    b ov006_021db6a8_L2d4
ov006_021db6a8_L270:
    bl native_fn_021e2f38
    ldr r0, [r0]
    cmp r9, r0
    bne ov006_021db6a8_L2d4
    mov r0, #7
    bl native_fn_021d79d4
    b ov006_021db6a8_L2d4
ov006_021db6a8_L28c:
    bl native_fn_020679f0
    ldr r0, [r0]
    ldr r1, [r4, #0x18]
    cmp r1, r0
    bne ov006_021db6a8_L2d4
    bl native_fn_020679f0
    ldr r0, [r0, #0x34]
    bl native_fn_021dc750
    ldr r1, [r4, #0xc]
    sub r1, r1, #3
    cmp r1, r0
    bne ov006_021db6a8_L2d4
    bl native_fn_020679f0
    ldr r0, [r0, #0x38]
    cmp r9, r0
    bne ov006_021db6a8_L2d4
    mov r0, #7
    bl native_fn_021d79d4
ov006_021db6a8_L2d4:
    add r0, r10, #3
    and r0, r0, #255
    mov r1, r7
    bl native_fn_021d7ad0
    ldr r0, [r4, #0x4]
    mov r1, r7
    add r2, r10, r0
    mov r0, #36
    mla r0, r2, r0, r8
    ldrh r0, [r0, #12]
    mov r2, #16
    mov r3, #4
    bl native_fn_021d8414
    add r0, r10, #23
    and r0, r0, #255
    mov r1, r7
    bl native_fn_021d7ad0
    ldr r0, [r4, #0x4]
    add r1, r10, r0
    mov r0, #36
    mla r0, r1, r0, r8
    ldr r0, [r0, #0x10]
    cmp r0, #0
    bne ov006_021db6a8_L344
    mov r0, r10
    mov r1, #0
    bl native_fn_021d80e8
    b ov006_021db6a8_L37c
ov006_021db6a8_L344:
    cmp r9, r0
    bne ov006_021db6a8_L35c
    mov r0, r10
    mov r1, #1
    bl native_fn_021d80e8
    b ov006_021db6a8_L37c
ov006_021db6a8_L35c:
    cmp r0, r9
    mov r0, r10
    bls ov006_021db6a8_L374
    mov r1, #0
    bl native_fn_021d80e8
    b ov006_021db6a8_L37c
ov006_021db6a8_L374:
    mov r1, #2
    bl native_fn_021d80e8
ov006_021db6a8_L37c:
    add r10, r10, #1
    cmp r10, #10
    blt ov006_021db6a8_L1ac
    bl native_fn_021d7e34
    ldr r7, =native_data10_0220f3b8
    mov r5, #0
    mov r4, #3
    mov r9, #11
    mov r6, #36
ov006_021db6a8_L3a0:
    ldr r0, [r7, #0x4]
    add r1, r5, r0
    mla r0, r1, r6, r8
    ldrh r0, [r0, #14]
    bl native_fn_020643fc
    mov r1, r9
    mov r2, r4
    bl native_fn_021d7ebc
    add r5, r5, #1
    cmp r5, #10
    add r4, r4, #2
    blt ov006_021db6a8_L3a0
    mov r0, #0
    bl native_fn_021d8328
    ldr r0, =native_data10_0220f3b8
    mov r1, #1
    strb r1, [r0]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
