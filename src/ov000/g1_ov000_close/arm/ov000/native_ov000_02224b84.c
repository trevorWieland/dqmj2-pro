/* ov000 row 0x02224b84: 692 bytes.
 *
 * What it does: 169 instructions; 11 call(s) to 0x0205e7a8, 0x02224c2c, 0x02224de4, +8 more; loops (back edge at +0x70); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x2a4 -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x2a8 -> native_data_0222feb4 (image word 0x0222feb4)
 *   pool +0x2ac -> constant 0x02246aa8 (image word 0x02246aa8)
 *   pool +0x2b0 -> constant 0x02246c84 (image word 0x02246c84)
 *   branch +0x3c -> +0x78
 *   branch +0x4c -> +0x60
 *   branch +0x5c -> +0x29c
 *   branch +0x64 -> +0x29c
 *   branch +0x74 -> +0x29c
 *   branch +0x80 -> +0xb4
 *   branch +0x88 -> +0xa8
 *   branch +0x8c -> +0x140
 *   branch +0x94 -> +0x198
 *   branch +0xa4 -> +0x260
 *   branch +0xac -> +0xd4
 *   branch +0xb0 -> +0x260
 *   branch +0xb8 -> +0x260
 *   branch +0xc0 -> +0x260
 *   branch +0xc4 -> +0x210
 *   branch +0xcc -> +0x1c8
 *   branch +0xd0 -> +0x260
 *   branch +0xdc -> +0xf4
 *   branch +0xe4 -> +0x108
 *   branch +0xec -> +0x12c
 *   branch +0xf0 -> +0x260
 *   branch +0x104 -> +0x260
 *   branch +0x128 -> +0x260
 *   branch +0x13c -> +0x260
 *   branch +0x148 -> +0x160
 *   branch +0x150 -> +0x170
 *   branch +0x158 -> +0x184
 *   branch +0x15c -> +0x260
 *   branch +0x16c -> +0x260
 *   branch +0x180 -> +0x260
 *   branch +0x194 -> +0x260
 *   branch +0x1c4 -> +0x260
 *   branch +0x1d0 -> +0x1e0
 *   branch +0x1d8 -> +0x1f0
 *   branch +0x1dc -> +0x200
 *   branch +0x1ec -> +0x200
 *   branch +0x20c -> +0x260
 *   branch +0x218 -> +0x240
 *   branch +0x23c -> +0x254
 *   branch +0x268 -> +0x27c
 *   branch +0x278 -> +0x298
 *   branch +0x280 -> +0x298
 *   test +0x30 cmp r3, #29
 *   test +0x48 cmp r0, #2
 *   test +0x60 cmp r10, #0
 *   test +0x78 cmp r1, #17
 *   test +0x84 cmp r1, #11
 *   test +0x90 cmp r1, #16
 *   test +0x98 cmp r1, #17
 *   test +0xa8 cmp r1, #2
 *   test +0xb4 cmp r1, #23
 *   test +0xbc cmp r1, #22
 *   test +0xc8 cmp r1, #23
 *   test +0xe0 cmp r9, #1
 *   test +0xe8 cmp r9, #2
 *   test +0x14c cmp r9, #1
 *   test +0x154 cmp r9, #2
 *   test +0x1a4 cmp r0, #0
 *   test +0x1d4 cmp r9, #1
 *   test +0x214 cmp r0, #0
 *   test +0x224 cmp r0, #0
 *   test +0x264 cmp r0, #2
 *   test +0x27c cmp r10, #0
 *   test +0x284 cmp r8, #0
 *   0 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224b84; the literal pool and
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

extern u8 native_data_0222feb4[];
extern void native_fn_0205e7a8(void);
extern void native_fn_01ffb368(void);
extern void native_fn_022249b0(void);
extern void native_fn_02061260(void);


asm u32 native_ov000_02224b84 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r2, =0x022468b8
    ldr r7, =native_data_0222feb4
    ldrsb r1, [r2, #24]
    mov r10, r0
    mov r4, #5
    add r0, r1, r1, lsl #2
    add r5, r7, r0
    ldrsb r3, [r5, #2]
    ldr r11, =0x02246aa8
    ldr r6, =0x02246c84
    add r0, r3, r3, lsl #2
    cmp r3, #29
    add r7, r7, r0
    mov r8, #1
    beq ov000_02224b84_L78
    ldrsb r0, [r5]
    strb r3, [r2, #0x1a]
    cmp r0, #2
    bne ov000_02224b84_L60
    ldrb r0, [r5, #0x3]
    mov r0, r0, lsl #28
    movs r0, r0, lsr #28
    bne ov000_02224b84_L29c
ov000_02224b84_L60:
    cmp r10, #0
    beq ov000_02224b84_L29c
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    b ov000_02224b84_L29c
ov000_02224b84_L78:
    cmp r1, #17
    mov r9, #0
    bgt ov000_02224b84_Lb4
    cmp r1, #11
    blt ov000_02224b84_La8
    beq ov000_02224b84_L140
    cmp r1, #16
    beq ov000_02224b84_L198
    cmp r1, #17
    moveq r0, #20
    streqb r0, [r2, #0x1a]
    b ov000_02224b84_L260
ov000_02224b84_La8:
    cmp r1, #2
    beq ov000_02224b84_Ld4
    b ov000_02224b84_L260
ov000_02224b84_Lb4:
    cmp r1, #23
    bgt ov000_02224b84_L260
    cmp r1, #22
    blt ov000_02224b84_L260
    beq ov000_02224b84_L210
    cmp r1, #23
    beq ov000_02224b84_L1c8
    b ov000_02224b84_L260
ov000_02224b84_Ld4:
    bl native_fn_01ffb368
    movs r9, r0
    beq ov000_02224b84_Lf4
    cmp r9, #1
    beq ov000_02224b84_L108
    cmp r9, #2
    beq ov000_02224b84_L12c
    b ov000_02224b84_L260
ov000_02224b84_Lf4:
    ldr r0, =0x022468b8
    mov r1, #3
    strb r1, [r0, #0x1a]
    mov r4, #6
    b ov000_02224b84_L260
ov000_02224b84_L108:
    ldr r0, =0x022468b8
    mov r2, #4
    mov r1, #3
    strb r2, [r0, #0x1a]
    mov r2, #0
    strb r2, [r0, #0x1b]
    strb r1, [r6, #0x18d]
    strb r1, [r11, #0x18d]
    b ov000_02224b84_L260
ov000_02224b84_L12c:
    ldr r0, =0x022468b8
    mov r1, r4
    strb r1, [r0, #0x1a]
    mov r8, #0
    b ov000_02224b84_L260
ov000_02224b84_L140:
    bl native_fn_01ffb368
    movs r9, r0
    beq ov000_02224b84_L160
    cmp r9, #1
    beq ov000_02224b84_L170
    cmp r9, #2
    beq ov000_02224b84_L184
    b ov000_02224b84_L260
ov000_02224b84_L160:
    ldr r0, =0x022468b8
    mov r1, #12
    strb r1, [r0, #0x1a]
    b ov000_02224b84_L260
ov000_02224b84_L170:
    ldr r0, =0x022468b8
    mov r1, #15
    strb r1, [r0, #0x1a]
    mov r4, #6
    b ov000_02224b84_L260
ov000_02224b84_L184:
    ldr r0, =0x022468b8
    mov r1, #13
    strb r1, [r0, #0x1a]
    mov r8, #0
    b ov000_02224b84_L260
ov000_02224b84_L198:
    ldrsh r0, [r6, #24]
    mov r3, #0
    mov r1, #82
    cmp r0, #0
    movne r0, #17
    moveq r0, #20
    strb r0, [r2, #0x1a]
    ldr r2, =0x022468b8
    sub r0, r3, #1
    strb r3, [r2, #0x20]
    bl native_fn_0205e7a8
    b ov000_02224b84_L260
ov000_02224b84_L1c8:
    bl native_fn_01ffb368
    movs r9, r0
    beq ov000_02224b84_L1e0
    cmp r9, #1
    beq ov000_02224b84_L1f0
    b ov000_02224b84_L200
ov000_02224b84_L1e0:
    ldr r0, =0x022468b8
    mov r1, #24
    strb r1, [r0, #0x1a]
    b ov000_02224b84_L200
ov000_02224b84_L1f0:
    ldr r0, =0x022468b8
    mov r1, #25
    strb r1, [r0, #0x1a]
    mov r8, #0
ov000_02224b84_L200:
    mov r0, #127
    strb r0, [r11, #0x18c]
    bl native_fn_022249b0
    b ov000_02224b84_L260
ov000_02224b84_L210:
    ldrb r0, [r2, #0x20]
    cmp r0, #0
    bne ov000_02224b84_L240
    ldrsh r0, [r11, #24]
    mov r1, #1
    cmp r0, #0
    movne r0, #18
    moveq r0, #20
    strb r0, [r2, #0x1a]
    ldr r0, =0x022468b8
    strb r1, [r0, #0x20]
    b ov000_02224b84_L254
ov000_02224b84_L240:
    mov r0, r9
    bl native_fn_02061260
    ldr r0, =0x022468b8
    mov r1, #23
    strb r1, [r0, #0x1a]
ov000_02224b84_L254:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
ov000_02224b84_L260:
    ldrsb r0, [r5]
    cmp r0, #2
    bne ov000_02224b84_L27c
    ldrb r0, [r7, #0x4]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    bne ov000_02224b84_L298
ov000_02224b84_L27c:
    cmp r10, #0
    beq ov000_02224b84_L298
    cmp r8, #0
    movne r1, #82
    moveq r1, #83
    mvn r0, #0
    bl native_fn_0205e7a8
ov000_02224b84_L298:
    strb r9, [r6, #0x18c]
ov000_02224b84_L29c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
