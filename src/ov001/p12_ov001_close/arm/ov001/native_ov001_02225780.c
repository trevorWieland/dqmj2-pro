/* ov001 row 0x02225780: 212 bytes.
 *
 * What it does: 52 instructions; 6 call(s) to 0x02008e0c, 0x022257ac, 0x022257fc, +3 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (52 instructions, 6 calls, 2 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0xd0 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x34 -> +0x5c
 *   back edge +0x68 -> +0x2c
 *   branch +0x84 -> +0x94
 *   back edge +0x9c -> +0x7c
 *   branch +0xb0 -> +0xc4
 *   test +0x30 cmp r0, #0
 *   test +0x44 cmp r2, r0
 *   test +0x54 cmp r0, r4
 *   test +0x60 cmp r12, #3
 *   test +0x80 cmp r1, #0
 *   test +0x8c cmp r1, r4
 *   test +0x98 cmp r5, #3
 *   test +0xac cmp r4, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225780; the literal pool and
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
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02225780 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #24
    mov r5, r1
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    ldr r4, =0x0000270f
    bl native_fn_02008e0c
    mov r12, #0
    add r1, sp, #12
    add r3, sp, #0
ov001_02225780_L2c:
    ldr r0, [r3, r12, lsl #2]
    cmp r0, #0
    beq ov001_02225780_L5c
    ldr r0, [r5, #0x1e8]
    ldrb r2, [r0, #0x8d]
    ldrb r0, [r0, #0x8e]
    cmp r2, r0
    strge r2, [r1, r12, lsl #2]
    strlt r0, [r1, r12, lsl #2]
    ldr r0, [r1, r12, lsl #2]
    cmp r0, r4
    movlt r4, r0
ov001_02225780_L5c:
    add r12, r12, #1
    cmp r12, #3
    add r5, r5, #1088
    blt ov001_02225780_L2c
    mov r5, #0
    mov r0, r5
    add r2, sp, #12
    add r3, sp, #0
ov001_02225780_L7c:
    ldr r1, [r3, r5, lsl #2]
    cmp r1, #0
    beq ov001_02225780_L94
    ldr r1, [r2, r5, lsl #2]
    cmp r1, r4
    strgt r0, [r3, r5, lsl #2]
ov001_02225780_L94:
    add r5, r5, #1
    cmp r5, #3
    blt ov001_02225780_L7c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225780_Lc4
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225780_Lc4:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, pc}
}
