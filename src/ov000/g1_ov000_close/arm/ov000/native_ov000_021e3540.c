/* ov000 row 0x021e3540: 1032 bytes.
 *
 * What it does: 247 instructions; 37 call(s) to 0x021e3444, 0x021e3910, 0x021e3478, +34 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}; 11 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3dc -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x3e0 -> native_data_0222ec00 (image word 0x0222ec00)
 *   pool +0x3e4 -> native_data_0222ec04 (image word 0x0222ec04)
 *   pool +0x3e8 -> native_data_0222ec08 (image word 0x0222ec08)
 *   pool +0x3ec -> native_data_0222ec0c (image word 0x0222ec0c)
 *   pool +0x3f0 -> native_data_0222ec10 (image word 0x0222ec10)
 *   pool +0x3f4 -> native_data_0222ec14 (image word 0x0222ec14)
 *   pool +0x3f8 -> native_data_0222ec18 (image word 0x0222ec18)
 *   pool +0x3fc -> native_data_0222ec1c (image word 0x0222ec1c)
 *   pool +0x400 -> native_data_0222ec20 (image word 0x0222ec20)
 *   pool +0x404 -> native_data_0222ec24 (image word 0x0222ec24)
 *   branch +0x18 -> +0x3d0
 *   branch +0x84 -> +0xc4
 *   branch +0xc0 -> +0x3b8
 *   branch +0xd8 -> +0x114
 *   branch +0x110 -> +0x3b8
 *   branch +0x128 -> +0x168
 *   branch +0x164 -> +0x3b8
 *   branch +0x17c -> +0x1bc
 *   branch +0x1b8 -> +0x3b8
 *   branch +0x1d0 -> +0x210
 *   branch +0x20c -> +0x3b8
 *   branch +0x224 -> +0x264
 *   branch +0x260 -> +0x3b8
 *   branch +0x278 -> +0x2ac
 *   branch +0x2a8 -> +0x3b8
 *   branch +0x2c0 -> +0x2f4
 *   branch +0x2f0 -> +0x3b8
 *   branch +0x308 -> +0x344
 *   branch +0x340 -> +0x3b8
 *   branch +0x364 -> +0x398
 *   branch +0x394 -> +0x3b8
 *   branch +0x3c0 -> +0x3c8
 *   test +0x14 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0xd4 cmp r0, #0
 *   test +0x124 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   test +0x1cc cmp r0, #0
 *   test +0x220 cmp r0, #0
 *   test +0x274 cmp r0, #0
 *   test +0x2bc cmp r0, #0
 *   test +0x304 cmp r0, #0
 *   test +0x354 cmp r0, #0
 *   test +0x3bc cmp r0, #0
 *   8 block transfer(s), 41 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e3540; the literal pool and
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

extern void native_fn_021e3444(void);
extern void native_fn_021e3478(void);
extern void native_fn_0201b208(void);
extern void native_fn_0201d780(void);
extern void native_fn_021df2d4(void);
extern u8 native_data_0222ec00[];
extern void native_fn_0201d914(void);
extern void native_fn_021e34b8(void);
extern void native_fn_021e34f0(void);
extern u8 native_data_0222ec04[];
extern u8 native_data_0222ec08[];
extern u8 native_data_0222ec0c[];
extern u8 native_data_0222ec10[];
extern u8 native_data_0222ec14[];
extern u8 native_data_0222ec18[];
extern u8 native_data_0222ec1c[];
extern u8 native_data_0222ec20[];
extern u8 native_data_0222ec24[];
extern void native_fn_021e7b08(void);


asm u32 native_ov000_021e3540 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #52
    mov r5, r0
    mov r6, #0
    bl native_fn_021e3444
    cmp r0, #0
    blt ov000_021e3540_L3d0
    ldr r2, =0x02234388
    mov r1, #52
    mla r4, r0, r1, r2
    mov r0, r4
    mov r1, r5
    mov r2, r6
    bl native_fn_021e3478
    add r0, sp, #20
    mov r1, r6
    mov r2, #32
    bl native_fn_0201b208
    add r0, sp, #20
    add r1, r5, #2
    mov r2, #7
    bl native_fn_0201d780
    ldrsb r1, [r5, #9]
    add r0, sp, #20
    sub r1, r1, #65
    strb r1, [r4, #0x1e]
    bl native_fn_021df2d4
    strb r0, [r4, #0x1f]
    ldr r1, =native_data_0222ec00
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_Lc4
    mov r3, #1
    str r3, [sp]
    mov r12, r6
    str r12, [sp, #0x4]
    str r12, [sp, #0x8]
    str r12, [sp, #0xc]
    mov r0, r4
    mov r1, #6
    mov r2, #3
    str r12, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_Lc4:
    ldr r1, =native_data_0222ec04
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L114
    mov r2, r6
    mov r0, #3
    stmia sp, {r0, r2}
    str r2, [sp, #0x8]
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #1
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L114:
    ldr r1, =native_data_0222ec08
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L168
    mov r2, r6
    mov r0, #3
    stmia sp, {r0, r2}
    mov r0, #2
    str r0, [sp, #0x8]
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #1
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L168:
    ldr r1, =native_data_0222ec0c
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L1bc
    mov r2, r6
    mov r0, #3
    stmia sp, {r0, r2}
    mov r0, #4
    str r0, [sp, #0x8]
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #1
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L1bc:
    ldr r1, =native_data_0222ec10
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L210
    mov r0, #3
    str r0, [sp]
    mov r2, r6
    mov r0, #1
    stmib sp, {r0, r2}
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #10
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L210:
    ldr r1, =native_data_0222ec14
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L264
    mov r0, #3
    str r0, [sp]
    mov r2, r6
    mov r0, #2
    stmib sp, {r0, r2}
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #13
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L264:
    ldr r1, =native_data_0222ec18
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L2ac
    mov r0, #3
    str r0, [sp]
    mov r2, r6
    mov r0, #2
    stmib sp, {r0, r2}
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #8
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    b ov000_021e3540_L3b8
ov000_021e3540_L2ac:
    ldr r1, =native_data_0222ec1c
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L2f4
    mov r0, #3
    str r0, [sp]
    mov r2, r6
    mov r0, #2
    stmib sp, {r0, r2}
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #4
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    b ov000_021e3540_L3b8
ov000_021e3540_L2f4:
    ldr r1, =native_data_0222ec20
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e3540_L344
    mov r2, r6
    mov r0, #3
    stmia sp, {r0, r2}
    str r2, [sp, #0x8]
    str r2, [sp, #0xc]
    mov r0, r4
    mov r3, r2
    mov r1, #26
    str r2, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L344:
    ldr r1, =native_data_0222ec24
    add r0, r5, #10
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, #1
    mov r1, #3
    str r0, [sp]
    bne ov000_021e3540_L398
    mov r3, r6
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    str r3, [sp, #0xc]
    mov r0, r4
    mov r2, r1
    str r3, [sp, #0x10]
    bl native_fn_021e34b8
    mov r0, r4
    add r1, r5, #12
    bl native_fn_021e34f0
    b ov000_021e3540_L3b8
ov000_021e3540_L398:
    mov r3, r6
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    str r3, [sp, #0xc]
    mov r0, r4
    mov r2, r1
    str r3, [sp, #0x10]
    bl native_fn_021e34b8
ov000_021e3540_L3b8:
    ldrsh r0, [r4, #46]
    cmp r0, #0
    ble ov000_021e3540_L3c8
    bl native_fn_021e7b08
ov000_021e3540_L3c8:
    mov r6, #1
    strb r6, [r4, #0x1c]
ov000_021e3540_L3d0:
    mov r0, r6
    add sp, sp, #52
    ldmia sp!, {r3, r4, r5, r6, pc}
}
