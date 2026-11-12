/* ov001 row 0x022112c4: 428 bytes.
 *
 * What it does: 106 instructions; 12 call(s) to 0x021f1a58, 0x021f1a44, 0x021f1a38, +9 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (106 instructions, 12 calls, 4 branches, 10 back edges, 1 literal slot).
 *
 *   pool +0x1a8 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x50 -> +0x80
 *   back edge +0x7c -> +0x4c
 *   branch +0xec -> +0x1a0
 *   branch +0x10c -> +0x12c
 *   branch +0x114 -> +0x12c
 *   branch +0x128 -> +0x144
 *   branch +0x148 -> +0x1a0
 *   back edge +0x19c -> +0x100
 *   test +0x20 cmp r0, #127
 *   test +0x4c cmp r0, #0
 *   test +0x80 cmp r7, #0
 *   test +0x98 cmp r6, #20
 *   test +0xa0 cmp r6, #236
 *   test +0xac cmp r5, #8
 *   test +0xb4 cmp r5, #184
 *   test +0xc0 cmp r4, #16
 *   test +0xe8 cmp r7, #1
 *   test +0x108 cmp r0, #1
 *   test +0x110 cmp r10, #0
 *   test +0x118 cmp r7, #1
 *   test +0x144 cmp r1, #0
 *   test +0x198 cmp r7, #1
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022112c4; the literal pool and
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


asm u32 native_ov001_022112c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r6, r1
    mov r5, r2
    mov r4, r3
    mov r7, #0
    bl native_fn_021f1a58
    str r0, [sp]
    cmp r0, #127
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_021f1a44
    mov r8, r0
    bl native_fn_021f1a38
    ldrb r1, [r8, #0x22]
    ldr r2, =0x66666667
    mov r0, r10
    add r1, r1, #1
    strb r1, [r8, #0x22]
    str r10, [r8, #0x2c]
ov001_022112c4_L4c:
    cmp r0, #0
    ble ov001_022112c4_L80
    ldrb r3, [r8, #0x22]
    smull r1, r11, r2, r0
    mov r0, r0, lsr #31
    add r11, r0, r11, asr #2
    mov r0, r11, lsl #16
    add r1, r7, #1
    mov r0, r0, asr #16
    and r7, r1, #255
    add r1, r3, #1
    strb r1, [r8, #0x22]
    b ov001_022112c4_L4c
ov001_022112c4_L80:
    cmp r7, #0
    ldreqb r0, [r8, #0x22]
    mov r1, #3
    addeq r0, r0, #1
    streqb r0, [r8, #0x22]
    mov r0, #1
    cmp r6, #20
    movlt r6, #20
    cmp r6, #236
    movgt r6, #236
    str r0, [r8]
    cmp r5, #8
    movlt r5, #8
    cmp r5, #184
    movgt r5, #184
    strh r6, [r8, #20]
    cmp r4, #16
    strh r5, [r8, #22]
    movhi r4, #16
    strb r4, [r8, #0x20]
    ldr r0, [sp]
    strb r1, [r8, #0x21]
    bl native_fn_021f1a90
    ldrb r0, [r8, #0x22]
    sub r0, r0, #1
    and r7, r0, #255
    cmp r7, #1
    blo ov001_022112c4_L1a0
    ldr r5, =0x66666667
    mov r11, #15
    mov r6, #0
    mov r4, #10
ov001_022112c4_L100:
    ldrb r0, [r8, #0x22]
    mov r1, r6
    cmp r0, #1
    bls ov001_022112c4_L12c
    cmp r10, #0
    ble ov001_022112c4_L12c
    cmp r7, #1
    movne r0, r11
    moveq r0, #5
    and r9, r0, #255
    b ov001_022112c4_L144
ov001_022112c4_L12c:
    ldr r0, [r8, #0x1c]
    mov r1, r7
    bl native_fn_0205f98c
    mov r1, #90
    bl native_fn_021f1ba0
    mov r1, #1
ov001_022112c4_L144:
    cmp r1, #0
    bne ov001_022112c4_L1a0
    ldr r0, [r8, #0x1c]
    mov r1, r7
    bl native_fn_0205f98c
    smull r1, r2, r5, r10
    mov r1, r10, lsr #31
    add r2, r1, r2, asr #2
    smull r1, r2, r4, r2
    sub r2, r10, r1
    add r1, r9, r2
    and r9, r1, #255
    mov r1, r9
    bl native_fn_021f1ba0
    smull r0, r1, r5, r10
    mov r0, r10, lsr #31
    add r1, r0, r1, asr #2
    mov r0, r1, lsl #16
    mov r10, r0, asr #16
    sub r0, r7, #1
    and r7, r0, #255
    cmp r7, #1
    bhs ov001_022112c4_L100
ov001_022112c4_L1a0:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
