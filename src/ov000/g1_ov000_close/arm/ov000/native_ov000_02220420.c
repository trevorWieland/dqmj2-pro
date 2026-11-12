/* ov000 row 0x02220420: 608 bytes.
 *
 * What it does: 150 instructions; 15 call(s) to 0x0221c658, 0x0221c758, 0x0221c658, +12 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x258 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x25c -> constant 0x022463dc (image word 0x022463dc)
 *   back edge +0x104 -> +0xb4
 *   branch +0x10c -> +0x14c
 *   back edge +0x1cc -> +0x174
 *   branch +0x200 -> +0x22c
 *   back edge +0x228 -> +0x20c
 *   test +0xb4 cmp r7, #0
 *   test +0x100 cmp r7, #2
 *   test +0x108 cmp r10, #0
 *   test +0x14c cmp r10, #0
 *   test +0x174 cmp r10, #0
 *   test +0x1c8 cmp r8, #3
 *   test +0x1d4 cmp r10, #0
 *   test +0x1ec cmp r0, #0
 *   test +0x1f4 cmpne r0, #0
 *   test +0x218 cmp r0, #0
 *   test +0x224 cmp r3, #3
 *   2 block transfer(s), 24 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220420; the literal pool and
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
extern void native_fn_0221c758(void);
extern void native_fn_0221c8dc(void);
extern void native_fn_0221cab0(void);


asm u32 native_ov000_02220420 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    movs r10, r1
    str r0, [sp, #0x14]
    movne r0, #3
    moveq r0, #2
    mov r5, r0, lsl #1
    bl native_fn_0221c658
    mov r4, r0
    mov r0, #5
    add r1, r5, #2
    str r0, [sp]
    mov r2, #17
    str r2, [sp, #0x4]
    and r1, r1, #255
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    mov r3, #0
    str r3, [sp, #0x10]
    ldrsb r1, [r4, #16]
    mov r2, #12
    bl native_fn_0221c758
    bl native_fn_0221c658
    add r1, r5, #7
    and r1, r1, #255
    str r1, [sp]
    mov r1, #19
    str r1, [sp, #0x4]
    mov r1, #8
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    mov r3, #0
    str r3, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #6
    mov r2, #12
    bl native_fn_0221c758
    mov r7, #0
    mov r8, #6
    mov r6, #15
    mov r5, #2
    mov r11, r7
    mov r4, #1
ov000_02220420_Lb4:
    cmp r7, #0
    moveq r9, #4
    movne r9, #1
    bl native_fn_0221c658
    mov r1, r9, lsl #24
    mov r2, r1, asr #24
    and r1, r8, #255
    stmia sp, {r1, r6}
    str r5, [sp, #0x8]
    str r11, [sp, #0xc]
    str r4, [sp, #0x10]
    ldrsb r1, [r0, #16]
    add r0, r7, #10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r3, r4
    bl native_fn_0221c758
    add r7, r7, #1
    add r8, r8, #2
    cmp r7, #2
    blt ov000_02220420_Lb4
    cmp r10, #0
    beq ov000_02220420_L14c
    bl native_fn_0221c658
    mov r1, #10
    str r1, [sp]
    mov r1, #15
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    mov r1, #0
    mov r2, #1
    str r1, [sp, #0xc]
    str r2, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r3, r2
    mov r0, #12
    bl native_fn_0221c758
ov000_02220420_L14c:
    cmp r10, #0
    movne r0, #13
    moveq r0, #12
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    mov r8, #0
    mov r5, #14
    mov r6, #12
    mov r11, #17
    mov r4, #1
ov000_02220420_L174:
    cmp r10, #0
    movne r9, r5
    moveq r9, r6
    bl native_fn_0221c658
    and r1, r9, #255
    stmia sp, {r1, r11}
    mov r1, #2
    str r1, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r4, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, r7, lsl #24
    mov r0, r0, asr #24
    mov r2, r4
    mov r3, r4
    bl native_fn_0221c758
    add r8, r8, #1
    add r5, r5, #2
    add r6, r6, #2
    add r7, r7, #1
    cmp r8, #3
    blt ov000_02220420_L174
    ldr r0, =0x022463b0
    cmp r10, #0
    ldr r2, [r0, #0x1c]
    movne r1, #6
    ldrsh r0, [r2, #24]
    moveq r1, #5
    and r1, r1, #255
    cmp r0, #0
    ldrnesh r0, [r2, #156]
    cmpne r0, #0
    subeq r0, r1, #3
    andeq r1, r0, #255
    beq ov000_02220420_L22c
    ldr r2, =0x022463dc
    mov r3, #0
ov000_02220420_L20c:
    mov r0, r3, lsl #1
    ldrsh r0, [r2, r0]
    add r3, r3, #1
    cmp r0, #0
    subeq r0, r1, #1
    andeq r1, r0, #255
    cmp r3, #3
    blt ov000_02220420_L20c
ov000_02220420_L22c:
    mov r3, #0
    str r3, [sp]
    mov r4, #1
    ldr r0, [sp, #0x14]
    mov r2, r1
    mov r3, #10
    str r4, [sp, #0x4]
    bl native_fn_0221c8dc
    bl native_fn_0221cab0
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
