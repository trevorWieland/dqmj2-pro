/* ov001 row 0x02224a88: 284 bytes.
 *
 * What it does: 70 instructions; 11 call(s) to 0x02008e0c, 0x02210ba8, 0x022244a0, +8 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (70 instructions, 11 calls, 4 branches, 10 back edges, 1 literal slot).
 *
 *   pool +0x118 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x3c -> +0xa4
 *   branch +0x50 -> +0x78
 *   branch +0x74 -> +0x98
 *   back edge +0xb0 -> +0x34
 *   branch +0xcc -> +0xdc
 *   back edge +0xe4 -> +0xc4
 *   branch +0xf8 -> +0x10c
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x9c cmp r0, r5
 *   test +0xa8 cmp r6, #3
 *   test +0xc8 cmp r1, #0
 *   test +0xd4 cmp r1, r5
 *   test +0xe0 cmp r4, #3
 *   test +0xf4 cmp r4, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224a88; the literal pool and
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
extern void native_fn_02210ba8(void);
extern void native_fn_022244a0(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224a88 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r7, r1
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    ldr r5, =0x0000270f
    bl native_fn_02008e0c
    mov r6, #0
    add r10, sp, #16
    mov r11, #5
    add r4, sp, #4
    mov r8, #30
ov001_02224a88_L34:
    ldr r0, [r4, r6, lsl #2]
    cmp r0, #0
    beq ov001_02224a88_La4
    mov r0, r7
    bl native_fn_02210ba8
    cmp r0, #0
    mov r0, r7
    bne ov001_02224a88_L78
    mov r1, r11
    bl native_fn_022244a0
    mov r9, r0
    mov r0, r7
    mov r1, #0
    bl native_fn_022244a0
    add r0, r9, r0, lsl #1
    str r0, [r10, r6, lsl #2]
    b ov001_02224a88_L98
ov001_02224a88_L78:
    mov r1, #5
    bl native_fn_022244a0
    mov r9, r0
    mov r0, r7
    mov r1, #0
    bl native_fn_022244a0
    mla r1, r0, r8, r9
    str r1, [r10, r6, lsl #2]
ov001_02224a88_L98:
    ldr r0, [r10, r6, lsl #2]
    cmp r0, r5
    movlt r5, r0
ov001_02224a88_La4:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02224a88_L34
    mov r4, #0
    mov r0, r4
    add r2, sp, #16
    add r3, sp, #4
ov001_02224a88_Lc4:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_02224a88_Ldc
    ldr r1, [r2, r4, lsl #2]
    cmp r1, r5
    strgt r0, [r3, r4, lsl #2]
ov001_02224a88_Ldc:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_02224a88_Lc4
    add r0, sp, #4
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224a88_L10c
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224a88_L10c:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
