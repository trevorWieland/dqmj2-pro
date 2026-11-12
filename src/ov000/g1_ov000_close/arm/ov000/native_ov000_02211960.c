/* ov000 row 0x02211960: 1192 bytes.
 *
 * What it does: 294 instructions; 21 call(s) to 0x021d8a50, 0x0202859c, 0x02211ddc, +18 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x498 -> constant 0x0224157c (image word 0x0224157c)
 *   pool +0x49c -> constant 0x057e4000 (image word 0x057e4000)
 *   pool +0x4a0 -> native_data_0222badc (image word 0x0222badc)
 *   pool +0x4a4 -> constant 0x02240ddc (image word 0x02240ddc)
 *   branch +0x14 -> +0x20
 *   branch +0x1c -> +0x28
 *   branch +0x3c -> +0x484
 *   branch +0x48 -> +0x47c
 *   branch +0x64 -> +0x47c
 *   branch +0x78 -> +0x110
 *   branch +0xc4 -> +0x110
 *   branch +0xcc -> +0x110
 *   branch +0xec -> +0x110
 *   branch +0x118 -> +0x1c4
 *   branch +0x12c -> +0x16c
 *   branch +0x178 -> +0x1c4
 *   branch +0x180 -> +0x1c4
 *   branch +0x1a0 -> +0x1c4
 *   branch +0x1cc -> +0x278
 *   branch +0x1e0 -> +0x220
 *   branch +0x22c -> +0x278
 *   branch +0x234 -> +0x278
 *   branch +0x254 -> +0x278
 *   branch +0x280 -> +0x33c
 *   branch +0x320 -> +0x33c
 *   branch +0x350 -> +0x478
 *   branch +0x36c -> +0x37c
 *   branch +0x380 -> +0x478
 *   back edge +0x488 -> +0x40
 *   test +0x0c cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x58 cmpne r0, #0
 *   test +0x60 cmpne r0, #0
 *   test +0x74 cmp r0, #0
 *   test +0xe8 cmp r0, #0
 *   test +0x108 cmp r3, r2
 *   test +0x114 cmp r0, #0
 *   test +0x19c cmp r0, #0
 *   test +0x1bc cmp r3, r2
 *   test +0x1c8 cmp r0, #0
 *   test +0x250 cmp r0, #0
 *   test +0x270 cmp r2, r1
 *   test +0x27c cmp r0, #0
 *   test +0x31c cmp r7, r0
 *   test +0x34c cmp r7, r4
 *   test +0x358 cmp r0, #0
 *   test +0x364 cmp r0, #0
 *   test +0x37c cmp r1, r4
 *   test +0x484 cmp r5, #24
 *   4 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211960; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_0202859c(void);
extern void native_fn_020413fc(void);
extern void native_fn_021dfbd4(void);
extern void native_fn_02029964(void);
extern void native_fn_021dfca4(void);
extern void native_fn_02029834(void);
extern void native_fn_021dfd48(void);
extern void native_fn_020281b8(void);
extern void native_fn_022115cc(void);
extern u8 native_data_0222badc[];
extern void native_fn_0202bd74(void);
extern void native_fn_02028fac(void);
extern void native_fn_02000ce8(void);
extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);


asm u32 native_ov000_02211960 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    mov r6, #0
    cmp r0, #0
    mov r0, r6
    bne ov000_02211960_L20
    bl native_fn_021d8a50
    b ov000_02211960_L28
ov000_02211960_L20:
    mov r1, r6
    bl native_fn_0202859c
ov000_02211960_L28:
    mov r10, r0
    ldr r9, =0x0224157c
    mov r5, #0
    mvn r4, #0
    ldr r11, =0x057e4000
    b ov000_02211960_L484
ov000_02211960_L40:
    ldrsh r0, [r9]
    cmp r0, #0
    ble ov000_02211960_L47c
    ldrb r0, [r9, #0xa]
    cmp r0, #0
    ldrneb r0, [r9, #0x9]
    cmpne r0, #0
    ldrneb r0, [r9, #0xc]
    cmpne r0, #0
    beq ov000_02211960_L47c
    mov r8, r4
    mov r7, r4
    ldrb r0, [r9, #0x4]
    cmp r0, #0
    beq ov000_02211960_L110
    ldr r1, [r10, #0x8]
    ldr r0, [r9, #0x8c]
    ldr r2, [r10]
    sub r3, r1, r0
    ldr r0, [r9, #0x84]
    ldr r1, [r10, #0x4]
    sub r2, r2, r0
    ldr r0, [r9, #0x88]
    sub r0, r1, r0
    smull r7, r1, r0, r0
    smlal r7, r1, r2, r2
    smlal r7, r1, r3, r3
    mov r8, r7, lsr #12
    orr r8, r8, r1, lsl #20
    subs r0, r8, r11
    mov r7, r1, asr #12
    mov r0, #0
    sbcs r0, r7, r0
    bge ov000_02211960_L110
    movs r0, #1
    beq ov000_02211960_L110
    add r0, r9, #20
    mov r1, #4096
    mov r2, #0
    bl native_fn_020413fc
    ldrb r0, [r9, #0x4]
    bl native_fn_021dfbd4
    cmp r0, #0
    blt ov000_02211960_L110
    ldr r1, [r9, #0x74]
    ldr r2, [r1, #0x8]
    ldr r3, [r1]
    ldrh r2, [r2, #4]
    mov r2, r2, lsl #12
    sub r2, r2, #1
    cmp r3, r2
    strge r0, [r1]
ov000_02211960_L110:
    ldrb r0, [r9, #0x5]
    cmp r0, #0
    beq ov000_02211960_L1c4
    mov r0, #0
    subs r0, r8, r0
    mov r0, #0
    sbcs r0, r7, r0
    bge ov000_02211960_L16c
    ldr r1, [r10, #0x8]
    ldr r0, [r9, #0x8c]
    ldr r2, [r10]
    sub r3, r1, r0
    ldr r0, [r9, #0x84]
    ldr r1, [r10, #0x4]
    sub r2, r2, r0
    ldr r0, [r9, #0x88]
    sub r0, r1, r0
    smull r7, r1, r0, r0
    smlal r7, r1, r2, r2
    smlal r7, r1, r3, r3
    mov r8, r7, lsr #12
    mov r7, r1, asr #12
    orr r8, r8, r1, lsl #20
ov000_02211960_L16c:
    subs r0, r8, r11
    mov r0, #0
    sbcs r0, r7, r0
    bge ov000_02211960_L1c4
    movs r0, #1
    beq ov000_02211960_L1c4
    add r0, r9, #20
    mov r1, #4096
    mov r2, #0
    bl native_fn_02029964
    ldrb r0, [r9, #0x5]
    bl native_fn_021dfca4
    cmp r0, #0
    blt ov000_02211960_L1c4
    ldr r1, [r9, #0x80]
    ldr r2, [r1, #0x8]
    ldr r3, [r1]
    ldrh r2, [r2, #4]
    mov r2, r2, lsl #12
    sub r2, r2, #1
    cmp r3, r2
    strge r0, [r1]
ov000_02211960_L1c4:
    ldrb r0, [r9, #0x6]
    cmp r0, #0
    beq ov000_02211960_L278
    mov r0, #0
    subs r0, r8, r0
    mov r0, #0
    sbcs r0, r7, r0
    bge ov000_02211960_L220
    ldr r1, [r10, #0x8]
    ldr r0, [r9, #0x8c]
    ldr r2, [r10]
    sub r3, r1, r0
    ldr r0, [r9, #0x84]
    ldr r1, [r10, #0x4]
    sub r2, r2, r0
    ldr r0, [r9, #0x88]
    sub r0, r1, r0
    smull r7, r1, r0, r0
    smlal r7, r1, r2, r2
    smlal r7, r1, r3, r3
    mov r8, r7, lsr #12
    mov r7, r1, asr #12
    orr r8, r8, r1, lsl #20
ov000_02211960_L220:
    subs r0, r8, r11
    mov r0, #0
    sbcs r0, r7, r0
    bge ov000_02211960_L278
    movs r0, #1
    beq ov000_02211960_L278
    add r0, r9, #20
    mov r1, #4096
    mov r2, #0
    bl native_fn_02029834
    ldrb r0, [r9, #0x6]
    bl native_fn_021dfd48
    cmp r0, #0
    blt ov000_02211960_L278
    ldr r3, [r9, #0x7c]
    ldr r1, [r3, #0x8]
    ldr r2, [r3]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r2, r1
    strge r0, [r3]
ov000_02211960_L278:
    ldrb r0, [r9, #0xb]
    cmp r0, #0
    beq ov000_02211960_L33c
    ldr r2, [r9, #0x84]
    ldr r1, [r9, #0x144]
    add r0, sp, #60
    sub r1, r2, r1
    str r1, [r9, #0x84]
    ldr r2, [r9, #0x88]
    ldr r1, [r9, #0x148]
    sub r1, r2, r1
    str r1, [r9, #0x88]
    ldr r2, [r9, #0x8c]
    ldr r1, [r9, #0x14c]
    sub r1, r2, r1
    str r1, [r9, #0x8c]
    ldr r2, [r9, #0x130]
    ldr r7, [r9, #0x13c]
    ldr r3, [r9, #0x12c]
    sub r7, r2, r7
    ldr r1, [r9, #0x138]
    str r7, [sp, #0x40]
    sub r1, r3, r1
    ldr r7, [r9, #0x84]
    str r1, [sp, #0x3c]
    sub r3, r3, r7
    str r3, [sp, #0x30]
    ldr r7, [r9, #0x88]
    ldr r1, [r9, #0x134]
    ldr r8, [r9, #0x140]
    sub r2, r2, r7
    sub r8, r1, r8
    ldr r3, [r9, #0x8c]
    str r8, [sp, #0x44]
    sub r1, r1, r3
    str r2, [sp, #0x34]
    str r1, [sp, #0x38]
    bl native_fn_020281b8
    mov r7, r0
    add r0, sp, #48
    bl native_fn_020281b8
    cmp r7, r0
    bge ov000_02211960_L33c
    add r0, r9, #312
    add r3, r9, #132
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    strb r0, [r9, #0xb]
ov000_02211960_L33c:
    ldrsh r0, [r9]
    ldrsh r1, [r9, #2]
    bl native_fn_022115cc
    mov r7, r0
    cmp r7, r4
    beq ov000_02211960_L478
    ldr r0, [r9, #0x24]
    cmp r0, #0
    addne r0, r0, #64
    moveq r0, #0
    cmp r0, #0
    moveq r1, r4
    beq ov000_02211960_L37c
    ldr r1, =native_data_0222badc
    bl native_fn_0202bd74
    mov r1, r0
ov000_02211960_L37c:
    cmp r1, r4
    beq ov000_02211960_L478
    ldr r2, [r9, #0x74]
    add r0, r9, #20
    ldr r2, [r2]
    add r3, sp, #36
    bl native_fn_02028fac
    ldr r1, [r9, #0x90]
    ldr r0, [sp, #0x24]
    ldr r2, [sp, #0x28]
    smull r8, r3, r1, r0
    mov r0, #2048
    adds r8, r8, r0
    mov r0, #0
    adc r0, r3, r0
    mov r3, r8, lsr #12
    orr r3, r3, r0, lsl #20
    str r3, [sp, #0x24]
    smull r3, r2, r1, r2
    mov r0, #2048
    adds r3, r3, r0
    mov r0, #0
    adc r0, r2, r0
    mov r2, r3, lsr #12
    orr r2, r2, r0, lsl #20
    str r2, [sp, #0x28]
    ldr r2, [sp, #0x2c]
    add r0, sp, #0
    smull r3, r2, r1, r2
    adds r3, r3, #2048
    adc r1, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r1, lsl #20
    str r2, [sp, #0x2c]
    bl native_fn_02000ce8
    ldr r1, [r9, #0xa0]
    add r0, sp, #0
    bl native_fn_02028044
    add r0, sp, #36
    add r1, sp, #0
    mov r2, r0
    bl native_fn_0200103c
    ldr r0, =0x02240ddc
    mov r1, #96
    mla r3, r7, r1, r0
    ldr r1, [sp, #0x24]
    ldr r0, [r9, #0x84]
    ldr r2, [sp, #0x28]
    add r0, r1, r0
    str r0, [sp, #0x24]
    ldr r0, [r9, #0x88]
    ldr r1, [sp, #0x2c]
    add r0, r2, r0
    str r0, [sp, #0x28]
    ldr r0, [r9, #0x8c]
    add r8, r3, #20
    add r0, r1, r0
    str r0, [sp, #0x2c]
    add r0, sp, #36
    ldmia r0, {r0, r1, r2}
    stmia r8, {r0, r1, r2}
    ldr r7, [r9, #0x118]
    str r7, [r3, #0x18]
ov000_02211960_L478:
    add r6, r6, #1
ov000_02211960_L47c:
    add r5, r5, #1
    add r9, r9, #360
ov000_02211960_L484:
    cmp r5, #24
    blt ov000_02211960_L40
    mov r0, r6
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
