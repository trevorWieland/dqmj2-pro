/* ov001 row 0x021edf1c: 1220 bytes.
 *
 * What it does: 303 instructions; 40 call(s) to 0x021db8d0, 0x021f82d8, 0x021dca04, +37 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 40 calls (303 instructions, 40 calls, 36 branches, 16 back edges, 2 literal slots).
 *
 *   pool +0x4bc -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x4c0 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x14 -> +0x60
 *   branch +0x24 -> +0x40
 *   branch +0x5c -> +0x4b0
 *   branch +0x64 -> +0x80
 *   branch +0x7c -> +0x4b0
 *   branch +0x84 -> +0x258
 *   branch +0xc4 -> +0xd8
 *   branch +0xf8 -> +0x118
 *   branch +0x11c -> +0x248
 *   branch +0x130 -> +0x190
 *   branch +0x18c -> +0x230
 *   branch +0x1ec -> +0x214
 *   branch +0x210 -> +0x220
 *   branch +0x244 -> +0x4b0
 *   branch +0x254 -> +0x4b0
 *   branch +0x25c -> +0x280
 *   branch +0x27c -> +0x4b0
 *   branch +0x284 -> +0x390
 *   branch +0x2b8 -> +0x384
 *   branch +0x324 -> +0x34c
 *   branch +0x348 -> +0x358
 *   branch +0x380 -> +0x4b0
 *   branch +0x38c -> +0x4b0
 *   branch +0x394 -> +0x3b8
 *   branch +0x3b4 -> +0x4b0
 *   branch +0x3bc -> +0x41c
 *   branch +0x3d0 -> +0x3e4
 *   branch +0x3e0 -> +0x4b0
 *   branch +0x3f8 -> +0x40c
 *   branch +0x408 -> +0x4b0
 *   branch +0x418 -> +0x4b0
 *   branch +0x420 -> +0x464
 *   branch +0x434 -> +0x4b0
 *   branch +0x450 -> +0x4b0
 *   branch +0x460 -> +0x4b0
 *   branch +0x468 -> +0x4b0
 *   branch +0x47c -> +0x4a4
 *   branch +0x48c -> +0x4a4
 *   branch +0x4a0 -> +0x4b0
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x60 cmp r1, #5
 *   test +0x80 cmp r1, #10
 *   test +0xc0 cmp r0, #237
 *   test +0xf4 cmp r7, #0
 *   test +0x10c cmp r0, #0
 *   test +0x118 cmp r5, #0
 *   test +0x120 cmp r6, #100
 *   test +0x12c tst r0, #32
 *   test +0x1e8 cmp r6, #0
 *   test +0x258 cmp r1, #15
 *   test +0x26c cmp r1, #30
 *   test +0x280 cmp r1, #20
 *   test +0x2b4 cmp r1, #121
 *   test +0x2e0 cmp r1, r0
 *   test +0x320 cmp r0, #0
 *   test +0x390 cmp r1, #25
 *   test +0x3a4 cmp r1, #30
 *   test +0x3b8 cmp r1, #30
 *   test +0x3cc cmp r0, #0
 *   test +0x3f4 cmp r0, #0
 *   test +0x41c cmp r1, #40
 *   test +0x430 cmp r0, #0
 *   test +0x44c cmp r0, #0
 *   test +0x464 cmp r1, #100
 *   test +0x478 cmp r1, #0
 *   test +0x488 cmp r0, #0
 *   0 block transfer(s), 26 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021edf1c; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021f82d8(void);
extern void native_fn_021dca04(void);
extern void native_fn_0207afec(void);
extern void native_fn_0207d884(void);
extern void native_fn_0207b058(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_021f94d8(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f949c(void);
extern void native_fn_0220f530(void);
extern void native_fn_021dbb14(void);
extern void native_fn_0220f868(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_022168e8(void);
extern void native_fn_021eb144(void);


asm u32 native_ov001_021edf1c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #8
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x21]
    cmp r1, #0
    bne ov001_021edf1c_L60
    ldr r0, [r0, #0x50]
    bl native_fn_021db8d0
    cmp r0, #0
    bne ov001_021edf1c_L40
    ldr r0, =0x02238d7c
    mov r1, #19
    strb r1, [r0, #0x13]
    add sp, sp, #8
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_021edf1c_L40:
    ldr r1, =0x02238d7c
    ldr r0, [r1, #0x50]
    add r0, r0, #256
    ldrsb r0, [r0, #228]
    cmp r0, #0
    moveq r0, #5
    streqb r0, [r1, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L60:
    cmp r1, #5
    bne ov001_021edf1c_L80
    ldr r0, [r0, #0x50]
    bl native_fn_021f82d8
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L80:
    cmp r1, #10
    bne ov001_021edf1c_L258
    ldr r0, [r0, #0x50]
    mov r5, #0
    bl native_fn_021dca04
    ldr r1, =0x02238d7c
    strh r0, [sp, #4]
    ldrh r0, [r1, #54]
    bl native_fn_0207afec
    ldr r1, =0x02238d7c
    ldrb r4, [r0, #0x1e]
    ldrh r0, [r1, #54]
    bl native_fn_0207afec
    ldr r0, =0x02238d7c
    mov r6, r5
    ldrh r0, [r0, #54]
    cmp r0, #237
    bne ov001_021edf1c_Ld8
    ldrsh r0, [sp, #4]
    mov r5, #1
    add r0, r0, r0, lsr #31
    add r6, r6, r0, asr #1
ov001_021edf1c_Ld8:
    ldr r0, =0x02238d7c
    add r1, sp, #4
    ldr r0, [r0, #0x60]
    mov r2, #1
    ldrb r0, [r0, #0x1fd]
    bl native_fn_0207d884
    mov r7, r0
    cmp r7, #0
    ble ov001_021edf1c_L118
    ldr r0, =0x02238d7c
    mov r1, #32
    ldrh r0, [r0, #54]
    bl native_fn_0207b058
    cmp r0, #0
    addne r6, r6, r7
    movne r5, #1
ov001_021edf1c_L118:
    cmp r5, #0
    beq ov001_021edf1c_L248
    cmp r6, #100
    movge r6, #100
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021edf1c_L190
    ldr r0, =0x02238d7c
    mov r1, r6
    ldrh r2, [r0, #54]
    ldr r0, [r0, #0x50]
    bl native_fn_021f0f0c
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x50]
    bl native_fn_021ee9fc
    ldr r0, =0x02238d7c
    mov r1, r6
    ldr r0, [r0, #0x50]
    mov r2, r4
    bl native_fn_021ee7d4
    mov r0, #19
    mov r1, #0
    bl native_fn_021f94d8
    ldr r0, =0x02238d7c
    rsb r2, r6, #0
    ldr r1, [r0, #0x50]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    b ov001_021edf1c_L230
ov001_021edf1c_L190:
    ldr r0, =0x02238d7c
    mov r1, r6
    ldrh r2, [r0, #54]
    ldr r0, [r0, #0x50]
    bl native_fn_021f0eb4
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x50]
    bl native_fn_021ee9fc
    mov r1, #0
    ldr r0, =0x02238d7c
    str r1, [sp]
    ldrh r2, [r0, #54]
    ldr r0, [r0, #0x50]
    mov r1, r6
    mov r3, r4
    bl native_fn_021ee78c
    ldr r0, =0x02238d7c
    rsb r2, r6, #0
    ldr r1, [r0, #0x50]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    cmp r6, #0
    ble ov001_021edf1c_L214
    ldr r0, =0x02238d7c
    mov r1, #4
    ldr r0, [r0, #0x50]
    mov r2, #1
    bl native_fn_021d9494
    mov r0, #239
    mov r1, #0
    bl native_fn_021f949c
    b ov001_021edf1c_L220
ov001_021edf1c_L214:
    mov r0, #242
    mov r1, #0
    bl native_fn_021f949c
ov001_021edf1c_L220:
    ldr r0, =0x02238d7c
    mov r1, #1
    ldr r0, [r0, #0x50]
    bl native_fn_0220f530
ov001_021edf1c_L230:
    ldr r0, =0x02238d7c
    mov r1, #15
    strb r1, [r0, #0x21]
    mov r1, #0
    strb r1, [r0, #0x20]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L248:
    ldr r0, =0x02238d7c
    mov r1, #20
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L258:
    cmp r1, #15
    bne ov001_021edf1c_L280
    ldrb r1, [r0, #0x20]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x20]
    movhs r1, #20
    strhsb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L280:
    cmp r1, #20
    bne ov001_021edf1c_L390
    ldr r0, [r0, #0x50]
    bl native_fn_021dca04
    ldr r1, =0x02238d7c
    strh r0, [sp, #4]
    ldrh r0, [r1, #54]
    bl native_fn_0207afec
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    bl native_fn_0207afec
    ldr r0, =0x02238d7c
    ldrh r1, [r0, #54]
    cmp r1, #121
    bne ov001_021edf1c_L384
    ldr r0, [r0, #0x50]
    bl native_fn_021ee9fc
    ldr r0, =0x02238d7c
    mov r2, #0
    ldr r1, [r0, #0x50]
    ldr r0, =0x0000270f
    strb r2, [r1, #0x357]
    ldrsh r1, [sp, #4]
    mov r3, #1
    cmp r1, r0
    movge r1, r0
    strh r1, [sp, #4]
    mov r0, #0
    str r0, [sp]
    ldr r0, =0x02238d7c
    ldrsh r1, [sp, #4]
    ldrh r2, [r0, #54]
    ldr r0, [r0, #0x50]
    bl native_fn_021ee78c
    ldr r0, =0x02238d7c
    ldrsh r1, [sp, #4]
    ldrh r2, [r0, #54]
    ldr r0, [r0, #0x50]
    bl native_fn_021f0eb4
    ldrsh r0, [sp, #4]
    cmp r0, #0
    ble ov001_021edf1c_L34c
    ldr r0, =0x02238d7c
    mov r1, #4
    ldr r0, [r0, #0x50]
    mov r2, #1
    bl native_fn_021d9494
    mov r0, #238
    mov r1, #0
    bl native_fn_021f949c
    b ov001_021edf1c_L358
ov001_021edf1c_L34c:
    mov r0, #242
    mov r1, #0
    bl native_fn_021f949c
ov001_021edf1c_L358:
    ldr r0, =0x02238d7c
    mov r1, #0
    strb r1, [r0, #0x20]
    mov r1, #25
    strb r1, [r0, #0x21]
    ldr r1, [r0, #0x50]
    ldrsh r2, [sp, #4]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    b ov001_021edf1c_L4b0
ov001_021edf1c_L384:
    mov r1, #30
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L390:
    cmp r1, #25
    bne ov001_021edf1c_L3b8
    ldrb r1, [r0, #0x20]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x20]
    movhs r1, #30
    strhsb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L3b8:
    cmp r1, #30
    bne ov001_021edf1c_L41c
    ldr r0, [r0, #0x50]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_021edf1c_L3e4
    ldr r0, =0x02238d7c
    mov r1, #40
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L3e4:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x50]
    ldrb r0, [r0, #0x31e]
    bl native_fn_0220f868
    cmp r0, #0
    beq ov001_021edf1c_L40c
    ldr r0, =0x02238d7c
    mov r1, #40
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L40c:
    ldr r0, =0x02238d7c
    mov r1, #100
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L41c:
    cmp r1, #40
    bne ov001_021edf1c_L464
    ldr r0, [r0, #0x50]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_021edf1c_L4b0
    ldr r1, =0x02238d7c
    mov r0, #0
    ldr r1, [r1, #0x50]
    ldrb r1, [r1, #0x31e]
    bl native_fn_022168e8
    cmp r0, #0
    beq ov001_021edf1c_L4b0
    ldr r0, =0x02238d7c
    mov r1, #100
    strb r1, [r0, #0x21]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L464:
    cmp r1, #100
    bne ov001_021edf1c_L4b0
    mov r1, #0
    strb r1, [r0, #0x21]
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    beq ov001_021edf1c_L4a4
    ldr r0, [r0, #0x50]
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021edf1c_L4a4
    bl native_fn_021eb144
    ldr r0, =0x02238d7c
    mov r1, #11
    strb r1, [r0, #0x13]
    b ov001_021edf1c_L4b0
ov001_021edf1c_L4a4:
    ldr r0, =0x02238d7c
    mov r1, #19
    strb r1, [r0, #0x13]
ov001_021edf1c_L4b0:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
