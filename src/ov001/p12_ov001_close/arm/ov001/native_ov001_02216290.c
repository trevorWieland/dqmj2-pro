/* ov001 row 0x02216290: 464 bytes.
 *
 * What it does: 114 instructions; 19 call(s) to 0x021f1354, 0x021f1414, 0x021f1438, +16 more; loops (back edge at +0x24); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 19 calls (114 instructions, 19 calls, 16 branches, 17 back edges, 2 literal slots).
 *
 *   pool +0x1c8 -> constant 0x02242ba0 (image word 0x02242ba0)
 *   pool +0x1cc -> constant 0x02242bb4 (image word 0x02242bb4)
 *   branch +0x10 -> +0x64
 *   branch +0x60 -> +0x1c0
 *   branch +0x68 -> +0x8c
 *   branch +0x88 -> +0x1c0
 *   branch +0x90 -> +0xc0
 *   branch +0xa8 -> +0x1c0
 *   branch +0xbc -> +0x1c0
 *   branch +0xc4 -> +0xe4
 *   branch +0xe0 -> +0x1c0
 *   branch +0xe8 -> +0x10c
 *   branch +0x108 -> +0x1c0
 *   branch +0x110 -> +0x158
 *   branch +0x11c -> +0x1c0
 *   branch +0x154 -> +0x1c0
 *   branch +0x15c -> +0x18c
 *   branch +0x174 -> +0x1c0
 *   branch +0x188 -> +0x1c0
 *   branch +0x190 -> +0x1c0
 *   test +0x0c cmp r1, #0
 *   test +0x64 cmp r1, #5
 *   test +0x8c cmp r1, #10
 *   test +0xa4 cmp r1, #30
 *   test +0xc0 cmp r1, #15
 *   test +0xe4 cmp r1, #20
 *   test +0xf8 cmp r1, #30
 *   test +0x10c cmp r1, #25
 *   test +0x118 cmp r0, #0
 *   test +0x158 cmp r1, #30
 *   test +0x170 cmp r1, #30
 *   test +0x18c cmp r1, #100
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02216290; the literal pool and
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

extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_021d7f54(void);
extern void native_fn_022161c0(void);
extern void native_fn_02041898(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_0221621c(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_02216290 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242ba0
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov001_02216290_L64
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #31
    bl ov001_begin_state_transition_021f1354
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242bb4
    bl native_fn_0202ac08
    mov r0, #131
    mov r1, #0
    bl native_fn_021eea10
    mov r0, #0
    bl native_fn_021d7f54
    bl native_fn_022161c0
    ldr r0, =0x02242ba0
    mov r1, #5
    strb r1, [r0, #0x1]
    b ov001_02216290_L1c0
ov001_02216290_L64:
    cmp r1, #5
    bne ov001_02216290_L8c
    mov r0, #0
    bl native_fn_02041898
    ldr r0, =0x02242ba0
    mov r1, #10
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216290_L1c0
ov001_02216290_L8c:
    cmp r1, #10
    bne ov001_02216290_Lc0
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02216290_L1c0
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #15
    strb r1, [r0, #0x1]
    b ov001_02216290_L1c0
ov001_02216290_Lc0:
    cmp r1, #15
    bne ov001_02216290_Le4
    bl native_fn_0221621c
    ldr r0, =0x02242ba0
    mov r1, #20
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216290_L1c0
ov001_02216290_Le4:
    cmp r1, #20
    bne ov001_02216290_L10c
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0]
    movhs r1, #25
    strhsb r1, [r0, #0x1]
    b ov001_02216290_L1c0
ov001_02216290_L10c:
    cmp r1, #25
    bne ov001_02216290_L158
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_02216290_L1c0
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #24
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242ba0
    mov r1, #30
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216290_L1c0
ov001_02216290_L158:
    cmp r1, #30
    bne ov001_02216290_L18c
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02216290_L1c0
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #100
    strb r1, [r0, #0x1]
    b ov001_02216290_L1c0
ov001_02216290_L18c:
    cmp r1, #100
    bne ov001_02216290_L1c0
    mov r0, #131
    bl native_fn_021eeb70
    ldr r0, =0x02242bb4
    bl native_fn_0202ac4c
    ldr r0, =0x02242ba0
    mov r1, #0
    strb r1, [r0, #0x1]
    mov r1, #4
    str r1, [r0, #0x8]
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_02216290_L1c0:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
