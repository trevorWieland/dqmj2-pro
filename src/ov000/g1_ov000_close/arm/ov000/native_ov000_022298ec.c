/* ov000 row 0x022298ec: 1512 bytes.
 *
 * What it does: 375 instructions; 43 call(s) to 0x02062a10, 0x02062a10, 0x02229974, +40 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5dc -> constant 0x02247480 (image word 0x02247480)
 *   pool +0x5e0 -> constant 0x0224748c (image word 0x0224748c)
 *   pool +0x5e4 -> constant 0x0224748d (image word 0x0224748d)
 *   back edge +0x38 -> +0x20
 *   branch +0x7c -> +0xe0
 *   branch +0x90 -> +0xa4
 *   branch +0xa0 -> +0xd0
 *   branch +0xa8 -> +0xc0
 *   branch +0xbc -> +0xd0
 *   back edge +0xcc -> +0x88
 *   back edge +0xdc -> +0x74
 *   back edge +0xe8 -> +0x6c
 *   branch +0x124 -> +0x154
 *   branch +0x138 -> +0x148
 *   back edge +0x150 -> +0x128
 *   branch +0x184 -> +0x2e4
 *   branch +0x190 -> +0x2d0
 *   branch +0x1a4 -> +0x2d0
 *   branch +0x1b0 -> +0x250
 *   branch +0x1b8 -> +0x250
 *   branch +0x1e0 -> +0x210
 *   branch +0x1f4 -> +0x204
 *   back edge +0x20c -> +0x1e4
 *   branch +0x230 -> +0x250
 *   branch +0x24c -> +0x2d0
 *   branch +0x25c -> +0x2c4
 *   branch +0x278 -> +0x2c4
 *   branch +0x2a0 -> +0x2c4
 *   branch +0x2c0 -> +0x2d0
 *   back edge +0x2cc -> +0x19c
 *   back edge +0x2e0 -> +0x188
 *   branch +0x2f4 -> +0x454
 *   branch +0x300 -> +0x43c
 *   branch +0x358 -> +0x39c
 *   branch +0x36c -> +0x39c
 *   branch +0x380 -> +0x39c
 *   branch +0x398 -> +0x3bc
 *   back edge +0x3a8 -> +0x350
 *   back edge +0x3b8 -> +0x344
 *   branch +0x3c4 -> +0x43c
 *   branch +0x3d4 -> +0x3e8
 *   branch +0x3e4 -> +0x430
 *   branch +0x40c -> +0x43c
 *   branch +0x42c -> +0x43c
 *   back edge +0x438 -> +0x328
 *   back edge +0x450 -> +0x2f8
 *   branch +0x478 -> +0x4d4
 *   branch +0x48c -> +0x4ac
 *   branch +0x49c -> +0x4ac
 *   back edge +0x4a8 -> +0x490
 *   branch +0x4b0 -> +0x4d4
 *   back edge +0x4dc -> +0x470
 *   branch +0x4f0 -> +0x5c0
 *   branch +0x520 -> +0x548
 *   back edge +0x550 -> +0x514
 *   back edge +0x55c -> +0x50c
 *   branch +0x57c -> +0x590
 *   branch +0x58c -> +0x5a0
 *   back edge +0x5bc -> +0x4f4
 *   test +0x78 cmp r11, #0
 *   test +0x8c cmp r8, #0
 *   test +0xa4 cmp r8, r11
 *   test +0xc4 cmp r9, #10
 *   test +0xd4 cmp r5, #5
 *   test +0xe4 cmp r4, #2
 *   test +0x100 cmp r0, #1
 *   test +0x104 cmpeq r10, #1
 *   test +0x118 cmp r5, #0
 *   test +0x134 cmp r0, #0
 *   test +0x14c cmp r6, r5
 *   test +0x18c cmp r0, #0
 *   test +0x1a0 cmp r1, #0
 *   test +0x1ac cmp r0, r1
 *   test +0x1b4 cmp r10, #0
 *   test +0x1c4 cmp r0, #1
 *   test +0x1c8 cmpeq r10, #1
 *   test +0x1d8 cmp r5, #0
 *   test +0x1f0 cmp r0, #0
 *   test +0x208 cmp r8, r5
 *   test +0x22c cmp r0, #0
 *   test +0x258 cmp r1, r0
 *   test +0x274 cmp r2, r0
 *   test +0x29c cmp r0, #0
 *   test +0x2c8 cmp r7, #10
 *   test +0x2fc cmp r0, #0
 *   test +0x354 cmp r1, #0
 *   test +0x368 cmp r3, r1
 *   test +0x37c cmp r2, r1
 *   test +0x3a4 cmp r7, #5
 *   test +0x3b0 cmp r10, #2
 *   test +0x3c0 cmp r0, #0
 *   test +0x3d0 cmp r1, #6
 *   test +0x3e0 cmp r0, #0
 *   test +0x408 cmp r0, #0
 *   test +0x434 cmp r1, #6
 *   test +0x474 cmp r10, #0
 *   test +0x488 cmp r5, #0
 *   test +0x494 cmp r3, r10
 *   test +0x4a4 cmp r11, r0
 *   test +0x4ac cmp r4, #0
 *   test +0x4d8 cmp r1, #10
 *   test +0x4ec cmp r0, #0
 *   test +0x51c cmp r7, r0
 *   test +0x54c cmp r10, #5
 *   test +0x558 cmp r9, #2
 *   test +0x578 cmp r0, r1
 *   test +0x5b8 cmp r8, r0
 *   0 block transfer(s), 35 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022298ec; the literal pool and
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

extern void native_fn_02062a10(void);
extern void native_fn_02044d84(void);
extern void native_fn_020449d4(void);
extern void native_fn_0207abac(void);
extern void native_fn_02229ed4(void);
extern void native_fn_0207aa98(void);
extern void native_fn_0207ac98(void);
extern void native_fn_02008d78(void);
extern void native_fn_02025a70(void);
extern void native_fn_02025578(void);
extern void native_fn_02024e0c(void);
extern void native_fn_020259e8(void);


asm u32 native_ov000_022298ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    mov r5, r1
    str r2, [sp, #0x4]
    add r4, sp, #38
    mov r10, r3
    mov r2, #5
    mov r1, #0
ov000_022298ec_L20:
    strb r1, [r4]
    strb r1, [r4, #0x1]
    strb r1, [r4, #0x2]
    strb r1, [r4, #0x3]
    add r4, r4, #4
    subs r2, r2, #1
    bne ov000_022298ec_L20
    bl native_fn_02062a10
    add r1, r0, #122
    mov r0, r5
    str r1, [sp, #0x14]
    bl native_fn_02062a10
    mov r4, #0
    add r0, r0, #122
    str r0, [sp, #0x18]
    mov r1, r4
    add r0, sp, #38
    mov r3, r4
    add r2, sp, #20
ov000_022298ec_L6c:
    ldr r6, [r2, r4, lsl #2]
    mov r5, r3
ov000_022298ec_L74:
    ldrb r11, [r6]
    cmp r11, #0
    beq ov000_022298ec_Le0
    mov r9, r1
    mov r7, r0
ov000_022298ec_L88:
    ldrb r8, [r7]
    cmp r8, #0
    bne ov000_022298ec_La4
    strb r11, [r7]
    ldrb r8, [r6, #0x1]
    strb r8, [r7, #0x1]
    b ov000_022298ec_Ld0
ov000_022298ec_La4:
    cmp r8, r11
    bne ov000_022298ec_Lc0
    ldrb r9, [r7, #0x1]
    ldrb r8, [r6, #0x1]
    add r8, r9, r8
    strb r8, [r7, #0x1]
    b ov000_022298ec_Ld0
ov000_022298ec_Lc0:
    add r9, r9, #1
    cmp r9, #10
    add r7, r7, #2
    blt ov000_022298ec_L88
ov000_022298ec_Ld0:
    add r5, r5, #1
    cmp r5, #5
    add r6, r6, #2
    blt ov000_022298ec_L74
ov000_022298ec_Le0:
    add r4, r4, #1
    cmp r4, #2
    blt ov000_022298ec_L6c
    ldr r1, =0x02247480
    ldr r0, [sp, #0x4]
    mov r2, #0
    str r2, [r1]
    bl native_fn_02044d84
    cmp r0, #1
    cmpeq r10, #1
    moveq r5, #2
    ldr r0, [sp, #0x4]
    movne r5, r10
    bl native_fn_020449d4
    cmp r5, #0
    ldrb r4, [r0, #0x5f]
    mov r6, #0
    ble ov000_022298ec_L154
ov000_022298ec_L128:
    mov r0, r4
    bl native_fn_0207abac
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    beq ov000_022298ec_L148
    mov r0, r4
    bl native_fn_0207abac
    ldrb r4, [r0, #0x2]
ov000_022298ec_L148:
    add r6, r6, #1
    cmp r6, r5
    blt ov000_022298ec_L128
ov000_022298ec_L154:
    ldr r1, =0x02247480
    ldr r0, =0x0224748c
    ldr r5, [r1]
    mov r11, #0
    add r2, r5, #1
    strb r4, [r0, r5, lsl #1]
    ldr r3, =0x0224748d
    mov r0, r11
    strb r11, [r3, r5, lsl #1]
    str r2, [r1]
    bl native_fn_0207abac
    movs r6, r0
    beq ov000_022298ec_L2e4
ov000_022298ec_L188:
    ldrb r0, [r6, #0x1]
    cmp r0, #0
    beq ov000_022298ec_L2d0
    mov r7, #0
    add r4, sp, #38
ov000_022298ec_L19c:
    ldrb r1, [r4, r7, lsl #1]
    cmp r1, #0
    beq ov000_022298ec_L2d0
    ldrb r0, [r6]
    cmp r0, r1
    bne ov000_022298ec_L250
    cmp r10, #0
    beq ov000_022298ec_L250
    ldr r0, [sp, #0x4]
    bl native_fn_02044d84
    cmp r0, #1
    cmpeq r10, #1
    moveq r5, #2
    movne r5, r10
    mov r9, r11
    cmp r5, #0
    mov r8, #0
    ble ov000_022298ec_L210
ov000_022298ec_L1e4:
    mov r0, r9
    bl native_fn_0207abac
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    beq ov000_022298ec_L204
    mov r0, r9
    bl native_fn_0207abac
    ldrb r9, [r0, #0x2]
ov000_022298ec_L204:
    add r8, r8, #1
    cmp r8, r5
    blt ov000_022298ec_L1e4
ov000_022298ec_L210:
    ldr r0, =0x02247480
    str r9, [sp]
    ldr r3, [r0]
    ldr r2, =0x0224748c
    mov r0, r4
    mov r1, #10
    bl native_fn_02229ed4
    cmp r0, #0
    bne ov000_022298ec_L250
    ldr r0, =0x02247480
    ldr r1, =0x0224748c
    ldr r3, [r0]
    add r2, r3, #1
    str r2, [r0]
    strb r9, [r1, r3, lsl #1]
    b ov000_022298ec_L2d0
ov000_022298ec_L250:
    ldrb r1, [r6]
    ldrb r0, [r4, r7, lsl #1]
    cmp r1, r0
    bne ov000_022298ec_L2c4
    mov r0, r11
    bl native_fn_0207aa98
    add r1, r4, r7, lsl #1
    ldrb r2, [r0, #0x9]
    ldrb r0, [r1, #0x1]
    cmp r2, r0
    bhi ov000_022298ec_L2c4
    ldrb r2, [r6, #0x2]
    ldr r3, =0x02247480
    mov r0, r4
    str r2, [sp]
    ldr r2, =0x0224748c
    ldr r3, [r3]
    mov r1, #10
    bl native_fn_02229ed4
    cmp r0, #0
    bne ov000_022298ec_L2c4
    ldr r0, =0x02247480
    ldr r1, =0x0224748c
    ldr r3, [r0]
    add r2, r3, #1
    str r2, [r0]
    ldrb r0, [r6, #0x2]
    strb r0, [r1, r3, lsl #1]
    b ov000_022298ec_L2d0
ov000_022298ec_L2c4:
    add r7, r7, #1
    cmp r7, #10
    blt ov000_022298ec_L19c
ov000_022298ec_L2d0:
    add r11, r11, #1
    mov r0, r11
    bl native_fn_0207abac
    movs r6, r0
    bne ov000_022298ec_L188
ov000_022298ec_L2e4:
    mov r0, #0
    str r0, [sp, #0xc]
    bl native_fn_0207ac98
    movs r4, r0
    beq ov000_022298ec_L454
ov000_022298ec_L2f8:
    ldrh r0, [r4]
    cmp r0, #0
    beq ov000_022298ec_L43c
    add r0, sp, #28
    mov r1, #0
    mov r2, #10
    bl native_fn_02008d78
    mov r0, #0
    str r0, [sp, #0x8]
    add r5, sp, #20
    mov r11, r0
    add r6, sp, #28
ov000_022298ec_L328:
    mov r0, #0
    str r0, [sp, #0x10]
    mov r10, r0
    mov r8, r0
    ldr r0, [sp, #0x8]
    mov r12, r0, lsl #1
    add r0, r4, r0, lsl #1
ov000_022298ec_L344:
    ldr lr, [r5, r10, lsl #2]
    mov r7, r11
    add r9, r6, r8
ov000_022298ec_L350:
    ldrb r1, [r9]
    cmp r1, #0
    bne ov000_022298ec_L39c
    ldrh r3, [r4, r12]
    mov r2, r7, lsl #1
    ldrb r1, [lr, r7, lsl #1]
    cmp r3, r1
    bne ov000_022298ec_L39c
    add r1, lr, r2
    ldrb r1, [r1, #0x1]
    ldrh r2, [r0, #12]
    cmp r2, r1
    bgt ov000_022298ec_L39c
    mov r0, #1
    add r2, r10, r10, lsl #2
    add r1, r6, r7
    str r0, [sp, #0x10]
    strb r0, [r2, r1]
    b ov000_022298ec_L3bc
ov000_022298ec_L39c:
    add r9, r9, #1
    add r7, r7, #1
    cmp r7, #5
    blt ov000_022298ec_L350
    add r10, r10, #1
    cmp r10, #2
    add r8, r8, #5
    blt ov000_022298ec_L344
ov000_022298ec_L3bc:
    ldr r0, [sp, #0x10]
    cmp r0, #0
    beq ov000_022298ec_L43c
    ldr r0, [sp, #0x8]
    add r1, r0, #1
    cmp r1, #6
    bge ov000_022298ec_L3e8
    add r0, r4, r0, lsl #1
    ldrh r0, [r0, #2]
    cmp r0, #0
    bne ov000_022298ec_L430
ov000_022298ec_L3e8:
    ldrh r2, [r4, #24]
    ldr r1, =0x02247480
    add r0, sp, #38
    str r2, [sp]
    ldr r3, [r1]
    ldr r2, =0x0224748c
    mov r1, #10
    bl native_fn_02229ed4
    cmp r0, #0
    bne ov000_022298ec_L43c
    ldr r0, =0x02247480
    ldr r1, =0x0224748c
    ldr r3, [r0]
    add r2, r3, #1
    str r2, [r0]
    ldrh r0, [r4, #24]
    strb r0, [r1, r3, lsl #1]
    b ov000_022298ec_L43c
ov000_022298ec_L430:
    str r1, [sp, #0x8]
    cmp r1, #6
    blt ov000_022298ec_L328
ov000_022298ec_L43c:
    ldr r0, [sp, #0xc]
    add r0, r0, #1
    str r0, [sp, #0xc]
    bl native_fn_0207ac98
    movs r4, r0
    bne ov000_022298ec_L2f8
ov000_022298ec_L454:
    ldr r2, =0x02247480
    mov r1, #0
    ldr r7, =0x0224748c
    ldr r5, [r2]
    mov r6, #1
    mov r8, r1
    add r9, sp, #38
ov000_022298ec_L470:
    ldrb r10, [r9, r1, lsl #1]
    cmp r10, #0
    beq ov000_022298ec_L4d4
    mov r4, r8
    mov r11, r8
    mov r0, r5
    cmp r5, #0
    ble ov000_022298ec_L4ac
ov000_022298ec_L490:
    ldrb r3, [r7, r11, lsl #1]
    cmp r3, r10
    moveq r4, r6
    beq ov000_022298ec_L4ac
    add r11, r11, #1
    cmp r11, r0
    blt ov000_022298ec_L490
ov000_022298ec_L4ac:
    cmp r4, #0
    bne ov000_022298ec_L4d4
    add r3, r9, r1, lsl #1
    ldrb r4, [r9, r1, lsl #1]
    ldrb r3, [r3, #0x1]
    add r5, r5, #1
    strb r4, [r7, r0, lsl #1]
    add r0, r7, r0, lsl #1
    str r5, [r2]
    strb r3, [r0, #0x1]
ov000_022298ec_L4d4:
    add r1, r1, #1
    cmp r1, #10
    blt ov000_022298ec_L470
    ldr r0, =0x02247480
    mov r8, #0
    ldr r0, [r0]
    cmp r0, #0
    ble ov000_022298ec_L5c0
ov000_022298ec_L4f4:
    ldr r0, =0x0224748c
    mov r5, #0
    ldrb r7, [r0, r8, lsl #1]
    mov r9, r5
    mov r4, #1073741824
    add r11, sp, #20
ov000_022298ec_L50c:
    ldr r6, [r11, r9, lsl #2]
    mov r10, #0
ov000_022298ec_L514:
    ldrb r0, [r6, r10, lsl #1]
    mov r1, r10, lsl #1
    cmp r7, r0
    bne ov000_022298ec_L548
    add r0, r6, r1
    ldrb r0, [r0, #0x1]
    bl native_fn_02025a70
    mov r1, r4
    bl native_fn_02025578
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r5, r0
ov000_022298ec_L548:
    add r10, r10, #1
    cmp r10, #5
    blt ov000_022298ec_L514
    add r9, r9, #1
    cmp r9, #2
    blt ov000_022298ec_L50c
    mov r0, r7
    bl native_fn_0207aa98
    mov r4, r0
    mov r0, r5
    bl native_fn_020259e8
    ldrb r1, [r4, #0x9]
    cmp r0, r1
    bhs ov000_022298ec_L590
    mov r0, r5
    bl native_fn_020259e8
    and r2, r0, #255
    b ov000_022298ec_L5a0
ov000_022298ec_L590:
    ldr r0, =0x0224748c
    ldrb r0, [r0, r8, lsl #1]
    bl native_fn_0207aa98
    ldrb r2, [r0, #0x9]
ov000_022298ec_L5a0:
    ldr r0, =0x02247480
    ldr r1, =0x0224748c
    ldr r0, [r0]
    add r1, r1, r8, lsl #1
    add r8, r8, #1
    strb r2, [r1, #0x1]
    cmp r8, r0
    blt ov000_022298ec_L4f4
ov000_022298ec_L5c0:
    ldr r1, [sp, #0x60]
    ldr r2, =0x0224748c
    ldr r0, =0x02247480
    str r2, [r1]
    ldr r0, [r0]
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
