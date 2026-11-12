/* ov001 row 0x021f7544: 964 bytes.
 *
 * What it does: 238 instructions; 29 call(s) to 0x0207afec, 0x021e1410, 0x021ee78c, +26 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 29 calls (238 instructions, 29 calls, 19 branches, 22 back edges, 3 literal slots).
 *
 *   pool +0x3b8 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x3bc -> constant 0x0223995c (image word 0x0223995c)
 *   pool +0x3c0 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x3c -> +0x7c
 *   branch +0x50 -> +0x7c
 *   branch +0x78 -> +0x3ac
 *   branch +0x88 -> +0xcc
 *   branch +0xa0 -> +0xcc
 *   branch +0xc8 -> +0x3ac
 *   branch +0x128 -> +0x190
 *   branch +0x13c -> +0x1b8
 *   back edge +0x188 -> +0x144
 *   branch +0x18c -> +0x1b8
 *   branch +0x1c0 -> +0x28c
 *   branch +0x1c8 -> +0x204
 *   branch +0x1e8 -> +0x1fc
 *   branch +0x294 -> +0x2cc
 *   branch +0x2c8 -> +0x35c
 *   branch +0x2d4 -> +0x338
 *   branch +0x2f0 -> +0x35c
 *   branch +0x334 -> +0x35c
 *   branch +0x340 -> +0x35c
 *   branch +0x368 -> +0x3a4
 *   branch +0x37c -> +0x3a4
 *   branch +0x394 -> +0x3a4
 *   test +0x38 cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0x9c cmp r0, #0
 *   test +0x124 cmp r0, #0
 *   test +0x138 cmp r0, #0
 *   test +0x184 cmp r7, r0
 *   test +0x1bc cmp r0, #0
 *   test +0x1c4 cmp r6, #0
 *   test +0x1e4 cmp r0, #0
 *   test +0x290 cmp r0, #0
 *   test +0x2d0 cmp r0, #0
 *   test +0x2ec cmp r0, #0
 *   test +0x33c cmp r0, #0
 *   test +0x360 cmp r0, #0
 *   test +0x36c cmp r6, #0
 *   test +0x374 cmpne r0, #0
 *   test +0x38c cmp r0, #0
 *   test +0x398 cmp r6, #20
 *   0 block transfer(s), 31 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f7544; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021e1410(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021f949c(void);
extern void native_fn_021e1468(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021f0818(void);
extern void native_fn_021db718(void);
extern void native_fn_021e13c8(void);
extern void native_fn_021d9494(void);
extern void native_fn_022024d4(void);
extern void native_fn_021dc9d4(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220f600(void);
extern void native_fn_021dc59c(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021dc5d4(void);


asm u32 native_ov001_021f7544 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #56
    ldr r3, =0x0223989c
    mov r10, r1
    ldrh r4, [r3, #80]
    str r0, [sp, #0x1c]
    mov r1, #0
    mov r0, r4
    mov r9, r2
    str r1, [sp, #0x20]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r5, r0
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    bne ov001_021f7544_L7c
    ldr r0, [sp, #0x1c]
    mov r1, r4
    bl native_fn_021e1410
    cmp r0, #0
    beq ov001_021f7544_L7c
    mov r1, #0
    str r1, [sp]
    ldrb r3, [r5, #0x1e]
    mov r0, r10
    mov r2, r4
    bl native_fn_021ee78c
    mov r0, #228
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021f7544_L3ac
ov001_021f7544_L7c:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne ov001_021f7544_Lcc
    ldr r0, [sp, #0x1c]
    mov r1, r10
    mov r2, r4
    bl native_fn_021e1468
    cmp r0, #0
    beq ov001_021f7544_Lcc
    mov r1, #0
    str r1, [sp]
    ldrb r3, [r5, #0x1e]
    mov r0, r10
    mov r2, r4
    bl native_fn_021ee78c
    mov r0, #228
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021f7544_L3ac
ov001_021f7544_Lcc:
    mov r0, #0
    str r0, [sp]
    add r1, sp, #36
    str r1, [sp, #0x4]
    add r0, sp, #52
    str r0, [sp, #0x8]
    add r0, r10, #844
    str r0, [sp, #0xc]
    add r1, sp, #44
    str r1, [sp, #0x10]
    add r0, sp, #48
    str r0, [sp, #0x14]
    add r1, sp, #40
    str r1, [sp, #0x18]
    ldr r0, =0x0223989c
    ldr r1, [sp, #0x1c]
    ldrb r3, [r0, #0x10]
    mov r0, r4
    mov r2, r10
    bl native_fn_021e1a60
    ldr r11, =0x0223989c
    ldrb r0, [r11, #0x10]
    cmp r0, #0
    beq ov001_021f7544_L190
    ldrsb r0, [r11, #43]
    mov r6, #0
    mov r7, r6
    cmp r0, #0
    ble ov001_021f7544_L1b8
    ldr r8, =0x0223995c
ov001_021f7544_L144:
    ldrb r0, [r8], #1
    mov r1, r10
    mov r2, r4
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    ldr r0, =0x022399b8
    str r9, [sp, #0xc]
    ldr r0, [r0, r7, lsl #2]
    mov r3, #0
    bl native_fn_021f0818
    add r6, r6, r0
    ldrsb r0, [r11, #43]
    add r7, r7, #1
    cmp r7, r0
    blt ov001_021f7544_L144
    b ov001_021f7544_L1b8
ov001_021f7544_L190:
    mov r3, #0
    str r3, [sp]
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    ldr r0, [sp, #0x1c]
    mov r1, r10
    mov r2, r4
    str r9, [sp, #0xc]
    bl native_fn_021f0818
    mov r6, r0
ov001_021f7544_L1b8:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    beq ov001_021f7544_L28c
    cmp r6, #0
    ble ov001_021f7544_L204
    mov r0, r10
    rsb r1, r6, #0
    bl native_fn_021db718
    mov r0, r10
    mov r1, r4
    bl native_fn_021e13c8
    cmp r0, #0
    bne ov001_021f7544_L1fc
    mov r0, r10
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
ov001_021f7544_L1fc:
    mov r0, #1
    str r0, [sp, #0x20]
ov001_021f7544_L204:
    mov r0, #0
    str r0, [sp]
    ldrb r3, [r5, #0x1e]
    mov r0, r10
    mov r1, r6
    mov r2, r4
    bl native_fn_021ee78c
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r6
    bl native_fn_022024d4
    ldrb r0, [r10, #0x357]
    ldr r1, =0x0223989c
    add r0, r0, #1
    strb r0, [r10, #0x357]
    ldr r0, [r1, #0x84]
    ldrb r2, [r10, #0x31f]
    add r0, r0, #78
    add r3, r0, #768
    mov r2, r2, lsl #1
    ldrsh r0, [r3, r2]
    add r0, r0, r6
    strh r0, [r3, r2]
    ldr r0, [r1, #0x84]
    bl native_fn_021dc9d4
    mov r7, r0
    mov r0, r4
    bl native_fn_021f2464
    str r0, [sp]
    ldr r0, [sp, #0x1c]
    mov r3, r7
    mov r1, r10
    mov r2, r4
    bl native_fn_0220f600
ov001_021f7544_L28c:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    beq ov001_021f7544_L2cc
    ldr r0, =0x0223989c
    ldr r7, [sp, #0x28]
    ldrsb r8, [r0, #43]
    ldr r5, =0x0223995c
    ldr r2, =0x022399b8
    add r3, r8, #1
    ldrh r1, [sp, #36]
    strb r7, [r5, r8]
    strb r3, [r0, #0x2b]
    str r10, [r2, r8, lsl #2]
    add r0, r10, #768
    strh r1, [r0, #74]
    b ov001_021f7544_L35c
ov001_021f7544_L2cc:
    ldr r0, [sp, #0x2c]
    cmp r0, #0
    beq ov001_021f7544_L338
    mov r0, r10
    mov r1, r4
    bl native_fn_021dc59c
    add r0, r10, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    beq ov001_021f7544_L35c
    bl native_fn_0205d790
    add r1, r10, #768
    mov r2, r0
    ldrh r0, [r1, #76]
    mov r1, r10
    bl native_fn_021eec7c
    mov r0, r10
    bl native_fn_021dc5d4
    mov r1, #0
    add r0, r10, #768
    strh r1, [r0, #76]
    str r1, [sp]
    ldrb r3, [r5, #0x1e]
    mov r0, r10
    mov r2, r4
    bl native_fn_021ee78c
    b ov001_021f7544_L35c
ov001_021f7544_L338:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    bne ov001_021f7544_L35c
    mov r1, #0
    str r1, [sp]
    ldrb r3, [r5, #0x1e]
    mov r0, r10
    mov r2, r4
    bl native_fn_021ee78c
ov001_021f7544_L35c:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    movne r0, #243
    bne ov001_021f7544_L3a4
    cmp r6, #0
    ldrne r0, [sp, #0x30]
    cmpne r0, #0
    moveq r0, #242
    beq ov001_021f7544_L3a4
    mov r0, r10
    mov r1, r4
    bl native_fn_021e13c8
    cmp r0, #0
    movne r0, #241
    bne ov001_021f7544_L3a4
    cmp r6, #20
    movge r0, #239
    movlt r0, #238
ov001_021f7544_L3a4:
    mov r1, #1
    bl native_fn_021f949c
ov001_021f7544_L3ac:
    ldr r0, [sp, #0x20]
    add sp, sp, #56
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
