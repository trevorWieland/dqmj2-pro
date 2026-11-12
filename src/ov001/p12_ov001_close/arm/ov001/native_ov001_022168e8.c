/* ov001 row 0x022168e8: 476 bytes.
 *
 * What it does: 118 instructions; 18 call(s) to 0x021db438, 0x02216964, 0x021db8d0, +15 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (118 instructions, 18 calls, 13 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x1d8 -> constant 0x02242bf4 (image word 0x02242bf4)
 *   branch +0x14 -> +0x124
 *   branch +0x20 -> +0x38
 *   branch +0x44 -> +0x7c
 *   branch +0x5c -> +0x6c
 *   back edge +0x78 -> +0x50
 *   branch +0xa4 -> +0x108
 *   branch +0xbc -> +0xf8
 *   branch +0xc8 -> +0xf8
 *   back edge +0x104 -> +0xb0
 *   branch +0x120 -> +0x1d0
 *   branch +0x128 -> +0x17c
 *   branch +0x134 -> +0x150
 *   branch +0x14c -> +0x1d0
 *   branch +0x178 -> +0x1d0
 *   branch +0x180 -> +0x1ac
 *   branch +0x198 -> +0x1d0
 *   branch +0x1a8 -> +0x1d0
 *   branch +0x1b0 -> +0x1d0
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r8, #0
 *   test +0x40 cmp r6, #0
 *   test +0x58 cmp r0, #0
 *   test +0x64 tst r0, #2
 *   test +0x70 cmp r5, r6
 *   test +0x7c cmp r7, #0
 *   test +0x9c cmp r6, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xc4 tst r0, #2
 *   test +0xfc cmp r7, r6
 *   test +0x124 cmp r0, #5
 *   test +0x130 cmp r0, #0
 *   test +0x148 cmp r1, #5
 *   test +0x17c cmp r0, #10
 *   test +0x194 cmp r0, #40
 *   test +0x1ac cmp r0, #20
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022168e8; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_022168ac(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f14e4(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_022168d0(void);


asm u32 native_ov001_022168e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r2, =0x02242bf4
    mov r8, r0
    ldrsb r0, [r2, #1]
    cmp r0, #0
    bne ov001_022168e8_L124
    cmp r8, #0
    movne r6, #1
    bne ov001_022168e8_L38
    mov r0, r1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r8, r0
    mov r6, #3
ov001_022168e8_L38:
    mov r7, #0
    mov r5, r7
    cmp r6, #0
    ble ov001_022168e8_L7c
    mov r9, r8
    mov r4, #1
ov001_022168e8_L50:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022168e8_L6c
    ldr r0, [r9, #0x33c]
    tst r0, #2
    movne r7, r4
ov001_022168e8_L6c:
    add r5, r5, #1
    cmp r5, r6
    add r9, r9, #1088
    blt ov001_022168e8_L50
ov001_022168e8_L7c:
    cmp r7, #0
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    mov r0, #252
    bl native_fn_022168ac
    mov r0, #252
    bl native_fn_0205d790
    mov r5, r0
    cmp r6, #0
    mov r7, #0
    ble ov001_022168e8_L108
    mov r4, #252
    mov r9, r7
ov001_022168e8_Lb0:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022168e8_Lf8
    ldr r0, [r8, #0x33c]
    tst r0, #2
    beq ov001_022168e8_Lf8
    mov r0, r4
    mov r1, r8
    mov r2, r5
    bl ov001_effect_resource_create_021eec7c
    ldr r0, [r8, #0x33c]
    mov r2, r9
    bic r0, r0, #2
    str r0, [r8, #0x33c]
    ldrb r0, [r8, #0x31e]
    ldrb r1, [r8, #0x31f]
    bl native_fn_022024d4
ov001_022168e8_Lf8:
    add r7, r7, #1
    cmp r7, r6
    add r8, r8, #1088
    blt ov001_022168e8_Lb0
ov001_022168e8_L108:
    ldr r0, =0x02242bf4
    mov r1, #5
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    str r1, [r0, #0xc]
    b ov001_022168e8_L1d0
ov001_022168e8_L124:
    cmp r0, #5
    bne ov001_022168e8_L17c
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_022168e8_L150
    ldr r0, =0x02242bf4
    ldr r1, [r0, #0xc]
    add r1, r1, #1
    str r1, [r0, #0xc]
    cmp r1, #5
    blt ov001_022168e8_L1d0
ov001_022168e8_L150:
    mov r0, #11
    mov r1, #0
    mov r2, #47
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242bf4
    mov r1, #10
    strb r1, [r0, #0x1]
    b ov001_022168e8_L1d0
ov001_022168e8_L17c:
    cmp r0, #10
    bne ov001_022168e8_L1ac
    ldrsb r0, [r2]
    add r0, r0, #1
    strb r0, [r2]
    ldrsb r0, [r2]
    cmp r0, #40
    blt ov001_022168e8_L1d0
    mov r0, #20
    strb r0, [r2, #0x1]
    bl ov001_clear_state_flag4_021f14a4
    b ov001_022168e8_L1d0
ov001_022168e8_L1ac:
    cmp r0, #20
    bne ov001_022168e8_L1d0
    mov r0, #252
    bl native_fn_022168d0
    ldr r0, =0x02242bf4
    mov r1, #0
    strb r1, [r0, #0x1]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_022168e8_L1d0:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
