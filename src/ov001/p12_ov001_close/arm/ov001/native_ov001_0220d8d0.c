/* ov001 row 0x0220d8d0: 504 bytes.
 *
 * What it does: 125 instructions; 14 call(s) to 0x021ee9fc, 0x0220d6f0, 0x021dbcbc, +11 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (125 instructions, 14 calls, 20 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x1f4 -> constant 0x0223e0d8 (image word 0x0223e0d8)
 *   branch +0x10 -> +0x30
 *   branch +0x2c -> +0x1ec
 *   branch +0x34 -> +0x54
 *   branch +0x50 -> +0x1ec
 *   branch +0x58 -> +0x134
 *   branch +0x80 -> +0x94
 *   branch +0x90 -> +0xd4
 *   branch +0x98 -> +0xb0
 *   branch +0xac -> +0xc0
 *   branch +0x130 -> +0x1ec
 *   branch +0x138 -> +0x15c
 *   branch +0x158 -> +0x1ec
 *   branch +0x160 -> +0x1a8
 *   branch +0x184 -> +0x198
 *   branch +0x194 -> +0x1ec
 *   branch +0x1a4 -> +0x1ec
 *   branch +0x1ac -> +0x1d4
 *   branch +0x1c0 -> +0x1ec
 *   branch +0x1d0 -> +0x1ec
 *   branch +0x1d8 -> +0x1ec
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r0, #5
 *   test +0x54 cmp r0, #10
 *   test +0x78 cmp r0, #0
 *   test +0x94 cmp r5, #2
 *   test +0x134 cmp r0, #20
 *   test +0x148 cmp r0, #30
 *   test +0x15c cmp r0, #30
 *   test +0x180 cmp r0, #0
 *   test +0x1a8 cmp r0, #40
 *   test +0x1bc cmp r0, #0
 *   test +0x1d4 cmp r0, #100
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220d8d0; the literal pool and
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

extern void native_fn_021ee9fc(void);
extern void native_fn_0220d6f0(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dcda8(void);
extern void native_fn_021f949c(void);
extern void native_fn_021d9494(void);
extern void native_fn_021db718(void);
extern void native_fn_021ee78c(void);
extern void native_fn_022024d4(void);
extern void native_fn_0220f530(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);


asm u32 native_ov001_0220d8d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x0223e0d8
    ldrb r0, [r1]
    cmp r0, #0
    bne ov001_0220d8d0_L30
    ldr r0, [r1, #0xc]
    add r0, r0, #256
    ldrsb r0, [r0, #228]
    cmp r0, #0
    moveq r0, #5
    streqb r0, [r1]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L30:
    cmp r0, #5
    bne ov001_0220d8d0_L54
    ldr r0, [r1, #0xc]
    bl native_fn_021ee9fc
    bl native_fn_0220d6f0
    ldr r0, =0x0223e0d8
    mov r1, #10
    strb r1, [r0]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L54:
    cmp r0, #10
    bne ov001_0220d8d0_L134
    ldr r0, [r1, #0xc]
    bl native_fn_021dbcbc
    ldr r1, =0x0223e0d8
    mov r4, r0
    ldr r0, [r1, #0xc]
    ldrsb r5, [r1, #1]
    bl native_fn_021dcda8
    cmp r0, #0
    mov r1, #1
    beq ov001_0220d8d0_L94
    mov r0, #242
    mov r4, #0
    bl native_fn_021f949c
    b ov001_0220d8d0_Ld4
ov001_0220d8d0_L94:
    cmp r5, #2
    bne ov001_0220d8d0_Lb0
    add r2, r4, #7
    mov r0, #239
    mov r4, r2, asr #3
    bl native_fn_021f949c
    b ov001_0220d8d0_Lc0
ov001_0220d8d0_Lb0:
    add r2, r4, #15
    mov r0, #238
    mov r4, r2, asr #4
    bl native_fn_021f949c
ov001_0220d8d0_Lc0:
    ldr r0, =0x0223e0d8
    mov r1, #4
    ldr r0, [r0, #0xc]
    mov r2, #1
    bl native_fn_021d9494
ov001_0220d8d0_Ld4:
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
    mov r1, #0
    strb r1, [r0, #0xa]
    mov r1, #20
    strb r1, [r0]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L134:
    cmp r0, #20
    bne ov001_0220d8d0_L15c
    ldrb r0, [r1, #0xa]
    add r2, r0, #1
    and r0, r2, #255
    cmp r0, #30
    strb r2, [r1, #0xa]
    movhi r0, #30
    strhib r0, [r1]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L15c:
    cmp r0, #30
    bne ov001_0220d8d0_L1a8
    ldr r0, [r1, #0xc]
    mov r1, #0
    bl native_fn_0220f530
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_0220d8d0_L198
    ldr r0, =0x0223e0d8
    mov r1, #40
    strb r1, [r0]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L198:
    ldr r0, =0x0223e0d8
    mov r1, #100
    strb r1, [r0]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L1a8:
    cmp r0, #40
    bne ov001_0220d8d0_L1d4
    ldr r0, [r1, #0xc]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_0220d8d0_L1ec
    ldr r0, =0x0223e0d8
    mov r1, #100
    strb r1, [r0]
    b ov001_0220d8d0_L1ec
ov001_0220d8d0_L1d4:
    cmp r0, #100
    bne ov001_0220d8d0_L1ec
    mov r0, #0
    strb r0, [r1]
    mov r0, #2
    strb r0, [r1, #0x2]
ov001_0220d8d0_L1ec:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
