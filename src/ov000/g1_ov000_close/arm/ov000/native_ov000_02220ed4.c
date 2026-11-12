/* ov000 row 0x02220ed4: 580 bytes.
 *
 * What it does: 141 instructions; 24 call(s) to 0x0221c658, 0x02220afc, 0x02049ad0, +21 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x234 -> constant 0x02246424 (image word 0x02246424)
 *   pool +0x238 -> constant 0x022463dc (image word 0x022463dc)
 *   pool +0x23c -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x240 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x7c -> +0x198
 *   branch +0x8c -> +0x114
 *   branch +0x9c -> +0xb4
 *   branch +0xb0 -> +0xb8
 *   branch +0x110 -> +0x218
 *   branch +0x194 -> +0x218
 *   back edge +0x228 -> +0x3c
 *   test +0x1c cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x78 cmpne r0, #0
 *   test +0x88 cmp r7, #0
 *   test +0x98 cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0x224 cmp r10, #3
 *   3 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220ed4; the literal pool and
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
extern void native_fn_02220afc(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02008d78(void);
extern void native_fn_02220714(void);
extern void native_fn_02220778(void);
extern void native_fn_020603ec(void);
extern void native_fn_020449d4(void);
extern void native_fn_0221f5fc(void);
extern void native_fn_02049ffc(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02085270(void);
extern void native_fn_02087a48(void);
extern void native_fn_02086b14(void);


asm u32 native_ov000_02220ed4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #108
    str r0, [sp, #0x8]
    bl native_fn_0221c658
    bl native_fn_02220afc
    ldr r0, [sp, #0x8]
    ldr r9, =0x02246424
    cmp r0, #0
    movne r0, #13
    moveq r0, #12
    mov r0, r0, lsl #24
    ldr r11, =0x022463dc
    mov r8, r0, asr #24
    mov r10, #0
    add r4, sp, #76
ov000_02220ed4_L3c:
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r5, r0
    ldr r1, [r5]
    add r0, sp, #12
    ldr r6, [r1, #0x4]
    mov r1, #0
    mov r2, #64
    bl native_fn_02008d78
    ldr r0, =0x022463b0
    ldr r1, [r0, #0x1c]
    ldrsh r0, [r1, #24]
    cmp r0, #0
    ldrnesh r0, [r1, #156]
    cmpne r0, #0
    beq ov000_02220ed4_L198
    mov r0, r10, lsl #1
    ldrsh r7, [r11, r0]
    cmp r7, #0
    beq ov000_02220ed4_L114
    ldr r0, [sp, #0x8]
    bl native_fn_02220714
    cmp r0, #0
    beq ov000_02220ed4_Lb4
    mov r0, r7
    bl native_fn_02220778
    cmp r0, #0
    movne r5, #1
    bne ov000_02220ed4_Lb8
ov000_02220ed4_Lb4:
    mov r5, #3
ov000_02220ed4_Lb8:
    mov r0, #0
    str r0, [sp]
    mov r1, r10, lsl #1
    ldrsh r1, [r11, r1]
    ldrb r2, [r9]
    add r0, sp, #12
    mov r3, #15
    bl native_fn_020603ec
    mov r0, r10, lsl #1
    ldrsh r0, [r11, r0]
    bl native_fn_020449d4
    mov r1, #0
    stmia sp, {r1, r5}
    ldrh r1, [r0, #4]
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    and r2, r1, #255
    add r1, sp, #12
    mov r3, #8
    bl native_fn_0221f5fc
    b ov000_02220ed4_L218
ov000_02220ed4_L114:
    mov r0, r6
    bl native_fn_02049ffc
    add r2, r10, #5
    mov r2, r2, lsl #16
    mov r0, #9
    mov r1, #0
    mov r2, r2, lsr #16
    bl native_fn_0205dc70
    str r4, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    mov r1, r0
    ldr r0, =0x021c9698
    mov r2, #80
    mov r3, #1
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f4c
    mov r1, #0
    add r0, r6, #60
    mov r2, r1
    bl native_fn_02085270
    mov r0, #3
    mov r1, #0
    stmia sp, {r0, r4}
    mov r0, r6
    mov r2, #8
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r6
    mov r1, #0
    bl native_fn_02086b14
    b ov000_02220ed4_L218
ov000_02220ed4_L198:
    mov r0, r6
    bl native_fn_02049ffc
    add r2, r10, #5
    mov r2, r2, lsl #16
    mov r0, #9
    mov r1, #0
    mov r2, r2, lsr #16
    bl native_fn_0205dc70
    str r4, [sp]
    mov r1, #255
    str r1, [sp, #0x4]
    mov r1, r0
    ldr r0, =0x021c9698
    mov r2, #80
    mov r3, #1
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f4c
    mov r1, #0
    add r0, r6, #60
    mov r2, r1
    bl native_fn_02085270
    mov r0, #3
    mov r1, #0
    stmia sp, {r0, r4}
    mov r0, r6
    mov r2, #8
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r6
    mov r1, #0
    bl native_fn_02086b14
ov000_02220ed4_L218:
    add r8, r8, #1
    add r9, r9, #1
    add r10, r10, #1
    cmp r10, #3
    blt ov000_02220ed4_L3c
    add sp, sp, #108
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
