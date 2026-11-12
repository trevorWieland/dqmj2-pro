/* ov000 row 0x0221e8c8: 792 bytes.
 *
 * What it does: 197 instructions; 17 call(s) to 0x0221e974, 0x020636e0, 0x0221c658, +14 more; loops (back edge at +0x68); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x314 -> constant 0x022463a0 (image word 0x022463a0)
 *   branch +0x30 -> +0xac
 *   back edge +0xa8 -> +0x44
 *   branch +0xdc -> +0xf8
 *   branch +0x16c -> +0x228
 *   back edge +0x224 -> +0x180
 *   test +0x24 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x80 cmp r9, #0
 *   test +0x9c cmp r8, r0, asr #24
 *   test +0xc8 cmp r9, #0
 *   test +0xe8 cmp r1, r8
 *   test +0x108 cmp r2, r8
 *   test +0x110 cmp r0, #6
 *   test +0x164 cmp r9, #0
 *   test +0x180 cmp r10, #0
 *   test +0x21c cmp r9, r0, asr #24
 *   2 block transfer(s), 36 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e8c8; the literal pool and
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

extern void native_fn_020636e0(void);
extern void native_fn_0221c658(void);
extern void native_fn_0221c758(void);
extern void native_fn_0221c8dc(void);
extern void native_fn_0206dbdc(void);
extern void native_fn_0221c938(void);
extern void native_fn_0221ef90(void);


asm u32 native_ov000_0221e8c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    and r2, r2, #255
    mov r8, r2
    str r0, [sp, #0x14]
    mov r0, r8
    str r2, [sp, #0x1c]
    mov r10, r1
    str r3, [sp, #0x18]
    cmp r0, #0
    ldr r9, [sp, #0x48]
    mov r6, #0
    ble ov000_0221e8c8_Lac
    ldr r4, =0x022463a0
    mov r7, r6
    mov r11, #1
    mov r5, r6
ov000_0221e8c8_L44:
    ldrb r2, [r10, r6, lsl #1]
    ldr r0, [r4, #0xc]
    add r1, r10, r6, lsl #1
    strb r2, [r0, r7]
    ldr r0, [r4, #0xc]
    ldrb r1, [r1, #0x1]
    add r0, r0, r7
    strb r1, [r0, #0x1]
    ldrb r0, [r10, r6, lsl #1]
    bl native_fn_020636e0
    cmp r0, #0
    ldr r0, [r4, #0xc]
    moveq r1, r11
    movne r1, #0
    add r0, r0, r7
    cmp r9, #0
    strb r1, [r0, #0x2]
    ldrne r0, [r4, #0xc]
    addne r0, r0, r7
    strneb r5, [r0, #0x3]
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    add r7, r7, #7
    mov r6, r0, asr #24
    bgt ov000_0221e8c8_L44
ov000_0221e8c8_Lac:
    ldr r0, [sp, #0x1c]
    ldr r1, =0x022463a0
    rsb r3, r0, r0, lsl #3
    ldr r0, [r1, #0xc]
    mov r2, #0
    strb r2, [r0, r3]
    ldr r0, [r1, #0xc]
    cmp r9, #0
    add r0, r0, r3
    strb r2, [r0, #0x1]
    ldr r0, [sp, #0x1c]
    strb r0, [r1]
    beq ov000_0221e8c8_Lf8
    ldr r0, [sp, #0x18]
    add r1, r0, #3
    cmp r1, r8
    ldr r0, =0x022463a0
    movge r1, r8
    strb r1, [r0, #0x2]
ov000_0221e8c8_Lf8:
    ldr r0, [sp, #0x18]
    ldr r1, =0x022463a0
    add r2, r0, #3
    ldr r0, [sp, #0x1c]
    cmp r2, r8
    movge r2, r8
    cmp r0, #6
    movhi r8, #6
    and r9, r8, #255
    strb r2, [r1, #0x1]
    bl native_fn_0221c658
    mov r1, r9, lsl #1
    mov r2, #5
    add r1, r1, #2
    str r2, [sp]
    mov r2, #30
    str r2, [sp, #0x4]
    and r1, r1, #255
    str r1, [sp, #0x8]
    mov r3, #1
    str r3, [sp, #0xc]
    mov r1, #0
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #7
    mov r2, #12
    bl native_fn_0221c758
    cmp r9, #0
    mov r10, #0
    ble ov000_0221e8c8_L228
    mov r8, #6
    mov r5, #17
    mov r4, #2
    mov r11, r10
ov000_0221e8c8_L180:
    cmp r10, #0
    moveq r6, #5
    moveq r7, #6
    movne r6, #7
    movne r7, #8
    bl native_fn_0221c658
    and r1, r8, #255
    stmia sp, {r1, r5}
    str r4, [sp, #0x8]
    str r11, [sp, #0xc]
    mov r1, #1
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    add r0, r10, #10
    mov r0, r0, lsl #24
    mov r2, r6
    mov r0, r0, asr #24
    mov r3, r4
    bl native_fn_0221c758
    bl native_fn_0221c658
    and r1, r8, #255
    str r1, [sp]
    mov r1, #11
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    add r0, r10, #20
    mov r0, r0, lsl #24
    mov r2, r7
    mov r0, r0, asr #24
    mov r3, #19
    bl native_fn_0221c758
    add r0, r10, #1
    mov r0, r0, lsl #24
    add r8, r8, #2
    cmp r9, r0, asr #24
    mov r10, r0, asr #24
    bgt ov000_0221e8c8_L180
ov000_0221e8c8_L228:
    ldr r1, [sp, #0x1c]
    mov r3, #5
    str r3, [sp]
    mov r4, #7
    ldr r0, [sp, #0x14]
    mov r2, r9
    mov r3, #10
    str r4, [sp, #0x4]
    bl native_fn_0221c8dc
    mov r0, #9
    mov r1, #0
    mov r2, #11
    bl native_fn_0206dbdc
    mov r4, r0
    add r0, r4, #7
    mov r0, r0, asr #3
    add r0, r0, #4
    and r5, r0, #255
    bl native_fn_0221c658
    mov r1, #4
    stmia sp, {r1, r5}
    mov r2, #2
    rsb r3, r5, #31
    str r2, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #8
    and r3, r3, #255
    bl native_fn_0221c758
    rsb r0, r4, r5, lsl #3
    add r0, r0, r0, lsr #31
    mov r0, r0, asr #1
    and r0, r0, #255
    str r0, [sp]
    mov r0, #8
    mov r1, #9
    mov r2, #0
    mov r3, #11
    bl native_fn_0221c938
    bl native_fn_0221c658
    mov r1, r0
    mov r0, #21
    str r0, [sp]
    mov r0, #28
    str r0, [sp, #0x4]
    mov r2, #2
    str r2, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
    ldrsb r1, [r1, #16]
    mov r3, r2
    bl native_fn_0221c758
    ldr r0, [sp, #0x14]
    bl native_fn_0221ef90
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
