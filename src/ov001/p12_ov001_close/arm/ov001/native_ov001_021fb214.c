/* ov001 row 0x021fb214: 1352 bytes.
 *
 * What it does: 329 instructions; 29 call(s) to 0x02008d78, 0x021fb1dc, 0x02044fcc, +26 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 9 literal slot(s) in the extent
 *
 * Decoded shape: loop with 29 calls (329 instructions, 29 calls, 27 branches, 26 back edges, 9 literal slots).
 *
 *   pool +0x524 -> constant 0x02239abc (image word 0x02239abc)
 *   pool +0x528 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x52c -> constant 0x02239b29 (image word 0x02239b29)
 *   pool +0x530 -> constant 0x02239adc (image word 0x02239adc)
 *   pool +0x534 -> constant 0x02239add (image word 0x02239add)
 *   pool +0x538 -> native_data_0222e040 (image word 0x0222e040)
 *   pool +0x53c -> constant 0x000003e7 (image word 0x000003e7)
 *   pool +0x540 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x544 -> constant 0x02239ae6 (image word 0x02239ae6)
 *   branch +0x20 -> +0x518
 *   branch +0x4c -> +0x70
 *   branch +0x6c -> +0x80
 *   branch +0xe8 -> +0xf8
 *   branch +0xfc -> +0x10c
 *   branch +0x1a4 -> +0x1bc
 *   branch +0x1e0 -> +0x22c
 *   branch +0x228 -> +0x23c
 *   branch +0x240 -> +0x3b8
 *   branch +0x2e4 -> +0x320
 *   branch +0x2f8 -> +0x330
 *   back edge +0x32c -> +0x2d0
 *   branch +0x344 -> +0x408
 *   branch +0x394 -> +0x3a4
 *   back edge +0x3b0 -> +0x358
 *   branch +0x3b4 -> +0x408
 *   branch +0x3ec -> +0x408
 *   back edge +0x404 -> +0x3e0
 *   branch +0x40c -> +0x4a0
 *   branch +0x418 -> +0x42c
 *   branch +0x428 -> +0x4b0
 *   branch +0x430 -> +0x444
 *   branch +0x440 -> +0x4b0
 *   branch +0x448 -> +0x45c
 *   branch +0x458 -> +0x4b0
 *   branch +0x468 -> +0x47c
 *   branch +0x478 -> +0x4b0
 *   branch +0x47c -> +0x490
 *   branch +0x48c -> +0x4b0
 *   branch +0x49c -> +0x4b0
 *   branch +0x4b4 -> +0x4cc
 *   branch +0x4d8 -> +0x4e8
 *   branch +0x4f8 -> +0x508
 *   test +0x1c cmp r10, #0
 *   test +0x48 cmp r0, #0
 *   test +0xd4 cmp r7, #0
 *   test +0xf8 cmp r7, #0
 *   test +0x194 cmp r7, #0
 *   test +0x1dc cmp r7, #0
 *   test +0x23c cmp r7, #0
 *   test +0x2e0 cmp r8, #0
 *   test +0x2f4 cmp r0, r1
 *   test +0x324 cmp r6, #4
 *   test +0x340 cmp r0, #1
 *   test +0x388 cmp r1, r8
 *   test +0x390 cmp r0, #0
 *   test +0x3ac cmp r9, r0
 *   test +0x3e8 cmp r0, #0
 *   test +0x3f8 cmp r2, #5
 *   test +0x408 cmp r7, #0
 *   test +0x414 cmp r0, #1
 *   test +0x42c cmp r0, #2
 *   test +0x444 cmp r0, #3
 *   test +0x464 cmp r0, #8
 *   test +0x4b0 cmp r7, #0
 *   test +0x4cc cmp r7, #0
 *   test +0x4ec cmp r7, #0
 *   0 block transfer(s), 43 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fb214; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_021fb1dc(void);
extern void native_fn_02044fcc(void);
extern void native_fn_0203d294(void);
extern void native_fn_02063c00(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02044f9c(void);
extern void native_fn_0207c8a4(void);
extern void native_fn_0207c9b8(void);
extern void native_fn_0207c8fc(void);
extern void native_fn_020449d4(void);
extern u8 native_data_0222e040[];
extern void native_fn_02064998(void);
extern void native_fn_021d9124(void);
extern void native_fn_021d924c(void);
extern void native_fn_021d9214(void);
extern void native_fn_021d8d1c(void);
extern void native_fn_020655f8(void);


asm u32 native_ov001_021fb214 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r10, r0
    ldr r0, =0x02239abc
    mov r1, #0
    mov r2, #132
    bl native_fn_02008d78
    cmp r10, #0
    beq ov001_021fb214_L518
    bl native_fn_021fb1dc
    ldr r1, =0x02239abc
    mov r2, #1
    strb r2, [r1, #0x67]
    ldr r1, [r10, #0x1e8]
    mov r7, r0
    ldrsh r0, [r1, #42]
    ldrb r1, [r1, #0x2c]
    bl native_fn_02044fcc
    cmp r0, #0
    bne ov001_021fb214_L70
    ldr r1, [r10, #0x1e8]
    ldr r0, =0x02239abc
    ldrsh r1, [r1, #42]
    strh r1, [r0, #100]
    ldr r1, [r10, #0x1e8]
    ldrb r1, [r1, #0x2c]
    strb r1, [r0, #0x66]
    b ov001_021fb214_L80
ov001_021fb214_L70:
    ldr r1, =0x02239abc
    mov r2, r0, lsr #16
    strh r0, [r1, #100]
    strb r2, [r1, #0x66]
ov001_021fb214_L80:
    ldrb r2, [r10, #0x31f]
    ldr r0, =0x02239abc
    add r1, r10, #256
    strb r2, [r0, #0x69]
    ldr r0, [r10, #0x1e8]
    ldrsh r12, [r1, #236]
    ldrsh r11, [r0, #50]
    ldrsh r9, [r1, #238]
    ldrsh r8, [r0, #52]
    add r11, r12, r11
    str r11, [sp]
    ldrsh r6, [r1, #244]
    ldrsh r4, [r0, #54]
    ldrsh r5, [r1, #246]
    ldrsh r3, [r0, #56]
    ldrsh r2, [r1, #248]
    ldrsh lr, [r0, #58]
    add r4, r6, r4
    ldrsh r1, [r1, #250]
    ldrsh r0, [r0, #60]
    add r11, r9, r8
    cmp r7, #0
    add r5, r5, r3
    add r6, r2, lr
    add r8, r1, r0
    movne r9, #100
    bne ov001_021fb214_Lf8
    mov r0, #20
    bl native_fn_0203d294
    add r9, r0, #90
ov001_021fb214_Lf8:
    cmp r7, #0
    beq ov001_021fb214_L10c
    mov r0, #10
    mov r1, #1
    bl native_fn_02063c00
ov001_021fb214_L10c:
    ldr r0, [sp]
    mul r2, r11, r9
    mul r3, r0, r9
    mul r1, r4, r9
    mul r0, r5, r9
    mul r4, r8, r9
    ldr r11, =0x51eb851f
    mul r5, r6, r9
    mov r8, r3, lsr #31
    smull r3, r6, r11, r3
    add r6, r8, r6, asr #5
    ldr r3, =0x02239abc
    mov r8, r2, lsr #31
    smull r9, r2, r11, r2
    strh r6, [r3]
    add r2, r8, r2, asr #5
    mov r6, r1, lsr #31
    smull r8, r1, r11, r1
    strh r2, [r3, #2]
    add r1, r6, r1, asr #5
    mov r2, r0, lsr #31
    smull r0, r6, r11, r0
    strh r1, [r3, #8]
    mov r0, r5, lsr #31
    smull r1, r5, r11, r5
    add r6, r2, r6, asr #5
    add r5, r0, r5, asr #5
    strh r6, [r3, #10]
    mov r0, r4, lsr #31
    smull r1, r2, r11, r4
    strh r5, [r3, #12]
    add r2, r0, r2, asr #5
    strh r2, [r3, #14]
    ldrsh r0, [r3]
    cmp r7, #0
    strh r0, [r3, #4]
    ldrsh r0, [r3, #2]
    strh r0, [r3, #6]
    beq ov001_021fb214_L1bc
    ldr r0, [r10, #0x1e8]
    ldr r1, =0x02239b29
    add r0, r0, #178
    mov r2, #20
    bl native_fn_02008e0c
ov001_021fb214_L1bc:
    ldr r1, =0x02239abc
    ldrsh r0, [r1, #100]
    ldrb r1, [r1, #0x66]
    bl native_fn_02044f9c
    ldrb r2, [r10, #0x1fc]
    ldr r1, =0x02239abc
    mov r4, r0
    strb r2, [r1, #0x10]
    cmp r7, #0
    bne ov001_021fb214_L22c
    mov r1, r4
    mov r0, #1
    bl native_fn_0207c8a4
    ldr r1, =0x02239abc
    mov r0, r4
    ldrb r1, [r1, #0x10]
    bl native_fn_0207c9b8
    ldr r1, =0x02239abc
    str r0, [r1, #0x14]
    ldrb r1, [r1, #0x10]
    mov r0, r4
    add r1, r1, #1
    bl native_fn_0207c9b8
    ldr r1, =0x02239abc
    str r0, [r1, #0x18]
    mov r0, #1
    bl native_fn_0207c8fc
    b ov001_021fb214_L23c
ov001_021fb214_L22c:
    ldr r0, [r10, #0x200]
    str r0, [r1, #0x14]
    ldr r0, [r10, #0x204]
    str r0, [r1, #0x18]
ov001_021fb214_L23c:
    cmp r7, #0
    bne ov001_021fb214_L3b8
    ldr r0, =0x02239abc
    ldrsh r0, [r0, #100]
    bl native_fn_020449d4
    ldr r1, =0x02239abc
    ldrb r4, [r0, #0x5f]
    ldrb r3, [r1, #0x68]
    ldr r0, =0x02239adc
    ldr r2, =0x02239add
    strb r4, [r0, r3, lsl #1]
    ldrb r3, [r1, #0x68]
    mov r4, #0
    ldr r0, =native_data_0222e040
    strb r4, [r2, r3, lsl #1]
    ldrb r2, [r1, #0x68]
    add r2, r2, #1
    strb r2, [r1, #0x68]
    ldrb r2, [r0]
    ldrb r1, [r0, #0x1]
    strb r2, [sp, #0x4]
    strb r1, [sp, #0x5]
    ldrb r1, [r0, #0x2]
    ldrb r0, [r0, #0x3]
    strb r1, [sp, #0x6]
    strb r0, [sp, #0x7]
    ldrb r0, [r10, #0x31f]
    bl native_fn_02064998
    mov r1, r0
    mov r0, #1
    sub r2, r0, #2
    mov r3, r2
    bl native_fn_021d9124
    ldr r5, =0x02239abc
    add r9, sp, #4
    mov r6, r4
    mov r11, r4
ov001_021fb214_L2d0:
    mov r0, r11
    bl native_fn_021d924c
    add r0, r0, r6
    ldrb r8, [r0, #0x51]
    cmp r8, #0
    beq ov001_021fb214_L320
    mov r0, #100
    bl native_fn_0203d294
    ldrb r1, [r9]
    cmp r0, r1
    bge ov001_021fb214_L330
    ldrb r0, [r5, #0x68]
    add r0, r5, r0, lsl #1
    strb r8, [r0, #0x20]
    ldrb r0, [r5, #0x68]
    add r0, r5, r0, lsl #1
    strb r4, [r0, #0x21]
    ldrb r0, [r5, #0x68]
    add r0, r0, #1
    strb r0, [r5, #0x68]
ov001_021fb214_L320:
    add r6, r6, #1
    cmp r6, #4
    add r9, r9, #1
    blt ov001_021fb214_L2d0
ov001_021fb214_L330:
    bl native_fn_021d9214
    ldr r5, =0x02239abc
    mov r9, #1
    ldrb r0, [r5, #0x10]
    cmp r0, #1
    blt ov001_021fb214_L408
    ldr r8, =0x000003e7
    ldr r4, =0x66666667
    mov r6, #19
    mov r11, r9
ov001_021fb214_L358:
    mov r0, r9
    bl native_fn_021d8d1c
    ldrb r1, [r5, #0x68]
    ldrsh r3, [r5, #28]
    mul r0, r1, r0
    add r0, r0, #4
    mov r1, r0, lsr #31
    smull r2, r0, r4, r0
    add r0, r1, r0, asr #1
    add r1, r3, r0
    strh r1, [r5, #28]
    ldrsh r1, [r5, #28]
    cmp r1, r8
    strgth r8, [r5, #28]
    cmp r0, #0
    ble ov001_021fb214_L3a4
    mov r0, r6
    mov r1, r11
    bl native_fn_02063c00
ov001_021fb214_L3a4:
    ldrb r0, [r5, #0x10]
    add r9, r9, #1
    cmp r9, r0
    ble ov001_021fb214_L358
    b ov001_021fb214_L408
ov001_021fb214_L3b8:
    ldr r0, [r10, #0x1e8]
    ldr r1, =0x02239adc
    add r0, r0, #210
    mov r2, #10
    bl native_fn_02008e0c
    add r0, r10, #512
    ldrsh r0, [r0, #8]
    ldr r1, =0x02239abc
    mov r2, #0
    strh r0, [r1, #28]
ov001_021fb214_L3e0:
    add r0, r1, r2, lsl #1
    ldrb r0, [r0, #0x20]
    cmp r0, #0
    beq ov001_021fb214_L408
    ldrb r0, [r1, #0x68]
    add r2, r2, #1
    cmp r2, #5
    add r0, r0, #1
    strb r0, [r1, #0x68]
    blt ov001_021fb214_L3e0
ov001_021fb214_L408:
    cmp r7, #0
    bne ov001_021fb214_L4a0
    bl native_fn_020655f8
    cmp r0, #1
    bne ov001_021fb214_L42c
    ldr r0, =0x02239abc
    mov r1, #0
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L42c:
    cmp r0, #2
    bne ov001_021fb214_L444
    ldr r0, =0x02239abc
    mov r1, #1
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L444:
    cmp r0, #3
    bne ov001_021fb214_L45c
    ldr r0, =0x02239abc
    mov r1, #2
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L45c:
    mov r0, #17
    bl native_fn_0203d294
    cmp r0, #8
    bge ov001_021fb214_L47c
    ldr r0, =0x02239abc
    mov r1, #0
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L47c:
    ble ov001_021fb214_L490
    ldr r0, =0x02239abc
    mov r1, #1
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L490:
    ldr r0, =0x02239abc
    mov r1, #2
    strb r1, [r0, #0x6a]
    b ov001_021fb214_L4b0
ov001_021fb214_L4a0:
    ldr r1, [r10, #0x1e8]
    ldr r0, =0x02239abc
    ldrb r1, [r1, #0xad]
    strb r1, [r0, #0x6a]
ov001_021fb214_L4b0:
    cmp r7, #0
    beq ov001_021fb214_L4cc
    ldr r0, [r10, #0x1e8]
    ldr r1, =0x02239ae6
    add r0, r0, #220
    mov r2, #58
    bl native_fn_02008e0c
ov001_021fb214_L4cc:
    cmp r7, #0
    ldreq r0, =0x02239abc
    moveq r1, #0
    beq ov001_021fb214_L4e8
    ldr r1, [r10, #0x1e8]
    ldr r0, =0x02239abc
    ldrb r1, [r1, #0xae]
ov001_021fb214_L4e8:
    strb r1, [r0, #0x6b]
    cmp r7, #0
    ldreq r0, =0x02239abc
    moveq r1, #0
    beq ov001_021fb214_L508
    ldr r1, [r10, #0x1e8]
    ldr r0, =0x02239abc
    ldrb r1, [r1, #0xab]
ov001_021fb214_L508:
    strb r1, [r0, #0x6c]
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021fb214_L518:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
