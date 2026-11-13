/* ov001 row 0x02225ee4: 328 bytes.
 *
 * What it does: 82 instructions; 13 call(s) to 0x02008e0c, 0x02225fd4, 0x022180e0, +10 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 13 calls (82 instructions, 13 calls, 4 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x108
 *   branch +0x48 -> +0x8c
 *   branch +0x54 -> +0xf0
 *   back edge +0x84 -> +0x58
 *   branch +0x88 -> +0xf0
 *   branch +0xa4 -> +0xc4
 *   branch +0xb0 -> +0xc4
 *   back edge +0xc0 -> +0xa8
 *   branch +0xc8 -> +0xe4
 *   back edge +0xec -> +0x90
 *   back edge +0x114 -> +0x24
 *   branch +0x128 -> +0x13c
 *   test +0x2c cmp r0, #0
 *   test +0x44 cmp r0, #1
 *   test +0x50 cmp r0, #0
 *   test +0x6c tst r8, r0
 *   test +0x80 cmp r7, r0
 *   test +0x9c cmp r7, #0
 *   test +0xac cmp r0, r1
 *   test +0xb8 cmp r2, r7
 *   test +0xc4 cmp r2, r7
 *   test +0xd4 tst r8, r0
 *   test +0xe8 cmp r7, #6
 *   test +0xf8 cmp r0, #0
 *   test +0x10c cmp r6, #3
 *   test +0x124 cmp r4, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225ee4; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_022180e0(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02225ee4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #24
    mov r9, r1
    mov r8, r2
    add r1, sp, #0
    mov r2, #12
    mov r10, r0
    bl native_fn_02008e0c
    mov r6, #0
ov001_02225ee4_L24:
    add r0, sp, #0
    ldr r0, [r0, r6, lsl #2]
    cmp r0, #0
    beq ov001_02225ee4_L108
    add r5, sp, #12
    mov r7, #0
    str r7, [r5, r6, lsl #2]
    ldrb r0, [r9, #0x322]
    cmp r0, #1
    beq ov001_02225ee4_L8c
    ldrb r0, [r9, #0x323]
    cmp r0, #0
    ble ov001_02225ee4_Lf0
ov001_02225ee4_L58:
    add r0, r9, r7
    ldrb r0, [r0, #0x35e]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    add r7, r7, #1
    tst r8, r0
    ldrne r0, [r5, r6, lsl #2]
    addne r0, r0, #1
    strne r0, [r5, r6, lsl #2]
    ldrb r0, [r9, #0x323]
    cmp r7, r0
    blt ov001_02225ee4_L58
    b ov001_02225ee4_Lf0
ov001_02225ee4_L8c:
    mov r4, r7
ov001_02225ee4_L90:
    ldr r3, [r9, #0x1e8]
    mov r2, r4
    add r0, r3, r7
    cmp r7, #0
    ldrb r0, [r0, #0x8]
    ble ov001_02225ee4_Lc4
ov001_02225ee4_La8:
    ldrb r1, [r3, #0x8]
    cmp r0, r1
    beq ov001_02225ee4_Lc4
    add r2, r2, #1
    cmp r2, r7
    add r3, r3, #1
    blt ov001_02225ee4_La8
ov001_02225ee4_Lc4:
    cmp r2, r7
    blt ov001_02225ee4_Le4
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r8, r0
    ldrne r0, [r5, r6, lsl #2]
    addne r0, r0, #1
    strne r0, [r5, r6, lsl #2]
ov001_02225ee4_Le4:
    add r7, r7, #1
    cmp r7, #6
    blt ov001_02225ee4_L90
ov001_02225ee4_Lf0:
    add r0, sp, #12
    ldr r0, [r0, r6, lsl #2]
    cmp r0, #0
    addeq r0, sp, #0
    moveq r1, #0
    streq r1, [r0, r6, lsl #2]
ov001_02225ee4_L108:
    add r6, r6, #1
    cmp r6, #3
    add r9, r9, #1088
    blt ov001_02225ee4_L24
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225ee4_L13c
    add r0, sp, #0
    mov r1, r10
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225ee4_L13c:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
