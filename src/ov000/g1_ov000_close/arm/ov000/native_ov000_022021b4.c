/* ov000 row 0x022021b4: 948 bytes.
 *
 * What it does: 231 instructions; 27 call(s) to 0x02049008, 0x02202248, 0x02217814, +24 more; loops (back edge at +0x48); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x39c -> constant 0x02237d9c (image word 0x02237d9c)
 *   pool +0x3a0 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x3a4 -> native_data_0222f51c (image word 0x0222f51c)
 *   pool +0x3a8 -> constant 0x02237f7c (image word 0x02237f7c)
 *   pool +0x3ac -> constant 0x02237e8c (image word 0x02237e8c)
 *   pool +0x3b0 -> native_data_0222f4cc (image word 0x0222f4cc)
 *   branch +0x20 -> +0x34
 *   branch +0x28 -> +0x148
 *   branch +0x30 -> +0x390
 *   branch +0x58 -> +0x94
 *   back edge +0x90 -> +0x68
 *   branch +0x9c -> +0x390
 *   branch +0xd8 -> +0x114
 *   branch +0x110 -> +0x130
 *   back edge +0x140 -> +0xb8
 *   branch +0x144 -> +0x390
 *   branch +0x198 -> +0x2a0
 *   branch +0x1a0 -> +0x1dc
 *   back edge +0x1d8 -> +0x1b0
 *   branch +0x1e4 -> +0x390
 *   branch +0x204 -> +0x26c
 *   branch +0x268 -> +0x288
 *   back edge +0x298 -> +0x1f4
 *   branch +0x29c -> +0x390
 *   branch +0x2a4 -> +0x2e8
 *   branch +0x2c0 -> +0x2d4
 *   back edge +0x2e4 -> +0x2b4
 *   branch +0x2f0 -> +0x390
 *   back edge +0x38c -> +0x30c
 *   test +0x18 cmp r0, #1
 *   test +0x24 cmp r0, #3
 *   test +0x2c cmp r0, #5
 *   test +0x54 cmp r1, #0
 *   test +0x74 cmp r0, #0
 *   test +0x8c cmp r7, r1
 *   test +0x94 cmp r1, #0
 *   test +0xc4 cmp r0, #0
 *   test +0xd4 cmp r0, #127
 *   test +0x13c cmp r10, r0
 *   test +0x194 cmp r0, #12
 *   test +0x19c cmp r1, #0
 *   test +0x1c0 cmp r0, #0
 *   test +0x1d4 cmp r6, r1
 *   test +0x1dc cmp r1, #0
 *   test +0x200 cmp r1, r0
 *   test +0x230 cmp r0, #0
 *   test +0x294 cmp r10, r0
 *   test +0x2a0 cmp r1, #0
 *   test +0x2bc cmp r6, #0
 *   test +0x2cc cmp r0, #0
 *   test +0x2e0 cmp r6, r1
 *   test +0x2e8 cmp r1, #0
 *   test +0x338 cmp r0, #0
 *   test +0x344 cmp r10, #0
 *   test +0x388 cmp r10, r0
 *   2 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022021b4; the literal pool and
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

extern void native_fn_02049008(void);
extern void native_fn_02217814(void);
extern void native_fn_0204a574(void);
extern u8 native_data_0222f51c[];
extern void native_fn_0204a808(void);
extern void native_fn_0220201c(void);
extern u8 native_data_0222f4cc[];
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02217dbc(void);


asm u32 native_ov000_022021b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    add r1, sp, #12
    mov r2, #0
    strh r2, [r1]
    strh r2, [r1, #2]
    cmp r0, #1
    ldr r9, =0x02237d9c
    beq ov000_022021b4_L34
    cmp r0, #3
    beq ov000_022021b4_L148
    cmp r0, #5
    b ov000_022021b4_L390
ov000_022021b4_L34:
    mov r1, #4
    mov r0, r9
    str r1, [sp]
    mov r1, #5
    mov r3, #1
    bl native_fn_02049008
    ldrh r1, [r9, #12]
    mov r7, #0
    cmp r1, #0
    ble ov000_022021b4_L94
    ldr r6, =0x02237d94
    mov r4, r7
    mov r5, #1
ov000_022021b4_L68:
    add r8, r6, r7
    ldrb r0, [r8, #0x1e8]
    bl native_fn_02217814
    cmp r0, #0
    streqb r5, [r8, #0x3f4]
    strneb r4, [r8, #0x3f4]
    add r0, r7, #1
    ldrh r1, [r9, #12]
    and r7, r0, #255
    cmp r7, r1
    blt ov000_022021b4_L68
ov000_022021b4_L94:
    cmp r1, #0
    mov r10, #0
    ble ov000_022021b4_L390
    mov r7, #1
    ldr r8, =0x02237d94
    mov r11, #3
    mov r6, #16
    mov r4, r7
    add r5, sp, #12
ov000_022021b4_Lb8:
    add r1, r8, r10
    ldrb r0, [r1, #0x3f4]
    strh r6, [sp, #12]
    cmp r0, #0
    ldrb r0, [r1, #0x1e8]
    moveq r2, r7
    movne r2, r11
    cmp r0, #127
    beq ov000_022021b4_L114
    add r0, r0, #1
    mov r0, r0, lsl #16
    mov r1, r0, lsr #16
    stmia sp, {r1, r2}
    add r0, r10, #5
    mov r0, r0, lsl #24
    mov r2, #0
    str r2, [sp, #0x8]
    mov r1, r5
    mov r0, r0, asr #24
    mov r2, #5
    mov r3, #0
    bl native_fn_0204a574
    b ov000_022021b4_L130
ov000_022021b4_L114:
    add r0, r10, #5
    mov r0, r0, lsl #24
    ldr r3, =native_data_0222f51c
    mov r1, r5
    mov r0, r0, asr #24
    str r4, [sp]
    bl native_fn_0204a808
ov000_022021b4_L130:
    ldrh r0, [r9, #12]
    add r1, r10, #1
    and r10, r1, #255
    cmp r10, r0
    blt ov000_022021b4_Lb8
    b ov000_022021b4_L390
ov000_022021b4_L148:
    ldr r1, [r9]
    ldr r0, =0x02237f7c
    ldrb r5, [r0, r1]
    mov r0, r5
    bl native_fn_0220201c
    ldr r9, =0x02237e8c
    mov r4, #2
    mov r0, r9
    mov r1, #5
    mov r2, #0
    mov r3, #1
    str r4, [sp]
    bl native_fn_02049008
    ldr r4, =0x02237d94
    ldr r0, =0x02237f7c
    ldr r1, [r4, #0x8]
    mov r6, #0
    ldrb r0, [r0, r1]
    ldrh r1, [r9, #12]
    cmp r0, #12
    bne ov000_022021b4_L2a0
    cmp r1, #0
    ble ov000_022021b4_L1dc
    and r7, r5, #255
    mov r5, #1
    mov r8, r6
ov000_022021b4_L1b0:
    add r10, r4, r6
    mov r0, r7
    strb r8, [r10, #0x3f4]
    bl native_fn_02217814
    cmp r0, #0
    streqb r5, [r10, #0x3f4]
    add r0, r6, #1
    ldrh r1, [r9, #12]
    and r6, r0, #255
    cmp r6, r1
    blt ov000_022021b4_L1b0
ov000_022021b4_L1dc:
    cmp r1, #0
    mov r10, #0
    ble ov000_022021b4_L390
    ldr r5, =0x02237d94
    ldr r11, =native_data_0222f4cc
    mov r4, #16
ov000_022021b4_L1f4:
    ldr r2, [r9, #0x4]
    ldrh r0, [r9, #14]
    add r1, r2, r10
    cmp r1, r0
    bge ov000_022021b4_L26c
    add r7, r5, r10
    add r0, r7, r2
    add r8, r10, #5
    ldrb r6, [r0, #0x1ec]
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldrb r0, [r7, #0x3f4]
    strh r4, [sp, #12]
    mov r3, #0
    cmp r0, #0
    mov r0, #6
    mla r0, r6, r0, r11
    ldrh r1, [r0, #2]
    moveq r2, #1
    movne r2, #3
    stmia sp, {r1, r2}
    mov r0, r8, lsl #24
    mov r2, #1
    str r2, [sp, #0x8]
    mov r0, r0, asr #24
    add r1, sp, #12
    mov r2, #6
    bl native_fn_0204a574
    b ov000_022021b4_L288
ov000_022021b4_L26c:
    add r0, r10, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
ov000_022021b4_L288:
    ldrh r0, [r9, #12]
    add r1, r10, #1
    and r10, r1, #255
    cmp r10, r0
    blt ov000_022021b4_L1f4
    b ov000_022021b4_L390
ov000_022021b4_L2a0:
    cmp r1, #0
    ble ov000_022021b4_L2e8
    and r7, r5, #255
    mov r5, #1
    mov r8, r6
ov000_022021b4_L2b4:
    add r10, r4, r6
    strb r8, [r10, #0x3f4]
    cmp r6, #0
    bne ov000_022021b4_L2d4
    mov r0, r7
    bl native_fn_02217814
    cmp r0, #0
    streqb r5, [r10, #0x3f4]
ov000_022021b4_L2d4:
    ldrh r1, [r9, #12]
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, r1
    blt ov000_022021b4_L2b4
ov000_022021b4_L2e8:
    cmp r1, #0
    mov r10, #0
    ble ov000_022021b4_L390
    mov r7, #1
    ldr r8, =0x02237d94
    mov r6, #3
    mov r5, #16
    mov r11, #26
    mov r4, r7
ov000_022021b4_L30c:
    ldr r1, [r9]
    ldr r0, [r9, #0x4]
    add r1, r1, #5
    sub r0, r1, r0
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    add r0, r8, r10
    ldrb r0, [r0, #0x3f4]
    strh r5, [sp, #12]
    mov r2, #5
    cmp r0, #0
    moveq r1, r7
    movne r1, r6
    cmp r10, #0
    moveq r0, r11
    movne r0, #12
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    str r1, [sp, #0x4]
    add r0, r10, #5
    mov r0, r0, lsl #24
    add r1, sp, #12
    mov r0, r0, asr #24
    str r4, [sp, #0x8]
    mov r3, #2
    bl native_fn_0204a574
    add r1, r10, #1
    ldrh r0, [r9, #12]
    and r10, r1, #255
    cmp r10, r0
    blt ov000_022021b4_L30c
ov000_022021b4_L390:
    bl native_fn_02217dbc
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
