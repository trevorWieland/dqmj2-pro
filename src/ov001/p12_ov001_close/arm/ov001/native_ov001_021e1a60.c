/* ov001 row 0x021e1a60: 1276 bytes.
 *
 * What it does: 317 instructions; 25 call(s) to 0x0207b004, 0x0207afec, 0x0207b004, +22 more; loops (back edge at +0xb8); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 25 calls (317 instructions, 25 calls, 30 branches, 23 back edges, 2 literal slots).
 *
 *   pool +0x4f4 -> constant 0x0000010d (image word 0x0000010d)
 *   pool +0x4f8 -> constant 0x00000119 (image word 0x00000119)
 *   branch +0xac -> +0xf8
 *   branch +0xc0 -> +0xf8
 *   branch +0xdc -> +0xf8
 *   branch +0x104 -> +0x15c
 *   branch +0x118 -> +0x15c
 *   branch +0x134 -> +0x15c
 *   branch +0x168 -> +0x1bc
 *   branch +0x17c -> +0x1bc
 *   branch +0x198 -> +0x1bc
 *   branch +0x1cc -> +0x208
 *   branch +0x1e0 -> +0x208
 *   branch +0x218 -> +0x270
 *   branch +0x22c -> +0x270
 *   branch +0x248 -> +0x270
 *   branch +0x27c -> +0x2d8
 *   branch +0x290 -> +0x2d8
 *   branch +0x2a4 -> +0x2b8
 *   branch +0x2b4 -> +0x2d8
 *   branch +0x2e4 -> +0x320
 *   branch +0x2f8 -> +0x320
 *   branch +0x32c -> +0x364
 *   branch +0x340 -> +0x364
 *   branch +0x370 -> +0x3c0
 *   branch +0x384 -> +0x3c0
 *   branch +0x398 -> +0x3c0
 *   branch +0x3cc -> +0x41c
 *   branch +0x3e0 -> +0x41c
 *   branch +0x428 -> +0x454
 *   branch +0x43c -> +0x454
 *   branch +0x47c -> +0x4b8
 *   test +0x1c cmp r8, #0
 *   test +0x28 cmp r7, #0
 *   test +0x34 cmp r6, #0
 *   test +0x44 cmp r11, #0
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r5, #0
 *   test +0x80 cmp r4, #0
 *   test +0x8c cmp r3, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   test +0xd8 cmp r0, #1
 *   test +0x100 cmp r0, #0
 *   test +0x114 cmp r0, #0
 *   test +0x130 cmp r0, #1
 *   test +0x164 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   test +0x194 cmp r0, #1
 *   test +0x1c8 cmp r0, #0
 *   test +0x1dc cmp r0, #0
 *   test +0x214 cmp r0, #0
 *   test +0x228 cmp r0, #0
 *   test +0x244 cmp r0, #1
 *   test +0x278 cmp r0, #0
 *   test +0x28c cmp r0, #0
 *   test +0x2a0 cmp r1, r0
 *   test +0x2b0 cmp r0, #0
 *   test +0x2e0 cmp r0, #0
 *   test +0x2f4 cmp r0, #0
 *   test +0x328 cmp r0, #0
 *   test +0x33c cmp r0, #0
 *   test +0x36c cmp r0, #0
 *   test +0x380 cmp r0, #0
 *   test +0x394 cmp r1, r0
 *   test +0x3c8 cmp r0, #0
 *   test +0x3dc cmp r0, #0
 *   test +0x3f4 cmp r0, #0
 *   test +0x424 cmp r0, #0
 *   test +0x438 cmp r0, #0
 *   test +0x478 cmp r0, #7
 *   test +0x48c cmp r0, #1
 *   test +0x4ac cmp r0, #1
 *   test +0x4c8 cmp r0, #0
 *   0 block transfer(s), 48 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e1a60; the literal pool and
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

extern void native_fn_0207b004(void);
extern void native_fn_0207afec(void);
extern void native_fn_021dce50(void);
extern void native_fn_021dcdec(void);
extern void native_fn_021dc108(void);
extern void native_fn_021dcda8(void);
extern void native_fn_021f08ec(void);
extern void native_fn_021f0d10(void);
extern void native_fn_021d90c4(void);
extern void native_fn_021e19e4(void);


asm u32 native_ov001_021e1a60 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r10, r0
    ldr r0, [sp, #0x40]
    ldr r8, [sp, #0x30]
    str r0, [sp, #0x40]
    str r1, [sp]
    cmp r8, #0
    ldr r7, [sp, #0x34]
    addeq r8, sp, #8
    cmp r7, #0
    ldr r6, [sp, #0x38]
    addeq r7, sp, #4
    cmp r6, #0
    mov r1, #0
    ldr r11, [sp, #0x3c]
    addeq r6, sp, #8
    cmp r11, #0
    strh r1, [r7]
    ldr r0, [sp, #0x40]
    addeq r11, sp, #4
    cmp r0, #0
    addeq r0, sp, #8
    streq r0, [sp, #0x40]
    ldr r5, [sp, #0x44]
    ldr r0, [sp, #0x40]
    str r1, [r6]
    cmp r5, #0
    str r1, [r0]
    ldr r4, [sp, #0x48]
    addeq r5, sp, #8
    mov r0, #1
    cmp r4, #0
    addeq r4, sp, #8
    str r0, [r5]
    cmp r3, #0
    mov r9, r2
    addne sp, sp, #12
    str r1, [r4]
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r9, #512
    ldrsb r0, [r0, #81]
    cmp r0, #0
    beq ov001_021e1a60_Lf8
    mov r0, r10
    mov r1, #8
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_Lf8
    mov r0, r10
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021e1a60_Lf8
    ldr r1, =0x0000010d
    mov r0, #1
    strh r1, [r7]
    add sp, sp, #12
    str r0, [r6]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_Lf8:
    add r0, r9, #512
    ldrsb r0, [r0, #95]
    cmp r0, #0
    beq ov001_021e1a60_L15c
    mov r0, r10
    mov r1, #8
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L15c
    mov r0, r10
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021e1a60_L15c
    ldr r1, =0x00000119
    mov r0, #1
    strh r1, [r7]
    str r0, [r6]
    str r0, [r4]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L15c:
    add r0, r9, #512
    ldrsb r0, [r0, #71]
    cmp r0, #0
    beq ov001_021e1a60_L1bc
    mov r0, r10
    mov r1, #8
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L1bc
    mov r0, r10
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021e1a60_L1bc
    ldr r1, =0x00000119
    mov r0, #1
    strh r1, [r7]
    str r0, [r6]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L1bc:
    mov r0, r9
    mov r1, #48
    bl native_fn_021dce50
    cmp r0, #0
    beq ov001_021e1a60_L208
    mov r0, r10
    mov r1, #33554432
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L208
    mov r0, #249
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    str r0, [r4]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L208:
    mov r0, r9
    mov r1, #49
    bl native_fn_021dce50
    cmp r0, #0
    beq ov001_021e1a60_L270
    mov r0, r10
    mov r1, #67108864
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L270
    mov r0, r10
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021e1a60_L270
    mov r0, #249
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    str r0, [r4]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L270:
    mov r0, r9
    bl native_fn_021dcdec
    cmp r0, #0
    beq ov001_021e1a60_L2d8
    mov r0, r10
    mov r1, #2097152
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L2d8
    add r0, r9, #512
    ldrsb r1, [r0, #137]
    mvn r0, #1
    cmp r1, r0
    beq ov001_021e1a60_L2b8
    mov r0, r9
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_021e1a60_L2d8
ov001_021e1a60_L2b8:
    mov r0, #249
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L2d8:
    add r0, r9, #512
    ldrsb r0, [r0, #94]
    cmp r0, #0
    beq ov001_021e1a60_L320
    mov r0, r10
    mov r1, #4096
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L320
    mov r0, #176
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    str r0, [r4]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L320:
    add r0, r9, #512
    ldrsb r0, [r0, #69]
    cmp r0, #0
    beq ov001_021e1a60_L364
    mov r0, r10
    mov r1, #4096
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L364
    mov r0, #176
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L364:
    add r0, r9, #512
    ldrsb r0, [r0, #96]
    cmp r0, #0
    beq ov001_021e1a60_L3c0
    mov r0, r10
    mov r1, #4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L3c0
    ldr r0, [sp]
    ldrb r1, [r0, #0x31e]
    ldrb r0, [r9, #0x31e]
    cmp r1, r0
    beq ov001_021e1a60_L3c0
    mov r0, #176
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    str r0, [r4]
    mov r0, #0
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L3c0:
    add r0, r9, #512
    ldrsb r0, [r0, #72]
    cmp r0, #0
    beq ov001_021e1a60_L41c
    mov r0, r10
    mov r1, #524288
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L41c
    mov r0, #0
    str r0, [r8]
    str r0, [r5]
    ldrh r0, [r11]
    cmp r0, #0
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x40]
    mov r1, #1
    str r1, [r0]
    rsb r0, r1, #312
    add sp, sp, #12
    strh r0, [r11]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L41c:
    mov r0, r9
    bl native_fn_021dcda8
    cmp r0, #0
    beq ov001_021e1a60_L454
    mov r0, r10
    mov r1, #2048
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021e1a60_L454
    mov r0, #0
    str r0, [r8]
    add sp, sp, #12
    str r0, [r5]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L454:
    mov r0, r9
    mov r1, r10
    bl native_fn_021f08ec
    mov r4, r0
    ldr r0, [sp]
    mov r1, r9
    mov r2, r10
    mov r3, #1
    bl native_fn_021f0d10
    cmp r0, #7
    bne ov001_021e1a60_L4b8
    mov r0, r4
    mov r1, #0
    bl native_fn_021d90c4
    cmp r0, #1
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r10
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021e1a60_L4b8:
    ldr r1, [sp]
    mov r0, r10
    mov r2, r9
    bl native_fn_021e19e4
    cmp r0, #0
    addeq sp, sp, #12
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #176
    strh r0, [r7]
    mov r0, #1
    str r0, [r6]
    mov r0, #0
    str r0, [r5]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
