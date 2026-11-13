/* ov001 row 0x022256a8: 216 bytes.
 *
 * What it does: 53 instructions; 6 call(s) to 0x02008e0c, 0x022256d4, 0x02225728, +3 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (53 instructions, 6 calls, 2 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0xd4 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x34 -> +0x60
 *   back edge +0x6c -> +0x2c
 *   branch +0x88 -> +0x98
 *   back edge +0xa0 -> +0x80
 *   branch +0xb4 -> +0xc8
 *   test +0x30 cmp r0, #0
 *   test +0x44 cmp r2, r0
 *   test +0x58 cmp r0, r4
 *   test +0x64 cmp r12, #3
 *   test +0x84 cmp r1, #0
 *   test +0x90 cmp r1, r4
 *   test +0x9c cmp r5, #3
 *   test +0xb0 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022256a8; the literal pool and
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


asm u32 native_ov001_022256a8 (register u32 a0)
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
ov001_022256a8_L2c:
    ldr r0, [r3, r12, lsl #2]
    cmp r0, #0
    beq ov001_022256a8_L60
    ldr r0, [r5, #0x1e8]
    ldrb r2, [r0, #0x8d]
    ldrb r0, [r0, #0x8e]
    cmp r2, r0
    addle r0, r0, r2, lsl #1
    addgt r0, r2, r0, lsl #1
    str r0, [r1, r12, lsl #2]
    ldr r0, [r1, r12, lsl #2]
    cmp r0, r4
    movlt r4, r0
ov001_022256a8_L60:
    add r12, r12, #1
    cmp r12, #3
    add r5, r5, #1088
    blt ov001_022256a8_L2c
    mov r5, #0
    mov r0, r5
    add r2, sp, #12
    add r3, sp, #0
ov001_022256a8_L80:
    ldr r1, [r3, r5, lsl #2]
    cmp r1, #0
    beq ov001_022256a8_L98
    ldr r1, [r2, r5, lsl #2]
    cmp r1, r4
    strgt r0, [r3, r5, lsl #2]
ov001_022256a8_L98:
    add r5, r5, #1
    cmp r5, #3
    blt ov001_022256a8_L80
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022256a8_Lc8
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_022256a8_Lc8:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, pc}
}
