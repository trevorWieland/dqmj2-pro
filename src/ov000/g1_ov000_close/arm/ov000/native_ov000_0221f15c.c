/* ov000 row 0x0221f15c: 504 bytes.
 *
 * What it does: 124 instructions; 11 call(s) to 0x0221c658, 0x0221c758, 0x0204a574, +8 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1f0 -> native_data_0222df38 (image word 0x0222df38)
 *   pool +0x1f4 -> constant 0x022463a0 (image word 0x022463a0)
 *   branch +0xb0 -> +0x1bc
 *   branch +0xf4 -> +0x120
 *   branch +0x130 -> +0x15c
 *   back edge +0x1b8 -> +0xc8
 *   test +0xac cmp r1, #0
 *   test +0xf0 tst r8, #1
 *   test +0x120 tst r8, #2
 *   test +0x1b4 cmp r1, r0, asr #24
 *   0 block transfer(s), 27 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221f15c; the literal pool and
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

extern u8 native_data_0222df38[];
extern void native_fn_0221c658(void);
extern void native_fn_0221c758(void);
extern void native_fn_0204a574(void);
extern void native_fn_0221e85c(void);
extern void native_fn_02087554(void);
extern void native_fn_0204a808(void);
extern void native_fn_0221cdcc(void);


asm u32 native_ov000_0221f15c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #36
    ldr r1, =native_data_0222df38
    str r0, [sp, #0x14]
    ldrh r0, [r1, #2]
    ldrh r1, [r1]
    strh r0, [sp, #34]
    strh r1, [sp, #32]
    bl native_fn_0221c658
    mov r1, #4
    str r1, [sp]
    mov r2, #30
    ldr r1, =0x022463a0
    str r2, [sp, #0x4]
    ldrsb r2, [r1, #1]
    mov r1, #0
    mov r3, #1
    mov r2, r2, lsl #1
    add r2, r2, #2
    and r2, r2, #255
    str r2, [sp, #0x8]
    str r1, [sp, #0xc]
    str r3, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #10
    mov r2, #2
    bl native_fn_0221c758
    mov r0, #16
    mov r3, #0
    strh r0, [sp, #28]
    strh r3, [sp, #30]
    mov r0, #14
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #28
    mov r0, #10
    mov r2, #9
    bl native_fn_0204a574
    ldr r4, =0x022463a0
    mov r10, #0
    ldrsb r1, [r4, #1]
    cmp r1, #0
    ble ov000_0221f15c_L1bc
    mov r9, #16
    add r6, sp, #28
    add r11, sp, #24
    mov r5, r10
    mov r7, r10
ov000_0221f15c_Lc8:
    sub r0, r1, r10
    ldr r1, [r4, #0x4]
    add r0, r1, r0, lsl #1
    ldrb r0, [r0, #-0x2]
    bl native_fn_0221e85c
    mov r8, r0
    mov r0, #24
    strh r7, [sp, #26]
    strh r0, [sp, #28]
    strh r9, [sp, #30]
    tst r8, #1
    beq ov000_0221f15c_L120
    mov r0, r7
    bl native_fn_02087554
    strh r0, [sp, #24]
    mov r0, #0
    str r0, [sp]
    mov r0, #10
    mov r1, r6
    mov r2, #1
    mov r3, r11
    bl native_fn_0204a808
ov000_0221f15c_L120:
    tst r8, #2
    ldrsh r0, [sp, #28]
    add r0, r0, #8
    strh r0, [sp, #28]
    beq ov000_0221f15c_L15c
    mov r0, #1
    bl native_fn_02087554
    strh r0, [sp, #24]
    mov r0, #0
    str r0, [sp]
    mov r0, #10
    mov r1, r6
    mov r2, #1
    mov r3, r11
    bl native_fn_0204a808
ov000_0221f15c_L15c:
    ldrsh r2, [sp, #28]
    ldrsb r1, [r4, #1]
    mov r0, #10
    add r2, r2, #8
    strh r2, [sp, #28]
    ldr r3, [r4, #0x4]
    sub r2, r1, r10
    add r2, r3, r2, lsl #1
    ldrb r8, [r2, #-0x2]
    mov r1, r6
    mov r2, #8
    str r8, [sp]
    mov r8, #1
    str r8, [sp, #0x4]
    mov r3, r5
    str r5, [sp, #0x8]
    bl native_fn_0204a574
    add r0, r10, #1
    mov r0, r0, lsl #24
    ldrsb r1, [r4, #1]
    add r9, r9, #16
    mov r10, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_0221f15c_Lc8
ov000_0221f15c_L1bc:
    mov r0, r1, lsl #1
    add r0, r0, #6
    and r1, r0, #255
    str r1, [sp]
    mov r4, #12
    ldr r0, [sp, #0x14]
    add r2, sp, #32
    mov r1, #2
    mov r3, #1
    str r4, [sp, #0x4]
    bl native_fn_0221cdcc
    add sp, sp, #36
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
