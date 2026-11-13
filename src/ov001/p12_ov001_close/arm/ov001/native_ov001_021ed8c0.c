/* ov001 row 0x021ed8c0: 1052 bytes.
 *
 * What it does: 260 instructions; 38 call(s) to 0x0207afec, 0x021db438, 0x021edb28, +35 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 38 calls (260 instructions, 38 calls, 41 branches, 19 back edges, 3 literal slots).
 *
 *   pool +0x410 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x414 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x418 -> constant 0x02238e14 (image word 0x02238e14)
 *   branch +0x20 -> +0x284
 *   branch +0x60 -> +0x268
 *   branch +0x6c -> +0x268
 *   branch +0x78 -> +0x88
 *   branch +0x80 -> +0x1c8
 *   branch +0x84 -> +0x20c
 *   branch +0x90 -> +0x1c0
 *   branch +0xa8 -> +0x13c
 *   branch +0xb4 -> +0x108
 *   branch +0xec -> +0xfc
 *   branch +0xf8 -> +0x100
 *   branch +0x104 -> +0x10c
 *   branch +0x138 -> +0x20c
 *   branch +0x144 -> +0x188
 *   branch +0x168 -> +0x180
 *   branch +0x184 -> +0x18c
 *   branch +0x1bc -> +0x20c
 *   branch +0x1c4 -> +0x20c
 *   branch +0x1d0 -> +0x204
 *   branch +0x1e8 -> +0x204
 *   branch +0x200 -> +0x20c
 *   branch +0x21c -> +0x268
 *   branch +0x264 -> +0x408
 *   back edge +0x27c -> +0x3c
 *   branch +0x280 -> +0x408
 *   branch +0x288 -> +0x2ac
 *   branch +0x294 -> +0x29c
 *   branch +0x2a8 -> +0x408
 *   branch +0x2b0 -> +0x374
 *   branch +0x2bc -> +0x408
 *   branch +0x2cc -> +0x2dc
 *   branch +0x2d4 -> +0x330
 *   branch +0x2d8 -> +0x35c
 *   branch +0x30c -> +0x320
 *   branch +0x31c -> +0x35c
 *   branch +0x32c -> +0x35c
 *   branch +0x370 -> +0x408
 *   branch +0x378 -> +0x39c
 *   branch +0x398 -> +0x408
 *   branch +0x3a0 -> +0x3d4
 *   branch +0x3ac -> +0x408
 *   branch +0x3d0 -> +0x408
 *   branch +0x3d8 -> +0x408
 *   branch +0x3e4 -> +0x3ec
 *   test +0x1c cmp r0, #0
 *   test +0x5c cmp r1, #0
 *   test +0x68 cmp r0, #0
 *   test +0x74 cmp r0, #123
 *   test +0x7c cmp r0, #124
 *   test +0x8c cmp r0, #0
 *   test +0xa0 cmp r1, #0
 *   test +0xb0 cmp r0, #0
 *   test +0xcc cmp r1, #100
 *   test +0xe8 cmp r0, r10
 *   test +0xf0 cmp r1, #100
 *   test +0x140 cmp r0, #0
 *   test +0x164 cmp r10, r2
 *   test +0x1cc cmp r0, #0
 *   test +0x1e4 cmp r0, #0
 *   test +0x210 cmp r0, #0
 *   test +0x218 cmpeq r0, #0
 *   test +0x268 cmp r9, #2
 *   test +0x278 cmp r9, #3
 *   test +0x284 cmp r0, #5
 *   test +0x290 cmp r0, #0
 *   test +0x2ac cmp r0, #10
 *   test +0x2b8 cmp r0, #0
 *   test +0x2c8 cmp r1, #123
 *   test +0x2d0 cmp r1, #124
 *   test +0x308 cmp r0, #0
 *   test +0x374 cmp r0, #20
 *   test +0x388 cmp r0, #30
 *   test +0x39c cmp r0, #30
 *   test +0x3a8 cmp r0, #0
 *   test +0x3d4 cmp r0, #100
 *   test +0x3e0 cmp r0, #0
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ed8c0; the literal pool and
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
extern void native_fn_020444a8(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021e3508(void);
extern void native_fn_021e3534(void);
extern void native_fn_021e3eec(void);
extern void native_fn_020630e4(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void native_fn_021f14e4(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_02048094(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_02047d40(void);
extern void native_fn_021e9d70(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021ed8c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    bl native_fn_0207afec
    ldr r5, =0x02238d7c
    str r0, [sp]
    ldrb r0, [r5, #0x26]
    cmp r0, #0
    bne ov001_021ed8c0_L284
    mov r9, #0
    ldr r4, =0x66666667
    mov r8, r9
    mov r7, r9
    mov r11, #1
    mov r6, r9
ov001_021ed8c0_L3c:
    ldr r0, [r5, #0x54]
    mov r1, r9
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    ldr r1, [r5, #0x60]
    add r1, r1, r9, lsl #1
    add r1, r1, #768
    ldrsh r1, [r1, #78]
    cmp r1, #0
    ble ov001_021ed8c0_L268
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021ed8c0_L268
    ldrh r0, [r5, #54]
    cmp r0, #123
    beq ov001_021ed8c0_L88
    cmp r0, #124
    beq ov001_021ed8c0_L1c8
    b ov001_021ed8c0_L20c
ov001_021ed8c0_L88:
    bl native_fn_020444a8
    cmp r0, #0
    bne ov001_021ed8c0_L1c0
    ldr r0, [r5, #0x60]
    mov r2, #1
    ldrb r1, [r0, #0x31e]
    cmp r1, #0
    mov r1, #2
    bne ov001_021ed8c0_L13c
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_021ed8c0_L108
    ldr r2, [r5, #0x54]
    ldrh r0, [r5, #44]
    ldr r2, [r2, #0x1e8]
    ldrsh r2, [r2, #40]
    rsb r1, r0, #300
    cmp r1, #100
    add r3, r2, #9
    smull r2, r10, r4, r3
    movlt r0, r1
    mov r2, r3, lsr #31
    movge r0, #100
    add r10, r2, r10, asr #2
    cmp r0, r10
    bge ov001_021ed8c0_Lfc
    cmp r1, #100
    movge r1, #100
    b ov001_021ed8c0_L100
ov001_021ed8c0_Lfc:
    mov r1, r10
ov001_021ed8c0_L100:
    strh r1, [r5, #52]
    b ov001_021ed8c0_L10c
ov001_021ed8c0_L108:
    strh r8, [r5, #52]
ov001_021ed8c0_L10c:
    ldrh r0, [r5, #52]
    bl native_fn_021e3508
    ldrh r2, [r5, #52]
    ldrh r0, [r5, #44]
    add r0, r0, r2
    strh r0, [r5, #44]
    ldr r0, [r5, #0x54]
    ldr r1, [r0, #0x1e8]
    ldrsh r0, [r1, #48]
    sub r0, r0, r2
    strh r0, [r1, #48]
    b ov001_021ed8c0_L20c
ov001_021ed8c0_L13c:
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_021ed8c0_L188
    ldrh r0, [r5, #42]
    rsb r10, r0, #300
    bl native_fn_021e3534
    add r1, r0, #9
    smull r0, r2, r4, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #2
    cmp r10, r2
    blt ov001_021ed8c0_L180
    bl native_fn_021e3534
    add r1, r0, #9
    smull r0, r10, r4, r1
    mov r0, r1, lsr #31
    add r10, r0, r10, asr #2
ov001_021ed8c0_L180:
    strh r10, [r5, #52]
    b ov001_021ed8c0_L18c
ov001_021ed8c0_L188:
    strh r7, [r5, #52]
ov001_021ed8c0_L18c:
    ldrh r0, [r5, #52]
    rsb r0, r0, #0
    bl native_fn_021e3508
    ldrh r2, [r5, #52]
    ldrh r0, [r5, #42]
    add r0, r0, r2
    strh r0, [r5, #42]
    ldr r0, [r5, #0x54]
    ldr r1, [r0, #0x1e8]
    ldrsh r0, [r1, #48]
    add r0, r0, r2
    strh r0, [r1, #48]
    b ov001_021ed8c0_L20c
ov001_021ed8c0_L1c0:
    strh r6, [r5, #52]
    b ov001_021ed8c0_L20c
ov001_021ed8c0_L1c8:
    bl native_fn_020444a8
    cmp r0, #0
    bne ov001_021ed8c0_L204
    ldr r0, [r5, #0x54]
    mov r1, #1
    bl native_fn_021e3eec
    strh r0, [r5, #50]
    cmp r0, #0
    beq ov001_021ed8c0_L204
    mov r1, #1
    bl native_fn_020630e4
    ldr r0, [r5, #0x54]
    ldr r0, [r0, #0x1e8]
    strb r11, [r0, #0xb1]
    b ov001_021ed8c0_L20c
ov001_021ed8c0_L204:
    mov r0, #0
    strh r0, [r5, #50]
ov001_021ed8c0_L20c:
    ldrh r0, [r5, #50]
    cmp r0, #0
    ldreqh r0, [r5, #52]
    cmpeq r0, #0
    beq ov001_021ed8c0_L268
    ldr r0, [sp]
    ldrsh r4, [r0, #14]
    ldr r0, =0x02238e14
    bl native_fn_0202ac08
    mov r0, r4
    mov r1, #0
    bl native_fn_021eea10
    mov r0, r4
    bl native_fn_0205d790
    ldr r1, =0x02238d7c
    mov r2, r0
    ldr r1, [r1, #0x54]
    mov r0, r4
    bl native_fn_021e9cd8
    ldr r0, =0x02238d7c
    mov r1, #5
    strb r1, [r0, #0x26]
    b ov001_021ed8c0_L408
ov001_021ed8c0_L268:
    cmp r9, #2
    moveq r0, #100
    add r9, r9, #1
    streqb r0, [r5, #0x26]
    cmp r9, #3
    blt ov001_021ed8c0_L3c
    b ov001_021ed8c0_L408
ov001_021ed8c0_L284:
    cmp r0, #5
    bne ov001_021ed8c0_L2ac
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021ed8c0_L29c
    bl ov001_clear_state_flag4_021f14a4
ov001_021ed8c0_L29c:
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0x26]
    b ov001_021ed8c0_L408
ov001_021ed8c0_L2ac:
    cmp r0, #10
    bne ov001_021ed8c0_L374
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_021ed8c0_L408
    mov r0, r5
    ldrh r1, [r0, #54]
    cmp r1, #123
    beq ov001_021ed8c0_L2dc
    cmp r1, #124
    beq ov001_021ed8c0_L330
    b ov001_021ed8c0_L35c
ov001_021ed8c0_L2dc:
    ldrh r0, [r0, #52]
    mov r1, #0
    bl native_fn_02048094
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #42
    bl ov001_begin_state_transition_021f1354
    mov r0, r5
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021ed8c0_L320
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    b ov001_021ed8c0_L35c
ov001_021ed8c0_L320:
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    b ov001_021ed8c0_L35c
ov001_021ed8c0_L330:
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #41
    bl ov001_begin_state_transition_021f1354
    mov r0, r5
    ldrh r0, [r0, #50]
    bl native_fn_02047d40
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
ov001_021ed8c0_L35c:
    ldr r0, =0x02238d7c
    mov r1, #20
    strb r1, [r0, #0x26]
    mov r1, #0
    strb r1, [r0, #0x25]
    b ov001_021ed8c0_L408
ov001_021ed8c0_L374:
    cmp r0, #20
    bne ov001_021ed8c0_L39c
    ldrb r0, [r5, #0x25]
    add r1, r0, #1
    and r0, r1, #255
    cmp r0, #30
    strb r1, [r5, #0x25]
    movhs r0, #30
    strhsb r0, [r5, #0x26]
    b ov001_021ed8c0_L408
ov001_021ed8c0_L39c:
    cmp r0, #30
    bne ov001_021ed8c0_L3d4
    bl native_fn_021e9d70
    cmp r0, #0
    beq ov001_021ed8c0_L408
    ldr r0, [sp]
    ldrsh r0, [r0, #14]
    bl native_fn_021eeb70
    ldr r0, =0x02238e14
    bl native_fn_0202ac4c
    mov r0, r5
    mov r1, #100
    strb r1, [r0, #0x26]
    b ov001_021ed8c0_L408
ov001_021ed8c0_L3d4:
    cmp r0, #100
    bne ov001_021ed8c0_L408
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021ed8c0_L3ec
    bl ov001_clear_state_flag4_021f14a4
ov001_021ed8c0_L3ec:
    ldr r0, =0x02238d7c
    mov r1, #0
    strb r1, [r0, #0x26]
    strh r1, [r0, #52]
    strh r1, [r0, #50]
    mov r1, #9
    strb r1, [r0, #0x13]
ov001_021ed8c0_L408:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
