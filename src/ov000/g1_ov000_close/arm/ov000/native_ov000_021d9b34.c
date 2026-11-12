/* ov000 row 0x021d9b34: 1368 bytes.
 *
 * What it does: 338 instructions; 21 call(s) to 0x02025a70, 0x02024e0c, 0x02025a70, +18 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x548 -> constant 0x02231bd4 (image word 0x02231bd4)
 *   pool +0x54c -> constant 0x04000358 (image word 0x04000358)
 *   pool +0x550 -> constant 0x02231be0 (image word 0x02231be0)
 *   pool +0x554 -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x20 -> +0x448
 *   branch +0x2c -> +0x44
 *   branch +0x40 -> +0x50
 *   branch +0x5c -> +0x74
 *   branch +0x70 -> +0x80
 *   branch +0xe0 -> +0x20c
 *   back edge +0x1cc -> +0x1a4
 *   back edge +0x214 -> +0xd4
 *   back edge +0x25c -> +0x23c
 *   branch +0x2ac -> +0x2f0
 *   branch +0x2c0 -> +0x2d4
 *   branch +0x2ec -> +0x324
 *   branch +0x350 -> +0x3cc
 *   back edge +0x3c4 -> +0x35c
 *   branch +0x444 -> +0x53c
 *   branch +0x454 -> +0x46c
 *   branch +0x474 -> +0x4b8
 *   branch +0x4b4 -> +0x53c
 *   branch +0x4bc -> +0x500
 *   branch +0x4fc -> +0x53c
 *   test +0x18 cmp r2, r4
 *   test +0xdc cmp r0, #0
 *   test +0x1c8 cmp r1, #3
 *   test +0x210 cmp r4, #4
 *   test +0x248 cmp r5, #3
 *   test +0x2a8 cmp r1, #1
 *   test +0x2bc cmp r1, #0
 *   test +0x2e0 cmp r1, #0
 *   test +0x2fc cmp r1, #0
 *   test +0x314 cmp r1, #0
 *   test +0x344 cmp r0, #0
 *   test +0x34c cmpne r0, #0
 *   test +0x394 cmp r8, #8
 *   test +0x450 cmp r0, #0
 *   test +0x470 cmp r0, #0
 *   test +0x480 cmp r1, #0
 *   test +0x494 cmp r1, #0
 *   test +0x4a8 cmp r1, #0
 *   test +0x4b8 cmp r0, #1
 *   test +0x4c8 cmp r1, #0
 *   test +0x4dc cmp r1, #0
 *   test +0x4f0 cmp r1, #0
 *   test +0x508 cmp r1, #0
 *   test +0x51c cmp r1, #0
 *   test +0x530 cmp r1, #0
 *   0 block transfer(s), 32 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d9b34; the literal pool and
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

extern void native_fn_02025a70(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_0200235c(void);
extern void native_fn_021dfee8(void);
extern void native_fn_021dfe5c(void);
extern void native_fn_021dfe80(void);
extern void native_fn_020046c8(void);
extern void native_fn_02029c88(void);
extern void native_fn_021d99ac(void);


asm u32 native_ov000_021d9b34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #56
    mov r4, r1
    mov r6, r0
    mov r0, #0
    str r3, [sp]
    cmp r2, r4
    str r0, [sp, #0x10]
    beq ov000_021d9b34_L448
    subs r0, r2, r4
    mov r0, r0, lsl #12
    beq ov000_021d9b34_L44
    bl native_fn_02025a70
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021d9b34_L50
ov000_021d9b34_L44:
    bl native_fn_02025a70
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021d9b34_L50:
    mov r5, r0
    subs r0, r6, r4
    mov r0, r0, lsl #12
    beq ov000_021d9b34_L74
    bl native_fn_02025a70
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021d9b34_L80
ov000_021d9b34_L74:
    bl native_fn_02025a70
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021d9b34_L80:
    bl native_fn_020259b4
    mov r4, r0
    mov r0, r5
    bl native_fn_020259b4
    mov r1, r0
    mov r0, r4
    bl native_fn_0200235c
    ldr r1, [sp, #0x60]
    mov r6, r0
    str r1, [sp, #0x4]
    ldr r3, =0x02231bd4
    ldr r1, [sp]
    mov r5, r6, asr #31
    ldr r2, [r3, r1, lsl #2]
    ldr r1, [sp, #0x4]
    add r0, r2, #4
    ldr r1, [r3, r1, lsl #2]
    str r0, [sp, #0xc]
    add r0, r1, #4
    str r0, [sp, #0x8]
    mov r4, #0
ov000_021d9b34_Ld4:
    mov r0, r4
    bl native_fn_021dfee8
    cmp r0, #0
    beq ov000_021d9b34_L20c
    ldr r0, [sp, #0xc]
    add lr, sp, #36
    add r3, r0, r4, lsl #4
    ldr r0, [sp, #0x8]
    ldr r11, [r3, #0x4]
    add r12, r0, r4, lsl #4
    ldr r0, [sp, #0xc]
    ldr r9, [r12, #0x8]
    ldr r0, [r0, r4, lsl #4]
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x8]
    ldr r1, [r0, r4, lsl #4]
    ldr r0, [sp, #0x14]
    sub r2, r1, r0
    ldr r1, [r12, #0x4]
    mov r0, r2, asr #31
    sub r7, r1, r11
    mov r8, r7, asr #31
    str r8, [sp, #0x18]
    ldr r8, [r3, #0x8]
    mov r1, #0
    str r8, [sp, #0x1c]
    sub r8, r9, r8
    mov r9, r8, asr #31
    str r9, [sp, #0x20]
    umull r10, r9, r6, r2
    mla r9, r6, r0, r9
    adds r0, r10, #2048
    mla r9, r5, r2, r9
    adc r2, r9, #0
    mov r0, r0, lsr #12
    orr r0, r0, r2, lsl #20
    ldr r2, [sp, #0x18]
    umull r10, r9, r6, r7
    mla r9, r6, r2, r9
    adds r2, r10, #2048
    mla r9, r5, r7, r9
    adc r7, r9, #0
    mov r2, r2, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x20]
    umull r10, r9, r6, r8
    mla r9, r6, r7, r9
    adds r7, r10, #2048
    mla r9, r5, r8, r9
    adc r8, r9, #0
    mov r7, r7, lsr #12
    orr r7, r7, r8, lsl #20
ov000_021d9b34_L1a4:
    ldrb r8, [r3, #0xc]
    ldrb r9, [r12, #0xc]
    add r3, r3, #1
    add r12, r12, #1
    sub r9, r9, r8
    mul r9, r6, r9
    add r8, r8, r9, asr #12
    strb r8, [lr], #1
    add r1, r1, #1
    cmp r1, #3
    blt ov000_021d9b34_L1a4
    ldr r1, [sp, #0x14]
    ldr r3, [sp, #0x1c]
    add r1, r1, r0
    mov r0, r4
    add r2, r11, r2
    add r3, r3, r7
    bl native_fn_021dfe5c
    ldrb r1, [sp, #0x24]
    ldrb r2, [sp, #0x25]
    ldrb r3, [sp, #0x26]
    mov r0, r4
    bl native_fn_021dfe80
    ldr r0, [sp, #0x10]
    add r0, r0, #1
    str r0, [sp, #0x10]
ov000_021d9b34_L20c:
    add r4, r4, #1
    cmp r4, #4
    blt ov000_021d9b34_Ld4
    ldr r3, =0x02231bd4
    ldr r1, [sp]
    add r0, sp, #36
    ldr r2, [r3, r1, lsl #2]
    ldr r1, [sp, #0x4]
    mov r5, #0
    ldr r1, [r3, r1, lsl #2]
    add r3, r2, #68
    add r4, r1, #68
ov000_021d9b34_L23c:
    ldrb r2, [r3, r5]
    ldrb r1, [r4, r5]
    add r5, r5, #1
    cmp r5, #3
    sub r1, r1, r2
    mul r1, r6, r1
    add r1, r2, r1, asr #12
    strb r1, [r0], #1
    blt ov000_021d9b34_L23c
    ldrb r2, [r3, #0x3]
    ldrb r1, [r4, #0x3]
    ldr r0, [sp, #0x60]
    ldrb r4, [sp, #0x24]
    sub r1, r1, r2
    mul r1, r6, r1
    ldrb r3, [sp, #0x25]
    add r1, r2, r1, asr #12
    and r2, r1, #255
    sub r1, r0, #1
    ldrb r5, [sp, #0x26]
    orr r0, r4, r3, lsl #5
    mov r3, r2, lsl #16
    orr r0, r0, r5, lsl #10
    mov r0, r0, lsl #16
    ldr r2, =0x04000358
    orr r0, r3, r0, lsr #16
    str r0, [r2]
    cmp r1, #1
    bhi ov000_021d9b34_L2f0
    ldr r1, =0x02231be0
    ldr r0, [sp]
    ldr r1, [r1, r0, lsl #2]
    cmp r1, #0
    beq ov000_021d9b34_L2d4
    rsb r0, r6, #4096
    rsb r0, r0, r0, lsl #5
    mov r0, r0, asr #12
    strb r0, [r1, #0x172]
ov000_021d9b34_L2d4:
    ldr r1, =0x02231be0
    ldr r0, [sp, #0x4]
    ldr r1, [r1, r0, lsl #2]
    cmp r1, #0
    movne r0, #31
    strneb r0, [r1, #0x172]
    b ov000_021d9b34_L324
ov000_021d9b34_L2f0:
    ldr r1, =0x02231be0
    ldr r0, [sp]
    ldr r1, [r1, r0, lsl #2]
    cmp r1, #0
    movne r0, #31
    strneb r0, [r1, #0x172]
    ldr r1, =0x02231be0
    ldr r0, [sp, #0x4]
    ldr r1, [r1, r0, lsl #2]
    cmp r1, #0
    rsbne r0, r6, r6, lsl #5
    movne r0, r0, asr #12
    strneb r0, [r1, #0x172]
ov000_021d9b34_L324:
    ldr r1, =0x02231bd4
    ldr r0, [sp]
    ldr r2, [r1, r0, lsl #2]
    ldr r0, [sp, #0x4]
    add r5, r2, #116
    ldr r1, [r1, r0, lsl #2]
    ldrb r0, [r5, #0x10]
    add r7, r1, #116
    cmp r0, #0
    ldrneb r0, [r7, #0x10]
    cmpne r0, #0
    beq ov000_021d9b34_L3cc
    mov r8, #0
    add r0, sp, #40
ov000_021d9b34_L35c:
    mov r4, r8, lsl #1
    ldrh r3, [r7, r4]
    ldrh r1, [r5, r4]
    add r8, r8, #1
    mov r2, r3, asr #1
    mov r9, r1, asr #1
    and r9, r9, #15
    and r2, r2, #15
    add r10, r9, r2
    mov r9, r1, asr #6
    mov r1, r1, asr #11
    and r2, r1, #15
    and r1, r10, #255
    and r9, r9, #15
    cmp r8, #8
    mov r10, r3, asr #11
    and r10, r10, #15
    add r2, r2, r10
    and r2, r2, #255
    mov r3, r3, asr #6
    and r3, r3, #15
    add r3, r9, r3
    and r3, r3, #255
    orr r1, r1, r3, lsl #5
    orr r1, r1, r2, lsl #10
    strh r1, [r0, r4]
    blt ov000_021d9b34_L35c
    bl native_fn_020046c8
ov000_021d9b34_L3cc:
    ldr r1, =0x02231bd4
    ldr r0, [sp]
    ldr r2, [r1, r0, lsl #2]
    ldr r0, [sp, #0x4]
    ldrb r3, [r2, #0x88]
    ldr r1, [r1, r0, lsl #2]
    ldrb r0, [r1, #0x88]
    sub r0, r0, r3
    mul r0, r6, r0
    add r0, r3, r0, asr #12
    strb r0, [sp, #0x24]
    ldrb r4, [r2, #0x89]
    ldrb r3, [r1, #0x89]
    and r0, r0, #255
    sub r3, r3, r4
    mul r3, r6, r3
    add r4, r4, r3, asr #12
    strb r4, [sp, #0x25]
    ldrb r3, [r2, #0x8a]
    ldrb r2, [r1, #0x8a]
    and r1, r4, #255
    sub r2, r2, r3
    mul r2, r6, r2
    add r3, r3, r2, asr #12
    and r2, r3, #255
    strb r3, [sp, #0x26]
    bl native_fn_02029c88
    ldr r0, =0x0223142c
    mov r1, #1
    strb r1, [r0, #0x7c1]
    b ov000_021d9b34_L53c
ov000_021d9b34_L448:
    ldr r0, =0x0223142c
    ldrb r0, [r0, #0x7c1]
    cmp r0, #0
    beq ov000_021d9b34_L46c
    mov r0, r3
    bl native_fn_021d99ac
    ldr r0, =0x0223142c
    mov r1, #0
    strb r1, [r0, #0x7c1]
ov000_021d9b34_L46c:
    ldr r0, [sp]
    cmp r0, #0
    bne ov000_021d9b34_L4b8
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b4]
    cmp r1, #0
    movne r0, #31
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b8]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7bc]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    b ov000_021d9b34_L53c
ov000_021d9b34_L4b8:
    cmp r0, #1
    bne ov000_021d9b34_L500
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b4]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b8]
    cmp r1, #0
    movne r0, #31
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7bc]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    b ov000_021d9b34_L53c
ov000_021d9b34_L500:
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b4]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7b8]
    cmp r1, #0
    movne r0, #0
    strneb r0, [r1, #0x172]
    ldr r0, =0x0223142c
    ldr r1, [r0, #0x7bc]
    cmp r1, #0
    movne r0, #31
    strneb r0, [r1, #0x172]
ov000_021d9b34_L53c:
    ldr r0, [sp, #0x10]
    add sp, sp, #56
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
