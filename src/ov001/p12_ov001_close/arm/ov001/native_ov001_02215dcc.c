/* ov001 row 0x02215dcc: 1012 bytes.
 *
 * What it does: 252 instructions; 44 call(s) to 0x02215d3c, 0x021f1354, 0x021f1414, +41 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 44 calls (252 instructions, 44 calls, 33 branches, 41 back edges, 1 literal slot).
 *
 *   pool +0x3f0 -> constant 0x02242ba0 (image word 0x02242ba0)
 *   branch +0x10 -> +0x58
 *   branch +0x54 -> +0x3e8
 *   branch +0x5c -> +0xd8
 *   branch +0x98 -> +0xb4
 *   back edge +0xbc -> +0x80
 *   branch +0xd4 -> +0x3e8
 *   branch +0xdc -> +0x178
 *   branch +0xf4 -> +0x3e8
 *   branch +0x104 -> +0x168
 *   branch +0x128 -> +0x144
 *   back edge +0x14c -> +0x110
 *   branch +0x164 -> +0x3e8
 *   branch +0x174 -> +0x3e8
 *   branch +0x17c -> +0x19c
 *   branch +0x188 -> +0x3e8
 *   branch +0x198 -> +0x3e8
 *   branch +0x1a0 -> +0x1c4
 *   branch +0x1c0 -> +0x3e8
 *   branch +0x1c8 -> +0x268
 *   branch +0x228 -> +0x244
 *   back edge +0x24c -> +0x210
 *   branch +0x264 -> +0x3e8
 *   branch +0x26c -> +0x308
 *   branch +0x284 -> +0x3e8
 *   branch +0x294 -> +0x2f8
 *   branch +0x2b8 -> +0x2d4
 *   back edge +0x2dc -> +0x2a0
 *   branch +0x2f4 -> +0x3e8
 *   branch +0x304 -> +0x3e8
 *   branch +0x30c -> +0x32c
 *   branch +0x318 -> +0x3e8
 *   branch +0x328 -> +0x3e8
 *   branch +0x330 -> +0x354
 *   branch +0x350 -> +0x3e8
 *   branch +0x358 -> +0x394
 *   branch +0x390 -> +0x3e8
 *   branch +0x398 -> +0x3c8
 *   branch +0x3b0 -> +0x3e8
 *   branch +0x3c4 -> +0x3e8
 *   branch +0x3cc -> +0x3e8
 *   test +0x0c cmp r1, #0
 *   test +0x58 cmp r1, #2
 *   test +0x94 cmp r0, #0
 *   test +0xb8 cmp r9, #3
 *   test +0xd8 cmp r1, #5
 *   test +0xf0 cmp r1, #30
 *   test +0x100 cmp r0, #8
 *   test +0x124 cmp r0, #0
 *   test +0x148 cmp r6, #3
 *   test +0x178 cmp r1, #10
 *   test +0x184 cmp r0, #0
 *   test +0x19c cmp r1, #12
 *   test +0x1b0 cmp r1, #30
 *   test +0x1c4 cmp r1, #15
 *   test +0x224 cmp r0, #0
 *   test +0x248 cmp r9, #3
 *   test +0x268 cmp r1, #20
 *   test +0x280 cmp r1, #30
 *   test +0x290 cmp r0, #8
 *   test +0x2b4 cmp r0, #0
 *   test +0x2d8 cmp r6, #3
 *   test +0x308 cmp r1, #25
 *   test +0x314 cmp r0, #0
 *   test +0x32c cmp r1, #27
 *   test +0x340 cmp r1, #30
 *   test +0x354 cmp r1, #30
 *   test +0x394 cmp r1, #35
 *   test +0x3ac cmp r1, #30
 *   test +0x3c8 cmp r1, #40
 *   0 block transfer(s), 28 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02215dcc; the literal pool and
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

extern void native_fn_02215d3c(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_021d7f54(void);
extern void native_fn_02041898(void);
extern void native_fn_02215d84(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbf98(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_021ee91c(void);
extern void native_fn_021f14e4(void);


asm u32 native_ov001_02215dcc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r0, =0x02242ba0
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov001_02215dcc_L58
    bl native_fn_02215d3c
    mov r2, r0
    mov r0, #1
    mov r3, r0
    mov r1, #0
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r0, #1
    bl native_fn_021d7f54
    ldr r0, =0x02242ba0
    mov r1, #2
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L58:
    cmp r1, #2
    bne ov001_02215dcc_Ld8
    mov r0, #0
    bl native_fn_02041898
    bl native_fn_02215d84
    mov r9, #0
    mov r4, #1
    mov r8, r0
    mov r5, r9
    mov r7, r4
ov001_02215dcc_L80:
    mov r0, r7
    mov r1, r9
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215dcc_Lb4
    mov r0, r6
    mov r1, r8
    mov r2, r4
    mov r3, r5
    str r5, [sp]
    bl native_fn_021dbf98
ov001_02215dcc_Lb4:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_02215dcc_L80
    ldr r0, =0x02242ba0
    mov r1, #5
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_Ld8:
    cmp r1, #5
    bne ov001_02215dcc_L178
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02215dcc_L3e8
    bl ov001_clear_state_flag4_021f14a4
    bl native_fn_02215d84
    cmp r0, #8
    bne ov001_02215dcc_L168
    mov r6, #0
    mov r5, #1
ov001_02215dcc_L110:
    mov r0, r5
    mov r1, r6
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215dcc_L144
    mov r0, r4
    bl native_fn_021ee9fc
    add r0, r4, #512
    ldrsb r1, [r0, #52]
    mov r0, r4
    bl native_fn_021ee91c
ov001_02215dcc_L144:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_02215dcc_L110
    ldr r0, =0x02242ba0
    mov r1, #12
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L168:
    ldr r0, =0x02242ba0
    mov r1, #10
    strb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L178:
    cmp r1, #10
    bne ov001_02215dcc_L19c
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_02215dcc_L3e8
    ldr r0, =0x02242ba0
    mov r1, #15
    strb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L19c:
    cmp r1, #12
    bne ov001_02215dcc_L1c4
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0]
    movhs r1, #15
    strhsb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L1c4:
    cmp r1, #15
    bne ov001_02215dcc_L268
    bl native_fn_02215d3c
    mov r2, r0
    mov r0, #1
    mov r3, r0
    mov r1, #0
    bl ov001_begin_state_transition_021f1354
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r0, #0
    bl native_fn_021d7f54
    bl native_fn_02215d84
    mov r9, #0
    mov r8, r0
    mov r5, r9
    mov r4, #1
    mov r7, r9
ov001_02215dcc_L210:
    mov r0, r7
    mov r1, r9
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215dcc_L244
    mov r0, r6
    mov r1, r8
    mov r2, r4
    mov r3, r5
    str r5, [sp]
    bl native_fn_021dbf98
ov001_02215dcc_L244:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_02215dcc_L210
    ldr r0, =0x02242ba0
    mov r1, #20
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L268:
    cmp r1, #20
    bne ov001_02215dcc_L308
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02215dcc_L3e8
    bl ov001_clear_state_flag4_021f14a4
    bl native_fn_02215d84
    cmp r0, #8
    bne ov001_02215dcc_L2f8
    mov r6, #0
    mov r5, r6
ov001_02215dcc_L2a0:
    mov r0, r5
    mov r1, r6
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215dcc_L2d4
    mov r0, r4
    bl native_fn_021ee9fc
    add r0, r4, #512
    ldrsb r1, [r0, #52]
    mov r0, r4
    bl native_fn_021ee91c
ov001_02215dcc_L2d4:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_02215dcc_L2a0
    ldr r0, =0x02242ba0
    mov r1, #27
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L2f8:
    ldr r0, =0x02242ba0
    mov r1, #25
    strb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L308:
    cmp r1, #25
    bne ov001_02215dcc_L32c
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_02215dcc_L3e8
    ldr r0, =0x02242ba0
    mov r1, #30
    strb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L32c:
    cmp r1, #27
    bne ov001_02215dcc_L354
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0]
    movhs r1, #30
    strhsb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L354:
    cmp r1, #30
    bne ov001_02215dcc_L394
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #24
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242ba0
    mov r1, #35
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L394:
    cmp r1, #35
    bne ov001_02215dcc_L3c8
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02215dcc_L3e8
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #40
    strb r1, [r0, #0x1]
    b ov001_02215dcc_L3e8
ov001_02215dcc_L3c8:
    cmp r1, #40
    bne ov001_02215dcc_L3e8
    mov r1, #0
    strb r1, [r0, #0x1]
    mov r1, #4
    str r1, [r0, #0x8]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_02215dcc_L3e8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
