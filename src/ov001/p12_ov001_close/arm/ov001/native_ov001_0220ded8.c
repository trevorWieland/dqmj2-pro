/* ov001 row 0x0220ded8: 496 bytes.
 *
 * What it does: 123 instructions; 19 call(s) to 0x0220d6f0, 0x021ee9fc, 0x021dbcf0, +16 more; loops (back edge at +0x1c); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 19 calls (123 instructions, 19 calls, 10 branches, 17 back edges, 1 literal slot).
 *
 *   pool +0x1ec -> constant 0x0223e0d8 (image word 0x0223e0d8)
 *   branch +0x18 -> +0x3c
 *   branch +0x38 -> +0x1e0
 *   branch +0x40 -> +0x184
 *   branch +0xa8 -> +0x110
 *   branch +0x10c -> +0x1e0
 *   branch +0x180 -> +0x1e0
 *   branch +0x188 -> +0x1b8
 *   branch +0x1a0 -> +0x1e0
 *   branch +0x1b4 -> +0x1e0
 *   branch +0x1bc -> +0x1e0
 *   branch +0x1c8 -> +0x1e0
 *   test +0x14 cmp r1, #0
 *   test +0x3c cmp r1, #10
 *   test +0x74 cmp r0, #0
 *   test +0x98 cmp r4, #50
 *   test +0xa4 tst r0, #32
 *   test +0x184 cmp r1, #20
 *   test +0x19c cmp r1, #30
 *   test +0x1b8 cmp r1, #100
 *   test +0x1c4 cmp r0, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220ded8; the literal pool and
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

extern void native_fn_0220d6f0(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_0220f91c(void);
extern void native_fn_021dcda8(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021db7cc(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f94d8(void);
extern void native_fn_021db834(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021d9494(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f14e4(void);


asm u32 native_ov001_0220ded8 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r0, =0x0223e0d8
    mov r4, #0
    ldrb r1, [r0, #0x7]
    cmp r1, #0
    bne ov001_0220ded8_L3c
    bl native_fn_0220d6f0
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    bl native_fn_021ee9fc
    ldr r0, =0x0223e0d8
    mov r1, #10
    strb r1, [r0, #0x7]
    b ov001_0220ded8_L1e0
ov001_0220ded8_L3c:
    cmp r1, #10
    bne ov001_0220ded8_L184
    ldr r0, [r0, #0xc]
    bl native_fn_021dbcf0
    ldr r2, =0x0223e0d8
    mov r1, r0
    ldr r0, [r2, #0xc]
    ldr r0, [r0, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f91c
    ldr r1, =0x0223e0d8
    add r4, r4, r0
    ldr r0, [r1, #0xc]
    bl native_fn_021dcda8
    cmp r0, #0
    mov r0, #11
    mov r1, #0
    mov r2, #15
    mov r3, #1
    movne r4, #0
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    cmp r4, #50
    movgt r4, #50
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_0220ded8_L110
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    bl native_fn_021db7cc
    mov r4, r0
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    mov r2, #2
    bl native_fn_021ee7d4
    ldr r0, =0x0223e0d8
    rsb r2, r4, #0
    ldr r1, [r0, #0xc]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    mov r0, #21
    mov r1, #0
    bl native_fn_021f94d8
    ldr r0, =0x0223e0d8
    mov r1, #0
    strb r1, [r0, #0x6]
    mov r1, #20
    strb r1, [r0, #0x7]
    b ov001_0220ded8_L1e0
ov001_0220ded8_L110:
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    bl native_fn_021db834
    mov r2, #0
    ldr r0, =0x0223e0d8
    str r2, [sp]
    ldr r0, [r0, #0xc]
    mov r1, r4
    sub r2, r2, #1
    mov r3, #2
    bl native_fn_021ee78c
    ldr r0, =0x0223e0d8
    mov r2, r4
    ldr r1, [r0, #0xc]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x0223e0d8
    mov r1, #4
    ldr r0, [r0, #0xc]
    mov r2, #1
    bl native_fn_021d9494
    ldr r0, =0x0223e0d8
    mov r1, #0
    strb r1, [r0, #0x6]
    mov r1, #20
    strb r1, [r0, #0x7]
    b ov001_0220ded8_L1e0
ov001_0220ded8_L184:
    cmp r1, #20
    bne ov001_0220ded8_L1b8
    ldrb r1, [r0, #0x6]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x6]
    cmp r1, #30
    bls ov001_0220ded8_L1e0
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x0223e0d8
    mov r1, #100
    strb r1, [r0, #0x7]
    b ov001_0220ded8_L1e0
ov001_0220ded8_L1b8:
    cmp r1, #100
    bne ov001_0220ded8_L1e0
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_0220ded8_L1e0
    ldr r0, =0x0223e0d8
    mov r1, r4
    strb r1, [r0, #0x7]
    mov r1, #9
    strb r1, [r0, #0x2]
ov001_0220ded8_L1e0:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
