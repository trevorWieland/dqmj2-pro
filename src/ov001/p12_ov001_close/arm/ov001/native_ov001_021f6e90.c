/* ov001 row 0x021f6e90: 860 bytes.
 *
 * What it does: 213 instructions; 32 call(s) to 0x0207afec, 0x021db438, 0x021db438, +29 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 32 calls (213 instructions, 32 calls, 15 branches, 25 back edges, 2 literal slots).
 *
 *   pool +0x354 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x358 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x50 -> +0x78
 *   branch +0x74 -> +0x88
 *   branch +0x90 -> +0x260
 *   branch +0xa8 -> +0x20c
 *   branch +0x11c -> +0x1c0
 *   branch +0x130 -> +0x170
 *   branch +0x16c -> +0x1c0
 *   branch +0x1c8 -> +0x200
 *   branch +0x208 -> +0x214
 *   branch +0x21c -> +0x24c
 *   branch +0x22c -> +0x24c
 *   back edge +0x25c -> +0x9c
 *   branch +0x268 -> +0x318
 *   branch +0x288 -> +0x2b8
 *   branch +0x294 -> +0x2b8
 *   branch +0x2b4 -> +0x2bc
 *   branch +0x2cc -> +0x304
 *   branch +0x2d8 -> +0x304
 *   back edge +0x314 -> +0x278
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r10, #0
 *   test +0x88 cmp r5, #0
 *   test +0xa4 cmp r0, #0
 *   test +0x118 cmp r0, #0
 *   test +0x124 tst r0, #32
 *   test +0x144 cmp r1, #0
 *   test +0x1c4 cmp r0, #0
 *   test +0x218 tst r0, #32
 *   test +0x228 cmp r0, #0
 *   test +0x258 cmp r4, r5
 *   test +0x260 cmp r5, #0
 *   test +0x27c cmp r0, #0
 *   test +0x284 cmpne r0, #0
 *   test +0x290 tst r0, #32
 *   test +0x2c0 cmp r0, #0
 *   test +0x2c8 cmpne r0, #0
 *   test +0x2d4 tst r0, #32
 *   test +0x308 cmp r8, r5
 *   test +0x31c cmp r0, #0
 *   0 block transfer(s), 23 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f6e90; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021d9494(void);
extern void native_fn_0220f530(void);
extern void native_fn_021f5ac4(void);
extern void native_fn_021dc53c(void);
extern void native_fn_021db788(void);
extern void native_fn_0220ecd8(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f6e90 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    ldr r4, =0x0223989c
    str r0, [sp, #0x1c]
    ldrh r0, [r4, #80]
    mov r10, r1
    mov r1, #0
    mov r9, r2
    mov r11, r3
    str r1, [sp, #0x24]
    bl native_fn_0207afec
    mov r1, r4
    str r0, [sp, #0x20]
    ldr r0, [r1, #0x84]
    mov r1, #0
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r4, #0
    movne r4, #1
    cmp r10, #0
    bne ov001_021f6e90_L78
    mov r0, r4
    bl ov001_side_slot_record_021db438
    mov r10, r0
    add r0, r4, #2
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r6, r0
    mov r5, #3
    b ov001_021f6e90_L88
ov001_021f6e90_L78:
    add r0, r4, #2
    bl ov001_side_slot_record_021db438
    mov r6, r0
    mov r5, #1
ov001_021f6e90_L88:
    cmp r5, #0
    mov r4, #0
    ble ov001_021f6e90_L260
    mov r7, r10
    mov r8, r6
ov001_021f6e90_L9c:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f6e90_L20c
    add r0, sp, #56
    str r0, [sp]
    add r0, sp, #40
    str r0, [sp, #0x4]
    add r0, sp, #52
    str r0, [sp, #0x8]
    add r0, r7, #844
    str r0, [sp, #0xc]
    add r0, sp, #44
    str r0, [sp, #0x10]
    add r0, sp, #48
    str r0, [sp, #0x14]
    mov r0, #0
    str r0, [sp, #0x18]
    ldr r0, =0x0223989c
    ldr r3, =0x0223989c
    ldrh r0, [r0, #80]
    ldrb r3, [r3, #0x10]
    ldr r1, [sp, #0x1c]
    mov r2, r7
    bl native_fn_021e1a60
    mov r0, r7
    bl native_fn_021dbcbc
    add r0, r0, r0, lsr #31
    mov r0, r0, asr #1
    str r0, [sp, #0x38]
    ldr r0, [sp, #0x30]
    cmp r0, #0
    beq ov001_021f6e90_L1c0
    bl native_fn_021e29e8
    tst r0, #32
    mov r0, r7
    mov r2, #49
    bne ov001_021f6e90_L170
    ldr r1, [sp, #0x38]
    bl native_fn_021f0f0c
    ldr r1, [sp, #0x34]
    mov r2, #1
    cmp r1, #0
    streq r0, [sp, #0x38]
    ldr r1, [sp, #0x38]
    mov r0, r7
    bl native_fn_021ee7d4
    ldr r2, [sp, #0x38]
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    rsb r2, r2, #0
    bl native_fn_022024d4
    b ov001_021f6e90_L1c0
ov001_021f6e90_L170:
    ldr r1, [sp, #0x38]
    bl native_fn_021f0eb4
    mov r0, #0
    str r0, [sp]
    ldr r1, [sp, #0x38]
    mov r0, r7
    mov r2, #49
    mov r3, #1
    bl native_fn_021ee78c
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    ldr r2, [sp, #0x38]
    bl native_fn_022024d4
    mov r0, r7
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    mov r0, r7
    mov r1, #1
    bl native_fn_0220f530
ov001_021f6e90_L1c0:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    beq ov001_021f6e90_L200
    ldr r0, =0x0223989c
    ldr r2, [sp, #0x24]
    ldrsb r1, [r0, #43]
    add r2, r2, #1
    str r2, [sp, #0x24]
    ldr r2, =0x0223989c
    add r3, r1, #1
    strb r3, [r2, #0x2b]
    ldr r2, =0x022399b8
    add r0, r7, #768
    str r7, [r2, r1, lsl #2]
    ldrh r1, [sp, #40]
    strh r1, [r0, #74]
ov001_021f6e90_L200:
    mov r0, #1
    strb r0, [r9, r4]
    b ov001_021f6e90_L214
ov001_021f6e90_L20c:
    mov r0, #0
    strb r0, [r9, r4]
ov001_021f6e90_L214:
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021f6e90_L24c
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f6e90_L24c
    mov r0, r8
    bl native_fn_021dbcbc
    add r0, r0, r0, lsr #31
    mov r1, r0, asr #1
    mov r0, r8
    mov r2, #49
    bl native_fn_021f0f0c
ov001_021f6e90_L24c:
    add r7, r7, #1088
    add r8, r8, #1088
    add r4, r4, #1
    cmp r4, r5
    blt ov001_021f6e90_L9c
ov001_021f6e90_L260:
    cmp r5, #0
    mov r8, #0
    ble ov001_021f6e90_L318
    ldr r9, =0x0223989c
    mov r4, r8
    mov r7, #1
ov001_021f6e90_L278:
    ldrb r0, [r10, #0x31c]
    cmp r0, #0
    ldrneb r0, [r10, #0x1ff]
    cmpne r0, #0
    beq ov001_021f6e90_L2b8
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021f6e90_L2b8
    ldr r0, [sp, #0x20]
    mov r1, r10
    ldrsh r2, [r0, #18]
    ldr r0, [r9, #0x84]
    mov r3, #0
    bl native_fn_021f5ac4
    strb r7, [r11, r8]
    b ov001_021f6e90_L2bc
ov001_021f6e90_L2b8:
    strb r4, [r11, r8]
ov001_021f6e90_L2bc:
    ldrb r0, [r6, #0x31c]
    cmp r0, #0
    ldrneb r0, [r6, #0x1ff]
    cmpne r0, #0
    beq ov001_021f6e90_L304
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021f6e90_L304
    mov r0, r6
    bl native_fn_021dc53c
    mov r0, r6
    bl native_fn_021dbcbc
    add r0, r0, r0, lsr #31
    mov r1, r0, asr #1
    mov r0, r6
    bl native_fn_021db788
    mov r0, r6
    bl native_fn_0220ecd8
ov001_021f6e90_L304:
    add r8, r8, #1
    cmp r8, r5
    add r10, r10, #1088
    add r6, r6, #1088
    blt ov001_021f6e90_L278
ov001_021f6e90_L318:
    ldr r0, [sp, #0x24]
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #0
    streqb r1, [r0, #0x10]
    addeq sp, sp, #60
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
    strb r1, [r0, #0x10]
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
