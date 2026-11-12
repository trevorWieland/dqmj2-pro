/* ov001 row 0x02210f64: 864 bytes.
 *
 * What it does: 215 instructions; 20 call(s) to 0x021f1a58, 0x021f1a44, 0x021f1a38, +17 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 20 calls (215 instructions, 20 calls, 49 branches, 17 back edges, 1 literal slot).
 *
 *   pool +0x35c -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x5c -> +0x90
 *   back edge +0x8c -> +0x64
 *   branch +0xa8 -> +0xf0
 *   branch +0xb4 -> +0x110
 *   branch +0xb8 -> +0xfc
 *   branch +0xbc -> +0xfc
 *   branch +0xc0 -> +0x108
 *   branch +0xc4 -> +0x108
 *   branch +0xc8 -> +0x108
 *   branch +0xcc -> +0x110
 *   branch +0xd0 -> +0x110
 *   branch +0xd4 -> +0x110
 *   branch +0xd8 -> +0x110
 *   branch +0xdc -> +0x110
 *   branch +0xe0 -> +0x110
 *   branch +0xe4 -> +0x110
 *   branch +0xe8 -> +0x110
 *   branch +0xec -> +0xfc
 *   branch +0xf4 -> +0x108
 *   branch +0xf8 -> +0x110
 *   branch +0x104 -> +0x110
 *   branch +0x170 -> +0x18c
 *   branch +0x19c -> +0x34c
 *   branch +0x1ac -> +0x1f4
 *   branch +0x1b8 -> +0x2d4
 *   branch +0x1bc -> +0x200
 *   branch +0x1c0 -> +0x200
 *   branch +0x1c4 -> +0x288
 *   branch +0x1c8 -> +0x29c
 *   branch +0x1cc -> +0x2b0
 *   branch +0x1d0 -> +0x2d4
 *   branch +0x1d4 -> +0x2d4
 *   branch +0x1d8 -> +0x2d4
 *   branch +0x1dc -> +0x2d4
 *   branch +0x1e0 -> +0x2d4
 *   branch +0x1e4 -> +0x2d4
 *   branch +0x1e8 -> +0x2d4
 *   branch +0x1ec -> +0x2d4
 *   branch +0x1f0 -> +0x244
 *   branch +0x1f8 -> +0x2c4
 *   branch +0x1fc -> +0x2d4
 *   branch +0x208 -> +0x228
 *   branch +0x210 -> +0x228
 *   branch +0x224 -> +0x2d4
 *   branch +0x240 -> +0x2d4
 *   branch +0x24c -> +0x26c
 *   branch +0x254 -> +0x26c
 *   branch +0x268 -> +0x2d4
 *   branch +0x284 -> +0x2d4
 *   branch +0x298 -> +0x2d4
 *   branch +0x2ac -> +0x2d4
 *   branch +0x2c0 -> +0x2d4
 *   branch +0x2d8 -> +0x34c
 *   back edge +0x348 -> +0x1a4
 *   test +0x20 cmp r0, #127
 *   test +0x38 cmp r9, #0
 *   test +0x58 cmp r9, #0
 *   test +0x90 cmp r7, #0
 *   test +0xa4 cmp r7, #98
 *   test +0xf0 cmp r7, #119
 *   test +0x110 cmp r8, #20
 *   test +0x118 cmp r8, #236
 *   test +0x120 cmp r5, #8
 *   test +0x128 cmp r5, #184
 *   test +0x134 cmp r10, #16
 *   test +0x168 cmp r9, #0
 *   test +0x198 cmp r8, r5
 *   test +0x1a4 cmp r7, #98
 *   test +0x1b0 cmp r10, #0
 *   test +0x1f4 cmp r7, #119
 *   test +0x204 cmp r0, #1
 *   test +0x20c cmp r9, #0
 *   test +0x214 cmp r8, r5
 *   test +0x248 cmp r0, #1
 *   test +0x250 cmp r9, #0
 *   test +0x258 cmp r8, r5
 *   test +0x288 cmp r8, r5
 *   test +0x29c cmp r8, r5
 *   test +0x2b0 cmp r8, r5
 *   test +0x2c4 cmp r8, r5
 *   test +0x2d4 cmp r1, #0
 *   test +0x344 cmp r8, r5
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02210f64; the literal pool and
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

extern void native_fn_021f1a58(void);
extern void native_fn_021f1a44(void);
extern void native_fn_021f1a38(void);
extern void native_fn_021f1a90(void);
extern void native_fn_0205f98c(void);
extern void native_fn_021f1ba0(void);
extern void native_fn_0201af84(void);


asm u32 native_ov001_02210f64 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r9, r0
    mov r8, r1
    mov r5, r2
    mov r10, r3
    mov r7, #0
    bl native_fn_021f1a58
    str r0, [sp]
    cmp r0, #127
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_021f1a44
    mov r4, r0
    bl native_fn_021f1a38
    ldrb r0, [r4, #0x22]
    cmp r9, #0
    mov r3, r9
    add r0, r0, #1
    strb r0, [r4, #0x22]
    str r9, [r4, #0x2c]
    ldrltb r0, [r4, #0x22]
    addlt r0, r0, #1
    strltb r0, [r4, #0x22]
    cmp r9, #0
    beq ov001_02210f64_L90
    ldr r0, =0x66666667
ov001_02210f64_L64:
    ldrb r1, [r4, #0x22]
    smull r11, r2, r0, r3
    mov r3, r3, lsr #31
    add r2, r3, r2, asr #2
    mov r2, r2, lsl #16
    add r7, r7, #1
    movs r3, r2, asr #16
    and r7, r7, #255
    add r1, r1, #1
    strb r1, [r4, #0x22]
    bne ov001_02210f64_L64
ov001_02210f64_L90:
    cmp r7, #0
    ldreqb r0, [r4, #0x22]
    ldrb r7, [sp, #0x28]
    addeq r0, r0, #1
    streqb r0, [r4, #0x22]
    cmp r7, #98
    bgt ov001_02210f64_Lf0
    subs r0, r7, #85
    addpl pc, pc, r0, lsl #2
    b ov001_02210f64_L110
    b ov001_02210f64_Lfc
    b ov001_02210f64_Lfc
    b ov001_02210f64_L108
    b ov001_02210f64_L108
    b ov001_02210f64_L108
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_L110
    b ov001_02210f64_Lfc
ov001_02210f64_Lf0:
    cmp r7, #119
    beq ov001_02210f64_L108
    b ov001_02210f64_L110
ov001_02210f64_Lfc:
    mov r0, #0
    str r0, [r4]
    b ov001_02210f64_L110
ov001_02210f64_L108:
    mov r0, #3
    str r0, [r4]
ov001_02210f64_L110:
    cmp r8, #20
    movlt r8, #20
    cmp r8, #236
    movgt r8, #236
    cmp r5, #8
    movlt r5, #8
    cmp r5, #184
    movgt r5, #184
    strh r8, [r4, #20]
    cmp r10, #16
    strh r5, [r4, #22]
    movhi r10, #16
    strb r10, [r4, #0x20]
    ldr r0, [sp]
    mov r1, #3
    strb r1, [r4, #0x21]
    bl native_fn_021f1a90
    ldr r0, [r4, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldrb r1, [sp, #0x28]
    bl native_fn_021f1ba0
    cmp r9, #0
    mov r5, #1
    bge ov001_02210f64_L18c
    ldr r0, [r4, #0x1c]
    mov r1, r5
    bl native_fn_0205f98c
    mov r1, #120
    bl native_fn_021f1ba0
    add r5, r5, #1
ov001_02210f64_L18c:
    ldrb r0, [r4, #0x22]
    sub r0, r0, #1
    and r8, r0, #255
    cmp r8, r5
    blt ov001_02210f64_L34c
    sub r10, r7, #85
ov001_02210f64_L1a4:
    cmp r7, #98
    mov r1, #0
    bgt ov001_02210f64_L1f4
    cmp r10, #0
    addge pc, pc, r10, lsl #2
    b ov001_02210f64_L2d4
    b ov001_02210f64_L200
    b ov001_02210f64_L200
    b ov001_02210f64_L288
    b ov001_02210f64_L29c
    b ov001_02210f64_L2b0
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L2d4
    b ov001_02210f64_L244
ov001_02210f64_L1f4:
    cmp r7, #119
    beq ov001_02210f64_L2c4
    b ov001_02210f64_L2d4
ov001_02210f64_L200:
    ldrb r0, [r4, #0x22]
    cmp r0, #1
    bls ov001_02210f64_L228
    cmp r9, #0
    ble ov001_02210f64_L228
    cmp r8, r5
    movne r0, #15
    moveq r0, #5
    and r6, r0, #255
    b ov001_02210f64_L2d4
ov001_02210f64_L228:
    ldr r0, [r4, #0x1c]
    mov r1, r8
    bl native_fn_0205f98c
    mov r1, #90
    bl native_fn_021f1ba0
    mov r1, #1
    b ov001_02210f64_L2d4
ov001_02210f64_L244:
    ldrb r0, [r4, #0x22]
    cmp r0, #1
    bls ov001_02210f64_L26c
    cmp r9, #0
    ble ov001_02210f64_L26c
    cmp r8, r5
    movne r0, #109
    moveq r0, #99
    and r6, r0, #255
    b ov001_02210f64_L2d4
ov001_02210f64_L26c:
    ldr r0, [r4, #0x1c]
    mov r1, r8
    bl native_fn_0205f98c
    mov r1, #90
    bl native_fn_021f1ba0
    mov r1, #1
    b ov001_02210f64_L2d4
ov001_02210f64_L288:
    cmp r8, r5
    movne r0, #75
    moveq r0, #65
    and r6, r0, #255
    b ov001_02210f64_L2d4
ov001_02210f64_L29c:
    cmp r8, r5
    movne r0, #35
    moveq r0, #25
    and r6, r0, #255
    b ov001_02210f64_L2d4
ov001_02210f64_L2b0:
    cmp r8, r5
    movne r0, #55
    moveq r0, #45
    and r6, r0, #255
    b ov001_02210f64_L2d4
ov001_02210f64_L2c4:
    cmp r8, r5
    movne r0, #131
    moveq r0, #121
    and r6, r0, #255
ov001_02210f64_L2d4:
    cmp r1, #0
    bne ov001_02210f64_L34c
    ldr r0, [r4, #0x1c]
    mov r1, r8
    bl native_fn_0205f98c
    mov r11, r0
    mov r0, r9
    bl native_fn_0201af84
    ldr r2, =0x66666667
    smull r3, r1, r2, r0
    mov r2, r0, lsr #31
    add r1, r2, r1, asr #2
    mov r2, #10
    smull r1, r3, r2, r1
    sub r1, r0, r1
    add r0, r6, r1
    and r6, r0, #255
    mov r0, r11
    mov r1, r6
    bl native_fn_021f1ba0
    ldr r0, =0x66666667
    smull r1, r2, r0, r9
    mov r0, r9, lsr #31
    add r2, r0, r2, asr #2
    mov r0, r2, lsl #16
    mov r9, r0, asr #16
    sub r0, r8, #1
    and r8, r0, #255
    cmp r8, r5
    bge ov001_02210f64_L1a4
ov001_02210f64_L34c:
    ldrb r1, [sp, #0x28]
    ldr r0, [sp]
    str r1, [r4, #0x30]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
