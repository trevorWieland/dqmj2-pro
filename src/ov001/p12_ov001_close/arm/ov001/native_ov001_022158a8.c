/* ov001 row 0x022158a8: 544 bytes.
 *
 * What it does: 135 instructions; 20 call(s) to 0x02215760, 0x021d7f54, 0x021f1354, +17 more; loops (back edge at +0x18); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 20 calls (135 instructions, 20 calls, 28 branches, 18 back edges, 1 literal slot).
 *
 *   pool +0x21c -> constant 0x02242ba0 (image word 0x02242ba0)
 *   branch +0x14 -> +0x98
 *   branch +0x30 -> +0x68
 *   branch +0x34 -> +0x68
 *   branch +0x38 -> +0x68
 *   branch +0x3c -> +0x54
 *   branch +0x40 -> +0x54
 *   branch +0x44 -> +0x68
 *   branch +0x48 -> +0x68
 *   branch +0x4c -> +0x5c
 *   branch +0x50 -> +0x64
 *   branch +0x58 -> +0x68
 *   branch +0x60 -> +0x68
 *   branch +0x94 -> +0x214
 *   branch +0x9c -> +0xc4
 *   branch +0xc0 -> +0x214
 *   branch +0xc8 -> +0xf4
 *   branch +0xe0 -> +0x214
 *   branch +0xf0 -> +0x214
 *   branch +0xf8 -> +0x118
 *   branch +0x104 -> +0x214
 *   branch +0x114 -> +0x214
 *   branch +0x11c -> +0x18c
 *   branch +0x188 -> +0x214
 *   branch +0x190 -> +0x1c8
 *   branch +0x1b4 -> +0x214
 *   branch +0x1c4 -> +0x214
 *   branch +0x1cc -> +0x1fc
 *   branch +0x1e4 -> +0x214
 *   branch +0x1f8 -> +0x214
 *   branch +0x200 -> +0x214
 *   test +0x10 cmp r1, #0
 *   test +0x28 cmp r0, #7
 *   test +0x98 cmp r1, #10
 *   test +0xc4 cmp r1, #20
 *   test +0xdc cmp r1, #30
 *   test +0xf4 cmp r1, #25
 *   test +0x100 cmp r0, #0
 *   test +0x118 cmp r1, #30
 *   test +0x144 cmp r0, #0
 *   test +0x18c cmp r1, #40
 *   test +0x1b0 cmp r0, #0
 *   test +0x1c8 cmp r1, #50
 *   test +0x1e0 cmp r1, #60
 *   test +0x1fc cmp r1, #100
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022158a8; the literal pool and
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

extern void native_fn_02215760(void);
extern void native_fn_021d7f54(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_02215780(void);
extern void native_fn_02041898(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f14e4(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);


asm u32 native_ov001_022158a8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x02242ba0
    mov r4, #0
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov001_022158a8_L98
    bl native_fn_02215760
    bl native_fn_021d7f54
    ldr r0, =0x02242ba0
    ldrb r0, [r0, #0x2]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b ov001_022158a8_L68
    b ov001_022158a8_L68
    b ov001_022158a8_L68
    b ov001_022158a8_L54
    b ov001_022158a8_L54
    b ov001_022158a8_L68
    b ov001_022158a8_L68
    b ov001_022158a8_L5c
    b ov001_022158a8_L64
ov001_022158a8_L54:
    mov r4, #23
    b ov001_022158a8_L68
ov001_022158a8_L5c:
    mov r4, #27
    b ov001_022158a8_L68
ov001_022158a8_L64:
    mov r4, #28
ov001_022158a8_L68:
    mov r0, #1
    mov r2, r4
    mov r3, r0
    mov r1, #0
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242ba0
    mov r1, #10
    strb r1, [r0, #0x1]
    b ov001_022158a8_L214
ov001_022158a8_L98:
    cmp r1, #10
    bne ov001_022158a8_Lc4
    bl native_fn_02215780
    mov r0, r4
    bl native_fn_02041898
    ldr r0, =0x02242ba0
    mov r1, #20
    strb r1, [r0, #0x1]
    mov r1, r4
    strb r1, [r0]
    b ov001_022158a8_L214
ov001_022158a8_Lc4:
    cmp r1, #20
    bne ov001_022158a8_Lf4
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_022158a8_L214
    mov r1, #25
    strb r1, [r0, #0x1]
    bl ov001_clear_state_flag4_021f14a4
    b ov001_022158a8_L214
ov001_022158a8_Lf4:
    cmp r1, #25
    bne ov001_022158a8_L118
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_022158a8_L214
    ldr r0, =0x02242ba0
    mov r1, #30
    strb r1, [r0, #0x1]
    b ov001_022158a8_L214
ov001_022158a8_L118:
    cmp r1, #30
    bne ov001_022158a8_L18c
    bl native_fn_02215760
    movs r4, r0
    moveq r0, #1
    movne r0, #0
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r1, r4
    mov r0, #0
    bl native_fn_021dbb14
    cmp r0, #0
    ldrne r0, =0x02242ba0
    movne r1, #40
    ldreq r0, =0x02242ba0
    moveq r1, #50
    strb r1, [r0, #0x1]
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #24
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242ba0
    mov r1, #0
    strb r1, [r0]
    b ov001_022158a8_L214
ov001_022158a8_L18c:
    cmp r1, #40
    bne ov001_022158a8_L1c8
    ldrb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    bl native_fn_02215760
    mov r1, r0
    mov r0, r4
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_022158a8_L214
    ldr r0, =0x02242ba0
    mov r1, #50
    strb r1, [r0, #0x1]
    b ov001_022158a8_L214
ov001_022158a8_L1c8:
    cmp r1, #50
    bne ov001_022158a8_L1fc
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #60
    blo ov001_022158a8_L214
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #100
    strb r1, [r0, #0x1]
    b ov001_022158a8_L214
ov001_022158a8_L1fc:
    cmp r1, #100
    bne ov001_022158a8_L214
    mov r1, #4
    str r1, [r0, #0x8]
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_022158a8_L214:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
