/* ov001 row 0x02225d6c: 376 bytes.
 *
 * What it does: 94 instructions; 14 call(s) to 0x02008e0c, 0x02225e60, 0x0207b004, +11 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 14 calls (94 instructions, 14 calls, 5 branches, 10 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x104
 *   branch +0x4c -> +0x90
 *   branch +0x58 -> +0xf4
 *   back edge +0x88 -> +0x5c
 *   branch +0x8c -> +0xf4
 *   branch +0xa8 -> +0xc8
 *   branch +0xb4 -> +0xc8
 *   back edge +0xc4 -> +0xac
 *   branch +0xcc -> +0xe8
 *   back edge +0xf0 -> +0x94
 *   back edge +0x110 -> +0x28
 *   branch +0x12c -> +0x13c
 *   back edge +0x144 -> +0x124
 *   branch +0x158 -> +0x16c
 *   test +0x30 cmp r0, #0
 *   test +0x48 cmp r0, #1
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x84 cmp r8, r0
 *   test +0xa0 cmp r8, #0
 *   test +0xb0 cmp r0, r1
 *   test +0xbc cmp r2, r8
 *   test +0xc8 cmp r2, r8
 *   test +0xd8 cmp r0, #0
 *   test +0xec cmp r8, #6
 *   test +0xfc cmp r6, r0
 *   test +0x108 cmp r7, #3
 *   test +0x128 cmp r1, #0
 *   test +0x134 cmp r6, r1
 *   test +0x140 cmp r4, #3
 *   test +0x154 cmp r4, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225d6c; the literal pool and
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
extern void native_fn_0207b004(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02225d6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    mov r10, r1
    mov r9, r2
    add r1, sp, #0
    mov r2, #12
    mov r11, r0
    mov r6, #0
    bl native_fn_02008e0c
    mov r7, r6
ov001_02225d6c_L28:
    add r0, sp, #0
    ldr r0, [r0, r7, lsl #2]
    cmp r0, #0
    beq ov001_02225d6c_L104
    add r5, sp, #12
    mov r8, #0
    str r8, [r5, r7, lsl #2]
    ldrb r0, [r10, #0x322]
    cmp r0, #1
    beq ov001_02225d6c_L90
    ldrb r0, [r10, #0x323]
    cmp r0, #0
    ble ov001_02225d6c_Lf4
ov001_02225d6c_L5c:
    add r0, r10, r8
    ldrb r0, [r0, #0x35e]
    mov r1, r9
    bl native_fn_0207b004
    cmp r0, #0
    ldrne r0, [r5, r7, lsl #2]
    add r8, r8, #1
    addne r0, r0, #1
    strne r0, [r5, r7, lsl #2]
    ldrb r0, [r10, #0x323]
    cmp r8, r0
    blt ov001_02225d6c_L5c
    b ov001_02225d6c_Lf4
ov001_02225d6c_L90:
    mov r4, r8
ov001_02225d6c_L94:
    ldr r3, [r10, #0x1e8]
    mov r2, r4
    add r0, r3, r8
    cmp r8, #0
    ldrb r0, [r0, #0x8]
    ble ov001_02225d6c_Lc8
ov001_02225d6c_Lac:
    ldrb r1, [r3, #0x8]
    cmp r0, r1
    beq ov001_02225d6c_Lc8
    add r2, r2, #1
    cmp r2, r8
    add r3, r3, #1
    blt ov001_02225d6c_Lac
ov001_02225d6c_Lc8:
    cmp r2, r8
    blt ov001_02225d6c_Le8
    mov r1, r9
    bl native_fn_0207b004
    cmp r0, #0
    ldrne r0, [r5, r7, lsl #2]
    addne r0, r0, #1
    strne r0, [r5, r7, lsl #2]
ov001_02225d6c_Le8:
    add r8, r8, #1
    cmp r8, #6
    blt ov001_02225d6c_L94
ov001_02225d6c_Lf4:
    add r0, sp, #12
    ldr r0, [r0, r7, lsl #2]
    cmp r6, r0
    movlt r6, r0
ov001_02225d6c_L104:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_02225d6c_L28
    mov r4, #0
    mov r0, r4
    add r2, sp, #12
    add r3, sp, #0
ov001_02225d6c_L124:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_02225d6c_L13c
    ldr r1, [r2, r4, lsl #2]
    cmp r6, r1
    strgt r0, [r3, r4, lsl #2]
ov001_02225d6c_L13c:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_02225d6c_L124
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225d6c_L16c
    add r0, sp, #0
    mov r1, r11
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225d6c_L16c:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
