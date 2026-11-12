/* ov000 row 0x0221e03c: 812 bytes.
 *
 * What it does: 199 instructions; 23 call(s) to 0x02221344, 0x02221358, 0x0221c664, +20 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x31c -> constant 0x02246318 (image word 0x02246318)
 *   pool +0x320 -> constant 0x02246348 (image word 0x02246348)
 *   pool +0x324 -> native_data_0222fb28 (image word 0x0222fb28)
 *   pool +0x328 -> native_data_0222fb20 (image word 0x0222fb20)
 *   branch +0x40 -> +0x298
 *   branch +0x4c -> +0x298
 *   branch +0x5c -> +0x298
 *   branch +0xc4 -> +0x180
 *   branch +0xe0 -> +0x180
 *   branch +0xfc -> +0x180
 *   branch +0x110 -> +0x180
 *   branch +0x138 -> +0x154
 *   branch +0x17c -> +0x194
 *   branch +0x19c -> +0x230
 *   branch +0x1ac -> +0x230
 *   branch +0x1bc -> +0x230
 *   branch +0x1e4 -> +0x204
 *   branch +0x22c -> +0x244
 *   back edge +0x25c -> +0x8c
 *   branch +0x264 -> +0x2f8
 *   back edge +0x290 -> +0x26c
 *   branch +0x294 -> +0x2f8
 *   back edge +0x2c4 -> +0x2a0
 *   back edge +0x2f4 -> +0x2d0
 *   test +0x3c cmp r0, #2
 *   test +0x44 cmp r5, #0
 *   test +0x48 cmpne r4, #0
 *   test +0x58 cmp r0, #0
 *   test +0xa4 cmp r0, #0
 *   test +0xc0 cmp r0, #0
 *   test +0xdc cmp r6, r0
 *   test +0xf8 cmp r6, r0
 *   test +0x108 cmp r0, #0
 *   test +0x10c cmpne r6, #9
 *   test +0x11c cmp r1, r0
 *   test +0x128 cmpeq r1, r0
 *   test +0x134 cmpeq r1, r0
 *   test +0x198 cmp r0, #0
 *   test +0x1a8 cmp r0, #0
 *   test +0x1b8 cmp r0, #0
 *   test +0x1c8 cmp r1, r0
 *   test +0x1d4 cmpeq r1, r0
 *   test +0x1e0 cmpeq r1, r0
 *   test +0x258 cmp r8, #3
 *   test +0x260 cmp r8, #6
 *   test +0x28c cmp r8, #6
 *   test +0x2c0 cmp r4, #3
 *   test +0x2f0 cmp r4, #6
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e03c; the literal pool and
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

extern void native_fn_02221344(void);
extern void native_fn_02221358(void);
extern void native_fn_0221c664(void);
extern void native_fn_02062a10(void);
extern void native_fn_0222131c(void);
extern void native_fn_02044dc4(void);
extern void native_fn_02220778(void);
extern u8 native_data_0222fb28[];
extern void native_fn_02048644(void);
extern void native_fn_02048a60(void);
extern void native_fn_02063520(void);
extern void native_fn_0203cfe0(void);
extern u8 native_data_0222fb20[];


asm u32 native_ov000_0221e03c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r10, r0
    str r1, [sp]
    bl native_fn_02221344
    mov r5, r0
    bl native_fn_02221358
    mov r4, r0
    bl native_fn_0221c664
    ldrsb r1, [r10, #16]
    str r0, [sp, #0xc]
    sub r0, r1, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #2
    bhi ov000_0221e03c_L298
    cmp r5, #0
    cmpne r4, #0
    beq ov000_0221e03c_L298
    ldr r0, =0x02246318
    ldrb r0, [r0]
    cmp r0, #0
    bne ov000_0221e03c_L298
    mov r0, r5
    bl native_fn_02062a10
    str r0, [sp, #0x8]
    mov r0, r4
    bl native_fn_02062a10
    ldr r5, =0x02246348
    ldr r4, =0x02246318
    str r0, [sp, #0x4]
    mov r8, #0
    mov r11, #14
    mov r7, #12
ov000_0221e03c_L8c:
    mov r0, r8
    add r1, sp, #16
    add r2, sp, #18
    bl native_fn_0222131c
    ldr r0, [sp]
    ldrb r1, [sp, #0x12]
    cmp r0, #0
    movne r9, r11, lsl #3
    ldrsh r0, [sp, #16]
    moveq r9, r7, lsl #3
    bl native_fn_02044dc4
    mov r6, r0
    ldrsh r0, [sp, #16]
    cmp r0, #0
    beq ov000_0221e03c_L180
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x8]
    ldrsh r0, [r0, #24]
    ldrb r1, [r1, #0x1a]
    bl native_fn_02044dc4
    cmp r6, r0
    bls ov000_0221e03c_L180
    ldr r0, [sp, #0x4]
    ldr r1, [sp, #0x4]
    ldrsh r0, [r0, #24]
    ldrb r1, [r1, #0x1a]
    bl native_fn_02044dc4
    cmp r6, r0
    bls ov000_0221e03c_L180
    ldrsh r0, [sp, #16]
    bl native_fn_02220778
    cmp r0, #0
    cmpne r6, #9
    beq ov000_0221e03c_L180
    ldrsb r1, [r4, #2]
    ldrsb r0, [r10, #16]
    cmp r1, r0
    ldreq r1, [r4, #0x8]
    ldreq r0, [r10]
    cmpeq r1, r0
    ldreq r1, [r4, #0xc]
    ldreq r0, [sp, #0xc]
    cmpeq r1, r0
    beq ov000_0221e03c_L154
    ldr r0, =native_data_0222fb28
    ldr r1, [r4, #0x10]
    ldrb r2, [r0, r6]
    add r0, r5, r8, lsl #2
    ldr r0, [r0, #0x34]
    bl native_fn_02048644
ov000_0221e03c_L154:
    add r0, r5, r8, lsl #2
    ldr r0, [r0, #0x34]
    mov r1, #0
    add r2, r9, #8
    bl native_fn_02048a60
    add r0, r5, r8, lsl #2
    ldr r1, [r0, #0x34]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
    b ov000_0221e03c_L194
ov000_0221e03c_L180:
    add r0, r5, r8, lsl #2
    ldr r1, [r0, #0x34]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221e03c_L194:
    ldrsh r0, [sp, #16]
    cmp r0, #0
    beq ov000_0221e03c_L230
    ldrb r1, [sp, #0x12]
    bl native_fn_02063520
    cmp r0, #0
    bne ov000_0221e03c_L230
    ldrsh r0, [sp, #16]
    bl native_fn_02220778
    cmp r0, #0
    beq ov000_0221e03c_L230
    ldrsb r1, [r4, #2]
    ldrsb r0, [r10, #16]
    cmp r1, r0
    ldreq r1, [r4, #0x8]
    ldreq r0, [r10]
    cmpeq r1, r0
    ldreq r1, [r4, #0xc]
    ldreq r0, [sp, #0xc]
    cmpeq r1, r0
    beq ov000_0221e03c_L204
    bl native_fn_0203cfe0
    ldr r1, =native_data_0222fb20
    ldrb r2, [r1, r0]
    add r0, r5, r8, lsl #2
    ldr r0, [r0, #0x40]
    ldr r1, [r4, #0x10]
    bl native_fn_02048644
ov000_0221e03c_L204:
    add r0, r5, r8, lsl #2
    ldr r0, [r0, #0x40]
    mov r2, r9
    mov r1, #0
    bl native_fn_02048a60
    add r0, r5, r8, lsl #2
    ldr r1, [r0, #0x40]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
    b ov000_0221e03c_L244
ov000_0221e03c_L230:
    add r0, r5, r8, lsl #2
    ldr r1, [r0, #0x40]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221e03c_L244:
    add r11, r11, #2
    add r7, r7, #2
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #3
    blt ov000_0221e03c_L8c
    cmp r8, #6
    bge ov000_0221e03c_L2f8
    ldr r3, =0x02246348
ov000_0221e03c_L26c:
    add r0, r3, r8, lsl #2
    ldr r2, [r0, #0x40]
    add r0, r8, #1
    ldr r1, [r2, #0x7c]
    mov r0, r0, lsl #24
    bic r1, r1, #2
    mov r8, r0, asr #24
    str r1, [r2, #0x7c]
    cmp r8, #6
    blt ov000_0221e03c_L26c
    b ov000_0221e03c_L2f8
ov000_0221e03c_L298:
    ldr r3, =0x02246348
    mov r4, #0
ov000_0221e03c_L2a0:
    add r0, r3, r4, lsl #2
    ldr r2, [r0, #0x34]
    add r0, r4, #1
    ldr r1, [r2, #0x7c]
    mov r0, r0, lsl #24
    bic r1, r1, #2
    mov r4, r0, asr #24
    str r1, [r2, #0x7c]
    cmp r4, #3
    blt ov000_0221e03c_L2a0
    ldr r3, =0x02246348
    mov r4, #0
ov000_0221e03c_L2d0:
    add r0, r3, r4, lsl #2
    ldr r2, [r0, #0x40]
    add r0, r4, #1
    ldr r1, [r2, #0x7c]
    mov r0, r0, lsl #24
    bic r1, r1, #2
    mov r4, r0, asr #24
    str r1, [r2, #0x7c]
    cmp r4, #6
    blt ov000_0221e03c_L2d0
ov000_0221e03c_L2f8:
    ldrsb r0, [r10, #16]
    ldr r1, =0x02246318
    strb r0, [r1, #0x2]
    ldr r0, [r10]
    str r0, [r1, #0x8]
    ldr r0, [sp, #0xc]
    str r0, [r1, #0xc]
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
