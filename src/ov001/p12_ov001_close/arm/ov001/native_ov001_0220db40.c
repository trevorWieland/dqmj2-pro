/* ov001 row 0x0220db40: 812 bytes.
 *
 * What it does: 200 instructions; 27 call(s) to 0x0220d6f0, 0x021ee9fc, 0x021dbcbc, +24 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 27 calls (200 instructions, 27 calls, 23 branches, 23 back edges, 3 literal slots).
 *
 *   pool +0x320 -> constant 0x0223e0d8 (image word 0x0223e0d8)
 *   pool +0x324 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x328 -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x14 -> +0x80
 *   branch +0x50 -> +0x70
 *   branch +0x7c -> +0x318
 *   branch +0x84 -> +0x200
 *   branch +0x90 -> +0xd8
 *   branch +0x124 -> +0x18c
 *   branch +0x188 -> +0x318
 *   branch +0x1fc -> +0x318
 *   branch +0x204 -> +0x228
 *   branch +0x224 -> +0x318
 *   branch +0x22c -> +0x250
 *   branch +0x238 -> +0x240
 *   branch +0x24c -> +0x318
 *   branch +0x254 -> +0x278
 *   branch +0x274 -> +0x318
 *   branch +0x27c -> +0x2c4
 *   branch +0x2a0 -> +0x2b4
 *   branch +0x2b0 -> +0x318
 *   branch +0x2c0 -> +0x318
 *   branch +0x2c8 -> +0x2f0
 *   branch +0x2dc -> +0x318
 *   branch +0x2ec -> +0x318
 *   branch +0x2f4 -> +0x318
 *   branch +0x300 -> +0x318
 *   test +0x10 cmp r1, #0
 *   test +0x4c cmp r0, #0
 *   test +0x80 cmp r1, #10
 *   test +0x8c cmp r1, #0
 *   test +0x10c cmp r0, #0
 *   test +0x114 cmp r4, #100
 *   test +0x120 tst r0, #32
 *   test +0x200 cmp r1, #20
 *   test +0x214 cmp r1, #30
 *   test +0x228 cmp r1, #30
 *   test +0x234 cmp r0, #0
 *   test +0x250 cmp r1, #40
 *   test +0x264 cmp r1, #30
 *   test +0x278 cmp r1, #50
 *   test +0x29c cmp r0, #0
 *   test +0x2c4 cmp r1, #60
 *   test +0x2d8 cmp r0, #0
 *   test +0x2f0 cmp r1, #100
 *   test +0x2fc cmp r0, #0
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220db40; the literal pool and
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
extern void native_fn_021dbcbc(void);
extern void native_fn_0220f8b4(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_0203d294(void);
extern void native_fn_021dcda8(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021db718(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f94d8(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f14e4(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_0220f530(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);


asm u32 native_ov001_0220db40 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x0223e0d8
    mov r4, #0
    ldrb r1, [r0, #0x9]
    cmp r1, #0
    bne ov001_0220db40_L80
    bl native_fn_0220d6f0
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    bl native_fn_021ee9fc
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    bl native_fn_021dbcbc
    ldr r2, =0x0223e0d8
    mov r1, r0
    ldr r0, [r2, #0xc]
    ldr r0, [r0, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f8b4
    cmp r0, #0
    ble ov001_0220db40_L70
    mov r0, #11
    mov r1, r4
    mov r2, #14
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
ov001_0220db40_L70:
    ldr r0, =0x0223e0d8
    mov r1, #10
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L80:
    cmp r1, #10
    bne ov001_0220db40_L200
    ldrsb r1, [r0, #3]
    cmp r1, #0
    beq ov001_0220db40_Ld8
    ldr r0, [r0, #0xc]
    bl native_fn_021dbcbc
    mov r5, r0
    mov r0, #11
    bl native_fn_0203d294
    add r2, r5, #5
    ldr r3, =0x66666667
    mov r1, r2, lsr #31
    smull r2, r12, r3, r2
    add r12, r1, r12, asr #2
    add r0, r0, #90
    mul r1, r12, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    add r4, r4, r3
ov001_0220db40_Ld8:
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    bl native_fn_021dbcbc
    ldr r2, =0x0223e0d8
    mov r1, r0
    ldr r0, [r2, #0xc]
    ldr r0, [r0, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f8b4
    ldr r1, =0x0223e0d8
    add r4, r4, r0
    ldr r0, [r1, #0xc]
    bl native_fn_021dcda8
    cmp r0, #0
    movne r4, #0
    cmp r4, #100
    movgt r4, #100
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_0220db40_L18c
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    bl native_fn_021db718
    mov r4, r0
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    mov r2, #1
    bl native_fn_021ee7d4
    ldr r0, =0x0223e0d8
    rsb r2, r4, #0
    ldr r1, [r0, #0xc]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    mov r0, #19
    mov r1, #1
    bl native_fn_021f94d8
    ldr r0, =0x0223e0d8
    mov r1, #0
    strb r1, [r0, #0x8]
    mov r1, #20
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L18c:
    ldr r0, =0x0223e0d8
    rsb r1, r4, #0
    ldr r0, [r0, #0xc]
    bl native_fn_021db718
    mov r2, #0
    ldr r0, =0x0223e0d8
    str r2, [sp]
    ldr r0, [r0, #0xc]
    mov r1, r4
    sub r2, r2, #1
    mov r3, #1
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
    strb r1, [r0, #0x8]
    mov r1, #40
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L200:
    cmp r1, #20
    bne ov001_0220db40_L228
    ldrb r1, [r0, #0x8]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x8]
    movhi r1, #30
    strhib r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L228:
    cmp r1, #30
    bne ov001_0220db40_L250
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_0220db40_L240
    bl ov001_clear_state_flag4_021f14a4
ov001_0220db40_L240:
    ldr r0, =0x0223e0d8
    mov r1, #100
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L250:
    cmp r1, #40
    bne ov001_0220db40_L278
    ldrb r1, [r0, #0x8]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x8]
    movhi r1, #50
    strhib r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L278:
    cmp r1, #50
    bne ov001_0220db40_L2c4
    ldr r0, [r0, #0xc]
    mov r1, r4
    bl native_fn_0220f530
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_0220db40_L2b4
    ldr r0, =0x0223e0d8
    mov r1, #60
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L2b4:
    ldr r0, =0x0223e0d8
    mov r1, #30
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L2c4:
    cmp r1, #60
    bne ov001_0220db40_L2f0
    ldr r0, [r0, #0xc]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_0220db40_L318
    ldr r0, =0x0223e0d8
    mov r1, #30
    strb r1, [r0, #0x9]
    b ov001_0220db40_L318
ov001_0220db40_L2f0:
    cmp r1, #100
    bne ov001_0220db40_L318
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_0220db40_L318
    ldr r0, =0x0223e0d8
    mov r1, r4
    strb r1, [r0, #0x9]
    mov r1, #4
    strb r1, [r0, #0x2]
ov001_0220db40_L318:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
