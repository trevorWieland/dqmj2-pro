/* ov001 row 0x022079a4: 948 bytes.
 *
 * What it does: 237 instructions; 24 call(s) to 0x02207938, 0x020443ec, 0x020443ec, +21 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (237 instructions, 24 calls, 28 branches, 21 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0x3c
 *   branch +0x2c -> +0x3c
 *   branch +0x38 -> +0x50
 *   branch +0x4c -> +0x54
 *   back edge +0x1ac -> +0x18c
 *   back edge +0x1cc -> +0x188
 *   branch +0x1e4 -> +0x218
 *   branch +0x1ec -> +0x288
 *   branch +0x1f4 -> +0x29c
 *   branch +0x1fc -> +0x29c
 *   branch +0x200 -> +0x224
 *   branch +0x208 -> +0x240
 *   branch +0x210 -> +0x254
 *   branch +0x214 -> +0x29c
 *   branch +0x21c -> +0x268
 *   branch +0x220 -> +0x29c
 *   branch +0x23c -> +0x2a8
 *   branch +0x250 -> +0x2a8
 *   branch +0x264 -> +0x2a8
 *   branch +0x284 -> +0x2a8
 *   branch +0x298 -> +0x2a8
 *   branch +0x2ac -> +0x390
 *   branch +0x2c0 -> +0x2d8
 *   branch +0x2c8 -> +0x2e0
 *   branch +0x2d0 -> +0x2e8
 *   branch +0x2d4 -> +0x300
 *   branch +0x2dc -> +0x300
 *   branch +0x2e4 -> +0x300
 *   branch +0x338 -> +0x350
 *   branch +0x34c -> +0x364
 *   branch +0x380 -> +0x390
 *   back edge +0x3a0 -> +0x1d8
 *   test +0x1c cmp r0, #0
 *   test +0x28 cmp r0, #6
 *   test +0x34 cmp r0, #8
 *   test +0x40 cmp r0, #1
 *   test +0x44 cmpne r0, #3
 *   test +0x1a8 cmp r1, #22
 *   test +0x1c4 cmp r7, #2
 *   test +0x1dc cmp r9, #56
 *   test +0x1e8 cmp r9, #56
 *   test +0x1f0 cmp r9, #47
 *   test +0x1f8 cmp r9, #45
 *   test +0x204 cmp r9, #46
 *   test +0x20c cmp r9, #47
 *   test +0x218 cmp r9, #57
 *   test +0x22c cmp r0, #0
 *   test +0x234 cmpne r0, #0
 *   test +0x248 tst r0, #1
 *   test +0x25c tst r0, #4
 *   test +0x26c cmp r0, #0
 *   test +0x27c tst r7, r0
 *   test +0x290 tst r0, #32
 *   test +0x2a0 cmp r0, #0
 *   test +0x2a8 cmp r8, #0
 *   test +0x2bc cmp r0, #0
 *   test +0x2c4 cmp r0, #1
 *   test +0x2cc cmp r0, #2
 *   test +0x2ec cmp r0, #0
 *   test +0x308 cmp r4, #0
 *   test +0x318 cmp r7, #0
 *   test +0x368 cmp r4, #0
 *   test +0x39c cmp r9, #60
 *   1 block transfer(s), 39 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022079a4; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_020443ec(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_02045efc(void);
extern void native_fn_021fd354(void);
extern void native_fn_0202a37c(void);
extern void native_fn_020852d0(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021e2aa4(void);
extern void native_fn_0220815c(void);
extern void native_fn_02207f9c(void);


asm u32 native_ov001_022079a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    bl native_fn_02207938
    mov r5, r0
    ldr r11, [r5, #0x10]
    add r6, r11, #556
    bl native_fn_020443ec
    cmp r0, #0
    beq ov001_022079a4_L3c
    bl native_fn_020443ec
    cmp r0, #6
    beq ov001_022079a4_L3c
    bl native_fn_020443ec
    cmp r0, #8
    bne ov001_022079a4_L50
ov001_022079a4_L3c:
    ldrb r0, [r11, #0x31e]
    cmp r0, #1
    cmpne r0, #3
    moveq r1, #2
    beq ov001_022079a4_L54
ov001_022079a4_L50:
    mov r1, #4
ov001_022079a4_L54:
    mov r0, #3
    str r0, [sp]
    mov r0, #20
    stmib sp, {r0, r1}
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, #24
    mov r1, #8
    mov r2, #31
    mov r3, #10
    bl native_fn_021fe4ac
    str r0, [r5]
    mov r1, #8
    str r1, [sp]
    mov r0, #28
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, #25
    mov r2, #127
    bl native_fn_021fe4ac
    str r0, [r5, #0x4]
    mov r0, #11
    str r0, [sp]
    mov r0, #30
    str r0, [sp, #0x4]
    mov r0, #14
    str r0, [sp, #0x8]
    mov r3, #1
    str r3, [sp, #0xc]
    str r3, [sp, #0x10]
    mov r0, #26
    mov r1, #8
    mov r2, #127
    bl native_fn_021fe4ac
    str r0, [r5, #0x8]
    mov r0, #1
    bl native_fn_02045efc
    mov r0, #3
    bl native_fn_021fd354
    mov r0, #2
    mov r1, #2048
    mov r2, #4
    bl native_fn_0202a37c
    str r0, [r5, #0x14]
    mov r3, #1
    str r3, [r5, #0x1c]
    mov r1, #0
    str r1, [r5, #0x20]
    mov r0, #19
    str r0, [sp]
    mov r0, #30
    str r0, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    str r1, [sp, #0xc]
    mov r0, #28
    mov r1, #8
    mov r2, #127
    str r3, [sp, #0x10]
    bl native_fn_021fe4ac
    str r0, [r5, #0xc]
    ldr r0, [r5, #0x8]
    mov r1, #1
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_020852d0
    mov r7, #0
    mov r0, r5
    mov r9, r7
    mov r3, r7
ov001_022079a4_L188:
    mov r1, r3
ov001_022079a4_L18c:
    add r2, r0, r1
    add r1, r1, #1
    strb r9, [r2, #0x2c]
    mov r1, r1, lsl #24
    strb r9, [r2, #0x42]
    mov r1, r1, asr #24
    strb r9, [r2, #0x58]
    cmp r1, #22
    blt ov001_022079a4_L18c
    add r1, r7, #1
    mov r1, r1, lsl #24
    strh r9, [r0, #110]
    mov r7, r1, asr #24
    strh r9, [r0, #112]
    cmp r7, #2
    add r0, r0, #70
    blt ov001_022079a4_L188
    strb r9, [sp, #0x15]
    strb r9, [sp, #0x14]
ov001_022079a4_L1d8:
    mov r8, #0
    cmp r9, #56
    mov r7, r8
    bgt ov001_022079a4_L218
    cmp r9, #56
    bge ov001_022079a4_L288
    cmp r9, #47
    bgt ov001_022079a4_L29c
    cmp r9, #45
    blt ov001_022079a4_L29c
    beq ov001_022079a4_L224
    cmp r9, #46
    beq ov001_022079a4_L240
    cmp r9, #47
    beq ov001_022079a4_L254
    b ov001_022079a4_L29c
ov001_022079a4_L218:
    cmp r9, #57
    beq ov001_022079a4_L268
    b ov001_022079a4_L29c
ov001_022079a4_L224:
    ldr r1, [r5, #0x10]
    ldrb r0, [r1, #0x31c]
    cmp r0, #0
    ldrneb r0, [r1, #0x1ff]
    cmpne r0, #0
    movne r8, #1
    b ov001_022079a4_L2a8
ov001_022079a4_L240:
    mov r7, #1
    bl native_fn_021e29e8
    tst r0, #1
    movne r8, r7
    b ov001_022079a4_L2a8
ov001_022079a4_L254:
    mov r7, #4
    bl native_fn_021e29e8
    tst r0, #4
    movne r8, #1
    b ov001_022079a4_L2a8
ov001_022079a4_L268:
    ldrb r0, [r11, #0x31e]
    cmp r0, #0
    moveq r7, #8
    movne r7, #16
    bl native_fn_021e29e8
    tst r7, r0
    movne r8, #1
    b ov001_022079a4_L2a8
ov001_022079a4_L288:
    mov r7, #32
    bl native_fn_021e29e8
    tst r0, #32
    movne r8, #1
    b ov001_022079a4_L2a8
ov001_022079a4_L29c:
    ldrsb r0, [r6, r9]
    cmp r0, #0
    movne r8, #1
ov001_022079a4_L2a8:
    cmp r8, #0
    beq ov001_022079a4_L390
    mov r0, r9
    bl native_fn_021d8dec
    ldrsb r0, [r0, #8]
    cmp r0, #0
    beq ov001_022079a4_L2d8
    cmp r0, #1
    beq ov001_022079a4_L2e0
    cmp r0, #2
    beq ov001_022079a4_L2e8
    b ov001_022079a4_L300
ov001_022079a4_L2d8:
    mov r4, #0
    b ov001_022079a4_L300
ov001_022079a4_L2e0:
    mov r4, #1
    b ov001_022079a4_L300
ov001_022079a4_L2e8:
    ldrsb r0, [r6, r9]
    cmp r0, #0
    movgt r0, #0
    movle r0, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
ov001_022079a4_L300:
    mov r0, #70
    mla r8, r4, r0, r5
    cmp r4, #0
    addeq r10, sp, #21
    addne r10, sp, #20
    ldrsb r0, [r10]
    cmp r7, #0
    add r2, r6, r9
    add r0, r8, r0
    strb r9, [r0, #0x2c]
    ldrsb r0, [r10]
    ldrsb r1, [r6, r9]
    add r0, r8, r0
    strb r1, [r0, #0x42]
    bne ov001_022079a4_L350
    ldrsb r1, [r2, #60]
    ldrsb r0, [r10]
    add r0, r8, r0
    strb r1, [r0, #0x58]
    b ov001_022079a4_L364
ov001_022079a4_L350:
    mov r0, r7
    bl native_fn_021e2aa4
    ldrsb r1, [r10]
    add r1, r8, r1
    strb r0, [r1, #0x58]
ov001_022079a4_L364:
    ldrsh r0, [r8, #110]
    cmp r4, #0
    add r0, r0, #1
    strh r0, [r8, #110]
    ldrnesb r0, [sp, #20]
    addne r0, r0, #1
    strneb r0, [sp, #0x14]
    bne ov001_022079a4_L390
    ldrsb r0, [sp, #21]
    add r0, r0, #1
    strb r0, [sp, #0x15]
ov001_022079a4_L390:
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    cmp r9, #60
    blt ov001_022079a4_L1d8
    bl native_fn_0220815c
    bl native_fn_02207f9c
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
